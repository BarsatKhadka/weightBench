# Iteration 29 — 2026-05-10 — Cross-task help mechanism: not cleanly explained by magnitude, alignment, or shared direction

iter_028 surfaced: pure agnews_42 LoRA scores 0.68 on BoolQ vs pure
boolq_42 LoRA scoring 0.55 on BoolQ. A cross-task LoRA outperforms
the same-task LoRA on its own task. iter_029 ran three diagnostic
probes to look for the mechanism.

**Result.** No single probe cleanly explains the effect. Each probe
ruled out one hypothesis and left the mechanism partially open.

---

## Setup

CPU-only probe over iter_024's 14-LoRA real-task pool. 9 representative
layers (q_proj/v_proj/down_proj at depths 0/11/23). Per layer, three
diagnostics:
- A: ||dW||_F per LoRA
- B: cosine(vec(dW_a), vec(dW_b)) for selected pair types
- C: projection of each LoRA's dW onto Σ(all 14 dWs) direction

## Probe A — magnitude per layer (partial signal, not a uniform story)

Mean ± std of ||dW||_F per task per layer:

| layer | agnews | boolq | rt |
|---|---|---|---|
| L0 q_proj | **0.345** ± 0.028 | 0.264 ± 0.033 | 0.342 ± 0.013 |
| L0 v_proj | **0.122** ± 0.013 | 0.096 ± 0.011 | 0.106 ± 0.010 |
| L0 mlp_down | **0.357** ± 0.046 | 0.282 ± 0.039 | 0.310 ± 0.020 |
| L11 q_proj | 0.281 ± 0.008 | **0.497** ± 0.030 | 0.301 ± 0.023 |
| L11 v_proj | 0.108 ± 0.009 | 0.107 ± 0.013 | 0.080 ± 0.005 |
| L11 mlp_down | **0.290** ± 0.028 | 0.227 ± 0.030 | 0.225 ± 0.018 |
| L23 q_proj | 0.265 ± 0.020 | 0.254 ± 0.058 | 0.235 ± 0.025 |
| L23 v_proj | 0.100 ± 0.010 | 0.114 ± 0.019 | 0.140 ± 0.033 |
| L23 mlp_down | 0.226 ± 0.028 | 0.221 ± 0.026 | **0.320** ± 0.043 |

Reading: **agnews has the largest magnitude in 4 of 9 probed layers
(early-network attention + early/middle MLP). boolq has the largest
in only 1 layer (L11 q_proj). rt has the largest in 2.**

If "agnews helps boolq because agnews pushed harder in the right
layers" is the mechanism, we'd expect agnews magnitudes to dominate
in *boolq-relevant* layers. We don't yet know which layers are
boolq-relevant; this would need a sensitivity analysis (perturb each
layer separately, measure boolq accuracy change).

So magnitude is *consistent with* a layer-targeted story but doesn't
prove it.

## Probe B — cosine of dW vectors (counterintuitive)

For three pair types, mean cosine of vec(dW_a) and vec(dW_b) over
9 probed layers:

| pair type | mean cosine | min | max |
|---|---|---|---|
| agnews-agnews same-task (42 vs 123) | **+0.006** | -0.001 | +0.015 |
| boolq-boolq same-task (42 vs 123) | +0.023 | -0.000 | +0.092 |
| agnews-boolq diff-task (42 vs 42) | **+0.034** | -0.032 | +0.167 |

**Same-task LoRAs are *less* aligned in dW-vector cosine than diff-
task LoRAs.** This counterintuitively contradicts iter_022's C1
finding (same-task pairs are *more* similar in subspace principal-
angle distance).

The two metrics measure different things:
- **C1 / subspace distance:** which directions are *spanned* by the
  rank-16 update. Same-task LoRAs span similar subspaces.
- **Vec-cosine:** which specific *pattern* (point in those directions)
  is learned. Same-task LoRAs learn different patterns within their
  shared subspace.

Reading: **same-task LoRAs share the *direction set* but not the
*specific point*** — different seeds explore different parts of the
same subspace, consistent with iter_026's "task identity =
neighborhood, not point" finding.

The diff-task pair (agnews-boolq) has higher vec-cosine because both
tasks share some "general adaptation direction" outside their task-
specific Region 2 subspaces. This direction is present in any LoRA
that genuinely fine-tunes (vs an untouched LoRA), and same-task
seed-pairs cancel it out via their varied within-subspace learning.

This is a real geometric finding worth follow-up: **the apparent
contradiction between high subspace overlap and low vec-cosine on
same-task is informative about how LoRA training explores its
task subspace.**

## Probe C — shared-adaptation direction (rules out one hypothesis)

For each LoRA, compute projection of vec(dW) onto vec(Σ_all 14 dWs)
direction (the "average adaptation" direction):

```
Per-task mean ± std:
  agnews     : 0.273 ± 0.046
  boolq      : 0.271 ± 0.057
  rt         : 0.279 ± 0.056

Per-LoRA notable values:
  agnews_42  : 0.259 (BELOW agnews mean)
  boolq_42   : 0.299 (ABOVE boolq mean)
```

