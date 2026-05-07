# Graph Report - finding_literature  (2026-05-07)

## Corpus Check
- 50 files · ~500,000 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 786 nodes · 1083 edges · 54 communities (39 shown, 15 thin omitted)
- Extraction: 78% EXTRACTED · 17% INFERRED · 0% AMBIGUOUS · INFERRED: 189 edges (avg confidence: 0.83)
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
- [[_COMMUNITY_Fiber Bundle & Geometry|Fiber Bundle & Geometry]]
- [[_COMMUNITY_Universal Subspace|Universal Subspace]]
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
- **Three Papers Converge on SVD Spectrum of B as Canonical Representation** — lora_insights_asymmetry_paper, lora_insights_adalora_paper, lora_insights_symmetries_wsl_paper [EXTRACTED 1.00]
- **Width and Depth Confounders Both Addressed by Null-Calibration** —  [EXTRACTED 1.00]
- **LoRA introduces intruder dimensions via low-rank matrix product, which distort spectral structure and cause catastrophic forgetting** — lora_vs_fullft_lora_method, lora_vs_fullft_intruder_dimensions, lora_vs_fullft_catastrophic_forgetting, lora_vs_fullft_svd_analysis [EXTRACTED 1.00]
- **Both papers address the gap between weight-space/spectral structure and functional behavior: LoRA intruder dimensions reveal hidden behavioral differences; FuLA reveals that activation-space alignment is necessary for true functional similarity** — lora_vs_fullft_intruder_dimensions, lora_vs_fullft_spectral_properties, model_stitching_fula_functional_similarity, model_stitching_fula_affine_transformation [INFERRED 0.75]
- **Task-based stitching methods (TLM, SLM) fabricate functional alignment by overfitting to task cues, while FuLA avoids this with task-agnostic functional hints** — model_stitching_fula_method, model_stitching_fula_task_loss_matching, model_stitching_fula_fabricated_alignment, model_stitching_fula_functional_hints [EXTRACTED 1.00]
- **Spectral Analysis of Neural Network Weights: Shared Theme Across Papers** —  [INFERRED 0.85]
- **LoRA, SpecLoRA and PEFT: Low-Rank Spectral Fine-Tuning** —  [EXTRACTED 1.00]
- **TRS Core: MP Null + Intruder Dims + Universal Subspace define Genuine TRS** — big_ideas_trs, big_ideas_intruder_dims, big_ideas_universal_subspace, big_ideas_genuine_trs [EXTRACTED 0.95]
- **Forgetting Triangle: TRS Distance + Subspace Geometry + EBLoRA Imbalance all govern catastrophic forgetting** — big_ideas_forgetting_geometry, eblora_spectral_imbalance, big_ideas_trs_continual_curriculum [INFERRED 0.85]
- **Cross-Architecture TRS Validity requires controlling Spectral Maturity (HTMP phase) and Intrinsic Dimension Profile** — spikes_to_ht_spectral_maturity, big_ideas_trs_htmp, gelora_intrinsic_dim [INFERRED 0.75]
- **Four-Way Spectral Decomposition Framework** —  [0.95]
- **Spectral-Population Duality: TRS and Population PCA** —  [0.75]
- **Fiber Bundle Geometric Framework for Weight Space** —  [0.75]

## Communities (54 total, 15 thin omitted)

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
Cohesion: 0.06
Nodes (51): Low-Rank Adaptation (LoRA) for Parameter-Efficient Fine-Tuning, Model Merging Without Extra Training, Singular Value Decomposition Applied to Weight Space Analysis, Task Interference in Multi-Task Model Merging, DARE Merging (Yu et al. 2024), Iso-CTS Merging (Marczak et al. 2025), Model Merging (Weight Space Addition), Spectral Over-Accumulation in Model Merging (Li et al. 2026) (+43 more)

### Community 5 - "RMT & Heavy Tails"
Cohesion: 0.06
Nodes (44): Interpretability in Parameter Space: APD (Attribution-based Parameter Decomposition), Bilinear MLPs Enable Weight-Based Mechanistic Interpretability, Block-Level Adaptation (mtLoRA), Deterministic Equivalent for Feature Covariance, Fiber Bundle Framework for Weight Space, Fine-Grained Routing (mtLoRA), Geometry of Neural Net Parameter Spaces Under Reparametrization (Kristiadi et al.), Learning in the Fisher Subspace: Guided Initialization for LoRA (+36 more)

