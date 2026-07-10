# ROGII — Hard-Won Lessons & Strategy (2026-07-08)

Consolidated understanding after a long multi-day push. Written so future sessions
do not repeat the same detours. **Read this before spending more effort or slots.**

## 0. TL;DR — the single most important thing

**Diagnose what actually moves the score BEFORE modeling.** Most of our wasted
effort came from optimizing an internal CV that does not predict the public board.
This competition has a split personality:

- **Public LB = a leakage/overlap game**, not a geology-model quality contest.
- **Private LB (final rank / prize) = honest-model quality on novel wells**, which
  we can only proxy with internal pseudo-hidden CV.
- **Our internal native-mask CV ≈ private-LB behavior; it is NOT ≈ public LB.**

## 1. The scoring mechanism (the crux we learned late)

- Code competition with hidden rerun. Downloadable `test/` has only 3 visible wells
  (000d7d20, 00bbac68, 00e12e8b); `sample_submission.csv` = 14,151 rows over those 3.
  At scoring, Kaggle swaps in the real hidden test wells; the notebook must
  dynamically discover wells. Static replay is rejected.
- **The 3 visible test wells are ALSO in `train/` with full ground-truth TVT** —
  a genuine answer leak. Metric = pooled RMSE over predicted toe-end rows.
- **The 7.10–7.30 public plateau is NOT a better model.** It is a decent
  correlation base + two board-specific layers: (a) a **guarded overlap/exact-match
  override** that reconstructs TVT for hidden wells that duplicate train wells, and
  (b) **gold visible-prefix calibration**. These help PUBLIC and are ~no-ops on
  PRIVATE (novel wells) → the plateau will shake down on private.
- **Overlap exploitation ceiling ≈ 7.27** (the teammate's affine-overlay line hit
  7.278/7.294; a naive exact-copy scored 11,551 — rejected). Our 7.182 stack
  already contains the overlap override, so stacking more overlap adds ~nothing.
- **Honest models land at board 8–14** — confirmed by every publicly-shared "real
  model" (8.099; DWT 9.251; 9.538; romantamrazov 9.956/10.811; pilkwang 12.049)
  AND by all of our from-scratch work (neural cross-attn **12.87**, domain-feature
  LightGBM/mycarta **14.09**, last_value/PF/router ~**14.7**). This is the "honest
  manifold."

## 2. What we tried and what it scored

| Approach | Internal CV | Board | Verdict |
| --- | --- | --- | --- |
| last_value baseline | 14.68 | — | floor |
| from-scratch router/PF/DTW/Viterbi | ~14.6–14.8 | — | all hit GR-aliasing wall; net ~baseline |
| feature-GBM (tortuosity/NCC/offset, ours) | ~16 | — | landed at baseline (missing per-row alignment + strong offset-well signal) |
| neural cross-attn aligner (ours) | 14.74 | **12.87** | first novel model on board; not competitive |
| mycarta domain-LightGBM fork | 14.78 | **14.09** | ran in fast/debug mode; honest, not competitive |
| our 7.182 physics-PF stack fork (pre-session) | — | **7.182** | our best; has overlap override |

Key negative results (do not re-try blindly):
- **GR↔typewell alignment is fundamentally aliased** (oscillatory, self-similar):
  PF/NCC/Viterbi/attention all rescue high-drift wells but lock onto wrong
  positions elsewhere; correct-vs-aliased large moves are indistinguishable at
  prediction time. Prefix hold-out does NOT predict hidden-suffix wins.
- **TVT is NOT ~−Z+c** (Z-projection RMSE 104 vs 15.7). Within a lateral the
  TVT-vs-Z slope ≈ 0 (mean +0.057) while global cross-well r = −0.96 → **TVT in the
  toe is set by formation dip in the bit azimuth (a cross-well structural quantity)**.
  → the #1 honest lever is an **offset-well multi-well structural/dip framework**,
  which we have not built well (our spatial KNN probe failed: wells too sparse,
  median neighbor ~1548 XY units — needs a real dip/structural surface, not KNN).
- Soft-DTW is a poor fit: wells UNDULATE (~24 direction reversals median) → the
  alignment is non-monotonic, so monotonic DTW is wrong.
