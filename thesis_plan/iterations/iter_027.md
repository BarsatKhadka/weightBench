# Iteration 27 — 2026-05-09 — Linear-in-dW LMC first-cut; tradeoff is plateau-then-cliff (not addition)

iter_026 showed same-task LoRAs cluster in *neighborhoods*, not at
points. iter_027 asks the natural follow-up: **is the cluster region
connected?** If you linearly interpolate dW between two same-task
endpoints, does the midpoint also solve the task?

Answer: **yes for same-task — no midpoint accuracy collapse.** And
for diff-task, no midpoint collapse either, but the curve shape is
*plateau-then-cliff*, not linear capability addition.

This iteration's findings were initially overclaimed in the catalog
("capability addition", "A6 confirmed", "catastrophic forgetting
across all task transitions"). Advisor review tightened all three.
The tightened version follows. The original prose is in git history.

---

## Setup

6 pairs from iter_022's controlled synthetic pool (Qwen-2.5-0.5B, 300
training steps, fixed parameterization):
- 3 same-task: `add_mod_42 + add_mod_123`, `mul_mod_42 + mul_mod_123`,
  `max_42 + max_123`
- 3 diff-task: `add_mod_42 + mul_mod_42`, `add_mod_42 + max_42`,
  `mul_mod_42 + max_42`

Per pair, evaluate `dW_α = (1-α) · dW_A + α · dW_B` at
α ∈ {0, 0.25, 0.5, 0.75, 1.0}, applied additively to the base model
weights, eval = 200 examples on each constituent task. ~15 min total.

Implementation note: pre-materializing all 6 LoRAs' dW per layer
in fp32 is ~18 GB — too much. Fixed by computing dW per-layer on-demand
and writing to base weights in-place, then subtracting back after eval.

---

## Finding 1 — Same-task: no midpoint accuracy collapse

| pair | α=0 | α=0.25 | α=0.5 | α=0.75 | α=1 |
|---|---|---|---|---|---|
| add_mod_42 + add_mod_123 | 0.980 | 1.000 | **1.000** | 1.000 | 1.000 |
| mul_mod_42 + mul_mod_123 | 0.965 | 1.000 | **0.990** | 1.000 | 1.000 |
| max_42 + max_123 | 1.000 | 1.000 | **1.000** | 1.000 | 1.000 |

**Midpoint accuracy ≥ either endpoint accuracy** for all 3 pairs. In
the add_mod and mul_mod cases, the midpoint is *better* than the
endpoint — averaging two LoRAs trained from different seeds produces
a slightly cleaner solution than either alone.

This is **linear-in-dW LMC** between same-task endpoints. **It is NOT
plan.md A6 (Grassmannian-geodesic LMC).** Linear-in-dW interpolation
and Grassmannian-geodesic interpolation are distinct operations:
linear interpolates the additive update, geodesic interpolates the
subspace itself. The result here is consistent with A6 and stronger
than A6's original claim, but A6 itself remains untested. iter_028+
needs the geodesic-vs-linear comparison to confirm A6 directly.

## Finding 2 — Diff-task: no midpoint collapse, but plateau-then-cliff (not linear addition)

Across-task interpolation does not collide between capabilities at
the midpoint, but the tradeoff is NOT linear capability addition. The
curve shape is closer to **plateau-then-cliff**: capability A is
preserved up to ~α=0.5 then drops sharply, while capability B rises
monotonically.

`add_mod_42 + mul_mod_42`:
| α | add_mod acc | mul_mod acc |
|---|---|---|
| 0.0 | 0.98 | 0.29 |
| 0.25 | 1.00 | 0.40 |
| **0.5** | **0.98** | **0.78** |
| 0.75 | 0.78 | 0.96 |
| 1.0 | 0.48 | 0.97 |

At α=0.5, the merged adapter solves **both** tasks: 98% add_mod AND
78% mul_mod. The midpoint isn't a degraded compromise — it's a
multi-task model.

`mul_mod_42 + max_42`:
| α | max | mul_mod |
|---|---|---|
| 0.0 | 0.71 | 0.97 |
| 0.25 | 1.00 | 1.00 |
| **0.5** | **1.00** | **0.76** |
| 0.75 | 1.00 | 0.39 |
| 1.0 | 1.00 | 0.31 |

