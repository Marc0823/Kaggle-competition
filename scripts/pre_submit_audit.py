#!/usr/bin/env python3
"""Pre-submit checks for ROGII submission.csv files."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fail(errors: list[str], msg: str) -> None:
    errors.append(msg)


def audit(submission_path: Path, sample_path: Path | None = None) -> dict:
    errors: list[str] = []
    warnings: list[str] = []

    if not submission_path.is_file():
        raise FileNotFoundError(f"submission not found: {submission_path}")

    sub = pd.read_csv(submission_path)
    if list(sub.columns) != ["id", "tvt"]:
        fail(errors, f"columns must be exactly ['id', 'tvt']; got {list(sub.columns)}")

    if "id" not in sub.columns:
        fail(errors, "missing id column")
    if "tvt" not in sub.columns:
        fail(errors, "missing tvt column")

    if "id" in sub.columns:
        sub["id"] = sub["id"].astype(str)
        duplicated = int(sub["id"].duplicated().sum())
        if duplicated:
            fail(errors, f"duplicate ids: {duplicated}")

    tvt_stats = {}
    if "tvt" in sub.columns:
        tvt = pd.to_numeric(sub["tvt"], errors="coerce").to_numpy(dtype=float)
        finite = np.isfinite(tvt)
        non_finite = int((~finite).sum())
        if non_finite:
            fail(errors, f"non-finite tvt values: {non_finite}")
        if len(tvt):
            tvt_stats = {
                "tvt_min": float(np.nanmin(tvt)),
                "tvt_max": float(np.nanmax(tvt)),
                "tvt_mean": float(np.nanmean(tvt)),
                "tvt_std": float(np.nanstd(tvt)),
            }
            if tvt_stats["tvt_std"] == 0:
                warnings.append("tvt has zero standard deviation")

    sample_info = {}
    if sample_path is not None:
        if not sample_path.is_file():
            raise FileNotFoundError(f"sample not found: {sample_path}")
        sample = pd.read_csv(sample_path)
        if "id" not in sample.columns:
            fail(errors, "sample is missing id column")
        else:
            sample_ids = sample["id"].astype(str)
            sample_info["sample_rows"] = int(len(sample))
            if len(sub) != len(sample):
                fail(errors, f"row count mismatch: submission={len(sub)} sample={len(sample)}")
            if "id" in sub.columns:
                order_match = bool(sub["id"].equals(sample_ids))
                sample_info["id_order_matches_sample"] = order_match
                if not order_match:
                    fail(errors, "id order does not match sample_submission.csv")

    return {
        "status": "PASS" if not errors else "FAIL",
        "submission_path": str(submission_path),
        "sample_path": str(sample_path) if sample_path is not None else None,
        "rows": int(len(sub)),
        "columns": list(sub.columns),
        "sha256_submission_csv": sha256_file(submission_path),
        "errors": errors,
        "warnings": warnings,
        **sample_info,
        **tvt_stats,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("submission", type=Path, help="Path to submission.csv")
    parser.add_argument("--sample", type=Path, default=None, help="Path to sample_submission.csv")
    parser.add_argument("--json-out", type=Path, default=None, help="Optional audit JSON output path")
    args = parser.parse_args()

    result = audit(args.submission, args.sample)
    text = json.dumps(result, indent=2, sort_keys=True)
    print(text)

    if args.json_out is not None:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(text + "\n", encoding="utf-8")

    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
