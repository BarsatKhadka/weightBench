# Synthesis 9: The Grand Chain — Implicit Regularization, BBP Transition, and Grokking as Horizontal Subbundle Return

**Date:** 2026-05-07
**Session:** 4 (continued)
**Previous synthesis:** synthesis_night_run_8_mechanistic_intruder_dims.md

---

## The Chain

This synthesis documents a chain of equivalences that was NOT visible from within any single
paper but becomes clear when you read the graph:

```
Nuclear norm minimization (Gunasekar 1705.09280)
    = GD's implicit variational principle on factorized matrices
    = sparse singular value spectrum
    = few above-MP singular values

BBP phase transition (Baik-Ben Arous-Péché)
    = singular value crosses Marchenko-Pastur upper edge
    = λ+ = σ²(1 + √(n/m))² = σ(√m + √n)
    = same threshold in DP-SGD gradient matrices (2510.01137)
    = same threshold in TRS signal detection
    = "Bulk+Spike" phase onset in HT-SR (Martin & Mahoney)

Grokking as rank minimization (2408.11804)
    = generalizing networks → low-rank W
    = memorizing networks → high-rank W
    = grokking transition = moment of rank drop
    = weight decay amplifies rank drop

Horizontal subbundle (fiber bundle theory)
    = ker(ω) = W₀-orthogonal subspace
    = OPLoRA's U_W₀^⊥ constraint
    = low-rank solution in W₀-aligned directions
    = zero forgetting
```

**The chain claims:** All four chains describe the SAME geometric phenomenon from different vantage points.

---

## 1. Nuclear Norm Minimization = Horizontal Subbundle Variational Principle

Gunasekar et al. (1705.09280) proved that gradient descent on underdetermined factorized
objectives implicitly minimizes the nuclear norm:
    ||ΔW||_* = Σᵢ σᵢ(ΔW)

Minimizing nuclear norm = minimizing total singular value mass = biasing toward a sparse
singular value spectrum = few singular values above the MP threshold.

Kim et al. (2502.09376) extends this to LoRA specifically: LoRA training with zero-init B
and weight decay converges to a low-rank global minimum via this implicit bias.

**What the fiber bundle framework adds:** Nuclear norm minimization is the variational
statement of the horizontal subbundle condition. The minimum nuclear norm solution for ΔW
consistent with task constraints is the solution that minimizes the number of above-MP
singular values — and among solutions with the same count, the one that best aligns those
singular values with the W₀ fiber (genuine TRS directions).

This is why LoRA works even without OPLoRA's explicit projection: implicit regularization
already exerts horizontal subbundle pressure. OPLoRA makes the constraint exact; implicit
regularization makes it approximate but automatic.

**New prediction:** The "nuclear norm optimal" LoRA and the "OPLoRA-constrained" LoRA should
converge to similar solutions when the implicit regularization is strong enough (high weight
decay, sufficient training). At low weight decay (weak implicit regularization), they diverge:
the unconstrained LoRA accumulates more intruder dims (vertical fiber drift), while OPLoRA
maintains the horizontal constraint exactly.

---

## 2. BBP = MP = TRS = HT-SR: Four-Way Equivalence of a Single Threshold

The BBP (Baik-Ben Arous-Péché) phase transition is a theorem from random matrix theory:
for an m×n random matrix plus a rank-1 signal, the signal is detectable if and only if
its singular value exceeds:

    λ_BBP = σ(√m + √n)  [= σ²(1 + √(n/m))² in eigenvalue normalization]

This is exactly the Marchenko-Pastur upper edge λ+ for an m×n noise matrix.

The four-way equivalence:
1. **RMT (MP):** Above the Marchenko-Pastur edge = signal (not noise)
2. **BBP:** Signal has undergone the Baik-Ben Arous-Péché phase transition = detectable
3. **TRS:** Above-MP singular value of ΔW = candidate for genuine TRS or intruder dim
4. **HT-SR:** "Bulk+Spike" phase = first singular value has crossed the MP edge = spectral
   evidence of learned structure

This is not an analogy. It is the same mathematical inequality expressed in four different
contexts and vocabularies. The TRS detection criterion is the BBP phase transition criterion
applied to ΔW's singular values.

