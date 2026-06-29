
import warnings; warnings.filterwarnings('ignore')
import subprocess  # needed for kaggle CLI fallback download
# All packages are pre-installed on Kaggle GPU kernels — no pip install needed.
# (internet disabled; pip installs were causing CUDA library conflicts)

import os, json, time
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.model_selection import GroupKFold
from sklearn.metrics import root_mean_squared_error
import lightgbm as lgb
import xgboost as xgb
from catboost import CatBoostRegressor

# ── Inline hill-climbing blend optimizer (replaces pip package) ───────────────
class _HillClimber:
    """Greedy hill-climbing ensemble weight optimizer."""
    def __init__(self, precision=0.001, n_rounds=200, allow_negative=True):
        self.precision = precision
        self.n_rounds = n_rounds
        self.allow_negative = allow_negative
        self.weights_ = None

    def fit(self, X, y):
        X = np.asarray(X, np.float32); y = np.asarray(y, np.float32)
        n = X.shape[1]
        w = np.ones(n) / n
        def rmse(w_): return float(np.sqrt(np.mean((X @ w_ - y) ** 2)))
        best = rmse(w)
        for _ in range(self.n_rounds):
            improved = False
            for i in range(n):
                for sign in (1, -1):
                    w2 = w.copy(); w2[i] += sign * self.precision
                    if not self.allow_negative: w2 = np.clip(w2, 0, None)
                    s = rmse(w2)
                    if s < best - 1e-8:
                        best, w, improved = s, w2, True
            if not improved:
                break
        self.weights_ = w
        return self

    def predict(self, X):
        return np.asarray(X, np.float32) @ self.weights_

    @property
    def weights(self): return self.weights_

t0 = time.time()

# ── Load pre-computed features ──────────────────────────────────────────────
COMP_DIR = Path('/kaggle/input/competitions/rogii-wellbore-geology-prediction')
FEAT_DIR = Path('/kaggle/input/notebooks/hongweiluan/rogii-wellbore-v11-feat-script')

# Try multiple mount paths (Kaggle uses different paths by version)
_SLUG = 'rogii-wellbore-v11-feat-script'
for _candidate in [
    Path(f'/kaggle/input/notebooks/hongweiluan/{_SLUG}'),
    Path(f'/kaggle/input/{_SLUG}'),
]:
    if (_candidate / 'train_features.parquet').exists():
        FEAT_DIR = _candidate; break
else:
    raise FileNotFoundError(f'v10 feat-script not mounted. Check kernel_sources.')

print('Loading pre-computed train features...', flush=True)
train_df = pd.read_parquet(FEAT_DIR / 'train_features.parquet')
feat_cols = json.loads(open(FEAT_DIR / 'feat_cols.json').read())
feat_cols = [c for c in feat_cols if c in train_df.columns]
print(f'Train: {train_df.shape}, Features: {len(feat_cols)}', flush=True)
print(f'Loaded in {time.time()-t0:.1f}s', flush=True)

# ── Prepare arrays ──────────────────────────────────────────────────────────
X_np  = np.nan_to_num(train_df[feat_cols].values.astype(np.float32), nan=0., posinf=0., neginf=0.)
y_np  = train_df['target'].values.astype(np.float32)
g_arr = train_df['well'].values

N_SPLITS = 5
cv = GroupKFold(n_splits=N_SPLITS)

