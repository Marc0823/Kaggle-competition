# Planned Slot Review

This report combines release gates, audit readiness, final-package state, per-well impact, and pairwise diversity into one slot-level review. It does not submit to Kaggle.

## Review Counts

| slot_review | count |
| --- | --- |
| HOLD_EXTERNAL_CONTEXT | 5 |

## Slot Review

| planned_slot | slot_role | family | slot_review | slot_action | evidence_review | evidence_action | release_gate | impact_bucket | diversity_flag | min_pair_rmse | top_well | slot_review_reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | structural_candidate | projection_branch | HOLD_EXTERNAL_CONTEXT | WAIT | KEEP_FOR_FINAL_REVIEW | KEEP | BLOCKED_EXTERNAL_CONTEXT | BROAD | OK | 1.71662 | 00bbac68 | Release gate is BLOCKED_EXTERNAL_CONTEXT; do not submit or package yet. |
| 2 | calibration_sweep | projection_learned_blend | HOLD_EXTERNAL_CONTEXT | WAIT | KEEP_ONLY_IF_CALIBRATION_SWEEP | REVIEW | BLOCKED_EXTERNAL_CONTEXT | BROAD | REDUNDANT_REVIEW | 0.702226 | 00bbac68 | Release gate is BLOCKED_EXTERNAL_CONTEXT; do not submit or package yet. |
| 3 | calibration_sweep | projection_learned_blend | HOLD_EXTERNAL_CONTEXT | WAIT | KEEP_ONLY_IF_CALIBRATION_SWEEP | REVIEW | BLOCKED_EXTERNAL_CONTEXT | CONCENTRATED | REDUNDANT_REVIEW | 0.159696 | 00bbac68 | Release gate is BLOCKED_EXTERNAL_CONTEXT; do not submit or package yet. |
| 4 | calibration_sweep | projection_learned_blend | HOLD_EXTERNAL_CONTEXT | WAIT | KEEP_ONLY_IF_CALIBRATION_SWEEP | REVIEW | BLOCKED_EXTERNAL_CONTEXT | CONCENTRATED | REDUNDANT_REVIEW | 0.159696 | 00bbac68 | Release gate is BLOCKED_EXTERNAL_CONTEXT; do not submit or package yet. |
| 5 | flexible_information_slot | plateau_signal | HOLD_EXTERNAL_CONTEXT | WAIT | SPARSE_INFO_SLOT_REVIEW | REVIEW | BLOCKED_EXTERNAL_CONTEXT | SINGLE_WELL_DOMINATED | OK | 4.02266 | 00e12e8b | Release gate is BLOCKED_EXTERNAL_CONTEXT; do not submit or package yet. |

## Release Interpretation

- `HOLD_EXTERNAL_CONTEXT`: keep blocked until scores/kernel outcomes resolve.
- `evidence_review` shows the latent quality/diversity decision even while the release gate is blocked.
- `KEEP_ONLY_IF_CALIBRATION_SWEEP`: the slot is redundant, but may be kept if the explicit experiment is to map a blend curve.
- `SPARSE_INFO_SLOT_REVIEW`: use only as an information slot, not as broad model promotion.
- `KEEP_FOR_FINAL_REVIEW`: candidate has enough non-redundant evidence for final review once gates clear.

## Outputs

- `experiments/planned_slot_review.csv`
- `reports/planned_slot_review.md`
