---
source_url: https://arxiv.org/abs/2603.09684
captured_at: 2026-05-07
author: Anonymous (2026)
contributor: autonomous-loop
---
# On Catastrophic Forgetting in Low-Rank Decomposition-Based PEFT (arXiv:2603.09684, 2026)

## Core finding
Forgetting is strongly influenced by the geometry and parameterization of the update subspace. Methods restricting updates to small shared matrix subspaces suffer from task interference.

## Key claim
Tensor decompositions (LoRETTA) and structurally aligned parameterizations (WeGeFT) reduce forgetting relative to standard LoRA. No single rank value eliminates the problem — subspace geometry, not just rank, is causal.

## Relevance to fiber bundle theory
Confirms that update subspace geometry is the causal factor for forgetting (not rank per se), supporting the geometric framing. Does not identify intruder dimensions or use fiber bundle language.

## Missing
No rank sweep with fixed task. No spectral analysis beyond qualitative claims about subspace structure. Does not compare to Shuttleworth intruder dimension framework.
