# Graph Report - finding_literature  (2026-05-07)

## Corpus Check
- 56 files · ~700,000 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 863 nodes · 1190 edges · 52 communities (36 shown, 16 thin omitted)
- Extraction: 78% EXTRACTED · 17% INFERRED · 0% AMBIGUOUS · INFERRED: 208 edges (avg confidence: 0.83)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_TRS Spectral Theory Core|TRS Spectral Theory Core]]
- [[_COMMUNITY_LoRA Geometry & Merging|LoRA Geometry & Merging]]
- [[_COMMUNITY_Weight Space Learning|Weight Space Learning]]
- [[_COMMUNITY_Mechanistic Interpretability|Mechanistic Interpretability]]
- [[_COMMUNITY_Grokking & Phase Transitions|Grokking & Phase Transitions]]
- [[_COMMUNITY_RMT & Heavy Tails|RMT & Heavy Tails]]
- [[_COMMUNITY_Forgetting & Continual Learning|Forgetting & Continual Learning]]
- [[_COMMUNITY_Task Arithmetic & Composition|Task Arithmetic & Composition]]
- [[_COMMUNITY_Fiber Bundle & Holonomy|Fiber Bundle & Holonomy]]
- [[_COMMUNITY_Universal Subspace|Universal Subspace]]
- [[_COMMUNITY_Fisher & Natural Gradient|Fisher & Natural Gradient]]
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

## God Nodes (most connected - your core abstractions)
1. `A Survey of Weight Space Learning: Understanding, Representation, and Generation` - 20 edges
2. `Task Residual Spectrum (TRS)` - 19 edges
3. `Cross-LoRA Transfer for Heterogeneous LLMs` - 17 edges
4. `W2T: LoRA Weights Already Know What They Can Do` - 17 edges
5. `Task Residual Spectrum (TRS)` - 17 edges
6. `W2T Framework (Weight-to-Token)` - 16 edges
7. `The Universal Weight Subspace Hypothesis` - 14 edges
8. `Intruder Dimensions` - 13 edges
9. `Grokking as a Phase Transition between Competing Basins: a Singular Learning Theory Approach` - 13 edges
10. `Universal Weight Subspace` - 13 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Hyperedges (group relationships)
- **Fisher-Based CL Hierarchy: EWC → EWC-LoRA → FILet → FOPNG → FILet+FOPNG (Increasing Faithfulness to Horizontal Subbundle)** — ewc_kirkpatrick_paper, ewc_lora_paper, filet_paper, fopng_paper, concept_fisher_bundle_connection, concept_ewc_horizontal_subbundle, concept_filet_fopng_prediction [EXTRACTED 1.00]
- **Holonomy = Accumulated Drift (Neural Network Forgetting + Recommender Content Drift): Cross-Domain Instance** — recbundle_paper, concept_recbundle_holonomy_recommenders, concept_holonomy_intruder_correspondence, concept_rank1_hebbian_holonomy, concept_recbundle_general_holonomy_tool [INFERRED 0.85]
- **TRS Paper Core Theorem Cluster: Spectral Decomposition + Holonomy-Intruder + Fisher Bundle Connection** — concept_spectral_decomposition_theorem1, concept_holonomy_intruder_correspondence, concept_fisher_bundle_connection, concept_unified_bundle_table, concept_steele_forgetting_formula [EXTRACTED 1.00]
- **W_qk Curvature as Training Artifact: Bilinear Metric + Rank-1 Hebbian + Decoder vs Encoder Asymmetry** — wqk_curvature_paper, concept_wqk_bilinear_metric, concept_rank1_hebbian_holonomy, concept_decoder_curvature_lora_intruder_dims [EXTRACTED 1.00]
- **RecBundle Fiber Bundle Formalism: Base Manifold (Users) + Fiber (Preferences) + Connection + Holonomy** — recbundle_paper, concept_recbundle_parallel_transport_collab, concept_recbundle_holonomy_recommenders, concept_recbundle_curvature_curvature_distortion, concept_recbundle_gbi_metric, concept_recbundle_meta_learning_bundle [EXTRACTED 1.00]
- **EWC-LoRA Mathematical Foundations: Proposition 1 (Separate≠Full) + Proposition 3 (FIM over ΔW) + Full-Space Fisher** — ewc_lora_paper, concept_ewclora_proposition1, concept_ewclora_proposition3, concept_ewclora_fim_fullspace, concept_ewclora_stability_plasticity [EXTRACTED 1.00]

