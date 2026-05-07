# Synthesis 15: One Number — Four Frameworks Measuring the Same Invariant

**Date:** 2026-05-07
**Session:** 5
**Previous synthesis:** synthesis_night_run_14_slt_gauge_singularity_grokking_lora.md

---

## The Core Observation

Four independent frameworks give prescriptions for LoRA rank. They are measuring the same invariant.

| Framework | Rank Prescription | What It Measures |
|-----------|-------------------|------------------|
| GELoRA (2412.09250) | r_i = max(d_{i+1}-d_i, 0) + 1 | Change in intrinsic dim of data manifold |
| AlphaLoRA (alphalore_htsr_rank_allocation.pdf) | r_i ∝ alpha_i (PL_Alpha_Hill) | HTSR power-law exponent of weight matrix |
| TRS (this project) | r_i = #{above-MP, W₀-aligned-orth SVs} | Genuine TRS direction count |
| SLT RLCT (synthesis 14) | 2×RLCT/n ≈ LLC ∝ d_task(m+n-d_task)/n | Bayesian effective complexity |

**All four converge on the same quantity: d_task = the intrinsic dimension of the task.**

---

## Why They Must Agree

GELoRA's intrinsic dimension = the number of independent directions the data manifold expands
across a transformer layer = the number of independent "new signals" the network must represent.

TRS genuine count = the number of above-MP, W₀-non-redundant singular vectors of ΔW = the
number of new directions the fine-tuning adds to the pretrained representation.

SLT RLCT = the effective number of non-redundant parameters in the gauge-fixed LoRA quotient =
the rank of the manifold of functions achievable by rank-r LoRA.

HTSR alpha = the power-law exponent of the weight matrix ESD. At alpha ≈ 2, the layer has
the optimal balance of signal (above-MP spikes) and noise (MP bulk) — exactly the TRS signal
count that matches the intrinsic dimension.

**These four quantities are equal when the LoRA rank is calibrated to the task.**

---

## The Training Phases Map to TRS Development

The "From Spikes to Heavy Tails" paper (from_spikes_to_heavy_tails_spectral_evolution.pdf)
gives the temporal trajectory of how HTSR alpha changes during training:

**Phase 1: Random** — ESD = pure MP bulk, alpha undefined (no signal)
**Phase 2: Bleeding-Out** — first eigenvalues separate from bulk edge
**Phase 3: Bulk+Spike** — FIRST GENUINE TRS DIRECTION EMERGES (above-MP spike = Region 2 onset)
**Phase 4: Bulk-Decay** — spikes grow, MP bulk shrinks (signal-to-noise improves)
**Phase 5: Heavy-Tailed** — alpha approaches 2 (power-law tail develops, optimal generalization)
**Phase 6: Rank Collapse** — rank drops sharply (= GROKKING TRANSITION in spectral terms)

At Phase 5, the HTSR alpha ≈ 2. This is the same as:
- The BBP phase transition boundary (alpha = 2 = "bulk edge" exponent for Wigner matrices)
- The point where the number of genuine TRS directions ≈ d_task
- The GELoRA optimal rank being achieved

Phase 6 (Rank Collapse) = the network has converged to the minimum-rank solution = GELoRA's
d_task = SLT's RLCT generalization basin = genuine TRS only.

**The grokking transition = the entry into Phase 5 (alpha → 2) followed by Phase 6 (rank collapse).**

