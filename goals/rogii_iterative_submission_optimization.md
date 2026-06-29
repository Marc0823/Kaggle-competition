# Goal: ROGII Iterative Submission Optimization

## Objective

Build a repeatable optimization loop for the ROGII Wellbore Geology Prediction competition that continuously generates, tests, audits, selectively submits, and learns from candidate outputs.

Primary target:

- Beat the current confirmed project best public RMSE: `7.235`.

Secondary target:

- Maintain a disciplined validation and submission system so that daily Kaggle submissions are used as high-value experiments, not as blind leaderboard probing.

## Hard Constraints

- Official Kaggle submission limit: maximum 5 submissions per team per UTC day.
- Official submissions must be made through Kaggle Notebooks.
- Notebook output must include a file named exactly `submission.csv`.
- CPU and GPU notebook runtime must each be at most 9 hours.
- Internet must be disabled for official notebook submissions.
- Visible `test/` files are only examples; hidden rerun will replace them with actual hidden test wells.
- Notebooks must be hidden-test compatible:
  - no hardcoded visible well IDs;
  - no fixed `14,151` row assumption;
  - no static visible-test `submission.csv` replay;
  - dynamically discover `test/*__horizontal_well.csv`;
  - generate IDs from the current run's `sample_submission.csv` or current test files.
- Do not commit Kaggle credentials, access tokens, data, artifacts, model binaries, or generated submissions.

## Current Baseline

Confirmed project public scores:

| score | candidate | interpretation |
| ---: | --- | --- |
| 7.235 | Wellbore wizard physics PF stack | current best baseline |
| 7.263 | David v12 budget guarded clean GPU | near-duplicate backup |
| 7.588-7.606 | Fleongg / Ricardo-style branches | plausible but weaker |
| 7.703 | David bimodal fastcpu no-sameid | weaker but still useful calibration |
| 20.579 | Nickson artifact inference | known bad |
| 11551.955 | direct train TVT overlap lookup | known catastrophic |
| 15357.198 | failed 7.159-style attempts | known catastrophic in current implementation |

The baseline to beat is `7.235`, but near-duplicates of the baseline have low upside even if they are safe.

## Optimization Philosophy

Use Kaggle kernel runs liberally for execution and output generation. Use official competition submissions aggressively but deliberately: the default goal is to spend at least 4 of 5 daily slots, and preferably all 5, as long as the slots answer planned experimental questions.

Every official submission must answer a specific experimental question, such as:

- Does blend weight `0.20` improve over `0.10`?
- Does a new GR/typewell alignment branch improve over the physics/PF baseline?
- Does per-well gating beat global blending?
- Does an artifact-stack candidate remain valid under hidden rerun?

Do not submit candidates only because they are new. Do submit enough qualified, diverse candidates to learn from public-score feedback every UTC day.

## Operating Loop

For every candidate:

1. Define the hypothesis.
   - What changed?
   - Why might it beat `7.235`?
   - What new risk does it introduce?

2. Generate the candidate.
   - Edit the notebook or script.
   - Run locally only when local data is available and the workload is small.
   - Otherwise push/run a Kaggle kernel.
   - Download output artifacts.

3. Run the pre-submit audit.
   - Validate format.
   - Validate hidden-test compatibility.
   - Validate shape and physical plausibility.
   - Compare against known good and bad submissions.

4. Run validation.
   - Use train pseudo-test validation when the method can be executed on train wells.
   - Use repeated grouped-by-well splits.
   - Use missing-GR robustness tests when GR alignment is important.
   - Compare against the current `7.235` baseline under the same split.

5. Decide.
   - `BLOCK`: do not submit.
   - `HOLD`: keep for later or blend/search.
   - `SUBMIT_CANDIDATE`: eligible for official submission if budget allows.

6. Submit selectively.
   - Target 4-5 official submissions per UTC day when enough qualified candidates exist.
   - Keep one flexible slot early in the day, then release it near the daily cutoff if no emergency fix is needed.
   - Record the exact kernel, version, file, message, and result.

7. Calibrate.
   - Add public score to `experiments/submission_ledger.csv`.
   - Re-run surrogate calibration against known scored submissions.
   - Update thresholds and next candidate plan.

## Submission Budget Policy

Daily maximum: 5 official submissions.

Daily target:

- Minimum target: 4 official submissions per UTC day.
- Preferred target: 5 official submissions per UTC day.
- Exception: use fewer than 4 only when there are not enough audited candidates, Kaggle operations are blocked, or pending results are required to avoid duplicating the same experiment.

Default allocation:

| slot type | count | purpose |
| --- | ---: | --- |
| structured calibration | 2-3 | low-dimensional public-score learning, such as blend weights or thresholds |
| strong candidate | 1-2 | candidates supported by CV and audit |
| flexible / release slot | 0-1 | emergency fix early in the day; use for another planned candidate near cutoff |

