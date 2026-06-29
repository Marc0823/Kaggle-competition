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

## Continuous Question Engine

The loop should always maintain a small queue of concrete questions. Work should not begin with "try another model"; it should begin with a question that can change the next decision.

At all times keep:

- 3-5 open strategic questions;
- 2-4 candidate options for the highest-priority question;
- one selected option set for the current batch;
- a written rule for what to do if the result improves, worsens, fails audit, or stays pending.

Every question should have one of these decision effects:

| decision effect | meaning |
| --- | --- |
| build | create a new candidate/model family |
| block | reject an unsafe or low-value path |
| calibrate | tune a low-dimensional choice |
| route | choose between methods per well or per condition |
| promote | move a candidate into the ensemble pool |
| demote | remove or downweight a candidate |

If a proposed experiment does not have a clear decision effect, rewrite the question before spending time or submissions.

## Codex Decision Protocol

Codex should run the project as a decision engine, not only as a notebook editor.

At the beginning of every work block, Codex must inspect the current state and produce a small decision set:

1. What is the highest-value uncertainty right now?
2. What 2-4 feasible options could answer it?
3. Which option or option set should be selected, and why?
4. What evidence will decide whether the selected option worked?
5. What follow-up question should be asked for each likely outcome?

The default behavior is for Codex to choose and execute the best option after recording the reasoning. Ask the human before acting only when the choice changes the strategic direction, consumes official submission slots in a way not covered by the daily plan, risks rule/compliance issues, or requires credentials/data that are not already available.

### Required Question Categories

Every full batch should include at least four active questions:

| category | required question |
| --- | --- |
| score question | What pending or completed public score changes the next decision? |
| model question | Which model family or structural idea is most worth testing now? |
| validation question | What local audit/CV test would prevent a bad submission? |
| submission question | Which 4-5 candidates should use the next daily submission budget? |
| operations question | Which kernel, artifact, credential, or data issue blocks progress? |

If there are fewer than four active questions, generate new ones before editing notebooks.

### Option Design Contract

For each top-priority question, list options in these lanes when possible:

| lane | purpose | example |
| --- | --- | --- |
| conservative | protect or reproduce a known-good path | active-account `7.235` baseline reproduction |
| structural / high-upside | introduce new information beyond tuning | GR/typewell alignment or pseudo-test residual correction |
| diagnostic / cheap | learn quickly without spending a submission | source audit, output distance check, or local pseudo-CV |
| calibration | tune a low-dimensional choice after a safe branch exists | blend `0.10/0.20/0.30` |
| block / defer | explicitly reject a low-value path | static replay or near-duplicate output |

Do not select only calibration options unless a structural candidate has already passed audit.

### Option Scoring Rule

Score each option on a simple `0-3` scale before selection:

| factor | 0 means | 3 means |
| --- | --- | --- |
| upside | cannot plausibly beat baseline | could plausibly beat `7.235` |
| information value | result will not change future work | result clearly changes next decisions |
| independence | near-duplicate of current best | new signal source or method family |
| audit readiness | likely invalid or hidden-incompatible | already passes format/source checks |
| validation support | no local evidence possible | pseudo-CV or robustness evidence available |
| submission efficiency | spends a slot on a duplicate or vague test | one slot answers a clear question |
| overfit risk | high public-LB chasing risk | low-dimensional or structurally justified |
| implementation cost | slow, brittle, or blocked | fast and directly executable |

Selection priority:

1. First choose options with high information value and acceptable audit readiness.
2. Break ties by independence and expected upside.
3. Use implementation cost to decide timing, not to avoid important work forever.
4. Prefer a small diverse option set over several variants of the same idea.

### Default Batch Shape

When enough candidates exist, a full batch should contain:

| slot | role | example |
| --- | --- | --- |
| 1 | reference / anchor | active-account known-good reproduction or backup reference |
| 2 | structural candidate | GR/typewell, physics constraint, residual correction, or reference fork |
| 3 | calibration point | one blend/gate/smoothing setting tied to the structural candidate |
| 4 | robustness or comparison | gated vs global, missing-GR-safe variant, or backup branch |
| 5 | flexible information slot | high-novelty audited candidate or late-day release slot |

If fewer than 4 candidates pass audit, do not force invalid submissions. Instead, spend the waiting time creating the next candidate queue.

### Batch Review Contract

After each batch, Codex must update the plan in this order:

1. Record exact outputs:
   - kernel slug/version;
   - artifact folder;
   - submission ID;
   - score/status;
   - audit/CV result.
2. Close or update each question that the batch answered.
3. Promote, hold, demote, or block each candidate.
4. Compare public score with local validation and note disagreements.
5. Decide whether validation thresholds or audit rules need to change.
6. Generate the next 3-5 concrete questions.
7. Select the next batch's first action.

The next batch may start only after the previous review produces at least one new model question, one validation question, and one submission question.

### Outcome-To-Question Branching

Each selected option must have prewritten follow-up branches:

| outcome | follow-up question |
| --- | --- |
| improves clearly | Which narrow exploitation sweep can confirm the improvement without overfitting? |
| improves slightly or ties | Does the candidate add ensemble diversity, or is it only noise? |
| worsens moderately | Which wells changed most, and should the method be gated instead of rejected? |
| worsens catastrophically | What audit rule or CV test should have blocked it? |
| blank score / scoring failure | Is the notebook hidden-compatible, or was this static visible-test replay? |
| pending | What independent kernels, audits, or CV jobs can proceed while waiting? |
| audit fails | Is the failure fixable, or should the method family be blocked? |

### Human Escalation Boundary

Codex should make routine technical choices directly, including:

- choosing the next source audit;
- selecting among equivalent local validation commands;
- blocking invalid submissions;
- preparing kernel forks;
- updating ledgers and reports.

Codex should ask for human direction before:

- changing the daily submission philosophy away from 4-5 informative slots;
- submitting a candidate that fails any required audit;
- using public score as a training target instead of a low-dimensional calibration signal;
- adding external datasets or dependencies with unclear competition eligibility;
- changing repository ownership, visibility, or credential handling.

## Batch Decision Flow

Each batch follows this exact sequence:

1. Generate questions.
   - Start from the previous batch review.
   - Add questions from public-score surprises, CV failures, audit failures, and new public notebook ideas.
   - Split vague questions into answerable subquestions.

2. List options.
   - For the top question, list at least 2 options when possible.
   - Include the conservative baseline-adjacent option, the structural/high-upside option, and the cheapest diagnostic option.

3. Score options.
   - Use the option selection rubric below.
   - Prefer options that create reusable knowledge even if they are not the highest expected score.
   - Avoid spending multiple slots on variants that answer the same question.

4. Select the batch.
   - Choose one primary option and, when useful, 1-3 support options.
   - Map selected options to Kaggle kernel runs, local CV jobs, or official submissions.
   - Predefine the branch decision for each possible result.

5. Execute and record.
   - Run kernels and audits first.
   - Submit only audited, informative candidates.
   - Update ledgers immediately when a kernel starts, output is downloaded, a submission is made, or a score appears.

6. Review and regenerate.
   - Summarize what changed.
   - Close or update answered questions.
   - Create the next 3-5 questions before starting the next batch.

## Operating Loop

This project should run as a question-driven research loop, not as a stream of disconnected notebook edits.

For every batch, start with specific questions. For each question, list multiple feasible options, select the best options to test, execute them, then review the whole plan and generate the next set of questions.

### Batch-Level Question Loop

Each batch must include:

1. A question.
   - What uncertainty are we trying to reduce?
   - What decision will change after we get the answer?
   - Which evidence will count as a useful answer?

2. Candidate solutions.
   - List at least 2 feasible options when possible.
   - Include one conservative option and one higher-upside option when available.
   - Mark whether each option is a structural idea, a calibration point, or an implementation fix.

3. Selection.
   - Choose the option or small option set with the best expected information value.
   - Explain why discarded options are less useful right now.
   - Avoid spending multiple submissions on options that answer the same question.

4. Execution.
   - Build/run the selected candidates.
   - Audit outputs.
   - Submit 4-5 informative official candidates when the batch supports it.

5. Review.
   - Record what the batch taught us.
   - Update the ledger, reports, surrogate thresholds, and candidate queue.
   - Produce the next set of project questions.

### Candidate-Level Loop

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

## Question Backlog And Decision Records

Maintain a running backlog of project questions. A question is better than a task because it forces each experiment to produce reusable knowledge.

Good question examples:

- Does GR/typewell alignment add independent signal beyond the `7.235` physics/PF baseline?
- Which blend weight range between baseline and artifact stack is most promising?
- Does per-well gating beat a global blend?
- Which wells are consistently worst under pseudo-test CV, and what failure mode do they share?
- Does missing-GR robustness explain public-score failures?
- Is a high-upside artifact branch hidden-compatible, or only visible-test compatible?

Each question should be recorded with this structure:

| field | meaning |
| --- | --- |
| `question_id` | stable ID, for example `Q20260630-01` |
| `question` | concrete uncertainty to resolve |
| `why_now` | why this matters before other work |
| `candidate_options` | 2+ feasible approaches |
| `selected_option` | chosen option or option set |
| `selection_reason` | why this is the best test now |
| `evidence_needed` | CV, audit, public score, logs, or output comparison |
| `result` | what happened |
| `next_question` | what to ask next |

Decision records should be short and factual. They should explain why an option was chosen, blocked, or deferred, not just list a score.

## Strategy Question Types

Use these recurring question types to avoid falling into pure parameter overfitting.

### 1. Signal Discovery Questions

Purpose: find genuinely new information beyond the current baseline.

Examples:

- Can GR/typewell alignment produce a valid independent path?
- Can train pseudo-test worst wells identify a new routing rule?
- Does a learned model improve only specific well classes?

Expected outputs:

- new method branch;
- pseudo-CV comparison;
- per-well failure analysis;
- at most 1-2 official submissions unless audit and CV are strong.

### 2. Calibration Questions

Purpose: use public score to tune low-dimensional choices.

Examples:

- Which blend weight is best among `0.10`, `0.20`, `0.30`?
- Which smoothing strength preserves anchor continuity without flattening useful signal?
- Which fallback threshold is best for per-well gating?

Expected outputs:

- 2-3 submissions in one planned sweep;
- simple curve or ranking;
- one follow-up exploitation question if the sweep is promising.

### 3. Robustness Questions

Purpose: test whether a candidate will survive hidden rerun and private leaderboard.

Examples:

- Does the notebook dynamically handle different test wells?
- Does the method degrade gracefully when GR is missing?
- Does it avoid train-only columns and static visible-test assumptions?

Expected outputs:

- audit result;
- blocked/fixed notebook;
- no official submission until fixed.

### 4. Ensemble And Gating Questions

Purpose: combine vetted signals without letting bad methods drag the trajectory.

Examples:

- Is global blend better than per-well gate?
- Can uncertainty select between baseline and GR alignment?
- Does weighted median beat mean blending when one branch is unstable?

Expected outputs:

- candidate pool;
- per-well disagreement report;
- 1-2 official submissions after audit.

### 5. Operational Questions

Purpose: keep the loop moving.

Examples:

- Which kernels are pending, failed, or ready for output download?
- Which candidate outputs need audit?
- Are we blocked by GPU slots or submission allowance?

Expected outputs:

- updated ledger;
- next batch plan;
- no model changes unless needed.

## Model Idea Sources

Do not rely only on parameter tuning. New candidates should come from several independent idea sources so the daily 4-5 submissions are informative and not just public-LB overfit.

### 1. Reference Notebook Reproduction

Use public high-score notebooks as anchors, but fork them into the active account and audit hidden compatibility before trusting them.

Useful when asking:

- Can we reproduce a known public score under `joezzzzz`?
- Is a notebook truly hidden-compatible, or did it only work on visible examples?
- Does a public notebook add signal independent from the `7.235` baseline?

Typical outputs:

- baseline reproduction kernel;
- clean active-account fork;
- exact output distance vs known scored references;
- eligibility decision for official submission.

### 2. Physics And Sequence Constraints

Create candidates from the structure of TVT trajectories instead of arbitrary model changes.

Idea families:

- anchor-continuity correction from the last known `TVT_input`;
- monotonicity and slope bounds;
- curvature/smoothing constraints;
- particle filtering or beam search around physically plausible paths;
- fallback to the current `7.235` trajectory when a correction is uncertain.

Useful question:

- Which physical constraint fixes high-error wells without damaging already-good wells?

### 3. GR / Typewell Alignment

Use geological signal alignment as a structural source of new information.

Idea families:

- GR-to-typewell correlation or dynamic time warping;
- per-well alignment confidence;
- local TVT shifts derived from strongest GR matches;
- missing-GR robustness fallback;
- light correction on top of the baseline rather than a full replacement.

Useful question:

- Does GR/typewell alignment add independent signal beyond the physics/PF baseline?

### 4. Pseudo-Test Residual Learning

Train simple correction models on repeated grouped train pseudo-tests, not on public score directly.

Allowed model classes:

- shallow residual models;
- low-dimensional correction rules;
- per-well class routers;
- uncertainty estimators for gating.

Avoid high-capacity models that only explain a few public-score observations.

Useful question:

- Can pseudo-test residual patterns identify when the baseline should be corrected?

### 5. Ensemble And Gating

Combine only vetted candidates.

Idea families:

- global blend among 2-3 known-good methods;
- weighted median or trimmed mean;
- per-well gate based on alignment confidence, shape risk, and model disagreement;
- safe fallback to `7.235` when confidence is low.

Useful question:

- Does a gate improve over a global blend by applying risky signal only where evidence is strong?

### 6. Negative Controls

Occasionally use diagnostic candidates to calibrate the validation framework, but do not waste official submissions on already-known failures.

Useful when asking:

- Does our audit detect the kind of failure that caused `20.579`, `11551.955`, or `15357.198`?
- Does pseudo-CV warn us before a public-score disaster?

## Anti-Overfit Rules

Public score should guide low-dimensional decisions, not become the training target.

Rules:

- A parameter sweep should change only 1-2 dimensions at a time.
- Every sweep must be attached to a structural question.
- Do not run a second sweep in the same direction unless the first sweep gives a monotonic or interpretable signal.
- If public score improves but pseudo-CV and physics audits disagree, mark the result as `public_promising_private_risk` and require a robustness follow-up.
- If public score worsens but CV improves, inspect whether the candidate targets private-like robustness before discarding it.
- Keep at least one structural/new-signal candidate in each full daily batch when possible.
- Do not let a bad method enter an ensemble only because it is different.

## Option Selection Rubric

When several options are available, select the next tests by expected information value, not only by expected score.

Score each option informally on:

| criterion | high score means |
| --- | --- |
| expected upside | could plausibly beat `7.235` |
| information value | result will change future choices |
| independence | adds signal not already captured by baseline |
| audit readiness | likely to pass format and hidden-compatibility checks |
| CV support | pseudo-test evidence is favorable or worth measuring |
| submission efficiency | one submission answers a clear question |
| overfit risk | lower is better |

Prioritize options with high information value and acceptable risk. Defer options that are only small parameter tweaks unless they are part of a planned sweep.

## Batch Review Cadence

Run a review after every completed submission batch, or at least once per UTC day.

The review must answer:

1. What did we learn?
2. Which hypotheses were supported, weakened, or rejected?
3. Which candidates should enter the ensemble pool?
4. Which candidates should be blocked permanently?
5. Did public score disagree with pseudo-CV or audit?
6. Are our validation thresholds too strict or too loose?
7. What are the next 3-5 concrete questions?
8. Which 4-5 submissions should be planned for the next available day?

The next batch should not start from a blank slate. It should start from the review's next questions.

### Next-Question Generation Rules

After a batch, generate questions from four sources:

| source | ask |
| --- | --- |
| score movement | What changed relative to `7.235`, and is the movement explainable? |
| validation disagreement | Where did public score, pseudo-CV, shape audit, or known-submission distance disagree? |
| model disagreement | Which wells changed most across candidate outputs, and are those changes plausible? |
| operations | Which pending kernels, failed notebooks, or missing artifacts block the next informative batch? |

Each completed batch must produce:

- one exploitation question if a candidate improved or nearly improved;
- one robustness question if any candidate looked promising but risky;
- one replacement question if a selected direction failed;
- one operational question if Kaggle status, runtime, or hidden compatibility blocked progress.

### Result Branch Rules

Before executing a candidate, write the branch rule:

| result | next action |
| --- | --- |
| clear improvement | run one narrow exploitation sweep and one robustness check |
| small improvement / tie | compare distance and shape; keep only if it adds ensemble diversity |
| moderate worsening | inspect per-well differences; decide whether to downweight or gate |
| catastrophic worsening | block method family or add audit rule that would have caught it |
| blank score / scoring failure | treat as operational failure until hidden compatibility is proven |
| pending | continue independent kernels, audits, and question planning |

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

