# Synthesis 10: Three Implementations of the Horizontal Subbundle + Sheaf Resolution of GAP 1

**Date:** 2026-05-07
**Session:** 4 (continued)
**Previous synthesis:** synthesis_night_run_9_implicit_reg_bbp_grokking.md

---

## Overview

This synthesis connects three independently derived implementations of the horizontal subbundle
constraint, discovers a genuine tension and its resolution between EBLoRA and TRS, and
proposes the sheaf-theoretic atlas (Javidnia 2603.00824) as a more principled resolution
of GAP 1 than the Tikhonov regularization proposed in synthesis 7.

---

## 1. Three Implementations of the Same Constraint

The fiber bundle framework predicts: ΔW ∈ ker(ω) ↔ orthogonal to W₀'s dominant singular
subspace ↔ zero forgetting. Three papers independently implement versions of this constraint:

### Implementation A: OPLoRA (arXiv:2510.13003)
**Constraint:** ΔW ∈ span(U_{W₀}^⊥) — W₀-singular-subspace orthogonality
**Reference frame:** W₀ singular subspace (pretrained weight structure)
**Mechanism:** Explicit projection at initialization + during training
**What it prevents:** Overwriting of pretrained singular triples
**Mathematical guarantee:** Exact preservation of top-k singular triples

### Implementation B: EBLoRA (arXiv:2602.00722)
**Constraint:** U_t ∈ M_t = {U | U^TU = I_r, G_{t-1}^T U_t = 0}
— gradient-subspace orthogonality (Restricted Stiefel Manifold)
**Reference frame:** Previous task gradient subspace
**Mechanism:** Projection onto restricted Stiefel manifold + whitening retraction
**What it prevents:** Overwriting of directions sensitive to previous task performance
**Mathematical guarantee:** Zero gradient interference with previous task directions

