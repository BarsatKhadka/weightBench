# Synthesis 13: The HOSVD O(1/√N) Theorem as a Central Limit Law in Weight Space

**Date:** 2026-05-07
**Session:** 5
**Previous synthesis:** synthesis_night_run_12_revised_trs_spectrum_three_regions.md

---

## The Core Mathematical Statement

HOSVD (subspace_boosted_model_merging_hosvd.pdf) proves:

**Proposition 1:** σ_task(merged) ~ O(1/√N) as N → ∞
**Proposition 2:** stable_rank(merged) → rank(common_subspace) as N → ∞

This is a **Central Limit Theorem in weight space**. Here is why:

When N task vectors {ΔW_1, ..., ΔW_N} are summed (task arithmetic), decompose each:
    ΔW_i = C_i + T_i
where C_i ∈ common subspace (Region 1) and T_i ∈ task-specific subspace (Region 2).

**Common components:** C_i ~ O(1) for all i, and they all point in roughly the same direction
(by definition of "common subspace" = high inter-task alignment, 89% per mtLoRA).
    ||Σ C_i||_F ~ O(N)    (coherent summation)

**Task-specific components:** T_i are in "random" relative orientations (3% inter-task alignment
in bottom 50% per mtLoRA). Their sum is like a random walk in weight space:
    ||Σ T_i||_F ~ O(√N)   (incoherent, CLT-like summation)

Therefore, when you divide by N to normalize the merge:
    C term: O(N)/N = O(1) — survives
    T term: O(√N)/N = O(1/√N) — decays

This is **exactly** Proposition 1. The O(1/√N) is not an accident — it is the signature of
incoherent (random-direction) summation, the same scaling as a random walk.

---

## Self-Averaging of Holonomy

In fiber bundle language, the HOSVD CLT becomes:

**The holonomy of the averaged model converges to the identity as N → ∞.**

Recall: holonomy measures how much parallel transport around a loop deviates from identity.
- Region 1 (universal fiber): zero holonomy — parallel transport is the identity already
- Region 2 (task-specific): nonzero holonomy — these are the "curved" directions

When averaging N task vectors:
- Region 1 holonomy = 0 for each task → 0 for the average ✓
- Region 2 holonomy: H_1, H_2, ..., H_N are in random relative positions in the Lie group.
  By the Law of Large Numbers on SO(d): (1/N)Σ H_i → exp(E[log H_i]).
  If the H_i have zero mean (no preferred curvature direction), this → identity matrix.

The O(1/√N) from HOSVD = the **rate of convergence** of this holonomy averaging to identity.
At any finite N, the averaged holonomy is O(1/√N) away from identity.

**New prediction:** For N merged models, the residual task signal (Region 2 component) has
magnitude O(1/√N) relative to the universal fiber. The merged model "forgets" all task-
specific signal, retaining only the flat-fiber universal component — exactly what Proposition 2
(stable rank collapse to common subspace rank) states geometrically.

---

## Task Arithmetic Is a Law of Large Numbers Operation

This reframes task arithmetic fundamentally:

**Task arithmetic = projection onto the flat fiber in the N → ∞ limit.**

The convergence rate is O(1/√N). For small N (2-5 tasks), significant task signal (Region 2)
remains in the merged model. For large N, the merge collapses to the universal fiber.

Consequence 1: **Task arithmetic fails in the rank-collapse regime not because it's a bad
algorithm — it's doing exactly what averaging does: converging to the mean direction.**
The failure is using the merged model for a specific task when you needed the task-specific
(Region 2) component, which has been diluted.

Consequence 2: **The "effective number of independent tasks" in a merge is proportional to N.**
But the signal-to-noise ratio for any individual task decays as 1/√N. This is the **fundamental
tradeoff** in task arithmetic: merging more models reduces individual task fidelity quadratically
in the merge count.

Consequence 3: **Extracting task-specific signal after merging.** If the merged model M_merged
is available, and one task-specific model M_task is known, then:
    Region 2 component of M_task = M_task - M_merged + O(1/√N) correction
This is a practical denoising procedure: subtract the universal fiber (= merged model)
to recover approximately task-specific signal.

---

## Connection to Spectral Over-Accumulation

The spectral over-accumulation paper (2602.05536) identifies that aligned TRS spikes double
when merging. This is now explained by the HOSVD CLT:

- **Aligned task vectors (Region 1)**: O(N) growth (coherent) → spike amplitude doubles, triples, ...
- **Unaligned task vectors (Region 2)**: O(√N) growth (incoherent) → spike amplitude grows slowly

The SVC (Singular Value Calibration) correction proposed by spectral over-accumulation = a manual
correction for the O(N) vs O(√N) differential growth rate. SVC rescales Region 1 spikes back
from O(N) to O(1). This is an empirical fix for the same mathematical phenomenon HOSVD proves.

