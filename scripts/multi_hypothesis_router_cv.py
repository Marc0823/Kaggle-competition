#!/usr/bin/env python3
"""Evaluate a first multi-hypothesis geosteering router on pseudo-hidden splits."""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


DEFAULT_DATA_DIR = Path("data/sample")
DEFAULT_OUTPUT_DIR = Path("experiments")
DEFAULT_REPORT = Path("reports/multi_hypothesis_router_cv_report.md")
STRAT_COLUMNS = ["Z", "ANCC", "ASTNU", "ASTNL", "EGFDU", "EGFDL", "BUDA"]


@dataclass
class PathCandidate:
    method: str
    values: np.ndarray
    status: str = "ok"
    detail: str = ""
    diagnostics: dict[str, float] | None = None


def fmt(value: Any) -> str:
    if isinstance(value, float):
        return "" if not np.isfinite(value) else f"{value:.6g}"
    if pd.isna(value):
        return ""
    return str(value)


def markdown_table(df: pd.DataFrame) -> str:
    if df.empty:
        return "No rows."
    cols = list(df.columns)
    lines = [
        "| " + " | ".join(cols) + " |",
        "| " + " | ".join(["---"] * len(cols)) + " |",
    ]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(fmt(row[c]) for c in cols) + " |")
    return "\n".join(lines)


def rmse(pred: np.ndarray, true: np.ndarray) -> float:
    pred = np.asarray(pred, dtype=float)
    true = np.asarray(true, dtype=float)
    mask = np.isfinite(pred) & np.isfinite(true)
    if int(mask.sum()) == 0:
        return float("nan")
    diff = pred[mask] - true[mask]
    return float(np.sqrt(np.mean(diff * diff)))


def finite_line_fit(x: np.ndarray, y: np.ndarray) -> tuple[float, float] | None:
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    mask = np.isfinite(x) & np.isfinite(y)
    if int(mask.sum()) < 2:
        return None
    x = x[mask]
    y = y[mask]
    if float(np.ptp(x)) <= 1e-9:
        return None
    slope, intercept = np.polyfit(x, y, 1)
    return float(slope), float(intercept)


def safe_interp(x: np.ndarray, y: np.ndarray, target: np.ndarray) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    target = np.asarray(target, dtype=float)
    mask = np.isfinite(x) & np.isfinite(y)
    if int(mask.sum()) < 5:
        return np.full(len(target), np.nan, dtype=float)
    x = x[mask]
    y = y[mask]
    order = np.argsort(x)
    x = x[order]
    y = y[order]
    keep = np.r_[True, np.diff(x) > 1e-9]
    x = x[keep]
    y = y[keep]
    if len(x) < 5:
        return np.full(len(target), np.nan, dtype=float)
    return np.interp(target, x, y, left=np.nan, right=np.nan)


def predict_line(x_train: np.ndarray, y_train: np.ndarray, x_eval: np.ndarray, fallback: float) -> np.ndarray:
    fit = finite_line_fit(x_train, y_train)
    if fit is None:
        return np.full(len(x_eval), float(fallback), dtype=float)
    slope, intercept = fit
    pred = slope * np.asarray(x_eval, dtype=float) + intercept
    pred[~np.isfinite(pred)] = float(fallback)
    return pred.astype(float)


def damp_toward(fallback: float, raw: np.ndarray, damp: float, max_move: float) -> np.ndarray:
    move = np.asarray(raw, dtype=float) - float(fallback)
    move = np.clip(damp * move, -max_move, max_move)
    return float(fallback) + move


def interp_typewell_gr(tw: pd.DataFrame, tvt: np.ndarray) -> np.ndarray:
    if not {"TVT", "GR"}.issubset(tw.columns):
        return np.full(len(tvt), np.nan, dtype=float)
    work = tw[["TVT", "GR"]].copy()
    work["TVT"] = pd.to_numeric(work["TVT"], errors="coerce")
    work["GR"] = pd.to_numeric(work["GR"], errors="coerce")
    work = work.dropna().sort_values("TVT")
    return safe_interp(work["TVT"].to_numpy(float), work["GR"].to_numpy(float), np.asarray(tvt, dtype=float))