### Implementation C: FILet (arXiv:2605.01046)
**Constraint:** Initialize LoRA in low-Fisher-energy directions
**Reference frame:** Fisher information matrix curvature
**Mechanism:** Select initialization via Fisher energy E(Z) = min singular value of FIM
**What it prevents:** Initializing in directions of high curvature (high forgetting risk)
**Mathematical guarantee:** Horizontal subbundle initialization (Alignment Collapse shows
  this doesn't persist under training, but it is the right START)

### The Triangle of Equivalence
When W₀ is well-trained (pretrained), these three reference frames approximately coincide:
- U_{W₀} dominant singular subspace ≈ principal gradient directions of pretraining ≈
  high-Fisher-energy directions at W₀

All three say: "don't move in the directions that encode pretrained knowledge." They are
the same constraint expressed in three languages: singular vector geometry (OPLoRA), gradient
memory (EBLoRA), and Fisher curvature (FILet).

The triangle is not exact — they diverge in edge cases (e.g., when W₀ is not fully trained,
or when task gradients diverge from W₀'s singular structure). But the structural equivalence
is the key insight.

---

## 2. The EBLoRA-TRS Tension and Its Resolution

### The apparent conflict
- **TRS:** large above-MP singular values of ΔW = genuine task signal (good)
- **EBLoRA:** large singular values = spectral imbalance = cause of forgetting (bad)

### The resolution
Both are right, but in different settings:
- **TRS context:** single fine-tuning task; large above-MP components = efficient encoding
  of task signal into few directions; no previous task to overwrite
- **EBLoRA context:** continual learning, sequential tasks; large ΔW_t singular values in
  W₀-aligned directions overwrite W₀ + ΔW_{t-1} structure

The distinction is DIRECTION, not magnitude:
- Large σ_i in W₀-orthogonal direction = good (genuine TRS, no overwriting)
- Large σ_i in W₀-aligned direction = bad (intruder dim in single-task; forgetting in CL)

**What EBLoRA should do (but doesn't):** equalize singular values WITHIN the W₀-orthogonal
subspace, allowing genuine TRS components to be large while keeping them all within ker(ω).
Current EBLoRA equalizes globally — it suppresses genuine TRS signal along with intruder dims.

### The optimal algorithm (not yet implemented)
Combining OPLoRA + EBLoRA + TRS:
1. Project ΔW into U_{W₀}^⊥ (OPLoRA's constraint) — ensures horizontal subbundle
2. Equalize singular values within U_{W₀}^⊥ (EBLoRA's principle) — prevents spectral
   imbalance within the allowed subspace
3. The resulting ΔW is: in ker(ω) AND has balanced energy distribution
   = pure genuine TRS with zero spectral concentration = minimum forgetting + optimal CL

This algorithm is a synthesis of three existing papers but doesn't exist in any of them.

---

## 3. Sheaf Theory as the Correct Framework for GAP 1

### The GAP 1 problem recap
The Fisher metric F degenerates (rank(F) < n²) throughout W. The horizontal subbundle
ker(ω) is not a proper vector bundle — it has varying dimension. Defense B (Tikhonov,
synthesis 7) adds εI to make F everywhere invertible, but loses the ε → 0 geometry.

### The sheaf resolution
A **sheaf** over a base space assigns to each open set a set of local sections, with
consistency conditions on overlaps. A fiber bundle is a sheaf where all fibers are isomorphic.
When fibers can have different dimensions, the correct structure is a sheaf.

For weight space:
- At "generic" W₀ (rank(F) = full): the horizontal subbundle ker(ω) has fixed dimension
  → fiber bundle structure holds locally
- At "singular" W₀ (rank(F) < full): the horizontal subbundle has larger dimension
  (more directions are horizontal) → the fiber "expands" → sheaf handles this

The **sheaf of horizontal subspaces** assigns to each W₀ the space ker(F(W₀)) with
appropriate consistency conditions as W₀ varies. This is mathematically natural and doesn't
require regularization.

### What this means for the paper
GAP 1 is resolved more elegantly by promoting the fiber bundle to a sheaf:
- Defense B (Tikhonov) = a regularization hack that makes the bundle work
- Defense A (constant-rank stratum) = restricts to where the bundle works
- Sheaf theory = the CORRECT framework for varying-rank connections

For the paper: restate Theorem 3 (Fisher Bundle Connection) as:
"The Fisher sheaf of horizontal subspaces on W assigns to each weight W₀ the kernel
ker(F(W₀)) ⊆ T_{W₀}W. When F(W₀) is everywhere full-rank (e.g., on the constant-rank
stratum), this sheaf restricts to a principal fiber bundle with structure group GL_r."

The sheaf formulation makes the rank-degeneracy explicit and handled, not an assumption.

### Javidnia's contribution: spanning-tree holonomy
Javidnia's Theorem 5.1 (Spanning-Tree Gauge Identity) gives a PRACTICAL ALGORITHM:

For a set of LoRA checkpoints {ΔW_1, ..., ΔW_T} on a task sequence:
1. Build a spanning tree on the task graph weighted by LoRA similarity
2. Chord residuals = mismatches between transport along tree paths vs. direct connections
3. Holonomy of fundamental cycle = chord residual product

**In our context:** This means measuring holonomy from pairwise LoRA adapter distances,
without running the sequential fine-tuning loop. The experiment in run_experiment.py
currently measures U_{W₀} vs. U_{S*} principal angles — Javidnia's theorem suggests a
complementary measurement: the holonomy computed from pairwise LoRA distances, using the
spanning tree of the 11 tasks.

This is a strictly more tractable version of the holonomy measurement that doesn't require
the weight-space ↔ representation-space isomorphism (which is still unproven).

---

## 4. New Connections in the Graph

### EBLoRA ↔ Restricted Stiefel ↔ Fiber Bundle
The Restricted Stiefel Manifold M_t is:
    M_t = Stiefel(r, d) ∩ {U : G_{t-1}^T U = 0}

In differential geometry, this is the intersection of:
- A compact Riemannian manifold (Stiefel)
- A closed submanifold (the gradient-orthogonality constraint)

The connection ω on the fiber bundle defines horizontal spaces; the Stiefel condition
defines orthonormality of the frame. M_t = the set of orthonormal horizontal frames.

This is the correct geometric interpretation: EBLoRA is doing gradient descent on M_t,
which is the horizontal frame bundle restricted to orthonormal frames.

### Neural Collapse ↔ EBLoRA ↔ Flat Spectrum
NC3 (equal top-C singular values) = flat singular spectrum of classifier weight matrix.
EBLoRA (equal singular values via scalar s_t) = flat singular spectrum of ΔW.
Universal subspace conjecture (16-dim flat fiber) = zero-holonomy directions in ker(ω).

All three point to the same geometric ideal: a flat (zero-curvature, equal-energy) structure
in the relevant weight subspace. The fiber bundle framework predicts this: the horizontal
subbundle has zero connection curvature (holonomy = 0), and zero curvature = flat metric =
equal singular values in all horizontal directions.

The universal subspace (flat fiber) = the ETF of the weight space = the neural collapse
condition applied to the adaptation subspace.

---

## 5. Open Questions Generated by This Synthesis

1. **Does EBLoRA + OPLoRA together outperform either alone?** The combined algorithm
   (orthogonal projection + flat spectrum) should be strictly better than either alone
   on continual learning benchmarks. This is a direct experimental test.

2. **What is the RLCT of the Restricted Stiefel Manifold M_t?** SLT says the LLC
   measures how "degenerate" the parameter space is at a solution. M_t is a manifold
   with a specific singularity structure (the gradient-orthogonality constraint creates
   a lower-dimensional intersection). The RLCT of M_t should be computable.

3. **Is the sheaf-theoretic formulation of GAP 1 equivalent to Defense B at ε → 0?**
   As ε → 0, Tikhonov F_ε → F and the regularized bundle approaches the singular
   sheaf. This is a formal limit question: does lim_{ε→0} (bundle with F_ε) = (sheaf
   with F)? If yes, Defense B and the sheaf formulation are canonically related.

4. **Can Javidnia's spanning-tree algorithm measure weight-space holonomy from LoRA
   pairwise distances?** This requires adapting Theorem 5.1 from representation space
   to weight space. The key question: is the pairwise LoRA distance (Frobenius norm of
   ΔW_i - ΔW_j) a valid "connection measure" for building the spanning tree? If the
   parallel transport in weight space is approximately Euclidean on small scales, yes.

5. **Does the ETF structure (NC3) of the classifier weight matrix predict LoRA intruder
   dim count?** If a model's classifier has strongly ETF-like singular values (flat top-C),
   does its LoRA fine-tuning produce fewer intruder dims? This bridges neural collapse and
   TRS in an experimentally testable way.