**Unification:** SVC + subspace boosting (HOSVD's correction) = spectral renormalization of
the merged model to restore the O(1) : O(1) balance between Region 1 and Region 2.
- SVC: scale down Region 1 (O(N) → O(1))
- Subspace boosting: scale up underrepresented Region 2 (rescue the O(1/√N) before it vanishes)

Together they implement a **merged-model spectral normalizer** that undoes the N-fold averaging
distortion.

---

## Connection to the Universal Subspace (arXiv:2512.05117)

The universal subspace paper identifies ~16 dimensions shared by 1100+ LoRA adapters.
HOSVD now explains WHY this universal subspace is universal:

**It is the set of directions that survived O(N) averaging across thousands of fine-tunings.**

The ~16-dimensional universal subspace is the N→∞ fixed point of the model merging operator
M_avg(ΔW_1, ..., ΔW_N) = (1/N) Σ ΔW_i.

Any direction not in the universal subspace decays as O(1/√N) under repeated averaging.
Only the zero-holonomy flat fiber directions (Region 1) survive. The universal subspace
= the eigenspace of M_avg with eigenvalue 1 (survives averaging exactly).

**New prediction from this connection:** The ~16 universal subspace dimensions should be
EXACTLY the same as the top-eigenvectors of any large-N average of LoRA adapters — regardless
of the specific tasks, architectures, or training procedures (subject to same base model).
This is a sharp testable prediction: collect 100+ LoRAs, compute their average, SVD → top-16
eigenvalues should match the reported universal subspace.

---

## Connection to GELoRA's Rank Bound

GELoRA gives r_i ≥ intrinsic_dim(task). Combined with the HOSVD CLT:

**When merging N tasks, the effective intrinsic dimension of the merged model is NOT N × d_task.**
It is approximately: dim(Region 1) + O(1/√N) × N × d_task = 16 + O(√N × d_task)

For large N, the merged model occupies approximately sqrt(N) × d_task dimensions above the
universal fiber. This is much smaller than the N × d_task expected from N independent tasks.
The CLT compression reduces the effective rank of the merged model to sublinear in N.

**GELoRA corollary for merging:** The optimal rank for a model that is to be merged with N
others is NOT r = 16 + d_task. It should be r = 16 + c × d_task/√N to account for the fact
that the task-specific signal will be diluted by 1/√N after merging. This suggests that
models intended for merging should use HIGHER rank (to survive the 1/√N dilution) or should
apply subspace boosting BEFORE merging (HOSVD's prescription).

---

## Connection to mtLoRA's SV-Weighting

mtLoRA's SV-weighting w(σ) = exp(-σ/σ̄) can now be interpreted as a CLT-aware regularizer:

- High σ (Region 1, common subspace): these survived N-fold averaging → low regularization weight
  = "these directions are robust, don't penalize them"
- Low σ (Region 2, task-specific): these decay as 1/√N under averaging → high regularization weight
  = "these directions need protection: orthogonalize them so they don't cancel each other"

The SV-weighting is implicitly encoding the HOSVD scaling law: it knows which directions
survive averaging (high σ) and which cancel (low σ), and regularizes accordingly.

**The mtLoRA regularizer is an implicit HOSVD correction.** It doesn't compute HO-GSVD
explicitly, but the exp(-σ/σ̄) weighting captures the same physics.

---

## Self-Averaging as a Phase Transition Framing

There is a precise analogy to **disorder-averaging in statistical mechanics**:

In spin glasses: individual disorder realizations J_ij are random, but physical observables
self-average to their quenched average in the thermodynamic limit.

In LoRA merging: individual task vectors T_i are in "random" relative orientations, but the
merged model self-averages to the universal fiber in the N→∞ limit.

**The holonomy is the order parameter for this "task averaging phase transition":**
- Small N (disordered phase): holonomy is large (O(1)), each task retains its identity
- Large N (averaged phase): holonomy → 0, all task identity lost, only universal fiber remains

The O(1/√N) decay is the finite-size scaling near the "transition." There is no sharp phase
transition (this is a smooth CLT convergence), but the analogy suggests that the "transition
temperature" is determined by the variance of the holonomy distribution: tasks with high
holonomy variance (highly varied tasks) will lose their signal faster than tasks with low
holonomy variance (all tasks are similar).

---

## Summary of New Connections

1. **HOSVD CLT = holonomy self-averaging law:** task-specific holonomy cancels as O(1/√N)
2. **Task arithmetic = flat-fiber projector in large N:** converges to universal subspace
3. **Universal subspace (~16 dims) = fixed point of averaging operator M_avg**
4. **SVC + subspace boosting = spectral renormalization that undoes N-fold averaging distortion**
5. **mtLoRA SV-weighting = implicit HOSVD correction** without explicit HO-GSVD computation
6. **GELoRA rank bound for merging:** optimal rank scales as 16 + c × d_task/√N for merged models
7. **Phase transition analogy:** holonomy is the order parameter; O(1/√N) is finite-size scaling

## Open Question

Does the self-averaging of holonomy depend on the gauge choice? The fiber bundle formulation
requires a choice of connection ω before holonomy is well-defined. If the connection is the
Fisher-metric connection (as the TRS framework suggests), then the averaging should be
Fisher-metric weighted. This would mean that tasks with high Fisher norm contribute MORE to
the average (they have higher weight in the Fisher metric), and the convergence is not
uniform-CLT but Fisher-weighted CLT.

Prediction: the universal subspace directions are NOT the eigenvectors of the uniform average
(1/N)Σ ΔW_i, but the eigenvectors of the Fisher-weighted average Σ I(φ_i) ΔW_i / Σ I(φ_i).
This is untested and would distinguish Fisher-connection averaging from Euclidean averaging.
