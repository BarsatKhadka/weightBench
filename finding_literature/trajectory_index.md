# Trajectory Geometry of LoRA Fine-Tuning — Graph Index

**Purpose:** Graph-trackable index aligning the corpus with the thesis plan at `C:/Users/barsa/Documents/thesis_plan/plan.md`. Each node here points to a corpus paper relevant to the **trajectory direction** (E2 of the thesis plan).

**Companion document:** `observations_lora_lmc_program.md`
**Plan:** `C:/Users/barsa/Documents/thesis_plan/plan.md`

---

## The Trajectory Conjecture (one line)

Under the GL(r)-quotient, fine-tuning trajectories of LoRAs on the same task converge to a shared low-dimensional task subspace through a measurable phase structure, and the trajectory's *shape* — beyond its endpoint — predicts mergeability, forgetting, and generalization.

---

## Nodes by Function

### Endpoint baseline (E1 — Section 4 of the paper)

- **W2T canonical decomposition** → `w2t_lora_weights_know_capabilities.pdf`
  Provides the QR+SVD canonical map π that resolves GL(r) ambiguity. Used as the within-task collapse measurement.
- **AsymmetryOfLoRA / Hayou theory** → `arxiv_2406_08447.md`
  Theoretical anchor: B and A have intrinsically different LR scaling. Predicts B clusters by task across seeds (the within-task collapse claim at endpoints).
- **Structure Is Not Enough (Schurholt group)** → `arxiv_2503_17138.md`
  THE prior to differentiate from. Argues structure-only insufficient; we extend with GL(r)-canonical Region-2 coordinates and add trajectory.
- **Compress then Serve** → `arxiv_2407_00066.md`
  Joint diagonalization across thousands of LoRAs confirms shared subspace existence at scale.
- **EigenLoRAx** → `eigenloreax_recycling_adapters_principal_subspace.pdf`
  Task-invariant principal subspaces from a LoRA population.

### Trajectory / training-dynamics core (E2 — Section 5 of the paper)

- **Phase Transitions Model Zoo (Schurholt et al. 2025)** → `arxiv_2504_18072.md`
  Phase definitions for full models. We extend their phase machinery to LoRAs.
- **Tracking Feature Dynamics in LLM Training (SAE-Track)** → `arxiv_2412_17626.md`
  Tracks features across checkpoints. Three phases: Init/Warmup, Emergent, Convergent. **Direct competitor / foundation for E2.** Different unit (features vs subspaces).
- **RL vs SFT Spectral Dynamics** → `arxiv_2508_16546.md`
  SVD analysis showing direction shifts of singular vectors >> singular values, concentrated on largest+smallest SVs. Spectral trajectory observation.
- **Layer-wise Analysis of Supervised Fine-Tuning** → `arxiv_2604_11838.md`
  Depth-dependent adaptation pattern across 1B–32B models. Information-theoretic + geometric metrics. Layer-wise trajectory analysis.
- **Massive Supervised Fine-tuning Experiments** → `arxiv_2506_14681.md`
  Large-scale: log-likelihood vectors of fine-tuned models in shared latent space; checkpoints converge toward common region. Endpoint+behavior aggregate at scale.
- **Learning Dynamics of LLM Finetuning** → `arxiv_2407_10490.md`
  Foundational: how learning of specific examples influences other predictions.
- **Controlled LLM Training on Spectral Sphere (SSO)** → `arxiv_2601_08393.md`
  Constrained optimization in tangent space + retraction. Geometric trajectory framing.
- **Provable Scaling Laws of Feature Emergence from Grokking** → `arxiv_2509_21519.md`
  Three-stage grokking dynamics: lazy → independent feature learning → interactive. Theoretical anchor for trajectory phases.
- **Spectral Dynamics of Weights** → `spectral_dynamics_weights_grokking_rank.md`
  In-corpus already. Most direct full-network analog to LoRA trajectory work.
- **From Spikes to Heavy Tails** → `from_spikes_to_heavy_tails_spectral_evolution.pdf`
  5+1 spectral phases of training. Operationalize on LoRA trajectories.

