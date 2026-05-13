# Continual Learning — Curated Corpus Index

**Date:** 2026-05-11
**Purpose:** Map the continual learning literature added to the corpus on
2026-05-11, identify the research groups, and align with this project's
existing weight-space / trajectory geometry frame.

---

## The Two Research Schools This Project Already Sits Between

| School | Members in corpus | Their object | Their angle |
|---|---|---|---|
| **Borth-Schürholt** (St.Gallen) | Damian Borth, Konstantin Schürholt, Léo Meynent, Damian Falk, **Florence Pfammatter** (you), Yefan Zhou, Yaoqing Yang | Weight space as data modality | Model zoos, autoencoders, phase transitions in weights |
| **Martin-Mahoney** (Berkeley / Dartmouth) | Charles H. Martin, Michael W. Mahoney, Yaoqing Yang, Yefan Zhou | Empirical spectral density of weights | HT-SR theory, alpha exponent, 5+1 phase model |

Yaoqing Yang and Yefan Zhou are the cross-bridge (co-author on both groups'
papers). Your project's natural lineage is: Borth-Schürholt's weight-space
program + Martin-Mahoney's HT-SR phases, extended to LoRA + trajectory.

**Neither school has published in continual learning directly.** That's the
gap this corpus-pull fills.

---

## Continual Learning — The Research Communities (and who to track)

The CL literature splits roughly into four communities. The frequent
researchers per community:

### 1. Foundational regularization-based CL (2017–2019 era)

- **James Kirkpatrick** (DeepMind) — Elastic Weight Consolidation (EWC), the
  Fisher-based foundation. Connects directly to your `EWC-LoRA` corpus paper.
  - `arxiv_1612_00796.md` — Overcoming catastrophic forgetting in neural networks (PNAS 2017)
- **Friedemann Zenke** (DeepMind / Friedrich Miescher Inst.) — Synaptic
  Intelligence (SI), path-based importance.
  - `arxiv_1703_04200.md` — Continual Learning Through Synaptic Intelligence
- **Rahaf Aljundi** — MAS (Memory-Aware Synapses), task-free CL.
  - `arxiv_1711_09601.md` — Memory Aware Synapses
- **David Lopez-Paz, Marc'Aurelio Ranzato** (Facebook AI / Meta) — GEM, A-GEM
  (gradient-projection-based CL).
  - `arxiv_1706_08840.md` — Gradient Episodic Memory (GEM)
  - `arxiv_1812_00420.md` — A-GEM (efficient version)
- **Matthias De Lange** — the canonical survey of regularization-based CL.
  - `arxiv_1909_08383.md` — A continual learning survey

### 2. Survey papers — these define the landscape

- **Liyuan Wang et al.** (Tsinghua) — *the* comprehensive CL survey, current.
  - `arxiv_2302_00487.md` — A Comprehensive Survey of Continual Learning
- **Zixuan Ke, Bing Liu** — CL for NLP specifically.
  - `arxiv_2302_03241.md` — Continual Learning of NLP Tasks
- **Tongtong Wu et al.** — CL for LLMs, the most recent landscape.
  - `arxiv_2402_01364.md` — Continual Learning for Large Language Models: A Survey
- **German I. Parisi et al.** — older comprehensive view, still cited.
  - `arxiv_1802_07569.md` — Continual lifelong learning with neural networks

### 3. Prompt-based CL for vision transformers

- **Zifeng Wang et al.** (Google) — L2P, the prompt-based foundation.
  - `arxiv_2112_08654.md` — Learning to Prompt for Continual Learning (L2P)
  - `arxiv_2204_04799.md` — DualPrompt
- **James Seale Smith et al.** — CODA-Prompt, more sophisticated prompt CL.
  - `arxiv_2211_13218.md` — CODA-Prompt
- **Anastasia Razdaibiedina et al.** — Progressive Prompts (NLP variant).
  - `arxiv_2301_12314.md` — Progressive Prompts

### 4. LoRA + task arithmetic + merging (the one closest to this project)

- **Xiao Wang et al.** (Fudan) — **O-LoRA**, the orthogonal subspace
  constraint for CL via LoRA. *Closest existing prior to plan.md.*
  - `arxiv_2310_14152.md` — Orthogonal Subspace Learning for LLM Continual Learning
- **Yang Liang et al.** — **InfLoRA**, infinite-task CL via LoRA decomposition.
  - `arxiv_2404_00228.md` — InfLoRA: Interference-Free Low-Rank Adaptation
- **Daniel Marczak et al.** — **MagMax**, task-arithmetic for CL with sign
  selection on the merge.
  - `arxiv_2407_06322.md` — MagMax
- **Chengyue Huang et al.** — **LoRAHub**, post-hoc LoRA selection & merging.
  - `arxiv_2307_13269.md` — LoRAHub
- **Gabriel Ilharco et al.** (UW) — **Task Arithmetic**, the foundation for
  arithmetic on task vectors.
  - `arxiv_2212_04089.md` — Editing Models with Task Arithmetic
- **Prateek Yadav et al.** (UNC) — **TIES-Merging**, resolves task-vector
  interference for merging.
  - `arxiv_2306_01708.md` — TIES-Merging
- **Mitchell Wortsman et al.** (UW) — **Model Soups**, weight-averaging baseline.
  - `arxiv_2203_05482.md` — Model Soups
- **Michael Matena, Colin Raffel** — **Fisher Merging**, the Fisher-weighted
  version of task arithmetic.
  - `arxiv_2111_09832.md` — Merging Models with Fisher-Weighted Averaging

### 5. Recent (2024–2025) LoRA-CL papers

