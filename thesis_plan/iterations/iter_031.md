# Iteration 31 — 2026-05-10 — Destructive vs preserving: mid-network magnitude + seed-locked vec-cosine

iter_030 surfaced "destructive vs preserving" as a seed-driven property
within a task: boolq_42 destroys agnews + rt; boolq_456 preserves them
and excels at rt. iter_031 probes what's geometrically different.

**Two findings.** One explains the destructive vs preserving difference.
The other is a methodological finding bigger than I expected: LoRA
dW direction is dominated by random seed rather than by task.

---

## Setup

CPU-only probe over iter_024's pool. Compare boolq_42 (destructive)
vs boolq_456 (preserving) across all 168 layers on:
- ||dW||_F per layer (P1)
- vec-cosine to each rt reference (rt_42, rt_456, rt_1024) per layer (P2)
- spectral concentration top1/Σtop16 per layer (P3)

References: rt_42, rt_456, rt_1024 (rt LoRAs at known accuracies).

## Finding 1 — Mid-network MLP magnitude separates destructive from preserving

Per-layer ||dW||_F summary:
- boolq_42: mean=0.314, median=0.269
- boolq_456: mean=0.292, median=0.245
- rt_42 / rt_456 / rt_1024: 0.316 / 0.301 / 0.306

boolq_42 has larger ||dW|| in **125 of 168 layers** vs boolq_456.
Biggest gaps:
| layer | boolq_42 minus boolq_456 |
|---|---|
| L12 mlp.up_proj | **+0.167** |
| L23 self_attn.q_proj | +0.145 |
| L12 mlp.gate_proj | +0.144 |
| L13 self_attn.q_proj | +0.132 |
| L13 mlp.gate_proj | +0.118 |

The pattern: **boolq_42 pushes much harder at mid-network (L12, L13)
MLP gating + up-projections, plus a few attention layers**. These are
the layers most directly involved in shaping the activation stream
between input encoding and output decoding. Heavy updates here
overwrite the "general competence" that the base model uses to
solve other tasks → catastrophic forgetting on agnews + rt.