Using 4-5 slots is preferred because each public score is useful calibration data. The constraint is not "save submissions"; the constraint is "do not spend submissions on uninformative or invalid experiments."

Each daily batch should be designed before submission. Good daily batches include:

- a one-dimensional sweep, such as blend weights `0.10`, `0.20`, `0.30`;
- a baseline-adjacent candidate plus a higher-novelty candidate;
- a per-well gating candidate compared with a global blend;
- one conservative candidate plus one or two high-upside candidates that passed audit.

Avoid daily batches where all submissions are near-duplicates of each other. If two candidates differ only by rounding, file path, or message text, submit at most one.

Never submit:

- invalid format candidates;
- static visible-test replays;
- hidden-incompatible notebooks;
- `high_shape_risk` candidates;
- candidates close to known catastrophic submissions;
- near-duplicates of `7.235` unless the submission is a deliberate calibration point;
- candidates that do not add information beyond another submission already planned for the same day.

## Candidate Decision Schema

Each candidate should receive these fields before official submission:

| field | values / meaning |
| --- | --- |
| `candidate_id` | stable short name |
| `hypothesis` | why the candidate should improve |
| `source_notebook` | local folder or Kaggle kernel slug |
| `output_path` | downloaded `submission.csv` path |
| `format_status` | `PASS` / `FAIL` |
| `hidden_compatibility` | `PASS` / `FAIL` / `UNKNOWN` |
| `shape_risk` | `LOW` / `MEDIUM` / `HIGH` |
| `cv_delta_vs_baseline` | pseudo-test CV delta, lower is better |
| `rmse_to_current_best_7p235` | output-vector distance to baseline |
| `nearest_known_public_score` | nearest known scored submission |
| `novelty` | `LOW` / `MEDIUM` / `HIGH` |
| `decision` | `BLOCK` / `HOLD` / `SUBMIT_CANDIDATE` / `SUBMITTED` |
| `notes` | short reason |

## Validation Framework

### 1. Format Audit

Check:

- file exists;
- file is named `submission.csv`;
- columns are exactly or effectively `id,tvt`;
- IDs match the current sample submission;
- no duplicate IDs;
- row count matches;
- `tvt` is numeric;
- no `NaN`, `inf`, or blank predictions.

### 2. Hidden Compatibility Audit

Check notebook source for:

- dynamic test-well discovery;
- no visible-well hardcoding;
- no hardcoded row count;
- no dependency on visible test labels;
- no train-only columns during test inference;
- no internet requirement.

### 3. Shape And Physics Audit

Compute per well:

- first hidden prediction gap vs last known `TVT_input`;
- initial slope continuity vs prefix slope;
- one-step jump rate;
- curvature distribution;
- typewell `TVT` range violation rate;
- per-well min/max/mean/std.

Block candidates with:

- large anchor gap;
- extreme jump rate;
- large typewell range violation;
- obvious nonphysical oscillation.

### 4. Known-Submission Calibration

Compare new output vectors to known scored submissions:

- current best `7.235`;
- `7.263`;
- `7.588-7.606`;
- `7.703`;
- `20.579`;
- `11551.955`;
- `15357.198`.

Interpretation:

- extremely close to `7.235`: safe but low upside;
- moderately different from good submissions with low shape risk: possible candidate;
- close to known bad submissions: block;
- far from all known good submissions: high risk unless CV strongly supports it.

### 5. Train Pseudo-Test CV

This is the most important non-submission validation.

Simulate Kaggle test on train wells:

1. Select validation wells by group, never by random rows.
2. Hide the target region by setting `TVT_input` to missing after a prefix.
3. Remove train-only inference fields:
   - `TVT`;
   - formation surfaces such as `ANCC`, `ASTNU`, `ASTNL`, `EGFDU`, `EGFDL`, `BUDA`;
   - typewell `Geology`, unless the method will not use it at real inference.
4. Run the candidate exactly like hidden-test inference.
5. Compute RMSE against true training `TVT`.

Use repeated grouped-by-well splits:

- multiple random seeds;
- multiple validation well groups;
- multiple prefix lengths;
- reported mean, median, standard deviation, and worst-well RMSE.

### 6. Missing-GR Robustness

For GR/typewell alignment methods, test:

- original GR;
- random GR masking;
- contiguous GR gaps;
- prefix-only or sparse-GR cases.

Prefer methods that degrade gracefully.

### 7. Ensemble Disagreement

For candidate pools:

- compute per-well disagreement across base submissions;
- identify wells where a new method changes the baseline most;
- inspect whether changes are localized and plausible;
- use high-disagreement wells for uncertainty-aware gating.

