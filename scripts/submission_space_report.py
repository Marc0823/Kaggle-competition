from __future__ import annotations

import hashlib
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "artifacts" / "submission_space_blends"
OUT_DIR.mkdir(parents=True, exist_ok=True)


CANDIDATES = {
    "sunny_best_7235": {
        "path": ROOT / "artifacts" / "sunny_physical_output" / "submission.csv",
        "score": 7.235,
    },
    "david_v12_7263": {
        "path": ROOT / "artifacts" / "david_v12_output" / "submission.csv",
        "score": 7.263,
    },
    "gold_fallback_7297": {
        "path": ROOT / "artifacts" / "emanuell_physics_output" / "submission.csv",
        "score": 7.297,
    },
    "fleongg_v5_report_7528": {
        "path": ROOT / "artifacts" / "fleongg_v5_output" / "submission.csv",
        "score": 7.528,
    },
    "ravaghi_hill_unknown": {
        "path": ROOT / "artifacts" / "ravaghi_hill_climbing_output" / "submission.csv",
        "score": np.nan,
    },
    "needless_sel15_unknown": {
        "path": ROOT / "artifacts" / "needless_sel15_vc_spread55_output" / "submission.csv",
        "score": np.nan,
    },
    "lightning_self_unknown": {
        "path": ROOT / "artifacts" / "lightning_self_verifying_output" / "submission.csv",
        "score": np.nan,
    },
    "henry_v10_unknown": {
        "path": ROOT / "artifacts" / "henry_tabicl_artifact_output" / "submission.csv",
        "score": np.nan,
    },
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def read_one(name: str, path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"{name}: {path}")
    df = pd.read_csv(path)
    if "tvt" not in df.columns:
        raise ValueError(f"{name} has no tvt column: {list(df.columns)}")
    df = df[["id", "tvt"]].copy()
    if len(df) != 14151:
        raise ValueError(f"{name} rows={len(df)}")
    if df["id"].duplicated().any():
        raise ValueError(f"{name} duplicate ids")
    df["tvt"] = df["tvt"].astype(float)
    if not np.isfinite(df["tvt"]).all():
        raise ValueError(f"{name} non-finite predictions")
    return df


def write_blend(name: str, base: pd.DataFrame, values: np.ndarray) -> Path:
    out = base.copy()
    out["tvt"] = np.round(values, 2)
    path = OUT_DIR / "submission.csv"
    named_path = OUT_DIR / f"submission_{name}.csv"
    out.to_csv(named_path, index=False)
    if name == "priority_sunny80_v10_20":
        out.to_csv(path, index=False)
    return named_path


def main() -> None:
    frames = {}
    audit = []
    ref_ids = None
    for name, meta in CANDIDATES.items():
        path = Path(meta["path"])
        if not path.exists():
            audit.append({"candidate": name, "status": "missing", "path": str(path)})
            continue
        df = read_one(name, path)
        if ref_ids is None:
            ref_ids = df["id"]
        if not df["id"].equals(ref_ids):
            audit.append({"candidate": name, "status": "id_mismatch", "path": str(path)})
            continue
        frames[name] = df
        audit.append(
            {
                "candidate": name,
                "status": "ok",
                "path": str(path),
                "score": meta["score"],
                "min": float(df["tvt"].min()),
                "max": float(df["tvt"].max()),
                "mean": float(df["tvt"].mean()),
                "std": float(df["tvt"].std()),
                "sha16": sha(path),
            }
        )

    names = list(frames)
    arr = np.column_stack([frames[n]["tvt"].to_numpy() for n in names])
    pair_rows = []
    for i, a in enumerate(names):
        for j, b in enumerate(names):
            if j <= i:
                continue
            da = arr[:, i] - arr[:, j]
            pair_rows.append(
                {
                    "a": a,
                    "b": b,
                    "rmsdiff": float(np.sqrt(np.mean(da * da))),
                    "meandiff_a_minus_b": float(da.mean()),
                    "corr": float(np.corrcoef(arr[:, i], arr[:, j])[0, 1]),
                }
            )

    base = frames["sunny_best_7235"]
    blends = []
    if "henry_v10_unknown" in frames:
        sunny = frames["sunny_best_7235"]["tvt"].to_numpy()
        v10 = frames["henry_v10_unknown"]["tvt"].to_numpy()
        for sw in [0.80, 0.70]:
            name = f"sunny{round(sw * 100):02d}_v10{round((1 - sw) * 100):02d}"
            path = write_blend(
                "priority_sunny80_v10_20" if sw == 0.80 else name,
                base,
                sw * sunny + (1.0 - sw) * v10,
            )
            diff = (sw * sunny + (1.0 - sw) * v10) - sunny
            blends.append(
                {
                    "candidate": name,
                    "path": str(path),
                    "rms_delta_vs_sunny": float(np.sqrt(np.mean(diff * diff))),
                    "mean_delta_vs_sunny": float(diff.mean()),
                    "reason": "Kojimar physical + v10 artifact stack blend",
                }
            )

    # Very conservative blend using only known-score branches. These are highly
    # correlated, so this is a backup candidate, not the sub-7 shot.
    known_branch_names = [
        n
        for n in ["sunny_best_7235", "david_v12_7263", "fleongg_v5_report_7528"]
        if n in frames
    ]
    if len(known_branch_names) == 3:
        weights = np.array([0.70, 0.20, 0.10], dtype=float)
        mat = np.column_stack([frames[n]["tvt"].to_numpy() for n in known_branch_names])
        values = mat @ weights
        path = write_blend("knownscore_70_20_10_backup", base, values)
        diff = values - frames["sunny_best_7235"]["tvt"].to_numpy()
        blends.append(
            {
                "candidate": "knownscore_70_20_10_backup",
                "path": str(path),
                "rms_delta_vs_sunny": float(np.sqrt(np.mean(diff * diff))),
                "mean_delta_vs_sunny": float(diff.mean()),
                "reason": "backup blend of known 7.x branches; expected small impact",
            }
        )

    pd.DataFrame(audit).to_csv(OUT_DIR / "candidate_audit.csv", index=False)
    pd.DataFrame(pair_rows).to_csv(OUT_DIR / "pairwise_submission_distance.csv", index=False)
    pd.DataFrame(blends).to_csv(OUT_DIR / "blend_candidates.csv", index=False)
    print(pd.DataFrame(audit).to_string(index=False))
    print()
    print(pd.DataFrame(blends).to_string(index=False))
    print(f"out_dir={OUT_DIR}")


if __name__ == "__main__":
    main()