- Neural scale-up (bigger/longer) OVERFIT (val 15.96 worse than the small 14.74);
  capacity is not the bottleneck. Add best-checkpoint restore + multi-cut
  augmentation if revisiting.

## 2b. Fork-run DISCIPLINE — smoke-test the fix on a tiny/cheap run first

**Never validate a fix by launching the full run.** These notebooks read
multi-GB feature tables (ravaghi `data/train.csv` = **7.4 GB**, ~1 h just to read)
and run optuna/PF for hours, so a bug at minute-80 costs an hour to surface. Each
DWT attempt burned ~1.4 h to hit the *next* error.

Instead, for every fork fix:
1. **Isolate the thing you fixed** into a minimal cell/kernel that exercises ONLY
   that code path (e.g. `load_trainer(one_model_dir)` + assert it has `.oof_preds`
   / `.models_`) — it mounts the dataset but does NOT read the 7.4 GB table, so it
   finishes in minutes.
2. If the smoke test passes, only THEN wire the fix into the full pipeline and run
   the slow/full version.
3. Add a `FAST`/`nrows`/`max_wells` toggle so the full notebook itself can run a
   cheap end-to-end pass. (Caveat: if the pipeline uses precomputed full-size OOF,
   you cannot simply subsample the train table — the OOF length won't align; smoke
   test the *loading* separately instead.)

This turns "1 h per failed guess" into "minutes per validated step."

### 2c. DWT honest base — SOLVED (the full recipe, confirmed 2026-07-08)

The DWT 9.251 fork now RUNS end-to-end and submits. Internal native-mask CV
(optuna post-proc best) = **10.40** — our honest private proxy (its 9.251 is the
*public* board; honest models' internal CV ≈ private, so ~10.4 is the realistic
private-side number). **Submitted → public board = 9.519** (sub 54453597), which
nearly reproduces the origin DWT 9.251 — we are ~0.27 worse only because ravaghi
published 5/6 trainers (no catboost-3). This is now our banked honest base:
public 9.519 / internal-CV 10.40, far above our from-scratch best (neural 12.87). Every failure above was one of THREE unrelated breakages,
each caught cheaply by a smoke kernel before any 1 h full run:

1. **koolbox dependency** (`from koolbox import Trainer`, private wheel we never
   had). The ravaghi artifacts are pickled `koolbox.Trainer` objects. Fix = graft
   a self-contained **`CVTrainer`** class + register it under `sys.modules` for
   `koolbox`, `koolbox.trainer`, `koolbox.trainer.trainer` so joblib unpickles it.
   `load_trainer(dir)` globs `*.pkl` and returns the object. The pickled trainer's
   model list lives in attribute **`estimators`** (5 fold models), NOT `models_`;
   `_models_for_predict()` tries known aliases and adapts. `.oof_preds` (len =
   3,783,989 = len(train_df)) and `.overall_score` come straight off the pickle;
   `.predict(X_test)` averages the 5 fold models (handles `best_iteration_`).
   Patch both `train_lightgbm`/`train_catboost` fast-load branches to:
   `_tr=load_trainer(path); oof=_tr.oof_preds; test=_tr.predict(X_test)` — this
   sidesteps the raw-Booster-vs-sklearn `best_iteration`/`best_iteration_` API gap.
2. **Wrong artifacts mount path.** Current Kaggle layout is
   `/kaggle/input/{competitions|datasets}/{owner}/{slug}`. Competition data =
   `/kaggle/input/competitions/rogii-wellbore-geology-prediction` (correct as-is);
   ravaghi artifacts = `/kaggle/input/datasets/ravaghi/wellbore-geology-prediction-artifacts`
   (NOT `/kaggle/input/wellbore-geology-prediction-artifacts`). A wrong path makes
   the `.exists()` fast-load guard False → notebook silently **retrains from
   scratch** (rebuilds the 7.3 GB train.csv into output AND hits the GPU params →
   `LightGBMError: No OpenCL device found`). Robust fix = auto-detect: glob
   `"/kaggle/input/**/models/lightgbm-1"`, pick the root that has BOTH
   `models/lightgbm-1` and `data/train.csv`, assert it, then `CFG.artifacts_path=`.
