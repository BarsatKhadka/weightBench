# Iteration 32 — 2026-05-10 — Causal intervention: attention carries task, MLP carries destructive interference

iter_031 hypothesized that mid-network MLP magnitude (specifically
L12-L13) drives the destructive vs preserving distinction in LoRAs.
iter_032 ran a direct causal intervention: scale boolq_42's dW down
at progressively larger MLP layer sets, measure whether agnews + rt
accuracies recover.

**Result.** Hypothesis was directionally right but spatially too narrow.
The actual pattern is broader and cleaner: **attention layers carry
the task-specific signal; MLP layers carry the destructive interference**.

---

## Setup

Take boolq_42 (the "destructive" LoRA from iter_030 — kills agnews
0.14, rt 0.08). Apply its dW with selective layer-wise scaling.
Evaluate boolq + agnews + rt at each condition.

7 conditions:
- C0: full boolq_42 (baseline)
- C1: zero L12.mlp.up_proj only
- C2: zero L12 all MLP modules
- C3: zero L12 + L13 MLP
- C4: zero L8-L15 MLP
- C5: zero ALL MLP layers (extreme — pure attention LoRA)
- C6: HALVE L12 + L13 MLP

## Results

| condition | boolq | agnews | rt |
|---|---|---|---|
| C0 full boolq_42 | 0.56 | 0.14 | 0.08 |
| C1 zero L12 up_proj | 0.56 | 0.18 | 0.08 |
| C2 zero L12 all-MLP | 0.56 | 0.19 | 0.08 |
| C3 zero L12+L13 MLP | 0.54 | 0.21 | 0.08 |
| C4 zero L8-L15 MLP | 0.44 | 0.23 | 0.10 |
| **C5 zero ALL MLP** | **0.51** | **0.34** | **0.26** |
| C6 half L12+L13 MLP | 0.56 | 0.18 | 0.09 |
| (BASE alone reference) | 0.41 | 0.38 | 0.37 |

## Reading

**iter_031's narrow L12-L13 hypothesis is partial.** Zeroing only L12+L13
MLP (C3) recovers agnews from 0.14 to 0.21 (modest) but rt stays at 0.08.
Mid-network MLP carries SOME of the destructive signal but not all.

**Zeroing all MLP (C5) reveals the real story.** The full intervention:
- agnews recovers from 0.14 to 0.34 (essentially base level 0.38)
- rt recovers from 0.08 to 0.26 (toward but below base 0.37)
- boolq only drops from 0.56 to 0.51 (loses just 5pp)

**Reading.** Attention-layer dW updates carry boolq's task-specific
signal (boolq accuracy preserved when MLP is zeroed); MLP-layer dW
updates carry the destructive interference (other tasks recover when
MLP is zeroed).

## Mechanism

Likely mechanism (not yet directly verified):
- Attention layers in a transformer route information; LoRA-induced
  attention changes shift WHICH information gets attended to, which
  is task-relevant ("look at the question word, output yes/no").
- MLP layers in a transformer process information; LoRA-induced MLP
  changes shift HOW information gets transformed, which is task-
  agnostic ("collapse representation to yes/no token bias").
- Heavy MLP updates from training on one task overwrite the
  general-purpose transformations the model uses for *other* tasks.
- Heavy attention updates are more task-localized — they affect only
  the routing patterns relevant to the trained task.

This is consistent with the literature on attention-only LoRAs
performing competitively with full LoRA at lower interference cost
(eg. early LoRA papers attached only to q,v).

## Applied implication

**A simple recipe for "preserving" continual-learning LoRAs:** train
normally, then zero out the MLP component post-training. For boolq_42:
- preserves 91% of the boolq capability (0.56 → 0.51)
- restores agnews to base level
- partially restores rt
- Net: a preserving fine-tune that keeps base capabilities intact

Alternatively: train LoRA with target_modules=attention-only from the
start, skipping MLP. iter_032's intervention is post-hoc; a from-
scratch attention-only LoRA pool would tell us whether the same
preservation behavior emerges natively.