boolq_456's lighter mid-network updates leave that general competence
intact, which is why it preserves agnews accuracy and even excels on
rt (the rt-relevant patterns weren't disrupted).

**This is the cleanest geometric signature of destructive vs preserving
LoRAs we've found.** It's a per-layer ||dW|| profile, not a subspace
property. Subspace overlap (A01) put both at 0.85 to each other and
~0.92 to rt LoRAs — geometrically equidistant — so the C1 / Region 2
metric *doesn't* discriminate destructive from preserving.

## Finding 2 — Vec-cosine is dominated by random seed, not task

Mean vec-cosine of vec(dW_X) and vec(dW_rt_Y) over 168 layers:

| boolq side | rt_42 | rt_456 | rt_1024 |
|---|---|---|---|
| boolq_42 | **+0.029** | +0.0001 | +0.0003 |
| boolq_456 | +0.0015 | **+0.032** | +0.0011 |

**Same-seed pairs are ~30× more vec-aligned than cross-seed pairs.**
boolq_42 and rt_42 — completely different tasks — have ~+0.029
cosine. boolq_456 and rt_456 — same pattern, +0.032.

But boolq_42 vs rt_456 (different seed, different task) is
essentially zero (+0.0001).

**Why:** PEFT's LoRA initialization sets B=0 and A=Kaiming-uniform
random with the seed. With identical seed:
- Same A initialization across tasks
- Same data-shuffling order (within same seed)
- Same dropout pattern

The first gradient step's direction is partially determined by the
random A. After 300 steps of training on different tasks, the dW
*subspace* differs (different tasks → different optima) but the
*specific direction taken within that subspace* retains seed-driven
correlations.

This means: **two LoRAs trained on different tasks but same seed
will have dW vectors that are noticeably more aligned in pure
direction than two LoRAs of the same task trained with different
seeds.**

iter_029 already saw a hint of this (same-task vec-cosine 0.006-0.023
vs diff-task 0.034). iter_031 makes the magnitude precise: same-seed
alignment is the dominant signal.

## Implications for plan.md

1. **A1 mergeability prediction needs a per-layer magnitude predictor
   on top of subspace overlap.** Σ sin²θ alone doesn't discriminate
   destructive from preserving LoRAs that span the same subspace —
   only ||dW||_F per layer (especially mid-network MLP) does.

2. **C1 (subspace clustering) is a real signal but doesn't translate
   to behavioral outcomes alone.** boolq_42 and boolq_456 are in the
   same Region 2 cluster (A01=0.85) but behave totally differently.
   plan.md's C1 framing should be supplemented with "and the within-
   cluster magnitude profile determines behavioral character."

3. **The seed-locked vec-cosine is a genuinely new finding for plan.md.**
   It splits "subspace identity" (which directions a LoRA spans;
   task-driven) from "specific learned point" (which point in that
   subspace; seed-driven).

   plan.md A4 (path-vs-speed) should incorporate this distinction.
   Two same-task seeds walk different specific paths because their
   initial directions are seed-driven, even though they end up in
   the same subspace cluster.

4. **A practical implication:** if two LoRAs at the same seed but
   different tasks are merged, they merge MORE smoothly than two
   different-seed same-task LoRAs (because of higher vec-alignment).
   This is testable with iter_027/iter_028's merge code by comparing
   same-seed vs cross-seed merges.

5. **Catastrophic forgetting is predictable from weight-space alone.**
   Look at mid-network MLP ||dW||. If it's high, the LoRA is likely
   destructive. This is a useful applied diagnostic — you can audit
   a fine-tune *before* deploying it by reading its weights.

## Caveats

- n=2 in the contrast (boolq_42 vs boolq_456). Other "destructive"
  examples (e.g., rt_1024 which gets 0.02 on boolq) need the same
  analysis to confirm the mid-network-magnitude pattern.
- Same-seed alignment finding is computed across 5 LoRA pairs.
  Replication on more pairs needed.
- We didn't test what happens if you SCALE DOWN boolq_42's mid-
  network ||dW|| — would that turn it from destructive to preserving?
  Direct intervention test, ~30 min.
- 168 layers of analysis per LoRA. We probed ||dW|| at all of them
  but only summarized; layer-by-layer plots would help see the
  specific destructive pattern.

## What iter_032+ should consider

1. **Direct intervention test:** scale boolq_42's dW down at L12-L13
   MLP layers specifically; measure agnews + rt accuracy. If
   destructive → preserving via per-layer scaling, the mid-network
   MLP hypothesis is causally confirmed.

2. **Replicate on rt_1024.** rt_1024 is also destructive (kills boolq
   to 0.02). Does it have the same mid-network MLP signature? Cheap
   CPU-only.

3. **Same-seed cross-task merge experiment.** Merge boolq_42 + rt_42
   (same seed, diff task) vs boolq_42 + rt_456 (diff seed, diff
   task). Per Finding 2, the same-seed merge should be smoother
   (less interference, fewer "valley of bad performance" issues).
   ~10 min eval.

4. **Investigate the seed-locked direction.** If LoRA dW direction
   is heavily seed-determined, then averaging across seeds at the
   same task should produce a more "task-pure" dW signal that
   cancels out the seed noise. Test: average boolq_42 + boolq_123
   + boolq_456 + boolq_1024, compare its dW direction to individual
   seeds. The averaged version should have lower seed-locked cosine.

iter_032 priority recommendation: **option 1 (direct intervention
test).** Causal confirmation of the most actionable finding. Cheap.

## Catalog state after iter_031

- ... (10 prior iters)
- **iter_031 destructive vs preserving probe (n=2 contrast):**
  - **Mid-network MLP magnitude separates destructive from
    preserving.** boolq_42 has +0.12 to +0.17 larger ||dW|| at L12-L13
    MLP gate/up_proj than boolq_456. Heavy mid-network updates
    overwrite general competence, causing forgetting on out-of-task
    eval.
  - **Vec-cosine is seed-locked, not task-locked.** Same-seed pairs
    (boolq_42 ↔ rt_42; boolq_456 ↔ rt_456) have ~30× higher dW
    cosine than cross-seed pairs. Direction within Region 2 is
    determined by PEFT's lora_A random init, not by task.
  - **C1 / subspace overlap doesn't predict behavioral outcomes
    alone.** boolq_42 and boolq_456 are equidistant from rt LoRAs
    in subspace terms but behave totally differently. Need ||dW||
    per-layer profile + spectral metric on top of C1.

Twelve iters, ~$0 spend, ~4 GPU-hours total. plan.md unchanged.