1. Update `experiments/submission_ledger.csv` with pending rows using `scripts/update_submission_ledger.py`.
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
3. Update `experiments/submission_ledger.csv` with `scripts/update_submission_ledger.py --append-missing`.
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
- `experiments/question_backlog.csv`: prioritized open questions and candidate option sets.
- `experiments/question_decision_log.csv`: closed/open question decisions and outcomes.
- `experiments/daily_submission_plan.csv`: daily slot plan, status, and next actions.
- `experiments/kernel_run_ledger.csv`: Kaggle kernel runs, versions, statuses, output artifacts, and next actions.
- `experiments/reference_submission_registry.csv`: standard known-good, pending, and known-bad reference outputs for deep audit distance checks.

Ignored / local only:

- `data/`
- `artifacts/`
- `submissions/`
- model files;
- Kaggle credentials;
- generated `submission.csv` files.

## Near-Term Strategy Roadmap

### Batch A: Account-Owned Baseline And Safety

Main question:

- Can `joezzzzz` reproduce the current `7.235` baseline through a hidden-compatible kernel?

Options:

- run the current physics/PF stack exactly under `joezzzzz`;
- fork the `7.263` backup reference as a fallback;
- block static replay candidates until they pass hidden-compatibility audit.

Preferred selection:

- run the `7.235` baseline reproduction first, because all future comparisons need an active-account reference output.

Exit criteria:

- kernel completes;
- output downloads;
- `submission.csv` passes audit;
- decide whether an official submission is useful as an account-owned calibration point.

### Batch B: First Structural Signal

Main question:

- Does GR/typewell alignment add useful correction signal beyond the baseline?

Options:

- light baseline correction from GR/typewell confidence;
- pure GR alignment path search;
- per-well gate between baseline and GR branch;
- artifact-stack branch from accessible datasets.

Preferred selection:

- start with light correction plus gate design. It has lower blast radius than replacing the whole trajectory and can fall back to `7.235`.

Exit criteria:

- pseudo-test split result;
- missing-GR robustness result;
- distance and shape comparison to `7.235`;
- decide whether one official submission is justified.

### Batch C: Low-Dimensional Calibration Sweep

Main question:

- If a structural branch is safe, what blend/gate strength is best?

Options:

- global blend weights such as `0.10`, `0.20`, `0.30`;
- per-well gate thresholds;
- smoothing strength around corrected sections.

Preferred selection:

- use 2-3 official slots in one planned sweep only after Batch B passes audit.

Exit criteria:

- public-score curve is interpretable;
- choose one exploitation candidate or reject the branch.

### Batch D: Ensemble Pool Refresh

Main question:

- Which vetted candidates should enter the ensemble pool, and which should be excluded?

Options:

- weighted blend of `7.235`, `7.263`, and the best structural branch;
- weighted median / trimmed mean;
- per-well uncertainty gate;
- conservative fallback ensemble with baseline dominance.

Preferred selection:

- favor gated or trimmed combinations if any branch shows high per-well disagreement.

Exit criteria:

- ensemble candidates pass audit;
- official submissions answer distinct blend/gate questions;
- update the next question backlog from results.

## Initial Implementation Backlog

Done:

- Create `scripts/pre_submit_audit.py`.
- Verify it on `lucifer_baseline_repro_joezzzzz_v1` against `data/sample/sample_submission.csv`.
- Extend `scripts/pre_submit_audit.py` with optional anchor-continuity, jump/curvature, typewell-range, and reference-distance checks.
- Add `experiments/reference_submission_registry.csv` and `--reference-registry` support for repeatable known-output distance checks.
- Create `scripts/update_submission_ledger.py` to sync Kaggle CLI submission status, scores, and missing historical rows into `experiments/submission_ledger.csv`.
- Create `scripts/notebook_source_audit.py`.
- Verify it on `lucifer_baseline_repro_joezzzzz`.
- Create `scripts/build_gr_typewell_light_candidate.py`.
- Generate and audit `gr_typewell_light_alpha010_v1`.
- Generate and audit `gr_typewell_light_alpha020_v1`.
- Create `scripts/candidate_decision_report.py`.

Next:

1. Run deep pre-submit audit with `experiments/reference_submission_registry.csv` on every completed kernel output before official submission.
2. Create `scripts/pseudo_test_cv.py`.
3. Add a standard candidate output folder convention under ignored `artifacts/`.
4. Add per-candidate audit reports under ignored `artifacts/<candidate>/audit.json`.
5. Add a report generator that ranks candidates by:
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
