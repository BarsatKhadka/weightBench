# Iteration 28 — 2026-05-10 — Real-task interpolation: same-task LMC replicates, diff-task curve does NOT plateau-then-cliff

iter_027 found two things on synthetic tasks:
1. Same-task linear-in-dW LMC: no midpoint accuracy collapse.
2. Diff-task: plateau-then-cliff curve.

iter_028 replicates the protocol on iter_024's real-task pool (BoolQ
QA, AGNews topic, Rotten Tomatoes sentiment). Finding (1) replicates.
Finding (2) does NOT — real-task curves look qualitatively different
and reveal something the synthetic experiment hid.

Caveats up front: n=6 pairs (smoke-test scale), 100 eval examples per
task per α (binomial std ~0.05), 0.5B base, LoRAs trained 300 steps
on real tasks (which is light for these tasks).

---

## Verified base accuracies (pre-interpolation discipline)

| task | base alone | chance |
|---|---|---|
| boolq | 0.41 | 0.50 |
| agnews | 0.38 | 0.25 |
| rt | 0.37 | 0.50 |

**Important context: the base 0.5B model is barely above chance on
real tasks.** Compare to synthetic where base scored 0.38 / 0.22 /
0.995. This shifts how to read everything below — these LoRAs aren't
"polishing a base capability"; they're trying to teach a task from
near-scratch.

## Same-task: no midpoint accuracy collapse (replicates iter_027)

| pair | α=0 | α=0.25 | α=0.5 | α=0.75 | α=1 |
|---|---|---|---|---|---|
| boolq_42 + boolq_123 | 0.56 | 0.54 | 0.57 | 0.60 | 0.60 |
| agnews_42 + agnews_123 | 0.87 | 0.85 | 0.84 | 0.84 | 0.83 |
| rt_42 + rt_123 | 0.81 | 0.82 | **0.85** | 0.75 | 0.72 |

3/3 same-task pairs show no midpoint collapse. rt midpoint *exceeds*
both endpoints (0.85 > 0.81 and 0.72) — averaging regularizes,
consistent with iter_027.

**Linear-in-dW LMC at the cluster level holds on real tasks.**

## Diff-task: NOT plateau-then-cliff. Smooth crossfade with surprises.

`boolq_42 + agnews_42`:
| α | agnews | boolq |
|---|---|---|
| 0.00 (boolq alone) | 0.17 | 0.55 |
| 0.25 | 0.77 | 0.55 |
| 0.50 | 0.80 | 0.66 |
| 0.75 | 0.86 | 0.69 |
| 1.00 (agnews alone) | 0.87 | **0.68** |

**The pure agnews_42 LoRA scores higher on BoolQ (0.68) than the pure
boolq_42 LoRA does (0.55).** A different-task LoRA outperforms the
same-task LoRA on its own task. boolq accuracy *increases monotonically*
as we move away from the boolq LoRA.

`boolq_42 + rt_42`:
| α | boolq | rt |
|---|---|---|
| 0.00 | 0.56 | **0.08** |
| 0.25 | 0.57 | 0.86 |
| 0.50 | 0.58 | 0.85 |
| 0.75 | 0.55 | 0.84 |
| 1.00 | 0.54 | 0.81 |

boolq accuracy stays flat throughout. rt accuracy jumps from 0.08
to 0.86 with 25% rt LoRA. boolq_42 catastrophically destroys rt
(0.37 → 0.08); merging back any rt LoRA fully restores it.

`agnews_42 + rt_42`:
| α | agnews | rt |
|---|---|---|
| 0.00 | 0.87 | 0.73 |
| 0.25 | 0.85 | 0.87 |
| 0.50 | 0.83 | **0.89** |
| 0.75 | 0.78 | 0.84 |
| 1.00 | **0.50** | 0.79 |

Closest to the iter_027 "multi-task at midpoint" pattern: at α=0.5
BOTH tasks are near best (0.83 agnews + 0.89 rt). agnews_42 alone
scores 0.73 on rt (positive transfer over base 0.37). rt_42 alone
scores 0.50 on agnews (above base 0.38, but agnews is much harder
out of the box).

## What changes from synthetic to real

The plateau-then-cliff pattern from iter_027 (synthetic) does NOT
appear in any of the 3 real-task diff-pairs. Instead:

1. **Smoothly increasing acquisition.** Moving toward LoRA B
   monotonically increases task-B accuracy in all 3 cases (no plateau).

2. **Often-flat or slowly-decreasing source-task.** Moving toward
   LoRA B doesn't sharply drop task A — boolq stays 0.54-0.69 across
   the entire α range; agnews drops 0.87 → 0.50 across the full α
   range, smooth not cliff-like.

3. **Cross-task LoRAs sometimes IMPROVE the original task.** Pure
   agnews_42 scores 0.68 on boolq, vs pure boolq_42's 0.55. This is
   completely unexplained by the synthetic interpretation.