## Communities (52 total, 16 thin omitted)

### Community 0 - "TRS Spectral Theory Core"
Cohesion: 0.05
Nodes (63): 2D Layer Selection Map (alpha x TRS), Bayesian Spectral Calibration, Fisher Subspace, GL_r Invariance of LoRA B-matrix, Grokking as Spectral Phase Transition, Intruder Dimensions, Marchenko-Pastur Distribution, NTK Optimal Rank Bound sqrt(N) (+55 more)

### Community 1 - "LoRA Geometry & Merging"
Cohesion: 0.06
Nodes (56): Continual Learning (Lifelong Learning Without Forgetting), LoRA: Low-Rank Adaptation for Parameter-Efficient Fine-Tuning, Singular Value Decomposition for Low-Rank Model Compression, Weight Space Learning (Neural Networks as Data Points), Catastrophic Forgetting (cross-paper: CL problem addressed by Share), LoRA Weight Subspace (cross-paper concept: low-rank adapter directions), Model Merging Ecosystem (cross-paper: task vectors + LoRA + subspaces), SVD Weight Analysis (cross-paper: PAVE CO-SVD + Share SVD + MoTHer LoRA dist) (+48 more)

### Community 2 - "Weight Space Learning"
Cohesion: 0.05
Nodes (53): Catastrophic Forgetting in Continual Learning, Depth-Aware Initialization: s_t^{(ℓ,0)} = s_min + (ℓ-1)/(L-1)*(s_max-s_min), Gradient Projection Memory (GPM), Gradient Orthogonality Constraint: G_{t-1}^T U_t = 0, Knowledge Component Decomposition: ΔW_t = Σ σ_{t,i} u_{t,i} v_{t,i}^T, Manifold Retraction via Whitening: U+ = Y(Y^T Y)^{-1/2}, EBLoRA: Spectral Imbalance and Catastrophic Forgetting, Restricted Stiefel Manifold: M_t = {U ∈ R^{d×r} | U^TU = I_r, G_{t-1}^T U = 0} (+45 more)

### Community 3 - "Mechanistic Interpretability"
Cohesion: 0.08
Nodes (51): LLaMA Models (2-7B, 3-8B), RoBERTa Models, ViT Models (B/32, B/16, L/14), Amplification Factor (AF) / Reverse AF, Burer-Monteiro Factorization, Common Subspace, Data-Parameter Interaction, Effective Rank (k_M) (+43 more)

### Community 4 - "Grokking & Phase Transitions"
Cohesion: 0.05
Nodes (46): Canonical TRS via QR+SVD, Forgetting Geometry Theorem, Four-Way Spectral Decomposition, Genuine TRS, Zero-Shot LoRA Audit via LoL + TRS, MP Bulk, Spectral-Population Duality, Near-zero Suppression Dimensions (+38 more)

### Community 5 - "RMT & Heavy Tails"
Cohesion: 0.06
Nodes (44): Interpretability in Parameter Space: APD (Attribution-based Parameter Decomposition), Bilinear MLPs Enable Weight-Based Mechanistic Interpretability, Block-Level Adaptation (mtLoRA), Deterministic Equivalent for Feature Covariance, Fiber Bundle Framework for Weight Space, Fine-Grained Routing (mtLoRA), Geometry of Neural Net Parameter Spaces Under Reparametrization (Kristiadi et al.), Learning in the Fisher Subspace: Guided Initialization for LoRA (+36 more)

### Community 6 - "Forgetting & Continual Learning"
Cohesion: 0.06
Nodes (41): Fiber Bundle Structure of Weight Space, Fisher Metric Connection, Universal Subspace = Flat Fiber Directions Zero Holonomy Conjecture (Idea 26), Four-Way Spectral Decomposition of LoRA (genuine TRS / intruder / bulk / suppression), Holonomy as Task Interference Measure, Holonomy-Intruder Duality (Idea 22), Intruder Dimensions (LoRA B matrix new directions), Marchenko-Pastur Null Distribution for TRS (+33 more)