def robust_mae(a: np.ndarray, b: np.ndarray) -> float:
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    mask = np.isfinite(a) & np.isfinite(b)
    if int(mask.sum()) < 20:
        return float("nan")
    return float(np.nanmedian(np.abs(a[mask] - b[mask])))


def best_gr_shift(gr: np.ndarray, tw: pd.DataFrame, tvt_path: np.ndarray, shifts: np.ndarray) -> tuple[float, float, float, float]:
    scores = np.asarray([robust_mae(gr, interp_typewell_gr(tw, tvt_path + shift)) for shift in shifts], dtype=float)
    if not np.isfinite(scores).any():
        return 0.0, float("nan"), float("nan"), 0.0
    zero_idx = int(np.argmin(np.abs(shifts)))
    zero_score = float(scores[zero_idx])
    best_idx = int(np.nanargmin(scores))
    best_score = float(scores[best_idx])
    improvement = 0.0
    if np.isfinite(zero_score):
        improvement = float((zero_score - best_score) / (abs(zero_score) + 1e-6))
    return float(shifts[best_idx]), zero_score, best_score, improvement


def native_cut_index(hw: pd.DataFrame) -> int | None:
    if "TVT_input" not in hw.columns:
        return None
    tvt_input = pd.to_numeric(hw["TVT_input"], errors="coerce").to_numpy(float)
    finite = np.flatnonzero(np.isfinite(tvt_input))
    if len(finite) == 0:
        return None
    return int(finite[-1] + 1)


def split_specs(hw: pd.DataFrame, cut_fracs: list[float], include_native: bool) -> list[tuple[str, int]]:
    specs: list[tuple[str, int]] = []
    if include_native:
        cut = native_cut_index(hw)
        if cut is not None:
            specs.append(("native_prefix", cut))
    n = len(hw)
    for frac in cut_fracs:
        specs.append((f"frac_{frac:.2f}", int(round(n * frac))))
    deduped: dict[tuple[str, int], tuple[str, int]] = {}
    for name, cut in specs:
        deduped.setdefault((name, cut), (name, cut))
    return list(deduped.values())


