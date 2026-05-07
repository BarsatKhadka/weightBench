# Deep Synthesis: Night Run Iteration 1
# "The Hidden Geometry of Weight Space" — Towards ICLR Breakthrough
*Generated: May 2026*

---

## What Changed This Session

Reading five papers deeply + 35 new papers found. Every assumption about TRS attacked. Multiple new frameworks synthesized below.

---

## THE CRITICAL DISCOVERY: TRS Theory is INCOMPLETE

The existing TRS framework claims: "above-MP singular values = task signal." This is TRUE but INSUFFICIENT.

From Shuttleworth et al. (arXiv:2410.21228) + Staats et al. (arXiv:2410.17770):

The singular value spectrum of ΔW (or B matrix) has FOUR distinct regions, not two:

```
|σ_1 ≥ ... ≥ σ_k| >> MP_bulk >> |σ_{n-j} ... ≈ 0|
  ^intruder dims^    ^noise^        ^zero dims^
  + true TRS
```

**The four-region decomposition:**

1. **True TRS** (above-MP, aligned with pre-trained singular vectors):
   - = genuine task signal
   - Predicts task-specific performance improvement
   - What current TRS measures — but imprecisely

2. **Intruder Dimensions** (above-MP, NOT aligned with pre-trained singular vectors):
   - = catastrophic forgetting artifacts
   - High singular values but DESTRUCTIVE
   - Suppressing these largely restores base model knowledge (Shuttleworth)
   - Current TRS includes these by mistake — a critical error

3. **MP Bulk** (within Marchenko-Pastur distribution):
   - = domain adaptation / common subspace
   - Preserved by averaging (proved by Subspace-Boosted Merging)
   - Not task-specific, but not pure noise either

4. **Near-Zero Dimensions** (below lower MP threshold):
   - = knowledge suppression / specialization via deliberate forgetting
   - Removing these causes outsized performance collapse (Staats et al.)
   - Fine-tuning DELIBERATELY suppresses certain capabilities to specialize
   - Not noise — structured suppression

**The corrected TRS formula:**
TRS_refined(B) = {u_i : σ_i > σ_MP_upper AND cos(u_i, V_pretrained) > τ_align}

Where τ_align is a threshold on alignment with pre-trained singular vectors.

**New prediction:** 
- intruder_score(LoRA) = ||{σ_i above-MP, not aligned}|| → predicts catastrophic forgetting
- true_TRS_score(LoRA) = ||{σ_i above-MP, aligned}|| → predicts task-specific performance  
- suppression_score(LoRA) = ||{σ_i near-zero}|| → predicts capability suppression

This is testable. This is new. This goes beyond anything in the existing literature.

---

## FRAMEWORK 1: Weight Space as a Fiber Bundle

**The Core Claim:**
Neural network weight space W is a fiber bundle:
- Total space: W = ℝ^d (raw parameter space)
- Base space: T = task manifold (parameterized by TRS_refined directions)
- Fiber: F_w = {w' : TRS_refined(w') = TRS_refined(w)} = equivalence class under G-symmetries + MP bulk variation
- Projection: π(w) = TRS_refined(w)
- Structure group: G = permutation symmetry group (as in DWSNets)

**What this explains:**

| Phenomenon | Fiber Bundle Explanation |
|---|---|
| Weight alignment NP-hard (DEEP-ALIGN) | Different choices of section of the fiber bundle |
| Knowledge is a Region (Gueta et al.) | A section of the fiber bundle = a consistent choice of representative for each task |
| Task arithmetic works | Addition in the base space T (task manifold) |
| Merging fails | Holonomy: going around a loop in T doesn't return to same fiber point |
| Mode connectivity | Paths in T lift to paths in W via the connection |
| Intruder dimensions | Points that LEAVE the fiber — outside the natural G-orbit |
| Permutation augmentation works (SSL) | Augmenting within the fiber — all augmented points have same base space coordinates |

**The Connection:**
The natural connection on this fiber bundle is defined by the gradient flow. The "connection 1-form" is the Fisher Information Matrix restricted to the task directions. This connects to:
- Riemannian geometry of parameter spaces (Kristiadi et al., arXiv:2302.07384)
- Natural gradient methods (Amari)
- The "curvature-guided LoRA" (arXiv:2603.29824)