# ── LGBM models with GPU (bimodal hedge architecture) ────────────────────────
# Model 1: fast GPU — num_leaves=255, standard regularisation
# Models 2-3: Optuna-tuned (heavy regularisation, small leaves, slow lr)
# Models 4-5: diverse seeds on standard config
lgb_configs = [
    # Standard fast config (notebook model 1)
    dict(num_leaves=255, min_child_samples=15, subsample=0.8, subsample_freq=1,
         colsample_bytree=0.8, reg_lambda=3.0, reg_alpha=0.05,
         learning_rate=0.030, n_estimators=5000, seed=123,
         max_bin=255, gpu_use_dp=False),
    # Optuna-tuned — high regularisation, small leaves (notebook models 2-3)
    dict(num_leaves=64, min_child_samples=40, subsample=0.474, subsample_freq=1,
         colsample_bytree=0.393, reg_lambda=95.754, reg_alpha=10.788,
         learning_rate=0.00934, n_estimators=10000, seed=0),
    dict(num_leaves=64, min_child_samples=40, subsample=0.474, subsample_freq=1,
         colsample_bytree=0.393, reg_lambda=95.754, reg_alpha=10.788,
         learning_rate=0.00934, n_estimators=10000, seed=29),
    # Additional diversity
    dict(num_leaves=255, min_child_samples=15, subsample=0.8, subsample_freq=1,
         colsample_bytree=0.8, reg_lambda=3.0, reg_alpha=0.05,
         learning_rate=0.022, n_estimators=8000, seed=17),
    dict(num_leaves=255, min_child_samples=15, subsample=0.8, subsample_freq=1,
         colsample_bytree=0.8, reg_lambda=3.0, reg_alpha=0.05,
         learning_rate=0.025, n_estimators=8000, seed=42),
]
lgb_base = dict(
    boosting_type='gbdt', objective='regression', metric='rmse',
    verbose=-1, n_jobs=-1, device='gpu',
)

lgb_oof_list = []
_lgbm_fold_models = []  # [config][fold]

for mi, cfg in enumerate(lgb_configs):
    params = {**lgb_base, **cfg}
    oof = np.zeros(len(y_np), np.float32)
    fold_models = []
    for fold, (tr, va) in enumerate(cv.split(X_np, y_np, g_arr)):
        m = lgb.LGBMRegressor(**params)
        m.fit(X_np[tr], y_np[tr],
              eval_set=[(X_np[va], y_np[va])],
              callbacks=[lgb.early_stopping(100, verbose=False)])
        oof[va] = m.predict(X_np[va]).astype(np.float32)
        fold_models.append(m)
    lgb_oof_list.append(oof)
    _lgbm_fold_models.append(fold_models)
    rmse = float(np.sqrt(np.mean((oof - y_np)**2)))
    print(f'  LGBM {mi+1}/{len(lgb_configs)} OOF RMSE: {rmse:.4f}', flush=True)

lgbm_oof_ens = np.stack(lgb_oof_list, axis=1).mean(1)
print(f'LGBM ensemble OOF: {float(np.sqrt(np.mean((lgbm_oof_ens - y_np)**2))):.4f}', flush=True)

# ── XGBoost with GPU ─────────────────────────────────────────────────────────
xgb_params = dict(
    max_depth=7, learning_rate=0.02, n_estimators=6000,
    subsample=0.8, colsample_bytree=0.8, reg_lambda=3.0,
    objective='reg:squarederror', random_state=42,
    tree_method='hist', device='cuda',
    n_jobs=1, early_stopping_rounds=100,
)
xgb_oof = np.zeros(len(y_np), np.float32)
_xgb_fold_models = []
for fold, (tr, va) in enumerate(cv.split(X_np, y_np, g_arr)):
    m = xgb.XGBRegressor(**xgb_params)
    m.fit(X_np[tr], y_np[tr], eval_set=[(X_np[va], y_np[va])], verbose=False)
    xgb_oof[va] = m.predict(X_np[va]).astype(np.float32)
    _xgb_fold_models.append(m)
print(f'XGB OOF: {float(np.sqrt(np.mean((xgb_oof - y_np)**2))):.4f}', flush=True)

