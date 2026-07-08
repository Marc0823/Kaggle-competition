# ROGII — Hard-Won Lessons & Strategy (2026-07-08)

Consolidated understanding after a long multi-day push. Written so future sessions
do not repeat the same detours. **Read this before spending more effort or slots.**

## 0. TL;DR — the single most important thing

**Diagnose what actually moves the score BEFORE modeling.** Most of our wasted
effort came from optimizing an internal CV that does not predict the public board.
This competition has a split personality:

- **Public LB = a leakage/overlap game**, not a geology-model quality contest.
- **Private LB (final rank / prize) = honest-model quality on novel wells**, which
  we can only proxy with internal pseudo-hidden CV.
- **Our internal native-mask CV ≈ private-LB behavior; it is NOT ≈ public LB.**

## 1. The scoring mechanism (the crux we learned late)

- Code competition with hidden rerun. Downloadable `test/` has only 3 visible wells
  (000d7d20, 00bbac68, 00e12e8b); `sample_submission.csv` = 14,151 rows over those 3.
  At scoring, Kaggle swaps in the real hidden test wells; the notebook must
  dynamically discover wells. Static replay is rejected.
- **The 3 visible test wells are ALSO in `train/` with full ground-truth TVT** —
  a genuine answer leak. Metric = pooled RMSE over predicted toe-end rows.
- **The 7.10–7.30 public plateau is NOT a better model.** It is a decent
  correlation base + two board-specific layers: (a) a **guarded overlap/exact-match
  override** that reconstructs TVT for hidden wells that duplicate train wells, and
  (b) **gold visible-prefix calibration**. These help PUBLIC and are ~no-ops on
  PRIVATE (novel wells) → the plateau will shake down on private.
- **Overlap exploitation ceiling ≈ 7.27** (the teammate's affine-overlay line hit
  7.278/7.294; a naive exact-copy scored 11,551 — rejected). Our 7.182 stack
  already contains the overlap override, so stacking more overlap adds ~nothing.
- **Honest models land at board 8–14** — confirmed by every publicly-shared "real
  model" (8.099; DWT 9.251; 9.538; romantamrazov 9.956/10.811; pilkwang 12.049)
  AND by all of our from-scratch work (neural cross-attn **12.87**, domain-feature
  LightGBM/mycarta **14.09**, last_value/PF/router ~**14.7**). This is the "honest
  manifold."

## 2. What we tried and what it scored

| Approach | Internal CV | Board | Verdict |
| --- | --- | --- | --- |
| last_value baseline | 14.68 | — | floor |
| from-scratch router/PF/DTW/Viterbi | ~14.6–14.8 | — | all hit GR-aliasing wall; net ~baseline |
| feature-GBM (tortuosity/NCC/offset, ours) | ~16 | — | landed at baseline (missing per-row alignment + strong offset-well signal) |
| neural cross-attn aligner (ours) | 14.74 | **12.87** | first novel model on board; not competitive |
| mycarta domain-LightGBM fork | 14.78 | **14.09** | ran in fast/debug mode; honest, not competitive |
| our 7.182 physics-PF stack fork (pre-session) | — | **7.182** | our best; has overlap override |

Key negative results (do not re-try blindly):
- **GR↔typewell alignment is fundamentally aliased** (oscillatory, self-similar):
  PF/NCC/Viterbi/attention all rescue high-drift wells but lock onto wrong
  positions elsewhere; correct-vs-aliased large moves are indistinguishable at
  prediction time. Prefix hold-out does NOT predict hidden-suffix wins.
- **TVT is NOT ~−Z+c** (Z-projection RMSE 104 vs 15.7). Within a lateral the
  TVT-vs-Z slope ≈ 0 (mean +0.057) while global cross-well r = −0.96 → **TVT in the
  toe is set by formation dip in the bit azimuth (a cross-well structural quantity)**.
  → the #1 honest lever is an **offset-well multi-well structural/dip framework**,
  which we have not built well (our spatial KNN probe failed: wells too sparse,
  median neighbor ~1548 XY units — needs a real dip/structural surface, not KNN).
- Soft-DTW is a poor fit: wells UNDULATE (~24 direction reversals median) → the
  alignment is non-monotonic, so monotonic DTW is wrong.
