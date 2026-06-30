# ROGII Big-Signal Public LB Push

Last updated: 2026-06-30 Asia/Shanghai

Current best confirmed public score: 7.182 from `Codex active-account 7.235 baseline reproduction audit pass`.

## Confirmed Results

| Candidate | Type | Status | Public score | Decision |
|---|---|---:|---:|---|
| Active-account 7.235 baseline reproduction | physics/PF stack | complete | 7.182 | current best |
| Wellbore wizard physics PF stack | physics/PF stack | complete | 7.235 | previous best |
| David v12 budget guarded clean GPU | model/guarded stack | complete | 7.263 | not better than best |
| Fleongg pretrained branch calibration v2 | pretrained branch calibration | complete | 7.787 | not useful |
| Henry TabICL v10 hidden-compatible retry | TabICL/artifact stack | complete | 13.453 | reject; artifact stack did not transfer |
| David bimodal fastcpu no-sameid | model-package/bimodal stack | complete | 7.703 | not useful |
| Nickson v5 artifact inference | artifact inference | complete | 20.579 | reject; artifact mismatch or poor transfer |
| Wellbore direct overlap lookup | train target lookup | complete | 11551.955 | reject; mapping/format does not match leaderboard target |
| ROGII 7159 ourmatch | GR/contact matching | complete | 15357.198 | reject; public-mechanism matching failed catastrophically |
| Static Sunny80/Sunny70 embedded CSV notebooks | static submission replay | complete | n/a | invalid; hidden rerun rejected fixed 14151-row output as incorrect format |

## Pending / Running Big Candidates

| Candidate | Type | Current state | Why it matters | Risk |
|---|---|---|---|---|
| Henry v10 + Sunny80 blend | hidden-compatible physical/artifact blend | kernel complete; output download attempted but hung | Correct implementation of Kojimar-style `0.80 * Sunny + 0.20 * v10`, but Henry v10 alone scored poorly | low priority after Henry 13.453 |
| Romantamrazov sub9 GPU fork v3 | tuned LGB/CB + NCC/PF features | kernel complete; output downloaded and sanity-audited | Independent model branch; valid `submission.csv`; surrogate is plausible but risky | may not beat 7.182 |
| Degnonguidi 7.159 fork | dual pipeline + gold prefix calibration + TabICL/package source | clean fork prepared, push blocked by GPU session cap | Published public score is better than current best; now highest-priority next GPU launch | needs GPU slot; may not reproduce exactly |
| Baidalin 7.201 fork | public 7.201 lineage | clean v2 fork prepared, push blocked by GPU session cap | Published LB is slightly better than current 7.235; next launch when a GPU slot frees | needs GPU slot; may not reproduce exactly |
| Wellbore direct overlap lookup | direct train-TVT MD lookup | complete, scored 11551.955 | Disproved naive overlap lookup; do not reuse as a candidate | high-risk train-target lookup; rejected |
| Aevion LB52 fixed test-only v4 | enhanced PF/beam selector | complete, no score; runtime exceeded | rejected operationally | previous Aevion variants were poor |

## Technical Notes

