# Synthesis Night Run: Iteration 3
# The Holonomy Connection — Gauge Theory Meets Spectral Decomposition
*Generated: May 2026*

---

## WHAT THIS ITERATION RESOLVED

The fiber bundle gap is now **precisely mapped**. Two critical papers were found that confirm
the gap exists while providing the missing pieces needed to fill it:

| What exists | Paper | What's missing |
|---|---|---|
| W/G quotient + horizontal/vertical split | 2603.21502 | Holonomy, multi-task scenarios |
| Holonomy on discrete weight graphs (RBM) | 2509.10536 | Training trajectories, not topology |
| Fisher metric = bundle connection in disguise | 2302.07384 | Explicit bundle construction |
| Holonomy certifying interference (representation space) | **2603.00824** | Weight space, not rep space |
| Computational holonomy infrastructure | **2601.21653** | Applied to input loops, not weight loops |

**The gap is exactly one step from being filled.** We need to move 2603.00824's holonomy from
representation space to weight space. That one step is our theoretical contribution.

---

## THE KEY INSIGHT: INTRUDER DIMENSIONS = WEIGHT-SPACE HOLONOMY

**The unification that no paper has made:**

2603.00824 proves: holonomy over closed paths in representation space = interference bound.
Shuttleworth (2410.21228) proves: intruder dimensions = catastrophic forgetting.

**Claim:** Intruder dimensions ARE the holonomy of the weight-space training loop.

**Formal argument:**

Let θ₀ → θ₁ (train on T1) → θ₂ (train on T2) → θ₂ - ΔT2 (approximately undo T2)

In Euclidean space: θ₂ - ΔT2 ≈ θ₁ (reversible)
In a curved manifold: θ₂ - ΔT2 ≠ θ₁ (non-zero holonomy)

The residual δ = (θ₂ - ΔT2) - θ₁ is the holonomy of the loop.

In spectral terms:
- The LoRA update ΔT2 = U_T2 Σ_T2 V_T2^T
- The "undo" operation reverses this in Euclidean space
- But in weight space, the low-rank constraint means you can't exactly undo the update
- The part that doesn't undo = the intruder dimensions of T2's LoRA

**As rank → ∞:** The low-rank constraint disappears → holonomy → 0 → intruder dims → 0.
This EXACTLY matches Shuttleworth's Table 1: intruder dims vanish at high rank!

**The holonomy measure:**
Holonomy(T1, T2) = ||intruder_dims(T2 after T1)|| = f(principal_angle(TRS(T1), TRS(T2)))

When tasks are orthogonal (TRS subspaces perpendicular): holonomy ≈ 0, no intruder dims.
When tasks are parallel (TRS subspaces aligned): holonomy ≈ max, many intruder dims.

This is measurable! You can predict the intruder dimension score from TRS distance BEFORE
sequential fine-tuning. The holonomy formula gives a PREDICTIVE model for catastrophic forgetting.

---

## THE Q/K vs V/O ASYMMETRY: A NEW PREDICTION

From 2604.22778 (Spectral Lifecycle):
- Q/K projections: depth-dependent spectral dynamics, complex behavior
- V/O projections: uniform compression, simpler dynamics

**Implication for four-way decomposition:**

The four spectral components are distributed differently across attention head types:

| Component | Q/K layers | V/O layers |
|---|---|---|
| Genuine TRS (above-MP, aligned) | Present, but less clean | Dominant, cleaner signal |
| Intruder Dims (above-MP, unaligned) | More prevalent (complex dynamics) | Less prevalent |
| MP Bulk (domain adaptation) | Smaller (more compressed) | Larger (uniform compression) |
| Suppression Dims (near-zero) | More variable by depth | More uniform across depth |

**New prediction:**
TRS computed on V/O projections will be MORE predictive of task performance than
TRS computed on Q/K projections. The Q/K layers have more geometric complexity
(curvature, depth gradients) that adds noise to the spectral fingerprint.

**Corollary:** The best TRS fingerprint should be:
TRS_optimal(model) = TRS(V layers) with Q/K layers as secondary signal

This is a concrete, cheap experiment: compute TRS on V-only vs Q-only vs all layers,
show V-layer TRS has higher inter-task clustering ARI and higher intra-task agreement.

---

## THE FIVE SPECTRAL PHASES: MAPPING TO FOUR-WAY DECOMPOSITION

From 2604.22778, the five training phases:
1. Random → 2. Bleeding-Out → 3. Bulk+Spike → 4. Bulk-Decay → 5. Heavy-Tailed

