# Next Submission Batch Plan

This is a conditional 4-5 slot plan built from audited candidates. It does not submit anything.

## Current Status

- Batch status: `WAIT_EXTERNAL_CONTEXT`
- Pending official submissions: `1`
- Running kernels: `0`
- Eligible audited candidates: `17`
- Planned slots: `5`
- Pending IDs: `54198676`
- Running kernels: ``

## Planned Slots

| planned_slot | slot_role | family | batch_status | current_action | priority_score | estimated_public_band | novelty_bucket | rmse_to_current_best_7p235 | path |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | structural_candidate | projection_branch | WAIT_EXTERNAL_CONTEXT | do_not_submit_yet | 124 | plausible_7p2_to_7p8_band | moderate | 1.45864 | artifacts/kernel_outputs/rogii-baidalin-7-201-preflight-codex_v1/sp45_projection_submission.csv |
| 2 | calibration_sweep | projection_learned_blend | WAIT_EXTERNAL_CONTEXT | do_not_submit_yet | 123 | plausible_7p2_to_7p8_band | moderate | 2.42452 | artifacts/kernel_outputs/rogii-baidalin-7-201-preflight-codex_v1/submission_sp45_fleongg_w0.50.csv |
| 3 | calibration_sweep | projection_learned_blend | WAIT_EXTERNAL_CONTEXT | do_not_submit_yet | 119 | plausible_7p2_to_7p8_band | moderate | 2.73598 | artifacts/sp45_projection_slot1_codex_v1/submission_sp45_fleongg_w0.55.csv |
| 4 | calibration_sweep | projection_learned_blend | WAIT_EXTERNAL_CONTEXT | do_not_submit_yet | 119 | plausible_7p2_to_7p8_band | moderate | 2.65427 | artifacts/sp45_projection_slot1_codex_v1/submission_sp45_fleongg_w0.60.csv |
| 5 | flexible_information_slot | plateau_signal | WAIT_EXTERNAL_CONTEXT | do_not_submit_yet | 65 | unknown_possible_but_risky | high | 4.72239 | artifacts/plateau_recent_quantile_v1/submission.csv |

## Release Rules

| result | next_action |
| --- | --- |
| 54174151 baseline scores near expected reference | Use it as the active-account anchor and allow SP45 projection review. |
| 54174151 blank or catastrophic | Block dependent submissions; repair active-account baseline before spending more slots. |
| 54174876 Fleongg improves or ties baseline | Prioritize SP45+Fleongg blend sweep slots after final review. |
| 54174876 Fleongg worsens materially | Prefer pure SP45 projection or plateau information slot; downweight Fleongg blends. |
| Degnonguidi v6 completes and audits cleanly | Insert its best distinct output ahead of lower-priority blend or plateau slots. |

## Outputs

- `experiments/next_submission_batch_plan.csv`
- `reports/next_submission_batch_plan.md`