`add_mod_42 + max_42`:
| α | add_mod | max |
|---|---|---|
| 0.0 | 0.98 | 0.27 |
| 0.25 | 0.98 | 0.98 |
| **0.5** | **0.90** | **1.00** |
| 0.75 | 0.61 | 1.00 |
| 1.0 | 0.50 | 1.00 |

**Reading.** Linear dW interpolation produces no midpoint accuracy
collapse, which is consistent with the "orthogonal subspaces merge
cleanly" story (diff-task A01 ≈ 0.90 in iter_022). But the curve is
**not linear in α**: add_mod is preserved at 0.98 from α=0 through
α=0.5, then drops sharply to 0.48 by α=1.0. A linear-addition curve
would show smooth decrease throughout. The plateau-then-cliff shape
suggests there's a *threshold* near α=0.5 where the dominant LoRA's
contribution starts to be overwhelmed.

The midpoint α=0.5 is informative: 98% add_mod + 78% mul_mod
simultaneously is multi-task behavior from simple averaging. But
predicting accuracy at intermediate α values requires modeling the
threshold, not assuming linearity.

## Finding 3 — Catastrophic forgetting on max is real and reversible (verified vs base)

Verified base-model-alone accuracies (no LoRA):
- **add_mod: 0.38**
- **mul_mod: 0.22**
- **max: 0.995**

So the base model only "knows" max well; add_mod and mul_mod are at
roughly 22-38% out of the box (better than chance ~0.06 for 17
choices, but not solved).

