# Graph Report - weightBench  (2026-05-07)

## Corpus Check
- 16 files · ~39,749 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1085 nodes · 1400 edges · 78 communities (61 shown, 17 thin omitted)
- Extraction: 81% EXTRACTED · 15% INFERRED · 0% AMBIGUOUS · INFERRED: 211 edges (avg confidence: 0.83)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `c7f47b89`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_LoRA Weight Space Core|LoRA Weight Space Core]]
- [[_COMMUNITY_Intrinsic Dimensionality & Fine-Tuning|Intrinsic Dimensionality & Fine-Tuning]]
- [[_COMMUNITY_Graph Metanetworks & Symmetry|Graph Metanetworks & Symmetry]]
- [[_COMMUNITY_Generative Weight Space & Neural Fields|Generative Weight Space & Neural Fields]]
- [[_COMMUNITY_LoRA Parameter Generation|LoRA Parameter Generation]]
- [[_COMMUNITY_Weight Alignment & Model Quality|Weight Alignment & Model Quality]]
- [[_COMMUNITY_Adaptive LoRA & Hypernetworks|Adaptive LoRA & Hypernetworks]]
- [[_COMMUNITY_Task Arithmetic & Model Editing|Task Arithmetic & Model Editing]]
- [[_COMMUNITY_Self-Modifying & Recurrent Weights|Self-Modifying & Recurrent Weights]]
- [[_COMMUNITY_Weight Space Geometry & Regions|Weight Space Geometry & Regions]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 23|Community 23]]
- [[_COMMUNITY_Community 24|Community 24]]
- [[_COMMUNITY_Community 25|Community 25]]
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Community 27|Community 27]]
- [[_COMMUNITY_Community 28|Community 28]]
- [[_COMMUNITY_Community 29|Community 29]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 31|Community 31]]
- [[_COMMUNITY_Community 32|Community 32]]
- [[_COMMUNITY_Community 33|Community 33]]
- [[_COMMUNITY_Community 34|Community 34]]
- [[_COMMUNITY_Community 35|Community 35]]
- [[_COMMUNITY_Community 36|Community 36]]
- [[_COMMUNITY_Community 37|Community 37]]
- [[_COMMUNITY_Community 38|Community 38]]
- [[_COMMUNITY_Community 39|Community 39]]
- [[_COMMUNITY_Community 40|Community 40]]
- [[_COMMUNITY_Community 41|Community 41]]
- [[_COMMUNITY_Community 42|Community 42]]
- [[_COMMUNITY_Community 43|Community 43]]
- [[_COMMUNITY_Community 44|Community 44]]
- [[_COMMUNITY_Community 45|Community 45]]
- [[_COMMUNITY_Community 46|Community 46]]
- [[_COMMUNITY_Community 47|Community 47]]
- [[_COMMUNITY_Community 48|Community 48]]
- [[_COMMUNITY_Community 49|Community 49]]
- [[_COMMUNITY_Community 50|Community 50]]
- [[_COMMUNITY_Community 51|Community 51]]
- [[_COMMUNITY_Community 52|Community 52]]
- [[_COMMUNITY_Community 53|Community 53]]
- [[_COMMUNITY_Community 54|Community 54]]
- [[_COMMUNITY_Community 55|Community 55]]
- [[_COMMUNITY_Community 56|Community 56]]
- [[_COMMUNITY_Community 57|Community 57]]
- [[_COMMUNITY_Community 58|Community 58]]
- [[_COMMUNITY_Community 59|Community 59]]
- [[_COMMUNITY_Community 60|Community 60]]
- [[_COMMUNITY_Community 63|Community 63]]
- [[_COMMUNITY_Community 64|Community 64]]
- [[_COMMUNITY_Community 65|Community 65]]
- [[_COMMUNITY_Community 66|Community 66]]
- [[_COMMUNITY_Community 67|Community 67]]
- [[_COMMUNITY_Community 68|Community 68]]
- [[_COMMUNITY_Community 69|Community 69]]
- [[_COMMUNITY_Community 70|Community 70]]
- [[_COMMUNITY_Community 71|Community 71]]
- [[_COMMUNITY_Community 72|Community 72]]
- [[_COMMUNITY_Community 73|Community 73]]
- [[_COMMUNITY_Community 74|Community 74]]
- [[_COMMUNITY_Community 75|Community 75]]
- [[_COMMUNITY_Community 76|Community 76]]
- [[_COMMUNITY_Community 77|Community 77]]

## God Nodes (most connected - your core abstractions)
1. `Task Residual Spectrum (TRS)` - 20 edges
2. `A Survey of Weight Space Learning: Understanding, Representation, and Generation` - 20 edges
3. `Running Synthesis — Weight Bench Night Research` - 18 edges
4. `Cross-LoRA Transfer for Heterogeneous LLMs` - 17 edges
5. `W2T: LoRA Weights Already Know What They Can Do` - 17 edges
6. `Task Residual Spectrum (TRS)` - 17 edges
7. `W2T Framework (Weight-to-Token)` - 16 edges
8. `Universal Weight Subspace` - 15 edges
9. `The Universal Weight Subspace Hypothesis` - 14 edges
10. `Intruder Dimensions` - 13 edges

## Surprising Connections (you probably didn't know these)
- `LoRA Weight Distance (max_l rank(u_l - v_l) via SVD)` --semantically_similar_to--> `Singular Value Decomposition for Low-Rank Model Compression`  [INFERRED] [semantically similar]
  origin_of_llamas_model_tree_heritage.pdf → finding_literature/purifying_task_vectors_knowledge_subspace.pdf
