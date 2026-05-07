# Synthesis 18: The Model Tree IS the Fiber Bundle Base Manifold

**Date:** 2026-05-07
**Session:** 5
**Previous synthesis:** synthesis_night_run_17_small_sv_w0_fine_tuning_target.md

---

## The Geometric Identification

The MoTHer paper (origin_of_llamas_model_tree_heritage.pdf) recovers the "model tree" — a
rooted tree of models where:
- Root = foundation model (LLaMA, etc.)
- Edges = fine-tuning operations (child is fine-tuned from parent)
- Leaves = specialized fine-tuned models

This is **exactly the base manifold B of the fiber bundle W → W/G.**

**Model Tree = Base Manifold B = the quotient space W/G = the space of model functions**

Each node in the model tree is a point in the quotient manifold — a distinct model FUNCTION
(not a specific set of parameters). The fine-tuning operations are GEODESICS on this manifold
connecting parent function to child function.

---

## Distances on the Model Manifold

MoTHer uses "LoRA Weight Distance: max_l rank(u_l - v_l) via SVD" as its distance metric.

This computes: for each layer l, find the maximum rank of the difference between the LoRA
updates u_l (model 1) and v_l (model 2). The maximum over layers = the "most different" layer.

In fiber bundle terms: u_l - v_l is the difference between two tangent vectors at different
points on the base manifold. The rank of this difference = the number of independent directions
in which the two models differ = the dimension of the "separation" between the two base points.

**This is an approximation of the Riemannian distance on the quotient manifold W/G.**

More precisely: the Fréchet distance on W/G (from the Fréchet averages paper) is:
    d(M₁, M₂)² = ||ΔW₁ - ΔW₂||_F²  (when both are near the same base point W₀)

MoTHer's rank-based distance is a more robust version: instead of Frobenius distance (which
mixes signal and noise), it uses the RANK of the difference = number of singular directions
where the models genuinely differ. This is the "TRS distance" between two models.

---

## The Isotropic Merging Perspective

Isotropic merging (isotropic_model_merging_spectral_skewness.pdf) introduces:
- "Spectral Skewness" = measure of SV distribution asymmetry
- High skewness: few very large SVs dominate (= Region 1 dominance = Platonic, universal)
- Low skewness: uniform SV distribution (= balance between Region 1 and Region 2)

The isotropic merging algorithm (Iso-CTS) normalizes for spectral skewness before merging.

In fiber bundle terms: spectral skewness = the ratio of Region 1 energy to Region 2 energy.
High skewness = merged model has lost task-specific signal (Region 2 averaged away, CLT effect)
= what happens after N-fold averaging (synthesis 13).

Isotropic merging is trying to RESTORE the Region 1 / Region 2 balance after averaging.
This is the same goal as:
- SVC (downscale Region 1 after over-accumulation)
- Subspace boosting (upscale Region 2 before it fully cancels)
- Isotropic merging (normalize for skewness = different framing of the same calibration)

**All three (SVC, subspace boosting, isotropic merging) are implementing the same spectral
renormalization of the merged model to restore the Region 1 / Region 2 balance.**

---

## The Specialization Stage Paradox Resolved

MoTHer observes: "Specialization Stage: fine-tuning weight outlier decrease"
The large SVs of W (= Region A of W₀) DECREASE during fine-tuning.

This seems paradoxical: fine-tuning adds information, so shouldn't the weight "energy" increase?

Resolution (from synthesis 17): **Correct fine-tuning redistributes weight from Region A to B.**

The large SVs (Region A = universal features, top-20%) are the "overhead" shared by all tasks.
During pretraining, these grow as the model learns universal patterns.
During fine-tuning: the new task redirects some of this universal capacity to task-specific uses.
The large SVs slightly decrease (Region A shrinks) while medium SVs increase (Region B grows).

This is CONSERVATION of spectral energy: the total Frobenius norm ||W||_F ≈ constant during
fine-tuning. Energy transfers from Region A (universal) to Region B (task-specific).

**DWS (Directional Weight Score = kurtosis) drops during fine-tuning** because kurtosis measures
the "peakedness" of the distribution (how much the extreme values dominate). As Region A shrinks
and Region B grows, the distribution becomes less peaked = lower kurtosis = lower DWS.

This makes DWS a measurement of how "general" vs "specialized" a model is:
- High DWS (high kurtosis) = dominated by Region A = general/pretrained
- Low DWS (lower kurtosis) = Region A/B balanced = specialized/fine-tuned
- Very low DWS (uniform) = Region A collapsed = over-fine-tuned / catastrophic forgetting

---

## Summary: The Complete Geometry of the Weight Space

The full picture that all these papers are converging on:

**Weight space W** = the space of all neural network parameter matrices
**Gauge group G = GL(r)** = the symmetry group of LoRA parameterizations
**Quotient manifold W/G** = the space of model FUNCTIONS = the model tree's base manifold

Distances on W/G:
- Fréchet distance (Fréchet averages paper) = exact metric
- MoTHer's rank distance = approximate robust metric
- Subspace Alignment Ratio SAR (isotropic merging) = angle-based metric

Moving on W/G:
- Fine-tuning = geodesic from W₀ to W_FT
- Task arithmetic = vector addition of geodesics (linear approximation)
- Model merging = barycenter computation on W/G

Structure of the tangent space at any point:
- Region 1 (universal fiber directions): same at every point → flat connection
- Region 2 (task-specific directions): varies with point → curved connection
- Region 3 (noise): isotropic, homogeneous → trivial structure

The model tree = the coarse topological structure of W/G:
each branching = fine-tuning that moves to a new region of W/G,
each leaf = a maximally specialized point far from the root.
