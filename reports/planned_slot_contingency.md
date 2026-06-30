# Planned Slot Contingency

This report defines what to do with the current planned official slots after pending scores or kernel results resolve. It does not submit to Kaggle.

## Action Counts

| release_action | count |
| --- | --- |
| WAIT_NO_SUBMIT | 1 |
| FINAL_REVIEW_BLEND_SWEEP | 1 |
| PARTIAL_RELEASE_NEEDS_REPLACEMENTS | 1 |
| BLOCK_ALL_DEPENDENT_SLOTS | 1 |
| INSERT_DEGNONGUIDI_AND_RERANK | 1 |
| FOLLOW_SCORE_BRANCH_WITHOUT_DEGNONGUIDI | 1 |
| KEEP_ONE_BLEND_FIND_REPLACEMENTS | 1 |

## Scenario Matrix

| scenario_id | trigger | release_action | keep_slots | review_slots | replace_slots | drop_slots | official_slot_target | new_candidate_needed | replacement_candidates | rationale | next_command |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S01_no_external_change | No new official score and Degnonguidi remains non-terminal. | WAIT_NO_SUBMIT | 1, 2, 3, 4, 5 | 1, 2, 3, 4, 5 |  |  | 0 now | 0 |  | Current release gate is blocked by external context; keep preparing but do not spend official slots. | python3 scripts/poll_and_refresh_state.py |
| S02_baseline_valid_fleongg_competitive | Baseline anchor scores in the expected band and Fleongg is competitive enough to justify ensemble calibration. | FINAL_REVIEW_BLEND_SWEEP | 1, 2, 3, 4 | 5 |  |  | 4-5 after gates clear | 0 |  | The three blend slots are redundant but acceptable if the explicit question is the low-dimensional blend curve. | python3 scripts/final_submission_package.py --prepare --planned-slot N |
| S03_baseline_valid_fleongg_weak | Baseline anchor is valid but Fleongg is materially worse than the active baseline. | PARTIAL_RELEASE_NEEDS_REPLACEMENTS | 1, 4, 5 | 4 | 2, 3 | 2, 3 | 2-3 current slots plus 1-2 replacements | 2 | artifacts/baidalin_preflight_redownload_v1/sp45_projection_submission.csv; artifacts/rogii_baidalin_7_201_preflight_codex_v1_sp45_projection_submission/submission.csv; artifacts/sp45_projection_slot1_codex_v1/fleongg_pretrained_submission.csv; artifacts/sp45_projection_slot1_codex_v1/sp45_projection_submission.csv | If learned signal is weak, submitting three nearby learned blends wastes slots; keep at most one as an information point. | rerun candidate generation or promote a reviewed replacement before trying to use 4-5 slots |
| S04_baseline_anchor_failed | Baseline anchor is blank, catastrophic, or far outside the expected reference band. | BLOCK_ALL_DEPENDENT_SLOTS |  |  | 1, 2, 3, 4, 5 | 1, 2, 3, 4, 5 | 0 until baseline repaired | 4 |  | All planned candidates depend on the active-account anchor being trustworthy. | repair baseline reproduction and rerun audit before any official submission |
| S05_degnonguidi_complete_clean | Degnonguidi v6 reaches COMPLETE and its downloaded output passes deep audit with distinct signal. | INSERT_DEGNONGUIDI_AND_RERANK | 1 | 4, 5 | 5, 2, 3 |  | 4-5 after rerank | 0 | audited Degnonguidi output | A clean 7.159-family output should outrank a sparse plateau slot and at least one redundant blend. | python3 scripts/audit_kernel_output.py --kernel joezzzzz/rogii-degnonguidi-7159-preflight-codex --force-download |
| S06_degnonguidi_error_or_deferred | Degnonguidi v6 fails, stalls beyond usefulness, or is explicitly deferred. | FOLLOW_SCORE_BRANCH_WITHOUT_DEGNONGUIDI | 1, 2, 3, 4, 5 | 2, 3, 4 |  |  | depends on Fleongg branch | 0 | artifacts/baidalin_preflight_redownload_v1/sp45_projection_submission.csv; artifacts/rogii_baidalin_7_201_preflight_codex_v1_sp45_projection_submission/submission.csv; artifacts/sp45_projection_slot1_codex_v1/fleongg_pretrained_submission.csv; artifacts/sp45_projection_slot1_codex_v1/sp45_projection_submission.csv | Do not let a blocked reference kernel stop unrelated audited Baidalin/SP45 decisions once score dependencies resolve. | record kernel decision, rerun poll_and_refresh_state.py, then follow S02 or S03 |
| S07_gates_clear_but_redundancy_unresolved | Release gates clear, but the batch question is not explicitly a blend-curve calibration sweep. | KEEP_ONE_BLEND_FIND_REPLACEMENTS | 1, 4, 5 | 4 | 2, 3 | 2, 3 | 4-5 only after replacements exist | 2 | artifacts/baidalin_preflight_redownload_v1/sp45_projection_submission.csv; artifacts/rogii_baidalin_7_201_preflight_codex_v1_sp45_projection_submission/submission.csv; artifacts/sp45_projection_slot1_codex_v1/fleongg_pretrained_submission.csv; artifacts/sp45_projection_slot1_codex_v1/sp45_projection_submission.csv | The daily 4-5 slot target should not force multiple near-duplicate submissions unless they answer a named sweep question. | use replacement pool or build a new structural candidate before packaging redundant slots |

