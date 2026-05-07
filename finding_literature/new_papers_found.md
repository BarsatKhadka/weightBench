# New Literature Found — Night Run, May 2026
*Updated: Iteration 3 additions appended below*

## Category 9: Gauge Theory / Holonomy in Neural Networks (NEW — Iteration 3)

**A Gauge Theory of Superposition: Toward a Sheaf-Theoretic Atlas of Neural Representations**
- arXiv:2603.00824 (Feb 2026)
- Replaces global dictionary model with sheaf-theoretic local semantic charts
- Uses holonomy over fundamental cycles in the context graph to certify interference bounds
- KEY: Proves holonomy is computable and gauge-invariant (after spanning-tree gauge fixing), non-trivial holonomy measures interference bounds on Llama-3.2-3B
- Closest paper to the fiber bundle gap: uses holonomy to certify task interference, but in representation space (input-space loops), not weight-space training trajectories
- **Gap remaining:** representation-space holonomy ≠ weight-space training holonomy

**Gauge-invariant Representation Holonomy**
- arXiv:2601.21653 (Jan 2026)
- Sevetlidis & Pavlidis
- Parallel-transports feature neighborhoods along loops in input space to compute holonomy metric
- Zero holonomy = flat (invariant) representations; non-zero = hidden curvature
- Invariant to orthogonal and affine transformations; correlates with adversarial robustness
- Provides concrete computational infrastructure for holonomy estimation
- **Application to weight space:** the parallel transport machinery can be adapted to weight-space loops if the right connection is specified

**Quotient Geometry, Effective Curvature, and Implicit Bias (Dong & Cheng)**
- arXiv:2603.21502 (Mar 2026)
- Confirmed: W/G quotient manifold with vertical/horizontal tangent decomposition
- Only the horizontal component contributes to first-order predictor evolution; vertical = gauge variation
- Does NOT use "principal fiber bundle" terminology but the structure is exactly that
- **Gap confirmed:** No holonomy, no parallel transport, no multi-task/continual learning analysis

## Category 11: EWC / Fisher Continual Learning Family (Iteration 5)

**Overcoming Catastrophic Forgetting in Neural Networks (EWC)**
- arXiv:1612.00796 (Kirkpatrick et al., 2017) — Nature
- Fisher penalty: L_B(θ) + Σᵢ (λ/2) Fᵢ (θᵢ - θᵢ^A)² 
- CRITICAL: F_i = curvature of Fisher metric at θ_A for dim i = vertical subbundle direction
- Bundle interpretation: EWC = "stay in the horizontal subbundle" = minimize intruder dims
- Every Fisher-based CL method is a special case of the bundle connection constraint

**EWC-LoRA: Revisiting Weight Regularization for Low-Rank Continual Learning**
- arXiv:2602.17559 (2026)
- Computes FIM over full-dimensional effective weight update ΔW = A·B, maps back to low-rank
- CRITICAL: This is Fisher regularization on the exact object TRS decomposes
- Prediction from our theory: EWC-LoRA reduces intruder_dim_score directly

**Synaptic Intelligence (SI)**
- arXiv:1703.04200 (Zenke et al., 2017)
- Path-integral Fisher: importance = integral of gradient dotted with weight-change trajectory
- Approximates the true Fisher bundle connection via the training path itself

**FOPNG: Fisher-Orthogonal Projected Natural Gradient**
- arXiv:2601.12816 (2026)
- Projects new-task gradients onto Fisher-metric orthogonal complement of previous-task gradients
- This IS Steele's zero-forgetting condition: θ_min = π/2 → F = β (minimum forgetting)
- Fisher-orthogonal = TRS-orthogonal = zero holonomy angle

**Natural Gradient Descent for Online Continual Learning**
- arXiv:2603.20898 (2026)  
- KFAC-based NGD curves loss landscape away from forgetting directions
- NGD = gradient along horizontal subbundle geodesic = natural horizontal trajectory
- Result: substantial improvements on Split CIFAR-100, CORE50, Split miniImageNet