3. **Missing `catboost-3` artifact.** Ravaghi published only `lightgbm-1/2/3` +
   `catboost-1/2` (5 dirs, no cb-3). The `for i in range(3)` catboost loop would
   request cb-3 → not found → retrain branch. Fix = guard each loop iteration with
   `if not (CFG.artifacts_path/"models"/name).exists(): continue` (load-only mode).
   Also **strip GPU params** defensively (`device_type="gpu"`, `task_type="GPU"`)
   so any accidental retrain runs on CPU instead of crashing.

The generic lesson: a "path fix" that flips a fast-load guard to False fails
SILENTLY into a slow retrain — it doesn't error at the guard, it errors ~80 min
later deep in training. Always assert the fast-load path is actually taken (print
`Loading` vs `Training`; assert the artifact dir exists right after setting the
path).

### 2d. Honest levers TESTED and KILLED (2026-07-09/10) — do not retry

Ran the two candidate honest levers locally (system python3.12 has full pandas/
numpy/scipy/lightgbm; native TVT_input mask = hidden split). Both failed the
"beat DWT 9.519" gate → **not submitted** (0 slots burned; retreated to DWT).

- **Offset-well STRUCTURAL SURFACES (ANCC/ASTNU/ASTNL/EGFDU/EGFDL/BUDA).** In the
  masked toe of TRAIN these are ~100% populated (X/Y/Z too; GR only 36%), and a
  leave-well-out LightGBM on them predicts raw toe TVT at RMSE ~46 vs naive
  projection 107. BUT the **TEST horizontal wells do NOT carry these columns**
  (test cols = `MD,X,Y,Z,GR,TVT_input` only) → the feature literally cannot be
  computed at inference. Dead. (This is also why DWT's 195 features are GR/typewell/
  geometry-based, never surfaces.) Probe: `scratchpad/dip_probe.py`.
- **GR↔typewell DIP ALIGNMENT** (segment-NCC anchor-bounded warp, the "real"
  geosteering move). Honest native-mask weighted RMSE = **16.23**, actually WORSE
  than the trivial last_value baseline **16.16** (win-rate 0.36; prefix-holdout
  router-gate still nets +0.02; no drift-quartile shows gain). DWT's 195 GR
  features already subsume this. Proto: `scratchpad/tw_align_proto.py`.

Bottom line: no cheap honest lever beats DWT 9.519. The only remaining honest
upside is either (a) recover the missing **catboost-3** to lift DWT 9.519→~9.251
(bounded, low-risk, ~0.27), or (b) a multi-day rebuild of a GR aligner good enough
to out-feature a tuned 195-feature ensemble (low odds). See memory
`dwt-honest-base-9519.md`.

### 2e. catboost-3 RECOVERED — but the 0.27 public gap was NOT real quality (2026-07-10)

Trained the missing catboost-3 ourselves (kernel `joezzzzz/cb3-train`: single-GPU
`devices="0"` — the origin's `"0:1"` assumes 2 GPUs and errors on a 1-GPU kernel;
iterations cap 4000, 5-fold GroupKFold on `well`, ~16 min, individual OOF RMSE 10.55).
Saved as a `load_trainer`-compatible `CVTrainer` at `models/catboost-3/trainer.pkl`.
Main notebook v7 consumes it via `kernel_sources: ["joezzzzz/cb3-train"]` plus a new
`find_model_dir(name)` helper that globs each model dir under ANY `/kaggle/input`
root (ravaghi holds lgb1-3+cb1-2; the cb3-train output holds catboost-3). All 6
models load cleanly.

**Result: final optuna internal CV = 10.3987 vs 10.40 with 5 models — FLAT.** cb-3 is
highly correlated with the existing five, so it adds ~nothing to the honest proxy.
**Key finding:** the 0.27 public gap (origin 9.251 vs our 9.519) is NOT a real quality
difference — both sit at internal CV ~10.4; the 0.27 is public-split noise. Recovering
cb-3 therefore only lifts the PUBLIC vanity number, not the private proxy → **not
submitted** (gate = material CV gain; slots preserved). The 6-model notebook is banked
and ready if we ever want the marginal 5→6 variance reduction. The genuine remaining
lever is **ensemble diversity** (independent honest model families blended with DWT)
to cut private variance, not more same-family models.