### Community 7 - "Task Arithmetic & Composition"
Cohesion: 0.07
Nodes (38): Anti-Grokking: Late-Stage Generalization Collapse, Barabasi-Albert Scale-Free Network, Competing Near-Zero-Loss Solution Basins (Grokking Mechanism), Correlation Traps (Anomalous Eigenvalues in Randomized Weight Matrices), DevInterp Package (LLC Estimation Tool), Dimensional Phase Transition in Neural Networks, Effective Dimensionality D (FSS Exponent of Gradient Avalanche Dynamics), Empirical Spectral Density (ESD) of Layer Weight Matrices (+30 more)

### Community 8 - "Fiber Bundle & Holonomy"
Cohesion: 0.08
Nodes (38): Low-Rank Adaptation (LoRA) for Parameter-Efficient Fine-Tuning, Model Merging Without Extra Training, Singular Value Decomposition Applied to Weight Space Analysis, Task Interference in Multi-Task Model Merging, DARE Merging (Yu et al. 2024), Iso-CTS Merging (Marczak et al. 2025), Model Merging (Weight Space Addition), Spectral Over-Accumulation in Model Merging (Li et al. 2026) (+30 more)

### Community 9 - "Universal Subspace"
Cohesion: 0.08
Nodes (36): Catastrophic Forgetting / Pre-training Distribution Forgetting, Continual Learning with LoRA vs Full Fine-tuning, Effective Rank of LoRA Update Matrix, Full Fine-tuning, Algorithm for Finding Intruder Dimensions, Intruder Dimensions, Intruder Dimension Scaling Experiment (Causal Intervention), LLaMA-2-7B Evaluation Model (+28 more)

### Community 10 - "Fisher & Natural Gradient"
Cohesion: 0.09
Nodes (33): Decoder W_qk Skew-Symmetry (Non-Zero Curvature) → More Intruder Dims in Tight-Rank LoRA Fine-tuning, EWC Diagonal Fisher Approximation Limitation: Misses Off-Diagonal Curvature → Residual Forgetting, EWC as Horizontal Subbundle Constraint (Fisher penalty = stay in ker(ω)), EWC-LoRA: Full-Dimensional FIM over ΔW=AB (not A,B separately) for Accurate Fisher Estimation, EWC-LoRA Proposition 1: Separate Regularization of A,B ≠ Full-Space Regularization of ΔW, EWC-LoRA Proposition 3: Empirical FIM over ΔW Induces Constraints on Low-Rank Factors A,B, EWC-LoRA Achieves Flexible Stability–Plasticity Trade-off via Tunable λ (Outperforms Vanilla LoRA by 8.92%), EWC-LoRA = Fisher Regularization on the TRS Object ΔW (Complementary to TRS Spectral Decomposition) (+25 more)

### Community 11 - "Community 11"
Cohesion: 0.1
Nodes (31): Projection Mismatch (Inter-task Interference Measure), Singular Value Inflation (from Cross-Task Alignment), Subspace Overlap (Column-Space Overlap in Merged Basis), Bulk Spectrum (Noise Floor in Weight Matrices), Zeroing Small Singular Values as Denoising (LASER insight), Eigenvalue Distribution in Weight Matrices (Bulk vs. Signal), LASER: Layer-Selective Rank Reduction (Sharma et al. 2023), SNR-Based Layer Selection for Targeted Training (+23 more)

### Community 12 - "Community 12"
Cohesion: 0.07
Nodes (30): Feature Learning Theory (cross-paper: RMT + empirical convergence), Mechanistic Interpretability (cross-paper: circuits + features + universality), Cross-Architecture Feature Similarity (avg MPPC=0.74), Depth Specialization (layer l in Pythia ~ layer 2l in Mamba), Induction Circuit ([A][B]...[A]->predict[B]), Local Convolution Layer (Mamba preprocessing), Mamba-130M (SSM model), Mamba SSM Induction (layer 17 SSM + local convolution) (+22 more)

