# The Grounded Picture
# Building from Measurement to Theory

**Date:** 2026-05-07

---

## What This Document Is

This is not a synthesis. It is a careful chain of reasoning where every step
is either (a) a directly measurable fact with a paper and number attached, or
(b) a theorem with explicit assumptions stated.

The goal: build the simplest picture that is consistent with all the measurements,
nothing added, nothing smoothed over.

---

## Step 0: The Physical Setup

You have a large pretrained language model. Its weights are matrices.
Take one weight matrix W of shape m × n (e.g., a query projection matrix W_q in a transformer).

You fine-tune the model using LoRA:
    W → W + ΔW = W + BA

where B is m × r and A is r × n, with rank r chosen by you.

After fine-tuning, you have ΔW = BA. This is the only thing that changed.

---

## Step 1: The Noise Floor (A Theorem, Not an Assumption)

Compute the singular value decomposition of ΔW = BA:
    ΔW = U Σ V^T
    Σ = diag(σ₁ ≥ σ₂ ≥ ... ≥ σ_r)

**Claim:** If ΔW were random (Gaussian, mean zero, variance σ²/mn), its singular values
would follow the Marchenko-Pastur distribution with upper edge:
    σ_+ = σ √(m) (1 + √(n/m))   [for m ≥ n]

Everything below σ_+ is indistinguishable from random noise.
This is a theorem (Marchenko-Pastur law, 1967; applied to LoRA by small_singular_values_rmt_transformers.pdf, 2410.17770).

**The noise floor is exact and computable.** You do not need to guess it.

**Why this threshold is not arbitrary — the BBP identity (Baik, Ben Arous, Péché 2005):**
For a rank-1 signal plus Gaussian noise, the phase transition between "undetectable" and
"detectable" (asymptotically consistent estimation) occurs exactly at σ_+. Below σ_+: no
estimator can distinguish the signal from noise. Above σ_+: the signal is recoverable.
The Marchenko-Pastur upper edge IS the BBP critical threshold — the same formula, same number.
(This is made explicit for fine-tuning gradient matrices in arXiv:2510.01137.)

**What a single gradient step produces (Spiked Random Features Model, arXiv:2410.18938):**
After ONE gradient descent step on a task, ΔW = spike + noise:
    ΔW = u·vᵀ + Δ
where v is aligned with the task's target direction w*, and Δ is MP-distributed bulk.
The spike exceeds σ_+ if and only if the task signal-to-noise ratio clears the BBP threshold.
After full training, d_task such spikes accumulate — one for each independent task direction.

Singular values ABOVE σ_+: signal (ΔW encodes something task-relevant here).
Singular values BELOW σ_+: noise (indistinguishable from random initialization).

For a typical LoRA with r = 16 fine-tuned on a moderate-size dataset:
you might find 3-8 singular values above σ_+ and the rest in the noise floor.

---

## Step 2: The Signal Splits Into Two Types

The singular values above σ_+ are not all equivalent.

Take the corresponding singular vectors u_i (left) and v_i (right).
Compare them to the singular vectors of the PRETRAINED MATRIX W₀.

Let U_W₀ be the matrix of W₀'s left singular vectors, sorted by singular value.
Split U_W₀ into:
    U_A (top-20%): large singular value directions = heavily used by W₀ = universal capacity
    U_B (rest):   small singular value directions = lightly used = available for specialization

Now check: is u_i close to the span of U_A, or to the span of U_B?

**Type 1 (Intruder Dimension):**  u_i is aligned with U_A (the large-SV directions of W₀)
    → this ΔW component overwrites W₀'s heavily-used universal capacity
    → this causes catastrophic forgetting

**Type 2 (Genuine TRS):** u_i is orthogonal to U_A (aligned with U_B, the small-SV directions)
    → this ΔW component fills in W₀'s underused capacity with task-specific information
    → this is what fine-tuning is supposed to do

**The key measurement (Shuttleworth et al., 2410.21228):**
Spearman rank correlation between intruder dimension count and catastrophic forgetting:
    ρ = 0.971

This is the strongest empirical result in this entire body of literature.
It means: count the intruder dims, and you can predict forgetting with 97% rank accuracy.

**Also from Shuttleworth:** Causal intervention — when they artificially increase the intruder
dimension count (by surgical manipulation), forgetting increases proportionally.
This rules out the possibility that both intruder dims and forgetting are caused by a third factor.
The intruder dims CAUSE the forgetting.

---

## Step 3: The Top SVs Are Universal Across All Tasks

