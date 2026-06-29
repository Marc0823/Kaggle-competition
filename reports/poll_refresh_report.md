# Poll And Refresh Report

This report summarizes the latest safe polling pass. It does not submit to Kaggle.

## Summary

| metric | value |
| --- | --- |
| kernel_updates_detected | 0 |
| kernel_errors | 0 |
| kernel_apply | False |
| submission_updates_detected | 0 |
| submission_appended_detected | 0 |
| submission_missing_not_appended | 0 |
| submission_dry_run | True |
| pending_official_submissions | 2 |
| running_kernels | 1 |
| readiness_status_counts | HOLD_PENDING_CONTEXT=9; HOLD_DUPLICATE=6; WAIT_OFFICIAL_SCORE=4; HOLD_LOW_UPSIDE=2; HOLD_INFORMATION_SLOT=1 |
| audit_gate_counts | AUDIT_PASS_WARN_REVIEW=19; AUDIT_PASS=3 |
| submission_gate_counts | AUDITED_WAIT_CONTEXT=13; HOLD_DUPLICATE=6; HOLD_LOW_UPSIDE=2; HOLD_INFORMATION_SLOT=1 |
| batch_status | WAIT_EXTERNAL_CONTEXT |
| planned_slots | 5 |
| current_action_counts | do_not_submit_yet=5 |
| release_gate_counts | BLOCKED_EXTERNAL_CONTEXT=5 |
| result_branch_rules | 7 |
| planning_validation_status_counts | PASS=17 |
| planning_validation_error_failures | 0 |

## Interpretation

- If `kernel_updates_detected` or `submission_updates_detected` is nonzero while the corresponding apply flag is false, rerun with explicit apply after reviewing the dry-run output.
- If `batch_status` is `WAIT_EXTERNAL_CONTEXT`, keep preparing candidates but do not spend official submission slots.
- Before any official submission, rerun this script after applying external state changes so readiness, audit summary, and batch plan agree.

## Outputs Refreshed

- `reports/next_batch_readiness_report.md`
- `reports/candidate_audit_summary_report.md`
- `reports/next_submission_batch_plan.md`
- `reports/submission_release_gate_report.md`
- `reports/planning_state_validation_report.md`
- `reports/result_branch_matrix.md`
- `experiments/poll_refresh_summary.csv`
- `reports/poll_refresh_report.md`