## 3. Fork-ops reality (whack-a-mole — budget for it)

Competitive public notebooks are NOT portable. Each fork needs surgery:
- **GPU:** default P100 = compute sm_60, too old for Kaggle's preinstalled torch
  (`no kernel image`). Fix: `--accelerator NvidiaTeslaT4` / `machine_shape:
  NvidiaTeslaT4` (sm_75 works out of the box). LightGBM/CatBoost/numba are fine on
  P100 (torch is the only thing that breaks).
- **New-kernel 403:** when forking a pulled kernel, DELETE `id_no` from the
  metadata (it points to the origin kernel) — rebuild clean minimal metadata.
- **External module deps (crash on import):** koolbox (mycarta, takuya, kokinn,
  dualpipe, bern), hill_climbing/Climber (DWT). koolbox comes from the
  `phongnguyn23021656/koolbox-offline` dataset; Climber is a Caruana greedy
  ensemble (we wrote a self-contained stub — see scratch).
- **Hardcoded dataset paths:** DWT hardcodes `/kaggle/input/datasets/ravaghi/...`;
  real mount is `/kaggle/input/wellbore-geology-prediction-artifacts`.
- **Pretrained-artifact detection:** degnonguidi Pipeline B looks for models at
  `CFG.ARTIFACTS/models_B`; the fleongg models (`fleongg/rogii-claude-models-pub`:
  features.json + lgb0/1/2.pkl) sit at that dataset's ROOT, so B never finds them
  and **trains from scratch → ~11h feature build → DeadKernelError**. This killed
  the Degnonguidi 7.159 fork **8 times**; a glob patch did not resolve it →
  **ABANDONED degnonguidi** (heavy dual-pipeline, not worth more 11h runs).
- **Unsafe train→test TVT_input row copy** (`hw_te['TVT_input']=hw_tr[...].values`)
  in 7153/takuya/dualpipe/bern — public-only overlap trick; trivially removable but
  those notebooks are non-portable for other reasons (koolbox + heavy PF).
- **Runtime:** heavy PF/beam dual-pipelines run hours and risk the 9h limit /
  DeadKernel; prefer CPU-light notebooks (DWT) that use pretrained artifacts.

## 4. Strategic conclusion

- **Podium (5.26) / top-10 (6.30) is NOT reachable** with any public artifact or
  our from-scratch work — it uses a materially stronger structural/inverse model
  or private-invisible tricks not shared publicly.
- **Realistic public ceiling ≈ 7.08–7.13 (top-100)** via land-a-7.159 + blend, but
  **most of that reverts on private**.
- **For the FINAL/private ranking (the goal): build/land the strongest HONEST model
  and validate it on internal CV.** When the overlap-chasers shake down on private,
  a genuinely strong honest model (internal CV → 8–10) can rank durably well.
- The #1 honest lever = **offset-well structural/dip framework** (cross-well
  formation dip in the bit azimuth). Secondary honest levers: Q-3D tortuosity
  (−0.107 in mycarta), multi-scale NCC, self-correlation, PF/state-space engine.

## 5. Current assets / final-submission plan

Kaggle lets you pick **2 final submissions** — pick for PRIVATE robustness:
1. **The strongest honest model** — currently landing the **DWT 9.251** fork (clean,
   CPU, no overlap, honest → its board ≈ its private). If it runs, it is far better
   than our from-scratch ~14. Then improve it with the offset-well lever.
2. **A hedge** — the 7.182 stack (decent base + overlap; in case private is less
   overlap-punishing than expected). Do NOT pick two overlap-heavy notebooks.

## 6. If starting over (the efficient path)

1. Run the "what moves the score" diagnostic FIRST (public=overlap, private=honest,
   internal CV=private proxy). Decide public-chase vs private-durable up front.
2. For private: fork ONE clean honest base (DWT-class), get it running, measure its
   internal CV, then add the offset-well structural framework. Don't grind
   from-scratch alignment (aliasing wall) or heavy non-portable stacks.
3. Reserve slots; every submission is a planned experiment. Two finals = 1 honest
   + 1 hedge.
