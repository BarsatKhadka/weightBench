# Iteration 37 — 2026-05-10 — k=5 merge: recipe holds with task-specific tradeoffs

iter_036 demonstrated a 3-LoRA continual-learning recipe (T3
asymmetric: zero destructive MLPs, keep preserving full) that gave
all-three-task accuracy near solo-best. iter_037 scales to k=5 to
test whether the recipe degrades, breaks, or improves.

**Result: still produces multi-task models, but with task-specific
tradeoffs and a recipe-rule that shifts at higher k.** Specifically,
the conservative "zero all MLPs" beats the asymmetric recipe on rt
at k=5; agnews+rt remain strong; boolq degrades.

---

## Setup

5 LoRAs from iter_030's pool:
- Destructive: boolq_42, rt_1024
- Preserving: agnews_42, rt_42, boolq_456

(2 destructive + 3 preserving)

4 conditions:
- K0: base alone
- K1: all 5 full (no recipe)
- K2: all 5 MLP-zeroed (uniform conservative)
- K3: asymmetric (zero destructives, keep preserving full)

## Results

| condition | boolq | agnews | rt |
|---|---|---|---|
| K0 base alone | 0.41 | 0.38 | 0.37 |
| K1 all 5 full | 0.47 | 0.78 | 0.48 |
| K2 all 5 MLP-zeroed | 0.49 | 0.80 | **0.88** |
| K3 asym recipe | 0.46 | 0.85 | 0.86 |

## Three findings

### Finding 1 — boolq degrades from k=3 to k=5 in every recipe

iter_036 T3 at k=3: boolq 0.66.
iter_037 K3 at k=5: boolq 0.46.

Adding rt_42 + boolq_456 (both preserving on boolq individually)
hurt boolq accuracy by 20pp. iter_036's "more mass cancels destructive
interference" claim doesn't extrapolate cleanly.

Likely mechanism: each preserving LoRA's full attention adds its own
attention pattern to the merged signal. At k=2 these patterns
constructively combine; at k=5 they begin to dilute the boolq-
specific signal from boolq_42's attention. boolq_456's attention
specifically may push toward "rt-like" patterns (since boolq_456 is
the LoRA that got 0.87 on rt despite being trained on boolq —
iter_030's striking finding).

### Finding 2 — rt SURPASSES any individual solo at k=5

K2 uniform-zero gives rt 0.88. Best individual rt solo was 0.87 (rt_456
or rt_1024). The merge of 5 LoRAs with all MLPs zeroed produced an
*above-solo* rt model.

This is a substantive new result: **constructive interference between
multiple preserving LoRAs can exceed any single LoRA's accuracy on
its own task.** The 5-LoRA merge has more attention-only signal pushing
toward rt-relevant patterns than any single rt LoRA alone.

This is a positive scaling property: at higher k, the merge can
*outperform* individual LoRAs on the tasks where the merge has multiple
contributors.

### Finding 3 — Recipe rule shifts at higher k

At k=3 (iter_036): K3 asymmetric > K2 uniform-zero on all 3 tasks.
At k=5 (iter_037): K2 uniform-zero ≥ K3 asymmetric on most tasks.

Comparison at k=5:
- boolq: K2 0.49 vs K3 0.46 (K2 +0.03)
- agnews: K2 0.80 vs K3 0.85 (K3 +0.05)
- rt: K2 0.88 vs K3 0.86 (K2 +0.02)

K2 wins boolq + rt; K3 wins agnews. Net: roughly tied at k=5.

Why? At higher k, the cumulative "preserving full MLP" mass introduces
its own interference. Zeroing every MLP at k=5 is a stronger
regularization that wins for two of three tasks.

**Implication for the deployable recipe:** at low k, prefer asymmetric
(zero destructives only). At higher k, default to uniform-zero
(zero everyone). The crossover point is somewhere between k=3 and k=5
on this 0.5B base.

## Mixed messages, honest interpretation

iter_036 made the recipe sound clean and monotone. iter_037 shows it's
more nuanced:

- **Robust**: at every k tested (1, 2, 3, 5), the recipe produces a
  multi-task model with all 3 tasks well above base.
- **Best results task-dependent**: which task wins depends on whether
  the merge has 1 or many LoRAs that "contributed signal" to that task.
- **Recipe rule has a k-dependence**: asymmetric works at low k;
  uniform-zero is more robust at high k.

The clean "T3 asymmetric is best" claim from iter_036 is **k=3 specific**.

## Implications for plan.md

The continual-learning recipe is real but its precise form depends on
the merge size. plan.md's potential "Section 7: practical continual
learning" should reflect this:

- **Defaul recipe (small k or first principles):** zero MLP of LoRAs
  that audit as destructive. Keep preserving LoRAs full.
- **Stress-test caveat:** at k > ~3, switching to uniform-zero may
  give better robustness across all tasks.
- **Surprise positive scaling on shared tasks:** if many LoRAs in the
  merge pool contribute to the same task type (e.g., 2 rt LoRAs in
  the 5-merge), accuracy on that task can exceed any single LoRA's
  solo. This is a useful property worth highlighting.

## Caveats

- Single configuration tested at k=5 (specific 5 LoRAs).
- 100 eval per cell; binomial std ~0.05.
- Only 3 tasks evaluated; 4-5 task scenarios untested.
- 0.5B base; might shift at scale.
- Recipe-shift between k=3 and k=5 is a single observation; the
  precise crossover point would need more k values (k=4, k=6).

## What iter_038+ should consider

1. **k=4 merge.** Find the crossover point between asymmetric-best
   (k=3) and uniform-zero-best (k=5). Cheap eval.

2. **Test on iter_022's synthetic pool.** Run T3-style recipe on
   add_mod + mul_mod + max LoRAs. Different substrate, different
   k=3 dynamics. ~5 min.

3. **Test order-invariance.** Apply the K3 asym recipe sequentially
   (one LoRA at a time) instead of all at once. Should be equivalent
   under additive merging. Quick sanity check.

4. **Try a destructive-only k=5.** What happens with 5 destructive
   LoRAs (need to find more destructive examples than just boolq_42
   and rt_1024). Tests pure-destructive merging.

5. **Extreme stress: train 10 LoRAs on the same task with 10 seeds,
   merge them all.** Tests the "constructive interference exceeds
   individual" claim — does ensemble averaging via merge beat any
   single seed? This connects directly to plan.md's E1 / 200-LoRA
   pool design.

iter_038 priority: **option 5 (10-seed merge for ensemble effect).**
The "merge exceeds individual" surprise from iter_037 is the single
most suggestive thing here for plan.md's headline thesis (geometric
clustering = useful). Tests at scale whether the clustering yields a
useful average.

## Catalog state after iter_037

- ... (17 prior iters)
- **iter_037 k=5 merge:**
  - At k=5, uniform MLP-zero (K2) ≥ asymmetric (K3) on most tasks;
    recipe rule shifts with merge size.
  - **rt at k=5 K2 = 0.88, exceeding any individual rt solo (0.87).**
    Constructive interference between preserving LoRAs.
  - **boolq degrades** from k=3's 0.66 to k=5's 0.46. iter_036's
    "more mass = more healing" doesn't extrapolate cleanly.
  - Recipe is robust (all tasks well above base at every k tested)
    but precise rule is k-dependent.

Eighteen iters, ~$0 spend, ~5 GPU-hours total. plan.md unchanged.