## Public Score Use Policy

Allowed uses:

- calibrate low-dimensional blend weights;
- tune smoothing strength;
- tune fallback thresholds;
- tune per-well gating thresholds;
- calibrate surrogate risk bands.

Disallowed uses:

- train a high-complexity model directly on public scores;
- consume daily submissions on duplicate, invalid, or hypothesis-free candidates;
- chase public LB changes that contradict pseudo-CV and physics audits;
- optimize only for visible public split at the expense of private robustness.

Treat public score as an expensive, noisy, low-dimensional signal.

Because the public-score signal is valuable, the operating default is to collect 4-5 public-score observations per day when the candidate queue supports it. Keep the model used for this feedback simple: low-dimensional blend curves, threshold sweeps, and calibration rules are allowed; high-capacity leaderboard-fitting is not.

## Ensemble Policy

Do not average every method.

Allowed ensemble patterns:

- non-negative weighted blend of vetted methods;
- weighted median or trimmed mean to reduce bad-model damage;
- per-well gating based on validation, uncertainty, and shape risk;
- fallback to `7.235` baseline when a method is uncertain.

Candidate base methods must pass audit before entering the ensemble pool.

Bad methods can drag results down, especially when they distort a continuous TVT trajectory. Exclude known bad or high-risk methods unless deliberately used as negative controls.

## Waiting And Polling Policy

Do not idle while waiting for Kaggle scoring.

Polling cadence:

- after a new official submission: check status every 10-15 minutes for the first hour;
- if still pending after one hour: check every 30-60 minutes;
- if several submissions are pending: summarize the queue and continue preparing the next candidate batch.

While waiting:

1. Update `experiments/submission_ledger.csv` with pending rows.
2. Run or queue the next Kaggle kernels.
3. Download and audit completed kernel outputs.
4. Run pseudo-test CV for methods that can be evaluated locally.
5. Prepare the next 2-5 candidate submissions, but avoid submitting dependent variants until the needed public score arrives.
6. Pre-write branch decisions:
   - if score improves, what is the next exploitation sweep?
   - if score worsens, what is rejected or downweighted?
   - if score is blank or delayed, what can proceed independently?

Pending submissions should block only experiments that directly depend on that pending score. They should not block unrelated notebook runs, audits, CV jobs, or preparation of the next daily batch.

## Daily Operating Checklist

1. Pull latest GitHub changes.
2. Check current Kaggle submissions and pending runs.
3. Update `experiments/submission_ledger.csv`.
4. Choose enough hypotheses to support 4-5 informative submissions.
5. Generate/run candidates.
6. Download outputs.
7. Run audit and validation.
8. Build a daily submission batch with diverse, non-duplicate experiments.
9. Submit 4 candidates by default; submit the 5th when it is informative or the flexible slot is no longer needed.
10. Poll pending submissions on cadence while continuing candidate preparation.
11. Record results and update reports.

## State Files

Tracked:

- `goals/rogii_iterative_submission_optimization.md`: this operating goal.
- `reports/problem_study_2026-06-29.md`: problem study and official constraints.
- `reports/local_surrogate_score_report.md`: latest surrogate summary.
- `experiments/local_surrogate_scores.csv`: candidate metrics.
- `experiments/big_signal_public_lb_tracker.csv`: prior project tracker.
- `experiments/submission_ledger.csv`: official submission log and decisions.

Ignored / local only:

- `data/`
- `artifacts/`
- `submissions/`
- model files;
- Kaggle credentials;
- generated `submission.csv` files.

## Initial Implementation Backlog

1. Create `scripts/pre_submit_audit.py`.
2. Create `scripts/pseudo_test_cv.py`.
3. Add a standard candidate output folder convention under ignored `artifacts/`.
4. Add per-candidate audit reports under ignored `artifacts/<candidate>/audit.json`.
5. Add an update command that appends Kaggle submission results to `experiments/submission_ledger.csv`.
6. Add a report generator that ranks candidates by:
   - audit status;
   - CV delta;
   - distance to known submissions;
   - novelty;
   - public score calibration.

## Stop / Escalation Rules

Stop submitting for the day if:

- two consecutive submissions fail for operational or formatting reasons;
- the same hypothesis gets worse across multiple planned calibration points;
- the remaining planned candidates no longer add information after new scores arrive;
- Kaggle scoring queue is delayed and all remaining candidates depend on pending results;
- there are fewer than 4 qualified candidates and forcing more would mean submitting invalid, duplicate, or high-risk outputs.

Escalate for human review if:

- a candidate contradicts pseudo-CV but improves public score;
- a candidate looks physically implausible but scores well;
- a notebook depends on external datasets or public kernels with unclear availability;
- a method may violate competition rules or reproducibility requirements.
