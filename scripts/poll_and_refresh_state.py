#!/usr/bin/env python3
"""Poll Kaggle state and refresh ROGII planning reports in one safe pass."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import pandas as pd


DEFAULT_KAGGLE_BIN = "/home/ubuntu/workstation/JoeProject/kaggle-api-workbench/.venv/bin/kaggle"
DEFAULT_SUMMARY = Path("experiments/poll_refresh_summary.csv")
DEFAULT_REPORT = Path("reports/poll_refresh_report.md")


def run_cmd(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, text=True, capture_output=True, check=False)


def run_json(cmd: list[str]) -> tuple[dict[str, Any], subprocess.CompletedProcess[str]]:
    proc = run_cmd(cmd)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or f"{cmd[0]} exited {proc.returncode}")
    try:
        parsed = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"could not parse JSON from {' '.join(cmd)}: {exc}") from exc
    return parsed, proc


def run_checked(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    proc = run_cmd(cmd)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or f"{cmd[0]} exited {proc.returncode}")
    return proc


def safe_read_csv(path: Path) -> pd.DataFrame:
    if not path.is_file():
        return pd.DataFrame()
    return pd.read_csv(path)


def pending_count(submissions: pd.DataFrame) -> int:
    if submissions.empty or "status" not in submissions.columns:
        return 0
    return int(submissions["status"].astype(str).str.lower().isin(["pending", "submitted", "running"]).sum())


def running_kernel_count(kernels: pd.DataFrame) -> int:
    if kernels.empty or "status" not in kernels.columns:
        return 0
    return int(kernels["status"].astype(str).str.upper().isin(["RUNNING", "PENDING", "QUEUED"]).sum())


def first_or_blank(df: pd.DataFrame, column: str) -> str:
    if df.empty or column not in df.columns:
        return ""
    return str(df.iloc[0].get(column, "") or "")


def count_values(df: pd.DataFrame, column: str) -> str:
    if df.empty or column not in df.columns:
        return ""
    counts = df[column].astype(str).value_counts()
    return "; ".join(f"{idx}={int(value)}" for idx, value in counts.items())


def write_outputs(summary: dict[str, Any], output_csv: Path, report: Path) -> None:
    rows = [{"metric": key, "value": value} for key, value in summary.items()]
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(output_csv, index=False)

    lines = [
        "# Poll And Refresh Report",
        "",
        "This report summarizes the latest safe polling pass. It does not submit to Kaggle.",
        "",
        "## Summary",
        "",
        "| metric | value |",
        "| --- | --- |",
    ]
    for key, value in summary.items():
        lines.append(f"| {key} | {value} |")
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- If `kernel_updates_detected` or `submission_updates_detected` is nonzero while the corresponding apply flag is false, rerun with explicit apply after reviewing the dry-run output.",
            "- If `batch_status` is `WAIT_EXTERNAL_CONTEXT`, keep preparing candidates but do not spend official submission slots.",
            "- Before any official submission, rerun this script after applying external state changes so readiness, audit summary, and batch plan agree.",
            "",
            "## Outputs Refreshed",
            "",
            "- `reports/next_batch_readiness_report.md`",
            "- `reports/candidate_audit_summary_report.md`",
            "- `reports/next_submission_batch_plan.md`",
            "- `reports/submission_release_gate_report.md`",
            "- `reports/planning_state_validation_report.md`",
            "- `reports/result_branch_matrix.md`",
            f"- `{output_csv.as_posix()}`",
            f"- `{report.as_posix()}`",
        ]
    )
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kaggle-bin", default=DEFAULT_KAGGLE_BIN)
    parser.add_argument("--page-size", type=int, default=12)
    parser.add_argument("--apply-kernel-updates", action="store_true")
    parser.add_argument("--apply-submission-updates", action="store_true")
    parser.add_argument("--append-missing-submissions", action="store_true")
    parser.add_argument("--summary-csv", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args()

    kernel_cmd = [
        sys.executable,
        "scripts/sync_kernel_ledger.py",
        "--kaggle-bin",
        args.kaggle_bin,
    ]
    if args.apply_kernel_updates:
        kernel_cmd.append("--apply")
    kernel_summary, _ = run_json(kernel_cmd)

    submission_cmd = [
        sys.executable,
        "scripts/update_submission_ledger.py",
        "--kaggle-bin",
        args.kaggle_bin,
        "--page-size",
        str(args.page_size),
    ]
    if args.append_missing_submissions:
        submission_cmd.append("--append-missing")
    if not args.apply_submission_updates:
        submission_cmd.append("--dry-run")
    submission_summary, _ = run_json(submission_cmd)

    run_checked([sys.executable, "scripts/next_batch_readiness_report.py"])
    run_checked([sys.executable, "scripts/candidate_audit_summary.py"])
    run_checked([sys.executable, "scripts/next_submission_batch_plan.py"])
    run_checked([sys.executable, "scripts/submission_release_gate.py"])
    run_checked([sys.executable, "scripts/result_branch_matrix.py"])

    submissions = safe_read_csv(Path("experiments/submission_ledger.csv"))
    kernels = safe_read_csv(Path("experiments/kernel_run_ledger.csv"))
    readiness = safe_read_csv(Path("experiments/next_batch_readiness.csv"))
    audit_summary = safe_read_csv(Path("experiments/candidate_audit_summary.csv"))
    batch_plan = safe_read_csv(Path("experiments/next_submission_batch_plan.csv"))
    release_gate = safe_read_csv(Path("experiments/submission_release_gate.csv"))
    result_matrix = safe_read_csv(Path("experiments/result_branch_matrix.csv"))

    summary = {
        "kernel_updates_detected": len(kernel_summary.get("updated", [])),
        "kernel_errors": len(kernel_summary.get("errors", [])),
        "kernel_apply": bool(kernel_summary.get("apply")),
        "submission_updates_detected": len(submission_summary.get("updated", [])),
        "submission_appended_detected": len(submission_summary.get("appended", [])),
        "submission_missing_not_appended": len(submission_summary.get("missing_not_appended", [])),
        "submission_dry_run": bool(submission_summary.get("dry_run")),
        "pending_official_submissions": pending_count(submissions),
        "running_kernels": running_kernel_count(kernels),
        "readiness_status_counts": count_values(readiness, "readiness_status"),
        "audit_gate_counts": count_values(audit_summary, "audit_gate"),
        "submission_gate_counts": count_values(audit_summary, "submission_gate"),
        "batch_status": first_or_blank(batch_plan, "batch_status"),
        "planned_slots": len(batch_plan),
        "current_action_counts": count_values(batch_plan, "current_action"),
        "release_gate_counts": count_values(release_gate, "release_gate"),
        "result_branch_rules": len(result_matrix),
    }

    write_outputs(summary, args.summary_csv, args.report)
    run_checked([sys.executable, "scripts/validate_planning_state.py"])
    validation = safe_read_csv(Path("experiments/planning_state_validation.csv"))
    error_failures = 0
    if not validation.empty and {"severity", "status"}.issubset(validation.columns):
        error_failures = int(((validation["severity"] == "ERROR") & (validation["status"] != "PASS")).sum())
    summary["planning_validation_status_counts"] = count_values(validation, "status")
    summary["planning_validation_error_failures"] = error_failures
    write_outputs(summary, args.summary_csv, args.report)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
