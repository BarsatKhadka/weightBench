# Graph Report - ./relevant_literature  (2026-05-04)

## Corpus Check
- 28 files · ~614,960 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 123 nodes · 197 edges · 10 communities detected
- Extraction: 61% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 22 edges (avg confidence: 0.77)
- Token cost: 0 input · 0 output

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

## God Nodes (most connected - your core abstractions)
1. `ICM-LoRA Framework` - 6 edges
2. `SANE: Sequential Autoencoder for Neural Embeddings` - 6 edges
3. `LoRA: Low-Rank Adaptation of Large Language Models` - 5 edges
4. `Low-Rank Adaptation (LoRA)` - 5 edges
5. `Multiplicative LoRA (mLoRA) for Neural Fields` - 5 edges
6. `WARP: Weight-space Adaptive Recurrent Prediction` - 5 edges
7. `Editing Models with Task Arithmetic` - 4 edges
8. `Knowledge Region in Weight Space` - 4 edges
9. `Equivariant Deep Weight Space Alignment (Deep-Align / DWSNets)` - 4 edges
10. `LoRAGen: Structure-Aware Weight Space Learning for LoRA Generation` - 4 edges

## Surprising Connections (you probably didn't know these)
- `Task Vector` --semantically_similar_to--> `Knowledge Region in Weight Space`  [INFERRED] [semantically similar]
  relevant_literature_but_not_limited_to/EditingModelWithTaskArthimetic.pdf → relevant_literature_but_not_limited_to/KnowledgeIsARegionInWeightSpace.pdf
- `Implicit Neural Representations (INRs / Neural Fields)` --applied_to--> `WARP: Weight-space Adaptive Recurrent Prediction`  [INFERRED]
  relevant_literature/WeightSpaceRepresentationLearningViaNeuralFieldAdaption.pdf → relevant_literature/WeightSpaceLinearRecurrentNeuralNetworks.pdf
- `Task Arithmetic` --semantically_similar_to--> `Rank-One Model Editing (ROME)`  [INFERRED] [semantically similar]
  relevant_literature_but_not_limited_to/EditingModelWithTaskArthimetic.pdf → relevant_literature_but_not_limited_to/LocatingAndEditingFactualAssosciationsInGPT.pdf
- `weights2weights (w2w) Space` --semantically_similar_to--> `Knowledge Region in Weight Space`  [INFERRED] [semantically similar]
  relevant_literature_but_not_limited_to/weight2weight.pdf → relevant_literature_but_not_limited_to/KnowledgeIsARegionInWeightSpace.pdf
- `Conditional Recurrent Diffusion for LoRA Generation` --semantically_similar_to--> `LoRAGen Method`  [INFERRED] [semantically similar]
  relevant_literature_but_not_limited_to/ORALLoraViaReccurentDiffusion.pdf → relevant_literature_but_not_limited_to/StructureAwareWeightSpaceLearningForLoraGeneration.pdf

## Hyperedges (group relationships)
- **LoRA Parameter Generation Paradigm** — oral_conditional_recurrent_diffusion, structureawarelorgen_lorangen, weight2weight_w2w_space, oral_parameter_generation [INFERRED 0.85]
- **Weight Space Structure and Geometry** — knowledgeinweightspace_weight_region, knowledgeinweightspace_linear_connectivity, dwsnets_permutation_symmetry, dwsnets_weight_alignment, selfsupervisedweightlearning_permutation_augmentation [INFERRED 0.85]
- **Low-Rank Hypothesis for Fine-Tuning** — intrinsicdimensionality_intrinsic_dimension, loraoriginal_rank_deficiency, loraoriginal_low_rank_adaptation, loralearnlessforgetless_high_rank_perturbation [EXTRACTED 0.95]
- **LoRA Ecosystem: Vanilla to Adaptive to Generated** —  [INFERRED]
- **Weight Space Composition Triangle** —  [INFERRED]
- **Symmetry-Aware Architecture Understanding** —  [INFERRED]
- **LoRA symmetry handling for weight-space generation** — lora_adaptation, permutation_symmetry_weight_space, multiplicative_lora [INFERRED 0.85]
- **Multi-task LoRA generation via task vectors and CVAE** — task_vector_extraction, cvae_lora_generator, in_context_metalearning [EXTRACTED 1.00]
- **Weight-space hidden state enables gradient-free adaptation** — weight_space_hidden_state, warp_rnn_mechanism, fast_weight_programmers [INFERRED 0.85]

## Communities (10 total, 0 thin omitted)

### Community 0 - "LoRA Weight Space Core"
Cohesion: 0.23
Nodes (22): AdaLoRA (Zhang et al., ICLR 2023), Dual-Signal Framing (WeightBench Core Concept), DWSNets (Deep Weight Space Networks), Hypernetwork / Parameter Generation, LoRA (Low-Rank Adaptation), Model Merging, NTK Linearization / Tangent Space Fine-tuning, Permutation Symmetry / Invariance in Neural Networks (+14 more)

### Community 1 - "Intrinsic Dimensionality & Fine-Tuning"
Cohesion: 0.17
Nodes (16): Intrinsic Dimension of Fine-Tuning, Intrinsic Dimensionality Explains the Effectiveness of Language Model Fine-Tuning, Structure-Aware Intrinsic Dimension (SAID), High-Rank Weight Perturbations in Full Fine-Tuning, LoRA Learns Less and Forgets Less, LoRA Learning-Forgetting Tradeoff, Low-Rank Adaptation (LoRA), LoRA: Low-Rank Adaptation of Large Language Models (+8 more)