- `Task Residual Spectrum (TRS)` --semantically_similar_to--> `SVD Features for LoRA Clustering`  [INFERRED] [semantically similar]
  finding_literature/BIG_IDEAS.md → finding_literature/data_driven_adapter_clustering_merging_svd.pdf
- `Task Residual Spectrum (TRS)` --semantically_similar_to--> `LoRA Spectrum Encodes Dataset Size`  [INFERRED] [semantically similar]
  finding_literature/BIG_IDEAS.md → finding_literature/desire_dataset_size_recovery_lora_svd.pdf
- `Canonical TRS via QR+SVD` --semantically_similar_to--> `EigenLoRAx Task-Invariant Principal Subspace`  [INFERRED] [semantically similar]
  finding_literature/BIG_IDEAS.md → finding_literature/eigenloreax_recycling_adapters_principal_subspace.pdf
- `Subspace Geometry Catastrophic Forgetting (2603.02224)` --semantically_similar_to--> `Spectral Imbalance in LoRA Updates`  [INFERRED] [semantically similar]
  finding_literature/FINDINGS.md → finding_literature/eblora_spectral_imbalance_forgetting.pdf

## Hyperedges (group relationships)
- **Fisher-Based CL Hierarchy: EWC → EWC-LoRA → FILet → FOPNG → FILet+FOPNG (Increasing Faithfulness to Horizontal Subbundle)** — ewc_kirkpatrick_paper, ewc_lora_paper, filet_paper, fopng_paper, concept_fisher_bundle_connection, concept_ewc_horizontal_subbundle, concept_filet_fopng_prediction [EXTRACTED 1.00]
- **Holonomy = Accumulated Drift (Neural Network Forgetting + Recommender Content Drift): Cross-Domain Instance** — recbundle_paper, concept_recbundle_holonomy_recommenders, concept_holonomy_intruder_correspondence, concept_rank1_hebbian_holonomy, concept_recbundle_general_holonomy_tool [INFERRED 0.85]
- **TRS Paper Core Theorem Cluster: Spectral Decomposition + Holonomy-Intruder + Fisher Bundle Connection** — concept_spectral_decomposition_theorem1, concept_holonomy_intruder_correspondence, concept_fisher_bundle_connection, concept_unified_bundle_table, concept_steele_forgetting_formula [EXTRACTED 1.00]
- **W_qk Curvature as Training Artifact: Bilinear Metric + Rank-1 Hebbian + Decoder vs Encoder Asymmetry** — wqk_curvature_paper, concept_wqk_bilinear_metric, concept_rank1_hebbian_holonomy, concept_decoder_curvature_lora_intruder_dims [EXTRACTED 1.00]
- **RecBundle Fiber Bundle Formalism: Base Manifold (Users) + Fiber (Preferences) + Connection + Holonomy** — recbundle_paper, concept_recbundle_parallel_transport_collab, concept_recbundle_holonomy_recommenders, concept_recbundle_curvature_curvature_distortion, concept_recbundle_gbi_metric, concept_recbundle_meta_learning_bundle [EXTRACTED 1.00]
- **EWC-LoRA Mathematical Foundations: Proposition 1 (Separate≠Full) + Proposition 3 (FIM over ΔW) + Full-Space Fisher** — ewc_lora_paper, concept_ewclora_proposition1, concept_ewclora_proposition3, concept_ewclora_fim_fullspace, concept_ewclora_stability_plasticity [EXTRACTED 1.00]

## Communities (78 total, 17 thin omitted)

### Community 0 - "LoRA Weight Space Core"
Cohesion: 0.05
Nodes (66): 2D Layer Selection Map (alpha x TRS), Bayesian Spectral Calibration, Fisher Subspace, GL_r Invariance of LoRA B-matrix, Grokking as Spectral Phase Transition, Intruder Dimensions, Marchenko-Pastur Distribution, NTK Optimal Rank Bound sqrt(N) (+58 more)

### Community 1 - "Intrinsic Dimensionality & Fine-Tuning"
Cohesion: 0.06
Nodes (56): Continual Learning (Lifelong Learning Without Forgetting), LoRA: Low-Rank Adaptation for Parameter-Efficient Fine-Tuning, Singular Value Decomposition for Low-Rank Model Compression, Weight Space Learning (Neural Networks as Data Points), Catastrophic Forgetting (cross-paper: CL problem addressed by Share), LoRA Weight Subspace (cross-paper concept: low-rank adapter directions), Model Merging Ecosystem (cross-paper: task vectors + LoRA + subspaces), SVD Weight Analysis (cross-paper: PAVE CO-SVD + Share SVD + MoTHer LoRA dist) (+48 more)

### Community 2 - "Graph Metanetworks & Symmetry"
Cohesion: 0.05
Nodes (53): Catastrophic Forgetting in Continual Learning, Depth-Aware Initialization: s_t^{(ℓ,0)} = s_min + (ℓ-1)/(L-1)*(s_max-s_min), Gradient Projection Memory (GPM), Gradient Orthogonality Constraint: G_{t-1}^T U_t = 0, Knowledge Component Decomposition: ΔW_t = Σ σ_{t,i} u_{t,i} v_{t,i}^T, Manifold Retraction via Whitening: U+ = Y(Y^T Y)^{-1/2}, EBLoRA: Spectral Imbalance and Catastrophic Forgetting, Restricted Stiefel Manifold: M_t = {U ∈ R^{d×r} | U^TU = I_r, G_{t-1}^T U = 0} (+45 more)