## Category 12: Other Holonomy Applications (Iteration 5)

**RecBundle: Principal Bundle for Recommender Systems**
- arXiv:2603.16088 (Mar 2026)
- Uses principal bundle where holonomy quantifies user preference evolution via content drift
- CRITICAL: Another instance of principal bundle + holonomy = accumulated drift in parametric systems
- Cite as: fiber bundle + holonomy is a general tool, not ad hoc for neural networks

**Cross-LoRA: Data-Free Cross-Architecture LoRA Transfer**
- arXiv:2508.05232 (2025)
- Rank-truncated SVD + Frobenius-optimal linear transformation to align LoRA subspaces
- Closest paper to "cross-architecture LoRA transfer via spectral alignment"
- Validates cross-architecture TRS comparison via SVD-based subspace alignment

## Category 10: The 10 Priority Papers — Verification Results (Iteration 3)

All 10 arXiv IDs from synthesis_night_run_2 were VALID. Key corrections:
- arXiv:2412.00081 is "Task Singular Vectors: Reducing Task Interference in Model Merging" — about merging interference, not capability suppression during training (though closely related)
- arXiv:2512.05117 — "16-dim universal subspace" claim needs paper-body verification (abstract says "low-dimensional", not "16-dim" specifically)
- arXiv:2604.22778 — Q/K vs V/O spectral asymmetry: Q/K depth-dependent dynamics vs V/O uniform compression → four-way decomposition applies per projection type, not uniformly

## Category 1: Spectral Analysis / RMT on Real Weights

**Small Singular Values Matter: A Random Matrix Analysis of Transformer Models**
- arXiv:2410.17770 (Oct 2024)
- Uses MP as null; finds deviations at BOTH top AND bottom of spectrum are task-relevant
- CRITICAL: removing small (near-zero) singular values post-fine-tuning causes outsized performance collapse — more than removing mid-spectrum values
- Implication: the spectrum is TRIMODAL not bimodal. Near-zero ≠ noise.

**Approaching Deep Learning through the Spectral Dynamics of Weights**
- arXiv:2408.11804 (Aug 2024)
- Tracks SVD of weight matrices throughout training
- Unifies grokking, lottery tickets, loss surface structure via spectral evolution
- Weight decay acts geometrically to sharpen spectral structure

**The Spectral Lifecycle of Transformer Training**
- arXiv:2604.22778 (Apr 2026)
- Tracks full SVD every 25 steps, 30M–285M param models
- Discovers "transient compression waves" propagating depth-wise
- Q/K asymmetry vs V in spectral terms
- Rank and spectral SHAPE encode fundamentally different training information

## Category 2: LoRA Geometry and the Spectral Structure of Fine-tuning

**PiSSA: Principal Singular Values and Singular Vectors Adaptation**
- arXiv:2404.02948, NeurIPS 2024 Spotlight
- Initializes LoRA with principal singular components of pre-trained weights
- Outperforms standard LoRA across 12 models, 13 tasks
- Operational complement of TRS: if TRS is the theory, PiSSA is the practice

**LoRA vs Full Fine-tuning: An Illusion of Equivalence**
- arXiv:2410.21228 (Oct 2024) — CRITICAL PAPER
- Introduces "intruder dimensions": high-magnitude singular vectors in LoRA that are DISSIMILAR to pre-trained singular vectors
- Intruder dimensions concentrate catastrophic forgetting
- Suppressing intruder dimensions largely restores base model knowledge
- Implication for TRS: not all above-MP singular values are task signal. Need alignment criterion.

**Learning in the Fisher Subspace: Guided Initialization for LoRA**
- arXiv:2605.01046 (May 2026)
- Uses Fisher information matrix to identify task-relevant directions for LoRA init
- Bridges Fisher geometry and LoRA singular value spectrum directly