# ── CatBoost with GPU (exact bimodal notebook params) ────────────────────────
cb_configs = [
    dict(iterations=8000, learning_rate=0.020, depth=7, random_seed=7),
    dict(iterations=8000, learning_rate=0.030, depth=7, random_seed=123),
]
cb_base = dict(
    loss_function='RMSE', eval_metric='RMSE',
    l2_leaf_reg=2.0, min_data_in_leaf=15, border_count=254,
    task_type='GPU', verbose=0,
    od_type='Iter', od_wait=300,
)
cb_oof_list = []
_cb_fold_models = []  # [config][fold]
for mi, cfg in enumerate(cb_configs):
    params = {**cb_base, **cfg}
    oof = np.zeros(len(y_np), np.float32)
    fold_models = []
    for fold, (tr, va) in enumerate(cv.split(X_np, y_np, g_arr)):
        m = CatBoostRegressor(**params)
        m.fit(X_np[tr], y_np[tr], eval_set=[(X_np[va], y_np[va])], use_best_model=True)
        oof[va] = m.predict(X_np[va]).astype(np.float32)
        fold_models.append(m)
    cb_oof_list.append(oof)
    _cb_fold_models.append(fold_models)
    print(f'  CatBoost {mi+1}/{len(cb_configs)} OOF RMSE: {float(np.sqrt(np.mean((oof - y_np)**2))):.4f}', flush=True)

