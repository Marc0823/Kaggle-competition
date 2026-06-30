# Planned Slot Review

This report combines release gates, audit readiness, final-package state, per-well impact, and pairwise diversity into one slot-level review. It does not submit to Kaggle.

## Review Counts

| slot_review | count |
| --- | --- |
| KEEP_ONLY_IF_CALIBRATION_SWEEP | 3 |
| KEEP_FOR_FINAL_REVIEW | 1 |
| SPARSE_INFO_SLOT_REVIEW | 1 |

## Slot Review

| planned_slot | slot_role | family | slot_review | slot_action | evidence_review | evidence_action | release_gate | impact_bucket | diversity_flag | min_pair_rmse | top_well | slot_review_reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | structural_candidate | projection_branch | KEEP_FOR_FINAL_REVIEW | KEEP | KEEP_FOR_FINAL_REVIEW | KEEP | MANUAL_REVIEW_REQUIRED | BROAD | OK | 1.3733 | 00bbac68 | Candidate has non-redundant planned evidence; keep for final release review after external blockers clear. |
| 2 | calibration_sweep | projection_learned_blend | KEEP_ONLY_IF_CALIBRATION_SWEEP | REVIEW | KEEP_ONLY_IF_CALIBRATION_SWEEP | REVIEW | MANUAL_REVIEW_REQUIRED | BROAD | REDUNDANT_REVIEW | 0.171662 | 00bbac68 | This slot is redundant with nearby blend weights; keep only if the batch explicitly spends slots to map the blend curve. |
| 3 | calibration_sweep | projection_learned_blend | KEEP_ONLY_IF_CALIBRATION_SWEEP | REVIEW | KEEP_ONLY_IF_CALIBRATION_SWEEP | REVIEW | MANUAL_REVIEW_REQUIRED | BROAD | REDUNDANT_REVIEW | 0.171662 | 00bbac68 | This slot is redundant with nearby blend weights; keep only if the batch explicitly spends slots to map the blend curve. |
| 4 | calibration_sweep | projection_learned_blend | KEEP_ONLY_IF_CALIBRATION_SWEEP | REVIEW | KEEP_ONLY_IF_CALIBRATION_SWEEP | REVIEW | MANUAL_REVIEW_REQUIRED | BROAD | REDUNDANT_REVIEW | 0.171662 | 00bbac68 | This slot is redundant with nearby blend weights; keep only if the batch explicitly spends slots to map the blend curve. |
| 5 | flexible_information_slot | plateau_signal | SPARSE_INFO_SLOT_REVIEW | REVIEW | SPARSE_INFO_SLOT_REVIEW | REVIEW | MANUAL_REVIEW_REQUIRED | SINGLE_WELL_DOMINATED | OK | 4.01758 | 00e12e8b | Candidate is single-well dominated; use only as a sparse information slot. |

## Release Interpretation

- `HOLD_EXTERNAL_CONTEXT`: keep blocked until scores/kernel outcomes resolve.
- `evidence_review` shows the latent quality/diversity decision even while the release gate is blocked.
- `KEEP_ONLY_IF_CALIBRATION_SWEEP`: the slot is redundant, but may be kept if the explicit experiment is to map a blend curve.
- `SPARSE_INFO_SLOT_REVIEW`: use only as an information slot, not as broad model promotion.
- `KEEP_FOR_FINAL_REVIEW`: candidate has enough non-redundant evidence for final review once gates clear.

## Outputs

- `experiments/planned_slot_review.csv`
- `reports/planned_slot_review.md`
