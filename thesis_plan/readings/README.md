# Reading List — Aligned to E1 + E2 Plan

15 papers copied locally. 10 more must be downloaded from arxiv (script at the bottom). Total 25 papers, three tiers.

**Read in tier order. Don't read Tier 3 until pipeline is running.**

---

## Tier 1 — Read these first (5 papers, ~6 hours)

These five anchor every concept in the paper. If you're confused after reading them, ask me; don't move on until they make sense.

| # | Paper | Why it matters | File |
|---|---|---|---|
| 1 | **W2T: LoRA Weights Already Know What They Can Do** | Provides the QR+SVD canonical decomposition (the π map). This is the *exact* tooling for E1's weight coordinate. Read Sections 3 + 4 carefully; skim 5. | ✅ `01_w2t_canonical_decomposition.pdf` |
| 2 | **The Impact of Initialization on LoRA Finetuning Dynamics** (Hayou, Ghosh, Yu — NeurIPS 2024) | The "AsymmetryOfLoRA" theoretical paper. Proves B vs A intrinsically different dynamics. The theoretical anchor for *why* same-task LoRAs collapse onto a B-subspace. | ✅ `02_asymmetry_of_lora_hayou.pdf` |
| 3 | **Linear Mode Connectivity and the Lottery Ticket Hypothesis** (Frankle, Dziugaite, Roy, Carbin 2020) | Your formal cousin. Read so you know exactly what LoRA-LMC extends. | ❗ DOWNLOAD: `arxiv.org/abs/1912.05671` |
| 4 | **Mechanistic Mode Connectivity** (Lubana, Bigelow, Dick, Krueger, Tanaka — ICML 2023) | The framework E2's "behavior vs mechanism" question sits inside. "Lack of linear connectivity ⟹ dissimilar mechanisms." Cite as foundation. | ❗ DOWNLOAD: `arxiv.org/abs/2211.08422` |
| 5 | **Structure Is Not Enough: Leveraging Behavior for NN Weight Reconstruction** (Meynent, Schürholt, Borth — ICLR Workshop 2025) | THE prior to differentiate from. Same group as ViT Zoo + Phase Transitions Zoo. They argue structure-only is insufficient; we extend with GL(r)-canonical Region-2 + trajectory. | ❗ DOWNLOAD: `arxiv.org/abs/2503.17138` |

---

## Tier 2 — Read while building pipeline (8 papers, ~12 hours)

Read these in week 1–2 while you set up the LoRA training loop.

| # | Paper | Why it matters | File |
|---|---|---|---|
| 6 | **Knowledge Is a Region in Weight Space** | Full-model precursor to LoRA-LMC. "Convex Hull Low-Loss Region" = same idea, full models. Read for the framing language and what they don't quite claim. | ✅ `06_knowledge_is_a_region.pdf` |
| 7 | **A Model Zoo of Vision Transformers** (Falk, Meynent, Pfammatter, Schürholt, Borth — ICLR Workshop 2025) | Closest setup philosophy for E1. Different domain (vision). Read to know exactly what to *not* duplicate. | ❗ DOWNLOAD: `arxiv.org/abs/2504.10231` |
| 8 | **A Model Zoo on Phase Transitions in Neural Networks** (Schürholt, Meynent, Zhou, Yang, Borth) | The phase-transition machinery you'll extend to LoRAs in E2. Read carefully — this is the most direct prior for trajectory-population analysis. | ❗ DOWNLOAD: `arxiv.org/abs/2504.18072` |
| 9 | **Predicting Trends in NN Quality Without Test Data** (Martin, Peng, Mahoney — Nature Comms 2021) | The WeightWatcher methodology paper. Learn which metrics they compute and how they use HT-SR alpha to predict quality. You'll use this exact pipeline per checkpoint in E2. | ✅ `09_weightwatcher_nature.pdf` |
| 10 | **Compress then Serve: Serving Thousands of LoRA Adapters** (Brüel-Gabrielsson et al.) | Joint diagonalization across thousands of LoRAs. Confirming evidence that shared subspaces exist at scale. Read Section 3 carefully. | ❗ DOWNLOAD: `arxiv.org/abs/2407.00066` |
| 11 | **GELoRA: Geometric Adaptive Rank for LoRA** | Defines `d_task` operationally via 2-NN intrinsic dimensionality on the gradient flow. You'll measure d_task per LoRA. | ✅ `11_gelora_intrinsic_dimensionality.pdf` |
| 12 | **AlphaLoRA: HT-SR Layer Quality** | Applies HT-SR alpha specifically to LoRAs. Proof that the WeightWatcher alpha=2 criterion works on adapters. | ✅ `12_alphalora_htsr.pdf` |
| 13 | **From Spikes to Heavy Tails: Spectral Evolution of Weight Matrices** | The 5+1 spectral phases of training. Full-network. You're operationalizing this on LoRA trajectories — read carefully so you know what "phase" means precisely. | ✅ `13_from_spikes_to_heavy_tails.pdf` |

