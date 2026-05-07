# Synthesis 20: Arrhenius Grokking Time = Rank Collapse Barrier

**Date:** 2026-05-07
**Session:** 5
**Previous synthesis:** synthesis_night_run_19_trs_spectrum_sufficient_statistic.md

---

## The Arrhenius Hypothesis (SLT Grokking Paper)

The SLT grokking paper (grokking_slt_competing_basins.pdf) proposes an Arrhenius mechanism
for grokking timing:

    t_grokking ~ exp(ΔF / T)

where ΔF = free energy barrier between memorization basin and generalization basin,
and T = "temperature" (effective noise level = f(learning rate, weight decay, batch size)).

The Arrhenius form means: the delay before grokking is EXPONENTIAL in the free energy barrier.
Small barriers → fast grokking. Large barriers → slow grokking (or no grokking).

---

## What Is the Free Energy Barrier in LoRA?

In SLT, the free energy F = RLCT × log(n) + corrections. The barrier:

    ΔF = F_mem - F_gen = (RLCT_mem - RLCT_gen) × log(n)

From synthesis 14:
    RLCT_mem = r(m + n_param - r) / 2         [memorization basin, rank r]
    RLCT_gen = d_task(m + n_param - d_task) / 2  [generalization basin, rank d_task]

So:
    ΔF = [r(m + n_param - r) - d_task(m + n_param - d_task)] × log(n) / 2

For the typical regime r >> d_task and m, n_param >> r:
    ΔF ≈ (r - d_task) × (m + n_param) × log(n) / 2

**The grokking barrier is linear in (r - d_task) = the excess rank = number of intruder dims.**

Grokking time prediction:
    t_grokking ~ exp(c × (r - d_task) × log(n))

where c ~ (m + n_param) / 2T (m, n_param = layer dimensions, n = training examples, T = noise).

---

## Four Predictions from This Formula

**P1: More excess rank → exponentially slower grokking.**
    Using rank r = 16 when d_task = 4: exponentially slower than using rank r = 4.
    The current practice of using large fixed rank (r=64, r=128) massively slows grokking.

**P2: Higher learning rate → faster grokking.**
    T = f(learning_rate × weight_decay) increases with learning_rate.
    Consistent with empirical observation that higher LR speeds grokking.

**P3: More training data → faster grokking.**
    More n → larger log(n) → larger ΔF. But T also scales with n through batch size.
    Net effect: if batch size scales with n, T ~ n and the ratio ΔF/T = c(r-d_task) is constant.
    Grokking speed is batch-size dependent, not just data-size dependent.

**P4: Weight decay is the "temperature" for grokking.**
    Weight decay on LoRA = nuclear norm penalty = drives toward low-rank solutions (synthesis 9).
    Higher weight decay → higher T (more thermal noise) → faster escape to generalization basin.
    This is consistent with: grokking requires weight decay (empirical fact from Power et al.).

---

## Connection to AlphaLoRA and HTSR Training Phases

The Arrhenius formula predicts that with rank r = d_task (GELoRA optimal):
    ΔF = 0 → t_grokking = O(1)  [no barrier, immediate generalization]

With rank r >> d_task (standard large-rank LoRA):
    ΔF >> 0 → t_grokking = exp(c(r-d_task)) [exponential delay]

This means: **optimal LoRA rank (GELoRA's d_task) = zero grokking barrier = fast convergence.**

AlphaLoRA allocates rank by HTSR alpha: layers with alpha < 2 already need less rank
(they've done their grokking and are well-calibrated). Layers with alpha > 4 need more rank.

The AlphaLoRA rank prescription = choosing r ≈ d_task layer-by-layer = minimizing ΔF per layer.
This explains WHY AlphaLoRA converges faster: it removes the grokking barrier by using the
correct rank from the start.

---

## The Temperature T

In SGD-based training of LoRA:
    T = η × σ²(grad)  (roughly: learning rate × gradient variance)
    σ²(grad) ∝ 1/batch_size for SGD; ∝ weight_decay for Adam with weight decay

With Adam + weight decay λ:
    T ≈ η × λ  (the temperature is primarily controlled by η × λ)

The Grokking Severity Measure (GSM from the SLT paper) = negatively correlated with learning rate.
This is consistent: higher LR → higher T → lower ΔF/T → lower GSM (faster grokking).

The Arrhenius formula also explains the dimensionless grokking timing from the SLT paper:
    grokking_time ∝ exp(ΔF/T) = exp(c(r-d_task)/ηλ)

---

## A Unified Picture of Grokking in LoRA

**Grokking = rank reduction from r to d_task, activated by weight decay (temperature).**

The GL(r) gauge group creates a singularity (synthesis 14) with competing basins at different
RLCT values. The Arrhenius formula (from SLT) gives the TIMING of the escape from the high-RLCT
memorization basin to the low-RLCT generalization basin.

The free energy barrier = (r - d_task) × something: proportional to the number of EXCESS
rank directions = the intruder dim count.

**Every intruder dim contributes equally to the grokking barrier.** One way to read this:
intruder dims are not just bad for forgetting — they SLOW DOWN generalization by adding
an exponential barrier to the grokking transition.

---

## Connection to "From Spikes to Heavy Tails" Phase Sequence

The 5+1 training phases map to the Arrhenius escape:
- Phases 1-3 (Random → Bleeding-Out → Bulk+Spike): thermal fluctuations in the memorization basin
- Phase 4 (Bulk-Decay): approaching the barrier (SV structure consolidating)
- Phases 5-6 (Heavy-Tailed → Rank Collapse): tunneling through the barrier → generalization basin
  This is the Arrhenius escape: the rank collapse is the "reaction" and Phases 5-6 are the transition state

**The "transition state" of grokking = the Heavy-Tailed phase (alpha ≈ 2).**
The network spends exponential time in the memorization basin (Phases 1-4), then passes through
the transition state (Phase 5, critical alpha ≈ 2), then rapidly reaches generalization (Phase 6).