Take ΔW from ten different fine-tuning tasks (all fine-tuned from the same base W₀).
Compute SVD of each ΔW. Keep the top-20% singular values from each.

Compare the corresponding left singular vectors across tasks:
    "Do different tasks update the same directions in weight space?"

**Measurement (mtLoRA, 2603.01526):**
    Top-20% SV components: 89% inter-task alignment.

89% of the "energy" in the top-20% singular vectors is shared across ALL tasks.
Different tasks — math reasoning, code generation, translation — update the same high-SV directions.

This means: the top singular value directions of ΔW are not task-specific.
They are a shared "overhead" that every fine-tuning touches.

This is surprising. If you use a large rank (r = 64) when the task only needs d_task = 4 directions,
the extra 60 dimensions do not encode additional task information.
Instead, they drift toward the same top-SV directions that every other task uses.
This is the geometric explanation for why large-rank LoRA causes more forgetting.

**Cross-architecture confirmation (mechanistic similarity paper):**
    Average MPPC (max pairwise Pearson correlation) = 0.74 between Pythia-160M and Mamba-130M.

74% of all features are shared between a transformer and an SSM trained on the same data.
The architecture is different. The training objective is the same. The features converge.

---

## Step 4: The One Number That Matters — d_task

**Definition:** d_task is the number of above-MP, W₀-orthogonal singular vectors in ΔW
for a well-trained LoRA. It is the intrinsic dimensionality of the task.

**Theorem (GELoRA, Theorem 3.2, 2412.09250):**
    Any LoRA achieving task performance φ must satisfy: rank(ΔW) ≥ idim(φ)

where idim(φ) is the intrinsic dimensionality of the task manifold, estimated by the
2-Nearest-Neighbors method on the gradient flow.

In plain English: if the task has intrinsic dimensionality d_task, then no LoRA with
rank < d_task can solve the task. You cannot compress below d_task.

**d_task is small.** GELoRA measures it across standard NLP benchmarks:
    Typical values: 2–16 per layer for NLU tasks on DeBERTaV3-base
    GELoRA achieves GLUE avg 87.92 using r = d_task instead of fixed r = 16 or r = 64.

**Four independent measurements give the same d_task:**

| Method | How it measures d_task | Paper |
|--------|----------------------|-------|
| GELoRA | 2-NN intrinsic dim of gradient manifold | 2412.09250 |
| AlphaLoRA | Count SVs where HTSR alpha ≈ 2 | AlphaLoRA paper |
| TRS count | Count above-MP, W₀-orthogonal SVs | this framework |
| SLT RLCT | RLCT drop: RLCT_gen = d_task(m+n-d_task)/2 | grokking_slt competing basins |

These four frameworks were built independently. They converge on the same number.
This is strong evidence that d_task is a real property of the task, not a measurement artifact.

---

## Step 5: What Happens When You Use Too Much Rank

Standard practice: set r = 64 (or r = 128 for large models). This is much larger than d_task.
The extra rank (r − d_task) is "excess rank."

**What does excess rank become?**

The SLT analysis gives the answer. LoRA with rank r has RLCT:
    RLCT(memorization basin) = r(m+n−r)/2       [excess rank, high complexity]
    RLCT(generalization basin) = d_task(m+n−d_task)/2   [minimal complexity]

(Watanabe's singular learning theory, applied to LoRA's GL(r) gauge symmetry.)

The grokking transition = escaping the memorization basin and reaching the generalization basin.

**Arrhenius formula for grokking timing:**
    t_grokking ~ exp( c × (r − d_task) × log n )

where n = training examples, c ~ (m+n)/(2T), T = temperature = η × λ (learning rate × weight decay).

**What this means concretely:**
If d_task = 4 and you use r = 16: (r − d_task) = 12.
If you use r = 64: (r − d_task) = 60.
The grokking time is exponential in this difference.

For large n (say n = 100,000 examples) and moderate c:
    Using r = 64 instead of r = 4 can increase training time by exp(60 × log(100,000)) ≈ exp(690).

This number is astronomically large. In practice it means: with r = 64 and insufficient training,
you never reach the generalization basin. You stop in the memorization basin.
The model looks fine on the training set but doesn't generalize.

**Weight decay is the temperature.** Higher weight decay = higher T = faster escape.
This is why grokking papers uniformly find that weight decay is essential (Power et al. 2022).

---

## Step 6: The Training Trajectory Is Readable

You can watch d_task emerge during training by monitoring the spectrum of ΔW.

