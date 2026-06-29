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

Use Kaggle kernel runs liberally for execution and output generation. Use official competition submissions sparingly.

Every official submission must answer a specific experimental question, such as:

- Does blend weight `0.20` improve over `0.10`?
- Does a new GR/typewell alignment branch improve over the physics/PF baseline?
- Does per-well gating beat global blending?
- Does an artifact-stack candidate remain valid under hidden rerun?

Do not submit candidates only because they are new.

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
   - Use no more than the planned daily budget.
   - Reserve at least one emergency slot when possible.
   - Record the exact kernel, version, file, message, and result.

7. Calibrate.
   - Add public score to `experiments/submission_ledger.csv`.
   - Re-run surrogate calibration against known scored submissions.
   - Update thresholds and next candidate plan.

## Submission Budget Policy

Daily maximum: 5 official submissions.

Default allocation:

| slot type | count | purpose |
| --- | ---: | --- |
| exploratory | 1-2 | low-dimensional public-score calibration |
| strong candidate | 1-2 | candidates supported by CV and audit |
| reserved | 1 | emergency fix, rerun, or deadline handling |

Do not use all 5 slots by default. Use all slots only near a deadline or when each slot answers a planned experimental question.

Never submit:

- invalid format candidates;
- static visible-test replays;
- hidden-incompatible notebooks;
- `high_shape_risk` candidates;
- candidates close to known catastrophic submissions;
- near-duplicates of `7.235` unless the submission is a deliberate calibration point.

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
- consume all daily submissions without a written hypothesis;
- chase public LB changes that contradict pseudo-CV and physics audits;
- optimize only for visible public split at the expense of private robustness.

Treat public score as an expensive, noisy, low-dimensional signal.

## Ensemble Policy

Do not average every method.

Allowed ensemble patterns:

- non-negative weighted blend of vetted methods;
- weighted median or trimmed mean to reduce bad-model damage;
- per-well gating based on validation, uncertainty, and shape risk;
- fallback to `7.235` baseline when a method is uncertain.

Candidate base methods must pass audit before entering the ensemble pool.

Bad methods can drag results down, especially when they distort a continuous TVT trajectory. Exclude known bad or high-risk methods unless deliberately used as negative controls.

## Daily Operating Checklist

1. Pull latest GitHub changes.
2. Check current Kaggle submissions and pending runs.
3. Update `experiments/submission_ledger.csv`.
4. Choose 1-3 hypotheses for the day.
5. Generate/run candidates.
6. Download outputs.
7. Run audit and validation.
8. Decide which, if any, candidates deserve official submission.
9. Submit within budget.
10. Record results and update reports.

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
- Kaggle scoring queue is delayed and pending results block interpretation;
- the remaining daily slots are needed for a higher-priority candidate.

Escalate for human review if:

- a candidate contradicts pseudo-CV but improves public score;
- a candidate looks physically implausible but scores well;
- a notebook depends on external datasets or public kernels with unclear availability;
- a method may violate competition rules or reproducibility requirements.
