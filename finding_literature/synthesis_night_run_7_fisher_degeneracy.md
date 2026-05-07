---
created: 2026-05-07
session: 4
iteration: 14
type: synthesis
topic: Fisher degeneracy — GAP 1 defense analysis
---

# Synthesis 7: The Fisher Degeneracy Problem (GAP 1)

## The Problem Statement

The fiber bundle theory's Theorem 3 (Fisher Bundle Connection) rests on the claim that the
Fisher Information Matrix defines a connection 1-form ω on the weight-space bundle W → W/G.
The horizontal subbundle ker(ω) is the space of fine-tuning directions that avoid holonomy
and forgetting. Every method claim (EWC, FILet, FOPNG, NGD) is described as an approximation
to projecting onto ker(ω).

**The degeneracy problem (GAP 1):**

The empirical FIM for a neural network layer is:
  F = E_{(x,y)~D}[ ∇_W log p(y|x,W) · ∇_W log p(y|x,W)^T ]

This is a sum of rank-1 outer products over N training examples. For the GGN/expected Fisher
(which uses model-predicted labels), if the parameter space has dimension d = m×n and we
compute F empirically with batch_size B, then rank(F) ≤ min(B × output_dim, d). For the
empirical Fisher (which uses observed labels, as in the standard SGD gradient), the tighter
bound is rank(F) ≤ B, since each example contributes one rank-1 term. Either way, the bound
is much smaller than d for typical configurations:

For typical transformer fine-tuning: B = 32, output_dim = vocab_size = 32,000 → rank(F) ≤
min(1,024,000, d). This is not tight — in practice, B × output_dim << d for large layers.

**Consequence:** ker(ω) is not a subbundle of TW in the vector-bundle sense. The rank of F
is not constant across the weight space — it can drop on measure-zero strata where gradients
become degenerate. A subbundle requires constant rank. Therefore, ker(ω) is a distribution
that is not everywhere of constant rank, making Theorem 3's bundle construction ill-defined
at those strata.

**This is a genuine mathematical gap.** It does not invalidate the geometric intuition, but
it means Theorem 3 as stated ("ker(ω) is the horizontal subbundle") requires either:
(a) restriction to a constant-rank stratum, or
(b) a regularized Fisher that is everywhere full-rank.

---

## Defense A: Constant-Rank Stratum Restriction

**The argument:**

Let W^reg ⊂ W be the set of weight configurations where F(W) has constant rank r_0. This is
a smooth submanifold of W (by the constant-rank theorem for smooth maps). On W^reg, the
distribution ker(F) is a smooth vector bundle of fiber dimension (d - r_0).

**Theorem 3 (revised):** On the constant-rank stratum W^reg, the Fisher FIM defines a
well-formed connection 1-form ω_reg. The horizontal subbundle ker(ω_reg) is a proper vector
bundle on W^reg. All theorem claims hold on W^reg.

**The question is whether W^reg is dense and whether fine-tuning trajectories stay in it.**

For neural networks after the first step of gradient descent (i.e., not at initialization),
the gradients almost certainly have full rank up to the B × output_dim bound. The singular
locus {W : rank(F) < r_0} has measure zero under any reasonable prior on data/parameters.

**Moral support from Tron & Fioresi (arXiv:2409.07412):**

Tron & Fioresi prove that the singular foliation on DATA space induced by the Data Information
Matrix has a measure-zero singular set. Their result applies to:
  - The Data Information Matrix (DIM) on data/activation space, NOT the FIM on weight space
  - ReLU networks specifically
  - The geometry of the data manifold, not the parameter manifold

This is an ANALOGY, not a proof of our claim. The moral: "singular sets are generically
measure-zero in information-geometric structures of neural networks" is plausible and
consistent with Tron-Fioresi, but our claim requires the argument applied to FIM on W, which
they do not prove.

**What this defense provides:**
- Theorem 3 holds on W^reg (dense, measure-zero complement)
- Fine-tuning trajectories that remain in W^reg have well-defined horizontal subbundle
- The restriction is standard practice in differential geometry (e.g., regular value theorem,
  constant-rank distributions)

**What this defense does NOT provide:**
- It does not prove fine-tuning trajectories stay in W^reg (they could pass through singular
  strata, especially at initialization or at saddle points)
- It does not tell us what happens exactly at singular points (no continuity guarantee for
  ker(ω) at rank-drop points)
- Tron-Fioresi cannot be cited as proving this for weight space

**Honest label:** Defense A is an ASSUMPTION, not a proof. It is the standard geometrical
move (restrict to regular stratum) and it is clean, but we must state explicitly in the paper
that we assume the fine-tuning trajectory remains in W^reg.

---

## Defense B: Tikhonov-Regularized Fisher

**The argument:**

Replace the empirical FIM F with:
  F_ε = F + ε · I_d

for small ε > 0 (Tikhonov / L2 regularization). F_ε is strictly positive definite for all ε
> 0, regardless of the rank of F. Therefore ker(F_ε) = {0} and the connection 1-form ω_ε is
well-defined everywhere on W.

The horizontal subbundle under F_ε is then:
  H_W = { v ∈ T_W W : ω_ε(v) = 0 } = span of eigenvectors of F_ε with eigenvalue ε

This is the span of directions in which F assigns zero Fisher information — in other words,
the nullspace of the original F. For small ε, this converges to ker(F) away from the singular
stratum, and is well-defined everywhere.

**Practical connection:**

EWC's λ plays an analogous regularization role: it penalizes deviation in high-Fisher
directions. However, EWC's λ multiplies the full quadratic penalty on F (acting on F itself,
not as Tikhonov damping of F^{-1}), so it is not precisely an F_ε = F + εI regularizer —
the effects on conditioning are related but distinct. NGD adds explicit Tikhonov damping
(F + εI)^{-1} for numerical stability. The point stands that regularized Fisher is standard
practice; the bundle construction formalizes what practitioners already implicitly assume.