### Community 6 - "Forgetting & Continual Learning"
Cohesion: 0.07
Nodes (38): Anti-Grokking: Late-Stage Generalization Collapse, Barabasi-Albert Scale-Free Network, Competing Near-Zero-Loss Solution Basins (Grokking Mechanism), Correlation Traps (Anomalous Eigenvalues in Randomized Weight Matrices), DevInterp Package (LLC Estimation Tool), Dimensional Phase Transition in Neural Networks, Effective Dimensionality D (FSS Exponent of Gradient Avalanche Dynamics), Empirical Spectral Density (ESD) of Layer Weight Matrices (+30 more)

### Community 7 - "Task Arithmetic & Composition"
Cohesion: 0.08
Nodes (36): Catastrophic Forgetting / Pre-training Distribution Forgetting, Continual Learning with LoRA vs Full Fine-tuning, Effective Rank of LoRA Update Matrix, Full Fine-tuning, Algorithm for Finding Intruder Dimensions, Intruder Dimensions, Intruder Dimension Scaling Experiment (Causal Intervention), LLaMA-2-7B Evaluation Model (+28 more)

### Community 8 - "Fiber Bundle & Geometry"
Cohesion: 0.07
Nodes (30): Feature Learning Theory (cross-paper: RMT + empirical convergence), Mechanistic Interpretability (cross-paper: circuits + features + universality), Cross-Architecture Feature Similarity (avg MPPC=0.74), Depth Specialization (layer l in Pythia ~ layer 2l in Mamba), Induction Circuit ([A][B]...[A]->predict[B]), Local Convolution Layer (Mamba preprocessing), Mamba-130M (SSM model), Mamba SSM Induction (layer 17 SSM + local convolution) (+22 more)

### Community 9 - "Universal Subspace"
Cohesion: 0.13
Nodes (24): Anti-Grokking: Late-Stage Generalization Collapse (α < 2 after 10^7 steps), Correlation Traps (Anomalous Eigenvalues in W^rand ESD), Effective Dimensionality D (FSS Exponent: s_max ~ N^D), Empirical Spectral Density (ESD) and Marchenko-Pastur Distribution, Generalisation Basin (Low-LLC, Structured Algorithmic Solution), Grokking as Bayesian Phase Transition between Competing Basins, Grokking as Dimensional Phase Transition (D crosses 1 at critical point), Grokking Severity Measure (GSM): Negatively Correlated with Learning Rate (+16 more)

### Community 10 - "Community 10"
Cohesion: 0.14
Nodes (21): Algebraic Geometry (Foundation of SLT), Arrhenius Reaction Rate Hypothesis for Grokking, Autoencoder Bottleneck Dimension LLC Scaling, SLT Free Energy (Fn), Grokking (Delayed Generalization), Lau et al. 2023: Local Learning Coefficient (LLC) Paper, Local Learning Coefficient (LLC), Low-Rank Matrix Factorization Network LLC Experiment (+13 more)

### Community 11 - "Community 11"
Cohesion: 0.12
Nodes (21): Large-Scale Analysis: 1100+ Models (500 Mistral LoRAs, 500 ViTs, 50 LLaMA-8B), DARE-TIES Merging, EigenLoRAx (Recycling Adapters for Principal Subspaces), Truncated Zero-Centered Higher-Order SVD (HOSVD), KnOTS-TIES Merging (SVD-based Subspace Alignment), 50 LLaMA3-8B Models Subspace Analysis, Lottery Ticket Hypothesis, 500 Mistral-7B LoRA Models Subspace Analysis (+13 more)

### Community 12 - "Community 12"
Cohesion: 0.15
Nodes (20): FILet Algorithm (Fisher-Guided LoRA Initialization via Minimum Fisher Energy), Fisher Energy E(Z) for LoRA Direction Selection, Fisher Merging as Tractable Mahalanobis/Fréchet Surrogate, Fisher-Rao Geodesic Distance and Fisher Information Matrix, Fréchet Mean on Riemannian Manifold, GeoMerge Algorithm (Riemannian/Quotient Merging of LoRA Adapters), K-FAC Kronecker-Factored Fisher Approximation (S_W ≈ S_X ⊗ S_Y), LoRA Interference (Parameter-Data Interaction across Tasks Causing Merge Conflicts) (+12 more)

### Community 13 - "Community 13"
Cohesion: 0.12
Nodes (20): LoRA: Low-Rank Adaptation of Large Language Models (Hu et al. 2021), Eigenvector-Based LoRA Initialization via Sample Covariance, LoRA Subspace Constraint Before Fine-Tuning, OSRM: Orthogonal Subspaces for Robust Model Merging, Parameter-Data Interaction in LoRA Model Merging, Low-Rank LoRA Solution Generalization Guarantee, Low-Rank Solution Existence for Full Fine-Tuning in NTK Regime, No Spurious Local Minima in LoRA with Sufficient Rank (+12 more)