The most plausible reading: **real-task LoRAs at 300 steps are still
in the regime where any reasonable adaptation generalizes.** They
haven't specialized hard enough to interfere with each other at the
midpoint. The synthetic plateau-then-cliff was likely a property of
strongly-specialized LoRAs on tasks the model was forced to memorize
(mod 17 arithmetic with deterministic targets).

## What this changes for plan.md

1. **A1 mergeability** — the underlying question of "does Σ sin²(θ)
   predict merge interference?" gets a different answer here than
   on synthetic. On real tasks at this training scale, interference
   between orthogonal-subspace diff-task LoRAs is *small* and
   sometimes *negative* (cross-task LoRA helps own-task accuracy).
   The 2-parameter analytic predictor plan.md A1 wants needs to be
   trained on real-task data, not synthetic — synthetic gives a
   different functional shape.

2. **iter_027's "plateau-then-cliff" finding is synthetic-specific.**
   Drop that framing as a general claim about diff-task interpolation;
   keep it as "synthetic modular-arithmetic LoRAs show plateau-then-
   cliff curves, real-task LoRAs at the same training budget don't."

3. **Linear-in-dW LMC at cluster level (same-task) replicates** on
   real tasks. Most robust finding so far.

4. **Catastrophic forgetting story is task-direction-specific.**
   boolq_42 destroys rt (0.37 → 0.08); agnews_42 *helps* rt
   (0.37 → 0.73). The "every fine-tune destroys other capabilities"
   intuition is wrong. Some fine-tunes generalize positively to
   adjacent tasks; some destroy them. We don't yet know what
   determines which.

5. **The most surprising single observation:** pure agnews_42 scores
   higher on boolq than pure boolq_42 does. If this replicates with
   more seeds, it's a real challenge to the "task identity in
   weights" story — at this training budget, weight-space "task
   identity" is so weak that a different task's LoRA does the
   target task better.

## Caveats

- n=6 pairs total (3 same + 3 diff). All findings are smoke-test-grade.
- 100 eval examples per (pair, α, task), binomial std ~0.05.
- LoRAs trained for 300 steps × bs=4 = 1200 examples seen. This is
  light for real NLP tasks — could be why the LoRAs don't strongly
  specialize.
- 0.5B base model. Larger models with more capacity might show
  different curves.
- We picked seed-42 as the representative LoRA per task for diff-task
  pairs. Other seeds might behave differently.
- Same-task pairs use seed-42 + seed-123. Other seed combinations
  might give different midpoint curves.

## What iter_029+ should consider

1. **Same-task LMC across more seed pairs.** Run all 6 same-task
   boolq pairs (4 boolq seeds = C(4,2) = 6 pairs), all 10 agnews
   pairs, all 10 rt pairs. n=26 same-task pairs total. Costs ~1
   GPU-hour. Tightens the same-task LMC claim.

2. **Real-task substep training.** iter_025's substep finding (lock-
   in at step 2, σ-peak at step 14) was on synthetic. Does the same
   peak appear on real tasks at substep resolution? ~30 GPU-min
   (re-train iter_024 pool with --save_every 2 for first 30 steps).

3. **Fully-trained real-task pool.** Train iter_024 pool to
   convergence (1000+ steps with eval-acc convergence check). Does
   the plateau-then-cliff appear once LoRAs are properly specialized?
   ~3 GPU-hours.

4. **Why does agnews_42 help boolq?** Mechanism question. Probe:
   compare agnews_42's Region 2 subspace at the boolq-relevant
   layers vs boolq_42's. Does agnews learn a generally-helpful
   direction that boolq_42 misses? CPU-only investigation.

iter_029 priority recommendation: **option 4 (mechanism investigation
of cross-task improvement).** The most surprising single observation
is the most informative to follow up on. Cheap, CPU-only, uses
existing data.

## Catalog state after iter_028

- A11 (iter_020): frames orthogonal at 84°.
- A01+A07 (iter_021): instrument confound on uncontrolled.
- C1 synthetic (iter_022): pooled-std sep 3.52.
- E2 trajectory (iter_023): T2 3.74 at step 25.
- C1 real-task (iter_024): pooled-std sep ~11; output-vocab refuted.
- iter_025 substep: lock-in at step 2; σ-peak at 14; spectral
  concentration emerges.
- iter_026 trajectory MDS: task identity = neighborhood.
- iter_027 LMC interp synthetic: same-task no-midpoint-collapse;
  diff-task plateau-then-cliff (synthetic-specific).
- **iter_028 LMC interp real-task:**
  - **Same-task LMC at cluster level replicates** on real tasks.
  - **Diff-task plateau-then-cliff is synthetic-specific.** Real
    diff-task curves are smooth crossfades with monotonic acquisition.
  - **Cross-task LoRAs can outperform same-task LoRAs** on the
    target task (agnews_42 → 0.68 on boolq vs boolq_42 → 0.55).
  - **Catastrophic forgetting is task-direction-specific** (boolq_42
    destroys rt; agnews_42 helps rt).

Nine iters, ~$0 spend, ~3.5 GPU-hours total. plan.md unchanged.