### HT-SR foundations (the measurement instrument)

- **Martin & Mahoney HT-SR original (ICML 2019)** → `arxiv_1901_08276.md`
  Defines the 5+1 phases. Theoretical foundation. Mahoney is at Berkeley — direct US lineage.
- **Predicting NN Quality without Test Data (Nature Comms 2021)** → `www_nature_com_articles_s41467-021-24025-8.md`
  WeightWatcher's source paper. Per-layer alpha as quality measure. Methodology blueprint we extend to LoRAs.
- **AlphaLoRA HTSR Layer Quality** → `alphalore_htsr_rank_allocation.pdf`
  Applies HT-SR alpha to LoRA rank allocation. Shows alpha works on adapters.
- **Heavy-Tailed Mechanistic Universality (HTMP)** → `heavy_tailed_mechanistic_universality_htmp.pdf`
  Cross-architecture HT-SR claims.
- **WeightWatcher tool** → not a paper, but reference at github.com/CalculatedContent/WeightWatcher. The measurement instrument we use per checkpoint per layer.

### Mode connectivity foundation (E2's formal framework)

- **Linear Mode Connectivity (Frankle, Dziugaite, Roy, Carbin 2020)** → `arxiv_1912_05671.md`
  Formal cousin. SGD trajectories from same checkpoint converge to single connected basin.
- **Git Re-Basin (Ainsworth et al. 2022)** → `arxiv_2209_04836.md`
  Permutation-quotient version. Tells us how to write the GL(r)-quotient version.
- **Permutation Invariance and LMC (Entezari et al. 2021)** → `arxiv_2110_06296.md`
  Empirical core for full networks.
- **Linear Connectivity Reveals Generalization Strategies (Juneja et al. 2022)** → `arxiv_2205_12411.md`
  BERT fine-tunes can be linearly disconnected — the falsifier we now know about. Pretraining quality is the discriminator.
- **Mechanistic Mode Connectivity (Lubana et al. ICML 2023)** → `arxiv_2211_08422.md`
  THE formal framework for the "behavior vs mechanism" question. Lack of linear connectivity ⟹ dissimilar mechanisms.

### Implicit regularization (theoretical anchor for trajectory endpoint)

- **Gunasekar Implicit Regularization** → `implicit_regularization_matrix_factorization_gunasekar.md`
  GD on factorized matrix → minimum nuclear norm = sparse spectrum. Predicts which directions emerge first in trajectory.
- **LoRA Provably Converges to Low-Rank Global Minimum** → `lora_training_converges_lowrank_global_minimum.md`
  Endpoint convergence theorem.

### Predictive demonstration anchors (E2 — Section 6 of the paper)

- **Spectral Geometry of LoRA Adapters Encodes Training Objective** → `spectral_geometry_lora_adapters_training_objective.md`
  Spectrum predicts harmful compliance. Direct evidence trajectory features predict downstream behavior.
- **DSiRe (Dataset Size Recovery from LoRA Weights)** → `desire_dataset_size_recovery_lora_svd.pdf`
  Endpoint spectrum encodes training-data size. Trajectory should encode more.
- **Subspace Boosted Merging** → `subspace_boosted_model_merging_hosvd.md`
  Mergeability is predictable from subspace structure.
- **Spectral Over-Accumulation in Merging** → `spectral_over_accumulation_model_merging.md`
  Why merging fails — predictable from endpoint spectra.

### Cross-architecture (stretch — Section 5.5 of the paper)

- **Cross-LoRA: Data-Free LoRA Transfer** → `cross_lora_transfer_heterogeneous_llms.pdf`
  LoRA-Align: SVD subspace alignment + Frobenius-optimal linear. Methodology candidate ρ.
- **OrthoMerge** → `arxiv_2602_05943.md`
  Orthogonal Procrustes on Riemannian manifold. Best linear ρ.
- **Multi-Way Representation Alignment** → `arxiv_2602_06205.md`
  Generalized Procrustes Analysis for shared-orthogonal-universe.
