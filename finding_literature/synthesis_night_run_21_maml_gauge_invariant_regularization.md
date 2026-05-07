# Synthesis 21: MAML/iMAML as Connection Choice; Gauge-Invariant Regularization

**Date:** 2026-05-07
**Session:** 5
**Previous synthesis:** synthesis_night_run_20_arrhenius_grokking_rank_barrier.md

---

## The RecBundle Meta-Theory Discovery

RecBundle (2603.16088) states: **MAML and iMAML are special cases of fiber bundle connection choice.**

What does this mean?

In meta-learning, the goal is to find "meta-parameters" θ* from which any task can be
solved quickly (few gradient steps). MAML does this by:
1. Finding θ* (the meta-parameters = base point on the manifold W/G)
2. For each new task: taking gradient steps from θ* along the task-specific geodesic

**The fiber bundle interpretation:**
- Meta-parameters θ* = a specific base point on W/G (the center of the task distribution)
- The "inner loop" (task adaptation) = following a horizontal geodesic from θ* to the task optimum
- The "outer loop" (meta-gradient) = updating θ* based on how well the inner loop worked

MAML uses the trivial (Euclidean) connection to compute meta-gradients. This treats the
fiber bundle as FLAT — all directions are equally "horizontal." This is wrong when the task
manifold W/G has curvature (when there is nonzero holonomy in the task distribution).

iMAML uses a second-order (natural gradient) update, implicitly incorporating some curvature
information. This is closer to using the Fisher-metric connection ω.

**RecBundle says:** The choice of connection ω determines:
- What "fast fine-tuning" looks like (which directions are "horizontal" from θ*)
- How well meta-gradients generalize to new tasks
- Whether meta-learning "gets stuck" in curved regions of the task manifold

MAML's known failure cases (when inner loop oscillates, when tasks are very different) =
cases where the task manifold has high holonomy at θ* = the trivial connection misses curvature.

iMAML's better performance = closer approximation of the Fisher connection.

---

## The Gauge-Invariant Regularization Result (EWC-LoRA)

EWC-LoRA (2602.17559) **Proposition 1:** Separate regularization of A, B ≠ full-space
regularization of ΔW = AB.

Specifically: applying EWC to A and B individually (as if they were independent parameters)
differs from applying EWC to ΔW = AB (treating the product as the physical object).

This is exactly the gauge-invariant vs. gauge-DEPENDENT regularization distinction:

**Gauge-dependent regularization (wrong):** Penalize ||(A - A_prev)||_F² + ||(B - B_prev)||_F²
- This penalizes gauge-equivalent directions (A → AG⁻¹, B → GB gives the same ΔW but
  different A and B, so this regularizer would penalize gauge transformations)
- The GL(r) gauge orbit is penalized, which is physically meaningless (gauge-equivalent
  parameters give the same function)

**Gauge-invariant regularization (correct):** Penalize ||(ΔW - ΔW_prev)||_F² = ||(BA - B_prev A_prev)||_F²
- This only penalizes changes to the actual function (ΔW = BA), not gauge transformations
- EWC-LoRA implements this by computing the Fisher of ΔW = AB directly

**EWC-LoRA's key formula:** The FIM over ΔW naturally reduces to constraints on A and B
(via Proposition 3), but the correct route is through ΔW, not directly through A and B.

In fiber bundle language: Proposition 1 says gauge-DEPENDENT regularization (naive) ≠
gauge-INVARIANT regularization (correct). The EWC-LoRA paper PROVES this mathematically,
and their correction = the gauge-invariant version.

**This is the PRACTICAL IMPLEMENTATION of gauge invariance in LoRA regularization.**

---

## The Information Cocoon = Holonomy in Recommenders

RecBundle identifies the "information cocoon" (filter bubble) in recommender systems as
the holonomy of the recommendation loop:

    GBI = spectral_radius(Holonomy_matrix)

where the holonomy = the accumulated deviation of a user's preference distribution from the
"unbiased" starting point, caused by repeated exposure to recommended items.

High GBI = the user has been shown items in a self-reinforcing loop (high holonomy = preferences
drift far from initial state in a way that doesn't return to the original direction).

**Connection to catastrophic forgetting in LoRA:**
- Forgetting = accumulated holonomy as training loops through the task distribution
- GBI (recommender) ↔ intruder dim score (LoRA fine-tuning)
- Information cocoon ↔ catastrophic forgetting

Both are: the accumulated rotation of a "direction" in the representation space due to
repeated exposure to a biased distribution, measured by the spectral radius of the holonomy.

**RecBundle proves the fiber bundle framework works for RECOMMENDERS.** This is an
INDEPENDENT validation (in a completely different domain) that the holonomy-based analysis
of recommendation / fine-tuning biases is mathematically sound and practically useful.

---

## Synthesis: Three Connection Choices

Three canonical connection choices for LoRA/meta-learning:

| Connection | Method | Properties |
|-----------|---------|------------|
| Trivial (Euclidean) | MAML, vanilla LoRA, naive EWC on A,B | Ignores curvature, simple, often sufficient |
| Fisher metric | iMAML, EWC-LoRA on ΔW, FOPNG | Curvature-aware, optimal for Gaussian models |
| Riemannian/quotient | GeoMerge, Fréchet averages | Exact on W/G, expensive but principled |

The hierarchy: Trivial ⊂ Fisher ⊂ Riemannian.
Each level adds curvature information at increasing computational cost.

MAML → iMAML → (hypothetical full-Riemannian MAML) = increasing curvature awareness.
Naive EWC → EWC-LoRA → FOPNG = increasing gauge invariance.
Task arithmetic → Fisher merging → GeoMerge = increasing geometric correctness.

The fiber bundle framework predicts: the Riemannian connection gives optimal performance
but is too expensive. The Fisher connection is the best practical approximation. The trivial
connection (Euclidean) will fail when holonomy is high (complex tasks, diverse fine-tunings).