### Community 2 - "Graph Metanetworks & Symmetry"
Cohesion: 0.23
Nodes (16): Adaptive Weight-Space Ensembling for Few-Shot Fine-Tuning, CLIP Vision-Language Models, Functional Symmetries of Neural Networks, Graph Metanetworks for Processing Diverse Neural Architectures, Model Merging, Neural DAG Automorphisms, NTK Linearization / Tangent Space Fine-Tuning, Parameter Graphs (+8 more)

### Community 3 - "Generative Weight Space & Neural Fields"
Cohesion: 0.16
Nodes (15): Low-Rankness Property of Neural Network Activations, Asymmetric Masking for Permutation Symmetry Breaking, Class-Incremental Few-Shot Learning (CIFSL), Diffusion Transformer on LoRA Weight Representations, HyperDiffusion (Weight-Space Diffusion Baseline), Implicit Neural Representations (INRs / Neural Fields), Low-Rank Adaptation (LoRA), LoRA Weight Space Symmetry Analysis (+7 more)

### Community 4 - "LoRA Parameter Generation"
Cohesion: 0.18
Nodes (12): COND P-DIFF (Conditional LoRA Parameter Generation), Conditional Variational Autoencoder for LoRA Generation, Hyper-Representations for Neural Network Weight Spaces, ICM-LoRA Framework, In-Context Meta LoRA Generation (ICM-LoRA), In-Context Meta-Learning for Parameter Generation, Model Soup (Weight Averaging), Model Zoo Datasets for Weight Space Learning (+4 more)

### Community 5 - "Weight Alignment & Model Quality"
Cohesion: 0.25
Nodes (11): Deep-Align Framework, Equivariant Deep Weight Space Alignment (Deep-Align / DWSNets), Permutation Symmetry of Neural Networks, Weight Alignment, Predicting Trends in the Quality of State-of-the-Art Neural Networks without Access to Training or Testing Data, Power Law (Heavy-Tailed) Metrics for Model Quality, WeightWatcher Tool, Hyper-Representations of Neural Network Weights (+3 more)

### Community 6 - "Adaptive LoRA & Hypernetworks"
Cohesion: 0.36
Nodes (10): AdaLoRA: Adaptive Budget Allocation for Parameter-Efficient Fine-Tuning, AdaLoRA SVD Parameterization, Asymmetry of LoRA: Revisiting Early Stopping and Fine-Tuning, DnD Hyper-Generator Architecture, Drag-and-Drop LLMs: Zero-Shot Prompt-to-LoRA Generation, Hypernetworks / Parameter Generation, LoRA Matrix Asymmetry, Low-Rank Adaptation (LoRA) (+2 more)

### Community 7 - "Task Arithmetic & Model Editing"
Cohesion: 0.36
Nodes (8): Editing Models with Task Arithmetic, Task Arithmetic, Task Vector, Weight Interpolation, Causal Mediation Analysis for Knowledge Localization, Mid-Layer MLP Modules as Factual Association Storage, Locating and Editing Factual Associations in GPT (ROME), Rank-One Model Editing (ROME)

### Community 8 - "Self-Modifying & Recurrent Weights"
Cohesion: 0.38
Nodes (7): Delta Update Rule for Weight Modification, Fast Weight Programmers (FWP), Self-Referential Weight Matrix (SRWM) Mechanism, A Modern Self-Referential Weight Matrix That Learns to Modify Itself, WARP: Weight-space Adaptive Recurrent Prediction, Neural Network Weights as RNN Hidden State, Weight-Space Linear Recurrent Neural Networks (WARP model)

### Community 9 - "Weight Space Geometry & Regions"
Cohesion: 0.47
Nodes (6): Linear Mode Connectivity, Knowledge Is a Region in Weight Space for Finetuned Language Models, Knowledge Region in Weight Space, Meta-Latent Space over Model Weights, Weights2Weights: Interpreting the Weight Space of Customized Diffusion Models, weights2weights (w2w) Space

## Knowledge Gaps
- **21 isolated node(s):** `Weight Interpolation`, `Neural Network Parameter Generation`, `WeightWatcher Tool`, `Structure-Aware Intrinsic Dimension (SAID)`, `Module-Aware Mix-of-Experts (MoE) Decoder` (+16 more)
  These have ≤1 connection - possible missing edges or undocumented components.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Knowledge Region in Weight Space` connect `Weight Space Geometry & Regions` to `Task Arithmetic & Model Editing`?**
  _High betweenness centrality (0.059) - this node is a cross-community bridge._
- **Why does `Low-Rank Adaptation (LoRA)` connect `Intrinsic Dimensionality & Fine-Tuning` to `Weight Space Geometry & Regions`?**
  _High betweenness centrality (0.054) - this node is a cross-community bridge._
- **Why does `Task Vector` connect `Task Arithmetic & Model Editing` to `Weight Space Geometry & Regions`?**
  _High betweenness centrality (0.054) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Task Arithmetic in the Tangent Space: Improved Editing of Pre-Trained Models` (e.g. with `Drag-and-Drop LLMs: Zero-Shot Prompt-to-LoRA Generation` and `TIES-Merging: Resolving Interference When Merging Models`) actually correct?**
  _`Task Arithmetic in the Tangent Space: Improved Editing of Pre-Trained Models` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Weight Interpolation`, `Neural Network Parameter Generation`, `WeightWatcher Tool` to the rest of the system?**
  _21 weakly-connected nodes found - possible documentation gaps or missing edges._