# ── 1D-CNN Sequence Model ────────────────────────────────────────────────────
CNN_EPOCHS = 20
cnn_oof = np.zeros(len(y_np), np.float32)
try:
    import torch
    import torch.nn as nn
    from torch.utils.data import DataLoader, TensorDataset

    TRAIN_DIR = Path('/kaggle/input/competitions/rogii-wellbore-geology-prediction/train')
    WINDOW = 40  # half-window; full window = 2*WINDOW+1 = 81

    class WellCNN(nn.Module):
        def __init__(self):
            super().__init__()
            self.net = nn.Sequential(
                nn.Conv1d(3, 32, 7, padding=3), nn.BatchNorm1d(32), nn.GELU(),
                nn.Conv1d(32, 64, 5, padding=2), nn.BatchNorm1d(64), nn.GELU(),
                nn.Conv1d(64, 64, 3, padding=1), nn.BatchNorm1d(64), nn.GELU(),
            )
            self.head = nn.Sequential(
                nn.Linear(64, 32), nn.GELU(), nn.Linear(32, 1)
            )
        def forward(self, x):
            h = self.net(x)          # (B, 64, W)
            c = h[:, :, WINDOW]      # center token (index 40)
            return self.head(c).squeeze(-1)

    # Test GPU compatibility — skip CNN entirely if GPU not usable
    # (CPU training of 3.78M windows × 20 epochs takes ~5h and gets OOM-killed)
    device = torch.device('cpu')
    if torch.cuda.is_available():
        try:
            _t = torch.zeros(2, 3, 81).cuda()
            _m = torch.nn.Conv1d(3, 4, 3, padding=1).cuda()
            _ = _m(_t)
            device = torch.device('cuda')
            del _t, _m
        except Exception as _cuda_err:
            raise RuntimeError(f'GPU incompatible ({_cuda_err}); skipping CNN to avoid CPU timeout')
    else:
        raise RuntimeError('No CUDA GPU available; skipping CNN')
    print(f'CNN device: {device}', flush=True)

    # Build per-well windows aligned with train_df rows
    # train_df rows are sorted by (well, MD order from CSV); unknown-TVT = NaN TVT_input
    print('Building CNN windows from raw CSVs...', flush=True)
    win_X_list = []  # (N_unk, 3, 81) float32
    win_y_list = []  # (N_unk,) float32 — delta TVT target
    win_idx_list = []  # row indices into train_df

    for wid in train_df['well'].unique():
        csv_path = TRAIN_DIR / f'{wid}__horizontal_well.csv'
        if not csv_path.exists():
            continue
        raw = pd.read_csv(csv_path)
        # Align: take rows where TVT_input is NaN (unknown positions)
        unknown_mask = raw['TVT_input'].isna()
        n_rows = len(raw)
        # Normalize GR, ANCC, Z per-well
        sigs = raw[['GR', 'ANCC', 'Z']].values.astype(np.float32)
        for ch in range(3):
            mu, sd = sigs[:, ch].mean(), sigs[:, ch].std() + 1e-6
            sigs[:, ch] = (sigs[:, ch] - mu) / sd
        # Pad with edge values
        padded = np.pad(sigs, ((WINDOW, WINDOW), (0, 0)), mode='edge')  # (n+2W, 3)
        # Get train_df rows for this well (in order)
        wdf = train_df[train_df['well'] == wid]
        # unknown positions = rows where TVT_input is NaN in raw CSV
        unk_raw_indices = np.where(unknown_mask.values)[0]
        # Match to train_df indices (wdf is aligned to unknown rows)
        if len(unk_raw_indices) != len(wdf):
            # Fallback: use first len(wdf) unknown indices
            unk_raw_indices = unk_raw_indices[:len(wdf)]
        for i_wdf, i_raw in zip(wdf.index, unk_raw_indices):
            win = padded[i_raw: i_raw + 2*WINDOW + 1, :].T  # (3, 81)
            win_X_list.append(win)
            win_y_list.append(train_df.loc[i_wdf, 'target'])
            win_idx_list.append(i_wdf)

    if len(win_X_list) == 0:
        raise RuntimeError('No CNN windows built (raw CSVs missing?)')

    win_X = np.stack(win_X_list)  # (N, 3, 81)
    win_y = np.array(win_y_list, dtype=np.float32)
    win_idx = np.array(win_idx_list)

    # Map train_df row index → position in win arrays
    idx_to_pos = {idx: pos for pos, idx in enumerate(win_idx)}

    print(f'CNN windows: {win_X.shape}, targets: {win_y.shape}', flush=True)

    # 5-fold GroupKFold matching GBM folds (same g_arr)
    cnn_fold_models = []
    for fold, (tr_rows, va_rows) in enumerate(cv.split(X_np, y_np, g_arr)):
        # Filter to rows that have CNN windows
        tr_cnn = [r for r in tr_rows if r in idx_to_pos]
        va_cnn = [r for r in va_rows if r in idx_to_pos]
        if not tr_cnn or not va_cnn:
            cnn_fold_models.append(None)
            continue

        tr_pos = [idx_to_pos[r] for r in tr_cnn]
        va_pos = [idx_to_pos[r] for r in va_cnn]

        X_tr = torch.tensor(win_X[tr_pos], dtype=torch.float32)
        y_tr = torch.tensor(win_y[tr_pos], dtype=torch.float32)
        X_va = torch.tensor(win_X[va_pos], dtype=torch.float32)
        y_va = torch.tensor(win_y[va_pos], dtype=torch.float32)

        ds_tr = TensorDataset(X_tr, y_tr)
        dl_tr = DataLoader(ds_tr, batch_size=512, shuffle=True)

        model = WellCNN().to(device)
        optimizer = torch.optim.Adam(model.parameters(), lr=3e-4)
        scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=CNN_EPOCHS)
        loss_fn = nn.MSELoss()

        for epoch in range(CNN_EPOCHS):
            model.train()
            for xb, yb in dl_tr:
                xb, yb = xb.to(device), yb.to(device)
                optimizer.zero_grad()
                loss_fn(model(xb), yb).backward()
                optimizer.step()
            scheduler.step()

        model.eval()
        with torch.no_grad():
            X_va_d = X_va.to(device)
            va_pred = model(X_va_d).cpu().numpy().astype(np.float32)

        va_rmse = float(np.sqrt(np.mean((va_pred - win_y[va_pos])**2)))
        print(f'  CNN fold {fold} val RMSE: {va_rmse:.4f}', flush=True)

        # Fill OOF
        for r, pos in zip(va_cnn, va_pos):
            cnn_oof[r] = va_pred[va_pos.index(pos)]

        # Save fold model
        torch.save(model.state_dict(), f'{MODEL_DIR}/cnn_fold{fold}.pt')
        cnn_fold_models.append(model)

    cnn_rmse = float(np.sqrt(np.mean((cnn_oof[win_idx] - win_y)**2)))
    print(f'CNN OOF RMSE: {cnn_rmse:.4f}', flush=True)

