# Submission Release Gate

This report checks whether the planned official submission slots may be released. It does not submit anything.

## Overall Gate

- Status: `BLOCKED_EXTERNAL_CONTEXT`
- Reason: Pending official scores or running kernels still affect candidate interpretation.

## Gate Counts

| release_gate | count |
| --- | --- |
| BLOCKED_EXTERNAL_CONTEXT | 5 |

## Planned Slot Gates

| planned_slot | slot_role | family | release_gate | current_action | priority_score | path | release_reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | structural_candidate | projection_branch | BLOCKED_EXTERNAL_CONTEXT | do_not_submit_yet | 124 | artifacts/kernel_outputs/rogii-baidalin-7-201-preflight-codex_v1/sp45_projection_submission.csv | Release after 54174151 scores and Degnonguidi v6 either completes/audits or is explicitly deferred. |
| 2 | calibration_sweep | projection_learned_blend | BLOCKED_EXTERNAL_CONTEXT | do_not_submit_yet | 123 | artifacts/kernel_outputs/rogii-baidalin-7-201-preflight-codex_v1/submission_sp45_fleongg_w0.50.csv | Release only after 54174151 and 54174876 score; prioritize if Fleongg is competitive or useful for ensemble diversity. |
| 3 | calibration_sweep | projection_learned_blend | BLOCKED_EXTERNAL_CONTEXT | do_not_submit_yet | 123 | artifacts/kernel_outputs/rogii-baidalin-7-201-preflight-codex_v1/submission_sp45_fleongg_w0.55.csv | Release only after 54174151 and 54174876 score; prioritize if Fleongg is competitive or useful for ensemble diversity. |
| 4 | calibration_sweep | projection_learned_blend | BLOCKED_EXTERNAL_CONTEXT | do_not_submit_yet | 123 | artifacts/kernel_outputs/rogii-baidalin-7-201-preflight-codex_v1/submission_sp45_fleongg_w0.60.csv | Release only after 54174151 and 54174876 score; prioritize if Fleongg is competitive or useful for ensemble diversity. |
| 5 | flexible_information_slot | plateau_signal | BLOCKED_EXTERNAL_CONTEXT | do_not_submit_yet | 65 | artifacts/plateau_recent_quantile_v1/submission.csv | Release as the flexible 5th slot only after anchors resolve and no stronger audited candidate is available. |

## Outputs

- `experiments/submission_release_gate.csv`
- `reports/submission_release_gate_report.md`
