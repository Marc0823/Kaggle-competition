# Planning State Validation

This report validates consistency between polling, readiness, audit summary, batch plan, and release gate state.

## Overall

- Status: `PASS`
- Error failures: `0`
- Warning failures: `0`

## Counts

| severity | status | count |
| --- | --- | --- |
| ERROR | PASS | 22 |
| INFO | PASS | 2 |

## Checks

| check | severity | status | detail |
| --- | --- | --- | --- |
| input_poll_summary_exists | ERROR | PASS | poll refresh summary is readable |
| input_readiness_exists | ERROR | PASS | next-batch readiness CSV is readable |
| input_audit_summary_exists | ERROR | PASS | candidate audit summary CSV is readable |
| input_plan_exists | ERROR | PASS | next submission batch plan CSV is readable |
| input_release_gate_exists | ERROR | PASS | submission release gate CSV is readable |
| input_artifact_manifest_summary_exists | ERROR | PASS | candidate artifact manifest summary CSV is readable |
| input_final_submission_package_summary_exists | ERROR | PASS | final submission package summary CSV is readable |
| planned_slots_within_daily_limit | ERROR | PASS | planned slots=5; daily official limit=5 |
| planned_slots_have_release_rows | ERROR | PASS | plan-only=[]; release-only=[] |
| planned_slots_have_audit_rows | ERROR | PASS | missing audit rows=[] |
| planned_slots_have_readiness_rows | ERROR | PASS | missing readiness rows=[] |
| planned_slots_have_artifact_manifest_rows | ERROR | PASS | missing manifest rows=[] |
| planned_slots_have_final_package_rows | ERROR | PASS | missing package rows=[] |
| planned_paths_unique | ERROR | PASS | no duplicate planned submission paths |
| planned_submission_hashes_unique | ERROR | PASS | duplicate planned sha count=0 |
| no_missing_audit_in_candidate_pool | ERROR | PASS | MISSING_AUDIT rows=0 |
| external_context_blocks_release | ERROR | PASS | pending=2; running=1; batch_status=WAIT_EXTERNAL_CONTEXT; gates=['BLOCKED_EXTERNAL_CONTEXT'] |
| blocked_plan_does_not_submit | ERROR | PASS | current actions=['do_not_submit_yet'] |
| no_unapplied_poll_updates | INFO | PASS | poll refresh detected no unapplied kernel/submission updates |
| planned_slots_have_passing_audit_gate | ERROR | PASS | nonpassing planned audit rows=0 |
| planned_slots_have_valid_artifact_manifests | ERROR | PASS | nonpassing planned manifest rows=0; manifest rows=5 |
| planned_slots_have_no_final_package_failures | ERROR | PASS | failing planned package rows=0; package rows=5 |
| blocked_release_blocks_final_packaging | ERROR | PASS | package gates while external context pending=['BLOCKED_RELEASE_GATE'] |
| no_slots_ready_for_submit | INFO | PASS | no planned slot is currently releasable |

## Outputs

- `experiments/planning_state_validation.csv`
- `reports/planning_state_validation_report.md`
