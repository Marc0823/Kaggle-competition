# Planned Candidate Well Impact

This report analyzes planned submission candidates per well against the active-account baseline output. It is local validation only and does not submit to Kaggle.

## Impact Buckets

| impact_bucket | count |
| --- | --- |
| BROAD | 2 |
| CONCENTRATED | 2 |
| SINGLE_WELL_DOMINATED | 1 |

## Candidate Summary

| planned_slot | candidate_id | family | impact_bucket | changed_well_count | changed_row_frac | rmse_to_baseline | top_well | top_well_contribution_frac | top_well_rmse_diff |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | rogii_baidalin_7_201_preflight_codex_v1_sp45_projection_submission | projection_branch | BROAD | 3 | 1 | 1.45864 | 00bbac68 | 0.338564 | 1.3019 |
| 2 | rogii_baidalin_7_201_preflight_codex_v1_submission_sp45_fleongg_w0_50 | projection_learned_blend | BROAD | 3 | 1 | 2.42452 | 00bbac68 | 0.437617 | 2.46029 |
| 3 | sp45_projection_slot1_codex_v1_submission_sp45_fleongg_w0_55 | projection_learned_blend | CONCENTRATED | 3 | 1 | 2.73598 | 00bbac68 | 0.618246 | 3.29994 |
| 4 | sp45_projection_slot1_codex_v1_submission_sp45_fleongg_w0_60 | projection_learned_blend | CONCENTRATED | 3 | 1 | 2.65427 | 00bbac68 | 0.638478 | 3.25334 |
| 5 | plateau_recent_quantile_v1_submission | plateau_signal | SINGLE_WELL_DOMINATED | 1 | 0.303936 | 4.72239 | 00e12e8b | 1 | 8.56585 |

## Top Impacted Wells

| planned_slot | candidate_id | well | contribution_frac | rmse_diff | changed_frac | p95_abs_diff | max_abs_diff | mean_signed_diff |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | rogii_baidalin_7_201_preflight_codex_v1_sp45_projection_submission | 00bbac68 | 0.338564 | 1.3019 | 1 | 2.59667 | 4.76804 | 0.323119 |
| 1 | rogii_baidalin_7_201_preflight_codex_v1_sp45_projection_submission | 000d7d20 | 0.33566 | 1.62312 | 1 | 3.29489 | 7.81309 | 0.6049 |
| 1 | rogii_baidalin_7_201_preflight_codex_v1_sp45_projection_submission | 00e12e8b | 0.325775 | 1.51013 | 1 | 3.06144 | 4.0465 | -0.507775 |
| 2 | rogii_baidalin_7_201_preflight_codex_v1_submission_sp45_fleongg_w0_50 | 00bbac68 | 0.437617 | 2.46029 | 1 | 5.53273 | 6.07445 | 0.897835 |
| 2 | rogii_baidalin_7_201_preflight_codex_v1_submission_sp45_fleongg_w0_50 | 00e12e8b | 0.407818 | 2.80846 | 1 | 5.34942 | 6.68331 | 0.382931 |
| 2 | rogii_baidalin_7_201_preflight_codex_v1_submission_sp45_fleongg_w0_50 | 000d7d20 | 0.154564 | 1.83078 | 1 | 3.88664 | 5.25057 | 1.14909 |
| 3 | sp45_projection_slot1_codex_v1_submission_sp45_fleongg_w0_55 | 00bbac68 | 0.618246 | 3.29994 | 1 | 7.39983 | 7.8274 | 1.61113 |
| 3 | sp45_projection_slot1_codex_v1_submission_sp45_fleongg_w0_55 | 00e12e8b | 0.267512 | 2.56681 | 1 | 4.87013 | 5.99194 | 0.185078 |
| 3 | sp45_projection_slot1_codex_v1_submission_sp45_fleongg_w0_55 | 000d7d20 | 0.114242 | 1.77615 | 1 | 4.03108 | 5.09783 | 1.04881 |
| 4 | sp45_projection_slot1_codex_v1_submission_sp45_fleongg_w0_60 | 00bbac68 | 0.638478 | 3.25334 | 1 | 7.18134 | 7.5869 | 1.63895 |
| 4 | sp45_projection_slot1_codex_v1_submission_sp45_fleongg_w0_60 | 00e12e8b | 0.24678 | 2.39171 | 1 | 4.48168 | 5.54404 | 0.0862435 |
| 4 | sp45_projection_slot1_codex_v1_submission_sp45_fleongg_w0_60 | 000d7d20 | 0.114742 | 1.72687 | 1 | 4.00924 | 4.93067 | 0.980958 |
| 5 | plateau_recent_quantile_v1_submission | 00e12e8b | 1 | 8.56585 | 1 | 15.5186 | 15.9286 | -3.33841 |
| 5 | plateau_recent_quantile_v1_submission | 000d7d20 | 0 | 0 | 0 | 0 | 0 | 0 |
| 5 | plateau_recent_quantile_v1_submission | 00bbac68 | 0 | 0 | 0 | 0 | 0 | 0 |

## Interpretation

- `SINGLE_WELL_DOMINATED` or `SPARSE_INFORMATION` candidates can still be useful information slots, but they should not be treated as broad model improvements without stronger evidence.
- `CONCENTRATED` candidates need per-well review before release because leaderboard movement may depend on a small number of wells.
- `BROAD` candidates change many wells and should be checked for hidden-format and physical-shape risk before any official submission.

## Outputs

- `experiments/planned_candidate_well_impact.csv`
- `experiments/planned_candidate_well_impact_summary.csv`
- `reports/planned_candidate_well_impact_report.md`
