# Synthesis 6: Formal Proofs, Honest Gaps, and Falsification Landscape
*Night run iteration 13 — 2026-05-07*
*Status: WORKING DOCUMENT — proof sketches, not final theorems*

---

## 0. What This Document Does

Prior syntheses built toward three "paper theorems." This document:
1. Distinguishes what is genuinely **proved under stated assumptions** from what is **conjecture**
2. Writes proof sketches that a referee could check
3. States explicit **falsifiers** — specific outcomes that would break each claim
4. Records the mathematical precision issues surfaced by falsification analysis

Standing instructions honored: "you are in no hurry to make a claim, keep going and exploring."

---

## 1. THEOREM 1: Spectral Decomposition (PROVED under listed assumptions)

### Statement
Let ΔW = BA be a LoRA fine-tuning update (B ∈ ℝ^{m×r}, A ∈ ℝ^{r×n}).
Under the **spiked covariance model** for ΔW (Definition 1.1), the minimum-MSE, GL_r-invariant estimator of the task-specific signal is the **above-MP singular subspace** of ΔW.

The four spectral regions (Definition 1.2):
- **TRS (Task Residual Spectrum):** above-MP singular vectors aligned with pretraining structure
- **Intruder Dims:** above-MP singular vectors that have escaped the pretraining fiber
- **MP Bulk:** within-MP singular values (noise, zero signal content)
- **Suppression Region:** below-minimum-MP (attenuated directions)

### Definitions

**Definition 1.1 (Spiked covariance model for ΔW):**
ΔW = S^{1/2} Z + σ · E, where:
- Z ∈ ℝ^{r×n} is the rank-r task signal (low-rank per NTK theory; Jang et al. 2024, ICML)
- E ∈ ℝ^{m×n} has i.i.d. entries with mean 0, variance 1 (noise)
- S ∈ ℝ^{m×m} is the signal covariance, rank ≤ r
- σ = initialization scale of frozen base model parameters (approximately 1/√n for typical init)

**Definition 1.2 (MP threshold):** For an m×n matrix with aspect ratio γ = m/n:
MP edge λ_{+} = σ²(1 + √γ)² (Marchenko-Pastur 1967)
Singular values above σ(1 + √γ) are above-MP.

**Definition 1.3 (GL_r invariance):** A function f(B, A) is GL_r-invariant if f(BG, G^{-1}A) = f(B, A) for all G ∈ GL_r. The singular subspace of ΔW = BA is GL_r-invariant; the singular values of B or A separately are not.

### Proof Sketch

**Step 1 (GL_r invariance requires subspace representation):**
Any GL_r-invariant function of the LoRA factorization reduces to a function of ΔW = BA, since ΔW is the unique GL_r-invariant combination. Among functions of ΔW, the column space col(ΔW) = col(B) is GL_r-invariant. This is a point on the Grassmannian G(r, m). ∎ (algebraic fact)

**Step 2 (Above-MP = consistent signal estimator):**
By the spike model (Definition 1.1), eigenvalues of ΔW ΔWᵀ above λ_{+} are consistent estimators of the true signal eigenvalues as m, n → ∞ with m/n → γ (Paul 2007, Ann. Statist.). The optimal estimator under MSE loss is the MP-shrunken matrix (Nadler 2014; Gavish & Donoho 2014). The subspace of above-MP singular vectors is the minimum-MSE estimator of col(B). ∎ (reduces to classical RMT)

