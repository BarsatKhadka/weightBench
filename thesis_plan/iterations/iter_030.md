# Iteration 30 — 2026-05-10 — Cross-task help replicates partially; seed variance dominates

iter_028 surprised: pure agnews_42 LoRA scored 0.68 on BoolQ, beating
pure boolq_42 LoRA's 0.55. iter_030 replicates at scale: full
14-LoRA × 3-task accuracy matrix.

**Result.** iter_028's surprise was real but partly seed-specific.
Cross-task help is statistically robust on boolq (population-level)
but seed variance within a task is huge — and that variance, not
cross-task transfer, is what dominates the ranking.

---

## The 14×3 matrix

```
LoRA            boolq   agnews    rt
BASE            0.410   0.380   0.370
agnews_1024     0.710   0.850   0.640
agnews_123      0.660   0.830   0.570
agnews_42       0.680   0.870   0.720
agnews_456      0.690   0.850   0.720
agnews_789      0.510   0.820   0.600
boolq_1024      0.740   0.530   0.800   ← best boolq LoRA
boolq_123       0.600   0.360   0.460
boolq_42        0.560   0.160   0.080   ← destructive (kills others)
boolq_456       0.410   0.370   0.870   ← TIES best on rt
rt_1024         0.020   0.500   0.860
rt_123          0.220   0.160   0.710
rt_42           0.560   0.510   0.800
rt_456          0.180   0.470   0.870   ← best rt LoRA
rt_789          0.300   0.510   0.790
```

## Three findings

### Finding 1 — Cross-task help on boolq replicates at population level

Mean accuracy on boolq across 5 seeds:
- agnews seeds: (0.71 + 0.66 + 0.68 + 0.69 + 0.51) / 5 = **0.65**
- boolq seeds:  (0.74 + 0.60 + 0.56 + 0.41) / 4 = **0.58**
- rt seeds:     (0.56 + 0.22 + 0.56 + 0.18 + 0.30) / 5 = 0.36

**On average, agnews LoRAs score 7 percentage points HIGHER on boolq
than boolq LoRAs do.** This isn't a single-pair fluke — it holds
across the population.

But: **the *best* LoRA on boolq is still a boolq LoRA** (boolq_1024
at 0.74, beating agnews_1024 at 0.71). The population-mean cross-task
advantage doesn't translate to the per-seed-best LoRA winning.

Reading: at this training budget (300 steps × bs=4), boolq is hard
enough that boolq-specific training doesn't reliably specialize. Many
seeds fail to learn boolq well. Agnews, being easier (more pattern
in the targets), reliably produces a "decent fine-tune" that
generalizes to boolq — better than a poorly-converged boolq LoRA but
worse than a well-converged one.

### Finding 2 — Best on rt is a TIE between same-task and cross-task

- rt_456: 0.87 (rt LoRA)
- boolq_456: 0.87 (boolq LoRA, on rt)

**A LoRA trained on BoolQ ties for top accuracy on Rotten Tomatoes.**

boolq_456 is interesting: scores 0.41 on its OWN task (no learning
above base 0.41), 0.37 on agnews (base), but 0.87 on rt. The LoRA
"trained on boolq" essentially didn't learn boolq — but somehow
became excellent at rt. Most plausible: the boolq prompt format
("yes / no") taught the model a 2-token-vs-2-token distinction that
transferred verbatim to RT's "positive/negative" format.

This is a **prompt-format-mediated transfer** finding, not weight-
geometry-mediated. The LoRA that "answers in 1-2 tokens following a
binary cue" works for both yes/no and positive/negative.

### Finding 3 — Seed variance within a task is enormous

Each task's 4-5 seeds span huge ranges on the OWN task:
- boolq seeds: 0.41 → 0.74 (33-point spread)
- agnews seeds: 0.82 → 0.87 (5-point spread; agnews trained reliably)
- rt seeds: 0.71 → 0.87 (16-point spread)

And on OTHER tasks, the variance is even wilder. boolq seeds on rt:
0.08 (boolq_42 destroys rt) to 0.87 (boolq_456 ties best). Same task,
4 seeds, span 79 percentage points.

