# Graph Report - .  (2026-05-04)

## Corpus Check
- Corpus is ~664 words - fits in a single context window. You may not need a graph.

## Summary
- 63 nodes · 109 edges · 8 communities detected
- Extraction: 44% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 7 edges (avg confidence: 0.81)
- Token cost: 9,800 input · 4,200 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Equivariant Weight Space Methods|Equivariant Weight Space Methods]]
- [[_COMMUNITY_Low-Rank Adaptation Theory|Low-Rank Adaptation Theory]]
- [[_COMMUNITY_Weight Alignment & Task Arithmetic|Weight Alignment & Task Arithmetic]]
- [[_COMMUNITY_Model Merging & Task Vectors|Model Merging & Task Vectors]]
- [[_COMMUNITY_LoRA Parameter Generation|LoRA Parameter Generation]]
- [[_COMMUNITY_Weight Analysis & Self-Supervised Learning|Weight Analysis & Self-Supervised Learning]]
- [[_COMMUNITY_Weight Space Geometry|Weight Space Geometry]]
- [[_COMMUNITY_Factual Knowledge Editing|Factual Knowledge Editing]]

## God Nodes (most connected - your core abstractions)
1. `LoRA: Low-Rank Adaptation of Large Language Models` - 5 edges
2. `Low-Rank Adaptation (LoRA)` - 5 edges
3. `Editing Models with Task Arithmetic` - 4 edges
4. `Knowledge Region in Weight Space` - 4 edges
5. `Equivariant Deep Weight Space Alignment (Deep-Align / DWSNets)` - 4 edges
6. `LoRAGen: Structure-Aware Weight Space Learning for LoRA Generation` - 4 edges
7. `Rank Deficiency in Weight Updates` - 4 edges
8. `Hyper-Representations of Neural Network Weights` - 4 edges
9. `Task Vector` - 3 edges
10. `Task Arithmetic` - 3 edges

## Surprising Connections (you probably didn't know these)
- `Knowledge Region in Weight Space` --semantically_similar_to--> `Task Vector`  [INFERRED] [semantically similar]
  relevant_literature_but_not_limited_to/KnowledgeIsARegionInWeightSpace.pdf → relevant_literature_but_not_limited_to/EditingModelWithTaskArthimetic.pdf
- `Rank-One Model Editing (ROME)` --semantically_similar_to--> `Task Arithmetic`  [INFERRED] [semantically similar]
  relevant_literature_but_not_limited_to/LocatingAndEditingFactualAssosciationsInGPT.pdf → relevant_literature_but_not_limited_to/EditingModelWithTaskArthimetic.pdf
- `Permutation Augmentation for Neural Network Weights` --semantically_similar_to--> `Permutation Symmetry of Neural Networks`  [INFERRED] [semantically similar]
  relevant_literature_but_not_limited_to/SelfSupervisedRepresentationLearningOnNeuralNetworkWeights.pdf → relevant_literature_but_not_limited_to/DWSNets.pdf
- `weights2weights (w2w) Space` --semantically_similar_to--> `Knowledge Region in Weight Space`  [INFERRED] [semantically similar]
  relevant_literature_but_not_limited_to/weight2weight.pdf → relevant_literature_but_not_limited_to/KnowledgeIsARegionInWeightSpace.pdf
- `Conditional Recurrent Diffusion for LoRA Generation` --semantically_similar_to--> `LoRAGen Method`  [INFERRED] [semantically similar]
  relevant_literature_but_not_limited_to/ORALLoraViaReccurentDiffusion.pdf → relevant_literature_but_not_limited_to/StructureAwareWeightSpaceLearningForLoraGeneration.pdf

## Hyperedges (group relationships)
- **LoRA Weight Space Methods** — lora_asymmetry, adalora, weight_space_via_neural_field, icm_lora, drag_and_drop_llms [INFERRED]
- **Equivariant Metanetworks for Weight Spaces** — equivariant_deep_weight_spaces, graph_meta_networks, concept_dwsnets, concept_permutation_symmetry [INFERRED]
- **Model Merging Methods** — task_arithmetic_tangent, ties_merging, equivariant_deep_weight_spaces, concept_model_merging, concept_task_vector [INFERRED]
- **Scalable Weight Space Representations** — sane_weight_space, graph_meta_networks, survey_weight_space_learning [INFERRED]
- **LoRA Parameter Generation Methods** — drag_and_drop_llms, icm_lora, concept_hypernetwork [INFERRED]
- **Evidence for Dual-Signal Hypothesis** — task_arithmetic_tangent, concept_weight_disentanglement, icm_lora, weight_space_via_neural_field, concept_dual_signal [INFERRED]
- **LoRA Parameter Generation Paradigm** — oral_conditional_recurrent_diffusion, structureawarelorgen_lorangen, weight2weight_w2w_space, oral_parameter_generation [INFERRED 0.85]
- **Weight Space Structure and Geometry** — knowledgeinweightspace_weight_region, knowledgeinweightspace_linear_connectivity, dwsnets_permutation_symmetry, dwsnets_weight_alignment, selfsupervisedweightlearning_permutation_augmentation [INFERRED 0.85]
- **Low-Rank Hypothesis for Fine-Tuning** — intrinsicdimensionality_intrinsic_dimension, loraoriginal_rank_deficiency, loraoriginal_low_rank_adaptation, loralearnlessforgetless_high_rank_perturbation [EXTRACTED 0.95]

