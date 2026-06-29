# Candidate Audit Summary

This report joins next-batch readiness with local audit JSON evidence.

## Counts

- Candidates tracked: `22`
- Audited candidates waiting on external context: `13`
- Candidates missing audit evidence: `0`

## Audit Gates

| audit_gate | count |
| --- | --- |
| AUDIT_PASS_WARN_REVIEW | 19 |
| AUDIT_PASS | 3 |

## Submission Gates

| submission_gate | count |
| --- | --- |
| AUDITED_WAIT_CONTEXT | 13 |
| HOLD_DUPLICATE | 6 |
| HOLD_LOW_UPSIDE | 2 |
| HOLD_INFORMATION_SLOT | 1 |

## Ranked Candidates

| path | family | submission_gate | readiness_status | audit_gate | estimated_public_band | novelty_bucket | rmse_to_current_best_7p235 | audit_rmse_to_fleongg_pending | anchor_first_abs_p90 | jump_rate_abs_slope_gt3 | cv_mean_delta |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| artifacts/lucifer_baseline_repro_joezzzzz_v1/fleongg_pretrained_submission.csv | learned_signal | AUDITED_WAIT_CONTEXT | WAIT_OFFICIAL_SCORE | AUDIT_PASS | plausible_7p2_to_7p8_band | high | 3.68124 |  | 0.125039 | 0 |  |
| artifacts/gr_typewell_light_alpha010_v1/submission.csv | gr_typewell_light | HOLD_LOW_UPSIDE | HOLD_LOW_UPSIDE | AUDIT_PASS | likely_around_7p235_low_upside | low | 0.349534 |  | 0.0360878 | 7.06814e-05 |  |
| artifacts/gr_typewell_light_alpha020_v1/submission.csv | gr_typewell_light | HOLD_LOW_UPSIDE | HOLD_LOW_UPSIDE | AUDIT_PASS | likely_around_7p235_low_upside | low | 0.699067 |  | 0.0360878 | 7.06814e-05 |  |
| artifacts/kernel_outputs/rogii-baidalin-7-201-preflight-codex_v1/sp45_projection_submission.csv | projection_branch | AUDITED_WAIT_CONTEXT | HOLD_PENDING_CONTEXT | AUDIT_PASS_WARN_REVIEW | plausible_7p2_to_7p8_band | moderate | 1.45864 | 3.42373 | 6.39778 | 0 |  |
| artifacts/kernel_outputs/rogii-baidalin-7-201-preflight-codex_v1/submission_sp45_fleongg_w0.60.csv | projection_learned_blend | AUDITED_WAIT_CONTEXT | HOLD_PENDING_CONTEXT | AUDIT_PASS_WARN_REVIEW | plausible_7p2_to_7p8_band | moderate | 2.15794 | 2.09107 | 3.85775 | 0 |  |
| artifacts/kernel_outputs/rogii-baidalin-7-201-preflight-codex_v1/submission_sp45_fleongg_w0.58.csv | projection_learned_blend | AUDITED_WAIT_CONTEXT | HOLD_PENDING_CONTEXT | AUDIT_PASS_WARN_REVIEW | plausible_7p2_to_7p8_band | moderate | 2.20956 | 2.02586 | 3.73075 | 0 |  |
| artifacts/kernel_outputs/rogii-baidalin-7-201-preflight-codex_v1/submission_sp45_fleongg_w0.55.csv | projection_learned_blend | AUDITED_WAIT_CONTEXT | HOLD_PENDING_CONTEXT | AUDIT_PASS_WARN_REVIEW | plausible_7p2_to_7p8_band | moderate | 2.28867 | 1.9285 | 3.54025 | 0 |  |
| artifacts/kernel_outputs/rogii-baidalin-7-201-preflight-codex_v1/submission_sp45_fleongg_w0.52.csv | projection_learned_blend | AUDITED_WAIT_CONTEXT | HOLD_PENDING_CONTEXT | AUDIT_PASS_WARN_REVIEW | plausible_7p2_to_7p8_band | moderate | 2.36963 | 1.83176 | 3.34974 | 0 |  |
| artifacts/kernel_outputs/rogii-baidalin-7-201-preflight-codex_v1/submission_sp45_fleongg_w0.50.csv | projection_learned_blend | AUDITED_WAIT_CONTEXT | HOLD_PENDING_CONTEXT | AUDIT_PASS_WARN_REVIEW | plausible_7p2_to_7p8_band | moderate | 2.42452 | 1.76765 | 3.22274 | 0 |  |
| artifacts/fleongg_branch_calibration_joezzzzz_v1/sp45_projection_submission.csv | projection_branch | AUDITED_WAIT_CONTEXT | HOLD_PENDING_CONTEXT | AUDIT_PASS_WARN_REVIEW | unknown_possible_but_risky | high | 5.79449 | 3.16788 | 2.65079 | 0 |  |
| artifacts/fleongg_branch_calibration_joezzzzz_v2/sp45_projection_submission.csv | projection_branch | AUDITED_WAIT_CONTEXT | HOLD_PENDING_CONTEXT | AUDIT_PASS_WARN_REVIEW | unknown_possible_but_risky | high | 5.79449 | 3.16788 | 2.65079 | 0 |  |
| artifacts/lucifer_baseline_repro_joezzzzz_v1/sp45_projection_submission.csv | projection_branch | AUDITED_WAIT_CONTEXT | HOLD_PENDING_CONTEXT | AUDIT_PASS_WARN_REVIEW | unknown_possible_but_risky | high | 5.79449 | 3.16788 | 2.65079 | 0 |  |
| artifacts/fleongg_branch_calibration_joezzzzz_v2/fleongg_pretrained_submission.csv | learned_signal | AUDITED_WAIT_CONTEXT | WAIT_OFFICIAL_SCORE | AUDIT_PASS_WARN_REVIEW | plausible_7p2_to_7p8_band | high | 3.92105 | 0 | 0.124812 | 0 |  |
| artifacts/fleongg_branch_calibration_joezzzzz_v1/fleongg_pretrained_submission.csv | learned_signal | AUDITED_WAIT_CONTEXT | WAIT_OFFICIAL_SCORE | AUDIT_PASS_WARN_REVIEW | plausible_7p2_to_7p8_band | high | 3.92669 | 0.215134 | 0.123879 | 0 |  |
| artifacts/kernel_outputs/rogii-baidalin-7-201-preflight-codex_v1/fleongg_pretrained_submission.csv | learned_signal | AUDITED_WAIT_CONTEXT | WAIT_OFFICIAL_SCORE | AUDIT_PASS_WARN_REVIEW | plausible_7p2_to_7p8_band | high | 3.93987 | 0.64874 | 0.124027 | 0 |  |
| artifacts/plateau_recent_quantile_v1/submission.csv | plateau_signal | HOLD_INFORMATION_SLOT | HOLD_INFORMATION_SLOT | AUDIT_PASS_WARN_REVIEW | unknown_possible_but_risky | high | 4.72239 | 4.43798 | 3.28521 | 7.06814e-05 | -0.407934 |
| artifacts/lucifer_baseline_repro_joezzzzz_v1/submission.csv | anchor_or_duplicate | HOLD_DUPLICATE | HOLD_DUPLICATE | AUDIT_PASS_WARN_REVIEW | likely_around_7p235_low_upside | duplicate | 0 | 3.92105 | 0.0360878 | 7.06814e-05 |  |
| artifacts/lucifer_baseline_repro_joezzzzz_v1/submission_gold_prefix_aggressive.csv | anchor_or_duplicate | HOLD_DUPLICATE | HOLD_DUPLICATE | AUDIT_PASS_WARN_REVIEW | likely_around_7p235_low_upside | duplicate | 0 | 3.92105 | 0.0360878 | 7.06814e-05 |  |
| artifacts/lucifer_baseline_repro_joezzzzz_v1/submission_gold_prefix_balanced.csv | anchor_or_duplicate | HOLD_DUPLICATE | HOLD_DUPLICATE | AUDIT_PASS_WARN_REVIEW | likely_around_7p235_low_upside | duplicate | 0 | 3.92105 | 0.0360878 | 7.06814e-05 |  |
| artifacts/lucifer_baseline_repro_joezzzzz_v1/submission_gold_prefix_conservative.csv | anchor_or_duplicate | HOLD_DUPLICATE | HOLD_DUPLICATE | AUDIT_PASS_WARN_REVIEW | likely_around_7p235_low_upside | duplicate | 0 | 3.92105 | 0.0360878 | 7.06814e-05 |  |
| artifacts/lucifer_baseline_repro_joezzzzz_v1/submission_pre_gold.csv | anchor_or_duplicate | HOLD_DUPLICATE | HOLD_DUPLICATE | AUDIT_PASS_WARN_REVIEW | likely_around_7p235_low_upside | duplicate | 0 | 3.92105 | 0.0360878 | 7.06814e-05 |  |
| artifacts/lucifer_baseline_repro_joezzzzz_v1/submission_public_self_verified.csv | anchor_or_duplicate | HOLD_DUPLICATE | HOLD_DUPLICATE | AUDIT_PASS_WARN_REVIEW | likely_around_7p235_low_upside | duplicate | 0 | 3.92105 | 0.0360878 | 7.06814e-05 |  |

## Outputs

- `experiments/candidate_audit_summary.csv`
- `reports/candidate_audit_summary_report.md`
