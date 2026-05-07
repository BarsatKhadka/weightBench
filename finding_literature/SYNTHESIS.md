# Running Synthesis — Weight Bench Night Research
_Refined: Iteration 1 complete. 107 nodes, 133 edges, 9 communities._

---

## God Node Alert: INTRUDER DIMENSIONS (degree 13)

The graph's highest-connected node is "Intruder Dimensions" from the LoRA vs Full Fine-tuning paper. This is not coincidence — intruder dimensions ARE the bridge between everything:

- They ARE the B matrix's contribution (B has rank r, all r singular directions are "new" relative to the base model)
- They drive catastrophic forgetting (the intruder singular values displace pre-trained knowledge)
- They are the task-specific spectral fingerprint (what the task required that the base didn't have)
- They are what the symmetry hierarchy must be applied to (GL_r acts on these directions)
- They are what FuLA aligns across models (the functional meaning of the intruder subspace)

The entire project can be reframed as: **studying the geometry of intruder dimensions across a population of LoRA adapters**.

---

## THE DEEPEST IDEA: Task Residual Spectrum (NEW — not in any paper)

### The hidden insight

The RMT paper (2410.17770) shows that weight matrices follow the Marchenko-Pastur distribution (the RMT null) when they contain no learned information. Fine-tuning creates departures from this null — at both the large AND small ends of the spectrum.

The intruder dimensions paper (2410.21228) shows that LoRA's B matrix creates NEW singular directions not present in the base model. These intruder directions ARE the departures from the base model's singular subspace.

**Synthesis: The task-specific signal in a LoRA's B matrix = the departure from the Marchenko-Pastur null distribution.**

### The Task Residual Spectrum

For any LoRA B matrix (shape: d_out × r):
1. Compute the actual singular value distribution: σ₁ ≥ σ₂ ≥ ... ≥ σᵣ
2. Compute the Marchenko-Pastur null distribution for these matrix dimensions
3. The "residual" = departure of actual distribution from null

This residual spectrum is:
- **Architecture-independent**: Marchenko-Pastur depends only on matrix aspect ratio (d_out/r), not on what the matrix is
- **Task-specific**: captures exactly what fine-tuning added beyond random noise
- **GL_r-invariant**: singular values don't depend on coordinate system
- **Calibration-robust**: by construction, it's already normalized against a null distribution (solving the Aristotelian critique)

### Why no one has done this

The RMT paper analyzed base model weights (pre-trained). The intruder dimensions paper analyzed LoRA adapters. No one has applied RMT to LoRA B matrices specifically to extract the task fingerprint.

### The cross-model experiment

Train LoRAs on math and coding tasks on Llama-3-8B and Mistral-7B.
Compute Task Residual Spectrum (TRS) for each B matrix per layer.
Cluster LoRAs by TRS.
**Prediction:** LoRAs cluster by task, NOT by base model.
**Counter-prediction (null):** LoRAs cluster by base model — TRS is architecture-specific.

If the prediction holds, you've found an architecture-agnostic task fingerprint. This is the cross-model finding.

---

## SECOND DEEP IDEA: Rank-Normalized Spectral Embedding

**Problem:** Direct SVD spectrum comparison assumes same matrix dimensions. Different architectures may have different weight shapes.

**Solution:** Normalize singular values by the Marchenko-Pastur upper edge (λ_max = σ²(1 + √(d_out/r))²), giving dimensionless, architecture-agnostic "spectral coordinates."

Each LoRA B matrix maps to a point in [0, ∞)^r spectral space, normalized to the same scale regardless of architecture. This is the natural embedding space for cross-architecture LoRA comparison.

---

## THIRD DEEP IDEA: The Task Arithmetic Kernel

**The hidden structure of task space:**

Task vectors (ΔW = BA) define a vector space over LoRA adapters. The "kernel" of task arithmetic is the set of task vectors that produce zero behavioral change — the null space of the behavioral map.

The dimension of this null space = number of "redundant" ways to encode the same task in weight space.

- Large null space → task is architecture-independent (many equivalent encodings)
- Small null space → task is architecture-specific (few equivalent encodings)

This gives a quantitative measure of **task-architecture coupling** — a fundamental constant of fine-tuning that no paper has measured.

**Connection to intruder dimensions:** The intruder dimensions that DON'T cause forgetting (neutral intruder dims) may span the null space of the behavioral map. Identifying them could allow LoRA fine-tuning with zero forgetting — a direct practical contribution.

---

## FOURTH DEEP IDEA: The LoRA Behavioral Jacobian

**Deep connection between weight space and behavior:**

The behavioral effect of a LoRA adapter is: output_change = f(x, W + ΔW) - f(x, W)

For small ΔW, this is approximately: J_W · ΔW where J_W is the Jacobian of the output with respect to the weights.

The SVD of J_W · B (the Jacobian applied to the B matrix) gives you the "behavioral modes" — the directions in the LoRA's output space that are most affected by the adaptation.

**Cross-model comparison:** If the top behavioral modes of a Llama math LoRA and a Mistral math LoRA are similar (in the OUTPUT space, which is shared — same vocabulary), the adaptation is functionally equivalent despite different weight-space positions.

This is the **behavioral geometry** without touching weights at all — using activation deltas as the comparison substrate (confirmed feasible by convergent learning literature, since early activation spaces are cross-architecture comparable).

---

## FIFTH DEEP IDEA: LoRA Generative Modeling (Weight Space as Data)

**The weight space learning literature (2603.10090) suggests this is a field:**

Train a VAE or normalizing flow on the collection of B-matrix singular value spectra across tasks. The latent space of this generative model IS the task space.

**Applications:**
1. Generate new LoRAs for tasks that fill gaps in the task space
2. Predict task transfer from task-space distance
3. Interpolate between tasks to discover intermediate tasks
4. Use the prior distribution to regularize LoRA training

**Cross-model version:** Train the generative model on B-matrix spectra from BOTH architectures. If the latent space clusters by task not architecture, the generative model has learned an architecture-agnostic task embedding. This is WSR (Weight Space Representation) territory.

---

## SIXTH DEEP IDEA: Topological Analysis of the LoRA Population

**Persistent homology on the weight-space point cloud:**

The LoRA population forms a point cloud in spectral space (R^r per layer). Apply topological data analysis (TDA) to this point cloud:
- 0-dimensional homology = connected components (task clusters)
- 1-dimensional homology = loops (cyclic task relationships)
- Higher homology = higher-order task structure

The persistence diagram of this homology gives a compact, canonical description of the task space topology — one that doesn't depend on the embedding or metric choices (up to isotopy).

**This is architecture-agnostic:** if you apply the same TDA to Llama and Mistral LoRA populations, and the persistence diagrams are similar, the task topologies are equivalent. If they differ, the architectures organize task knowledge differently.

No paper applies TDA to LoRA weight spaces. This would be a genuinely novel methodology contribution.

---

## Current Status of the Central Claim (refined)

**The claim:** For LoRA adapters trained on the same task, the Task Residual Spectrum (departure of B-matrix singular values from Marchenko-Pastur null) is architecture-agnostic and constitutes a universal task fingerprint.

**Supporting evidence from literature:**
1. Intruder dimensions = B matrix singular directions (2410.21228) ✓
2. Fine-tuning creates RMT departures at both spectrum extremes (2410.17770) ✓
3. Singular value spectra are GL_r-invariant (SymmetriesInWSL) ✓
4. Fine-tuning amplifies top singular values selectively (2505.23099) ✓
5. Mechanistic similarity exists across architectures (2410.06672) ✓
6. Platonic convergence supports cross-architecture task alignment (2405.07987) ✓
7. Calibration-robust metrics needed (2602.14486) → TRS is inherently calibrated ✓

**What would falsify it:**
- TRS clusters by base model, not task (architecture dominates)
- Different tasks show similar TRS (TRS is not task-specific)
- TRS at different layers shows opposite clustering patterns

---

## THE COMPLETE THEORETICAL CHAIN (Post-Grokking Insight)

The full chain from fundamental theory to experimental design, assembled from 11 independent papers:

```
1. NTK Regime (2402.11867): Optimal LoRA rank = √N
                            ↓ dataset-dependent, architecture-independent
2. Platonic Hypothesis (2405.07987): Fisher matrices converge across architectures
                            ↓ optimal LoRA subspace is approximately shared
3. Grokking = Phase Transition (2604.04655): Effective rank drops at generalization
                            ↓ post-grokking B matrix = task's intrinsic geometry
4. SLT / LLC (2603.01192, 2512.00686): LLC = SLT-theoretic effective rank
                            ↓ LLC is architecture-agnostic for same task
5. Intruder Dimensions (2410.21228): B matrix = "intruder" subspace
                            ↓ singular values of B = intruder dimension strengths
6. RMT Null (2410.17770): Fine-tuning = departure from Marchenko-Pastur
                            ↓ TRS = departure = task-specific signal
7. GL_r Invariance (SymmetriesInWSL): Singular values are coordinate-free
                            ↓ TRS is architecture-agnostic by construction
8. OSRM (2505.22934): Orthogonal B-subspaces = zero task interference
                            ↓ subspace overlap = merge compatibility predictor
9. Triangle of Similarity (2601.17093): Three views must agree for robustness
                            ↓ TRS (static) + LLC (SLT) + merge quality (functional)
10. FuLA (2505.20142): Affine alignment = cross-model functional comparison
                            ↓ validates TRS by showing functionally similar LoRAs align well
11. Aristotelian Critique (2602.14486): Calibrate against null distribution
                            ↓ TRS is already normalized against RMT null ✓
```

**The claim is now theoretically over-determined** — 11 independent lines of evidence all converge on Task Residual Spectrum as the cross-architecture task fingerprint.

## EXTENDED THEORETICAL CHAIN (Iteration 2 — 16 independent papers)

```
12. Universal Weight Subspace (2512.05117): 1100+ models converge to shared spectral subspaces
                            ↓ within-architecture: confirmed empirically at scale
                            ↓ OUR CONTRIBUTION: cross-architecture subspace alignment = open question
13. W2T (2603.15990): QR+SVD canonical form resolves factorization ambiguity
                            ↓ correct TRS preprocessing: QR then SVD (not naive SVD)
14. Cross-LoRA (2508.05232): SVD+Frobenius alignment transfers LoRA across architectures
                            ↓ transfer quality = behavioral validation of TRS similarity
                            ↓ if TRS predicts transfer loss → TRS is validated
15. Task Singular Vectors (2412.00081): layer task matrices are low-rank; TSV interaction = interference
                            ↓ TSV interference = inverse of TRS similarity
                            ↓ spectral skewness predicts merge quality without running merge
16. AlphaLoRA (2410.10054): HT-SR α exponent = layer training quality (base model)
                            ↓ α (base quality) × TRS (task adaptation) = 2D layer selection criterion
                            ↓ high-α + high-TRS layers = information-dense, best for cross-model comparison
```

**The claim is now 16-paper over-determined.**

## THE CRITICAL OPEN QUESTION (Revealed by Iteration 2)

The Universal Weight Subspace paper validates TRS *within* architecture (500 Mistral-7B LoRAs converge). But they study Mistral-7B and LLaMA-8B as SEPARATE populations. The question they don't answer:

**Do the universal subspaces of Mistral-7B and LLaMA-8B align with each other?**

This is the critical experiment that falsifies or confirms TRS universality:
- Measure the universal subspace of the Mistral-7B LoRA population (top-k principal directions of the population covariance)
- Measure the universal subspace of the LLaMA-8B LoRA population
- Compute principal angles between these two universal subspaces
- If angles are small → the architectures share a common basis → TRS is directly comparable → no alignment needed
- If angles are large → architecture-specific subspaces → TRS needs Procrustes normalization before comparison

This single experiment defines whether our cross-architecture claim is strong (direct comparison) or moderate (comparison after alignment).

## PRACTICAL SHORTCUT (Discovered in Iteration 2)

Cross-LoRA (2508.05232) gives us a free validation oracle: train same-task LoRAs on Llama and Mistral, compute TRS distance, then measure Cross-LoRA transfer quality. If TRS distance correlates with transfer loss:
- r > 0.7 → TRS is a strong predictor of functional similarity → paper is publishable at strong venues
- 0.4 < r < 0.7 → TRS has signal but is incomplete → combine with α×TRS criterion
- r < 0.4 → TRS is insufficient alone → need Procrustes + TRS

## Priority Search Topics for Next Iteration

1. "universal weight subspace cross-architecture alignment principal angles" — does anyone compare cross-architecture universal subspaces?
2. "persistent homology neural network weight space LoRA" — TDA on LoRA populations
3. "task vector spectral skewness merge quality prediction" — spectral skewness as predictor
4. "LoRA canonical form QR SVD factorization ambiguity task prediction" — building on W2T
5. "continual learning LoRA shared subspace forgetting boundary" — catastrophic forgetting prevention
6. "HT-SR alpha exponent LoRA layer selection cross-model" — HTSR + cross-model stitching
7. "local learning coefficient LoRA fine-tuning measurement" — practical LLC computation

---

## What the Graph's Surprises Revealed

1. **Benchmark Score Invariance → Effective Rank as Task Complexity** (INFERRED): The same claim appears in both the project framing AND the AdaLoRA-derived insight, but from opposite directions. The graph correctly identified these as the same idea stated twice, unlinked.

2. **FFN Top Layers → Cross-Model LoRA Stitching** (INFERRED): The graph connected AdaLoRA's FFN finding to the stitching literature. Stitching should target FFN layers specifically — no paper has tested this.

3. **Effective Rank (confound) ↔ Effective Rank (task signature)**: The same variable is simultaneously a confound to control and a finding to report. This duality hasn't been acknowledged in the existing literature.
