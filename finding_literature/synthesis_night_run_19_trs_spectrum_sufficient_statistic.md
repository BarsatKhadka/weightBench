# Synthesis 19: The TRS Spectrum as Complete Sufficient Statistic

**Date:** 2026-05-07
**Session:** 5
**Previous synthesis:** synthesis_night_run_18_model_tree_fiber_bundle_base_manifold.md

---

## The Central Claim

The TRS spectrum of a LoRA adapter {σ₁ ≥ σ₂ ≥ ... ≥ σ_r; their singular vectors} is a
**sufficient statistic** for the fine-tuning process. It encodes:

1. **Task identity:** Which directions are above-MP (the "task fingerprint" via GradientSpace, W2T)
2. **Dataset size:** How many directions are above-MP, and how stable they are (DSiRe, 2406.19395)
3. **Training progress:** The HTSR alpha phase of each above-MP direction (synthesis 15)
4. **Merge compatibility:** The subspace overlap between different adapters' Region 2 (synthesis 16)
5. **Forgetting risk:** The overlap between above-MP directions and W₀'s large SV directions (synthesis 17)

Nothing about the fine-tuning is hidden from the TRS spectrum.

---

## Reading the TRS Spectrum as a Timeline

The TRS spectrum reveals the HISTORY of training:

**Stage 1 (early training, few above-MP):**
- Only 1-3 directions above MP threshold
- HTSR alpha of these directions: alpha >> 4 (barely differentiated from noise)
- LLC: high (memorization basin, many intruder dims)
- DSiRe interpretation: dataset_size < N_threshold (not enough data to consolidate more directions)

**Stage 2 (mid training, growing above-MP count):**
- Growing number of above-MP directions (approaching d_task)
- HTSR alpha: transitioning from > 4 toward 2 (consolidating)
- LLC: decreasing (moving toward generalization basin)
- DSiRe interpretation: dataset_size in growth regime

**Stage 3 (optimal = grokking point):**
- Exactly d_task directions above-MP (rank collapse, synthesis 13 and 15)
- HTSR alpha ≈ 2 for all above-MP directions (optimal spectral state)
- LLC: at minimum (generalization basin reached)
- DSiRe interpretation: dataset_size = N_saturate (enough data for d_task directions)
- This is the CORRECT FINE-TUNING ENDPOINT: stop here

**Stage 4 (over-training, anti-grokking):**
- Still d_task + 0 directions above-MP (rank is stable), but HTSR alpha < 2 for some
- These over-trained directions = emerging intruder dims or distorted TRS
- LLC: increasing again (anti-grokking = second phase transition)
- DSiRe interpretation: dataset has been used too many times (overfitting regime)

---

## The Data Sufficiency Criterion (from DSiRe + GELoRA)

DSiRe (2406.19395): spectrum encodes dataset size. GELoRA: rank ≥ d_task is required.

Combined: **fine-tuning is data-sufficient when rank(TRS) ≥ d_task.**

Practical test: compare the measured TRS rank (number of above-MP SVs) to GELoRA's d_task estimate.
- rank(TRS) < d_task: NOT enough data or training (add more data, train longer)
- rank(TRS) = d_task: optimal (good fine-tuning, stop here)
- rank(TRS) > d_task: excess rank = intruder dims present (r > d_task)

This gives a PURELY SPECTRAL stopping criterion that requires no held-out data:
    Stop training when rank(TRS) = d_task AND HTSR alpha ≈ 2 for all above-MP directions.

---

## Why Four Systems All Predict Task Capabilities

W2T (predicts task capabilities from LoRA weights), GradientSpace (discovers task structure
from gradients), D2C clustering (clusters adapters by SVD features), and DSiRe (recovers
dataset size from spectrum) all work because:

**The TRS spectrum is a lossless representation of the task fine-tuning.**

All the information that distinguishes one LoRA from another is in its spectrum, because:
1. The GL(r) gauge symmetry is removed by SVD (synthesis 14) — different (A, B) pairs giving
   the same ΔW collapse to the same spectrum
2. The noise is separated from signal by the MP threshold
3. The signal directions encode task identity and training depth

**No information is lost when you map (A, B) → SVD(BA) = TRS spectrum.**

This is why W2T can predict task capabilities without knowing anything about the task:
the rank-level transformer is reading the TRS spectrum and inferring what it encodes.

---

## The Wavelet Perspective (SeLoRA)

SeLoRA (lora_parameter_redundancy_spectral_encoding.pdf) uses wavelet encoding for LoRA
spectral re-parameterization. This is a MULTI-SCALE analysis of the TRS spectrum:

- Wavelet coarse scale = Region 1 (low-frequency = universal fiber, large SVs)
- Wavelet fine scale = Region 2 (high-frequency = task-specific, moderate SVs)
- Wavelet noise scale = Region 3 (very high-frequency = below-MP noise)

The wavelet encoding is an alternative to the three-region hard decomposition: instead of
binning into three discrete regions, it provides a smooth multi-scale decomposition that
naturally captures the hierarchical structure of the TRS spectrum.

**SeLoRA's wavelet re-parameterization = a soft version of the three-region TRS decomposition.**
It implements the same physics (universal/task-specific/noise hierarchy) with a continuous
rather than discrete spectral decomposition.

---

## The Complete Reading of a LoRA Adapter

Given any LoRA adapter (A, B), compute ΔW = BA, then SVD:

**Region 1 (top-20% SVs, high inter-task alignment):**
    → These directions are what ALL fine-tunings share (universal fiber)
    → Changing these risks forgetting in other tasks
    → Not the task's unique signature

**Region 2 (above-MP, not top-20%, W₀-orthogonal):**
    → These are the GENUINE TRS: the task's unique spectral signature
    → Count of these = d_task (intrinsic rank of the task)
    → Their alignment with each other (across adapters) = merge compatibility
    → Their magnitude = training completeness (HTSR alpha)

**Region 2' (above-MP, not top-20%, W₀-aligned):**
    → These are INTRUDER DIMS: the rank excess (r - d_task)
    → Cause forgetting, reduce merge quality
    → Can be removed post-hoc (OSRM, PAVE) or prevented (EBLoRA, OPLoRA)

**Region 3 (below-MP):**
    → Pure noise (MP bulk)
    → Not task signal, not shared structure

**HTSR alpha of each above-MP direction:**
    → alpha > 4: undertrained direction (needs more data/training)
    → alpha ≈ 2: optimal direction (ready)
    → alpha < 2: overtrained direction (should have stopped earlier)

**Count of directions with alpha ≈ 2 in Region 2:** = number of "complete" TRS directions
    → Equals d_task when training is optimal
    → This is the data sufficiency indicator (DSiRe)

---

## The Simplest Summary

A LoRA adapter is a point in weight space W/G (the fiber bundle quotient).
Its TRS spectrum is the canonical coordinate of this point.
d_task is the essential rank of this point.
alpha ≈ 2 per direction is the quality certificate.
Everything else follows.
