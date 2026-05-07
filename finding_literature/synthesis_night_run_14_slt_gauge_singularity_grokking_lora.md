# Synthesis 14: LoRA's Gauge Symmetry IS the SLT Singularity — A Direct Connection

**Date:** 2026-05-07
**Session:** 5
**Previous synthesis:** synthesis_night_run_13_hosvd_clt_holonomy_averaging.md

---

## The Missing Connection (12 hops → 1)

The graph has a 12-hop path from RLCT to GL(r) symmetry through indirect spectral theory links.
This synthesis collapses it to a DIRECT connection:

**LoRA's GL(r) reparameterization symmetry IS the singularity that Watanabe's Singular Learning Theory (SLT) was designed to analyze.**

---

## What SLT Says About Singular Models

Watanabe (2009, 2018): A statistical model is **singular** if the parameter-to-function map
is non-identifiable: there exist parameter pairs θ ≠ θ' such that the model function
p(x|θ) = p(x|θ') in a neighborhood. For singular models:

- RLCT < dim(parameter space)/2 (reduced effective complexity)
- Free energy: F_n ≈ RLCT × log(n) − (m-1) × log(log(n)) where m = multiplicity
- LLC (local learning coefficient) ≈ 2 × RLCT / log(n) — measurable in practice via SGLD
- **Competing basins arise when multiple low-RLCT solutions coexist near zero loss**
- Grokking = phase transition between competing basins (high-LLC memorization → low-LLC generalization)

## LoRA Is Singular

For LoRA with factorization ΔW = BA (B ∈ R^{m×r}, A ∈ R^{r×n}):

**Proposition:** LoRA is a singular statistical model.

**Proof sketch:** The GL(r) gauge group acts freely on the parameter space:
    (B, A) ~ (BG^{-1}, GA)  for any invertible G ∈ GL(r)
All points on the same orbit give the same ΔW = BA = (BG^{-1})(GA) = BA.
Therefore p(y|W_0 + BA) = p(y|W_0 + B'A') whenever (B,A) and (B',A') are on the same orbit.
The set of zero-loss solutions has the structure of a GL(r)-orbit manifold (a non-isolated
variety), which is exactly the "manifold of equivalent parameters" that defines SLT singularity. □

**RLCT of LoRA:** For a rank-r factorization of an m×n matrix:
    RLCT(LoRA, rank r) = r(m + n - r) / 2

This is the dimension of the manifold of rank-≤r matrices in R^{m×n}, divided by 2
(following Watanabe's formula for matrix factorization models).

At the task's intrinsic rank d_task:
    RLCT(generalization basin) = d_task(m + n - d_task) / 2

At the memorization rank r > d_task (with intruder dims):
    RLCT(memorization basin) = r(m + n - r) / 2

The generalization basin has **strictly lower RLCT** when d_task < r. This is the
mechanism for grokking: the generalization basin is entropically preferred in the Bayesian sense
(lower RLCT = lower effective complexity = higher model evidence for the same loss).

---

## Grokking = Transition From Intruder-Dim-Rich to Genuine-TRS-Only Basin

Combining SLT (competing basins) with TRS (spectral decomposition):

**Memorization basin** (high LLC, high RLCT):
- rank(ΔW) ≈ r (full LoRA rank, many intruder dims present)
- RLCT ≈ r(m+n-r)/2
- Fits training data via high-rank structure that includes W₀-misaligned intruder dims
- LLC is high: many effective parameters, complex solution

**Generalization basin** (low LLC, low RLCT):
- rank(ΔW) ≈ d_task (intrinsic task dimension, only genuine TRS)
- RLCT ≈ d_task(m+n-d_task)/2 << memorization basin RLCT when d_task << r
- Fits training data via low-rank structure aligned with W₀'s task-relevant directions
- LLC is low: few effective parameters, simple solution

**Grokking transition:** The model tunnels from the memorization basin to the generalization basin.
In spectral terms: the above-MP intruder dims gradually decay while genuine TRS directions
consolidate. The LLC curve (measurable via SGLD) drops at the grokking transition.

**Testable prediction:** For LoRA fine-tuning on algorithmic tasks (as in grokking experiments):
1. LLC computed via SGLD should drop at the grokking transition
2. The LLC before grokking ≈ 2 × r(m+n-r)/2n = r(m+n-r)/n
3. The LLC after grokking ≈ 2 × d_task(m+n-d_task)/2n = d_task(m+n-d_task)/n
4. The LLC ratio (before/after) ≈ r(m+n-r) / d_task(m+n-d_task) ≥ r/d_task > 1

This is a **quantitative prediction** for the LLC drop magnitude at grokking, in terms of the
LoRA rank r and the task intrinsic dimension d_task (measurable via GELoRA/TwoNN).

---

## W2T's Canonical Decomposition = Gauge Fixing = Removing the SLT Singularity

W2T (w2t_lora_weights_know_capabilities.pdf) uses QR+SVD to compute a canonical representative
of each GL(r) orbit:
    (B, A) ↦ canonical(B, A) = QR-SVD form that is unique per orbit

This is exactly **gauge fixing** in the fiber bundle sense: choosing one canonical element from
each GL(r) orbit. After gauge fixing:
- The non-identifiability is removed: canonical parameters → unique function
- The parameter space becomes (locally) the quotient manifold W/G
- The RLCT of the gauge-fixed model = dim(W/G)/2 = RLCT(LoRA) as computed above

**W2T's sigma-guided pooling** (weighting each rank component by its singular value σᵢ) is
then a TRS-weighted aggregation: high-σ (Region 1, universal fiber) components get high weight,
low-σ (Region 2/3) components get lower weight. This is the OPPOSITE of mtLoRA's spectral
regularization (mtLoRA downweights high-σ for orthogonalization), but both respect the same
spectral structure.

W2T's empirical success at predicting task capabilities from LoRA weights = empirical validation
that the gauge-fixed TRS spectrum contains the causal information about task capabilities.

---

## The Aristotelian vs Platonic Resolution

The aristotelian_platonic_hypothesis.pdf paper finds:
- The **Platonic Hypothesis** (all networks converge to one universal representation) is too strong
- Instead, only **topological/local neighborhood structure** converges across architectures
- Metric distances do NOT converge universally

In TRS terms, this is exactly right:
- **Region 1 (universal fiber, ~16 dims)**: metric convergence IS true here
  → the universal subspace IS universal (all models share it metrically)
  → this is the Platonic component
- **Region 2 (task-specific, above-MP)**: only topological alignment
  → task-specific directions are aligned up to permutation and rotation, not metrically
  → this is the Aristotelian component

The three-region decomposition RESOLVES the Platonic vs Aristotelian debate:
**Both are correct, at different scales of the TRS spectrum.**
The universal fiber (Region 1) is the Platonic subspace; the task-specific subspace (Region 2)
is Aristotelian. The CKA / RSA measures used in the paper measure Region 1 alignment (metric)
and find it, but it's small (16 dims out of thousands). The rest is Aristotelian (neighborhood-only).

---

## Synthesis: The Gauge Singularity Unifies Five Phenomena

The GL(r) gauge symmetry of LoRA is the single mathematical fact that unifies:

| Phenomenon | How GL(r) gauge symmetry explains it |
|-----------|---------------------------------------|
| Grokking | SLT: GL(r) singularity creates competing basins with different RLCT |
| Intruder dims | Extra rank beyond task intrinsic dim → GL(r) orbit degeneracy in wrong directions |
| W2T capability prediction | GL(r) gauge fixing (QR+SVD) = principal bundle section → canonical TRS spectrum |
| Universal fiber | GL(r)-invariant subspace across tasks = flat fiber directions (zero curvature) |
| Anti-grokking | RLCT increases again when rank exceeds d_task on long training → second singularity |

The gauge group is not a nuisance to be removed — it IS the organizing principle. Every
phenomenon in LoRA fine-tuning is a consequence of navigating the GL(r) gauge orbit structure.

---

## The Simplest Version

**LoRA has a symmetry (GL(r)). Symmetries create singularities. Singularities explain everything.**

- Why grokking: competing solution basins with different effective complexity (SLT)
- Why intruder dims: wrong-direction gauge orbit components above noise
- Why universal subspace: gauge-invariant directions shared by all tasks
- Why merging fails: averaging mixes gauge-non-equivalent components
- Why W2T works: gauge fixing reveals the canonical TRS structure

This is the unifying principle that connects SLT, TRS, GELoRA, W2T, Aristotelian/Platonic, and
the fiber bundle framework through a single mathematical object: the GL(r) gauge group.

---

## Open Questions

1. **Anti-grokking as second-order singularity?** Anti-grokking (synthesis 9: intruder dim saturation)
   happens when training continues past the generalization basin. In SLT terms: a second phase
   transition back to a higher-RLCT basin? Or a different mechanism (overfitting vs. intruder dims)?

2. **LLC measurement in LoRA fine-tuning:** Has anyone measured LLC via SGLD during LoRA fine-tuning?
   This is a direct experimental test of the SLT connection — LLC should drop at grokking transition
   with magnitude proportional to r - d_task. This appears to be completely unexplored.

3. **RLCT formula vs. empirical LLC:** The theoretical RLCT formula r(m+n-r)/2 assumes the worst-case
   singularity at full rank r. In practice, the early intruder dims may not be at full rank.
   Does the empirical LLC interpolate continuously between memorization and generalization basins?