## Communities (8 total, 0 thin omitted)

### Community 0 - "Equivariant Weight Space Methods"
Cohesion: 0.34
Nodes (15): AdaLoRA (Zhang et al., ICLR 2023), DWSNets (Deep Weight Space Networks), Hypernetwork / Parameter Generation, LoRA (Low-Rank Adaptation), Permutation Symmetry / Invariance in Neural Networks, Weight Space Representation (WSR), Drag-and-Drop LLMs / DnD (Liang et al., 2025), Equivariant Deep Weight Spaces / DEEP-ALIGN (Navon et al., ICML 2024) (+7 more)

### Community 1 - "Low-Rank Adaptation Theory"
Cohesion: 0.33
Nodes (9): Intrinsic Dimension of Fine-Tuning, Intrinsic Dimensionality Explains the Effectiveness of Language Model Fine-Tuning, Structure-Aware Intrinsic Dimension (SAID), High-Rank Weight Perturbations in Full Fine-Tuning, LoRA Learns Less and Forgets Less, LoRA Learning-Forgetting Tradeoff, Low-Rank Adaptation (LoRA), LoRA: Low-Rank Adaptation of Large Language Models (+1 more)

### Community 2 - "Weight Alignment & Task Arithmetic"
Cohesion: 0.36
Nodes (8): Deep-Align Framework, Equivariant Deep Weight Space Alignment (Deep-Align / DWSNets), Permutation Symmetry of Neural Networks, Weight Alignment, Editing Models with Task Arithmetic, Task Arithmetic, Task Vector, Weight Interpolation

### Community 3 - "Model Merging & Task Vectors"
Cohesion: 0.48
Nodes (7): Dual-Signal Framing (WeightBench Core Concept), Model Merging, NTK Linearization / Tangent Space Fine-tuning, Task Vector, Weight Disentanglement, Task Arithmetic in Tangent Space (Ortiz-Jimenez et al., NeurIPS 2023), TIES-Merging (Yadav et al., NeurIPS 2023)

### Community 4 - "LoRA Parameter Generation"
Cohesion: 0.33
Nodes (7): Conditional Recurrent Diffusion for LoRA Generation, ORAL: Prompting Your Large-Scale LoRAs via Conditional Recurrent Diffusion, Neural Network Parameter Generation, LoRAGen Method, Module-Aware Mix-of-Experts (MoE) Decoder, Non-Uniqueness of Low-Rank Decomposition, LoRAGen: Structure-Aware Weight Space Learning for LoRA Generation

### Community 5 - "Weight Analysis & Self-Supervised Learning"
Cohesion: 0.38
Nodes (7): Predicting Trends in the Quality of State-of-the-Art Neural Networks without Access to Training or Testing Data, Power Law (Heavy-Tailed) Metrics for Model Quality, WeightWatcher Tool, Hyper-Representations of Neural Network Weights, Model Zoo, Self-Supervised Representation Learning on Neural Network Weights for Model Characteristic Prediction, Permutation Augmentation for Neural Network Weights

### Community 6 - "Weight Space Geometry"
Cohesion: 0.47
Nodes (6): Linear Mode Connectivity, Knowledge Is a Region in Weight Space for Finetuned Language Models, Knowledge Region in Weight Space, Meta-Latent Space over Model Weights, Weights2Weights: Interpreting the Weight Space of Customized Diffusion Models, weights2weights (w2w) Space

### Community 7 - "Factual Knowledge Editing"
Cohesion: 0.83
Nodes (4): Causal Mediation Analysis for Knowledge Localization, Mid-Layer MLP Modules as Factual Association Storage, Locating and Editing Factual Associations in GPT (ROME), Rank-One Model Editing (ROME)

## Knowledge Gaps
- **6 isolated node(s):** `Weight Interpolation`, `Neural Network Parameter Generation`, `WeightWatcher Tool`, `Structure-Aware Intrinsic Dimension (SAID)`, `Module-Aware Mix-of-Experts (MoE) Decoder` (+1 more)
  These have ≤1 connection - possible missing edges or undocumented components.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Knowledge Region in Weight Space` connect `Weight Space Geometry` to `Weight Alignment & Task Arithmetic`?**
  _High betweenness centrality (0.231) - this node is a cross-community bridge._
- **Why does `Low-Rank Adaptation (LoRA)` connect `Low-Rank Adaptation Theory` to `LoRA Parameter Generation`, `Weight Space Geometry`?**
  _High betweenness centrality (0.212) - this node is a cross-community bridge._
- **Why does `Task Vector` connect `Weight Alignment & Task Arithmetic` to `Weight Space Geometry`?**
  _High betweenness centrality (0.209) - this node is a cross-community bridge._
- **What connects `Weight Interpolation`, `Neural Network Parameter Generation`, `WeightWatcher Tool` to the rest of the system?**
  _6 weakly-connected nodes found - possible documentation gaps or missing edges._