### Community 13 - "Community 13"
Cohesion: 0.13
Nodes (24): Anti-Grokking: Late-Stage Generalization Collapse (α < 2 after 10^7 steps), Correlation Traps (Anomalous Eigenvalues in W^rand ESD), Effective Dimensionality D (FSS Exponent: s_max ~ N^D), Empirical Spectral Density (ESD) and Marchenko-Pastur Distribution, Generalisation Basin (Low-LLC, Structured Algorithmic Solution), Grokking as Bayesian Phase Transition between Competing Basins, Grokking as Dimensional Phase Transition (D crosses 1 at critical point), Grokking Severity Measure (GSM): Negatively Correlated with Learning Rate (+16 more)

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
Cohesion: 0.13
Nodes (17): ARC-Easy-LoRA Dataset (10,000 LoRA checkpoints), CelebA-LoRA Dataset (10,177 LoRA checkpoints), CUB-LoRA Dataset (11,788 LoRA checkpoints), GL(r)-Invariance Proposition (Proposition 3.1), GoEmotions-LoRA Dataset (20,000 LoRA checkpoints), Hu et al. 2022 (LoRA Original Paper), Kaushik et al. 2025 (EigenLoRAx), Low-Rank Adaptation (LoRA) (+9 more)

### Community 21 - "Community 21"
Cohesion: 0.18
Nodes (13): Activation Covariance Eigenvectorâ€“Singular Vector Overlap, Lazy Learning Regime in Transformer Pretraining, Marchenko-Pastur (MP) Law for Weight Matrix Spectra, Minimal Random Matrix Model for Small Singular Value Outliers, Random Matrix Theory as Zero-Information Null Hypothesis for Weights, Small Singular Values Encode Learned Information in Transformers, SVD-Based Pruning and Compression Guidance for LLMs, Low-Rank Adaptation (LoRA) (+5 more)

### Community 22 - "Community 22"
Cohesion: 0.2
Nodes (12): Aggregation-Aware Null Calibration, Aristotelian Representation Hypothesis, Centered Kernel Alignment (CKA), Depth Confounder in Representational Similarity, Local Neighborhood Convergence Across Modalities, Mutual k-Nearest Neighbors (mKNN), Permutation-Based Null-Calibration Framework, Platonic Representation Hypothesis (+4 more)

### Community 23 - "Community 23"
Cohesion: 0.18
Nodes (12): Federated Learning via Weight Space Generation, Functional Invariance in Weight Space, HyperDreamBooth (Hypernetwork for LoRA Initialization), Hypernetworks for Weight Space Generation, Implicit Neural Representations (INRs), Model Unification via Weight Space, Neural Architecture Search via Weight Space Generation, Neuron Permutation Invariance (+4 more)

### Community 24 - "Community 24"
Cohesion: 0.2
Nodes (12): Eilertsen et al. 2020 (Classifying the Classifier), Kofinas et al. 2024 (Neural Graph - NG), Model Zoo Benchmarks for WSL, Navon et al. 2023 (DWSNets), Unterthiner et al. 2020 (Predicting NN Accuracy from Weights), Functional Invariance and Equivariance in Weight Space, Hypernetworks for Weight Space Generation, A Survey of Weight Space Learning: Understanding, Representation, and Generation (+4 more)

### Community 25 - "Community 25"
Cohesion: 0.2
Nodes (11): A Matrix Seed Variation as Cross-Seed Robustness Ablation, AdaLoRA Paper, AsymmetryOfLoRA Paper, B Matrix Clusters by Task; A Matrix Does Not, Canonical Representation: SVD Spectrum of B per Layer with Importance Weighting, Effective Rank as Confound and Covariate Control, Concrete Experiment 1 Design Changes Table, FFN Top Layers Carry More Task-Specific Singular Values (+3 more)

### Community 26 - "Community 26"
Cohesion: 0.24
Nodes (10): Singular Statistical Models (Non-identifiable Neural Networks), Arrhenius Reaction Rate Hypothesis for Grokking Time, SLT Free Energy (Fn) for Phase Transition Timing, Grokking: Delayed Generalization Phase Transition, Local Learning Coefficient (LLC) as Complexity Measure, Modulo Arithmetic Network (Grokking Testbed), Using SLT to Understand Grokking and Phase Transitions in Neural Networks, Stochastic Gradient Langevin Dynamics (SGLD) for LLC Estimation (+2 more)

