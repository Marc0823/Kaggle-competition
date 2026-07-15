# ROGII Wellbore Geology Prediction — working directives for AI agents

These are long-term working instructions for any agent (Claude Code or otherwise) contributing
to this competition. Read them before starting work. They are set by the project owner (Joe) and
take precedence over an agent's default habits. Detailed domain knowledge, tested candidates, and
the reproduction recipe live in `reports/lessons_and_strategy_2026-07-08.md` — read that too.

Competition goal: the **final/private ranking** (novel wells), not the public leaderboard. Our
banked honest base is the DWT fork — public **9.519**, internal native-mask CV **10.40**
(submission ref 54453597). New candidates are measured against that base, not against the naive
`last_value` CV baseline.

## Directive 1 — keep searching, systematically

- The objective is **not** to stop at "no method found" and **not** a one-shot attempt. It is a
  continuous, systematic loop: propose candidate directions -> validate honestly -> record the
  evidence -> drop unsupported hypotheses -> **expand the search space and keep going**.
- Prefer **low-cost, honest, reproducible** validation first. Use train masked-CV / out-of-fold
  (OOF) as the private-ranking proxy. When a small-scale result looks promising, **scale the
  validation up before drawing a conclusion** — do not generalize from one small sample, and do
  not treat an oracle (truth-selected) result as an achievable gain.
- Keep an evidence ledger of what was tried and what was observed (in the strategy/lessons doc and
  in agent memory), so future rounds build on prior evidence instead of repeating it.
- **Submission authority:** if a candidate shows a clear, reproducible honest improvement in local
  validation (stable OOF/masked-CV gain vs the DWT base, or a stable gain on a clearly-defined
  well-family via a guarded router) **and** passes the pre-submit audit, you may submit to Kaggle
  under the established conditions **without** waiting for confirmation. Pre-submit audit:
  (a) inputs are only test-available — no train-only fields (structural surfaces, Geology) and no
  hidden-label leakage; (b) format / row order / all-finite / value range / sane diff-vs-baseline
  / notebook-source risk all pass. After submitting, **record**: submission id, public score, the
  matching commit / notebook / source, and any gap between local validation and public. Watch the
  remaining daily slots; do not spend them on clearly-weak or merely-exploratory candidates.

## Directive 2 — neutral technical language

- Do **not** use emotional or strongly-directive words in reports or docs: avoid "gamble / bet"
  ("赌"), "dead" ("死了"), "give up" ("认输"), "ceiling" ("天花板"), and similar.
- Prefer neutral technical phrasing: *candidate direction*, *validation result*, *no stable
  improvement observed*, *insufficient current evidence*, *next search space*, *submittable
  conditions*, *risk points*, *locally applicable*, *needs further validation*.
- The purpose is to support rational technical decisions. Report a negative as "candidate X: no
  stable OOF improvement vs the DWT base observed (evidence ...); moving to the next search space",
  not as "X is dead / we hit the ceiling". Wording should not imply a direction must be abandoned
  when the evidence only shows it did not improve on this attempt.
