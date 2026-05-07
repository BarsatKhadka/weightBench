# Big Ideas — Autonomous Night Synthesis
_Refined: Iteration 2 complete. 207 nodes, 250 edges, 17 communities. 16 papers in theoretical chain. Last updated: night run._

---

## THE NEWTON INSIGHT: The Task Residual Spectrum as a Universal Constant

### The full chain (built from 7 independent papers)

```
Platonic Hypothesis (2405.07987)
  → Representations converge across architectures
  → J_output (Jacobian of predictions) is approximately architecture-agnostic
  
NTK Theory for LoRA (2402.11867)
  → Optimal LoRA rank = √N (N = training examples)
  → This is DATASET-dependent, ARCHITECTURE-independent
  
Fisher Information = NTK (in random feature regime)
  → Optimal LoRA subspace = top-√N eigenvectors of Fisher matrix
  → Fisher matrix is approximately shared across architectures (via Platonic)
  
Intruder Dimensions (2410.21228)
  → LoRA's B matrix = the "intruder" subspace (rank r new directions)
  → These intruder directions encode what the task required beyond the base model
  
Small Singular Values Matter (2410.17770)
  → Fine-tuning creates departures from Marchenko-Pastur at BOTH spectrum ends
  → The departure pattern = learned signal; RMT conforming part = noise
  
SymmetriesInWSL (from some-insights.md)
  → Singular values of B are GL_r-invariant
  → Architecture-agnostic coordinate system
  
Aristotelian Critique (2602.14486)
  → Any similarity metric must be calibrated against null distribution
  → RMT provides the exact null distribution (Marchenko-Pastur)
```

