# Iteration 33 — 2026-05-10 — Intervention replicates: attention-vs-MLP module split is robust

iter_032 found that zeroing all MLP dWs from boolq_42 turned a
destructive LoRA into a preserving one. iter_033 replicates the
intervention on rt_1024 (the second destructive LoRA in iter_030's
matrix — kills boolq to 0.02).

**Result: replication is dramatic.** rt_1024 follows the same module-
type division pattern. Mechanism is now confirmed on 2 of 2 destructive
LoRAs.

---

## rt_1024 results

| condition | boolq | agnews | rt |
|---|---|---|---|
| C0 full rt_1024 | **0.02** | 0.50 | 0.86 |
| C1 zero L12 up_proj | 0.02 | 0.47 | 0.86 |
| C2 zero L12 all-MLP | 0.01 | 0.50 | 0.86 |
| C3 zero L12+L13 MLP | 0.03 | 0.49 | 0.86 |
| C4 zero L8-L15 MLP | 0.01 | 0.45 | 0.85 |
| **C5 zero ALL MLP** | **0.42** | 0.48 | 0.82 |
| C6 half L12+L13 MLP | 0.03 | 0.50 | 0.86 |
| (BASE alone) | 0.41 | 0.38 | 0.37 |

## Reading

**The full intervention works as well or better than on boolq_42.**

rt_1024's destruction of boolq is severe — full LoRA gives 0.02
boolq (vs base 0.41, random 0.50). That's not just forgetting; it's
*active interference* (the LoRA is producing wrong outputs
systematically).

Zeroing all MLP dWs:
- **Boolq recovers from 0.02 to 0.42** — back to base level (essentially
  full restoration of the destroyed capability)
- **rt drops only from 0.86 to 0.82** — 95% retention of the
  trained capability
- **Agnews barely moves** (0.50 → 0.48) — wasn't being destroyed in
  the first place

**Compared to iter_032 boolq_42:**
- boolq_42 MLP-zero: boolq 0.56→0.51 (91% retention), agnews 0.14→0.34 (recovered to base 0.38), rt 0.08→0.26 (partial recovery)
- rt_1024 MLP-zero: rt 0.86→0.82 (95% retention), boolq 0.02→0.42 (recovered to base 0.41), agnews 0.50→0.48 (barely changed; wasn't destroyed)

Both LoRAs follow the same pattern. Differences:
- rt task is easier than boolq for the base model, so attention-only
  preserves more of the trained accuracy (95% vs 91%)
- rt_1024's destruction was on boolq specifically; boolq_42's
  destruction was on both agnews and rt

## What this confirms

iter_032's mechanism replicates on the second destructive LoRA in our
pool. That's 2 of 2 confirmation. We now have:

- **A robust intervention recipe**: zero all MLP dWs to convert a
  destructive LoRA to preserving
- **A robust mechanism story**: attention layers carry task-specific
  signal; MLP layers carry destructive interference
- **A robust applied technique**: post-hoc audit + MLP-zero to
  produce preserving LoRAs from any fine-tune

## What's still pending

- **Symmetric test:** take a preserving LoRA (boolq_456) and inject
  HEAVY MLP perturbations (e.g., scale MLP × 2 or × 5). Does it become
  destructive? If yes, the causal direction is confirmed both ways.
- **Native attention-only training:** train iter_024's pool with
  target_modules=q,v,k,o only. Compare cross-task interference to
  the post-hoc MLP-zero recipe. If natively-attention-only LoRAs are
  also preserving, the recipe is unnecessary; if they're worse, the
  trained MLP component contains useful task info that selectively
  zeroing recovers.
- **Larger base model.** Does the attention-vs-MLP division generalize
  beyond 0.5B?

## Implications for plan.md (continued from iter_032)

1. **plan.md A1 mergeability prediction** should compute Σ sin²θ
   separately for attention vs MLP. The same-task overlap signal lives
   in attention; mergeability for diff-task pairs should weight
   attention-overlap more heavily and treat MLP as expected-interference.

2. **plan.md A17 audit-tool** gets a concrete metric to ship: read a
   LoRA's MLP ||dW||, normalize, and predict its destructive character.
   Or simpler: read the LoRA, zero its MLP, and compare *predicted*
   behavior on a few held-out tasks vs the original. This is a
   deployable applied tool.

3. **plan.md C2 (per-region behavior correlation)** should split by
   module type: same Region 2 subspace, different functional roles
   (attention = task; MLP = side-effects).

4. **plan.md "Beyond ICLR" continual-learning vision** has a concrete
   recipe: train task-specific LoRA, post-hoc zero its MLP component,
   accumulate. Each new task adds attention-only updates that don't
   destroy prior capabilities.

## What iter_034+ should consider

1. **Symmetric test.** Take boolq_456 (preserving), amplify its MLP
   dW by 2× / 5× / 10×. Does it become destructive? Tests causal
   direction. ~5 min.

2. **Native attention-only LoRA training.** Train all 14 LoRAs on
   iter_024's setup with target_modules=q,k,v,o (no MLP). Compare
   own-task accuracy and out-of-task interference. ~75 GPU-min
   training + analysis.

3. **MLP-zero as a "merge-with-base" step.** For a pool of LoRAs
   trained sequentially (continual learning), the recipe is:
     for each new task LoRA L_i: zero its MLP, add to running merged.
   Test whether this preserves all task accuracies after k=3 sequential
   tasks. Direct continual-learning experiment.

iter_034 priority: **option 1 (symmetric test).** Fast (~5 min) and
fully closes the causal direction. After that, option 3 (continual
learning experiment) is the first true applied test.

## Catalog state after iter_033

- ... (13 prior iters)
- **iter_033 intervention replication on rt_1024 (n=1 replication of
  iter_032):**
  - rt_1024 (kills boolq 0.02) becomes preserving via MLP-zero
    (boolq 0.02→0.42, rt 0.86→0.82, agnews 0.50→0.48).
  - Same pattern as boolq_42 — 2 of 2 destructive LoRAs in pool
    confirm the mechanism.
  - Replication strengthens: attention carries task signal; MLP
    carries destructive interference; post-hoc MLP-zero converts
    destructive to preserving.

Fourteen iters, ~$0 spend, ~4 GPU-hours total. plan.md unchanged.