---

## Tier 3 — Read while writing paper (~12 papers, skim or deep-read as needed)

Read these later, primarily for related-work section and to anchor methodology choices.

| # | Paper | Why it matters | File |
|---|---|---|---|
| 14 | **Gunasekar — Implicit Regularization in Matrix Factorization** | Theoretical foundation: GD on factorized matrix → minimum nuclear norm = sparse spectrum. Predicts which directions emerge first in the trajectory. | ✅ `14_gunasekar_implicit_regularization.pdf` |
| 15 | **Approaching Deep Learning Through the Spectral Dynamics of Weights** | Most direct full-network analog to E2 trajectory work. Empirical study of spectrum during training. | ✅ `15_spectral_dynamics_weights.pdf` |
| 16 | **Cross-LoRA: Data-Free LoRA Transfer Across Heterogeneous LLMs** | Methodology candidate ρ for E2 stretch (cross-arch). LoRA-Align = SVD subspace alignment + Frobenius-optimal linear. Use as one of three ρ baselines. | ✅ `16_cross_lora_transfer.pdf` |
| 17 | **SANE: Towards Scalable and Versatile Weight Space Learning** (Schürholt, Mahoney, Borth — ICML 2024) | Schürholt's main framework paper. Autoencoder weight-space embedding. Cite for related work and as an alternative to TRS-canonical. | ✅ `17_sane_scalable_wsl.pdf` |
| 18 | **Tracking Feature Dynamics in LLM Training (SAE-Track)** | Three trajectory phases (Init/Warmup, Emergent, Convergent) at the feature level. Direct competitor — different unit (features vs subspaces) but same temporal framing. | ❗ DOWNLOAD: `arxiv.org/abs/2412.17626` |
| 19 | **LoRA Provably Converges to Low-Rank Global Minimum** | Endpoint convergence theorem. Your trajectory work shows *how* it gets there. | ✅ `19_lora_converges_lowrank.pdf` |
| 20 | **EigenLoRAx: Recycling Adapters for Principal Subspaces** | Task-invariant principal subspaces from LoRA populations. Confirming evidence for LoRA-LMC. | ✅ `20_eigenlorax.pdf` |
| 21 | **Intrinsic Dimensionality of Fine-Tuning** | Foundational for d_task framing. Read for theoretical background. | ✅ `21_intrinsic_dimensionality_full_ft.pdf` |
| 22 | **LoRA Learns Less and Forgets Less** (Biderman et al.) | Empirical paper on LoRA properties — useful background, especially for the forgetting prediction in Section 6. | ✅ `22_lora_learns_less_biderman.pdf` |
| 23 | **Linear Connectivity Reveals Generalization Strategies** (Juneja et al. 2022) | The honest falsifier: BERT fine-tunes can be *linearly disconnected*. Pretraining quality is the discriminator. Justifies your choice of well-pretrained backbones. | ❗ DOWNLOAD: `arxiv.org/abs/2205.12411` |
| 24 | **Layer-wise Analysis of Supervised Fine-Tuning** | Depth-dependent adaptation pattern across 1B–32B models. Read to inform per-layer trajectory analysis. | ❗ DOWNLOAD: `arxiv.org/abs/2604.11838` |
| 25 | **Martin & Mahoney — Heavy-Tailed Self Regularization** (ICML 2019) | The original HT-SR paper. Defines the 5+1 phases and the alpha metric. Foundational; skim if Tier 2 #9 (Nature Comms) is enough. | ❗ DOWNLOAD: `arxiv.org/abs/1901.08276` |