### Community 14 - "Community 14"
Cohesion: 0.16
Nodes (19): Bulk+Spike ESD: MP Bulk with Outlier Singular Value After Large η Step, Empirical Spectral Density (ESD) of Weight Matrices, Five+One Training Phases: Random→Bleeding-Out→Bulk+Spike→Bulk-Decay→Heavy-Tailed→Rank Collapse, Good Generalization: PL_Alpha_Hill in Range (2, 2.5), HT-MU: Heavy-Tailed Self-Regularization Framework, Kernel Target Alignment (KTA): Feature Learning Quality Metric, From Spikes to Heavy Tails: Spectral Evolution of Weight Matrices, Power-Law Exponent (PL_Alpha_Hill, PL_Alpha_KS) for Tail Heaviness (+11 more)

### Community 15 - "Community 15"
Cohesion: 0.18
Nodes (18): Projection Mismatch (Inter-task Interference Measure), Subspace Overlap (Column-Space Overlap in Merged Basis), Biderman et al. 2024: LoRA Learns Less and Forgets Less, Catastrophic Forgetting in Continual Learning, Continual Learning (Sequential Task Training), Effective Rank (Entropy-Based) of LoRA Gradient Matrices, Geometric Forgetting Law: F = alpha*(1 - cos^2(theta_min)) + beta, Gradient Projection Memory (GPM) (+10 more)

### Community 16 - "Community 16"
Cohesion: 0.13
Nodes (18): Base-Model Transfer (SD1.4 to SD1.5) in W2T, Behavior Prediction from Weight Representations, Model Editing via Weight Space, Model-Free (Probe-Based) Weight Space Representation, Model Retrieval in Weight Space, Position-Level Transformer (f_pos) in W2T, ProbeGen (Deep Linear Probe Generator), ProbeLog (Probe-Based Model Representation) (+10 more)

### Community 17 - "Community 17"
Cohesion: 0.13
Nodes (17): ARC-Easy-LoRA Dataset (10,000 LoRA checkpoints), CelebA-LoRA Dataset (10,177 LoRA checkpoints), CUB-LoRA Dataset (11,788 LoRA checkpoints), GL(r)-Invariance Proposition (Proposition 3.1), GoEmotions-LoRA Dataset (20,000 LoRA checkpoints), Hu et al. 2022 (LoRA Original Paper), Kaushik et al. 2025 (EigenLoRAx), Low-Rank Adaptation (LoRA) (+9 more)

### Community 18 - "Community 18"
Cohesion: 0.17
Nodes (15): Eilertsen et al. 2020 (Classifying the Classifier), Foundation Models as Objects in Weight Space, Kofinas et al. 2024 (Neural Graph - NG), LoRA as Universal Low-Rank Adaptation Module for WSL, Model Zoo Benchmarks for WSL, Navon et al. 2023 (DWSNets), Open Question: Universal Architecture-Agnostic Weight Space Learner, Unterthiner et al. 2020 (Predicting NN Accuracy from Weights) (+7 more)

### Community 19 - "Community 19"
Cohesion: 0.18
Nodes (13): Activation Covariance Eigenvectorâ€“Singular Vector Overlap, Lazy Learning Regime in Transformer Pretraining, Marchenko-Pastur (MP) Law for Weight Matrix Spectra, Minimal Random Matrix Model for Small Singular Value Outliers, Random Matrix Theory as Zero-Information Null Hypothesis for Weights, Small Singular Values Encode Learned Information in Transformers, SVD-Based Pruning and Compression Guidance for LLMs, Low-Rank Adaptation (LoRA) (+5 more)

### Community 20 - "Community 20"
Cohesion: 0.2
Nodes (12): Aggregation-Aware Null Calibration, Aristotelian Representation Hypothesis, Centered Kernel Alignment (CKA), Depth Confounder in Representational Similarity, Local Neighborhood Convergence Across Modalities, Mutual k-Nearest Neighbors (mKNN), Permutation-Based Null-Calibration Framework, Platonic Representation Hypothesis (+4 more)

### Community 21 - "Community 21"
Cohesion: 0.18
Nodes (12): Deep Weight-Space Networks (DWSNets), Functional Equivariance in Weight Space, Functional Invariance in Weight Space, GLNet (GL(r)-Equivariant Baseline for LoRA), Graph Metanetworks (GMNs) for Weight Space, Model-Based Weight Space Representation, Neuron Permutation Invariance, Neural Functional Networks (NFN) (+4 more)