The grokking dimensional phase transition paper (D crosses 1) corresponds to:
- Phase 3→4 transition: the first genuine TRS direction (D crosses 1 = one signal dimension appears)
- The "super-diffusive" gradient regime (D > 1) = Phase 4/5 = TRS consolidation
- The final rank collapse (Phase 6) = the HTSR alpha drops below 2 again (anti-grokking) — OR
  stays at 2 if training stops at the right moment (optimal stopping = GELoRA's criterion)

---

## AlphaLoRA vs GELoRA: A Consistency Test

AlphaLoRA allocates rank proportional to alpha_i:
- High alpha (alpha > 4): layer hasn't converged yet → needs more rank
- Optimal alpha (alpha ≈ 2): layer is well-regularized → optimal rank achieved
- Low alpha (alpha < 2): layer is over-parameterized → reduce rank

GELoRA allocates rank proportional to d_{i+1} - d_i:
- Expanding layers (d_{i+1} > d_i): need extra rank to represent the expansion
- Contracting layers (d_{i+1} < d_i): can use rank 1
- Flat layers (d_{i+1} ≈ d_i): can use minimum rank

**These two prescriptions are measuring the same thing from different perspectives:**

AlphaLoRA measures: "has this layer's weight matrix converged to the signal-optimal alpha?"
GELoRA measures: "how many new signal directions does this layer need to represent?"

If the AlphaLoRA and GELoRA rank prescriptions are consistent:
- High alpha layers = intrinsic dimension expanding layers (both want high rank)
- Optimal alpha layers = intrinsic dimension stable layers (both want low rank)
- Low alpha layers = intrinsic dimension contracting layers (both want rank 1)

**Testable prediction:** For a well-trained LoRA model, the per-layer HTSR alpha_i should be
anti-correlated with the per-layer GELoRA rank bound (d_{i+1} - d_i). Layers that need high
rank (per GELoRA) should have high alpha (per AlphaLoRA) before training and alpha ≈ 2 after.

This is a direct cross-validation of two independent rank-allocation theories that have
never been connected in the literature.

---

## The Spectral Life Cycle of a Single Genuine TRS Direction

Tracing one genuine TRS direction through the training phases:

**Phase 1-2:** The direction doesn't exist yet. ΔW ≈ 0 (zero initialization of B).
**Phase 3 (Bulk+Spike):** The direction first emerges as a spike above MP bulk.
    - Singular value σ₁ just above MP threshold = BBP critical point
    - This is the genuine TRS direction "being born"
    - GELoRA would say: one unit of intrinsic dimension has been "discovered"
    - SLT would say: LLC drops by d_task(m+n-d_task)/n (one genuine direction added)
**Phase 4 (Bulk-Decay):** The direction consolidates. σ₁ grows, bulk shrinks.
    - HTSR alpha evolves toward 2 (this direction is becoming "signal")
**Phase 5 (Heavy-Tailed):** The direction is fully formed. sigma₁ >> sigma_MP.
    - alpha ≈ 2 = optimal for this direction
    - This is where HTSR says "good generalization"
**Phase 6 (Rank Collapse):** The direction stabilizes. Intruder dims that co-existed decay.
    - Remaining genuine TRS directions = d_task (intrinsic rank achieved)

For LoRA specifically: Phase 6 (Rank Collapse) is GROKKING. The B matrix's dominant singular
vectors converge from r random-ish directions to d_task genuine-TRS directions. The GL(r)
symmetry is spontaneously "broken" in the sense that the orbit now has a preferred canonical
form (the genuine TRS basis).

---

## The Simplest Possible Statement

**Everything in LoRA fine-tuning is about finding d_task.**

- d_task is the intrinsic dimension of the fine-tuning task (GELoRA's measure)
- It equals the number of genuine TRS directions (TRS measure)
- It equals the HTSR-optimal layer at alpha ≈ 2 (spectral measure)
- It equals the SLT generalization basin's RLCT/something (Bayesian measure)
- Finding d_task = grokking (the transition from trying all r directions to using d_task)
- Rank > d_task = intruder dims (the excess)
- Rank = d_task = optimal LoRA (zero forgetting, maximum task signal)
- Rank < d_task = underfitting (insufficient task signal)

The fiber bundle framework provides the geometric interpretation:
d_task = dim(horizontal subbundle / task direction) = dim(Region 2) per layer.

---

## What Remains Open

1. **Exact formula connecting alpha to d_task.** We know alpha ≈ 2 is optimal and GELoRA's
   d_task is the optimal rank. But is there a formula alpha = f(d_task, n, m)?

2. **Training dynamics of the LLC.** SLT predicts LLC drops at grokking. AlphaLoRA predicts
   alpha transitions. From Spikes predicts rank collapse. Do these happen simultaneously?
   A combined experiment tracking all three metrics during LoRA training would resolve this.

3. **Cross-layer consistency.** If GELoRA and AlphaLoRA agree per-layer, the consistency test
   (see above) is satisfied. But do they agree on the SAME layers? This has never been tested.