**Step 3 (Four-region partition):**
Given W_0 (pretrained weights), define the fiber direction as the fiber of the bundle W_0 (directions aligned with W_0's singular subspace). The above-MP singular vectors of ΔW partition into:
- Those with cos-similarity ≥ ε to U_{W_0,top-k}: "TRS" (in fiber region)
- Those with cos-similarity < ε to ALL of U_{W_0,top-k}: "Intruder Dims" (escaped fiber)
This definition is from Shuttleworth et al. 2410.21228, who empirically verified these cause forgetting. ∎

### Assumptions That Must Be Stated in Paper
| Assumption | Consequence if violated |
|---|---|
| ΔW has approximately Gaussian noise | MP threshold shifts; use empirical MP fit instead |
| Signal is low-rank (r ≤ √N) | Spiked covariance model breaks down |
| Noise and signal are approximately independent | Structured noise would invalidate Paul 2007 theorem |
| m/n aspect ratio far from degenerate | Near-square matrices have different MP limits |

### What Would Falsify Theorem 1
1. If empirical B-matrices (from real LoRA checkpoints) have non-MP bulk distributions → spiked model doesn't apply → above-MP is not the correct threshold
2. If B-matrices have systematically structured noise (e.g., all eigenvalues clustered near a discrete set) → universality argument fails
3. **Testable (free, in run_experiment.py):** Fit an empirical Marchenko-Pastur distribution to the singular values of each ΔW. If goodness-of-fit p < 0.05, flag that adapter's contribution.

---

## 2. CONJECTURE 2: Holonomy-Intruder Correspondence (NOT a theorem — CONDITIONAL)

### Statement (conditional form)
**IF** experiment_results_reference_frame.json shows mean principal angle < 30° (U_{W_0} ≈ U_{S*}), **THEN** the following correspondence is empirically supported:

intruder_dim_score ∝ ||Holonomy(training loop)||_{Fisher}

where holonomy is measured as the angle of rotation induced by parallel transport around the closed loop of the training trajectory in the Fisher bundle on W → W/G.

**IF** mean principal angle > 60° (U_{W_0} ⊥ U_{S*}), **THEN** the two reference frames (Shuttleworth, Kaushik) are distinct objects, the holonomy-intruder identification fails, and this conjecture is ABANDONED.

### Why This Is Not a Theorem

**Problem 1 — Gradient subspace angles ≠ holonomy eigen-angles (confirmed 2026-05-07):**
Steele (arXiv:2603.02224, "Subspace Geometry Governs Catastrophic Forgetting in Low-Rank Adaptation") defines θ_min as the **minimum principal angle between task gradient subspaces**, not as an eigenvalue of a holonomy matrix. The formula F = α(1−cos²θ_min) + β measures gradient subspace overlap at training time, not a geometric phase of the weight manifold.

The synthesis_night_run_4 claim that "Steele formula = holonomy formula in angular form" conflates two distinct objects:
- Gradient subspace angle: angle between ∇L_task1 column space and ∇L_task2 column space
- Holonomy eigen-angle: eigenvalue of the parallel transport operator around a closed loop in weight space

These may be related (if the gradient flow traces a closed loop and the connection is the Fisher metric), but this requires a separate argument. Until provided, label as INFERRED, confidence 0.65.

**Problem 2 — Fisher metric rank degeneracy:**
The empirical Fisher Information Matrix (FIM) has rank ≤ (batch size × output dimension), far below the parameter count of any transformer layer. This means the "horizontal subbundle" ker(ω) — defined as the complement of the vertical (gauge) subbundle under the Fisher metric — is not a smooth vector subbundle in the differential-geometric sense: its rank is not constant across the parameter manifold.

Consequences:
- Holonomy of a connection on a non-constant-rank distribution is not a standard mathematical object (requires singular foliation theory)
- EWC with diagonal Fisher is even further from the true horizontal subbundle
- This is a **definitional gap**, not an empirical question

Defense options:
1. Restrict to a constant-rank stratum (parameter configurations where Fisher has constant rank r_0)
2. Use regularized Fisher (Tikhonov: F + εI for ε > 0) — this is a well-defined positive-definite metric everywhere
3. Reformulate using the pseudo-Riemannian structure (degenerate metric, flat along null directions)

**Problem 3 — Zero-holonomy forgetting exists:**
Weight magnitude drift beyond the linearization radius, dead ReLU accumulation across layers, and BatchNorm running-statistic corruption all produce catastrophic forgetting with zero subspace-rotation signal. These are not exotic edge cases — they are standard in sequential fine-tuning literature.

Consequence: "forgetting iff nonzero holonomy" is **false** as a biconditional. The defensible version:
> "Holonomy is the necessary and sufficient cause of the **subspace-rotation component** of catastrophic forgetting. Other mechanisms (norm drift, activation statistics) cause forgetting through non-geometric channels."

### Conditional Proof Sketch (pending experiment)

**Hypothesis (INFERRED):** The two reference frames coincide: U_{W_0,top-k} ≈ U_{S*,top-k} (principal angles < 30°).

**If confirmed, the following chain holds:**
1. Above-MP singular vectors of ΔW that escape U_{W_0} = intruder dims (Shuttleworth, 2410.21228)
2. If U_{W_0} ≈ U_{S*}, then escape from U_{W_0} = escape from the universal task subspace U_{S*}
3. Escape from U_{S*} = catastrophic forgetting (Kaushik, 2512.05117 — "secondary subspace performance drastically worse")
4. The training trajectory's parallel transport in the Fisher bundle accumulates holonomy proportional to gradient subspace misalignment
5. If Steele's θ_min (gradient subspace angle) ≈ holonomy eigen-angle (Step 4 connection, INFERRED 0.65), then F ∝ ||Holonomy||_{Fisher}

**Weakest links:** Steps 2 (requires U_{W_0} ≈ U_{S*}) and 4-5 (gradient angle ≠ holonomy angle — INFERRED, not proved).

### Explicit Falsifiers for Conjecture 2
1. **Experiment yields mean angle > 60°:** U_{W_0} ⊥ U_{S*} → chain collapses at Step 2 → conjecture abandoned
2. **High-rank LoRA with more intruder dims AND less forgetting:** would break Step 3 causal link
3. **Sequential tasks with forgetting measured at zero gradient subspace overlap:** would decouple Steele's θ_min from forgetting, breaking Step 4-5
4. **Forgetting on tasks with nearly identical gradient subspaces:** zero θ_min but forgetting via weight norm drift → confirms the "partial holonomy" defense but restricts the claim

---

## 3. DEFINITION 3a + APPROXIMATION 3b: Fisher Bundle Connection

### Definition 3a (Definitional choice, not proved)
The Fisher metric g_{Fisher}(v, w) = E_{x}[v^T F(W) w] where F(W) = E[∇log p(y|x,W) ∇log p(y|x,W)^T] is the Fisher Information Matrix.

On weight space W, this induces a principal connection 1-form ω on the bundle W → W/G (quotient by gauge group G = GL_r action on LoRA factors). The **horizontal subbundle** ker(ω) is the orthogonal complement of the vertical (gauge) subbundle under g_{Fisher}.

**This is a definitional choice** — there is no theorem saying "the Fisher metric is the correct connection for fine-tuning." Cencov's theorem (1982) says the Fisher-Rao metric is the unique invariant metric on the *statistical manifold* (distributions), not on weight space directly. The pullback to weight space requires:
- Smoothness of W ↦ p(·|·, W) (true for standard networks)
- Non-degeneracy of the Fisher metric on the adaptation subspace (may fail — see degeneracy issue above)

The definition is well-motivated but the "uniqueness" claim is softer than synthesis_5 stated.

### Approximation 3b (EWC ≈ horizontal projection)

**Statement:** EWC's penalty ||ΔW||^2_{F_{diag}} is an approximation to the projection of ΔW onto the vertical subbundle (gauge directions) under g_{Fisher}.

**Error analysis:**
- True horizontal projection uses the full FIM F(W_0) (m·n × m·n matrix for each layer)
- EWC uses diagonal approximation: F_{diag} = diag(E[g_i²]) for each parameter i
- FILet (2605.01046) uses block-diagonal Fisher (per-layer rank-r approximation)
- FOPNG (2601.12816) uses the Fisher-orthogonal gradient, the closest published method to true horizontal projection

**Error bound (informal):**
||ΔW_horizontal - ΔW_EWC_horizontal||_F ≤ ||F - F_{diag}||_op · ||ΔW||_F

Where the operator norm ||F - F_{diag}||_op is the off-diagonal coupling strength of the FIM. For transformers, this is typically large (FIM has strong off-diagonal structure across attention heads). So EWC is a crude approximation; FILet and FOPNG are much better.

**What this means for the paper:**
- EWC = "inspired by" horizontal subbundle, not "implements" it exactly
- The precise chain: FOPNG > FILet > EWC in terms of approximation quality
- This is still a unifying insight, just quantitatively graded, not binary

### Explicit Falsifiers for 3a/3b
1. **If Fisher metric is identically zero on the adaptation subspace:** definition degenerates; requires regularized Fisher
2. **If EWC empirically worse than random projection at preventing forgetting:** approximation is too crude to be worth the "horizontal subbundle" framing
3. **If any non-Fisher regularizer achieves lower forgetting than FOPNG:** would suggest Fisher geometry is not the relevant geometry for fine-tuning

---

## 4. Precision Improvements From This Analysis

### Upgraded claims (from prior syntheses)

| Prior claim | Precise version |
|---|---|
| "EWC = horizontal subbundle" | "EWC approximates horizontal projection using diagonal Fisher; FOPNG is the closest known implementation" |
| "Steele formula = holonomy formula" | "Steele's F uses gradient subspace angles; holonomy uses weight-space parallel transport eigen-angles. These are distinct objects that may be related (INFERRED 0.65)" |
| "Theorem 2: intruder_dim_score ∝ holonomy" | "CONJECTURE 2: IF U_{W_0} ≈ U_{S*} (pending experiment), intruder dims are in the same orbit as holonomy; forgetting via non-geometric channels exists independently" |
| "Fisher metric is unique invariant" | "Fisher-Rao is unique on statistical manifold (Cencov 1982); pullback to weight space requires non-degeneracy of FIM on adaptation subspace (may fail)" |

### New mathematical gaps to address before submission
1. **Fisher degeneracy:** Address the non-constant-rank issue. Simplest fix: state that all bundle constructions are restricted to the stratum where rank(F(W)) = r (constant). This is a Zariski-open dense set — argument for why generic position holds.
2. **Holonomy vs. gradient angle:** Either prove the connection (requires path-integral calculation in the Fisher bundle) or keep as INFERRED conjecture with explicit gap statement.
3. **MP goodness-of-fit:** The run_experiment.py script can be augmented to fit an empirical Marchenko-Pastur and test goodness-of-fit. This makes Theorem 1's assumptions empirically checkable.

---

## 5. Graph Nodes to Add (for next graphify update)

New concepts identified this synthesis:
- `gradient_subspace_angle_steele` — θ_min in Steele's formula; gradient subspace overlap angle
- `holonomy_eigen_angle` — eigenvalue of parallel transport operator; distinct from gradient angle
- `fisher_metric_rank_degeneracy` — empirical FIM rank ≪ parameter count; horizontal subbundle rank not constant
- `singular_foliation_fine_tuning` — required mathematical framework when Fisher is degenerate
- `non_geometric_forgetting_channels` — weight norm drift, dead ReLU, BatchNorm statistics
- `tikhonov_regularized_fisher` — F + εI; resolves rank degeneracy at cost of metric uniqueness

New INFERRED edges:
- `steele_forgetting_formula` -[INFERRED 0.65]-> `holonomy_eigen_angle` (may be related; not the same object)
- `fisher_metric_rank_degeneracy` -[EXTRACTED]-> `horizontal_subbundle_definition` (makes ker(ω) ill-defined)
- `non_geometric_forgetting_channels` -[EXTRACTED]-> `conjecture_2_holonomy_intruder` (falsifier: zero holonomy but forgetting occurs)

---

## 6. Status Summary

| Claim | Status | Proof | Key assumption | Falsifier |
|---|---|---|---|---|
| Theorem 1: TRS = min-MSE GL_r estimator | **PROVED under assumptions** | Paul 2007 + Johnstone 2001 + GL_r algebraic fact | Spiked covariance model for ΔW | Non-MP bulk distribution |
| Conjecture 2: Holonomy ∝ intruder dims | **CONJECTURE (conditional)** | Pending experiment + gradient/holonomy angle connection | U_{W_0} ≈ U_{S*}; gradient angle ≈ holonomy angle | Experiment yields angles > 60° |
| Definition 3a: Fisher bundle connection | **DEFINITION (motivated choice)** | Cencov 1982 on statistical manifold | FIM non-degenerate on adaptation subspace | Degenerate FIM on task subspace |
| Approximation 3b: EWC ≈ horizontal | **APPROXIMATION (graded quality)** | Informal error bound | Diagonal ≈ full FIM (crude but nonzero) | EWC outperformed by random projection |

**Most urgent action:** `python run_experiment.py` — determines whether Conjecture 2 survives or collapses.

**Most urgent mathematical fix:** Fisher degeneracy → either (a) constant-rank stratum restriction or (b) Tikhonov regularization with explicit ε dependence. This must be resolved before formal submission.

---

## 7. Additional Falsifier: The Rank-Forgetting Empirical Tension

*Added 2026-05-07 from systematic literature search*

**The tension:**
- Shuttleworth et al. (2410.21228): Low rank (r ∈ {1,2,4,8}) produces MORE intruder dimensions than high rank (r=2048 essentially eliminates them)
- Biderman et al. (2405.09673, TMLR): Lower rank (r ∈ {16,64,256}) forgets LESS

If intruder-dim *count* mediates the rank-forgetting relationship, these two findings contradict: low rank → more intruder dims → should forget more; but empirically low rank forgets less.

**Why this is not yet a proven contradiction:**
The two studies test non-overlapping rank ranges (Shuttleworth: r ∈ {1−16}; Biderman: r ∈ {16−256}). r=16 is the only overlap point. They may describe two different regimes rather than a single monotonic relationship.

**The unresolved question (CONJECTURE 2b, untested):**
The mediating variable may be intruder-dim *Frobenius energy* (sum of squared intruder singular values), not intruder-dim *count*. Low-rank LoRA produces more intruder vectors, but each carries less energy (total ΔW energy is constrained by the rank bound). High-rank LoRA produces fewer intruder vectors but allows larger magnitude ones.

If correct: the TRS/MP threshold is the unifying mechanism — below-MP intruder dims are automatically noise-suppressed regardless of count. The relevant predictor is above-MP intruder Frobenius energy.

**This is testable:** `run_experiment.py` now measures both intruder count and intruder Frobenius energy per adapter per layer (added 2026-05-07). Comparing across adapters with known rank values (r ∈ {8, 16, 64, 256} in the current K=11 set) will directly test whether energy or count correlates with rank.

**Additional falsifier (from this tension):** If run_experiment.py shows that low-r adapters in our set have equal or *larger* intruder Frobenius energy compared to high-r adapters, then the count/magnitude distinction does not resolve the tension → Conjecture 2's causal mechanism is incorrect.

**Key papers for this question:**
- arXiv:2405.09673 (Biderman, LoRA Learns Less and Forgets Less) — monotonic rank↑→forgetting↑ in r={16,64,256}
- arXiv:2512.15634 (How Much is Too Much?) — non-monotonic, task-dependent; SVD cosine sim measured directly
- arXiv:2603.02224 (Steele) — rank approximately irrelevant when task subspaces are orthogonal
- arXiv:2603.09684 (Catastrophic Forgetting in Low-Rank PEFT) — update subspace geometry as causal factor
