# Planned Candidate Diversity

This report measures pairwise output diversity among planned submission slots. It is local validation only and does not submit to Kaggle.

## Redundancy Buckets

| redundancy_bucket | count |
| --- | --- |
| DIRECTIONALLY_DIVERSE | 4 |
| MODERATE_INCREMENT | 3 |
| RELATED_LOW_INCREMENT | 2 |
| NEAR_DUPLICATE | 1 |

## Candidate Summary

| planned_slot | candidate_id | family | min_pair_rmse | max_diff_corr | redundant_pair_count | most_similar_slot | diversity_flag |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | rogii_baidalin_7_201_preflight_codex_v1_sp45_projection_submission | projection_branch | 1.71662 | 0.729134 | 0 | 2 | OK |
| 2 | rogii_baidalin_7_201_preflight_codex_v1_submission_sp45_fleongg_w0_50 | projection_learned_blend | 0.702226 | 0.966929 | 2 | 3 | REDUNDANT_REVIEW |
| 3 | sp45_projection_slot1_codex_v1_submission_sp45_fleongg_w0_55 | projection_learned_blend | 0.159696 | 0.998497 | 2 | 4 | REDUNDANT_REVIEW |
| 4 | sp45_projection_slot1_codex_v1_submission_sp45_fleongg_w0_60 | projection_learned_blend | 0.159696 | 0.998497 | 2 | 3 | REDUNDANT_REVIEW |
| 5 | plateau_recent_quantile_v1_submission | plateau_signal | 4.02266 | 0.64703 | 0 | 2 | OK |

## Pairwise Distances

| left_slot | right_slot | left_family | right_family | pair_rmse | diff_corr_vs_baseline | same_direction_frac | redundancy_bucket |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | 5 | projection_learned_blend | plateau_signal | 4.02266 | 0.64703 | 0.258074 | DIRECTIONALLY_DIVERSE |
| 1 | 5 | projection_branch | plateau_signal | 4.29244 | 0.470765 | 0.263939 | DIRECTIONALLY_DIVERSE |
| 3 | 5 | projection_learned_blend | plateau_signal | 4.3003 | 0.571608 | 0.276023 | DIRECTIONALLY_DIVERSE |
| 4 | 5 | projection_learned_blend | plateau_signal | 4.31982 | 0.558568 | 0.280334 | DIRECTIONALLY_DIVERSE |
| 1 | 2 | projection_branch | projection_learned_blend | 1.71662 | 0.726826 | 0.759522 | MODERATE_INCREMENT |
| 1 | 4 | projection_branch | projection_learned_blend | 1.91553 | 0.729134 | 0.766801 | MODERATE_INCREMENT |
| 1 | 3 | projection_branch | projection_learned_blend | 2.02121 | 0.709909 | 0.756272 | MODERATE_INCREMENT |
| 3 | 4 | projection_learned_blend | projection_learned_blend | 0.159696 | 0.998497 | 0.987916 | NEAR_DUPLICATE |
| 2 | 3 | projection_learned_blend | projection_learned_blend | 0.702226 | 0.966929 | 0.950958 | RELATED_LOW_INCREMENT |
| 2 | 4 | projection_learned_blend | projection_learned_blend | 0.748133 | 0.955951 | 0.93958 | RELATED_LOW_INCREMENT |

## Interpretation

- `NEAR_DUPLICATE`, `HIGHLY_REDUNDANT`, and `RELATED_LOW_INCREMENT` pairs should not both be submitted unless they answer a deliberate calibration-sweep question.
- High correlation among blend weights is expected, but it reduces information value if daily slots are scarce.
- Diverse candidates can still be bad; this report only checks redundancy, not hidden-label accuracy.

## Outputs

- `experiments/planned_candidate_diversity.csv`
- `experiments/planned_candidate_diversity_summary.csv`
- `reports/planned_candidate_diversity_report.md`