except Exception as e:
    print(f'CNN failed: {e}', flush=True)
    cnn_oof = np.zeros(len(y_np), np.float32)

# ── Positive Ridge meta-learner (bimodal notebook architecture) ───────────────
# Train Ridge(alpha=1.66, positive=True) on per-model OOF predictions.
# positive=True enforces non-negative ensemble weights (no model shorting).
from sklearn.linear_model import Ridge as _Ridge
from sklearn.model_selection import cross_val_predict as _cvp

all_oof_stack = np.stack(lgb_oof_list + [xgb_oof] + cb_oof_list, axis=1)
n_lgbm = len(lgb_oof_list); n_xgb = 1; n_cb = len(cb_oof_list)

ridge_meta = _Ridge(alpha=1.6602834637650032, positive=True,
                    tol=0.0005030247295617308, fit_intercept=True, random_state=42)
try:
    from sklearn.model_selection import GroupKFold as _GKF
    ridge_oof = _cvp(ridge_meta, all_oof_stack, y_np,
                     cv=_GKF(n_splits=5).split(all_oof_stack, y_np, g_arr),
                     n_jobs=-1)
    ridge_meta.fit(all_oof_stack, y_np)
    blend_w = list(ridge_meta.coef_)
    ens_oof_gbm = ridge_oof.astype(np.float32)
    print(f'Positive Ridge OOF: {float(np.sqrt(np.mean((ens_oof_gbm - y_np)**2))):.4f}', flush=True)
    print(f'Ridge weights: {[f"{w:.4f}" for w in blend_w]}', flush=True)
except Exception as e:
    print(f'Positive Ridge failed ({e}), falling back to Hill Climbing...', flush=True)
    try:
        climber = _HillClimber(eval_metric=root_mean_squared_error,
                               allow_negative_weights=True, precision=0.001,
                               score_decimal_places=4, n_jobs=-1)
        climber.fit(pd.DataFrame(all_oof_stack), pd.Series(y_np))
        ens_oof_gbm = climber.predict(pd.DataFrame(all_oof_stack)).astype(np.float32)
        blend_w = list(climber.weights)
        print(f'Hill Climbing OOF: {float(np.sqrt(np.mean((ens_oof_gbm - y_np)**2))):.4f}', flush=True)
    except Exception as e2:
        print(f'Hill climbing also failed ({e2}), using fixed blend', flush=True)
        cb_oof_ens = np.stack(cb_oof_list, axis=1).mean(1)
        ens_oof_gbm = (0.55*lgbm_oof_ens + 0.20*xgb_oof + 0.25*cb_oof_ens).astype(np.float32)
        blend_w = [0.55/n_lgbm]*n_lgbm + [0.20] + [0.25/n_cb]*n_cb
        print(f'Fixed blend OOF: {float(np.sqrt(np.mean((ens_oof_gbm - y_np)**2))):.4f}', flush=True)

# Blend GBM ensemble with CNN OOF
# ── CNN quality gate: only blend if CNN meaningfully improves OOF ─────────────
gbm_rmse = float(np.sqrt(np.mean((ens_oof_gbm - y_np)**2)))
cnn_full_rmse = float(np.sqrt(np.mean((cnn_oof - y_np)**2)))
if cnn_full_rmse < gbm_rmse * 0.99 and cnn_oof.any():
    cnn_weight = 0.15
    ens_oof = (0.85 * ens_oof_gbm + cnn_weight * cnn_oof).astype(np.float32)
    print(f'CNN gate PASSED (CNN {cnn_full_rmse:.4f} < GBM {gbm_rmse:.4f}): blending at {cnn_weight:.0%}', flush=True)
