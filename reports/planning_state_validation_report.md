# Planning State Validation

This report validates consistency between polling, readiness, audit summary, batch plan, and release gate state.

## Overall

- Status: `PASS`
- Error failures: `0`
- Warning failures: `0`

## Counts

| severity | status | count |
| --- | --- | --- |
| ERROR | PASS | 38 |
| INFO | PASS | 3 |

## Checks

| check | severity | status | detail |
| --- | --- | --- | --- |
| input_poll_summary_exists | ERROR | PASS | poll refresh summary is readable |
| input_readiness_exists | ERROR | PASS | next-batch readiness CSV is readable |
| input_audit_summary_exists | ERROR | PASS | candidate audit summary CSV is readable |
| input_plan_exists | ERROR | PASS | next submission batch plan CSV is readable |
| input_well_impact_summary_exists | ERROR | PASS | planned candidate well-impact summary CSV is readable |
| input_candidate_diversity_summary_exists | ERROR | PASS | planned candidate diversity summary CSV is readable |
| input_planned_slot_review_exists | ERROR | PASS | planned slot review CSV is readable |
| input_planned_slot_contingency_exists | ERROR | PASS | planned slot contingency CSV is readable |
| input_planned_slot_replacement_pool_exists | ERROR | PASS | planned slot replacement pool CSV is readable |
| input_release_gate_exists | ERROR | PASS | submission release gate CSV is readable |
| input_artifact_manifest_summary_exists | ERROR | PASS | candidate artifact manifest summary CSV is readable |
| input_final_submission_package_summary_exists | ERROR | PASS | final submission package summary CSV is readable |
| input_result_application_plan_exists | ERROR | PASS | result application plan CSV is readable |
| planned_slots_within_daily_limit | ERROR | PASS | planned slots=5; daily official limit=5 |
| planned_slots_have_release_rows | ERROR | PASS | plan-only=[]; release-only=[] |
| planned_slots_have_audit_rows | ERROR | PASS | missing audit rows=[] |
| planned_slots_have_readiness_rows | ERROR | PASS | missing readiness rows=[] |
| planned_slots_have_well_impact_rows | ERROR | PASS | missing well-impact rows=[] |
| planned_slots_have_diversity_rows | ERROR | PASS | missing diversity rows=[] |
| planned_slots_have_slot_review_rows | ERROR | PASS | missing slot-review rows=[] |
| planned_slots_have_artifact_manifest_rows | ERROR | PASS | missing manifest rows=[] |
| planned_slots_have_final_package_rows | ERROR | PASS | missing package rows=[] |
| planned_paths_unique | ERROR | PASS | no duplicate planned submission paths |
| planned_submission_hashes_unique | ERROR | PASS | duplicate planned sha count=0 |
| no_missing_audit_in_candidate_pool | ERROR | PASS | MISSING_AUDIT rows=0 |
| external_context_blocks_release | ERROR | PASS | pending=2; running=1; batch_status=WAIT_EXTERNAL_CONTEXT; gates=['BLOCKED_EXTERNAL_CONTEXT'] |
| blocked_plan_does_not_submit | ERROR | PASS | current actions=['do_not_submit_yet'] |
| no_unapplied_poll_updates | INFO | PASS | poll refresh detected no unapplied kernel/submission updates |
| planned_slots_have_passing_audit_gate | ERROR | PASS | nonpassing planned audit rows=0 |
| planned_slots_have_impact_buckets | ERROR | PASS | well-impact rows=5; buckets=['BROAD', 'SINGLE_WELL_DOMINATED'] |
| planned_slots_have_diversity_flags | ERROR | PASS | diversity rows=5; flags=['OK', 'REDUNDANT_REVIEW'] |
| planned_slots_have_slot_reviews | ERROR | PASS | slot-review rows=5; reviews=['HOLD_EXTERNAL_CONTEXT'] |
| required_slot_contingency_scenarios_exist | ERROR | PASS | missing scenarios=[] |
| slot_contingency_new_candidate_needs_are_numeric | ERROR | PASS | new_candidate_needed values=['0', '0', '2', '4', '0', '0', '2'] |
| pending_context_has_wait_no_submit_contingency | ERROR | PASS | contingency actions=['BLOCK_ALL_DEPENDENT_SLOTS', 'FINAL_REVIEW_BLEND_SWEEP', 'FOLLOW_SCORE_BRANCH_WITHOUT_DEGNONGUIDI', 'INSERT_DEGNONGUIDI_AND_RERANK', 'KEEP_ONE_BLEND_FIND_REPLACEMENTS', 'PARTIAL_RELEASE_NEEDS_REPLACEMENTS', 'WAIT_NO_SUBMIT'] |
| replacement_pool_roles_available | INFO | PASS | replacement roles=['already_planned', 'alternate_blend_weight_only', 'backup_projection_review', 'conservative_low_upside_backup', 'do_not_use_duplicate', 'pending_equivalent_not_replacement'] |
| planned_slots_have_valid_artifact_manifests | ERROR | PASS | nonpassing planned manifest rows=0; manifest rows=5 |
| planned_slots_have_no_final_package_failures | ERROR | PASS | failing planned package rows=0; package rows=5 |
| blocked_release_blocks_final_packaging | ERROR | PASS | package gates while external context pending=['BLOCKED_RELEASE_GATE'] |
| pending_context_has_result_application_blockers | ERROR | PASS | blocking result-application rows=4 |
| no_slots_ready_for_submit | INFO | PASS | no planned slot is currently releasable |

## Outputs

- `experiments/planning_state_validation.csv`
- `reports/planning_state_validation_report.md`