**LoRA Training in the NTK Regime Has No Spurious Local Minima**
- arXiv:2402.11867, ICML 2024
- Proves full fine-tuning admits low-rank solution of rank ~sqrt(N)
- LoRA with rank > sqrt(N) eliminates all spurious local minima
- First formal guarantee that LoRA's restricted movement is sufficient

## Category 3: Riemannian / Information Geometry on Weight Space

**The Geometry of Neural Nets' Parameter Spaces Under Reparametrization**
- arXiv:2302.07384, NeurIPS 2023
- Proves Fisher information metric is "always present" and cannot be removed
- Euclidean Hessian measures of flatness are coordinate-dependent and inconsistent
- Riemannian foundation for why singular directions are geometrically privileged

## Category 4: Grassmannian and Subspace Geometry

**The Universal Weight Subspace Hypothesis**
- arXiv:2512.05117 (Dec 2025) — MUST READ
- Analyzes 1,100+ models (500 Mistral-7B LoRAs, 500 ViTs, 50 LLaMA-8B)
- Diverse tasks concentrate weight updates in SHARED low-dimensional spectral subspaces
- Directly corroborates TRS universality claim

**No Task Left Behind: Isotropic Model Merging**
- arXiv:2502.04959 (Feb 2025)
- Subspace Alignment Ratio from top SVD singular vectors
- Grassmannian of leading singular subspaces as natural metric space for comparing models

## Category 5: Phase Transitions / Singular Learning Theory

**Using Physics-Inspired Singular Learning Theory to Understand Grokking**
- arXiv:2512.00686 (Dec 2025)
- Applies Watanabe's RLCT to predict phase transitions
- SLT implies: MP bulk = degenerate (uninformative) singular model
- Transitions ABOVE bulk signal change in geometric complexity

**Compressibility Measures Complexity: MDL Meets Singular Learning Theory**
- arXiv:2510.12077 (2025)
- MDL principle to singular models via SLT
- LLC (local learning coefficient) = geometric invariant of loss landscape
- Linearly correlated with compressibility across quantization, factorization

## Category 6: Mechanistic Interpretability in Weight Space

**Bilinear MLPs Enable Weight-Based Mechanistic Interpretability**
- arXiv:2410.08417, ICLR 2025
- Bilinear MLPs expressible as linear operations via third-order tensor
- Eigendecomposition of weights → interpretable low-rank structure
- Recover circuits directly from weight matrices, no activation datasets needed

**Interpretability in Parameter Space: APD (Attribution-based Parameter Decomposition)**
- arXiv:2501.14926 (2025)
- Decomposes network weights into mechanistic components
- Faithful, minimal, maximally simple decomposition
- "Parameters-first" approach bridging MDL and mechanistic interpretability

## Category 7: Model Stitching (Weight-Space Compatibility)

**Revisiting Model Stitching to Compare Neural Representations**
- arXiv:2106.07682, NeurIPS 2021
- Model stitching as stronger probe than CKA
- Operational meaning: whether one model's geometry is usable by another
- Implication: TRS cross-architecture universality can be tested via stitching

## Category 8: Lottery Ticket + Geometry

**Linear Mode Connectivity and the Lottery Ticket Hypothesis**
- arXiv:1912.05671, ICML 2020
- Winning tickets = stable to SGD noise in weight space
- Connects LMC geometry to subnetwork trainability

## Key Papers Already in Corpus (re-read deeply this session)

- **Knowledge is a Region in Weight Space** (Gueta et al., EMNLP 2023) — nested bounded convex regions at dataset/task/general levels
- **Task Arithmetic in the Tangent Space** (Ortiz-Jiménez et al., NeurIPS 2023 Oral) — weight disentanglement via NTK eigenfunction localization
- **weight2weights (w2w)** (Dravid et al., NeurIPS 2024) — weight space as meta-latent space, PCA manifold, linear edit directions
- **DEEP-ALIGN** (Navon et al., ICML 2024) — equivariant weight alignment, H=G×G symmetry, NP-hard but learnable
- **SSL on NN Weights** (Schürholt et al., NeurIPS 2021) — hyper-representations, permutation augmentation crucial