### Community 3 - "Generative Weight Space & Neural Fields"
Cohesion: 0.08
Nodes (51): LLaMA Models (2-7B, 3-8B), RoBERTa Models, ViT Models (B/32, B/16, L/14), Amplification Factor (AF) / Reverse AF, Burer-Monteiro Factorization, Common Subspace, Data-Parameter Interaction, Effective Rank (k_M) (+43 more)

### Community 4 - "LoRA Parameter Generation"
Cohesion: 0.04
Nodes (44): ADDITIONAL DEEP IDEAS, Big Ideas — Autonomous Night Synthesis, code:block1 (Platonic Hypothesis (2405.07987)), Idea 10: The Canonical TRS via W2T, Idea 11: Universal Subspace as the TRS Prior, Idea 12: TRS = Optimal Bayes Estimator of Task Signal, Idea 13: Zero-Shot LoRA Audit via LoL + TRS, Idea 14: Bayesian Spectral Calibration — Unifying TRS and SVC (+36 more)

### Community 5 - "Weight Alignment & Model Quality"
Cohesion: 0.06
Nodes (44): Interpretability in Parameter Space: APD (Attribution-based Parameter Decomposition), Bilinear MLPs Enable Weight-Based Mechanistic Interpretability, Block-Level Adaptation (mtLoRA), Deterministic Equivalent for Feature Covariance, Fiber Bundle Framework for Weight Space, Fine-Grained Routing (mtLoRA), Geometry of Neural Net Parameter Spaces Under Reparametrization (Kristiadi et al.), Learning in the Fisher Subspace: Guided Initialization for LoRA (+36 more)

### Community 6 - "Adaptive LoRA & Hypernetworks"
Cohesion: 0.07
Nodes (38): Anti-Grokking: Late-Stage Generalization Collapse, Barabasi-Albert Scale-Free Network, Competing Near-Zero-Loss Solution Basins (Grokking Mechanism), Correlation Traps (Anomalous Eigenvalues in Randomized Weight Matrices), DevInterp Package (LLC Estimation Tool), Dimensional Phase Transition in Neural Networks, Effective Dimensionality D (FSS Exponent of Gradient Avalanche Dynamics), Empirical Spectral Density (ESD) of Layer Weight Matrices (+30 more)

### Community 7 - "Task Arithmetic & Model Editing"
Cohesion: 0.08
Nodes (36): Catastrophic Forgetting / Pre-training Distribution Forgetting, Continual Learning with LoRA vs Full Fine-tuning, Effective Rank of LoRA Update Matrix, Full Fine-tuning, Algorithm for Finding Intruder Dimensions, Intruder Dimensions, Intruder Dimension Scaling Experiment (Causal Intervention), LLaMA-2-7B Evaluation Model (+28 more)

### Community 8 - "Self-Modifying & Recurrent Weights"
Cohesion: 0.09
Nodes (33): Decoder W_qk Skew-Symmetry (Non-Zero Curvature) → More Intruder Dims in Tight-Rank LoRA Fine-tuning, EWC Diagonal Fisher Approximation Limitation: Misses Off-Diagonal Curvature → Residual Forgetting, EWC as Horizontal Subbundle Constraint (Fisher penalty = stay in ker(ω)), EWC-LoRA: Full-Dimensional FIM over ΔW=AB (not A,B separately) for Accurate Fisher Estimation, EWC-LoRA Proposition 1: Separate Regularization of A,B ≠ Full-Space Regularization of ΔW, EWC-LoRA Proposition 3: Empirical FIM over ΔW Induces Constraints on Low-Rank Factors A,B, EWC-LoRA Achieves Flexible Stability–Plasticity Trade-off via Tunable λ (Outperforms Vanilla LoRA by 8.92%), EWC-LoRA = Fisher Regularization on the TRS Object ΔW (Complementary to TRS Spectral Decomposition) (+25 more)

### Community 9 - "Weight Space Geometry & Regions"
Cohesion: 0.08
Nodes (32): Universal Subspace = Flat Fiber Directions Zero Holonomy Conjecture (Idea 26), Four-Way Spectral Decomposition of LoRA (genuine TRS / intruder / bulk / suppression), Holonomy-Intruder Duality (Idea 22), Marchenko-Pastur Null Distribution for TRS, Sheaf-Bundle Duality for Holonomy Measurement (Idea 25), Task Residual Spectrum as Universal Task Fingerprint, FILet: Fisher-Guided LoRA Initialization (arXiv:2605.01046), Fisher Information Metric Always Present (arXiv:2302.07384) (+24 more)

### Community 10 - "Community 10"
Cohesion: 0.06
Nodes (30): code:block1 (1. NTK Regime (2402.11867): Optimal LoRA rank = √N), code:block2 (12. Universal Weight Subspace (2512.05117): 1100+ models con), code:block3 (17. Isotropic Model Merging (2502.04959): Spectral skewness ), code:block4 (20. mtLoRA (2603.01526): Top-20% singular values = 89% inter), Current Status of the Central Claim (refined), EXTENDED THEORETICAL CHAIN (Iteration 2 — 16 independent papers), EXTENDED THEORETICAL CHAIN (Iteration 4 — 19 independent papers), EXTENDED THEORETICAL CHAIN (Iteration 5 — 25 independent papers) (+22 more)