- `arxiv_2403_16627.md` — recent LoRA-CL method
- `arxiv_2403_05175.md` — LAE (Learning-Accumulation-Ensemble) for CL
- `arxiv_2403_18922.md` — modern LoRA-CL
- `arxiv_2404_05868.md` — recent LoRA-CL
- `arxiv_2406_18585.md` — recent LoRA-CL
- `arxiv_2310_07234.md` — HiDe-Prompt
- `arxiv_2406_00153.md` — μLO meta-generalization
- `arxiv_2407_11401.md` — Boosting CL with Recursive Updates
- `arxiv_2503_00302.md` — recent LLM-CL
- `arxiv_2401_13586.md` — recent LoRA-CL
- `arxiv_2402_07876.md` — recent LoRA-CL
- `arxiv_2402_18865.md` — recent LoRA-CL
- `arxiv_2405_03003.md` — recent LoRA-CL
- `arxiv_2405_09673.md` — recent LoRA-CL
- `arxiv_2405_17604.md` — recent CL method
- `arxiv_2306_11192.md` — RoSA / sequential PEFT-CL
- `arxiv_2311_18763.md` — STAMINA (continual diffusion)
- `arxiv_2305_16213.md` — recent regularization-based CL
- `arxiv_1708_01547.md` — DEN (Dynamically Expanding Networks)

### 6. Already in corpus (CL-adjacent, pre-2026-05-11)

- `arxiv_2602_05943.md` — OrthoMerge (orthogonal LoRA subspaces for merging)
- `arxiv_2601_18699.md` — Mechanistic analysis of catastrophic forgetting
- `arxiv_2604_11838.md` — Layer-wise SFT analysis
- `arxiv_2602_19332.md` — Continual learning + spectral
- `arxiv_2601_12816.md` — Continual learning + LoRA
- `arxiv_2601_21577.md` — Continual learning method
- `arxiv_2505_18356.md` — Continual learning + LLM
- `shared_lora_subspaces_continual_learning.md` — Share (universal CL subspace)
- `neural_collapse_continual_learning_etf.md` — ProNC (ETF-based CL)
- `lora_vs_fullft_intruder_dimensions.md` — Shuttleworth (intruder dims ↔ forgetting, ρ=0.97)

---

## Most-Frequent CL Researchers (cross-paper)

These names appear in 3+ papers in the now-expanded corpus. Track their
arxiv pages.

| Researcher | Lab | What they work on | # papers in corpus |
|---|---|---|---|
| **Zifeng Wang** | Google Cloud AI | L2P, DualPrompt, prompt-based CL | 2+ |
| **Liyuan Wang** | Tsinghua | THE comprehensive CL survey lead | 1+ many citations |
| **Rahaf Aljundi** | KU Leuven (former)/Facebook | MAS, task-free CL | 1+ many citations |
| **Yang Liang / Heng-Tze Cheng** | various | LoRA-CL | many |
| **Prateek Yadav, Colin Raffel** | UNC | TIES-Merging, Fisher Merging | 2 |
| **Gabriel Ilharco, Mitchell Wortsman** | UW | Task Arithmetic, Model Soups | 2 |

**For your meeting:** when the senior asks "who is doing what in CL," point
to Wang Liyuan's 2302.00487 survey as the landscape, then say:
> *"The LoRA-CL community is currently dominated by orthogonality-based
> constraints (O-LoRA, InfLoRA, OrthoMerge) and task-arithmetic post-hoc
> merging (TIES, MagMax, LoRAHub). Both communities work with endpoint
> LoRAs. Nobody has measured the trajectory geometry that drives those
> orthogonality/merge results, which is the gap we're filling."*

---

## How the New Papers Connect to plan.md

| plan.md claim | CL paper that anticipates / extends it |
|---|---|
| C1: same-task LoRAs cluster | O-LoRA (2310.14152) — enforces by construction |
| Region 2 ⊥ W₀-top prevents forgetting | O-LoRA + InfLoRA (2404.00228) — both build this in |
| MLP-zero recipe (post-hoc) | TIES-Merging (2306.01708) — generalizes to "remove conflicting components" |
| Trajectory predicts mergeability | **Gap.** TIES is endpoint-only. We extend. |
| Self-evolving agents | μLO (2406.00153), MagMax (2407.06322) — meta-learning angle |
| The geometric instrument exists | Wang Liyuan 2302.00487 survey says "structural methods underexplored" |

---

## Reading Order for the Meeting (priority)

1. **Wang Liyuan 2302.00487** — read first; defines the landscape
2. **O-LoRA 2310.14152** — the closest existing LoRA-CL method; differentiate from
3. **TIES-Merging 2306.01708** — the closest task-arithmetic prior; differentiate from
4. **Wu 2402.01364** — LLM-specific CL survey; positions LoRA in larger context
5. **MagMax 2407.06322** — modern task-arithmetic-for-CL
6. **InfLoRA 2404.00228** — the "infinite-task" angle, modern

Skip the 2017–2019 foundational stuff unless asked; just know it exists
(EWC, MAS, GEM, SI).

---

## Status

- **Corpus before 2026-05-11**: 60+ papers, mostly weight-space and HT-SR
- **Added 2026-05-11**: 41 new arxiv MDs (CL-focused), enriched with full
  abstracts/authors via direct arxiv-page fetch
- **Total now**: ~100+ papers in `finding_literature/arxiv_*.md`
- **Graph**: 4520 nodes / 4685 edges / 378 communities after re-extraction

**Next steps for the user:**
1. Read the Wang Liyuan 2302.00487 survey to anchor your meeting framing
2. Read O-LoRA carefully — that's the paper your reviewer will reference first
3. The new arxiv MDs in this corpus need a semantic-extraction pass (LLM)
   to be fully integrated; the AST update only refreshed structural nodes
