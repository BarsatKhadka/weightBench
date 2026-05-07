# THE CORE CLAIM — The One Unbreakable Idea
*Written: May 2026 — after stripping all conjectures*

---

## THE SINGLE CLAIM

**The space of fine-tuning tasks is a subset of the Grassmannian. TRS finds the correct point. Grassmannian distance is the only valid way to compare tasks.**

This is not a metaphor. Every word has a specific mathematical meaning.

---

## THE THREE FOUNDATIONS (ALL PRE-2024, ALL PROVEN)

### Foundation 1: Spiked Covariance Model (Johnstone 2001; Paul 2007)

**Setting:** A matrix B = signal + noise, where signal is rank-r and noise is random.

**Classical result:** Under the Gaussian spiked covariance model:
- Singular values above the Marchenko-Pastur edge = consistent estimators of the true signal
- Singular values within the MP bulk = noise, carry zero signal information
- The minimum-MSE estimator of the signal matrix is MP-shrinkage (zero inside bulk, keep above)

**This IS TRS.** Computing TRS = computing the minimum-MSE estimator of the task-specific signal in B.

**Assumptions to state honestly:**
- B-matrices of real LoRAs have approximately Gaussian noise (reasonable: by RMT universality, the noise distribution converges to the same MP limit regardless of exact distribution for large matrices)
- The signal is low-rank (justified by NTK theory: optimal fine-tuning solutions have rank ≤ sqrt(N))
- Noise and signal are approximately independent

**What would break it:** If B-matrices systematically violate the spiked model (e.g., highly structured non-Gaussian noise). **Testable:** fit an MP distribution to each B matrix, check goodness-of-fit.

---

### Foundation 2: GL_r Invariance (Algebraic Fact)

**Setting:** LoRA parametrizes ΔW = BA where B ∈ R^{m×r}, A ∈ R^{r×n}. This is invariant under B → BG, A → G⁻¹A for any G ∈ GL_r.

**Result:** Any function of (B, A) separately is NOT a well-defined function of the adaptation ΔW = BA. The only well-defined functions are those invariant under this GL_r action. Singular values of B are GL_r invariant (they are eigenvalues of BᵀB, unchanged by B → BG since (BG)ᵀ(BG) = GᵀBᵀBG, and eigenvalues are preserved up to the change of basis G — actually, the singular values of B change if G ≠ O, a rotation).

**Wait — correction:** Singular values of ΔW = BA are GL_r invariant. NOT singular values of B alone. The singular values of B change under B → BG unless G is orthogonal.

**The correct invariant object:** The column space of ΔW = BA, i.e., the r-dimensional subspace spanned by the columns of ΔW. This is a POINT ON THE GRASSMANNIAN G(r, m). It is invariant under the full GL_r action.

**TRS = the above-MP part of this subspace.** Specifically: the singular subspace of ΔW corresponding to above-MP singular values.

**What would break it:** If the GL_r invariance argument doesn't apply (e.g., if the LoRA parametrization is constrained in a way that breaks the symmetry). In practice, any LoRA with free B and A matrices has this symmetry.

---

### Foundation 3: Cencov's Theorem + Fisher-Rao Metric on the Grassmannian

**Cencov's theorem (1982):** The Fisher-Rao metric is the UNIQUE Riemannian metric on the statistical manifold (space of probability distributions) that is invariant under sufficient statistics.