### Community 11 - "Community 11"
Cohesion: 0.07
Nodes (30): Feature Learning Theory (cross-paper: RMT + empirical convergence), Mechanistic Interpretability (cross-paper: circuits + features + universality), Cross-Architecture Feature Similarity (avg MPPC=0.74), Depth Specialization (layer l in Pythia ~ layer 2l in Mamba), Induction Circuit ([A][B]...[A]->predict[B]), Local Convolution Layer (Mamba preprocessing), Mamba-130M (SSM model), Mamba SSM Induction (layer 17 SSM + local convolution) (+22 more)

### Community 12 - "Community 12"
Cohesion: 0.13
Nodes (24): Anti-Grokking: Late-Stage Generalization Collapse (α < 2 after 10^7 steps), Correlation Traps (Anomalous Eigenvalues in W^rand ESD), Effective Dimensionality D (FSS Exponent: s_max ~ N^D), Empirical Spectral Density (ESD) and Marchenko-Pastur Distribution, Generalisation Basin (Low-LLC, Structured Algorithmic Solution), Grokking as Bayesian Phase Transition between Competing Basins, Grokking as Dimensional Phase Transition (D crosses 1 at critical point), Grokking Severity Measure (GSM): Negatively Correlated with Learning Rate (+16 more)

### Community 13 - "Community 13"
Cohesion: 0.09
Nodes (22): 0. What This Document Does, 1. THEOREM 1: Spectral Decomposition (PROVED under listed assumptions), 2. CONJECTURE 2: Holonomy-Intruder Correspondence (NOT a theorem — CONDITIONAL), 3. DEFINITION 3a + APPROXIMATION 3b: Fisher Bundle Connection, 4. Precision Improvements From This Analysis, 5. Graph Nodes to Add (for next graphify update), 6. Status Summary, Approximation 3b (EWC ≈ horizontal projection) (+14 more)

### Community 14 - "Community 14"
Cohesion: 0.14
Nodes (21): Algebraic Geometry (Foundation of SLT), Arrhenius Reaction Rate Hypothesis for Grokking, Autoencoder Bottleneck Dimension LLC Scaling, SLT Free Energy (Fn), Grokking (Delayed Generalization), Lau et al. 2023: Local Learning Coefficient (LLC) Paper, Local Learning Coefficient (LLC), Low-Rank Matrix Factorization Network LLC Experiment (+13 more)

### Community 15 - "Community 15"
Cohesion: 0.12
Nodes (21): Large-Scale Analysis: 1100+ Models (500 Mistral LoRAs, 500 ViTs, 50 LLaMA-8B), DARE-TIES Merging, EigenLoRAx (Recycling Adapters for Principal Subspaces), Truncated Zero-Centered Higher-Order SVD (HOSVD), KnOTS-TIES Merging (SVD-based Subspace Alignment), 50 LLaMA3-8B Models Subspace Analysis, Lottery Ticket Hypothesis, 500 Mistral-7B LoRA Models Subspace Analysis (+13 more)

### Community 16 - "Community 16"
Cohesion: 0.15
Nodes (20): FILet Algorithm (Fisher-Guided LoRA Initialization via Minimum Fisher Energy), Fisher Energy E(Z) for LoRA Direction Selection, Fisher Merging as Tractable Mahalanobis/Fréchet Surrogate, Fisher-Rao Geodesic Distance and Fisher Information Matrix, Fréchet Mean on Riemannian Manifold, GeoMerge Algorithm (Riemannian/Quotient Merging of LoRA Adapters), K-FAC Kronecker-Factored Fisher Approximation (S_W ≈ S_X ⊗ S_Y), LoRA Interference (Parameter-Data Interaction across Tasks Causing Merge Conflicts) (+12 more)

### Community 17 - "Community 17"
Cohesion: 0.12
Nodes (20): LoRA: Low-Rank Adaptation of Large Language Models (Hu et al. 2021), Eigenvector-Based LoRA Initialization via Sample Covariance, LoRA Subspace Constraint Before Fine-Tuning, OSRM: Orthogonal Subspaces for Robust Model Merging, Parameter-Data Interaction in LoRA Model Merging, Low-Rank LoRA Solution Generalization Guarantee, Low-Rank Solution Existence for Full Fine-Tuning in NTK Regime, No Spurious Local Minima in LoRA with Sufficient Rank (+12 more)

### Community 18 - "Community 18"
Cohesion: 0.12
Nodes (19): Base-Model Transfer (SD1.4 to SD1.5) in W2T, Behavior Prediction from Weight Representations, Model Editing via Weight Space, Model-Free (Probe-Based) Weight Space Representation, Model Retrieval in Weight Space, Position-Level Transformer (f_pos) in W2T, ProbeGen (Deep Linear Probe Generator), ProbeLog (Probe-Based Model Representation) (+11 more)

### Community 19 - "Community 19"
Cohesion: 0.16
Nodes (19): Bulk+Spike ESD: MP Bulk with Outlier Singular Value After Large η Step, Empirical Spectral Density (ESD) of Weight Matrices, Five+One Training Phases: Random→Bleeding-Out→Bulk+Spike→Bulk-Decay→Heavy-Tailed→Rank Collapse, Good Generalization: PL_Alpha_Hill in Range (2, 2.5), HT-MU: Heavy-Tailed Self-Regularization Framework, Kernel Target Alignment (KTA): Feature Learning Quality Metric, From Spikes to Heavy Tails: Spectral Evolution of Weight Matrices, Power-Law Exponent (PL_Alpha_Hill, PL_Alpha_KS) for Tail Heaviness (+11 more)

