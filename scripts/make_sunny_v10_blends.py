from __future__ import annotations

import hashlib
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "artifacts" / "sunny_v10_blend_candidates"
SUNNY_PATH = ROOT / "artifacts" / "sunny_physical_output" / "submission.csv"
V10_PATH = ROOT / "artifacts" / "henry_tabicl_artifact_output" / "submission.csv"


def sha256_prefix(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def read_submission(path: Path, name: str) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"{name} missing: {path}")
    df = pd.read_csv(path)
    if list(df.columns) != ["id", "tvt"]:
        raise ValueError(f"{name} has unexpected columns: {list(df.columns)}")
    if len(df) != 14151:
        raise ValueError(f"{name} row count {len(df)} != 14151")
    if df["id"].duplicated().any():
        raise ValueError(f"{name} has duplicate ids")
    values = df["tvt"].astype(float).to_numpy()
    if not np.isfinite(values).all():
        raise ValueError(f"{name} has NaN or inf")
    return df


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    sunny = read_submission(SUNNY_PATH, "sunny")
    v10 = read_submission(V10_PATH, "v10")
    if not sunny["id"].equals(v10["id"]):
        raise ValueError("sunny and v10 id order mismatch")

    report_rows = []
    for sunny_weight in [0.80, 0.70]:
        v10_weight = 1.0 - sunny_weight
        blended = sunny.copy()
        blended["tvt"] = (
            sunny_weight * sunny["tvt"].astype(float) + v10_weight * v10["tvt"].astype(float)
        ).round(2)
        tag = f"sunny{round(sunny_weight * 100):02d}_v10{round(v10_weight * 100):02d}"
        out_path = OUT_DIR / f"submission_{tag}.csv"
        blended.to_csv(out_path, index=False)
        diff = blended["tvt"].to_numpy() - sunny["tvt"].to_numpy()
        report_rows.append(
            {
                "candidate": tag,
                "path": str(out_path),
                "rows": len(blended),
                "id_order_matches_sunny": bool(blended["id"].equals(sunny["id"])),
                "nulls": int(blended["tvt"].isna().sum()),
                "min_tvt": float(blended["tvt"].min()),
                "max_tvt": float(blended["tvt"].max()),
                "mean_tvt": float(blended["tvt"].mean()),
                "std_tvt": float(blended["tvt"].std()),
                "rms_delta_vs_sunny": float(np.sqrt(np.mean(diff * diff))),
                "mean_delta_vs_sunny": float(diff.mean()),
                "sha256_prefix": sha256_prefix(out_path),
            }
        )

    report = pd.DataFrame(report_rows)
    report_path = OUT_DIR / "sunny_v10_blend_audit.csv"
    report.to_csv(report_path, index=False)
    print(report.to_string(index=False))
    print(f"audit={report_path}")


if __name__ == "__main__":
    main()