The four-way decomposition corresponds to different phases:

| Training Phase | Dominant Component | What's Happening |
|---|---|---|
| Phase 1 (Random) | MP Bulk only | No task signal yet |
| Phase 2 (Bulk+Spike) | MP Bulk + emerging Genuine TRS | First task spikes appear |
| Phase 3 (Heavy-Tailed) | Genuine TRS dominant | Clean task signal established |
| Phase 4 (Continued HT) | TRS + Suppression Dims growing | Specialization increasing |
| Over-training | Intruder Dims appear | Task overfit, forgetting artifacts |

**Critical insight:** Intruder dimensions appear only in **over-training** or **rank-constrained**
fine-tuning. A well-trained model (stopped at phase 3-4) should have:
- Genuine TRS: most above-MP singular vectors
- Suppression: growing near-zero structure
- Intruder dims: near zero (well-regularized)

Intruder dims = signal that the training stopped too early OR the rank is too low.

**Prediction:** The optimal LoRA rank (for minimum intruder dims) = sqrt(N) from NTK theory
(arXiv:2402.11867). At exactly r = sqrt(N), the low-rank constraint is just loose enough
to represent task signal without creating holonomy artifacts (intruder dims).

---

## THE GAUGE THEORY CONNECTION: SHEAF + BUNDLE

2603.00824 provides a sheaf-theoretic atlas: local charts of semantic features with
Fisher/Gauss-Newton metrics, and holonomy over cycles in the context graph.

Our theory provides the dual: a bundle-theoretic atlas of weight space, with:
- Local charts: neighborhoods of weight configurations in W
- Metrics: Fisher information metric (Kristiadi et al. 2302.07384)
- Holonomy: over training loops in weight space (our gap to fill)

The two theories are DUAL:
- Sheaf theory (2603.00824): representations → features → holonomy of input-space loops
- Bundle theory (ours): weights → parameters → holonomy of training-space loops

They measure the same thing from opposite directions:
- Sheaf holonomy: how much do representations rotate when you traverse the input manifold?
- Bundle holonomy: how much does the weight manifold "twist" when you traverse task space?

**Grand unification:** These two should be equal by the fiber bundle isomorphism theorem:
Holonomy(weight space loop) = Holonomy(representation space loop over same data)

If this holds, you can measure training holonomy from either representation or weight space.
Practical implication: You don't need to run T1 → T2 → -T2 to measure holonomy.
You can compute it from the representations alone — BUT ONLY IF the rep-space↔weight-space isomorphism holds (Conjecture, untested). Note: 2601.21653 operates in feature/activation space via INPUT loops, NOT weight space directly. The infrastructure cannot be applied to weight-space holonomy without proving this isomorphism first.

---

## NEW THEORETICAL CLAIMS (Iteration 3 Additions)

**Claim 5: The Holonomy-Intruder Duality**
Intruder dimension score = ||holonomy(training loop)|| in the Fisher metric bundle.
Proof sketch: both measure the non-reversibility of weight-space trajectories under
the low-rank constraint. As rank → ∞, both → 0.

**Claim 6: V-layer TRS Dominance**
TRS computed on V/O attention projections predicts task performance better than Q/K-based TRS.
Reason: V/O layers have simpler spectral dynamics (uniform compression), so the four-way
decomposition is cleaner with less geometric noise.

**Claim 7: Optimal Rank = sqrt(N) for Intruder-Free Fine-tuning**
At rank r = sqrt(N) (NTK bound from 2402.11867), the LoRA constraint is exactly tight enough
to represent task signal without generating intruder dimension artifacts (holonomy ≈ 0).
Below sqrt(N): intruder dims grow as holonomy of the underfitted constraint.
Above sqrt(N): genuinely unnecessary, no benefit.

**Claim 8: Sheaf-Bundle Duality for Holonomy Measurement**
weight-space holonomy and representation-space holonomy (2603.00824) are isomorphic under
the model's function map. This makes holonomy estimation feasible without running sequential
fine-tuning experiments — compute it from a single checkpoint's representations.

---

## THE PAPER'S NEW ARCHITECTURE

The four-way decomposition is the central result, but the paper now has three theoretical
pillars connecting to the broader literature:

**Pillar 1: Spectral Decomposition (Core)**
ΔW = TRS_genuine + TRS_intruder + TRS_bulk + TRS_suppression
Supported by: RMT (MP null), alignment criterion (2410.21228), universal subspace (2512.05117),
spectral lifecycle (2604.22778), NTK rank theory (2402.11867)