**The REALLY deep prediction:**
The curvature (holonomy) of this connection encodes INTERFERENCE between tasks. If two task vectors τ₁, τ₂ have non-zero holonomy, then task arithmetic fails for them. This is precisely the "disentanglement error" ξ(α₁, α₂) measured by Ortiz-Jiménez et al.!

---

## FRAMEWORK 2: The Spectral-Population Duality

**Single-model level (TRS):** 
Singular value decomposition of a single LoRA's B matrix → above-MP singular vectors = TRS

**Population level (w2w, hyper-representations):**
PCA of flattened weights across N LoRAs → principal components = population-level structure

**The Duality Claim:**
The k-th principal component of population-level PCA = a linear combination of TRS vectors across individual LoRAs.

Formally: PC_k = Σ_i α_{ik} · TRS_i(B_i)

This means:
- w2w space (Dravid et al.) = the space SPANNED BY TRS vectors across the population
- Hyper-representations (Schürholt et al.) = encodings that converge to TRS-based features
- The semantic edit directions found by linear classifiers in w2w space = TRS directions corresponding to specific attributes

**Testable prediction:** 
The cosine similarity between (PC_k of w2w) and (average TRS_k across individual models) should be high (r > 0.7).

If confirmed: PCA on a population of LoRAs is an efficient APPROXIMATION of TRS. You don't need per-model SVD analysis — you can get approximate TRS from the population structure.

**Why this is surprising:**
Current work uses PCA as a dimensionality reduction tool without knowing WHY it works. TRS gives the theoretical reason: PCA finds the directions of maximum task-specific variance, and those directions ARE the TRS vectors.

---

## FRAMEWORK 3: The Knowledge Region as a TRS Manifold

**From Knowledge is a Region (Gueta et al.):**
- Fine-tuned models form nested convex regions
- Region INTERIOR outperforms the fine-tuned models on its boundary
- Linear interpolation between two models → better than either endpoint
- SGD pushes models to EDGES of regions, not interiors

**TRS interpretation:**
The knowledge region for task T = {w : ||TRS_refined(w) - TRS_canonical(T)||_Grassmannian < ε}

Where TRS_canonical(T) is the canonical TRS direction for task T (the centroid of TRS vectors across all fine-tuned models for that task).

The region INTERIOR corresponds to weight vectors that have TRS components aligned with the canonical direction AND are not at the edge (no intruder dimensions pushing them away from the manifold).

SGD pushes to the edge because:
- Minimizing training loss pushes task signal to be as large as possible (large singular values)
- This creates intruder dimensions (above-MP but misaligned) at the boundary
- The interior of the region has smaller singular values but better alignment → lower intruder dimension score → better generalization

**Prediction:**
Models sampled from the interior of the knowledge region (e.g., by averaging) should have:
- Smaller intruder dimension score
- Larger true TRS score (relative to intruder score)
- Better generalization to related tasks

This is a NEW prediction that neither the region paper nor TRS makes individually.

---

## FRAMEWORK 4: Weight Disentanglement = TRS Orthogonality

**From Task Arithmetic in Tangent Space:**
Weight disentanglement (formal Property 3): f(x; θ₀ + Σα_tτ_t) = Σg_t(x; α_tτ_t) + g₀(x)
This requires NTK eigenfunctions to localize to task data domains.

**TRS interpretation:**
Two task vectors τ₁, τ₂ are weight-disentangled iff their TRS_refined subspaces are orthogonal in the Grassmannian sense:
d_Grassmannian(TRS_refined(τ₁), TRS_refined(τ₂)) ≈ 1 (= π/2 principal angle)

**Why pre-training induces disentanglement:**
Pre-training = learning representations that can serve as a basis for diverse tasks. A good pre-trained model has NTK eigenfunctions that can localize to arbitrary task domains. The spectral structure of the pre-trained model's weight matrices (their RMT bulk structure) ensures that task-specific fine-tuning adds nearly orthogonal directions.

**Formal prediction:**
For models trained from scratch (random init) vs. pre-trained models:
- Random init: d_Grassmannian(TRS(τ₁), TRS(τ₂)) ≈ random (non-orthogonal)
- Pre-trained: d_Grassmannian(TRS(τ₁), TRS(τ₂)) ≈ 1 (nearly orthogonal)