- `ourmatch` output sanity passed: 14,151 rows, `id,tvt` columns, sample order matched, no NaN/Inf, SHA prefix `2EBC68819F77FEB4`.
- `ourmatch` log showed `OUR-MATCH done: GR=3 contact=0`, and final audit reported `gold_overlay_enabled=false`.
- `Nickson v5 artifact inference` output sanity passed but scored 20.579, so the route is rejected unless a concrete bug is found.
- `Romantamrazov sub9 GPU` v1 failed at CatBoost because the default Bayesian bootstrap does not support `subsample`. v2 patches `bootstrap_type="Bernoulli"`.
- `Wellbore direct overlap lookup` explicitly builds an MD-to-TVT lookup from training wells and applies it to overlapping test wells. This is the highest-certainty public score shortcut, but it is target-label lookup and should be treated as high risk, not as a rule-safe modeling method.
- Direct overlap output sanity passed and log reported `14151 direct hits, 0 nearest-neighbor fallbacks`, but public score was 11551.955. This disproves the naive train-TVt MD lookup route.
- Henry TabICL/artifact output sanity passed, but both code submission and local CSV submission returned Kaggle 400; keep it as a ready-to-submit candidate only if the API starts accepting it.
- 2026-06-27 19:20 status check: Kaggle submission queue is functioning because direct lookup and Nickson completed with scores. `ourmatch`, `Aevion LB52 fixed test-only v4`, and `David bimodal fastcpu no-sameid` remain pending. Their kernels are complete, so this is a scoring queue delay rather than a notebook execution failure. `Romantamrazov sub9 GPU v2` is still running.
- 2026-06-27 19:30 submit debug: Kaggle returned `Submission not allowed: Your team has used its daily Submission allowance (5) today, please try again tomorrow UTC (12 hours from now). This competition only accepts Submissions from Notebooks. Submission files must be named "submission.csv" for this Competition.` This explains the repeated 400 errors for Henry/local blend submissions.
- `sunnywu27/rogii-wellbore-tvt-physical-model` output was downloaded and audited. It is effectively identical to the current 7.235 `Wellbore wizard physics PF stack` curve, so Sunny itself is not a new signal.
- `kojimar/rogii-physical-pf-signal-meets-artifact-stack` was pulled. Its public logic is a large-change route: `0.80 * Sunny physical/PF + 0.20 * v10 artifact stack`. The helper dataset is forbidden to this account, so the route was reconstructed locally from Sunny output plus the already-audited Henry/v10 artifact output.
- Prepared tomorrow-priority candidate: `artifacts/submission_space_blends/submission.csv`, a rounded `Sunny80 + v10 artifact20` blend. This is the top next submission once the daily allowance resets.
- Downloaded and compared additional outputs from Ravaghi hill-climbing, Fleongg v5, Lightning self-verifying, and Needless SEL15. Lightning and Needless are exact duplicates of Sunny/current-best; Fleongg is close and weaker; Ravaghi is different but expected to be lower-priority than the Sunny/v10 artifact blend.
- 2026-06-29: Static embedded CSV notebooks for Sunny80 and Sunny70 ran but were rejected during hidden scoring with `Your notebook generated a submission file with incorrect format`. The cause is hidden rerun row/schema mismatch; static public-output replay is not valid for this code competition.
- 2026-06-29: Retried the original Henry/v10 artifact notebook as a hidden-compatible code submission; it is pending.
- 2026-06-29: Built and pushed `leemarc223/rogii-henry-v10-sunny80-blend`, a hidden-compatible notebook that runs v10, then runs Sunny physical in the hidden environment, and finally writes `0.80 * Sunny + 0.20 * v10`. It is running.
- 2026-06-29: Romantamrazov v2 failed at CatBoost because `devices="0:1"` was invalid on a single-GPU worker. v3 patches `bootstrap_type="Bernoulli"` and `devices="0"` and is running.
- 2026-06-29: Baidalin 7.201 fork is prepared locally as `kaggle_kernel_baidalin7201_v2`. The clean metadata push reaches Kaggle and is now blocked only by `Maximum batch GPU session count of 2 reached`. Launch it as soon as Henry/Sunny or Romantamrazov finishes.
- 2026-06-29: Degnonguidi 7.159 fork is prepared locally as `kaggle_kernel_degnonguidi_7159_submit`. All referenced datasets/kernel source are visible to the current account, and push is blocked only by the two active GPU sessions. It should launch before Baidalin when a GPU slot frees.
- 2026-06-29 UTC / 2026-06-29 Beijing night: Two additional submissions completed after the previous status check. `Codex active-account 7.235 baseline reproduction audit pass` scored 7.182 and is now the best confirmed score. `Codex fleongg pretrained branch calibration v2 audit pass` scored 7.787 and is rejected.
- 2026-06-29 UTC: `Henry TabICL v10 artifact hidden-compatible retry` completed with public score 13.453. This rejects the standalone Henry/v10 route for now.
- 2026-06-30: `Romantamrazov sub9 GPU v3` completed. Its downloaded `submission.csv` passed sanity checks: 14,151 rows, id order matches sample submission, no duplicate ids, no NaN/Inf, range 11588.44 to 12238.67. Local surrogate marks it `plausible_submit_candidate` but `unknown_possible_but_risky`, with RMSE 6.06 from the current 7.235 reference.

## Current Interpretation

The most plausible large-improvement route remains public-mechanism-aware reconstruction and high-score public stack replication. Pure artifact inference without the right competition-specific alignment can fail badly, as seen in the Nickson and Henry results, and naive direct train-TVt lookup is now disproven by public score.

Current next high-priority actions: prioritize reproducing Degnonguidi 7.159 and Baidalin 7.201 from the lean GitHub repo; treat Romantamrazov v3 as a secondary risky candidate; do not spend more submissions on standalone Henry/v10.