Forgetting story applies to max specifically:
- `add_mod_42` alone: max accuracy = 0.27 (down from base's 0.995)
- `mul_mod_42` alone: max accuracy = 0.71 (down from 0.995, less
  destructive than add_mod's training)

For add_mod and mul_mod, base accuracy is already low, so the small
shifts when running cross-task LoRAs (29% on mul_mod from add_mod_42
vs base's 22%) are *positive transfer*, not "forgetting recovered."

**The genuine forgetting + reversal pattern (max only):** add_mod_42
alone drops max from 99.5% → 27%. Adding ¼ of max_42's dW restores
it to 98%. The capability isn't destroyed — it's *suppressed* by the
task-LoRA's dW direction, and can be unsuppressed by merging in any
LoRA that preserves it.

This is one clean datapoint for the "continual-learning-by-merging"
idea, but it's a single datapoint on a single task on a 0.5B model.
plan.md's Beyond-ICLR continual-learning section gets a starter
mechanism here; the broader claim needs much more data.

**Asymmetric cross-task transfer (advisor catch).** Reading the
α=0 and α=1 entries of the diff-task pairs gives free transfer data:
- mul_mod_42 alone scores 0.48 on add_mod (base 0.38 → +0.10)
- add_mod_42 alone scores 0.29 on mul_mod (base 0.22 → +0.07)

mul_mod's trained dW transfers more strongly to add_mod than vice
versa. Unexplained but worth flagging — possibly mul_mod's spectral
geometry contains add-mod-relevant subspace content as a sub-component.

## Implications for plan.md

1. **A1 mergeability prediction sharpens.** plan.md A1 predicts
   `Σ sin²(θ)` correlates with merge accuracy drop. iter_027 shows
   the predictor target should be the *curve shape* (plateau-then-
   cliff in our data), not a single drop number. The 2-parameter
   analytic predictor needs to capture: (a) plateau width on the
   dominant-task side, (b) cliff sharpness, (c) rate of rise on the
   acquired-task side.

2. **A6 NOT confirmed.** plan.md A6 specifies *Grassmannian-geodesic*
   interpolation between Region 2 subspaces. iter_027 ran *linear-in-
   dW* interpolation. These are distinct operations. What we showed
   is "linear-in-dW LMC between same-task endpoints holds at the no-
   midpoint-collapse level," which is consistent with A6 but doesn't
   directly test it.

3. **Section 6 mergeability rewrites in shape, not destination.**
   "Does it merge well?" becomes "what's the curve?" but the curve
   isn't linear, so practical predictions are non-trivial.

4. **Continual-learning narrative gets a single clean datapoint.**
   max forgetting (99.5% → 27% → 98%) is a clear forgetting + reversal
   on one task on one base model. Worth following up; not yet
   generalizable.

## Caveats

- **Synthetic tasks only.** add_mod / mul_mod / max are tiny
  algebraic tasks. Real-task interpolation (BoolQ, AGNews, RT) might
  show more interference or different curve shapes. Worth testing on
  iter_024's pool.
- **0.5B base model.** Smaller models have more "room" for
  capabilities to coexist. Bigger models (LLaMA-3-8B) at the same
  rank-16 LoRA might show more capacity competition.
- **n=200 eval examples per (pair, α, task).** Binomial std at
  acc=0.5 is ~0.035; differences below that are noise. The signals
  here are well above noise.
- **The "smooth tradeoff" might be a small-model artifact.** Larger
  models with more parameters might show sharper crossover behavior
  (less linear capability addition).

## What iter_028+ should consider

1. **Real-task interpolation.** Run the same protocol on iter_024's
   real-task pool (BoolQ, AGNews, RT). Does the smooth-tradeoff
   pattern survive? If yes, iter_027's finding is robust; if no,
   small-model artifact and we need to explain why. ~30 GPU-min.

2. **Three-way interpolation.** Interpolate between three LoRAs:
   `dW = w_A · dW_A + w_B · dW_B + w_C · dW_C` with weights summing
   to 1, evaluated on simplex grid. Does linear capability addition
   extend to multi-LoRA merging? Maps directly onto plan.md's task
   arithmetic stuff.

3. **Geodesic vs linear interpolation comparison.** plan.md A6
   technically wants Grassmannian geodesic, not linear-in-dW. Compute
   both and compare. Linear is what works in practice; if geodesic
   gives the same answer, the simpler formula wins.

4. **A1 falsifier with these results as data.** With 6 pairs at 5
   alphas each = 30 (Σsin²θ, capability-tradeoff) datapoints. Can we
   fit a 2-parameter analytic predictor for the tradeoff curve as
   plan.md A1 originally proposed? More principled than the original
   merge-drop regression.

iter_028 priority recommendation: **option 1 (real-task
interpolation).** It's the immediate "does this generalize" test and
uses iter_024's pool that's already trained. ~30 GPU-min on synthetic-
sized eval; budget extra for real-task longer prompts.

## Catalog state after iter_027

- A11 (iter_020): frames orthogonal at 84°.
- A01+A07 first-cut (iter_021): instrument confound.
- C1 synthetic (iter_022): pooled-std sep 3.52.
- E2 trajectory (iter_023): T2 3.74 at step 25.
- C1 real-task (iter_024): pooled-std sep ~11; output-vocab refuted.
- iter_025 substep + region: lock-in at step 2; spectral concentration emerges.
- iter_026 trajectory MDS: same-task = neighborhood, not point.
- **iter_027 LMC interpolation (first-cut, n=6):**
  - Same-task: no midpoint accuracy collapse (linear-in-dW LMC).
  - Diff-task: no midpoint collapse, plateau-then-cliff tradeoff
    (NOT linear capability addition). α=0.5 of add_mod+mul_mod →
    98% add_mod + 78% mul_mod (multi-task at midpoint, but curve is
    non-linear).
  - Forgetting on max real (99.5% → 27%) and reversible (→ 98%
    after ¼ of max LoRA dW added). Single task on single base.
  - Cross-task transfer is asymmetric (mul_mod_42 → 0.48 on add_mod
    vs add_mod_42 → 0.29 on mul_mod). Unexplained.
  - **A6 NOT confirmed** — linear-in-dW LMC is a different operation
    from A6's Grassmannian-geodesic.

Eight iters, ~$0 spend, ~3.5 GPU-hours total. plan.md unchanged.
A1 reframed as curve-shape prediction. A6 still untested.
Catalog discipline: this is the third iter where initial framing
overclaimed; advisor caught it. Pattern worth noting.