- **CAST / Activation Manifold Projection** → `arxiv_2510_17902.md`
  Activation-space rival. Tests whether functional > structural for cross-arch.
- **TeleLoRA** → `arxiv_2503_20228.md`
  Cross-LLM LoRA alignment for Trojan mitigation. Closest existing cross-arch LoRA work.
- **LS-Merge (ICLR 2026)** → openreview-only, full PDF blocked. Non-linear autoencoder embedding.
- **Universal Weight Subspace Hypothesis** → `universal_weight_subspace_hypothesis.pdf`
  1100+ models share a subspace. Null hypothesis for cross-arch.

### Agent vision anchors (Section 7 / discussion / PhD pitch)

- **TeleLoRA** → `arxiv_2503_20228.md`
  Cross-LLM adapter teleportation. Closest existing "agent uses LoRA structure" work.
- **ProbeLog (Can this Model Also Recognize Dogs?)** → `arxiv_2502_09619.md`
  Zero-shot capability search from weights via probes.
- **Charting Hugging Face's Model Atlas** → `arxiv_2503_10633.md`
  Visionary positioning paper. The atlas frame for self-evolving agents.
- **Spin-glass derivation of MP** → `arxiv_1811_08298.md`
  Cross-domain depth: training trajectories in spin-glass language.
- **NN as Spin Models** → `arxiv_2408_06421.md`
  Glass-to-hidden-order phase transition during training. Physics-grounded trajectory framing.

---

## Critical Confirming Empirical Anchors

These empirical results from the corpus are what the trajectory paper hangs on:

- **ρ = 0.971** intruder dim count → forgetting (Shuttleworth `lora_vs_fullft_intruder_dimensions.md`). Trajectory should predict where intruder dims form *before* they form.
- **89%** inter-task alignment of top-20% SVs (mtLoRA `mtlora_spectral_multitask_regularization.md`). Region 1 = universal. We project it out for trajectory analysis.
- **74%** MPPC across architectures (`mechanistic_similarity_transformers_mamba.pdf`). Cross-arch invariance evidence.
- **99% accuracy at 10x compression** keeping only TSV (`task_singular_vectors_merge_interference.pdf`). Region 2 = sufficient task signal.
- **Theoretical Θ(n^{-1/2}) vs Θ(n^{-1}) LR scaling** for Init[A] vs Init[B] (Hayou `arxiv_2406_08447.md`). Asymmetry is intrinsic.
- **5+1 phases** of training spectrum (Martin-Mahoney `arxiv_1901_08276.md`). The phase machinery applies to LoRAs.

---

## What's Still Missing in the Corpus

Genuine remaining gaps as of 2026-05-07:

1. **Cross-arch trajectory studies for fine-tuning specifically** — Layer-wise SFT (2604.11838) is closest but on full models, not LoRA. Open territory for the stretch.
2. **Empirical LoRA trajectory population at population scale** — nobody has done it. Compress-then-Serve does endpoints; Phase Transitions Zoo does full models. Our specific intersection is open.
3. **Connection between trajectory geometry and agent self-knowledge** — speculative; the agent vision section needs to acknowledge this is forward-looking.
4. **LS-Merge non-linearity argument** — full PDF is blocked. Need access to settle linear-vs-nonlinear question.

---

## How This Index Connects to the Plan

The thesis plan at `C:/Users/barsa/Documents/thesis_plan/plan.md` references this index and the companion `observations_lora_lmc_program.md`. The plan's:
- **Section 4 (E1 endpoint setup)** maps to nodes in *Endpoint baseline* and *Mode connectivity foundation*
- **Section 5 (E2 trajectory main contribution)** maps to nodes in *Trajectory / training-dynamics core* and *HT-SR foundations*
- **Section 6 (predictive demonstration)** maps to nodes in *Predictive demonstration anchors*
- **Section 7 (discussion / agent vision)** maps to nodes in *Agent vision anchors*

This index is the bridge from the unstructured corpus to the structured paper.

---

*Last updated 2026-05-07. Re-run `graphify update .` after edits.*