### Community 20 - "Community 20"
Cohesion: 0.11
Nodes (17): ADDITIONAL QUESTIONS RESOLVED BY THE SAME EXPERIMENT, code:python ("""), COST ESTIMATE, EXPECTED OUTPUTS AND INTERPRETATIONS, EXPERIMENT: Principal Angles Between U_W₀ and U_S*, EXPERIMENTAL DESIGN, If U_S* ⊂ U_W₀_bottom (aligns with W₀ minor subspace):, If U_S* ⊂ U_W₀_top (aligns with W₀ principal subspace): (+9 more)

### Community 21 - "Community 21"
Cohesion: 0.14
Nodes (17): DARE Merging (Yu et al. 2024), Iso-CTS Merging (Marczak et al. 2025), Model Merging (Weight Space Addition), Spectral Over-Accumulation in Model Merging (Li et al. 2026), Singular Value Calibration (SVC), Task Arithmetic (Ilharco et al. 2022), TIES Merging (Yadav et al. 2023), TSV-Merge (Gargiulo et al. 2025) - cited by SVC paper (+9 more)

### Community 22 - "Community 22"
Cohesion: 0.13
Nodes (17): ARC-Easy-LoRA Dataset (10,000 LoRA checkpoints), CelebA-LoRA Dataset (10,177 LoRA checkpoints), CUB-LoRA Dataset (11,788 LoRA checkpoints), GL(r)-Invariance Proposition (Proposition 3.1), GoEmotions-LoRA Dataset (20,000 LoRA checkpoints), Hu et al. 2022 (LoRA Original Paper), Kaushik et al. 2025 (EigenLoRAx), Low-Rank Adaptation (LoRA) (+9 more)

### Community 23 - "Community 23"
Cohesion: 0.21
Nodes (16): Biderman et al. 2024: LoRA Learns Less and Forgets Less, Catastrophic Forgetting in Continual Learning, Continual Learning (Sequential Task Training), Effective Rank (Entropy-Based) of LoRA Gradient Matrices, Geometric Forgetting Law: F = alpha*(1 - cos^2(theta_min)) + beta, Gradient Projection Memory (GPM), Gradient Subspace (Span of Gradients During Training), InfLoRA (Interference-Free Low-Rank Adaptation) (+8 more)

### Community 24 - "Community 24"
Cohesion: 0.13
Nodes (14): code:block1 (TRS_final(B) = {u_i : σ_i > σ_MP), Critical Theory Revision: Night Run Iteration 2, NEW LITERATURE TO ADD, THE ASSUMPTION THAT BROKE, THE COMPLETE FOUR-WAY DECOMPOSITION, THE FIBER BUNDLE STRUCTURE — CONFIRMED GAP, THE FORGETTING GEOMETRY THEOREM, The Four-Way Spectral Decomposition — A Complete Theory (+6 more)

### Community 25 - "Community 25"
Cohesion: 0.18
Nodes (15): Low-Rank Adaptation (LoRA) for Parameter-Efficient Fine-Tuning, Singular Value Decomposition Applied to Weight Space Analysis, Singular Value Decomposition (SVD) for Task Analysis, Task Matrix (Weight Difference per Layer), Task Vector (Fine-tuned minus Pre-trained Weights), Low-Rank Nature of Per-Layer Task Matrices, Low-Rank Nature of Layer Task Matrices, Task Singular Vectors (TSV) (+7 more)

### Community 26 - "Community 26"
Cohesion: 0.14
Nodes (13): code:block1 (F = α(1 − cos²θ_min) + β), code:block2 (Input:), CURRENT STATE OF THE THEORY (Summary of 4 Synthesis Documents), INTRUDER DIMENSIONS = "ESCAPING THE FIBER" (GEOMETRIC FORMALIZATION), NEW CRITICAL FINDING: FILet IS THE FISHER CONNECTION IN PRACTICE, NEW EXPERIMENT: FILet vs. Random vs. PiSSA Intruder Comparison, Steele's Formula = Holonomy. The Bridge Is Found., Synthesis Night Run: Iteration 4 (+5 more)

### Community 27 - "Community 27"
Cohesion: 0.15
Nodes (12): Foundation 1: Spiked Covariance Model (Johnstone 2001; Paul 2007), Foundation 2: GL_r Invariance (Algebraic Fact), Foundation 3: Cencov's Theorem + Fisher-Rao Metric on the Grassmannian, THE CORE CLAIM — The One Unbreakable Idea, THE EXPERIMENT THAT ANCHORS EVERYTHING, THE PAPER IN TWO SENTENCES, THE SINGLE CLAIM, THE THREE FOUNDATIONS (ALL PRE-2024, ALL PROVEN) (+4 more)

### Community 28 - "Community 28"
Cohesion: 0.15
Nodes (12): NEW THEORETICAL CLAIMS (Iteration 3 Additions), OPEN QUESTIONS (Iteration 3), PAPERS TO ADD TO CORPUS (Iteration 3), Synthesis Night Run: Iteration 3, THE FIVE SPECTRAL PHASES: MAPPING TO FOUR-WAY DECOMPOSITION, THE GAUGE THEORY CONNECTION: SHEAF + BUNDLE, The Holonomy Connection — Gauge Theory Meets Spectral Decomposition, THE KEY INSIGHT: INTRUDER DIMENSIONS = WEIGHT-SPACE HOLONOMY (+4 more)

### Community 29 - "Community 29"
Cohesion: 0.18
Nodes (13): Activation Covariance Eigenvectorâ€“Singular Vector Overlap, Lazy Learning Regime in Transformer Pretraining, Marchenko-Pastur (MP) Law for Weight Matrix Spectra, Minimal Random Matrix Model for Small Singular Value Outliers, Random Matrix Theory as Zero-Information Null Hypothesis for Weights, Small Singular Values Encode Learned Information in Transformers, SVD-Based Pruning and Compression Guidance for LLMs, Low-Rank Adaptation (LoRA) (+5 more)

### Community 30 - "Community 30"
Cohesion: 0.23
Nodes (13): Singular Value Inflation (from Cross-Task Alignment), Bulk Spectrum (Noise Floor in Weight Matrices), Zeroing Small Singular Values as Denoising (LASER insight), Eigenvalue Distribution in Weight Matrices (Bulk vs. Signal), LASER: Layer-Selective Rank Reduction (Sharma et al. 2023), SNR-Based Layer Selection for Targeted Training, Marchenko-Pastur Distribution, Overfitting Impact on Singular Values (Near-Zero SVs) (+5 more)

### Community 31 - "Community 31"
Cohesion: 0.17
Nodes (11): 8-Task Commonsense Suite, code:bash (lm_eval --model hf \), code:block2 ([boolq_acc, piqa_acc, hellaswag_acc, winogrande_acc, arc_eas), code:block3 (dataset/), Design: One LoRA Per Task (Specialist), Directory Structure, Evaluation Suite (Behavioral Coordinate), LoRA Training Configuration (Fixed Across All Tasks) (+3 more)

### Community 32 - "Community 32"
Cohesion: 0.2
Nodes (12): Aggregation-Aware Null Calibration, Aristotelian Representation Hypothesis, Centered Kernel Alignment (CKA), Depth Confounder in Representational Similarity, Local Neighborhood Convergence Across Modalities, Mutual k-Nearest Neighbors (mKNN), Permutation-Based Null-Calibration Framework, Platonic Representation Hypothesis (+4 more)

### Community 33 - "Community 33"
Cohesion: 0.18
Nodes (12): Federated Learning via Weight Space Generation, Functional Invariance in Weight Space, HyperDreamBooth (Hypernetwork for LoRA Initialization), Hypernetworks for Weight Space Generation, Implicit Neural Representations (INRs), Model Unification via Weight Space, Neural Architecture Search via Weight Space Generation, Neuron Permutation Invariance (+4 more)

### Community 34 - "Community 34"
Cohesion: 0.2
Nodes (12): Eilertsen et al. 2020 (Classifying the Classifier), Kofinas et al. 2024 (Neural Graph - NG), Model Zoo Benchmarks for WSL, Navon et al. 2023 (DWSNets), Unterthiner et al. 2020 (Predicting NN Accuracy from Weights), Functional Invariance and Equivariance in Weight Space, Hypernetworks for Weight Space Generation, A Survey of Weight Space Learning: Understanding, Representation, and Generation (+4 more)

### Community 35 - "Community 35"
Cohesion: 0.2
Nodes (11): A Matrix Seed Variation as Cross-Seed Robustness Ablation, AdaLoRA Paper, AsymmetryOfLoRA Paper, B Matrix Clusters by Task; A Matrix Does Not, Canonical Representation: SVD Spectrum of B per Layer with Importance Weighting, Effective Rank as Confound and Covariate Control, Concrete Experiment 1 Design Changes Table, FFN Top Layers Carry More Task-Specific Singular Values (+3 more)

### Community 36 - "Community 36"
Cohesion: 0.2
Nodes (7): key_format_diagnostic(), load_lora_delta(), measure_alignment(), Principal angles between U_W0 (pretrained singular subspace) and U_S* (cross-LoR, Print first 6 adapter state dict keys so you can verify the key pattern., For each layer, compute:       - Principal angles between U_W0_top_k and U_S* (t, Load ΔW = scaling * lora_B @ lora_A directly from the adapter checkpoint.     Do

### Community 37 - "Community 37"
Cohesion: 0.24
Nodes (10): Singular Statistical Models (Non-identifiable Neural Networks), Arrhenius Reaction Rate Hypothesis for Grokking Time, SLT Free Energy (Fn) for Phase Transition Timing, Grokking: Delayed Generalization Phase Transition, Local Learning Coefficient (LLC) as Complexity Measure, Modulo Arithmetic Network (Grokking Testbed), Using SLT to Understand Grokking and Phase Transitions in Neural Networks, Stochastic Gradient Langevin Dynamics (SGLD) for LLC Estimation (+2 more)

### Community 38 - "Community 38"
Cohesion: 0.29
Nodes (10): Q/K vs V/O Spectral Asymmetry in TRS (Idea 23), Spectral Lifecycle of Transformer Training: Q/K vs V/O Asymmetry (arXiv:2604.22778), Autoregressive Training Induces Column Dominance / Directionality in W_qk (Theorem 2.3), Bidirectional Training Induces Symmetry in W_qk (Theorem 2.4), Underlying Structures of Self-Attention: Symmetry, Directionality, Emergent Dynamics (arXiv:2502.10927), Symmetry Score and Directionality Score for Square Matrices (Definitions 3.1-3.2), W_qk = W_q * W_k^T as Bilinear Form Defining Metric in Embedding Space, Claim 6: V-layer TRS Dominance (Synthesis 3) (+2 more)

### Community 39 - "Community 39"
Cohesion: 0.22
Nodes (9): Task Residual Spectrum (TRS), TRS as Optimal Bayes Estimator, GradientSpace SVD Task Clusters (2512.06678), No Task Left Behind Isotropic Merging (2502.04959), mtLoRA Spectral Task Regularization (2603.01526), Small Singular Values Matter RMT (2410.17770), Spectral Over-Accumulation Merging (2602.05536), Spiked RMT Task Learning Features (2410.18938) (+1 more)

### Community 40 - "Community 40"
Cohesion: 0.22
Nodes (9): Fiber Bundle Structure of Weight Space, Fisher Metric Connection, Holonomy as Task Interference Measure, Intruder Dimensions (LoRA B matrix new directions), MiLoRA Paradox and Resolution, Platonic Weight Space Hypothesis, Frechet Averages Quotient Manifold (2604.27155), LoRA vs Full Fine-tuning Intruder Dimensions (2410.21228) (+1 more)

### Community 41 - "Community 41"
Cohesion: 0.29
Nodes (8): Model Merging Without Extra Training, Task Interference in Multi-Task Model Merging, Projection Mismatch (Inter-task Interference Measure), Shared Knowledge (Cross-Task Aligned Components), Spectral Over-Counting / Over-Accumulation, Subspace Overlap (Column-Space Overlap in Merged Basis), Per-Layer Task Interference Pattern (High in Early, Low in Deep Layers), Singular Task Interference (STI) Metric

### Community 42 - "Community 42"
Cohesion: 0.29
Nodes (8): Deep Weight-Space Networks (DWSNets), Functional Equivariance in Weight Space, GLNet (GL(r)-Equivariant Baseline for LoRA), Graph Metanetworks (GMNs) for Weight Space, Model-Based Weight Space Representation, Neural Functional Networks (NFN), Scale-GMN (Scaling + Permutation Equivariant GNN), Universal Neural Functionals (UNFs)

### Community 43 - "Community 43"
Cohesion: 0.32
Nodes (8): Cross-Architecture Subspace Gap, Foundation Models as Objects in Weight Space, Implicit Regularization via Shared Subspace, LoRA as Universal Low-Rank Adaptation Module for WSL, Open Question: Universal Architecture-Agnostic Weight Space Learner, Spectral Bias of Neural Networks (Low-Frequency Learning), Universal Subspace for Model Compression (100x Memory Reduction), Universal Weight Subspace

### Community 44 - "Community 44"
Cohesion: 0.32
Nodes (8): Forgetting Geometry Theorem, TRS-based Continual Learning Curriculum, Weight Disentanglement via TRS Orthogonality, Gradient Orthogonality Constraint (EBLoRA), EBLoRA Spectral Imbalance Forgetting (2602.00722), Spectral Imbalance in LoRA Updates, Stiefel Manifold Optimization for Balanced LoRA, Subspace Geometry Catastrophic Forgetting (2603.02224)

### Community 45 - "Community 45"
Cohesion: 0.29
Nodes (8): Universal Weight Subspace, D2C Iterative Clustering Algorithm, D2C Data-Driven Adapter Clustering and Merging (2601.17441), SVD Features for LoRA Clustering, EigenLoRAx Recycling Adapters Principal Subspace (2502.04700), EigenLoRAx Task-Invariant Principal Subspace, EigenLoRAx Generalization Bound Theorem 3.6, Universal Weight Subspace Hypothesis (2512.05117)

### Community 46 - "Community 46"
Cohesion: 0.29
Nodes (6): Concrete Experiment 1 Changes, Experiment 1 Insights from LoRA-Specific Papers, From AdaLoRA: The geometry is not uniform — layer position and module type predict information density, From AsymmetryOfLoRA: Your weight-space representation should be B-only, From SymmetriesInWSL: Your distance metric must match what you're predicting, Hidden Cross-Paper Insights

### Community 47 - "Community 47"
Cohesion: 0.29
Nodes (6): CONJECTURE EDGES (INFERRED, marked for graph), CONJECTURE: Universal Subspace ↔ TRS / Intruder Dims Bridge, PAPERS TO READ FOR DISCRIMINATING EVIDENCE, THE TWO REFERENCE FRAMES (operationally distinct in all existing papers), WHAT IS ESTABLISHED (EXTRACTED facts), WHAT MUST NOT BE CLAIMED (labeled CONJECTURE until measured)

### Community 48 - "Community 48"
Cohesion: 0.29
Nodes (6): Concrete Experiment 1 Changes, Experiment 1 Insights from LoRA-Specific Papers, From AdaLoRA: The geometry is not uniform — layer position and module type predict information density, From AsymmetryOfLoRA: Your weight-space representation should be B-only, From SymmetriesInWSL: Your distance metric must match what you're predicting, Hidden Cross-Paper Insights

### Community 49 - "Community 49"
Cohesion: 0.29
Nodes (7): Benchmark Score Invariant to Large Family of Weight-Space Transformations, Behavioral Signal (Benchmark Score Vector), Benchmark Evaluation Pipeline, Dual-Signal Framing (Weight-Space + Behavioral Combined), LoRA Training Pipeline (Infrastructure), Weight-Space Representation Extraction Method, Weight-Space Signal (LoRA Parameter Coordinate)

### Community 50 - "Community 50"
Cohesion: 0.38
Nodes (7): Induction Circuits in Transformers and Mamba, Mamba State Space Model Architecture, Max Pairwise Pearson Correlation (MPPC) Feature Similarity Metric, Off-by-One Preference Motif in Mamba SSM, Towards Universality: Studying Mechanistic Similarity Across Language Model Architectures, Sparse Autoencoders (SAEs) for Interpretable Feature Extraction, Universality Hypothesis in Mechanistic Interpretability

### Community 51 - "Community 51"
Cohesion: 0.33
Nodes (6): LoRA-WiSE Benchmark, DSiRe Dataset Size Recovery from LoRA (2406.19395), LoRA Spectrum Encodes Dataset Size, Intrinsic Dimensionality Profile Across Layers, GeLoRA Geometric Adaptive Ranks Intrinsic Dim (2412.09250), GeLoRA Rank Bound Theorem 3.2

### Community 52 - "Community 52"
Cohesion: 0.33
Nodes (6): Four-Way Spectral Decomposition, Genuine TRS, MP Bulk, Spectral-Population Duality, Near-zero Suppression Dimensions, Subspace-Boosted Merging Rank Collapse (2506.16506)

### Community 53 - "Community 53"
Cohesion: 0.6
Nodes (5): Diffusion-Based Weight Generation, DnD (Diffusion for LoRA via Task Vectors), Generative Models for Weight Space Generation, ICM-LoRA (Conditional VAE for LoRA Weights), SANE (Sequential Autoencoding for Network Weights)

### Community 54 - "Community 54"
Cohesion: 0.4
Nodes (5): TRS_HTMP Next-Generation Fingerprint, HTMP Heavy-Tailed Mechanistic Universality (2506.03470), From Spikes to Heavy Tails Spectral Evolution (2406.04657), MP to Spike to Heavy-Tail ESD Pathway, Spectral Maturity Cross-Architecture Confound

### Community 55 - "Community 55"
Cohesion: 0.5
Nodes (4): Canonical TRS via QR+SVD, Zero-Shot LoRA Audit via LoL + TRS, Learning on LoRAs GL-Equivariant (2410.04207), W2T LoRA Weights Know Task (2603.15990)

### Community 56 - "Community 56"
Cohesion: 0.5
Nodes (4): BIG_IDEAS Synthesis Document, Night Run 2 Critical Revision Document, Literature Findings Document, Running Synthesis Document

### Community 57 - "Community 57"
Cohesion: 0.67
Nodes (3): Spectral Stability of Non-Dominant Subspace During Fine-Tuning, Task-Specific Knowledge Injected Into Low-Dimensional Subspace, Top Singular Vectors Reorient During Fine-Tuning

### Community 58 - "Community 58"
Cohesion: 0.67
Nodes (3): 2D Layer Selection Map (alpha x TRS), AlphaLoRA HT-SR Layer Quality (2410.10054), Spectrum MP-null Layer Selection (2406.06623)

## Knowledge Gaps
- **428 isolated node(s):** `Principal angles between U_W0 (pretrained singular subspace) and U_S* (cross-LoR`, `Load ΔW = scaling * lora_B @ lora_A directly from the adapter checkpoint.     Do`, `Print first 6 adapter state dict keys so you can verify the key pattern.`, `For each layer, compute:       - Principal angles between U_W0_top_k and U_S* (t`, `graphify` (+423 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **17 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `A Survey of Weight Space Learning: Understanding, Representation, and Generation` connect `Community 34` to `Community 33`, `Community 43`, `Community 15`, `Community 18`, `Community 22`?**
  _High betweenness centrality (0.062) - this node is a cross-community bridge._
- **Why does `Model Merging Without Extra Training` connect `Community 41` to `Intrinsic Dimensionality & Fine-Tuning`, `Community 34`, `Community 21`, `Community 25`?**
  _High betweenness centrality (0.058) - this node is a cross-community bridge._
- **Why does `Universal Weight Subspace` connect `Community 43` to `LoRA Weight Space Core`, `Community 33`, `Community 18`, `Community 15`?**
  _High betweenness centrality (0.048) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `Task Residual Spectrum (TRS)` (e.g. with `Subspace Geometry and Catastrophic Forgetting` and `Fisher Subspace`) actually correct?**
  _`Task Residual Spectrum (TRS)` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `A Survey of Weight Space Learning: Understanding, Representation, and Generation` (e.g. with `The Universal Weight Subspace Hypothesis` and `W2T: LoRA Weights Already Know What They Can Do`) actually correct?**
  _`A Survey of Weight Space Learning: Understanding, Representation, and Generation` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Principal angles between U_W0 (pretrained singular subspace) and U_S* (cross-LoR`, `Load ΔW = scaling * lora_B @ lora_A directly from the adapter checkpoint.     Do`, `Print first 6 adapter state dict keys so you can verify the key pattern.` to the rest of the system?**
  _428 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `LoRA Weight Space Core` be split into smaller, more focused modules?**
  _Cohesion score 0.05 - nodes in this community are weakly interconnected._