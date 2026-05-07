# Synthesis 16: Zero Holonomy — Five Methods, One Constraint

**Date:** 2026-05-07
**Session:** 5
**Previous synthesis:** synthesis_night_run_15_htsr_alpha_intrinsic_dim_convergence.md

---

## The Geometric Fact

Two LoRA adapters ΔW_1, ΔW_2 can be cleanly merged iff their Region 2 subspaces are orthogonal.

In fiber bundle language: subspace orthogonality = zero holonomy when parallel-transporting from
one adapter's tangent space to the other's. Non-orthogonal subspaces = nonzero holonomy = the
two tasks "interfere" in the shared weight space.

Five independent papers have discovered this fact and implemented it differently:

---

## The Five Implementations

### 1. OSRM (lora_interference_orthogonal_subspaces.pdf)
**When:** At merge time (post-hoc)
**How:** Project ΔW_2 into the orthogonal complement of ΔW_1's right singular subspace
    ΔW_2^orth = ΔW_2 - U_{ΔW_1} U_{ΔW_1}^T ΔW_2
**What they call it:** "Subspace Overlap as Predictor of LoRA Merge Interference"
**Key finding:** High subspace overlap (high cosine similarity between right singular subspaces)
    causally predicts merge interference. This is the EMPIRICAL VALIDATION that Region 2 angle
    = holonomy = merge quality.

### 2. EBLoRA (eblora_spectral_imbalance_forgetting.md)
**When:** During training (continual learning)
**How:** Restricted Stiefel manifold M_t = {U | U^TU = I_r, G_{t-1}^T U = 0}
    where G_{t-1} = gradient subspace from previous task
**What they call it:** "Spectral Imbalance" as forgetting cause; restricted Stiefel = solution
**Key finding:** Training on the restricted Stiefel manifold enforces orthogonality between
    task gradient subspaces → prevents forgetting → zero holonomy from the beginning

### 3. OPLoRA (oplora_orthogonal_projection_forgetting.md)
**When:** At initialization and during training
**How:** ΔW ∈ U_{W₀}^⊥ — project LoRA update into the complement of W₀'s dominant singular
    subspace (preventing intruder dims by keeping ΔW in the horizontal subbundle)
**What they call it:** "Orthogonal Projection" to prevent forgetting
**Key finding:** This is orthogonality against W₀ (not against other tasks), but implements
    the same principle: keep ΔW in a subspace that is orthogonal to the "fixed" directions
    (W₀'s dominant subspace). This is INTER-MODEL holonomy (task vs. pretrained model).

### 4. mtLoRA (mtlora_spectral_multitask_regularization.md)
**When:** During multi-task LoRA training
**How:** SV-reweighted regularization L = λ Σ w(σ) ||(B_i)^T B_j||_F^2
    with w(σ) = exp(-σ/σ̄) — high weight for low-SV directions (Region 2)
**What they call it:** "Spectral Multi-Task Regularization"
**Key finding:** Orthogonalizing Region 2 (low-SV, task-specific) directions across tasks
    while protecting Region 1 (high-SV, shared) = soft zero-holonomy constraint on Region 2

### 5. Share (shared_lora_subspaces_continual_learning.md)
**When:** Across tasks (continual learning)
**How:** Maintains a "foundational subspace" (Region 1) shared across all tasks; task-specific
    updates are constrained to the orthogonal complement of this shared subspace
**What they call it:** "Shared LoRA Subspaces" for continual learning
**Key finding:** New tasks learn in the complement of the foundational subspace = orthogonal
    to all previous tasks' Region 1 = zero holonomy in the shared fiber direction

---

## Why These Are All the Same Constraint

The common constraint: **the Region 2 subspaces of any two tasks must be orthogonal.**

Geometrically: for LoRA adapters ΔW_i, ΔW_j:
    cos(Region2(ΔW_i), Region2(ΔW_j)) = 0  ↔  zero inter-task holonomy

Written as matrix equations:
- OSRM: V_1^T V_2 ≈ 0 (post-hoc, approximate)
- EBLoRA: U_1^T U_2 = 0 (enforced during training, exact)
- OPLoRA: V^T U_{W₀} ≈ 0 (orthogonal to pretrained, not other tasks)
- mtLoRA: B_i^T B_j ≈ 0 for low-SV components (soft, weighted)
- Share: new_task_vectors ⊥ foundational_subspace (categorical, exact for Region 1)

The five methods differ in:
- WHEN: training-time (EBLoRA, mtLoRA, Share) vs. merge-time (OSRM) vs. init-time (OPLoRA)
- WHICH pairs: task-task (OSRM, EBLoRA, mtLoRA, Share) vs. task-pretrained (OPLoRA)
- HOW STRICT: exact orthogonality (EBLoRA, Share) vs. soft regularization (mtLoRA) vs. post-hoc (OSRM)

But the underlying geometry is identical.

---

## New Prediction From This Unification

If zero holonomy = zero merge interference, then:
1. OSRM's post-hoc projection should achieve the same merge quality as EBLoRA's training-time orthogonality — IF the task subspaces after vanilla LoRA training are random (not already near-orthogonal).

2. mtLoRA's soft constraint (exp(-σ/σ̄) weighting) is an approximation of OSRM's hard projection. The approximation quality depends on the low-SV components — if they are already near-orthogonal in practice (as mtLoRA hopes), the soft constraint is sufficient.

3. **The GL(r) gauge symmetry is what makes these constraints necessary.** Without gauge symmetry, the "direction" of ΔW would be uniquely defined. With GL(r), the right singular subspace of ΔW is gauge-invariant (it's the canonical projection direction from synthesis 14). The orthogonality constraint is on THIS canonical subspace — not on the raw (A, B) matrices.

4. **Cross-LoRA transfer (cross_lora_transfer_heterogeneous_llms.pdf) should work best when the source and target models share the same Region 1 subspace** (same universal fiber direction). The LoRA-Align component is measuring exactly the overlap between these Region 1 subspaces across architectures. Zero transfer = orthogonal Region 1 subspaces = zero shared fiber.

---

## The Diagram

Pre-training W₀ creates a FIXED set of directions (its dominant singular subspace = Region 1).

Each fine-tuning task learns in a different direction in the COMPLEMENT of Region 1.
If two tasks learn in orthogonal directions: zero holonomy, perfect merging.
If two tasks learn in the same direction: maximum holonomy, total interference.

The optimal fine-tuning strategy: learn in directions that are:
- Orthogonal to W₀'s dominant singular subspace (prevents intruder dims → OPLoRA)
- Orthogonal to all other tasks (prevents merge interference → EBLoRA/mtLoRA/OSRM)
- Within the d_task-dimensional subspace determined by the task's intrinsic dimension (GELoRA)

This triple constraint uniquely determines the ideal LoRA update for any task:
    ΔW* = projection onto (U_{W₀}^⊥ ∩ span{all previous tasks}^⊥ ∩ task intrinsic subspace)

The Region 2 of the three-region decomposition IS this constrained subspace.
