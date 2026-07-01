# Full-Data Router Matrix Report

This is the first full-train candidate-path matrix and learned-prior router CV.
It is not a submission package.

## Run Config

- data_dir: `data/rogii`
- splits: native prefix plus `0.50`
- folds: `5` stable well-hash folds
- max_wells: `all`

## Method Summary

| method | splits | eval_rows | weighted_rmse | mean_delta_rmse_vs_baseline | median_delta_rmse_vs_baseline | win_rate_vs_baseline | catastrophic_rate_plus5 | hidden_compatible | router_eligible |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gr_shift__fault_step_recent_level | 1546 | 6330100 | 14.5985 | 0.039709 | 0 | 0.401035 | 0.0194049 | True | False |
| fault_step_recent_level | 1546 | 6330100 | 14.6074 | -0.00553682 | 0 | 0.113195 | 0 | True | False |
| gr_shift__last_value | 1546 | 6330100 | 14.6543 | 0.0779546 | 0 | 0.3674 | 0.0122898 | True | False |
| last_value | 1546 | 6330100 | 14.6844 | 0 | 0 | 0 | 0 | True | True |
| ncc_shift__last_value | 1546 | 6330100 | 14.6844 | 0 | 0 | 0 | 0 | True | False |
| gr_shift__self_corr_prefix_shape | 1546 | 6330100 | 14.7425 | 0.159078 | 0 | 0.370634 | 0.0278137 | True | False |
| piecewise_tail_slope_Z | 1546 | 6330100 | 14.7846 | 0.204276 | 0.29205 | 0.445666 | 0 | True | False |
| piecewise_tail_slope_md | 1546 | 6330100 | 14.8023 | 0.219348 | 0.321479 | 0.441785 | 0 | True | False |
| self_corr_prefix_shape | 1546 | 6330100 | 14.8315 | 0.134505 | 0 | 0.0271669 | 0.0161708 | True | True |
| gr_shift__piecewise_tail_slope_Z | 1546 | 6330100 | 14.8503 | 0.355989 | 0.293722 | 0.44696 | 0.0737387 | True | False |
| gr_shift__piecewise_tail_slope_md | 1546 | 6330100 | 14.8626 | 0.336568 | 0.305966 | 0.443726 | 0.0633894 | True | False |
| ncc_shift__recent_plateau_quantile | 1546 | 6330100 | 15.3467 | 0.470542 | 0.0853821 | 0.426261 | 0.0323415 | True | False |
| recent_plateau_quantile | 1546 | 6330100 | 15.3467 | 0.470542 | 0.0853821 | 0.426261 | 0.0323415 | True | True |
| gr_shift__recent_plateau_quantile | 1546 | 6330100 | 15.371 | 0.530933 | 0.184359 | 0.443079 | 0.076326 | True | False |
| damped_tail_linear_Z | 1546 | 6330100 | 15.8175 | 1.11761 | 0.63555 | 0.398448 | 0.198577 | True | True |
| gr_shift__damped_tail_linear_Z | 1546 | 6330100 | 15.8187 | 1.14812 | 0.904469 | 0.39586 | 0.189521 | True | False |
| gr_shift__damped_tail_linear_ASTNL | 1546 | 6330100 | 15.9688 | 1.21943 | 0.955243 | 0.394567 | 0.199871 | False | False |
| gr_shift__damped_tail_linear_BUDA | 1546 | 6330100 | 15.9718 | 1.2223 | 0.9553 | 0.394567 | 0.200517 | False | False |
| gr_shift__damped_tail_linear_ASTNU | 1546 | 6330100 | 15.9726 | 1.22261 | 0.955244 | 0.394567 | 0.200517 | False | False |
| gr_shift__damped_tail_linear_EGFDU | 1546 | 6330100 | 15.9735 | 1.22322 | 0.95515 | 0.394567 | 0.200517 | False | False |

## Router Summary

| router | splits | eval_rows | weighted_rmse | baseline_weighted_rmse | mean_delta_rmse_vs_baseline | median_delta_rmse_vs_baseline | win_rate_vs_baseline | catastrophic_rate_plus5 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| learned_prior_router | 1546 | 6330100 | 14.6844 | 14.6844 | 0 | 0 | 0 | 0 |

## Router Selection Counts

| selected_method | count |
| --- | --- |
| last_value | 1546 |

## Worst Router Decisions