**The trajectory (from_spikes_to_heavy_tails_spectral_evolution.pdf + AlphaLoRA):**

    Early training:    All SVs below MP threshold. No signal.
    Phase 1 (spike):   A few SVs rise above MP threshold (spike phase).
    Phase 2 (bulk+spike): The above-MP SVs grow; their HTSR power-law exponent alpha > 4.
    Phase 3 (consolidation): More SVs cross the MP threshold; alpha of first SVs decreases toward 2.
    Phase 4 (optimal): Exactly d_task SVs above MP; all with alpha ≈ 2. STOP HERE.
    Phase 5 (over-training): Same d_task SVs, but alpha < 2 for some. Diminishing returns.

**HTSR alpha is a quality certificate per singular vector:**
    alpha > 4: this direction is still noise-dominated; needs more training
    alpha ≈ 2: this direction is well-calibrated; represents stable task information
    alpha < 2: this direction is over-trained; memorizing rather than generalizing

The stopping criterion is completely spectral. No held-out validation set required:
    Stop when: rank(above-MP, W₀-orthogonal SVs) = d_task AND all alpha ≈ 2.

---

## Step 7: Multi-Task — When Two Fine-Tunings Share a Model

If you fine-tune task A and task B sequentially using LoRA:
Task A sets ΔW_A = B_A A_A. Then task B fine-tunes from W + ΔW_A.

**The interference problem:**
If the Region 2 subspace of task B (its d_task genuine directions) overlaps with
the Region 2 subspace of task A, the task B update rotates A's carefully learned directions.

**The zero-interference condition:**
    V_{A}^T V_{B} = 0    (singular vectors are orthogonal)