The paper 2510.01137 makes this explicit for gradient matrices during fine-tuning:
the BBP threshold = σ(√m + √n) = the MP upper edge is the exact denoising boundary.
Signal components above this threshold are preserved; noise components are suppressed.

**New prediction from BBP framework:** The number of LoRA rank dimensions that are
"effective" (contribute to task performance) = the number of ΔW singular values exceeding
the BBP threshold for the specific (m,n) dimensions of each weight layer. This gives
a layer-dependent, theoretically grounded rank selection criterion that should outperform
fixed-rank LoRA. This is exactly what AdaLoRA discovers empirically but without the BBP
theoretical grounding.

---

## 3. Grokking = Transition from Vertical Fiber to Horizontal Subbundle

Yunis et al. (2408.11804) establish empirically:
- True-label training: effective rank decreases → low-rank solution
- Random-label training (memorization): effective rank stays high → high-rank solution
- Grokking transition = the moment of rank drop

**Interpretation in the fiber bundle framework:**

The memorization solution lives in the **vertical fiber** (intruder-dim-rich):
- Many above-MP singular values of ΔW active
- Low W₀-alignment (the spurious label-feature correlations don't align with pretrained structure)
- High intruder Frobenius energy
- Equivalent to the Alignment Collapse paper's "overfitted" state

The generalization solution lives in the **horizontal subbundle** (genuine TRS dominant):
- Few above-MP singular values (the task signal is genuinely low-rank)
- High W₀-alignment (genuine task knowledge aligns with pretrained structure)
- Low intruder Frobenius energy
- Equivalent to OPLoRA's U_W₀^⊥-constrained solution

**Grokking = the network escaping the vertical fiber and finding the horizontal subbundle.**

Weight decay accelerates this because it suppresses intruder-dim singular values (which are
small but above-MP) faster than it suppresses genuine TRS singular values (which are large
and well above MP). This selective suppression is the geometric action of weight decay on
the fiber bundle.

### Anti-grokking in this framework

Anti-grokking (late-stage generalization collapse, Community 8 in the graph) = the network
drift BACK from the horizontal subbundle into the vertical fiber due to continued training
without weight decay. The Alignment Collapse quartic law (2602.15799) describes this drift:
after reaching the horizontal subbundle, curvature coupling continues to push ΔW into
non-horizontal (intruder dim) directions, eventually overwhelming the genuine TRS signal.

Together: grokking = reaching ker(ω); anti-grokking = escaping ker(ω) post-generalization.
Weight decay = the force that maintains ker(ω) residency.

---

## 4. The Slow Fisher Mode Connection

Grokfast (2405.20233) found that grokking's delayed transition is driven by "slow modes" —
gradient components with slowly changing direction. The fast gradient modes drive overfitting
(vertical fiber drift); the slow gradient modes drive generalization (horizontal subbundle
approach).

**Connection to Fisher structure:** The Fisher information matrix F identifies directions of
high curvature (fast Fisher modes) vs. low curvature (slow Fisher modes). The slow gradient
modes in Grokfast = the directions with low Fisher eigenvalues = directions near ker(F) = 
directions near the horizontal subbundle ker(ω).

**The grokking delay = the time for the optimization trajectory to accumulate enough
displacement along slow Fisher modes (near ker(ω)) to transition to the horizontal subbundle.**

Weight decay helps by making the vertical fiber (high curvature, high intruder dim) costly,
allowing the slow Fisher modes to dominate.

This connects:
- Grokfast's signal-processing insight (slow/fast gradients)
- Fisher geometry (high/low eigenvalue directions)
- Fiber bundle geometry (vertical fiber / horizontal subbundle)
All three are different descriptions of the same decomposition.

---

## 5. What These Connections Imply for Each Community in the Graph

### HT-SR Community (Community 21)
**New connection:** The five HT-SR training phases map to TRS stages:
- Bulk-only → no above-MP signal, no TRS
- Bulk+Spike → BBP transition occurred, genuine TRS emerging
- Heavy-Tailed → many above-MP components, mixed genuine TRS + intruder dims
- Rank Collapse → intruder dims dominated, genuine TRS overwhelmed (anti-grokking)

After LoRA fine-tuning, the power-law exponent α of W should:
- Decrease (ESD more heavy-tailed) if genuine TRS was added efficiently
- Increase toward α=2 (more random-looking) if intruder dims dominate (W corrupted)

**This is a testable prediction** connecting HT-SR's α exponent to intruder dim fraction.

### SLT/LLC Community (Community 17)
**New connection:** The generalization solution (low-LLC basin) = the horizontal subbundle
solution. Low LLC = low real log-canonical threshold = near a singularity of the parameter
space. The fiber bundle is singular exactly where GL_r acts non-freely (rank deficiency = GAP 1).

The LLC measures how "degenerate" the Fisher matrix is at the current solution. A solution
in ker(F) (horizontal subbundle) is the most degenerate (LLC ≈ minimum for the task class).
Low LLC at the generalization basin = the basin is in ker(F) = the basin is horizontal.

**The LLC measures horizontal subbundle proximity.** Low LLC = near ker(ω).

### Grokking Community (Communities 8, 16, 17)
**New unification:** All grokking explanations (SLT basins, dimensional phase transition,
HT-SR phases, rank minimization) are equivalent descriptions of the horizontal subbundle
transition. The "competing loss basins" (SLT) = vertical fiber vs. horizontal subbundle.
The "dimensional phase transition" (D crosses 1) = effective rank dropping below 1 above-MP
component = first genuine TRS emerging.

---

## 6. What Is Still Missing

### The RLCT of the Fiber Bundle Singularity
Watanabe's SLT computes the real log-canonical threshold (RLCT) λ for any singularity in
the parameter space. The fiber bundle W → W/G has singularities at rank-deficient points.
What is the RLCT of these singularities?

If the RLCT at ker(F) equals the empirically measured LLC at grokking basins, that would
confirm the SLT ↔ fiber bundle connection. This is an unexplored calculation.

### BBP for W₀ + ΔW (not just ΔW alone)
The current BBP analysis applies to ΔW in isolation. But the fine-tuned model is W = W₀ + ΔW,
where W₀ is NOT a random matrix — it is heavy-tailed (post-pretraining HT-SR phase).
The BBP transition for a heavy-tailed + low-rank signal perturbation is NOT the same as for
a pure MP noise matrix. This is an unsolved RMT problem for neural networks specifically.

### Implicit Regularization for Non-Zero B Initialization
Gunasekar's theorem requires initialization near zero. LoRA uses B=0 initialization (so the
theorem applies). But FILet, PiSSA, and MiLoRA use non-zero initializations for A and B.
The implicit regularization theorem breaks down in these cases. What replaces it?