### Community 22 - "Community 22"
Cohesion: 0.2
Nodes (12): Diffusion-Based Weight Generation, DnD (Diffusion for LoRA via Task Vectors), Federated Learning via Weight Space Generation, Generative Models for Weight Space Generation, HyperDreamBooth (Hypernetwork for LoRA Initialization), Hypernetworks for Weight Space Generation, ICM-LoRA (Conditional VAE for LoRA Weights), Implicit Neural Representations (INRs) (+4 more)

### Community 23 - "Community 23"
Cohesion: 0.2
Nodes (11): A Matrix Seed Variation as Cross-Seed Robustness Ablation, AdaLoRA Paper, AsymmetryOfLoRA Paper, B Matrix Clusters by Task; A Matrix Does Not, Canonical Representation: SVD Spectrum of B per Layer with Importance Weighting, Effective Rank as Confound and Covariate Control, Concrete Experiment 1 Design Changes Table, FFN Top Layers Carry More Task-Specific Singular Values (+3 more)

### Community 24 - "Community 24"
Cohesion: 0.24
Nodes (10): Singular Statistical Models (Non-identifiable Neural Networks), Arrhenius Reaction Rate Hypothesis for Grokking Time, SLT Free Energy (Fn) for Phase Transition Timing, Grokking: Delayed Generalization Phase Transition, Local Learning Coefficient (LLC) as Complexity Measure, Modulo Arithmetic Network (Grokking Testbed), Using SLT to Understand Grokking and Phase Transitions in Neural Networks, Stochastic Gradient Langevin Dynamics (SGLD) for LLC Estimation (+2 more)

### Community 25 - "Community 25"
Cohesion: 0.22
Nodes (9): Fiber Bundle Structure of Weight Space, Fisher Metric Connection, Holonomy as Task Interference Measure, Intruder Dimensions, MiLoRA Paradox and Resolution, Platonic Weight Space Hypothesis, Frechet Averages Quotient Manifold (2604.27155), LoRA vs Full Fine-tuning Intruder Dimensions (2410.21228) (+1 more)

### Community 26 - "Community 26"
Cohesion: 0.22
Nodes (9): Task Residual Spectrum (TRS), TRS as Optimal Bayes Estimator, GradientSpace SVD Task Clusters (2512.06678), No Task Left Behind Isotropic Merging (2502.04959), mtLoRA Spectral Task Regularization (2603.01526), Small Singular Values Matter RMT (2410.17770), Spectral Over-Accumulation Merging (2602.05536), Spiked RMT Task Learning Features (2410.18938) (+1 more)

### Community 27 - "Community 27"
Cohesion: 0.32
Nodes (8): Forgetting Geometry Theorem, TRS-based Continual Learning Curriculum, Weight Disentanglement via TRS Orthogonality, Gradient Orthogonality Constraint (EBLoRA), EBLoRA Spectral Imbalance Forgetting (2602.00722), Spectral Imbalance in LoRA Updates, Stiefel Manifold Optimization for Balanced LoRA, Subspace Geometry Catastrophic Forgetting (2603.02224)

### Community 28 - "Community 28"
Cohesion: 0.29
Nodes (8): Universal Weight Subspace, D2C Iterative Clustering Algorithm, D2C Data-Driven Adapter Clustering and Merging (2601.17441), SVD Features for LoRA Clustering, EigenLoRAx Recycling Adapters Principal Subspace (2502.04700), EigenLoRAx Task-Invariant Principal Subspace, EigenLoRAx Generalization Bound Theorem 3.6, Universal Weight Subspace Hypothesis (2512.05117)

### Community 29 - "Community 29"
Cohesion: 0.29
Nodes (7): Benchmark Score Invariant to Large Family of Weight-Space Transformations, Behavioral Signal (Benchmark Score Vector), Benchmark Evaluation Pipeline, Dual-Signal Framing (Weight-Space + Behavioral Combined), LoRA Training Pipeline (Infrastructure), Weight-Space Representation Extraction Method, Weight-Space Signal (LoRA Parameter Coordinate)

### Community 30 - "Community 30"
Cohesion: 0.29
Nodes (7): Cross-Architecture Subspace Gap, Implicit Regularization via Shared Subspace, Rank-Wise Singular Decomposition as Canonical Object of LoRA, Spectral Bias of Neural Networks (Low-Frequency Learning), Universal Subspace for Model Compression (100x Memory Reduction), Universal Weight Subspace, W2T Tokenization (Rank-Component to Token Mapping)

