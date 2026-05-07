---
source_url: https://arxiv.org/abs/2510.13003
captured_at: 2026-05-07
author: Yifeng Xiong, Xiaohui Xie (Oct 2025)
contributor: autonomous-loop
---
# OPLoRA: Orthogonal Projection LoRA Prevents Catastrophic Forgetting (arXiv:2510.13003)

## Core finding
Constraining LoRA updates to the orthogonal complement of the top-k singular subspace of the
pretrained weight matrix W₀ **exactly preserves** the top-k singular triples (mathematical
guarantee, not just empirical result). Introduces metric ρₖ quantifying how much updates
align with dominant W₀ directions.

## The constraint
ΔW must lie entirely in U_W₀^⊥ (orthogonal complement of top-k left singular vectors of W₀).
This is enforced via dual projections on A and B in the LoRA decomposition.

## Why this matters for fiber bundle theory
This is the operational definition of the HORIZONTAL SUBBUNDLE in practice:
  horizontal ⟺ orthogonal to top-k W₀ dominant directions
OPLoRA empirically proves that ΔW ∈ ker(ω) (horizontal subbundle) → zero forgetting.
The paper doesn't use fiber bundle or connection language, but the math is identical to
Theorem 3's horizontal constraint. This is independent empirical validation.

## What they do NOT do
- No fiber bundle, holonomy, or connection language
- No explanation of WHY gradient descent violates orthogonality (see 2602.15799)
- No four-way decomposition; only horizontal vs non-horizontal split

## Experiments
LLaMA-2 7B and Qwen2.5 7B; commonsense reasoning, math, code generation.
"Significantly reduces forgetting while maintaining competitive task-specific performance."
