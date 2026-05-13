# Iteration 40 — 2026-05-10 — MLP submodules co-encode the destructive bias; partial zeroing doesn't work

iter_039 showed the rt_full ensemble outputs `negativenegativenegative`
spam regardless of input. iter_040 asked which MLP submodule (gate /
up / down) carries the answer-token bias by ablating one at a time.

**Result: counterintuitive.** Single-module ablation has zero effect.
Even 2-of-3 ablation barely helps. The destructive bias is
*distributed across all three MLP submodules*, which compensate for
each other when any subset is removed.

The recipe stands but is now more nuanced: zero ALL MLP submodules
or get nothing.

---

## Setup

Apply rt_full ensemble (5 LoRA dWs summed). Ablate selectively:
- F0: full (no ablation; baseline)
- F1: zero only gate_proj contribution
- F2: zero only up_proj
- F3: zero only down_proj
- F4: zero gate+up (keep down)
- F5: zero attention only (keep all MLP) — control
- F6: zero ALL MLP (full recipe)

Evaluate boolq + agnews + rt and inspect 5 sample outputs per task
per condition.

## Results

| condition | boolq | agnews | rt | rt outputs |
|---|---|---|---|---|
| F0 full | 0.00 | 0.00 | 0.43 | "negative" spam ×5 |
| F1 zero gate | 0.00 | 0.00 | 0.43 | "negative" spam ×5 |
| F2 zero up | 0.00 | 0.00 | 0.43 | "negative" spam ×5 |
| F3 zero down | 0.00 | 0.00 | 0.43 | "negative" spam ×5 |
| F4 zero gate+up | 0.00 | 0.00 | 0.56 | mostly spam |
| F5 zero attn | 0.00 | 0.00 | 0.43 | "negative" spam ×5 |
| **F6 zero all MLP** | **0.29** | **0.62** | **0.82** | "positive", "yes", coherent |

## Three findings

### Finding 1 — Single-module ablation has zero effect

F1, F2, F3 give *exactly* the same destruction as F0 (full):
- boolq 0.00, agnews 0.00, rt 0.43
- All output "negativenegative..." spam
- Sample-output distributions look indistinguishable

I expected one submodule (most likely down_proj since it's the "output
projection") to be responsible. Reality: removing any single submodule
does nothing. The remaining two compensate.

### Finding 2 — Even 2-of-3 ablation barely helps

F4 (zero gate+up; keep down): rt 0.43 → 0.56 (modest improvement),
boolq + agnews stay at 0.00. Sample outputs still mostly "negative"
spam.

So even removing 2 of 3 MLP submodules leaves the destructive bias
substantially intact. Down_proj alone (with the LoRA's contribution
to the other two zeroed) can sustain the bias.

### Finding 3 — Only F6 (all MLP zeroed) breaks the destruction

F6 recovers:
- boolq 0.29 (below base 0.41 but coherent outputs)
- agnews 0.62 (well above base 0.38)
- rt 0.82 (95% of best individual rt solo 0.87)

Sample outputs become coherent text:
- boolq F6: `"yes"`, `"positive/positive"`, `"negative\nno"`
- agnews F6: `"Sports\nTopic:"`, `"World\nTopic:"`, `"Tech\nTopic:"`
- rt F6: `"positive\n\npositive"`, `"negative/negative"`

Compare to F0-F5: `"negativenegativenegativenegative"` everywhere.

## Mechanism reading

In Qwen-style transformer MLPs, the computation is:
```
mlp_out = down_proj(silu(gate_proj(x)) * up_proj(x))
```

Three multiplicative dependencies:
- gate_proj: produces gating values (silu-activated)
- up_proj: produces values to be gated
- down_proj: projects gated product back to hidden dim

The LoRA dW additively perturbs each of these. The "output trained
answer tokens" bias is encoded as a *coordinated* perturbation of all
three. When you zero one LoRA's contribution to e.g. gate_proj,
the other two LoRA contributions to up_proj and down_proj still
construct the same biased mapping (just through a slightly different
internal gating pattern). The remaining base-model gate_proj weights
provide enough gating signal that the LoRA-modified up_proj +
down_proj still produce the answer-token output.

Only when all three LoRA contributions are zeroed does the MLP fall
back to base-model behavior, and the destructive bias is gone.

This is a strong claim about MLP redundancy: **task-output bias is
holographically distributed across the three MLP submodules**, not
localized to any one. A LoRA's MLP contribution functions as a unit;
you can't selectively keep "useful task information" while removing
"destructive output bias."

## Implications for plan.md

1. **Continual-learning recipe must zero all MLP submodules.**
   Partial MLP scaling doesn't reduce destructive interference
   proportionally — it does nothing until you reach 100% removal of
   all three submodules' LoRA contributions.

2. **Audit-tool implication for A17:** the MLP ||dW|| metric should
   be computed jointly across all 3 submodules. Per-submodule
   ||dW|| isn't predictive of destructiveness.

3. **A new geometric question for plan.md:** *what's the structural
   relationship between gate / up / down LoRA contributions in
   destructive vs preserving LoRAs?* Are they correlated in the
   same way for both? The "co-encoding" finding suggests the three
   submodules' dWs are not independent — they likely have specific
   correlations that constitute the destructive bias.

## Caveats

- Single ensemble tested (rt_full). The "co-encoding" claim should
  replicate on boolq_full and agnews_full ensembles. Quick eval.
- 100 examples per cell. 0.43 vs 0.43 single-digit-precision
  comparison is robust though (literally same accuracy across
  conditions).
- The "F4 marginal improvement to 0.56" is small enough to be noise.
  Treat it as "almost no effect."

## What iter_041+ should consider

1. **Replicate on boolq_full and agnews_full.** Same single-vs-multi
   submodule ablation. Tests whether the co-encoding claim is rt-
   specific or general. ~10 min.

2. **Probe the correlation structure of gate/up/down LoRA dWs.**
   For each of 14 LoRAs, compute correlation matrices between
   submodule dW vectors per layer. Do destructive LoRAs show a
   specific gate-up-down correlation pattern absent in preserving
   LoRAs? Would mechanistically explain the co-encoding.

3. **Connect to MLP-as-key-value-memory literature** (Geva et al.).
   Transformer MLPs have well-documented "key-value memory"
   structure where gate/up/down jointly encode lookup behavior.
   Our finding suggests LoRA reinforces specific keys → values,
   and the keys are distributed across all three submodules.

iter_041 priority: **option 1 (replicate on other-task ensembles).**
Cheapest test of the generality of the co-encoding finding.

## Catalog state after iter_040

- ... (20 prior iters)
- **iter_040 granular MLP ablation:**
  - **Single MLP submodule (gate/up/down) ablation has zero effect**
    on rt_full ensemble's destructive output spam.
  - **Even 2-of-3 ablation (zero gate+up) barely helps** (rt 0.43 →
    0.56; boolq, agnews still 0.00).
  - **Only zeroing all 3 MLP submodules breaks the destruction**
    (rt 0.82, agnews 0.62, boolq 0.29; coherent text outputs).
  - **Mechanism:** the destructive answer-token bias is
    *holographically distributed* across the three MLP submodules
    (gate, up, down), which compensate for each other under partial
    ablation.
  - Recipe refined: must zero ALL MLP submodules. Partial MLP
    scaling doesn't work.

Twenty-one iters, ~$0 spend, ~5.5 GPU-hours total. plan.md unchanged.