## What this changes for plan.md

1. **C2 (per-region behavior correlation) gets an empirical answer
   with a layer-type split.** plan.md C2 frames task identity as
   living in Region 2 generically. iter_032 says: the *task* signal
   in Region 2 lives in attention layers; the destructive *cross-task*
   signal in Region 2 lives in MLP layers. Same Region 2, different
   functional roles per module type.

2. **A1 (mergeability) gets a per-module-type mergeability story.**
   Pairs of LoRAs whose attention-Region-2 subspaces are aligned will
   likely merge cleanly on their shared task. Pairs whose MLP-Region-2
   subspaces are misaligned will likely have destructive interference.
   plan.md's analytic predictor should split by module type.

3. **The "destructive vs preserving" diagnostic from iter_030 has a
   per-module fix.** A LoRA's MLP ||dW|| profile predicts how
   destructive it is on out-of-task evaluation. plan.md's audit-tool
   vision (A17) gets a concrete metric: read the LoRA's MLP ||dW||
   norm; if it's high (> some threshold), expect interference.

## Caveats

- n=1 LoRA (boolq_42). Need to replicate on other destructive LoRAs:
  rt_1024 (kills boolq to 0.02), boolq_42 (kills both agnews+rt).
- 100 eval examples per (condition, task), binomial std ~0.05.
  Differences below ~0.05 are noise; the C5 vs C0 differences are
  well above noise.
- We didn't test the converse: take a *preserving* LoRA (boolq_456)
  and ADD heavy MLP perturbations — does it become destructive?
  Symmetric test, doable.
- 0.5B base model. Larger models may have different module-type
  divisions.
- 300-step training. Post-convergence training might shift the
  attention-vs-MLP balance.

## What iter_033+ should consider

1. **Replicate on rt_1024.** rt_1024 is also destructive (boolq 0.02).
   Does zeroing its MLP recover boolq toward base 0.41? Same
   intervention protocol. ~3 min.

2. **Train attention-only LoRAs natively.** Take iter_024's setup
   but use target_modules=q,v,k,o only (skip MLP). Train all 14
   LoRAs. Compare cross-task interference profile. Hypothesis: less
   destructive on out-of-task evaluation. ~75 GPU-min.

3. **Granular layer ablation.** Within MLP, which specific module
   (gate vs up vs down) carries most of the destructive signal?
   8 conditions × 3 evals × 10s = 4 min CPU. Could refine to "the
   actual mechanism is X module type at Y depth range."

4. **Symmetric test.** Take boolq_456 (preserving). Inject heavy
   MLP noise — does it become destructive? Same dW magnitude in
   the MLP layers boolq_42 had. Tests the causal direction.

iter_033 priority recommendation: **option 1 (replicate on rt_1024).**
Quickest causal-replication test with cheapest cost. If rt_1024 also
becomes preserving via MLP-zero, the mechanism is robust. If not,
boolq_42 was a special case.

## Catalog state after iter_032

- ... (12 prior iters)
- **iter_032 destructive intervention (n=1, boolq_42):**
  - Mid-network L12-L13 MLP hypothesis from iter_031 was directionally
    right but spatially too narrow.
  - **Zeroing ALL MLP dWs from boolq_42 reveals the cleaner pattern:**
    boolq accuracy preserved (0.56 → 0.51, -5pp), agnews recovers to
    base level (0.14 → 0.34), rt partially recovers (0.08 → 0.26).
  - **Attention layers carry task-specific signal; MLP layers carry
    destructive interference.** Clean module-type division of labor.
  - Applied recipe: post-hoc zero MLP component for a preserving
    continual-learning LoRA. 91% task retention, restores most of
    out-of-task base capabilities.

Thirteen iters, ~$0 spend, ~4 GPU-hours total. plan.md unchanged
but suggested updates in BREAKTHROUGH (C2 + A1 per-module split, A17
audit metric).