| validation_fold | well | split | selected_method | router_rmse | baseline_rmse | delta_rmse_vs_baseline | selected_reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 000d7d20 | native_prefix | last_value | 7.45444 | 7.45444 | 0 | fallback_last_value |
| 3 | 7acda2df | native_prefix | last_value | 13.8412 | 13.8412 | 0 | fallback_last_value |
| 3 | 5d7198fd | native_prefix | last_value | 13.3665 | 13.3665 | 0 | fallback_last_value |
| 3 | 5cb483ac | frac_0.50 | last_value | 10.854 | 10.854 | 0 | fallback_last_value |
| 3 | 5cb483ac | native_prefix | last_value | 6.11408 | 6.11408 | 0 | fallback_last_value |
| 3 | 5aa03df7 | frac_0.50 | last_value | 12.422 | 12.422 | 0 | fallback_last_value |
| 3 | 5aa03df7 | native_prefix | last_value | 6.58601 | 6.58601 | 0 | fallback_last_value |
| 3 | 5a1a8fd8 | frac_0.50 | last_value | 11.6054 | 11.6054 | 0 | fallback_last_value |
| 3 | 5a1a8fd8 | native_prefix | last_value | 13.1653 | 13.1653 | 0 | fallback_last_value |
| 3 | 577eec7c | frac_0.50 | last_value | 18.4736 | 18.4736 | 0 | fallback_last_value |
| 3 | 577eec7c | native_prefix | last_value | 18.8753 | 18.8753 | 0 | fallback_last_value |
| 3 | 5567d551 | frac_0.50 | last_value | 6.13954 | 6.13954 | 0 | fallback_last_value |
| 3 | 5567d551 | native_prefix | last_value | 10.2895 | 10.2895 | 0 | fallback_last_value |
| 3 | 54753541 | frac_0.50 | last_value | 27.8908 | 27.8908 | 0 | fallback_last_value |
| 3 | 54753541 | native_prefix | last_value | 16.2228 | 16.2228 | 0 | fallback_last_value |
| 3 | 5305524b | frac_0.50 | last_value | 5.79663 | 5.79663 | 0 | fallback_last_value |

## Learned Method Priors

| method | prior_mean_delta | prior_median_delta | prior_win_rate | prior_catastrophic_rate_plus5 | prior_splits | prior_allowed | validation_fold |
| --- | --- | --- | --- | --- | --- | --- | --- |
| last_value | 0 | 0 | 0 | 0 | 1244 | True | 0 |
| self_corr_prefix_shape | 0.111259 | 0 | 0.0289389 | 0.0136656 | 1244 | False | 0 |
| recent_plateau_quantile | 0.463336 | 0.0824749 | 0.422026 | 0.0337621 | 1244 | False | 0 |
| damped_tail_linear_Z | 1.05997 | 0.557531 | 0.404341 | 0.19373 | 1244 | False | 0 |
| last_value | 0 | 0 | 0 | 0 | 1212 | True | 1 |
| self_corr_prefix_shape | 0.16092 | 0 | 0.0264026 | 0.0189769 | 1212 | False | 1 |
| recent_plateau_quantile | 0.485713 | 0.0829561 | 0.433993 | 0.0338284 | 1212 | False | 1 |
| damped_tail_linear_Z | 1.15578 | 0.665244 | 0.403465 | 0.20462 | 1212 | False | 1 |
| last_value | 0 | 0 | 0 | 0 | 1222 | True | 2 |
| self_corr_prefix_shape | 0.0843076 | 0 | 0.0270049 | 0.0114566 | 1222 | False | 2 |
| recent_plateau_quantile | 0.425152 | 0.0834899 | 0.42635 | 0.0278232 | 1222 | False | 2 |
| damped_tail_linear_Z | 1.14001 | 0.63555 | 0.392799 | 0.194763 | 1222 | False | 2 |
| last_value | 0 | 0 | 0 | 0 | 1284 | True | 3 |
| self_corr_prefix_shape | 0.14179 | 0 | 0.0272586 | 0.0179128 | 1284 | False | 3 |
| recent_plateau_quantile | 0.47238 | 0.0821736 | 0.42757 | 0.0327103 | 1284 | False | 3 |
| damped_tail_linear_Z | 1.11991 | 0.680303 | 0.392523 | 0.197819 | 1284 | False | 3 |
| last_value | 0 | 0 | 0 | 0 | 1222 | True | 4 |
| self_corr_prefix_shape | 0.174514 | 0 | 0.0261866 | 0.0188216 | 1222 | False | 4 |
| recent_plateau_quantile | 0.506289 | 0.0978227 | 0.42144 | 0.0335516 | 1222 | False | 4 |
| damped_tail_linear_Z | 1.11364 | 0.63555 | 0.399345 | 0.202128 | 1222 | False | 4 |

## Interpretation

- This run uses all available train wells unless `--max-wells` is set.
- The router is intentionally simple: out-of-fold method priors plus prefix-holdout evidence.
- Hidden-incompatible train-only formation columns are allowed as diagnostics in the matrix, but labeled explicitly.
- The learned-prior router is stricter than hidden compatibility: it currently allows only conservative release-eligible methods.
- A useful next router should beat `last_value` on weighted RMSE and keep catastrophic-rate low.

## Outputs

- `experiments/full_data_router_candidate_matrix.csv`
- `experiments/full_data_router_method_summary.csv`
- `experiments/full_data_router_choices.csv`
- `experiments/full_data_router_summary.csv`
- `experiments/full_data_router_method_priors.csv`