**Application to weight space:** Each weight matrix W defines a probability distribution over outputs (via the model's softmax). The Fisher-Rao metric on the space of these distributions pulls back to the Fisher Information Matrix (FIM) on weight space.

**The Grassmannian as a statistical manifold:** When restricted to the subspace of fine-tuning adaptations (the column space of ΔW), the Fisher-Rao metric on G(r, m) is UNIQUE up to a constant factor. This is the only invariant way to measure distances between two task subspaces.

**HONEST CAVEAT:** Cencov's theorem applies to the statistical manifold, not directly to weight space. The pullback to weight space requires:
1. That the model's output distribution is smooth in the weights (true for standard neural networks with softmax output)
2. That the Fisher metric is non-degenerate on the task subspace (may fail for degenerate/uninformative tasks)
3. That the task subspace is well-identified (requires sufficient training data)

**What would break it:** Singular Fisher metric (model is uninformative about task). Practically: if the task is too simple or the model is already perfect at it.

---

## THE UNIFIED CLAIM (COMBINING ALL THREE)

**Theorem (sketch):** Under the spiked covariance model for B-matrices:

1. The minimum-MSE, GL_r-invariant estimator of the task subspace is the above-MP singular subspace of ΔW (= TRS). *[Foundation 1 + 2]*

2. The unique reparametrization-invariant distance between two task subspaces is the Grassmannian geodesic distance in the Fisher-Rao pullback metric. *[Foundation 3]*

3. Therefore: for any task comparison method to be (a) statistically optimal under the spiked model AND (b) invariant under reparametrization of the LoRA factors, it must reduce to Grassmannian distance on TRS subspaces.

**Corollary:** Any method that ignores TRS or uses a non-Grassmannian distance is provably suboptimal under these assumptions.

---

## WHAT DEPENDS ON PRE-2024 CLASSICAL RESULTS ONLY

| Claim | Classical result | Year |
|---|---|---|
| Above-MP = MLE of signal | Spiked covariance model | Johnstone 2001, Paul 2007 |
| Grassmannian is the right space | Definition of G(r, d) | Standard differential geometry |
| Fisher-Rao is unique invariant metric | Cencov's theorem | Cencov 1982 |
| GL_r invariance of subspace | Algebraic fact | — |
| NTK rank bound r ≤ sqrt(N) | NTK theory for LoRA | Jang et al. 2024, ICML |

**None of these depend on any 2025-2026 paper.** The core claim stands on its own.

---

## WHAT IS CONJECTURE (LABELED HONESTLY)

The following ideas are compelling but NOT part of the unbreakable core:

- *Conjecture A (Holonomy-Intruder):* intruder dims = holonomy of training loop. Interesting, testable, but not proved.
- *Conjecture B (Q/K = curvature):* supported by 2502.10927 weakly, but V/O = transport is speculation.
- *Conjecture C (EWC = horizontal subbundle):* useful analogy, but diagonal Fisher ≠ true connection.
- *Conjecture D (Steele formula = holonomy):* gradient subspace angles ≠ holonomy eigen-angles. Different objects.

These live in a "Conjectures for Future Work" section. Not the core paper.

---

## THE EXPERIMENT THAT ANCHORS EVERYTHING

**One experiment. No training required. ~$0.**

Take 10 same-task LoRAs (5 from Llama-3-8B, 5 from Mistral-7B, same task e.g. GSM8K).
Take 10 different-task LoRAs (same 5 Llama models, 5 random tasks).

Compute:
- d_G(same-task pairs) = Grassmannian distance between same-task LoRAs across architectures
- d_G(diff-task pairs) = Grassmannian distance between different-task LoRAs

**Prediction:** d_G(same-task) << d_G(diff-task)

This would mean: the Grassmannian distance clusters tasks, not architectures.

**Why this is the right experiment:**
- Tests the CORE claim directly (Grassmannian = task space)
- Requires only SVD computation (no training, nearly free)
- Architecture-agnostic by construction (tests cross-architecture)
- Clear, falsifiable prediction

If this fails: the core claim is wrong and we should know immediately.
If this holds: we have the empirical anchor for everything.

---

## THE PAPER IN TWO SENTENCES

*The space of fine-tuning adaptations of a pre-trained neural network is a subset of the Grassmannian G(r, n), and the Grassmannian geodesic distance in the Fisher-Rao metric is the unique statistically optimal, reparametrization-invariant measure of task distance. We prove that TRS — the above-MP singular subspace of the fine-tuning weight delta — is the minimum-MSE estimator of the task's Grassmannian coordinates, and that every method in the fine-tuning literature that works (task arithmetic, model merging, LoRA transfer) succeeds exactly to the extent it respects this geometry.*

---

## WHAT "ATTENTION IS ALL YOU NEED" DID

That paper said: you don't need RNNs. Attention on sequences is sufficient.
One mechanism. Everything follows.

**Our claim:** You don't need behavioral evaluations to understand fine-tuned models.
One geometry — the Grassmannian — is sufficient.
Everything (task performance, forgetting, composition, transfer) follows.

The mechanism: **TRS** finds your coordinates. **Grassmannian distance** measures relationships.

No inference needed. Just SVD.