If the cross-task-help mechanism were "agnews_42 learned the
universal-fine-tune direction more strongly than boolq_42 did,"
agnews_42 should have HIGH projection and boolq_42 LOW. The opposite
holds: **agnews_42 (the one that helps) projects 0.259, BELOW its
task mean. boolq_42 (the one being helped) projects 0.299, ABOVE its
task mean.**

**This rules out "shared-direction-magnitude" as the mechanism.**

## What the probes do and don't say

**Rule out:**
- Cross-task help is NOT explained by agnews_42 having more "universal
  signal" magnitude (Probe C).
- Cross-task help is NOT explained by uniformly higher dW magnitudes
  (Probe A — agnews has larger magnitude in some layers, smaller in
  others).

**Consistent with (but not proven):**
- Layer-targeted help: agnews_42 has bigger ||dW|| at certain early
  layers (L0 attention/MLP, L11 MLP) which may happen to be the
  layers most useful for boolq accuracy. Would need sensitivity
  analysis to confirm.

**New geometric finding:**
- Same-task LoRAs are less vec-cosine-aligned than diff-task pairs
  despite being more subspace-distance-similar. **Same-task LoRAs
  share direction-set but learn different specific points within
  it.** Sharpens iter_026's "neighborhood, not point" picture.

## Implications for plan.md

1. **The cross-task-help finding remains unexplained at the mechanism
   level.** iter_028 marked it "needs replication"; iter_029 didn't
   refute it but didn't explain it either. Continued caution about
   interpreting it.

2. **A new C1-vs-vec-cosine geometric distinction** worth adding to
   plan.md's framing: "Region 2 subspace identity" (C1) and "specific
   learned pattern" (vec-cosine) are decoupled. Same-task LoRAs share
   the former but not the latter.

3. **Layer-sensitivity analysis is the natural next probe.** Perturb
   each probed layer separately (zero out dW at that layer only),
   measure accuracy on each task. Builds a per-layer "boolq sensitivity"
   profile. Then cross-reference against magnitude differences to
   test the layer-targeted hypothesis.

## Caveats

- 9 probed layers (out of 168). Other layers could tell different
  stories.
- Single seed pair tested for vec-cosine probe. Replication across
  more pairs needed.
- Probe C uses sum-of-all-dWs as "shared direction" — this includes
  task-specific noise from each LoRA. A cleaner signal would be the
  top singular vector of [dW_1 | dW_2 | ... | dW_14] stacked, not
  the simple sum.

## What iter_030+ should consider

1. **Per-layer ablation for boolq sensitivity.** Take agnews_42 and
   boolq_42; for each layer, zero out one LoRA's dW at that layer
   only, measure boolq accuracy change. Builds a layer importance
   profile. Cost: 168 evals × 2 LoRAs × ~30s = ~3 hours. Could probe
   subsets first.

2. **Replicate cross-task help with more seeds.** iter_028 used
   seed-42 of each task. Try seed-123 of each, seed-456, etc.
   Does boolq_seed_X always score lower than agnews_seed_Y on
   boolq? Tightens the finding statistically.

3. **Train real-task pool to convergence and re-test.** iter_028's
   weak-LoRA hypothesis ("light training → cross-task helps") would
   predict the effect *disappears* once LoRAs are properly
   specialized. ~3 GPU-hours.

4. **The "shared adaptation direction" geometric finding** deserves
   its own iteration. Compute the top singular vectors of the
   stacked dW across all 14 LoRAs, see if there's a clean rank-1 or
   rank-r "task-agnostic adaptation subspace." Connects to plan.md's
   Universal Weight Subspace Hypothesis (2512.05117 in Synthesis).

iter_030 priority: **option 2 (replicate with more seeds).** Quick
statistical confirmation of the iter_028 finding before investing
in deeper mechanism work.

## Catalog state after iter_029

- A11 (iter_020), A01+A07 (iter_021), C1 synthetic (iter_022),
  E2 trajectory (iter_023), C1 real-task (iter_024), substep+region
  (iter_025), trajectory MDS (iter_026), LMC interp synth (iter_027),
  LMC interp real (iter_028).
- **iter_029 cross-task help mechanism probe:**
  - Magnitude story (Probe A): partial; agnews larger in 4/9 probed layers.
  - Vec-cosine surprise (Probe B): same-task LoRAs LESS aligned in
    vec-cosine than diff-task LoRAs (despite C1 saying same-task
    subspaces are more similar). New geometric distinction:
    direction-set vs specific-pattern.
  - Shared-direction (Probe C): rules out "agnews_42 learned universal
    direction more strongly" — agnews_42 actually projects BELOW
    task mean.
  - Mechanism for cross-task help remains unexplained; layer-targeted
    hypothesis is consistent with data but not proven.

Ten iters, ~$0 spend, ~3.5 GPU-hours total. plan.md unchanged.