else:
    cnn_weight = 0.0
    ens_oof = ens_oof_gbm.copy()
    print(f'CNN gate FAILED (CNN {cnn_full_rmse:.4f} >= GBM {gbm_rmse:.4f}): using GBM-only', flush=True)
print(f'Final blend OOF: {float(np.sqrt(np.mean((ens_oof - y_np)**2))):.4f}', flush=True)

# ── Save models + OOF meta for inference kernel ──────────────────────────────
import os as _os
MODEL_DIR = '/kaggle/working/models'
_os.makedirs(MODEL_DIR, exist_ok=True)

# Save LGBM models (fold-level)
for mi, fold_models_list in enumerate(_lgbm_fold_models):
    for fold, m in enumerate(fold_models_list):
        m.booster_.save_model(f'{MODEL_DIR}/lgbm_{mi}_fold{fold}.txt')

# Save XGB models
for fold, m in enumerate(_xgb_fold_models):
    m.get_booster().save_model(f'{MODEL_DIR}/xgb_fold{fold}.json')

# Save CatBoost models
for mi, fold_models_list in enumerate(_cb_fold_models):
    for fold, m in enumerate(fold_models_list):
        m.save_model(f'{MODEL_DIR}/cb_{mi}_fold{fold}.cbm')

# Save feature columns and blend weights
json.dump(feat_cols, open(f'{MODEL_DIR}/feat_cols.json', 'w'))

try:
    w = climber.weights
    blend_w = list(w) if hasattr(w, '__len__') else None
    if blend_w is None or len(blend_w) != all_oof_stack.shape[1]:
        raise ValueError(f'HC weights invalid: {w}')
except:
    n_lgbm = len(lgb_oof_list); n_xgb = 1; n_cb = len(cb_oof_list)
    blend_w = [0.55/n_lgbm]*n_lgbm + [0.20] + [0.25/n_cb]*n_cb
json.dump({'weights': blend_w, 'n_lgbm': n_lgbm, 'n_xgb': 1, 'n_cb': n_cb,
           'cnn_weight': cnn_weight},
          open(f'{MODEL_DIR}/blend_weights.json', 'w'))

# Save OOF meta for PP fitting + per-model OOF for Ridge stacking in inference
pf_oof  = train_df['pf_ancc'].values - train_df['last_known_tvt'].values
form_cols = [c for c in train_df.columns if c.startswith('tvtF_') and not c.startswith('tvtFw') and not c.startswith('tvtF5')]
form_oof  = train_df[form_cols].mean(1).values - train_df['last_known_tvt'].values if form_cols else pf_oof

oof_meta_dict = {
    'well': train_df['well'].values, 'target': y_np,
    'last_known_tvt': train_df['last_known_tvt'].values,
    'pf_ancc_d': pf_oof.astype(np.float32),
    'form_d': form_oof.astype(np.float32),
    'md_since': train_df['md_since'].values,
    'ens_oof': ens_oof,
}
# Save per-model OOF for positive Ridge meta-learner in inference
for mi, oof_col in enumerate(lgb_oof_list):
    oof_meta_dict[f'lgb_{mi}_oof'] = oof_col.astype(np.float32)
oof_meta_dict['xgb_oof'] = xgb_oof.astype(np.float32)
for mi, oof_col in enumerate(cb_oof_list):
    oof_meta_dict[f'cb_{mi}_oof'] = oof_col.astype(np.float32)

pd.DataFrame(oof_meta_dict).to_parquet('/kaggle/working/oof_meta.parquet', index=False)

print(f'Total time: {time.time()-t0:.1f}s', flush=True)
print(f'Training complete: models saved', flush=True)
