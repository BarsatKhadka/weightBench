# Iteration 36 — 2026-05-10 — 3-way merge: asymmetric recipe scales cleanly to k=3

iter_035 demonstrated a 2-LoRA continual-learning recipe (boolq_42 +
rt_1024 with MLP zeroed → multi-task model). iter_036 adds agnews_42
to test scaling and refines the recipe.

**Result: the asymmetric recipe (zero MLP of destructive LoRAs only)
produces a clean 3-task model.** All three tasks at near-best solo
accuracy, plus an interesting positive effect from agnews_42's
preserving MLP.

---

## Conditions

| ID | description |
|---|---|
| T0 | base alone |
| T1 | all 3 LoRAs added with full dW (naive merge) |
| T2 | all 3 LoRAs MLP-zeroed (uniform recipe) |
| T3 | asymmetric: zero MLP of destructives (boolq_42, rt_1024); keep agnews_42 full |
| T4 | only boolq_42 zeroed (most destructive); keep rt_1024 + agnews_42 full |

## Results

| condition | boolq | agnews | rt |
|---|---|---|---|
| T0 base | 0.41 | 0.38 | 0.37 |
| T1 all full | 0.56 | 0.81 | 0.85 |
| T2 all zeroMLP | 0.47 | 0.81 | 0.81 |
| **T3 asym (destructives zeroed)** | **0.66** | **0.86** | **0.85** |
| T4 asym (only boolq_42 zeroed) | 0.62 | 0.82 | 0.85 |

## Three findings

### Finding 1 — T3 is the cleanly-best recipe at k=3

T3 produces a 3-task model with:
- boolq 0.66 (above 4/5 boolq solos; below only boolq_1024 at 0.74)
- agnews 0.86 (matches best agnews solo, 0.87)
- rt 0.85 (close to best rt solo, 0.87)

**No retraining; pure post-hoc combination of three independent
fine-tunes.**

### Finding 2 — Don't zero preserving LoRAs' MLP

T2 (uniform: zero all 3 MLPs) drops boolq from 0.66 to 0.47. The 19
percentage point loss came from zeroing agnews_42's MLP, which was
preserving (no out-of-task destruction).

This refines the recipe: **only zero MLP of LoRAs that show
destructive character on out-of-task evaluation. Preserving LoRAs'
MLP carries useful fine-tuning information.**

The mechanism likely: agnews_42's MLP is a "well-behaved fine-tune
of MLP" that doesn't push against base capabilities but still
contributes general task-adaptation signal that helps related tasks
(here, boolq's binary-answer pattern).

### Finding 3 — Naive 3-way merge (T1) is decent

Even without any recipe (T1: all full additive merge), the 3-LoRA
sum gives boolq 0.56, agnews 0.81, rt 0.85. Compare to iter_035's
2-LoRA M5 (boolq_42 + rt_1024 full): boolq 0.55, agnews 0.34,
rt 0.70.

**Adding the preserving agnews_42 fully restores agnews from 0.34
to 0.81.** More mass in the merge → more cancellation of destructive
perturbations.

Implication: as you add more LoRAs to a continual-learning chain,
each new preserving LoRA helps cancel the destructive effects of
prior LoRAs. The "destructive interference" problem gets *easier*
with more LoRAs, not harder. This is a counter-intuitive scaling
property.

## The deployable recipe (refined)

```
Continual-learning-by-merge recipe:

  base_model = M

  for each new task t:
    L_t = train_LoRA(M, task=t)
    is_destructive_t = audit(L_t, held_out_tasks)
    if is_destructive_t:
        L_t = zero_mlp(L_t)
    M = M + L_t

  result: M solves all tasks t1, ..., tk
```

The `audit` step is iter_030's eval-on-other-tasks. ~30 sec per LoRA
on a 0.5B model.

The `zero_mlp` step is a pure tensor operation: drop all MLP
components from L_t, keep attention-only.

The merge step is summation of dWs.

**No retraining at any step.** Each LoRA is trained once, audited
once, and combined.

## Implications for plan.md

This is now substantive enough to suggest a formal addition to plan.md:

- **A new applied section / Section 7?** "Practical continual-learning
  via auditing and partial merging." Built on iter_030-036's results.
  Does NOT require theory beyond the empirical mechanism (attention
  carries task; MLP carries interference). Connects directly to plan.md's
  "Beyond ICLR" continual-learning vision.

- **A1 mergeability prediction is DIFFERENT from this.** A1 predicts
  *can two LoRAs merge cleanly*. iter_036 shows you can *make* them
  merge cleanly via the recipe. The relationship: A1 says "untreated
  merges have varying compatibility"; iter_036 says "treated merges
  achieve compatibility." Both useful; complementary.

## Caveats

- 3 LoRAs in this merge. Untested at 5+, 10+, 20+.
- 100 eval examples per cell.
- Only "preserving" LoRA tested is agnews_42. Other preserving LoRAs
  (rt_42, boolq_456) might give different numbers. The "don't zero
  preserving" rule needs replication.
- 0.5B base model. Larger bases might shift the attention/MLP balance.
- Synthetic mod-arithmetic LoRAs not tested in this recipe — would
  iter_022's pool benefit similarly?
- We didn't test what happens at k=1 with a destructive LoRA for the
  "naive merge naturally heals" claim. The story is: more LoRAs =
  more healing, but that's based on k=2 and k=3 datapoints only.

## What iter_037+ should consider

1. **k=5 or k=6 merge.** Add agnews_456 + rt_42 + boolq_456 to the
   T3 recipe. Does the 5- or 6-way merge still hit near-best on every
   task, or do we see degradation? ~5 min eval.

2. **Sequential vs parallel.** Apply T3 sequentially (one LoRA at a
   time) vs all-at-once (the current). Should be equivalent under
   the additive model; verifies linearity.

3. **Other preserving LoRAs in the recipe.** Replace agnews_42 with
   rt_42 (a preserving rt LoRA) — does the recipe still work?

4. **Failure-mode hunting.** Find a 3-LoRA combination where the
   recipe FAILS. If we can't find one easily, the recipe is robust.
   If we find one, we learn its limits.

5. **Synthetic-pool replication.** Run T3-style recipe on iter_022's
   add_mod + mul_mod + max LoRAs. Does the same pattern hold?

iter_037 priority recommendation: **option 1 (k=5 merge).** Most
informative scaling test before declaring the recipe robust.

## Catalog state after iter_036

- ... (16 prior iters)
- **iter_036 3-way merge:**
  - **T3 (asymmetric: destructives zeroed, preservings full)** is
    the clean winner at k=3: boolq 0.66, agnews 0.86, rt 0.85.
  - **Don't zero preserving LoRAs' MLP** — uniform-zero (T2) loses
    19pp on boolq.
  - **Naive merge (T1) is decent** because more preserving mass
    cancels destructive perturbations. Scaling helps, not hurts.
  - **Recipe refined:** audit each LoRA, zero MLP only if destructive,
    sum.

Seventeen iters, ~$0 spend, ~4.5 GPU-hours total. plan.md unchanged.
The continual-learning-by-merge recipe is now a 3-task demonstration.