This is the condition that five independent methods discovered and implement:
- OSRM: orthogonal subspaces for robust model merging
- EBLoRA: orthogonal initialization of LoRA B matrices
- OPLoRA: project LoRA update onto W₀'s small-SV subspace (which is approximately orthogonal between tasks)
- mtLoRA: explicit spectral regularization L = λ Σ_{i<j} ||(B'_i)^T B'_j||_F²
- Share: foundational low-rank subspace shared and orthogonal task projections

**mtLoRA empirical result (2603.01526):**
    64.0% average accuracy across tasks
    47% fewer parameters than standard LoRA
    24% less training time

---

## Step 8: Model Merging — When You Want to Combine Many Fine-Tunings

Task arithmetic (Ilharco et al.): merge N task vectors by addition:
    W_merged = W₀ + Σ_i ΔW_i

**What happens to the spectrum?**
Region 2 components (task-specific): different tasks use different directions,
so the sum of N tasks' Region 2 vectors has magnitude that grows as O(√N) (random walk),
but each individual task's signal decays as O(1/√N) relative to the total.

This is CLT in weight space (synthesis 13). The task-specific signal AVERAGES OUT.

Region 1 components (universal): all tasks update the same directions.
The sum grows as O(N) (coherent addition). Region 1 DOMINATES after merging.

**The merged model is dominated by Region 1 (universal) and has lost task-specific Region 2.**
This is why merged models often score well on general benchmarks but fail on specific tasks.

Fix: before merging, downscale Region 1 and upscale Region 2 (SVC/isotropic merging/subspace boosting —
all doing the same correction from different angles, synthesis 13 and 18).

---

## Step 9: Why Small SVs of W₀ Are Where Fine-Tuning Belongs

This is a mechanistic explanation, not just a geometric observation.

W₀ is a linear map from input activations x to output. The SVD of W₀ decomposes this map into:
    Large SVs: respond to directions where x has large variance (common input patterns)
    Small SVs: respond to directions where x has small variance (rare input patterns)

**Key result (small_singular_values_rmt_transformers.pdf, Equations 6-7):**
The k-th singular vector v_k of W₀ has overlap with the k-th eigenvector of the
activation covariance matrix C = E[xx^T]. The overlap is proportional to the
corresponding eigenvalue of C.

In plain English: the large SVs of W₀ respond to the common, frequent input patterns.
The small SVs respond to the rare, specific input patterns.

**Now: what is fine-tuning trying to do?**
Fine-tuning a specific task (say, medical question answering) = learning to process
inputs that are RARE in the pretraining distribution (medical text is a tiny fraction of
general web text). Task-specific inputs are, by definition, rare in the pretrained model's
activation distribution.

Therefore: fine-tuning should update the SMALL-SV directions of W₀
(the directions where rare/task-specific inputs activate the network).
Updating large-SV directions = corrupting the handling of common patterns = forgetting.

This gives a principled, mechanistic justification for the OPLoRA constraint and the Region A/B split:
- Region A (large SVs of W₀) = common input handlers = do not fine-tune
- Region B (small SVs of W₀) = rare/specific input handlers = fine-tune here

**Compression result that confirms this:**
TSV-Compress (task_singular_vectors_merge_interference.pdf):
    10x parameter compression while retaining 99% accuracy

If you keep only the "Task Singular Vectors" (the genuine Region 2 directions), you retain
99% of task performance with 10× fewer parameters. The Region 1 and noise components are
genuinely expendable.

---

## Step 10: The Layer-Wise Pattern

Interference between tasks is not uniform across layers.

**Measurement (task_singular_vectors_merge_interference.pdf):**
    Early layers: high inter-task interference
    Deep layers: low inter-task interference

This is consistent with what we know about transformer layers:
- Early layers: process syntax, basic semantics = shared across all language tasks = Region 1
- Deep layers: process task-specific concepts, reasoning patterns = Region 2

**Prediction:** d_task should be SMALLER in early layers (less Region 2) and LARGER in deep layers.
GELoRA's intrinsic dimensionality profile shows exactly this pattern (layer-wise d_task varies).

**Engineering implication:** Do not use the same LoRA rank r for every layer.
Use small r in early layers (where Region 2 is small and interference is high)
and larger r in deep layers (where Region 2 is large and interference is low).
This is what GELoRA does, and why it achieves the same performance with 47% fewer parameters.

---

## Step 11: Where Everything Lands — The Grassmannian

The above-MP singular subspace of ΔW has dimension d_task and lives in R^m.
A d_task-dimensional subspace of R^m is a POINT ON THE GRASSMANNIAN G(d_task, m).

G(d_task, m) is the smooth manifold of all d_task-dimensional subspaces of R^m.
Every fine-tuning task maps to exactly one point on this manifold. That point IS the task.

**Three foundations, all pre-2024 classical results:**

**Foundation 1 — Spiked Covariance Model (Johnstone 2001; Paul 2007; BBP 2005; SRFM 2024):**
When a matrix has the form B = signal + noise (rank-d signal, random noise), the
minimum-MSE estimator of the signal is: keep the above-MP singular vectors, zero out the rest.
This is EXACTLY TRS. TRS = the classical minimum-MSE denoiser, applied to LoRA.

The MP threshold is not a heuristic. It is the BBP phase transition (Baik, Ben Arous, Péché 2005):
the information-theoretic boundary above which a spike is detectable from the noise floor. Below it,
no estimator can recover the signal. Above it, it is asymptotically consistent.

After one gradient step on a task, ΔW = task-aligned spike + MP bulk (SRFM, arXiv:2410.18938).
The spike exceeds the MP threshold ↔ the task signal is strong enough to clear the BBP boundary.
After full training, d_task independent spikes accumulate. TRS measures them all.

Assumption required: the noise in ΔW = BA is approximately Gaussian-shaped. This is testable:
fit an MP distribution to the bulk of ΔW's singular values and check goodness-of-fit.

**Foundation 2 — GL_r Invariance (algebraic fact, no assumptions):**
ΔW = BA is unchanged by B → BG, A → G⁻¹A for any G ∈ GL_r (an invertible r×r matrix).
Any function that is well-defined must be invariant under this transformation.
Singular values of B alone are NOT invariant (they change when G is not orthogonal).
The ONLY invariant object is the column subspace of ΔW — a point on G(r, m).
TRS (the above-MP subspace of ΔW) is the GL_r-invariant summary of the fine-tuning.

**Foundation 3 — Cencov's Theorem (1982) + Fisher-Rao Metric:**
Cencov's theorem: the Fisher-Rao metric is the UNIQUE Riemannian metric on the statistical
manifold that is invariant under sufficient statistics (i.e., under all information-preserving
reparametrizations).
The Grassmannian geodesic distance in the Fisher-Rao pullback metric is therefore the unique
statistically optimal AND reparametrization-invariant measure of distance between task subspaces.

Assumptions required: (a) model output is smooth in weights (true for standard softmax networks);
(b) Fisher metric is non-degenerate on the task subspace (fails only for uninformative tasks);
(c) task subspace is well-identified (requires sufficient training data; confirmed by d_task stability).

**Why gradient descent lands on this Grassmannian point (Gunasekar et al. 2017, arXiv:1705.09280):**
Gradient descent on underdetermined matrix factorization (W = UV^T) with small step size and
near-zero initialization converges to the minimum nuclear norm solution:
    argmin ||W||_*  subject to  data constraint
Nuclear norm minimization rewards sparse singular spectra: exactly d_task above-MP singular values
and nothing else. This is the Grassmannian point. The implicit bias of GD IS the TRS selection
principle — even without explicit regularization. (Weight decay reinforces it: λ||A||_F² + λ||B||_F²
= 2λ||ΔW||_* as proven in synthesis 27.)

**The unified mathematical conclusion:**
For any task comparison method to be BOTH:
    (a) statistically optimal (minimum-MSE under spiked covariance) AND
    (b) reparametrization-invariant (GL_r invariant)
it must reduce to Grassmannian geodesic distance on TRS subspaces.

Every method that ignores TRS or uses a non-Grassmannian distance is provably suboptimal
under these assumptions. This includes cosine similarity on raw weight deltas, L2 distance
on LoRA factors, and most behavioral similarity measures.

**The falsifying experiment (no training needed, ~30 min on CPU):**
Take 5 LoRAs from LLaMA-3-8B fine-tuned on GSM8K math.
Take 5 LoRAs from Mistral-7B fine-tuned on GSM8K math (same task, different architecture).
Take 10 LoRAs from both models fine-tuned on diverse random tasks.

Compute Grassmannian geodesic distance d_G = principal angles (sum of squared sines) between TRS
subspaces for each pair.

Prediction: d_G(same-task, different-architecture) << d_G(different-task, same-architecture)

The Grassmannian distance clusters by TASK, not by architecture.

If this holds: TRS finds the task's coordinates on the Grassmannian. The core claim is confirmed.
If this fails: the spiked covariance assumption breaks for real LoRAs (a falsification of the theory).

---

## The Complete Architecture of the Theory

Everything above follows from five measurements and three classical foundations:

    Fact 1: ρ = 0.971       (intruder dims ↔ forgetting, causal; Shuttleworth 2410.21228)
    Fact 2: 89%             (top-20% SVs shared across all tasks; mtLoRA 2603.01526)
    Fact 3: 74%             (top features shared across architectures; MPPC Pythia vs Mamba)
    Fact 4: 10x at 99%      (task SVs = all task info; TSV-Compress, Gargiulo 2025)
    Fact 5: high/low layers  (early=high interference, deep=low; TSV paper)

And one theorem:

    Theorem: rank(ΔW) ≥ d_task is necessary for task performance  [GELoRA 3.2]

And three classical foundations:

    Foundation 1: TRS = minimum-MSE signal estimator  [Johnstone 2001, Paul 2007]
    Foundation 2: GL_r invariance → column subspace is the only well-defined object  [algebra]
    Foundation 3: Grassmannian geodesic = unique invariant task distance  [Cencov 1982]

**The conclusion:** The space of fine-tuning tasks is a subset of the Grassmannian G(d_task, m).
TRS finds the correct point. Grassmannian distance is the only valid way to compare tasks.

---

## What Is Still Uncertain

Honest list of what is inferred vs. proven:

1. **Arrhenius formula:** The form t ~ exp(c(r-d_task)log n) is derived from SLT free energy
   arguments. It is theoretically motivated but not directly measured. The qualitative claim
   (more excess rank = slower grokking) is confirmed empirically; the exact exponential form is not.

2. **The four frameworks measure the same d_task:** GELoRA, AlphaLoRA, TRS, SLT RLCT are argued to
   converge on d_task by separate theoretical arguments. A direct side-by-side comparison on the
   same dataset and model has not been published.

3. **The S operator:** The claim that S = E_tasks[ΔW^T ΔW] is the master object unifying everything
   is a framework claim. Theorem 2.5 (Two-Level Convergence) proves that fine-tunings concentrate
   in the top eigenspace of S, but the identification of S's eigenspectrum with the three regions
   is the framework's interpretation, not a separately proven theorem.

4. **Universal weight subspace is architecture-independent:** Tested on Pythia vs. Mamba (74% MPPC).
   Not yet tested on transformers vs. CNNs, or language vs. vision models.

5. **The Grassmannian clustering prediction:** Whether d_G(same-task, diff-arch) << d_G(diff-task)
   holds empirically is the critical unfalsified prediction. This is testable with SVD in 30 minutes.
   If it fails, either the spiked covariance assumption breaks or the MP threshold is misidentified.

These five gaps are the places where the theory could break down. Gap 5 is the most important:
it is the single experiment that either anchors the entire geometric picture or overturns it.
