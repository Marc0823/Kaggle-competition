# Next Batch Readiness Report

This report ranks local candidates and blockers for the next official submission batch.

## Current Blockers

- Pending official submissions: `1`
- Running Kaggle kernels: `0`
- Ready-after-audit candidates with no context blocker: `0`

## Pending Official Submissions

| submission_id | candidate_id | status | decision | public_score |
| --- | --- | --- | --- | --- |
| 54198676 | sp45_projection_slot1_dynamic_rerun | pending | submitted_information |  |

## Running Kernels

No rows.

## Candidate Readiness

| path | family | readiness_status | base_decision | estimated_public_band | rmse_to_current_best_7p235 | anchor_first_abs_p90 | jump_rate_abs_slope_gt3 | next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| artifacts/gr_typewell_light_alpha040_v1/submission.csv | gr_typewell_light | HOLD_PENDING_CONTEXT | LOCAL_CANDIDATE | plausible_7p2_to_7p8_band | 1.39813 | 0.0360878 | 7.06814e-05 | Wait for pending official scores or running reference kernels before spending another slot. |
| artifacts/kernel_outputs/rogii-baidalin-7-201-preflight-codex_v1/sp45_projection_submission.csv | projection_branch | HOLD_PENDING_CONTEXT | LOCAL_CANDIDATE | plausible_7p2_to_7p8_band | 1.45864 | 6.39778 | 0 | Wait for pending official scores or running reference kernels before spending another slot. |
| artifacts/kernel_outputs/rogii-baidalin-7-201-preflight-codex_v1/submission_sp45_fleongg_w0.60.csv | projection_learned_blend | HOLD_PENDING_CONTEXT | LOCAL_CANDIDATE | plausible_7p2_to_7p8_band | 2.15794 | 3.85775 | 0 | Wait for pending official scores or running reference kernels before spending another slot. |
| artifacts/kernel_outputs/rogii-baidalin-7-201-preflight-codex_v1/submission_sp45_fleongg_w0.58.csv | projection_learned_blend | HOLD_PENDING_CONTEXT | LOCAL_CANDIDATE | plausible_7p2_to_7p8_band | 2.20956 | 3.73075 | 0 | Wait for pending official scores or running reference kernels before spending another slot. |
| artifacts/kernel_outputs/rogii-baidalin-7-201-preflight-codex_v1/submission_sp45_fleongg_w0.55.csv | projection_learned_blend | HOLD_PENDING_CONTEXT | LOCAL_CANDIDATE | plausible_7p2_to_7p8_band | 2.28867 | 3.54025 | 0 | Wait for pending official scores or running reference kernels before spending another slot. |
| artifacts/kernel_outputs/rogii-baidalin-7-201-preflight-codex_v1/submission_sp45_fleongg_w0.52.csv | projection_learned_blend | HOLD_PENDING_CONTEXT | LOCAL_CANDIDATE | plausible_7p2_to_7p8_band | 2.36963 | 3.34974 | 0 | Wait for pending official scores or running reference kernels before spending another slot. |
| artifacts/kernel_outputs/rogii-baidalin-7-201-preflight-codex_v1/submission_sp45_fleongg_w0.50.csv | projection_learned_blend | HOLD_PENDING_CONTEXT | LOCAL_CANDIDATE | plausible_7p2_to_7p8_band | 2.42452 | 3.22274 | 0 | Wait for pending official scores or running reference kernels before spending another slot. |
| artifacts/fleongg_branch_calibration_joezzzzz_v1/sp45_projection_submission.csv | projection_branch | HOLD_PENDING_CONTEXT | LOCAL_CANDIDATE | unknown_possible_but_risky | 5.79449 | 2.65079 | 0 | Wait for pending official scores or running reference kernels before spending another slot. |
| artifacts/fleongg_branch_calibration_joezzzzz_v2/sp45_projection_submission.csv | projection_branch | HOLD_PENDING_CONTEXT | LOCAL_CANDIDATE | unknown_possible_but_risky | 5.79449 | 2.65079 | 0 | Wait for pending official scores or running reference kernels before spending another slot. |
| artifacts/lucifer_baseline_repro_joezzzzz_v1/sp45_projection_submission.csv | projection_branch | HOLD_PENDING_CONTEXT | LOCAL_CANDIDATE | unknown_possible_but_risky | 5.79449 | 2.65079 | 0 | Wait for pending official scores or running reference kernels before spending another slot. |
| artifacts/plateau_recent_quantile_v1/submission.csv | plateau_signal | HOLD_INFORMATION_SLOT | LOCAL_CANDIDATE | unknown_possible_but_risky | 4.72239 | 3.28521 | 7.06814e-05 | Sparse local win; hold until pending anchors or stronger validation justify a slot. |
| artifacts/gr_typewell_light_alpha010_v1/submission.csv | gr_typewell_light | HOLD_LOW_UPSIDE | HOLD_LOW_UPSIDE | likely_around_7p235_low_upside | 0.349534 | 0.0360878 | 7.06814e-05 | Likely safe but low information value. |
| artifacts/gr_typewell_light_alpha020_v1/submission.csv | gr_typewell_light | HOLD_LOW_UPSIDE | HOLD_LOW_UPSIDE | likely_around_7p235_low_upside | 0.699067 | 0.0360878 | 7.06814e-05 | Likely safe but low information value. |
| artifacts/lucifer_baseline_repro_joezzzzz_v1/submission.csv | anchor_or_duplicate | HOLD_DUPLICATE | HOLD_DUPLICATE | likely_around_7p235_low_upside | 0 | 0.0360878 | 7.06814e-05 | Too close to the active baseline; useful as anchor only. |
| artifacts/lucifer_baseline_repro_joezzzzz_v1/submission_gold_prefix_aggressive.csv | anchor_or_duplicate | HOLD_DUPLICATE | HOLD_DUPLICATE | likely_around_7p235_low_upside | 0 | 0.0360878 | 7.06814e-05 | Too close to the active baseline; useful as anchor only. |
| artifacts/lucifer_baseline_repro_joezzzzz_v1/submission_gold_prefix_balanced.csv | anchor_or_duplicate | HOLD_DUPLICATE | HOLD_DUPLICATE | likely_around_7p235_low_upside | 0 | 0.0360878 | 7.06814e-05 | Too close to the active baseline; useful as anchor only. |
| artifacts/lucifer_baseline_repro_joezzzzz_v1/submission_gold_prefix_conservative.csv | anchor_or_duplicate | HOLD_DUPLICATE | HOLD_DUPLICATE | likely_around_7p235_low_upside | 0 | 0.0360878 | 7.06814e-05 | Too close to the active baseline; useful as anchor only. |
| artifacts/lucifer_baseline_repro_joezzzzz_v1/submission_pre_gold.csv | anchor_or_duplicate | HOLD_DUPLICATE | HOLD_DUPLICATE | likely_around_7p235_low_upside | 0 | 0.0360878 | 7.06814e-05 | Too close to the active baseline; useful as anchor only. |
| artifacts/lucifer_baseline_repro_joezzzzz_v1/submission_public_self_verified.csv | anchor_or_duplicate | HOLD_DUPLICATE | HOLD_DUPLICATE | likely_around_7p235_low_upside | 0 | 0.0360878 | 7.06814e-05 | Too close to the active baseline; useful as anchor only. |
| artifacts/lucifer_baseline_repro_joezzzzz_v1/fleongg_pretrained_submission.csv | learned_signal | HOLD_PENDING_ANCHOR | LOCAL_CANDIDATE | plausible_7p2_to_7p8_band | 3.68124 | 0.125039 | 0 | Learned-signal value should be interpreted after active baseline score resolves. |
| artifacts/fleongg_branch_calibration_joezzzzz_v2/fleongg_pretrained_submission.csv | learned_signal | HOLD_PENDING_ANCHOR | LOCAL_CANDIDATE | plausible_7p2_to_7p8_band | 3.92105 | 0.124812 | 0 | Learned-signal value should be interpreted after active baseline score resolves. |
| artifacts/fleongg_branch_calibration_joezzzzz_v1/fleongg_pretrained_submission.csv | learned_signal | HOLD_PENDING_ANCHOR | LOCAL_CANDIDATE | plausible_7p2_to_7p8_band | 3.92669 | 0.123879 | 0 | Learned-signal value should be interpreted after active baseline score resolves. |
| artifacts/kernel_outputs/rogii-baidalin-7-201-preflight-codex_v1/fleongg_pretrained_submission.csv | learned_signal | HOLD_PENDING_ANCHOR | LOCAL_CANDIDATE | plausible_7p2_to_7p8_band | 3.93987 | 0.124027 | 0 | Learned-signal value should be interpreted after active baseline score resolves. |

## Recommendation

Do not spend another official slot on dependent variants until pending scores or reference kernels resolve.
Continue polling, then audit completed kernel outputs before promoting any reference branch.

## Outputs

- `experiments/next_batch_readiness.csv`
