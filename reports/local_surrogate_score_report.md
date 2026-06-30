# ROGII Local Surrogate Score Report

This report scores already-generated submission CSV files without using hidden labels.
It cannot replace Kaggle Public LB, but it helps reject implausible candidates before spending limited submissions.

## Inputs
- Data dir: `D:\Codex\kaggle\rogii-wellbore\data`
- Valid submission files scored: `85`
- Known public-score calibration rows: `10`

## Important Limitation

A submission CSV only contains hidden-row predictions, so true prefix RMSE cannot be computed from a CSV alone.
Instead, the script computes visible-prefix compatibility: first hidden prediction vs last `TVT_input`, slope continuity, jump rate, typewell range checks, and distances to known scored references.

## Best Known Public Scores In This Scan

| path | known_public_score | risk_grade | rmse_to_current_best_7p235 | anchor_first_abs_p90 | jump_rate_abs_slope_gt3 |
| --- | --- | --- | --- | --- | --- |
| artifacts/sunny_physical_output/submission.csv | 7.235 | near_duplicate_low_upside | 0 | 0.0360878 | 7.06814e-05 |
| artifacts/david_v12_output/submission.csv | 7.263 | near_duplicate_low_upside | 0.00525135 | 0.036 | 7.06814e-05 |
| artifacts/fleongg_v5_output/submission_sp45_fleongg_w0.52.csv | 7.588 | plausible_submit_candidate | 2.5788 | 3.32816 | 0 |
| artifacts/fleongg_v5_output/submission_sp45_fleongg_w0.55.csv | 7.599 | plausible_submit_candidate | 2.5224 | 3.51742 | 0 |
| artifacts/fleongg_v5_output/submission_sp45_fleongg_w0.58.csv | 7.606 | plausible_submit_candidate | 2.46765 | 3.70667 | 0 |
| artifacts/david_fastcpu_output/submission.csv | 7.703 | plausible_submit_candidate | 3.88329 | 1.47903 | 0 |
| artifacts/nickson_v5_artifact_output/submission.csv | 20.579 | reject_known_bad | 10.5909 | 0.0526 | 0 |
| artifacts/wellbore_direct_overlap_output/submission.csv | 11552 | reject_known_bad | 199.917 | 962.294 | 7.06814e-05 |
| artifacts/kokinn_7159_ref_output/submission.csv | 15357.2 | reject_known_bad | 0 | 0.0360878 | 7.06814e-05 |
| artifacts/ourmatch_7159_output/submission.csv | 15357.2 | reject_known_bad | 0.00525135 | 0.036 | 7.06814e-05 |

## Top Unknown Candidates By Surrogate

