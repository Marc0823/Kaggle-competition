# Reference Notebook Preflight - 2026-06-29

This report records the first reference-notebook preflight batch after the goal protocol was tightened.

## Current State

Official submissions are still pending:

| submission_id | candidate | status |
| ---: | --- | --- |
| 54174876 | fleongg pretrained branch calibration | PENDING |
| 54174151 | active-account 7.235 baseline reproduction | PENDING |
| 54162612 | Henry TabICL/v10 hidden-compatible retry | PENDING |

Because these scores are pending, dependent calibration should wait. Independent reference-notebook preflight can continue without consuming official submission slots.

## Batch Question

Which reference notebook should be prepared while official scores are still pending?

## Options

| option | lane | evidence | decision |
| --- | --- | --- | --- |
| Run Degnonguidi 7.159 no-submit kernel | structural / high-upside | source audit PASS; dynamic test discovery; final submission validation; gold overlay off by default | selected |
| Run Baidalin 7.201 no-submit kernel | structural / high-upside | source audit FAIL: hardcoded visible train well demo and unsafe train/test `TVT_input` row copy | hold |
| Wait for pending official scores only | operational | would avoid extra work but does not improve next-batch readiness | reject |
| Patch audit before any reference run | diagnostic | useful for Baidalin, but Degnonguidi already passed current audit | partial: apply to Baidalin only |

## Source Audit Results

Degnonguidi 7.159:

```text
notebook: kaggle_kernel_degnonguidi_7159_submit/public-score-rogii-lb-7-159.ipynb
status: PASS
failures: 0
warnings: 0
required_signals:
  sample_submission: true
  dynamic_horizontal_well_discovery: true
  test_split_reference: true
  submission_write: true
```

Baidalin 7.201:

```text
notebook: kaggle_kernel_baidalin7201_v2/rogii-lb-7-201.ipynb
status: FAIL
failures:
  - hardcoded_visible_test_well
  - unsafe_train_test_tvtinput_row_copy
warnings:
  - fixed_width_id_slice
```

The Baidalin row copy finding is especially important:

```text
hw_te['TVT_input'] = hw_tr['TVT_input'].values
```

This is not safe for hidden rerun assumptions unless the code path is removed or proven unreachable.

## Selected Action

Fork Degnonguidi 7.159 into the active account and run it as a no-submit Kaggle kernel preflight:

```text
kernel: joezzzzz/rogii-degnonguidi-7159-preflight-codex
version: 1
status: RUNNING
official submission: none
```

This does not consume an official competition submission slot. The purpose is to test dependency/runtime/output sanity before deciding whether any official submission is justified.

## Metadata Notes

Degnonguidi metadata:

```text
enable_gpu: true
enable_internet: false
competition_sources:
  - rogii-wellbore-geology-prediction
dataset_sources:
  - phongnguyn23021656/koolbox-offline
  - nina2025/rogii-03
  - thbdh5765/rogii-v10-fresh-artifacts
  - fleongg/rogii-claude-models-pub
  - needless090/rogii-tabicl-mirror
  - ravaghi/wellbore-geology-prediction-artifacts
kernel_sources:
  - packagemanager/pm-119045926-at-06-21-2026-22-50-51
```

The original `leemarc223/rogii-degnonguidi-7159-submit` kernel is private/inaccessible from the active account, so active-account preflight is required.

## Next Branch Rules

| result | next action |
| --- | --- |
| kernel COMPLETE and output audit PASS | download output, run pre-submit audit, compare distance to `7.235`, decide whether it is a future submission candidate |
| kernel COMPLETE but audit FAIL | block official submission and add the failure to audit rules |
| kernel FAILED due dependency | record missing source and choose between dependency fix or inference-core port |
| output is near-duplicate of current best | hold as low-upside reference |
| output differs materially with low shape risk | consider one official slot after baseline score resolves |
| official scores appear while kernel runs | update ledger first, then re-rank next batch using new public scores |

## Decision

Proceed with Degnonguidi no-submit preflight and hold Baidalin until its source audit failures are fixed.