**Theorem 3 (Tikhonov version):**
For any ε > 0, F_ε = F + εI defines a connection 1-form ω_ε that is smooth and well-defined
everywhere on W. In the limit ε → 0, ω_ε → ω on W^reg. The horizontal subbundle ker(ω_ε)
is a proper vector bundle on all of W for every ε > 0.

**What this defense provides:**
- Bundle construction is rigorous for all ε > 0 with no stratum restriction
- Directly corresponds to what EWC/NGD/FILet actually compute in practice
- Clean mathematical object: positive-definite metric → well-defined connection

**What this defense does NOT provide:**
- For ε → 0, the limit is only well-defined on W^reg (same problem as Defense A in the limit)
- The "correct" ε is not specified by theory; different ε give different horizontal subbundles,
  and the choice of ε affects which directions count as "horizontal"
- The physical meaning of "horizontal under F_ε" weakens as ε grows: large ε means almost all
  directions are treated as equally horizontal

**Honest label:** Defense B is rigorous for any fixed ε > 0. The bundle claim is clean. The
weakness is that the meaningful geometric claim (horizontal = Fisher-null) only recovers as
ε → 0, and the limit isn't better than Defense A.

---

## What Is NOT Resolved by Either Defense

Both defenses are mathematically acceptable for a theoretical paper. But two things remain
genuinely open:

**1. The fine-tuning trajectory question:**
Neither defense tells us whether the fine-tuning trajectory for LoRA (specifically, the
low-rank path in weight space) is generically in W^reg. If there are rank-drop events along
the path (e.g., during learning rate warm-up, or at loss saddle points), the horizontal
subbundle rotates discontinuously and the holonomy integral may not be well-defined. This is
a real dynamical question, not just a static geometry question.

**2. Fisher rank measurement in practice:**
We have not found a paper that measures the empirical rank of the FIM specifically for
transformer LoRA fine-tuning. The claim that rank(F) ≤ B × output_dim is a worst-case bound,
not a measurement. The actual rank may be much smaller (FIM is notorious for being
concentrated in a low-dimensional eigenspace; see Kunstner 2019, Kaur 2023 for general nets,
but not transformer LoRA specifically).

Papers found that do NOT resolve this:
- Tron & Fioresi (2409.07412): DIM on data space, not FIM on weight space
- Kristiadi (2302.07384): proves Fisher always present, rank not measured
- Biderman et al (2405.09673): rank of ΔW measured, not rank of FIM

A paper that would resolve this: "Eigenspectrum of the Fisher Information Matrix for
transformer LoRA fine-tuning across layers" — not found in the current corpus.

---

## Implications for Conjecture 2 (Holonomy-Intruder Correspondence)

Conjecture 2 states: intruder_dim_score ∝ ||Holonomy(training loop)||_Fisher

This conjecture requires a well-defined holonomy integral, which in turn requires the
horizontal subbundle to be well-defined along the training trajectory.

**Under Defense A (constant-rank stratum):**
If the LoRA trajectory stays in W^reg (ASSUMED), holonomy is well-defined. Conjecture 2 is
testable and the experiment (run_experiment.py) measures the relevant quantities.

**Under Defense B (Tikhonov):**
Holonomy is well-defined for any ε > 0. Conjecture 2 is testable in this regularized sense.
Note: run_experiment.py does NOT compute Procrustes alignment or Fisher-weighted distances.
It computes per-adapter SVD, cosine alignment between U_S* (top ΔW singular vectors) and
U_W₀ (top W₀ singular vectors), and intruder Frobenius energy. The principal angles between
U_S* and U_W₀ are closer in spirit to Steele's gradient-subspace angle (arXiv:2603.02224)
than to a holonomy integral. The experiment tests a proxy for holonomy (Steele-style angle),
not the holonomy integral itself.

**The key empirical test remains unchanged:**
The experiment tests whether intruder Frobenius energy correlates with a proxy for holonomy
magnitude (principal angle between task gradient subspaces, Steele 2603.02224). If the
correlation is strong, Conjecture 2 survives regardless of which defense we choose. If it is
weak, the conjecture fails.

**The Fisher degeneracy gap does not block the experiment. It affects how we interpret a
positive result.** A positive result is consistent with both defenses. A negative result
falsifies the conjecture independent of the Fisher gap.

---

## Summary Status Table

| Claim | Status | Requires |
|---|---|---|
| Theorem 1 (Spectral Decomposition) | Proved under assumptions | RMT + GL_r algebraic fact |
| Theorem 3 (Fisher Bundle) | Holds on W^reg (Defense A) or for F_ε (Defense B) | Either assumption explicit in paper |
| Conjecture 2 (Holonomy-Intruder) | Conditional on experiment | Trajectory in W^reg + experiment result |
| Conjecture 2b (Frob energy mediates forgetting) | Untested | run_experiment.py |
| Sheaf-Bundle Duality (Claim 8) | Conjecture | Rep-space↔weight-space isomorphism unproved |

---

## Paper Writing Implication

For the ICLR submission, Theorem 3 should be stated with Defense B (Tikhonov) as the primary
construction. This is the cleanest version: "For any ε > 0, the regularized Fisher F_ε = F + εI
defines a well-formed connection on W." Defense A (constant-rank stratum) is then mentioned in
a remark: "For the unregularized Fisher, the construction holds on the constant-rank stratum
W^reg, which is dense and where fine-tuning trajectories generically reside."

This is the honest, rigorous framing that a reviewer can verify.
