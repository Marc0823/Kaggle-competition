# Submission Release Gate

This report checks whether the planned official submission slots may be released. It does not submit anything.

## Overall Gate

- Status: `READY_FOR_FINAL_REVIEW`
- Reason: External blockers are clear; run final manual review before any official submission.

## Gate Counts

| release_gate | count |
| --- | --- |
| MANUAL_REVIEW_REQUIRED | 5 |

## Planned Slot Gates

| planned_slot | slot_role | family | release_gate | current_action | priority_score | path | release_reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | structural_candidate | projection_branch | MANUAL_REVIEW_REQUIRED | final_review_before_submit | 19 | artifacts/kernel_outputs/rogii-baidalin-7-201-preflight-codex_v1/sp45_projection_submission.csv | Audit passed with warnings; review warnings and candidate purpose before submit. |
| 2 | calibration_sweep | projection_learned_blend | MANUAL_REVIEW_REQUIRED | final_review_before_submit | 18 | artifacts/kernel_outputs/rogii-baidalin-7-201-preflight-codex_v1/submission_sp45_fleongg_w0.50.csv | Audit passed with warnings; review warnings and candidate purpose before submit. |
| 3 | calibration_sweep | projection_learned_blend | MANUAL_REVIEW_REQUIRED | final_review_before_submit | 18 | artifacts/kernel_outputs/rogii-baidalin-7-201-preflight-codex_v1/submission_sp45_fleongg_w0.55.csv | Audit passed with warnings; review warnings and candidate purpose before submit. |
| 4 | calibration_sweep | projection_learned_blend | MANUAL_REVIEW_REQUIRED | final_review_before_submit | 18 | artifacts/kernel_outputs/rogii-baidalin-7-201-preflight-codex_v1/submission_sp45_fleongg_w0.60.csv | Audit passed with warnings; review warnings and candidate purpose before submit. |
| 5 | flexible_information_slot | plateau_signal | MANUAL_REVIEW_REQUIRED | final_review_before_submit | 65 | artifacts/plateau_recent_quantile_v1/submission.csv | Audit passed with warnings; review warnings and candidate purpose before submit. |

## Outputs

- `experiments/submission_release_gate.csv`
- `reports/submission_release_gate_report.md`
