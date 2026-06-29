# ROGII Execution Log - 2026-06-29

This log records concrete execution against `goals/rogii_iterative_submission_optimization.md`.

## Current Batch

Batch question:

```text
Q20260629-03: What should the first executable batch test now that static replay is known risky?
```

Selected approach:

```text
Run a hidden-compatible baseline reproduction under joezzzzz plus prepare a structural GR/typewell candidate.
```

Reason:

- Static Sunny80/Sunny70 notebooks completed with blank public score and are treated as hidden-format risk.
- Henry TabICL/v10 hidden-compatible retry is still pending, so it should be monitored but should not block independent preparation.
- A joezzzzz-owned baseline reproduction is needed before future aggressive daily batches can safely run from the active account.

## Kaggle State Snapshot

Checked via Kaggle API on 2026-06-29 UTC.

Recent official submissions:

| submission_id | candidate | status | public_score | action |
| ---: | --- | --- | ---: | --- |
| 54162612 | Henry TabICL v10 artifact hidden-compatible retry | PENDING |  | monitor |
| 54162415 | Kojimar style Sunny70 v10 artifact30 notebook | COMPLETE |  | reject static replay / hidden-format risk |
| 54162323 | Kojimar style Sunny80 v10 artifact20 notebook | COMPLETE |  | reject static replay / hidden-format risk |
| 54105734 | direct train TVT overlap lookup | COMPLETE | 11551.955 | known bad |
| 54105066 | ROGII 7159 ourmatch GR contact matching | COMPLETE | 15357.198 | known bad |

## Kernel Execution

Created an ignored local working copy:

```text
working/kaggle_kernel_lucifer_baseline_joezzzzz
```

Pushed to Kaggle:

```text
joezzzzz/rogii-lucifer-baseline-repro-codex
version: 1
status: COMPLETE
url: https://www.kaggle.com/code/joezzzzz/rogii-lucifer-baseline-repro-codex
```

Downloaded output to ignored local artifacts:

```text
artifacts/lucifer_baseline_repro_joezzzzz_v1/
```

Local pre-submit audit:

```text
status: PASS
rows: 14151
columns: id,tvt
id_order_matches_sample: true
sha256: fdf4a8175b6ec6a70c9b78fd6916ac3c317e43f7e9c08bbca87cd02314801ca9
```

Notebook source audit:

```text
status: PASS
failures: 0
warnings: 0
required_signals: sample_submission, dynamic_horizontal_well_discovery, test_split_reference, submission_write
```

Official submission:

```text
submission_id: 54174151
status: PENDING
message: Codex active-account 7.235 baseline reproduction audit pass
```

This consumes the fourth official submission slot for 2026-06-29 UTC and answers the active-account baseline calibration question.

## Records Updated

- `experiments/submission_ledger.csv`
  - Added static Sunny80/Sunny70 completed blank-score rows.
  - Kept Henry retry as pending.
  - Added `54174151` baseline reproduction as submitted/pending with audit pass.
- `experiments/question_decision_log.csv`
  - Marked the question-driven process setup as complete.
  - Recorded the baseline reproduction kernel push, output audit, and official pending submission.
  - Opened the first structural candidate question.
- `experiments/question_backlog.csv`
  - Added the prioritized open question queue for baseline reproduction, GR/typewell correction, gating, calibration, robustness, and reference-notebook reproduction.
  - Moved baseline reproduction to `submitted_pending`.
  - Moved GR/typewell correction to the active next implementation path.
- `experiments/daily_submission_plan.csv`
  - Captures the current 5-slot plan, including already-used official submissions, submitted baseline calibration, and remaining candidate preparation.
- `goals/rogii_iterative_submission_optimization.md`
  - Added the continuous question engine, model idea sources, anti-overfit rules, branch rules, and near-term Batch A-D roadmap.
- `reports/baseline_repro_audit_2026-06-29.md`
  - Added the kernel/output/submission audit details for the active-account baseline reproduction.
- `scripts/pre_submit_audit.py`
  - Added reusable local format/sample audit and verified it against the baseline output.
- `scripts/notebook_source_audit.py`
  - Added reusable source scan for hidden-test compatibility risks and verified it against the baseline notebook.
- `reports/gr_typewell_candidate_plan_2026-06-29.md`
  - Added the first structural candidate design: gated light GR/typewell correction on top of the audited baseline.
- `scripts/build_gr_typewell_light_candidate.py`
  - Added the first local builder for gated light GR/typewell correction.
  - Generated `artifacts/gr_typewell_light_alpha010_v1/submission.csv` locally; format audit passed.
  - Surrogate classified it as `near_duplicate_low_upside` with RMSE delta `0.3495` vs the active-account baseline.
- `artifacts/gr_typewell_light_alpha020_v1/` local-only
  - Generated alpha `0.20` GR/typewell probe; format audit passed.
  - Surrogate classified it as `near_duplicate_low_upside` with RMSE delta `0.6991` vs the active-account baseline.
- `reports/candidate_decision_report.md`
  - Added a compact pre-submission decision table.
  - Marked GR alpha probes as `HOLD_LOW_UPSIDE`.
  - Marked standalone `fleongg_pretrained_submission.csv` as `SUBMIT_CANDIDATE`.
- `joezzzzz/rogii-fleongg-branch-calibration-codex`
  - Directly submitting `fleongg_pretrained_submission.csv` from the baseline kernel failed with Kaggle API `400`.
  - Created and pushed a dedicated branch kernel whose final `submission.csv` is the fleongg pretrained branch.
  - Kernel version `1` completed, but audit rejected it before official submission because final `submission.csv` still matched the baseline and `fleongg_branch_submission_audit.json` was absent.
  - Fixed the notebook override cell and pushed kernel version `2`.
  - Kernel version `2` is currently `RUNNING`.

## Next Actions

1. Poll official submission `54174151`.
2. Poll pending Henry submission `54162612`.
3. If `54174151` reproduces the expected baseline region, close Q20260629-B01 and use the output as the active-account anchor.
4. Poll `joezzzzz/rogii-fleongg-branch-calibration-codex` version `2`; when complete, download and audit output.
5. If fleongg branch audit proves final `submission.csv` equals the fleongg branch, submit it as the fifth official slot for learned-signal calibration.
