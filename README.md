# Kaggle ROGII Wellbore Geology Prediction

This repository contains our working code, reports, experiment trackers, and Kaggle notebook forks for the **ROGII Wellbore Geology Prediction** competition.

The goal is to collaborate on high-quality, reproducible Kaggle submissions while keeping large data files, generated artifacts, and private credentials out of Git.

## Competition Summary

- Competition: ROGII Wellbore Geology Prediction
- Task type: regression / sequence reconstruction
- Target: `tvt`
- Metric: RMSE, lower is better
- Current confirmed public best in our logs: `7.235`

The problem is not a simple row-wise tabular regression problem. Strong solutions reconstruct the hidden TVT trajectory for each well using:

- known `TVT_input` prefix anchors
- GR curve alignment against typewell
- particle filtering / beam search
- well-wise smoothing and physical constraints
- public high-score stack replication

## Repository Structure

```text
.
├── scripts/                         # Utility scripts and local surrogate scoring
├── reports/                         # Progress notes and decision reports
├── experiments/                     # Lightweight experiment trackers
├── goals/                           # Operating goals and submission strategy
├── kaggle_kernel_lucifer_wellbore_wizard_pf_stack/      # current 7.235 reference
├── kaggle_kernel_degnonguidi_7159_submit/                # 7.159 reproduction target
├── kaggle_kernel_baidalin7201_v2/                        # 7.201 reproduction target
├── kaggle_kernel_henry_v10_sunny80_blend/                # artifact/physical blend candidate
├── kaggle_kernel_david_v12_budget_guarded_clean_gpu/     # 7.263 backup reference
├── requirements.txt
├── .gitignore
└── README.md
```

Not included in Git:

- `data/`
- `artifacts/`
- model files such as `.pkl`, `.ckpt`, `.pth`
- Kaggle credentials
- generated submission files

## Operating Goal

The current optimization workflow is documented in:

```text
goals/rogii_iterative_submission_optimization.md
```

Use this as the working contract for iterative submission improvement:

1. Generate candidates with a clear hypothesis.
2. Run notebooks and download outputs without spending official submissions.
3. Audit format, hidden-test compatibility, shape, and known-submission distance.
4. Run train pseudo-test CV when the method supports it.
5. Submit only candidates that pass the gate and answer a specific experiment question.
6. Record every official result in `experiments/submission_ledger.csv`.
7. Record batch questions and option choices in `experiments/question_decision_log.csv`.
8. Keep the next concrete questions in `experiments/question_backlog.csv` so each batch begins with a decision, not a vague modeling tweak.

Kaggle kernel runs are cheap compared with official submissions. Official submissions are capped at five per team per UTC day; the operating target is to use 4-5 slots when enough audited, informative candidates exist, with every submission treated as a planned experiment.

## Data Setup

Each teammate should download the competition data from Kaggle and place it locally.

Recommended local path:

```text
D:\Codex\kaggle\rogii-wellbore\data
```

Expected structure:

```text
data/
├── train/
├── test/
└── sample_submission.csv
```

If you use another path, pass it explicitly to scripts with `--data-dir`.

## Environment Setup

Create a virtual environment and install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Install and configure Kaggle API separately. Do not commit `kaggle.json` or any API token.

## Local Surrogate Scoring

Because Kaggle submissions are limited and scoring can be slow, we use a local surrogate checker before submitting.

Run:

```powershell
python scripts\local_surrogate_score.py --data-dir D:\Codex\kaggle\rogii-wellbore\data --root . --output-dir experiments
```

Outputs:

```text
experiments/local_surrogate_scores.csv
experiments/local_surrogate_pairwise_distance.csv
reports/local_surrogate_score_report.md
```

Important: this does **not** know hidden labels and cannot exactly predict Public LB. It is mainly used to reject obviously bad or duplicated candidates before spending submissions.

## Pre-Submit Format Audit

Before spending an official submission slot, audit the generated `submission.csv` against the current sample file:

```powershell
python scripts\pre_submit_audit.py artifacts\candidate_folder\submission.csv --sample data\sample\sample_submission.csv
```

This checks columns, row count, ID order, duplicate IDs, finite predictions, summary stats, and sha256. It does not replace hidden-compatibility source review or pseudo-test validation.

Audit the notebook source for common hidden-test risks:

```powershell
python scripts\notebook_source_audit.py kaggle_kernel_lucifer_wellbore_wizard_pf_stack\wellbore-wizard-physics-pf-stack.ipynb
```

This source scan flags hardcoded visible wells, fixed visible row counts, static replay patterns, and unsafe train/test row-alignment copies. It is a guardrail, not a proof of model quality.

## Submission Ledger

Official submission outcomes should be recorded in:

```text
experiments/submission_ledger.csv
```

This file tracks the candidate ID, kernel slug/version, public score, audit status, decision, and notes. Keep it lightweight and avoid adding generated outputs or private artifacts.

Batch-level questions and option choices should be recorded in:

```text
experiments/question_decision_log.csv
```

Use it to capture the concrete question, candidate options, selected option, evidence needed, result, and next question for each experiment batch.

Open strategic questions should be maintained in:

```text
experiments/question_backlog.csv
```

Use this file as the live queue of what to decide next. Each row includes the question type, decision effect, options, selected path, dependencies, and review trigger.

## Current Public LB Notes

Confirmed useful references from our tracker:

- `7.235`: Wellbore wizard physics PF stack, current best in our logs
- `7.263`: David v12 budget guarded clean GPU
- `7.588` to `7.606`: Ricardo/Fleongg-style blends
- `7.703`: David bimodal model package branch

Rejected or risky:

- naive train TVT lookup scored extremely badly and is not a safe route
- static replay notebooks failed hidden rerun formatting
- large artifact-only transfers can fail if alignment is wrong

## Current High-Priority Directions

1. Run and audit `Degnonguidi 7.159` fork when Kaggle GPU slots are available.
2. Run and audit `Baidalin 7.201` fork after that.
3. Monitor Henry TabICL / Sunny blend and Romantamrazov GPU runs.
4. Use local surrogate scoring before deciding whether a generated output is worth submitting.

## Why This Repo Is Lean

The local workspace contains many pulled public notebooks and generated artifacts, but the GitHub repo intentionally keeps only the files teammates need immediately:

- core scripts
- lightweight reports and trackers
- five important Kaggle kernel forks
- setup instructions

Large outputs, pulled reference notebooks, and generated submissions are excluded to keep cloning fast and avoid accidentally publishing data or model artifacts.

## Suggested Collaboration Split

Person A: data and diagnostics

- maintain reports
- inspect bad wells and trajectory failures
- run local surrogate scoring
- verify submission sanity

Person B: modeling and Kaggle kernels

- push/run Kaggle kernels
- download outputs
- submit only audited candidates
- maintain experiment tracker

## Useful Commands

Check Kaggle submissions:

```powershell
kaggle competitions submissions -c rogii-wellbore-geology-prediction --csv
```

Check a kernel:

```powershell
kaggle kernels status leemarc223/<kernel-slug>
```

Download kernel output:

```powershell
kaggle kernels output leemarc223/<kernel-slug> -p artifacts\<output-folder>
```

Submit a code-competition notebook output:

```powershell
kaggle competitions submit -c rogii-wellbore-geology-prediction -k leemarc223/<kernel-slug> -v 1 -f submission.csv -m "message"
```

## Team Notes

Use GitHub for code, reports, and experiment coordination. Use Kaggle or local storage for large data and generated outputs.

Do not commit:

- Kaggle API credentials
- competition data
- downloaded artifacts
- generated submission CSVs
- large model files