def prefix_holdout_cut(prefix_idx: np.ndarray, args: argparse.Namespace) -> int | None:
    if len(prefix_idx) < args.min_prefix_rows + args.router_min_holdout_rows:
        return None
    holdout_n = max(args.router_min_holdout_rows, int(round(args.router_holdout_frac * len(prefix_idx))))
    holdout_n = min(holdout_n, max(args.router_min_holdout_rows, len(prefix_idx) // 2))
    cut = int(prefix_idx[-holdout_n])
    if cut < args.min_prefix_rows:
        return None
    return cut


def candidate_paths(
    hw: pd.DataFrame,
    tw: pd.DataFrame,
    train_idx: np.ndarray,
    eval_idx: np.ndarray,
    true_tvt: np.ndarray,
    args: argparse.Namespace,
) -> list[PathCandidate]:
    md = pd.to_numeric(hw["MD"], errors="coerce").to_numpy(float)
    train_valid = train_idx[np.isfinite(true_tvt[train_idx])]
    if len(train_valid) == 0:
        return []
    fallback = float(true_tvt[train_valid[-1]])
    tail_idx = train_valid[-min(args.tail_rows, len(train_valid)) :]

    candidates: list[PathCandidate] = []
    candidates.append(PathCandidate("last_value", np.full(len(eval_idx), fallback, dtype=float)))

    raw_tail = predict_line(md[tail_idx], true_tvt[tail_idx], md[eval_idx], fallback)
    candidates.append(
        PathCandidate(
            "damped_tail_linear_md",
            damp_toward(fallback, raw_tail, args.tail_damp, args.max_move),
            detail=f"damp={args.tail_damp:.3f};max_move={args.max_move:.3f}",
        )
    )

    for col in STRAT_COLUMNS:
        if col not in hw.columns:
            continue
        x = pd.to_numeric(hw[col], errors="coerce").to_numpy(float)
        raw = predict_line(x[tail_idx], true_tvt[tail_idx], x[eval_idx], fallback)
        candidates.append(
            PathCandidate(
                f"damped_tail_linear_{col}",
                damp_toward(fallback, raw, args.strat_damp, args.max_move),
                detail=f"damp={args.strat_damp:.3f};max_move={args.max_move:.3f}",
            )
        )

    if len(train_valid) >= args.plateau_window:
        tail = true_tvt[train_valid[-min(args.plateau_window, len(train_valid)) :]]
        target = float(np.nanquantile(tail, args.plateau_quantile))
        move = np.clip(target - fallback, -args.max_move, args.max_move)
        candidates.append(
            PathCandidate(
                "recent_plateau_quantile",
                np.full(len(eval_idx), fallback + args.plateau_blend * move, dtype=float),
                detail=f"window={args.plateau_window};quantile={args.plateau_quantile:.3f};move={move:.3f}",
            )
        )

    if "GR" in hw.columns:
        gr_full = pd.to_numeric(hw["GR"], errors="coerce").interpolate(limit_direction="both").to_numpy(float)
        shifts = np.arange(-args.max_gr_shift, args.max_gr_shift + 1e-9, args.gr_shift_step)
        prefix_gr = train_valid[np.isfinite(gr_full[train_valid])]
        eval_gr_mask = np.isfinite(gr_full[eval_idx])
        if len(prefix_gr) >= args.min_gr_rows and int(eval_gr_mask.sum()) >= args.min_gr_rows:
            prefix_shift, _, _, prefix_improvement = best_gr_shift(gr_full[prefix_gr], tw, true_tvt[prefix_gr], shifts)
            for base in list(candidates):
                eval_shift, _, _, eval_improvement = best_gr_shift(
                    gr_full[eval_idx][eval_gr_mask],
                    tw,
                    base.values[eval_gr_mask],
                    shifts,
                )
                if abs(prefix_shift) > args.max_prefix_shift_abs:
                    status = "fallback"
                    shifted = base.values.copy()
                    detail = "prefix_shift_unstable"
                elif eval_improvement < args.min_eval_improvement or abs(eval_shift) < 1e-9:
                    status = "fallback"
                    shifted = base.values.copy()
                    detail = "eval_shift_not_confident"
                else:
                    status = "ok"
                    ramp = 1.0 - np.exp(-np.arange(len(eval_idx), dtype=float) / max(30.0, 0.10 * len(eval_idx)))
                    shifted = base.values + np.clip(args.gr_alpha * eval_shift * ramp, -args.max_move, args.max_move)
                    detail = f"eval_shift={eval_shift:.3f};eval_improvement={eval_improvement:.4f}"
                candidates.append(
                    PathCandidate(
                        f"gr_shift__{base.method}",
                        shifted,
                        status=status,
                        detail=detail,
                        diagnostics={
                            "prefix_gr_shift": prefix_shift,
                            "prefix_gr_improvement": prefix_improvement,
                            "eval_gr_shift": eval_shift,
                            "eval_gr_improvement": eval_improvement,
                        },
                    )
                )

    return candidates


def method_diagnostics(candidates: list[PathCandidate], true: np.ndarray) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for candidate in candidates:
        values = np.asarray(candidate.values, dtype=float)
        diff = values - true
        finite = np.isfinite(diff)
        rows.append(
            {
                "method": candidate.method,
                "status": candidate.status,
                "detail": candidate.detail,
                "eval_rows": int(finite.sum()),
                "rmse": rmse(values, true),
                "mae": float(np.mean(np.abs(diff[finite]))) if int(finite.sum()) else float("nan"),
                "bias": float(np.mean(diff[finite])) if int(finite.sum()) else float("nan"),
                "sse": float(np.sum(diff[finite] * diff[finite])) if int(finite.sum()) else float("nan"),
                "pred_std": float(np.nanstd(values)) if len(values) else float("nan"),
                **(candidate.diagnostics or {}),
            }
        )
    return rows


def is_guarded_candidate(method: str, allow_gr_shift: bool) -> bool:
    if method == "last_value":
        return True
    if method.startswith("gr_shift__") and not allow_gr_shift:
        return False
    if method in {"damped_tail_linear_md", "gr_shift__damped_tail_linear_md"}:
        return False
    if method.startswith("damped_tail_linear_") or method == "recent_plateau_quantile":
        return True
    return False


def select_router_method(
    hw: pd.DataFrame,
    tw: pd.DataFrame,
    prefix_idx: np.ndarray,
    true_tvt: np.ndarray,
    args: argparse.Namespace,
) -> dict[str, object]:
    holdout_cut = prefix_holdout_cut(prefix_idx, args)
    if holdout_cut is None:
        return {
            "router_method": "last_value",
            "router_status": "fallback",
            "router_detail": "short_prefix_for_holdout",
            "holdout_cut_idx": math.nan,
            "holdout_best_rmse": math.nan,
            "holdout_baseline_rmse": math.nan,
            "holdout_margin_rmse": math.nan,
            "holdout_improvement_rmse": math.nan,
            "guarded_method": "last_value",
            "guarded_status": "fallback",
            "guarded_detail": "short_prefix_for_holdout",
            "holdout_top2_methods": "",
        }

    train_idx = np.arange(0, holdout_cut, dtype=int)
    holdout_idx = np.arange(holdout_cut, int(prefix_idx[-1]) + 1, dtype=int)
    holdout_true = true_tvt[holdout_idx]
    holdout_candidates = candidate_paths(hw, tw, train_idx, holdout_idx, true_tvt, args)
    rows = method_diagnostics(holdout_candidates, holdout_true)
    valid = [row for row in rows if np.isfinite(float(row["rmse"]))]
    if not valid:
        return {
            "router_method": "last_value",
            "router_status": "fallback",
            "router_detail": "no_valid_holdout_candidate",
            "holdout_cut_idx": holdout_cut,
            "holdout_best_rmse": math.nan,
            "holdout_baseline_rmse": math.nan,
            "holdout_margin_rmse": math.nan,
            "holdout_improvement_rmse": math.nan,
            "guarded_method": "last_value",
            "guarded_status": "fallback",
            "guarded_detail": "no_valid_holdout_candidate",
            "holdout_top2_methods": "",
        }

    valid = sorted(valid, key=lambda row: (float(row["rmse"]), str(row["method"])))
    best = valid[0]
    baseline_rows = [row for row in valid if row["method"] == "last_value"]
    baseline_rmse = float(baseline_rows[0]["rmse"]) if baseline_rows else float("nan")
    second_rmse = float(valid[1]["rmse"]) if len(valid) > 1 else float("nan")
    margin = second_rmse - float(best["rmse"]) if np.isfinite(second_rmse) else float("nan")
    improvement = baseline_rmse - float(best["rmse"]) if np.isfinite(baseline_rmse) else float("nan")
    top2 = ";".join(str(row["method"]) for row in valid[:2])
    guarded_method = "last_value"
    guarded_status = "fallback"
    guarded_detail = "default_last_value"
    if str(best["method"]) == "last_value":
        guarded_status = "ok"
        guarded_detail = "holdout_selected_last_value"
    else:
        improvement_frac = improvement / (abs(baseline_rmse) + 1e-6) if np.isfinite(improvement) else float("nan")
        passes_improvement = (
            np.isfinite(improvement)
            and np.isfinite(improvement_frac)
            and improvement >= args.router_min_improvement_rmse
            and improvement_frac >= args.router_min_improvement_frac
        )
        passes_margin = np.isfinite(margin) and margin >= args.router_min_margin_rmse
        passes_family = is_guarded_candidate(str(best["method"]), args.router_allow_gr_shift)
        if passes_improvement and passes_margin and passes_family:
            guarded_method = str(best["method"])
            guarded_status = "ok"
            guarded_detail = "passed_guarded_holdout_gate"
        else:
            guarded_detail = (
                f"blocked_guard;improvement={improvement:.4f};"
                f"margin={margin:.4f};family_ok={passes_family}"
            )
    return {
        "router_method": str(best["method"]),
        "router_status": "ok",
        "router_detail": "selected_by_prefix_holdout_rmse",
        "holdout_cut_idx": holdout_cut,
        "holdout_best_rmse": float(best["rmse"]),
        "holdout_baseline_rmse": baseline_rmse,
        "holdout_margin_rmse": margin,
        "holdout_improvement_rmse": improvement,
        "guarded_method": guarded_method,
        "guarded_status": guarded_status,
        "guarded_detail": guarded_detail,
        "holdout_top2_methods": top2,
    }


def run_split(
    well: str,
    split_name: str,
    cut_idx: int,
    hw: pd.DataFrame,
    tw: pd.DataFrame,
    args: argparse.Namespace,
) -> tuple[list[dict[str, object]], dict[str, object] | None]:
    true_tvt = pd.to_numeric(hw["TVT"], errors="coerce").to_numpy(float)
    n = len(hw)
    if cut_idx < args.min_prefix_rows or n - cut_idx < args.min_eval_rows:
        return [], None

    prefix_idx = np.arange(0, cut_idx, dtype=int)
    eval_idx = np.arange(cut_idx, n, dtype=int)
    eval_true = true_tvt[eval_idx]
    candidates = candidate_paths(hw, tw, prefix_idx, eval_idx, true_tvt, args)
    if not candidates:
        return [], None

    router = select_router_method(hw, tw, prefix_idx, true_tvt, args)
    method_to_values = {candidate.method: candidate.values for candidate in candidates}
    chosen_method = str(router["router_method"])
    if chosen_method not in method_to_values:
        chosen_method = "last_value"
    chosen_values = method_to_values.get(chosen_method, candidates[0].values)
    candidates.append(PathCandidate("router_prefix_holdout_best", chosen_values, detail=f"selected={chosen_method}"))
    guarded_method = str(router.get("guarded_method", "last_value"))
    if guarded_method not in method_to_values:
        guarded_method = "last_value"
    guarded_values = method_to_values.get(guarded_method, candidates[0].values)
    candidates.append(PathCandidate("router_guarded_prefix_holdout", guarded_values, detail=f"selected={guarded_method}"))

    rows = []
    for row in method_diagnostics(candidates, eval_true):
        rows.append(
            {
                "well": well,
                "split": split_name,
                "cut_idx": cut_idx,
                "prefix_rows": len(prefix_idx),
                **row,
            }
        )

    decision = {
        "well": well,
        "split": split_name,
        "cut_idx": cut_idx,
        "prefix_rows": len(prefix_idx),
        "eval_rows": len(eval_idx),
        "selected_eval_method": chosen_method,
        "guarded_eval_method": guarded_method,
        **router,
    }
    return rows, decision


def summarize(scores: pd.DataFrame, baseline: str) -> pd.DataFrame:
    if scores.empty:
        return pd.DataFrame()
    key = ["well", "split", "cut_idx"]
    base = scores[scores["method"] == baseline][key + ["rmse"]].rename(columns={"rmse": "baseline_rmse"})
    work = scores.merge(base, on=key, how="left")
    work["delta_rmse_vs_baseline"] = work["rmse"] - work["baseline_rmse"]
    scores["baseline_rmse"] = work["baseline_rmse"].to_numpy(float)
    scores["delta_rmse_vs_baseline"] = work["delta_rmse_vs_baseline"].to_numpy(float)

    rows = []
    for method, group in work.groupby("method", sort=False):
        valid = group[np.isfinite(group["sse"]) & (group["eval_rows"] > 0)].copy()
        if valid.empty:
            continue
        rows.append(
            {
                "method": method,
                "splits": int(len(valid)),
                "eval_rows": int(valid["eval_rows"].sum()),
                "weighted_rmse": float(np.sqrt(valid["sse"].sum() / valid["eval_rows"].sum())),
                "mean_rmse": float(valid["rmse"].mean()),
                "median_rmse": float(valid["rmse"].median()),
                "mean_delta_rmse_vs_baseline": float(valid["delta_rmse_vs_baseline"].mean()),
                "median_delta_rmse_vs_baseline": float(valid["delta_rmse_vs_baseline"].median()),
                "win_rate_vs_baseline": float((valid["delta_rmse_vs_baseline"] < 0).mean()),
                "fallback_rate": float((valid["status"] != "ok").mean()) if "status" in valid.columns else 0.0,
            }
        )
    return pd.DataFrame(rows).sort_values(["weighted_rmse", "method"])


def write_report(scores: pd.DataFrame, summary: pd.DataFrame, decisions: pd.DataFrame, output: Path, baseline: str) -> None:
    best = summary.head(16).copy()
    router_rows = summary[summary["method"].astype(str).str.contains("router", regex=False, na=False)].copy()
    decision_counts = (
        decisions["selected_eval_method"].value_counts().rename_axis("selected_eval_method").reset_index(name="count")
        if not decisions.empty and "selected_eval_method" in decisions.columns
        else pd.DataFrame()
    )
    guarded_counts = (
        decisions["guarded_eval_method"].value_counts().rename_axis("guarded_eval_method").reset_index(name="count")
        if not decisions.empty and "guarded_eval_method" in decisions.columns
        else pd.DataFrame()
    )
    worst_router = scores[scores["method"] == "router_guarded_prefix_holdout"].sort_values("rmse", ascending=False).head(10)
    lines = [
        "# Multi-Hypothesis Router CV Report",
        "",
        "This report evaluates a first candidate-path matrix and prefix-holdout router on train pseudo-hidden splits.",
        "It is a diagnostic harness, not an official submission package.",
        "",
        f"Baseline comparator: `{baseline}`",
        "",
        "## Method Summary",
        "",
        markdown_table(best),
        "",
        "## Router Summary",
        "",
        markdown_table(router_rows),
        "",
        "## Router Selection Counts",
        "",
        markdown_table(decision_counts),
        "",
        "## Guarded Router Selection Counts",
        "",
        markdown_table(guarded_counts),
        "",
        "## Worst Router Splits",
        "",
        markdown_table(
            worst_router[
                [
                    "well",
                    "split",
                    "cut_idx",
                    "prefix_rows",
                    "eval_rows",
                    "rmse",
                    "baseline_rmse",
                    "delta_rmse_vs_baseline",
                    "detail",
                ]
            ]
            if not worst_router.empty
            else pd.DataFrame()
        ),
        "",
        "## Interpretation",
        "",
        "- `router_prefix_holdout_best` chooses a candidate family using only a holdout from the known prefix.",
        "- `router_guarded_prefix_holdout` falls back to `last_value` unless holdout improvement, margin, and family safety gates pass.",
        "- A useful router should improve weighted RMSE or at least reduce worst-split risk versus `last_value`.",
        "- If the router underperforms, inspect `experiments/multi_hypothesis_router_cv_decisions.csv` to see which candidate families the prefix holdout over-selected.",
        "",
        "## Outputs",
        "",
        "- `experiments/multi_hypothesis_router_cv_scores.csv`",
        "- `experiments/multi_hypothesis_router_cv_summary.csv`",
        "- `experiments/multi_hypothesis_router_cv_decisions.csv`",
    ]
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_cut_fracs(values: list[str]) -> list[float]:
    out: list[float] = []
    for value in values:
        frac = float(value)
        if not 0.05 <= frac <= 0.90:
            raise argparse.ArgumentTypeError(f"cut fraction out of range: {value}")
        out.append(frac)
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--cut-fracs", nargs="*", default=["0.25", "0.35", "0.50", "0.65"])
    parser.add_argument("--no-native-prefix", action="store_true")
    parser.add_argument("--min-prefix-rows", type=int, default=200)
    parser.add_argument("--min-eval-rows", type=int, default=200)
    parser.add_argument("--tail-rows", type=int, default=256)
    parser.add_argument("--tail-damp", type=float, default=0.25)
    parser.add_argument("--strat-damp", type=float, default=0.20)
    parser.add_argument("--max-move", type=float, default=12.0)
    parser.add_argument("--plateau-window", type=int, default=256)
    parser.add_argument("--plateau-quantile", type=float, default=0.50)
    parser.add_argument("--plateau-blend", type=float, default=1.0)
    parser.add_argument("--router-holdout-frac", type=float, default=0.20)
    parser.add_argument("--router-min-holdout-rows", type=int, default=80)
    parser.add_argument("--router-min-improvement-rmse", type=float, default=0.75)
    parser.add_argument("--router-min-improvement-frac", type=float, default=0.15)
    parser.add_argument("--router-min-margin-rmse", type=float, default=0.10)
    parser.add_argument("--router-allow-gr-shift", action="store_true")
    parser.add_argument("--min-gr-rows", type=int, default=50)
    parser.add_argument("--max-gr-shift", type=float, default=30.0)
    parser.add_argument("--gr-shift-step", type=float, default=5.0)
    parser.add_argument("--gr-alpha", type=float, default=0.20)
    parser.add_argument("--max-prefix-shift-abs", type=float, default=10.0)
    parser.add_argument("--min-eval-improvement", type=float, default=0.03)
    parser.add_argument("--baseline-method", default="last_value")
    args = parser.parse_args()

    train_dir = args.data_dir / "train"
    if not train_dir.is_dir():
        raise FileNotFoundError(f"missing train directory: {train_dir}")

    cut_fracs = parse_cut_fracs(args.cut_fracs)
    score_rows: list[dict[str, object]] = []
    decision_rows: list[dict[str, object]] = []
    for hw_path in sorted(train_dir.glob("*__horizontal_well.csv")):
        well = hw_path.name.removesuffix("__horizontal_well.csv")
        tw_path = train_dir / f"{well}__typewell.csv"
        if not tw_path.exists():
            continue
        hw = pd.read_csv(hw_path)
        tw = pd.read_csv(tw_path)
        if not {"MD", "TVT"}.issubset(hw.columns):
            continue
        for split_name, cut_idx in split_specs(hw, cut_fracs, include_native=not args.no_native_prefix):
            rows, decision = run_split(well, split_name, cut_idx, hw, tw, args)
            score_rows.extend(rows)
            if decision is not None:
                decision_rows.append(decision)

    scores = pd.DataFrame(score_rows)
    decisions = pd.DataFrame(decision_rows)
    if scores.empty:
        raise RuntimeError("no router CV rows generated")
    summary = summarize(scores, args.baseline_method)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    scores_path = args.output_dir / "multi_hypothesis_router_cv_scores.csv"
    summary_path = args.output_dir / "multi_hypothesis_router_cv_summary.csv"
    decisions_path = args.output_dir / "multi_hypothesis_router_cv_decisions.csv"
    scores.to_csv(scores_path, index=False)
    summary.to_csv(summary_path, index=False)
    decisions.to_csv(decisions_path, index=False)
    write_report(scores, summary, decisions, args.report, args.baseline_method)

    print(f"wrote {scores_path}")
    print(f"wrote {summary_path}")
    print(f"wrote {decisions_path}")
    print(f"wrote {args.report}")
    print(summary.head(16).to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