### Community 27 - "Community 27"
Cohesion: 0.29
Nodes (10): Q/K vs V/O Spectral Asymmetry in TRS (Idea 23), Spectral Lifecycle of Transformer Training: Q/K vs V/O Asymmetry (arXiv:2604.22778), Autoregressive Training Induces Column Dominance / Directionality in W_qk (Theorem 2.3), Bidirectional Training Induces Symmetry in W_qk (Theorem 2.4), Underlying Structures of Self-Attention: Symmetry, Directionality, Emergent Dynamics (arXiv:2502.10927), Symmetry Score and Directionality Score for Square Matrices (Definitions 3.1-3.2), W_qk = W_q * W_k^T as Bilinear Form Defining Metric in Embedding Space, Claim 6: V-layer TRS Dominance (Synthesis 3) (+2 more)

### Community 28 - "Community 28"
Cohesion: 0.32
Nodes (8): Cross-Architecture Subspace Gap, Foundation Models as Objects in Weight Space, Implicit Regularization via Shared Subspace, LoRA as Universal Low-Rank Adaptation Module for WSL, Open Question: Universal Architecture-Agnostic Weight Space Learner, Spectral Bias of Neural Networks (Low-Frequency Learning), Universal Subspace for Model Compression (100x Memory Reduction), Universal Weight Subspace

### Community 29 - "Community 29"
Cohesion: 0.29
Nodes (8): Deep Weight-Space Networks (DWSNets), Functional Equivariance in Weight Space, GLNet (GL(r)-Equivariant Baseline for LoRA), Graph Metanetworks (GMNs) for Weight Space, Model-Based Weight Space Representation, Neural Functional Networks (NFN), Scale-GMN (Scaling + Permutation Equivariant GNN), Universal Neural Functionals (UNFs)

### Community 30 - "Community 30"
Cohesion: 0.29
Nodes (7): Benchmark Score Invariant to Large Family of Weight-Space Transformations, Behavioral Signal (Benchmark Score Vector), Benchmark Evaluation Pipeline, Dual-Signal Framing (Weight-Space + Behavioral Combined), LoRA Training Pipeline (Infrastructure), Weight-Space Representation Extraction Method, Weight-Space Signal (LoRA Parameter Coordinate)

### Community 31 - "Community 31"
Cohesion: 0.38
Nodes (7): Induction Circuits in Transformers and Mamba, Mamba State Space Model Architecture, Max Pairwise Pearson Correlation (MPPC) Feature Similarity Metric, Off-by-One Preference Motif in Mamba SSM, Towards Universality: Studying Mechanistic Similarity Across Language Model Architectures, Sparse Autoencoders (SAEs) for Interpretable Feature Extraction, Universality Hypothesis in Mechanistic Interpretability

### Community 32 - "Community 32"
Cohesion: 0.6
Nodes (5): Diffusion-Based Weight Generation, DnD (Diffusion for LoRA via Task Vectors), Generative Models for Weight Space Generation, ICM-LoRA (Conditional VAE for LoRA Weights), SANE (Sequential Autoencoding for Network Weights)

### Community 33 - "Community 33"
Cohesion: 0.5
Nodes (4): BIG_IDEAS Synthesis Document, Night Run 2 Critical Revision Document, Literature Findings Document, Running Synthesis Document

### Community 34 - "Community 34"
Cohesion: 0.67
Nodes (3): Spectral Stability of Non-Dominant Subspace During Fine-Tuning, Task-Specific Knowledge Injected Into Low-Dimensional Subspace, Top Singular Vectors Reorient During Fine-Tuning

### Community 35 - "Community 35"
Cohesion: 0.67
Nodes (3): 2D Layer Selection Map (alpha x TRS), AlphaLoRA HT-SR Layer Quality (2410.10054), Spectrum MP-null Layer Selection (2406.06623)

## Knowledge Gaps
- **268 isolated node(s):** `NeurIPS Workshop Target Venue`, `LoRA Training Pipeline (Infrastructure)`, `Benchmark Evaluation Pipeline`, `Weight-Space Representation Extraction Method`, `Predictive Demonstration (Downstream Task)` (+263 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **16 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.