# Candidate Artifact Manifest Report

This report checks local ignored `candidate_manifest.json` files for the planned official-submission slots.

## Summary

| manifest_gate | count |
| --- | --- |
| PASS_SOURCE_POINTER | 5 |

## Planned Slot Manifests

| planned_slot | candidate_id | manifest_gate | manifest_found_by | source_path_exists | audit_json_exists | audit_gate | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | rogii_baidalin_7_201_preflight_codex_v1_sp45_projection_submission | PASS_SOURCE_POINTER | candidate_id | True | True | AUDIT_PASS_WARN_REVIEW | planned_slot_1_conditional_batch |
| 2 | rogii_baidalin_7_201_preflight_codex_v1_submission_sp45_fleongg_w0_50 | PASS_SOURCE_POINTER | candidate_id | True | True | AUDIT_PASS_WARN_REVIEW | planned_slot_2_conditional_batch |
| 3 | sp45_projection_slot1_codex_v1_submission_sp45_fleongg_w0_55 | PASS_SOURCE_POINTER | candidate_id | True | True | AUDIT_PASS_WARN_REVIEW | dynamic slot1 SP45 plus Fleongg w0.55 candidate; hold pending 54198676 public score |
| 4 | sp45_projection_slot1_codex_v1_submission_sp45_fleongg_w0_60 | PASS_SOURCE_POINTER | candidate_id | True | True | AUDIT_PASS_WARN_REVIEW | dynamic slot1 SP45 plus Fleongg w0.60 candidate; hold pending 54198676 public score |
| 5 | plateau_recent_quantile_v1_submission | PASS_SOURCE_POINTER | candidate_id | True | True | AUDIT_PASS_WARN_REVIEW | planned_slot_5_conditional_batch |

## Gate Meaning

- `PASS_SOURCE_POINTER`: the manifest exists, points to the exact planned output path, the selected output exists locally, and candidate audit evidence exists.
- `FAIL_*`: an official submission should not proceed until the missing or mismatched evidence is fixed.

## Outputs

- artifact root: `artifacts`
- `experiments/candidate_artifact_manifest_summary.csv`
- `reports/candidate_artifact_manifest_report.md`