Two distinct LoRAs trained the same way on the same task (boolq, seed
42 vs seed 456):
- boolq_42: 0.56 boolq, 0.16 agnews, 0.08 rt — DESTROYS other tasks
- boolq_456: 0.41 boolq, 0.37 agnews, **0.87 rt** — preserves agnews,
  excels on rt despite "training" on boolq

Same training pipeline. Different random seed. Completely different
behavior on out-of-task evaluation. **Seed determines whether a fine-
tune is "destructive" (loses base capabilities) or "preserving"
(keeps them).** This is consistent with iter_026's "task identity =
neighborhood, not point" — different seeds end up at different points
within the cluster, with different transfer/destruction profiles.

## What this changes for plan.md

1. **iter_028's surprise has a population-level signal but it's not
   a clean "weight-space task identity is wrong" finding.** The
   surprise was a combination of (a) real cross-task transfer +
   (b) seed-specific weak training of boolq_42.

2. **A1 mergeability prediction needs to account for seed variance
   first.** Before predicting how two LoRAs merge, predict whether
   each LoRA individually is "destructive" or "preserving" — that
   matters more than Σ sin²θ.

3. **plan.md C1 (within-task collapse on Region 2 subspace) holds**
   in the geometric sense (iter_022/iter_024) but the geometric
   "task identity" doesn't translate into uniform behavioral
   outcomes. Same Region 2 cluster → wildly different per-seed
   behavior on out-of-task evaluation.

4. **Suggested addition to plan.md:** a "destructive vs preserving"
   diagnostic. Within a task's seed pool, separate LoRAs that
   preserve base capabilities from those that destroy them. Predict
   from weight geometry. The signal IS in the weights — boolq_42
   and boolq_456 must look different geometrically, even if both
   are in the same Region 2 cluster.

## Caveats

- 100 eval examples per cell, binomial std ~0.05.
- Single eval seed (12345). Different eval samples might shift small
  numbers but the >0.05 differences should be robust.
- 0.5B base model.
- 300-step training is light for boolq specifically.
- The "boolq_456 ties best on rt" finding might be an artifact of the
  yes/no → positive/negative format mapping; needs follow-up to confirm.

## What iter_031+ should consider

1. **What distinguishes destructive from preserving LoRAs?** boolq_42
   destroys both agnews and rt; boolq_456 preserves them and even
   excels on rt. Geometric probe: compare their Region 2 subspaces,
   spectral distributions, R1/total ratios. Cheap, CPU-only.

2. **Train more boolq seeds to distinguish "trained well" from
   "trained badly" patterns.** boolq is the noisy task; getting more
   seed runs would help statistics.

3. **Real-task LoRAs at convergence.** Train iter_024 pool to 1000+
   steps with eval-acc convergence; does the cross-task advantage
   on boolq disappear? Tests the "weak training → cross-task helps"
   hypothesis.

4. **Format-mediated transfer.** boolq_456 → 0.87 on rt suggests
   "1-2 token binary answer" pattern transfers. Test by training a
   "yes/no" LoRA on a third yes/no task and seeing if it transfers
   to RT.

iter_031 priority: **option 1 (geometric probe of destructive vs
preserving).** Most directly informative for plan.md, cheap, uses
existing data.

## Catalog state after iter_030

- A11, A01+A07 first-cut, C1 synthetic, E2 trajectory, C1 real-task,
  substep+region, trajectory MDS, LMC interp synthetic, LMC interp
  real, cross-task probe.
- **iter_030 cross-task matrix (n=14 LoRAs × 3 tasks = 42 cells):**
  - Cross-task help on boolq replicates at population level (agnews
    mean 0.65 > boolq mean 0.58 on boolq).
  - Best on rt is TIE between rt_456 and boolq_456 (both 0.87).
  - Seed variance within a task is enormous (boolq spans 33 points
    on own task, 79 points on rt). "Destructive vs preserving"
    distinction is real and seed-driven.
  - iter_028's surprise was real but partial; seed cherry-picking
    inflated the magnitude.

Eleven iters, ~$0 spend, ~4 GPU-hours total. plan.md unchanged.