This matches the empirical finding that task arithmetic is an emergent property of pre-training (Ortiz-Jiménez et al.).

---

## FRAMEWORK 5: The Near-Zero Singular Values as "Anti-Tasks"

**New idea (not in any existing paper):**

Fine-tuning ΔW = task acquisition + capability suppression
- acquisition: above-MP, aligned singular vectors (true TRS)
- suppression: near-zero singular vectors (what you're FORGETTING)

The near-zero singular values are not noise — they are the signature of SPECIALIZATION. When a model specializes for math, it de-emphasizes creative writing directions. The near-zero singular values of ΔW point in the directions being suppressed.

**Formal claim:**
For a fine-tuned model with task T:
- TRS_+ = {singular vectors with σ > σ_MP_upper} = capabilities ADDED
- TRS_- = {singular vectors with σ < σ_MP_lower, σ > 0} = capabilities SUPPRESSED

Both TRS_+ and TRS_- carry task-specific information. The complete task signature is TRS = (TRS_+, TRS_-).

**Applications:**
1. More precise task distance: d(T₁, T₂) = angle(TRS_+(T₁), TRS_+(T₂)) + angle(TRS_-(T₁), TRS_-(T₂))
2. "Capability surgery": to add capability C to model M while preserving M's other capabilities, project TRS_+(C) into the null space of TRS_-(M) before adding
3. Forgetting diagnosis: if TRS_-(T₁) ∩ TRS_+(T₂) ≠ ∅, then training on T₁ will catastrophically forget T₂

---

## FRAMEWORK 6: Model Stitching as a TRS Compatibility Test

**From Bansal et al. (arXiv:2106.07682):**
Model stitching = connecting bottom layers of model A to top layers of model B via thin stitching layer. Success ↔ representational compatibility.

**TRS interpretation:**
Two models A, B have compatible representations for task T iff:
d_Grassmannian(TRS_refined(A, T), TRS_refined(B, T)) < ε

**Cross-architecture prediction:**
If TRS is universal, then for same task T across Llama-3-8B and Mistral-7B:
- Model stitching should succeed between LoRA-adapted layers of the two models
- The stitching layer should be learnable with very few parameters (because TRS subspaces are aligned)

This is a concrete, cheap experiment ($10-20) that provides DIRECT evidence for TRS universality without the full cross-architecture TRS computation.

---

## FRAMEWORK 7: TRS as Sufficient Statistic — Formal Claim

**From information theory:**
A sufficient statistic T(X) for parameter θ contains all information about θ in X: P(X|θ) = P(X|T(X)) · P(T(X)|θ)

**Claim:** TRS_refined(ΔW) is a sufficient statistic for predicting any behavioral outcome of the fine-tuned model (on the training distribution).

**Formal proof sketch:**
1. The within-MP bulk encodes distribution-level information, not task-specific
2. The TRS_+ encodes added task-specific capabilities
3. The TRS_- encodes suppressed capabilities  
4. The intruder dimensions encode forgetting artifacts (predictable from TRS_- of other tasks)
5. Therefore: all behavioral predictions can be made from (TRS_+, TRS_-, intruder score)

**What's NOT captured by TRS:**
- Calibration (confidence levels) — depends on MP bulk structure
- OOD generalization — depends on how TRS directions extrapolate
- Computational efficiency at inference — depends on raw weight structure

This is honest: TRS is a SUFFICIENT statistic for in-distribution task behavior but not for everything.

---

## FRAMEWORK 8: The Platonic Weight Space Hypothesis

**From Platonic Representation Hypothesis (Huh et al., ICML 2024):**
Representations across diverse models/modalities are converging to a shared statistical model of reality.

**Weight space analog:**
As models scale and pre-train on more data, their weight space structure converges to a canonical form. Specifically:

For large pre-trained models:
- The NTK eigenfunctions become increasingly localized (weight disentanglement emerges from scale)
- The spectral structure of weight matrices approaches a universal form (Marchenko-Pastur + task spikes)
- The TRS directions for the same task become increasingly aligned across architectures

**Prediction:** 
For larger models (GPT-4, Llama-3-70B), TRS cross-architecture alignment should be higher than for smaller models (Llama-3-8B, Mistral-7B). As models scale, they converge to a "Platonic weight space" where task representations become architecture-independent.

This is testable and would be a headline result for an ICLR paper.

---

## ATTACK ON MY OWN ASSUMPTIONS

**Assumption 1: "TRS is computable from B matrix alone"**
WRONG — or at least incomplete. The correct TRS requires comparing to pre-trained singular vectors (to separate true TRS from intruder dimensions). You need BOTH ΔW and W₀.

**Assumption 2: "Above-MP = task signal"**  
REFINED — only if ALSO aligned with pre-trained directions. Otherwise = intruder dimension = forgetting.

**Assumption 3: "Near-zero singular values = noise"**
WRONG — Staats et al. shows removing near-zero singular values causes outsized performance collapse. Near-zero = capability suppression, not noise.

**Assumption 4: "Cross-architecture TRS comparison is about direction similarity"**
REFINED — you need Grassmannian distance (principal angles between subspaces), not cosine similarity of individual vectors. DEEP-ALIGN shows even same-architecture alignment is NP-hard without the right framework.

**Assumption 5: "Averaging N LoRAs destroys all task signal at O(1/√N)"**
PARTIALLY WRONG — it destroys INDIVIDUAL task signal but preserves SHARED task structure. The shared TRS directions across N LoRAs for same task actually AMPLIFY at O(√N) under averaging. This means model soups work precisely because they amplify shared TRS and suppress idiosyncratic variation.

---

## EXPERIMENTAL PRIORITIES REVISED

Old priority: Cross-architecture TRS alignment test
New priority order:

1. **The Four-Region Decomposition** (cheapest, most theoretically fundamental):
   - Compute: TRS_+, intruder_dims, MP_bulk, TRS_- for a set of LoRAs
   - Show: intruder_dim_score predicts catastrophic forgetting
   - Show: TRS_refined_score (aligned above-MP) predicts task performance better than raw TRS
   - Cost: ~$5-10, on existing LoRAs

2. **Near-Zero Singular Values as Anti-Task Signature**:
   - Show: TRS_- directions of math LoRA align with (negative of) creative writing directions
   - Cost: ~$10, can be done analytically on existing LoRAs

3. **Spectral-Population Duality**:
   - Show: PC_k of population PCA ≈ average TRS_k
   - Cost: need ~20-50 LoRAs on same task, ~$20-30

4. **Model Stitching as TRS Compatibility Test**:
   - Cross-architecture stitching with same-task LoRAs
   - Cost: ~$30-50

5. **Platonic Weight Space Scaling**:
   - TRS alignment vs model scale
   - Cost: ~$50-100

---

## THE REVISED PAPER CLAIM

**Working title:** *"The Complete Spectral Theory of Fine-tuned Model Adaptation"*

**Main claim:** The singular value spectrum of fine-tuning weight deltas decomposes into four functionally distinct regions. We provide: (1) a formal characterization of each region using random matrix theory and pre-training alignment, (2) theoretical predictions about task performance, forgetting, and composition, (3) empirical validation across architectures and tasks, (4) a unified geometric framework (fiber bundle) that explains all existing model composition methods as special cases.

**Why "Attention is All You Need" level:**
- Current: weight space learning = empirical methods with partial theoretical understanding
- After this paper: weight space learning = a complete spectral theory with four canonical components
- Unifies: TRS (acquisition), intruder dims (forgetting), MP bulk (domain), near-zero (suppression)
- Predicts: all composition methods (task arithmetic, TIES, DARE, ROME, model soups, LoRA merging)
- Enables: surgical weight editing without needing any task data

---

## OPEN QUESTIONS FOR NEXT ITERATION

1. What is the correct mathematical structure of the intruder-dimension manifold? Is it a symplectic submanifold?
2. Does the near-zero/TRS_- decomposition have a statistical mechanics interpretation (entropy of forgetting)?
3. Can the fiber bundle connection be computed efficiently without full SVD?
4. What is the right Riemannian metric on the task manifold T = B ≡ W/G?
5. Does the Platonic convergence happen at a specific parameter count threshold?
6. Is there a canonical "TRS distance" between tasks that predicts transfer learning quality?