---

## 7. Summary

The investigation of four previously unexplored papers reveals a grand chain of equivalences:

**Nuclear norm minimization (Gunasekar)**
→ **sparse above-MP singular spectrum**
= **BBP phase transition threshold = MP upper edge** (from RMT)
= **TRS signal detection criterion**
= **HT-SR Bulk+Spike phase onset**
→ **grokking = rank drop = horizontal subbundle transition** (from 2408.11804)
→ **OPLoRA / FILet / ker(ω)** = the same geometric object reached by implicit regularization

These were five independent threads (implicit regularization, RMT/BBP, TRS, HT-SR, grokking)
that were always the same thread. The knowledge graph makes this visible.

Novel open predictions from this chain:
1. LoRA + weight decay → convergence toward pure genuine TRS (no intruder dims) as weight
   decay → ∞ (testable: measure intruder Frobenius vs. weight decay coefficient)
2. LLC of LoRA solution should anticorrelate with intruder dim energy (lower LLC = fewer intruder dims = closer to ker(F))
3. HT-SR α exponent post-LoRA-fine-tuning should decrease (more heavy-tailed) for task-efficient LoRA and increase (less heavy-tailed) for intruder-dim-dominated LoRA
4. LoRA rank r should be set to the number of ΔW singular values exceeding the BBP threshold — this is the theoretically optimal rank (AdaLoRA discovered this empirically)