---

## What's intentionally NOT in this list

To keep mental space:
- **LS-Merge** — non-linearity argument; future work, not this paper
- **CAST / Activation Manifold Projection** — alternative methodology; cite, don't deep-read until E2 stretch
- **OrthoMerge / Multi-Way Representation Alignment** — only relevant if you do cross-arch; defer
- **TeleLoRA, ProbeLog, Atlas of Models** — agent-vision flavor; read for the discussion section, not for methodology
- **Spin-glass / NN-as-spin-models** — cross-domain depth; cite if it fits, don't deep-read
- **Riemannian-LoRA cluster (RiemannLoRA, PoLAR, Stiefel-LoRA)** — alternative parameterization, not relevant to your path; future work
- All the synthesis docs — you wrote those; treat them as memory, not new reading

---

## Download script for the missing 10 papers

Run on your supercomp environment. Total ~50 MB.

```bash
cd readings/
wget -O 03_lmc_frankle.pdf https://arxiv.org/pdf/1912.05671
wget -O 04_mechanistic_mode_connectivity.pdf https://arxiv.org/pdf/2211.08422
wget -O 05_structure_is_not_enough.pdf https://arxiv.org/pdf/2503.17138
wget -O 07_vit_model_zoo.pdf https://arxiv.org/pdf/2504.10231
wget -O 08_phase_transitions_zoo.pdf https://arxiv.org/pdf/2504.18072
wget -O 10_compress_then_serve.pdf https://arxiv.org/pdf/2407.00066
wget -O 18_sae_track_feature_dynamics.pdf https://arxiv.org/pdf/2412.17626
wget -O 23_juneja_lmc_generalization.pdf https://arxiv.org/pdf/2205.12411
wget -O 24_layerwise_sft_analysis.pdf https://arxiv.org/pdf/2604.11838
wget -O 25_martin_mahoney_htsr.pdf https://arxiv.org/pdf/1901.08276
```

If `wget` is blocked: replace with `curl -L -o <name> <url>`.

---

## Reading time estimate

- Tier 1: 5 papers × 60–90 min each = ~6 hours. Spread over 3–4 days.
- Tier 2: 8 papers × 60–90 min each = ~10 hours. Spread over week 2.
- Tier 3: 12 papers × 30–60 min skim = ~8 hours. Spread over week 3–4 while writing.

**Total reading: ~24 hours over the first month.** That leaves the other ~140 hours of the month for setup + experiments + writing.

---

## How to read each paper (efficiency)

For each paper, in this order:
1. **Abstract + introduction** (5 min). Note the central claim in 1 sentence.
2. **Figures and tables** (10 min). Tables tell you what they actually measured and what numbers they got.
3. **Related work** (5 min skim). Note who they cite that you should also know.
4. **Method section** (15–30 min). Only deep-read if the method is something you'll reuse.
5. **Limitations / discussion** (5 min). What they couldn't show — that's where your contribution might land.

For Tier 2 + 3, often steps 1–2–5 are enough. Don't get stuck in method details unless you're implementing something.

---

## What to extract while reading

Keep a single notebook (paper or digital). For each paper, write:
- **In one sentence:** what they did
- **In one sentence:** what number / result is the central claim
- **Differs from my work because:** ...
- **I will reuse / cite for:** ... (specific section of your paper)

This is what makes the related-work section write itself in week 11.

---

*Reading list aligned to plan.md sections 4 (E1), 5 (E2), 6 (predictive demonstration). Last updated 2026-05-07.*