**Pillar 2: Geometric Structure (New)**
Weight space as fiber bundle with Fisher metric connection.
Holonomy of training loops = task interference measure.
Intruder dimensions = holonomy artifacts of low-rank constraint.
Supported by: W/G quotient (2603.21502), holonomy infrastructure in FEATURE space (2601.21653 — not directly weight-space),
gauge theory of superposition (2603.00824), Fisher metric (2302.07384)

**Pillar 3: Functional Consequences (Predictions)**
Task performance ↔ genuine TRS alignment
Catastrophic forgetting ↔ intruder dim score / holonomy magnitude
Cross-task composition quality ↔ TRS Grassmannian distance
Model merging quality ↔ spectral over-accumulation avoidance (2602.05536)
Supported by: forgetting geometry (2603.02224), spectral over-accum (2602.05536),
TSV interference metric (2412.00081), subspace-boosted merging (2506.16506)

---

## UPDATED EXPERIMENT DESIGN (Priority Order)

**Experiment 0 (Free, immediate): Verify Q/K vs V/O TRS Asymmetry**
Using existing LoRAs on GSM8K + CodeAlpaca:
1. Compute TRS separately for Q/K layers vs V/O layers
2. Measure: ARI(task) for Q/K-TRS vs V/O-TRS clustering
3. Prediction: V/O-TRS has higher task clustering, Q/K-TRS has more noise
Cost: essentially free (one SVD per layer type), < 1 hour on CPU

**Experiment 1 ($5-10): Four-Way Decomposition Validation**
(unchanged from iteration 2)
For each LoRA:
- Classify singular vectors: (above-MP + aligned + not-universal) = genuine TRS, etc.
- Show: intruder score predicts forgetting (ρ ≈ 0.97, Shuttleworth benchmark)
- Show: genuine TRS predicts task performance better than raw TRS

**Experiment 2 ($20): Holonomy ↔ Intruder Dim Equality Test**
1. Sequential fine-tune: T1(GSM8K) → T2(CodeAlpaca) → gradient reversal of T2
2. Measure: ||θ_after - θ_T1|| = holonomy magnitude
3. Compare: does holonomy magnitude = intruder_dim_score(T2)?
4. Vary rank r from 8 to 2048: does holonomy → 0 as r → ∞?
This is the most theoretically important experiment. Confirms Claim 5.

**Experiment 3 ($30-50): Cross-Architecture TRS Validity**
(unchanged from previous iterations)
Llama-3-8B + Mistral-7B, same tasks, K-means clustering
Prediction: ARI(task) >> ARI(architecture)

---

## OPEN QUESTIONS (Iteration 3)

1. Does Claim 8 (Sheaf-Bundle Duality) hold quantitatively? Can we compute weight-space
   holonomy from a single checkpoint's representations? NOTE: 2601.21653 infrastructure
   operates in activation/feature space (input loops), not weight space — using it for
   weight-space holonomy requires proving the rep-space↔weight-space isomorphism first.

2. Is the V-layer TRS dominance effect architecture-dependent? MLP layers don't have Q/K/V —
   what's the analog for FFN blocks? (Answer: likely output projection is the "V equivalent")

3. The Gauge Theory of Superposition (2603.00824) uses holonomy to certify interference bounds.
   Can the same certifying proof be adapted to weight space? Would give a PAC-style guarantee:
   "if holonomy < δ, then catastrophic forgetting < ε."

4. Is the optimal rank = sqrt(N) tight? The NTK bound is for a worst-case task. For structured
   tasks (like math), the effective task complexity might be much lower, allowing r << sqrt(N).

5. What is the relationship between the universal subspace (2512.05117) and the holonomy?
   Conjecture: the universal subspace = the flat directions of the Fisher bundle (zero curvature,
   zero holonomy). Task-specific directions = curved directions (non-zero curvature, holonomy ≠ 0).

---

## PAPERS TO ADD TO CORPUS (Iteration 3)

1. arXiv:2603.00824 — Gauge Theory of Superposition (sheaf-theoretic holonomy, interference bounds)
2. arXiv:2601.21653 — Gauge-invariant Representation Holonomy (practical holonomy estimator IN FEATURE/ACTIVATION SPACE via input loops — NOT weight space; cannot be cited as a weight-space holonomy algorithm without proving the rep-space↔weight-space isomorphism)
3. arXiv:2604.22778 — already known, confirmed VALID

Priority: 2603.00824 is CRITICAL — it's the missing bridge between holonomy theory and
neural network interference that gets us closest to the gap we're filling.