### Community 31 - "Community 31"
Cohesion: 0.38
Nodes (7): Induction Circuits in Transformers and Mamba, Mamba State Space Model Architecture, Max Pairwise Pearson Correlation (MPPC) Feature Similarity Metric, Off-by-One Preference Motif in Mamba SSM, Towards Universality: Studying Mechanistic Similarity Across Language Model Architectures, Sparse Autoencoders (SAEs) for Interpretable Feature Extraction, Universality Hypothesis in Mechanistic Interpretability

### Community 32 - "Community 32"
Cohesion: 0.33
Nodes (6): LoRA-WiSE Benchmark, DSiRe Dataset Size Recovery from LoRA (2406.19395), LoRA Spectrum Encodes Dataset Size, Intrinsic Dimensionality Profile Across Layers, GeLoRA Geometric Adaptive Ranks Intrinsic Dim (2412.09250), GeLoRA Rank Bound Theorem 3.2

### Community 33 - "Community 33"
Cohesion: 0.33
Nodes (6): Four-Way Spectral Decomposition, Genuine TRS, MP Bulk, Spectral-Population Duality, Near-zero Suppression Dimensions, Subspace-Boosted Merging Rank Collapse (2506.16506)

### Community 34 - "Community 34"
Cohesion: 0.4
Nodes (5): TRS_HTMP Next-Generation Fingerprint, HTMP Heavy-Tailed Mechanistic Universality (2506.03470), From Spikes to Heavy Tails Spectral Evolution (2406.04657), MP to Spike to Heavy-Tail ESD Pathway, Spectral Maturity Cross-Architecture Confound

### Community 35 - "Community 35"
Cohesion: 0.5
Nodes (4): Canonical TRS via QR+SVD, Zero-Shot LoRA Audit via LoL + TRS, Learning on LoRAs GL-Equivariant (2410.04207), W2T LoRA Weights Know Task (2603.15990)

### Community 36 - "Community 36"
Cohesion: 0.5
Nodes (4): BIG_IDEAS Synthesis Document, Night Run 2 Critical Revision Document, Literature Findings Document, Running Synthesis Document

### Community 37 - "Community 37"
Cohesion: 0.67
Nodes (3): Spectral Stability of Non-Dominant Subspace During Fine-Tuning, Task-Specific Knowledge Injected Into Low-Dimensional Subspace, Top Singular Vectors Reorient During Fine-Tuning

### Community 38 - "Community 38"
Cohesion: 0.67
Nodes (3): 2D Layer Selection Map (alpha x TRS), AlphaLoRA HT-SR Layer Quality (2410.10054), Spectrum MP-null Layer Selection (2406.06623)

## Knowledge Gaps
- **253 isolated node(s):** `NeurIPS Workshop Target Venue`, `LoRA Training Pipeline (Infrastructure)`, `Benchmark Evaluation Pipeline`, `Weight-Space Representation Extraction Method`, `Predictive Demonstration (Downstream Task)` (+248 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **15 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Marchenko-Pastur Distribution` connect `RMT & Heavy Tails` to `Community 10`, `Forgetting & Continual Learning`?**
  _High betweenness centrality (0.161) - this node is a cross-community bridge._
- **Why does `Local Learning Coefficient (LLC)` connect `Community 10` to `Community 15`?**
  _High betweenness centrality (0.155) - this node is a cross-community bridge._
- **Why does `Physics-Inspired Singular Learning Theory to Understand Grokking` connect `Community 10` to `RMT & Heavy Tails`?**
  _High betweenness centrality (0.152) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `A Survey of Weight Space Learning: Understanding, Representation, and Generation` (e.g. with `The Universal Weight Subspace Hypothesis` and `W2T: LoRA Weights Already Know What They Can Do`) actually correct?**
  _`A Survey of Weight Space Learning: Understanding, Representation, and Generation` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `Task Residual Spectrum (TRS)` (e.g. with `Subspace Geometry and Catastrophic Forgetting` and `Fisher Subspace`) actually correct?**
  _`Task Residual Spectrum (TRS)` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `Task Residual Spectrum (TRS)` (e.g. with `SVD Features for LoRA Clustering` and `LoRA Spectrum Encodes Dataset Size`) actually correct?**
  _`Task Residual Spectrum (TRS)` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `NeurIPS Workshop Target Venue`, `LoRA Training Pipeline (Infrastructure)`, `Benchmark Evaluation Pipeline` to the rest of the system?**
  _253 weakly-connected nodes found - possible documentation gaps or missing edges._