- Neural scale-up (bigger/longer) OVERFIT (val 15.96 worse than the small 14.74);
  capacity is not the bottleneck. Add best-checkpoint restore + multi-cut
  augmentation if revisiting.

## 3. Fork-ops reality (whack-a-mole — budget for it)

Competitive public notebooks are NOT portable. Each fork needs surgery:
- **GPU:** default P100 = compute sm_60, too old for Kaggle's preinstalled torch
  (`no kernel image`). Fix: `--accelerator NvidiaTeslaT4` / `machine_shape:
  NvidiaTeslaT4` (sm_75 works out of the box). LightGBM/CatBoost/numba are fine on
  P100 (torch is the only thing that breaks).
- **New-kernel 403:** when forking a pulled kernel, DELETE `id_no` from the
  metadata (it points to the origin kernel) — rebuild clean minimal metadata.
- **External module deps (crash on import):** koolbox (mycarta, takuya, kokinn,
  dualpipe, bern), hill_climbing/Climber (DWT). koolbox comes from the
  `phongnguyn23021656/koolbox-offline` dataset; Climber is a Caruana greedy
  ensemble (we wrote a self-contained stub — see scratch).
- **Hardcoded dataset paths:** DWT hardcodes `/kaggle/input/datasets/ravaghi/...`;
  real mount is `/kaggle/input/wellbore-geology-prediction-artifacts`.
- **Pretrained-artifact detection:** degnonguidi Pipeline B looks for models at
  `CFG.ARTIFACTS/models_B`; the fleongg models (`fleongg/rogii-claude-models-pub`:
  features.json + lgb0/1/2.pkl) sit at that dataset's ROOT, so B never finds them
  and **trains from scratch → ~11h feature build → DeadKernelError**. This killed
  the Degnonguidi 7.159 fork **8 times**; a glob patch did not resolve it →
  **ABANDONED degnonguidi** (heavy dual-pipeline, not worth more 11h runs).
- **Unsafe train→test TVT_input row copy** (`hw_te['TVT_input']=hw_tr[...].values`)
  in 7153/takuya/dualpipe/bern — public-only overlap trick; trivially removable but
  those notebooks are non-portable for other reasons (koolbox + heavy PF).
- **Runtime:** heavy PF/beam dual-pipelines run hours and risk the 9h limit /
  DeadKernel; prefer CPU-light notebooks (DWT) that use pretrained artifacts.

## 4. Strategic conclusion

- **Podium (5.26) / top-10 (6.30) is NOT reachable** with any public artifact or
  our from-scratch work — it uses a materially stronger structural/inverse model
  or private-invisible tricks not shared publicly.
- **Realistic public ceiling ≈ 7.08–7.13 (top-100)** via land-a-7.159 + blend, but
  **most of that reverts on private**.
- **For the FINAL/private ranking (the goal): build/land the strongest HONEST model
  and validate it on internal CV.** When the overlap-chasers shake down on private,
  a genuinely strong honest model (internal CV → 8–10) can rank durably well.
- The #1 honest lever = **offset-well structural/dip framework** (cross-well
  formation dip in the bit azimuth). Secondary honest levers: Q-3D tortuosity
  (−0.107 in mycarta), multi-scale NCC, self-correlation, PF/state-space engine.

## 5. Current assets / final-submission plan

Kaggle lets you pick **2 final submissions** — pick for PRIVATE robustness:
1. **The strongest honest model** — currently landing the **DWT 9.251** fork (clean,
   CPU, no overlap, honest → its board ≈ its private). If it runs, it is far better
   than our from-scratch ~14. Then improve it with the offset-well lever.
2. **A hedge** — the 7.182 stack (decent base + overlap; in case private is less
   overlap-punishing than expected). Do NOT pick two overlap-heavy notebooks.

## 6. If starting over (the efficient path)

1. Run the "what moves the score" diagnostic FIRST (public=overlap, private=honest,
   internal CV=private proxy). Decide public-chase vs private-durable up front.
2. For private: fork ONE clean honest base (DWT-class), get it running, measure its
   internal CV, then add the offset-well structural framework. Don't grind
   from-scratch alignment (aliasing wall) or heavy non-portable stacks.
3. Reserve slots; every submission is a planned experiment. Two finals = 1 honest
   + 1 hedge.