**Conclusion:** The TASK RESIDUAL SPECTRUM (TRS) — the departure of B-matrix singular values from the Marchenko-Pastur null — is:
1. Architecture-agnostic (calibrated against RMT null, GL_r-invariant)
2. Task-specific (encodes the task's cognitive complexity structure)
3. √N-bounded (NTK theory predicts the effective TRS rank)
4. Cross-paper convergent (7 independent papers support this)

**The singular claim:** The TRS is a **universal fingerprint of the task** — invariant under change of base model architecture.

---

## THE EXPERIMENTAL DESIGN THAT WOULD PROVE IT

### Setup
- 3 base models: Llama-3-8B, Mistral-7B, Qwen-2.5-7B
- 10 tasks: math, coding, summarization, translation, QA, reasoning, sentiment, NER, dialogue, classification
- 5 seeds per (model, task) pair → 3 × 10 × 5 = 150 LoRAs
- All at rank=16, same N per task

### Measurement (per LoRA B matrix, per layer)
1. Compute singular values σ₁ ≥ ... ≥ σ₁₆
2. Compute Marchenko-Pastur null for the matrix dimensions
3. TRS = log(σᵢ / λ_MP_edge) for each i — the log departure from null
4. Aggregate across layers using AdaLoRA importance weighting

### Test 1: Task clustering
- K-means with K=10 on TRS embeddings
- Metric: Adjusted Rand Index against task labels vs architecture labels
- **Prediction:** ARI(task) >> ARI(architecture)
- If ARI(task) > 0.7, claim is strongly supported

### Test 2: Effective rank universality
- Compute effective rank of TRS per task across architectures
- **Prediction:** effective rank clusters by task (same task → same effective rank across architectures)
- This directly tests the NTK prediction that optimal rank = f(N), not f(architecture)

### Test 3: NTK rank prediction
- Vary N (training size) for a fixed task
- **Prediction:** effective rank of B ∝ √N, regardless of architecture
- Plot (N, effective_rank) for Llama vs Mistral — lines should overlap

### Test 4: TRS predicts merge compatibility
- Compute TRS distance between all LoRA pairs
- Measure actual merge performance (task arithmetic)
- **Prediction:** TRS distance predicts merge quality better than raw weight distance or benchmark distance

---

## THE HIDDEN STRUCTURE: Why This Would Break the World

Current understanding: cross-architecture comparison requires alignment (CKA, stitching, Procrustes). These fail at shallow layers and are confounded by scale (Aristotelian critique).

Our claim: **no alignment needed for LoRA adapters**. The TRS is intrinsically normalized. You just compute it and compare.

This would mean:
1. Any LoRA on any architecture can be compared against any other LoRA on any other architecture for the same task
2. You can build a universal task library indexed by TRS — a "Dewey Decimal System for tasks"
3. Task transfer prediction across architectures becomes possible without retraining
4. LoRA merging compatibility prediction becomes architecture-agnostic

---

## ADDITIONAL DEEP IDEAS

### Idea 2: Model Tree Heritage in Reverse
The "Origin of Llamas" paper (2405.18432) recovers which base model a LoRA came from using weight-space signals. WE WANT THE OPPOSITE — identify which task a LoRA is doing, regardless of architecture. This is the inverse problem. If their method works in one direction, ours should work in the other, using TRS instead of raw weight features.

### Idea 3: Topological Task Space (TDA on TRS)
Apply persistent homology (zigzag persistence, paper 2410.11042) to the TRS point cloud. The persistence diagram of the task space is a canonical, topology-invariant description of how tasks relate to each other. This doesn't depend on metric choices. If the persistence diagrams match across architectures for the same task set, the task topology is universal.

### Idea 4: Fisher-NTK as the Unifying Theory
The Fisher information matrix at the base model defines the natural geometry of weight space. LoRA adapts in the top-r eigenvectors of this matrix. If the Fisher matrices of different architectures converge (Platonic hypothesis applied to Fisher geometry), the optimal LoRA subspaces converge, and the TRS convergence is explained theoretically, not just empirically.

**This would be a theorem:** If model A and model B have approximately equal Fisher information matrices (in a basis-independent sense), then for any task T trained on N examples, the TRS of LoRA_A(T) and LoRA_B(T) are approximately equal.

**The experimental test of the theorem:** Measure the alignment between Fisher matrices of Llama and Mistral. If high, TRS should converge. If low, TRS should diverge. This makes the claim falsifiable and theoretically grounded.

### Idea 5: LoRA as a Cognitive Operation Decomposition
Each singular direction of B with singular value σ_i represents a "cognitive operation" that the task requires. The σ_i encodes how strongly the task requires that operation.

If you could identify what each singular direction MEANS (by looking at which input features activate it), you'd have a decomposition of any task into primitive cognitive operations. The TRS is then the "cognitive operation histogram" of the task.

This connects to:
- Mechanistic interpretability (what circuits does the LoRA create?)
- Cognitive science (task decomposition into primitives)
- Multi-task learning (tasks that share singular directions can share adapters)

**The experiment:** For a math LoRA, look at the top-3 singular directions of B. Feed inputs that maximally activate each direction. Do they correspond to arithmetic, symbolic reasoning, number representation? If yes, the singular directions are interpretable cognitive operations.

### Idea 6: LoRA Spectral Genealogy
If you train LoRA on task A, then fine-tune that LoRA on task B, the resulting B matrix has a "spectral genealogy" — the old task's spectral structure is modified but not erased. You can see the history of tasks in the singular value spectrum.

This is the INVERSE of catastrophic forgetting — instead of asking what was forgotten, ask what remains. The TRS of a multi-task LoRA should be a superposition of the TRS of each constituent task. If you can deconvolve it, you can recover the task history. This is directly useful for model provenance and intellectual property.

### Idea 7: The Universality Threshold
Not all tasks have universal TRS. Tasks that require genuinely architecture-specific computation (e.g., tasks that exploit specific architectural biases of Llama vs Mistral) will have architecture-specific TRS. Tasks that require universal cognitive operations (math, language understanding) will have universal TRS.

This gives a TEST for architectural universality of a task: compute TRS variance within-architecture vs across-architecture. High within-architecture variance (seeds differ) + low across-architecture variance (architectures agree) = universal task. High across-architecture variance = architecture-specific task.

This is the "universality threshold" — a quantitative measure of how universal a task's cognitive requirements are.

---

## NEW IDEAS FROM ITERATION 2 (Night Run, May 2026)

### Idea 8: The Cross-LoRA Validation Oracle
Cross-LoRA (2508.05232) is a data-free LoRA transfer framework: it transfers LoRA adapters between different base model architectures using SVD subspace alignment. This gives us a FREE behavioral validation oracle for TRS.

**Protocol:**
1. Train same-task LoRAs on Llama-3-8B and Mistral-7B
2. Compute TRS distance between each LoRA pair
3. Run Cross-LoRA transfer: source=Llama LoRA, target=Mistral base → measure transfer quality (benchmark performance)
4. Correlation(TRS distance, transfer loss) is the falsification metric

If r > 0.7: TRS predicts cross-architecture functional similarity → publishable at strong venues
If 0.4 < r < 0.7: TRS has signal but needs augmentation (combine with α×TRS or subspace overlap)
If r < 0.4: TRS is insufficient → need Procrustes-normalized version

This is the cleanest single falsifiable test for the entire project.

### Idea 9: The 2D Layer Selection Map (α × TRS)
AlphaLoRA (2410.10054) measures the HT-SR power-law exponent α for each layer of the BASE model — this is a training quality score, architecture-agnostic, derived from the empirical spectral density.

TRS measures the LoRA's task adaptation strength per layer.

These two measures are ORTHOGONAL. Plotting them in 2D gives a layer selection map:
- α_high + TRS_high → "gold layers": well-trained base + strongly adapted → most task information
- α_high + TRS_low → "dormant layers": well-trained base + no task adaptation → skip
- α_low + TRS_high → "rescued layers": poorly-trained base + strongly adapted → LoRA compensated for bad base training
- α_low + TRS_low → "noise layers": bad base, no adaptation → definitely skip

For cross-model stitching: use ONLY gold layers (top quartile on both α and TRS). These are the layers where both models are well-trained AND both have strong task adaptation → maximal signal for cross-model comparison.

**No paper has proposed this 2D selection criterion.** It's directly derivable from two existing papers and addresses the layer selection problem in cross-model LoRA stitching.

### Idea 10: The Canonical TRS via W2T
W2T (2603.15990) shows that naive SVD of B has infinite factorization ambiguity — the same LoRA can have many different B matrices depending on how you split ΔW = BA. QR decomposition of B followed by SVD gives a canonical, unique representation.

**Critical implication for TRS**: If we compute TRS from naive SVD of B, we may be comparing arbitrary factorizations rather than canonical task representations. The QR+SVD canonical form should be the standard TRS computation procedure.

**New TRS definition (canonical):**
1. Given B (d_out × r), compute QR: B = QR where Q is orthogonal, R is upper triangular
2. Compute SVD of R: R = UΣV^T
3. TRS = log(σ_i / λ_MP_edge) for each singular value σ_i of R (not of B)

This resolves the factorization ambiguity that could otherwise make TRS comparison unreliable. W2T validates that this canonical form preserves task identity information.

### Idea 11: Universal Subspace as the TRS Prior
The Universal Weight Subspace Hypothesis (2512.05117) shows that 500 Mistral-7B LoRAs converge to a shared spectral subspace. This shared subspace IS the "universal prior" for LoRA adaptation on that architecture.

**Reframe TRS**: TRS is not just departure from the Marchenko-Pastur random matrix null — it's departure from the architecture-specific universal LoRA subspace.

Two-level departure:
- Level 1 (random null): departure from MP → removes noise
- Level 2 (architecture null): departure from the universal LoRA subspace → removes architecture-specific prior

The Level-2 TRS is what enables cross-architecture comparison: if both Llama and Mistral have architecture-specific priors, subtracting them leaves only task-specific signal.

**Experiment**: For a population of 500 Mistral-7B LoRAs on diverse tasks, compute the universal subspace (top-k PCA directions). For a population of 50 Llama-8B LoRAs, compute their universal subspace. If these two universal subspaces are aligned (small principal angles), then the universal prior is architecture-agnostic. If not, we need Level-2 normalization. This is a direct, measurable test.

---

## WHAT THE GRAPH REVEALED (17-community analysis, iteration 2)

Community structure shows:
- Communities 0, 4: LoRA spectral analysis (intruder dims + RMT)
- Community 1: Cross-model alignment (FuLA stitching)
- Communities 2, 3: The big ideas themselves (behavioral geometry + manifold/spectral fingerprint)
- Communities 5, 6: Metric calibration and symmetry-aware analysis
- Community 7: The original project framing (dual-signal)
- Community 8: Weight spectra adaptation geometry

**The god node is Intruder Dimensions (degree 13).** This confirms: the entire project converges on understanding what LoRA's B matrix ADDS to the base model — its structure, its universality, and its task-encoding capacity.

**Iteration 2 update:** TRS is now a co-god-node (degree 13). The graph has self-organized around the central claim. 17 communities, 207 nodes, 250 edges.

---

## PRIORITY SEARCH TOPICS FOR ITERATION 3

1. "universal weight subspace cross-architecture principal angles comparison" — do Llama/Mistral share universal subspaces?
2. "LoRA canonical form QR SVD task prediction retrieval" — W2T follow-on work
3. "task singular vectors cross-architecture interference prediction" — extending TSV (2412.00081) cross-model
4. "HT-SR alpha power law LoRA layer importance fine-tuning" — extending AlphaLoRA
5. "continual learning LoRA shared subspace catastrophic forgetting boundary" — spectral analysis of forgetting
6. "spectral skewness task vector model merging quality prediction" — skewness as merge predictor
7. "LoRA population manifold geometry clustering task identity" — manifold hypothesis for LoRA populations
8. "GrokLoRA grokking spectral transition" — grokking as spectral phase transition in B matrix
9. "local learning coefficient practical computation LoRA adapter" — how to measure LLC empirically