## Replacement Pool

| path | family | readiness_status | estimated_public_band | rmse_to_current_best_7p235 | replacement_role | replacement_rank | replacement_reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| artifacts/baidalin_preflight_redownload_v1/sp45_projection_submission.csv | projection_branch | HOLD_PENDING_CONTEXT | plausible_7p2_to_7p8_band | 1.45864 | backup_projection_review | 78 | Backup projection branch; review source/output distance before replacing a slot. |
| artifacts/rogii_baidalin_7_201_preflight_codex_v1_sp45_projection_submission/submission.csv | projection_branch | HOLD_PENDING_CONTEXT | plausible_7p2_to_7p8_band | 1.45864 | backup_projection_review | 78 | Backup projection branch; review source/output distance before replacing a slot. |
| artifacts/sp45_projection_slot1_codex_v1/fleongg_pretrained_submission.csv | projection_branch | HOLD_PENDING_CONTEXT | plausible_7p2_to_7p8_band | 3.96196 | backup_projection_review | 78 | Backup projection branch; review source/output distance before replacing a slot. |
| artifacts/sp45_projection_slot1_codex_v1/sp45_projection_submission.csv | projection_branch | HOLD_PENDING_CONTEXT | plausible_7p2_to_7p8_band | 2.31466 | backup_projection_review | 78 | Backup projection branch; review source/output distance before replacing a slot. |
| artifacts/sp45_projection_slot1_codex_v1/submission.csv | projection_branch | HOLD_PENDING_CONTEXT | plausible_7p2_to_7p8_band | 2.31466 | backup_projection_review | 78 | Backup projection branch; review source/output distance before replacing a slot. |
| artifacts/fleongg_branch_calibration_joezzzzz_v1/sp45_projection_submission.csv | projection_branch | HOLD_PENDING_CONTEXT | unknown_possible_but_risky | 5.79449 | backup_projection_review | 70 | Backup projection branch; review source/output distance before replacing a slot. |
| artifacts/fleongg_branch_calibration_joezzzzz_v2/sp45_projection_submission.csv | projection_branch | HOLD_PENDING_CONTEXT | unknown_possible_but_risky | 5.79449 | backup_projection_review | 70 | Backup projection branch; review source/output distance before replacing a slot. |
| artifacts/lucifer_baseline_repro_joezzzzz_v1/sp45_projection_submission.csv | projection_branch | HOLD_PENDING_CONTEXT | unknown_possible_but_risky | 5.79449 | backup_projection_review | 70 | Backup projection branch; review source/output distance before replacing a slot. |
| artifacts/baidalin_preflight_redownload_v1/submission_sp45_fleongg_w0.50.csv | projection_learned_blend | HOLD_PENDING_CONTEXT | plausible_7p2_to_7p8_band | 2.42452 | alternate_blend_weight_only | 53 | Another nearby blend weight; useful only for a deliberate blend curve. |
| artifacts/baidalin_preflight_redownload_v1/submission_sp45_fleongg_w0.52.csv | projection_learned_blend | HOLD_PENDING_CONTEXT | plausible_7p2_to_7p8_band | 2.36963 | alternate_blend_weight_only | 53 | Another nearby blend weight; useful only for a deliberate blend curve. |

## Interpretation

- Keep all slots blocked while external context is pending.
- If Fleongg is competitive, the three blend slots can be kept only as an explicit calibration sweep.
- If Fleongg is weak, keep at most one blend and create or promote replacements before trying to use 4-5 official slots.
- If Degnonguidi completes cleanly, insert it ahead of sparse or redundant slots after audit.

## Outputs

- `experiments/planned_slot_contingency.csv`
- `experiments/planned_slot_replacement_pool.csv`
- `reports/planned_slot_contingency.md`