| path | risk_grade | estimated_public_band | rmse_to_current_best_7p235 | nearest_known_public_score | rmse_to_nearest_known | anchor_first_abs_p90 | jump_rate_abs_slope_gt3 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| artifacts/aevion_lb52_fixed_v4_output/submission.csv | high_shape_risk | do_not_submit | 69.5323 | 7.235 | 69.5323 | 136.732 | 0 |
| artifacts/aevion_lb52_fixed_v4_output/submission_enhanced.csv | high_shape_risk | do_not_submit | 69.5323 | 7.235 | 69.5323 | 136.732 | 0 |
| artifacts/ourmatch_7159_output/_debug/submission_B.csv | medium_unknown | unknown_possible_but_risky | 10.0969 | 7.703 | 6.79513 | 0.0479383 | 0 |
| artifacts/henry_tabicl_artifact_output/submission.csv | medium_unknown | unknown_possible_but_risky | 10.7002 | 20.579 | 1.88017 | 0.005 | 0 |
| artifacts/david_fastcpu_output/submission_model_package_only.csv | medium_unknown | unknown_high_variance | 16.2641 | 7.235 | 16.2641 | 3.33424 | 0 |
| artifacts/emanuell_physics_output/submission.csv | near_duplicate_low_upside | near_known_7.235 | 0 | 7.235 | 0 | 0.0360878 | 7.06814e-05 |
| artifacts/emanuell_physics_output/submission_gold_prefix_aggressive.csv | near_duplicate_low_upside | near_known_7.235 | 0 | 7.235 | 0 | 0.0360878 | 7.06814e-05 |
| artifacts/emanuell_physics_output/submission_gold_prefix_balanced.csv | near_duplicate_low_upside | near_known_7.235 | 0 | 7.235 | 0 | 0.0360878 | 7.06814e-05 |
| artifacts/emanuell_physics_output/submission_gold_prefix_conservative.csv | near_duplicate_low_upside | near_known_7.235 | 0 | 7.235 | 0 | 0.0360878 | 7.06814e-05 |
| artifacts/emanuell_physics_output/submission_public_self_verified.csv | near_duplicate_low_upside | near_known_7.235 | 0 | 7.235 | 0 | 0.0360878 | 7.06814e-05 |
| artifacts/kokinn_gold_aggressive_output/submission.csv | near_duplicate_low_upside | near_known_7.235 | 0 | 7.235 | 0 | 0.0360878 | 7.06814e-05 |
| artifacts/kokinn_gold_balanced_output/submission.csv | near_duplicate_low_upside | near_known_7.235 | 0 | 7.235 | 0 | 0.0360878 | 7.06814e-05 |
| artifacts/lightning_self_verifying_output/submission.csv | near_duplicate_low_upside | near_known_7.235 | 0 | 7.235 | 0 | 0.0360878 | 7.06814e-05 |
| artifacts/needless_sel15_vc_spread55_output/submission.csv | near_duplicate_low_upside | near_known_7.235 | 0 | 7.235 | 0 | 0.0360878 | 7.06814e-05 |
| artifacts/ourmatch_7159_output/_debug/submission_dual_pipeline_blend.csv | near_duplicate_low_upside | near_known_7.235 | 0 | 7.235 | 0 | 0.0360878 | 7.06814e-05 |
| artifacts/boristown_lb7295_output/submission.csv | near_duplicate_low_upside | near_known_7.263 | 0.00525135 | 7.263 | 0 | 0.036 | 7.06814e-05 |
| artifacts/boristown_lb7295_output/v12_latest_valid_submission.csv | near_duplicate_low_upside | near_known_7.263 | 0.00525135 | 7.263 | 0 | 0.036 | 7.06814e-05 |
| artifacts/submission_space_blends/submission_knownscore_70_20_10_backup.csv | near_duplicate_low_upside | likely_around_7p235_low_upside | 0.126272 | 7.263 | 0.125724 | 0.182 | 7.06814e-05 |
| artifacts/fleongg_v5_output/submission.csv | plausible_submit_candidate | plausible_7p2_to_7p8_band | 1.2615 | 7.606 | 1.20703 | 1.75871 | 7.06814e-05 |
| artifacts/target_free_v3_error_output/submission_projected_ridge_pf_projection_d4_b075_raw.csv | plausible_submit_candidate | plausible_7p2_to_7p8_band | 1.53725 | 7.606 | 1.36985 | 0.0272429 | 7.06814e-05 |
| artifacts/fleongg_v5_output/sp45_projection_submission.csv | plausible_submit_candidate | plausible_7p2_to_7p8_band | 1.94509 | 7.606 | 1.19082 | 6.35626 | 0 |
| artifacts/target_free_v3_error_output/projected_ridge_pf_projection_submission.csv | plausible_submit_candidate | plausible_7p2_to_7p8_band | 1.98873 | 7.606 | 1.1643 | 6.09684 | 0 |
| artifacts/target_free_v3_error_output/submission_projected_ridge_pf_projection_d4_b075.csv | plausible_submit_candidate | plausible_7p2_to_7p8_band | 1.98873 | 7.606 | 1.1643 | 6.09684 | 0 |
| artifacts/target_free_v3_error_output/submission_projected_ridge_pf_projection_d4_b075_projected.csv | plausible_submit_candidate | plausible_7p2_to_7p8_band | 1.98873 | 7.606 | 1.1643 | 6.09684 | 0 |
| artifacts/lightning_self_verifying_output/sp45_projection_submission.csv | plausible_submit_candidate | plausible_7p2_to_7p8_band | 2.12687 | 7.606 | 1.17264 | 6.31995 | 0 |

## Recommended Use

1. Run this script after every new kernel output is downloaded.
2. Do not submit candidates marked `reject_known_bad`, `reject_far_from_best`, or `high_shape_risk` unless there is a specific reason.
3. Treat `near_duplicate_low_upside` as safe but unlikely to improve public LB.
4. Prioritize `plausible_submit_candidate` candidates that are not too far from the current best and have low jump/anchor risk.

## Output Files

- `experiments/local_surrogate_scores.csv`
- `experiments/local_surrogate_pairwise_distance.csv`