---
source_url: https://arxiv.org/abs/2604.08844
captured_at: 2026-05-07
author: Anonymous (April 2026)
contributor: autonomous-loop
---
# Spectral Geometry of LoRA Adapters Encodes Training Objective (arXiv:2604.08844, April 2026)

## Core finding
Per-layer spectral features (Frobenius norm, stable rank, singular-value entropy, effective rank, singular-vector cosine alignment to pretrained weights) can CLASSIFY which fine-tuning objective was applied. Query-projection weights detect training objective drift; value-projection weights identify specific objectives.

## Connection to Q/K vs V/O asymmetry
Directly validates the Q/K vs V/O functional asymmetry identified in synthesis_5: Q weights encode training objective information more strongly than V weights. This is consistent with Q/K = connection curvature (changes training trajectory) vs V/O = parallel transport (linear, objective-neutral).

## Relevance to intruder dimensions
Does not study catastrophic forgetting directly. However, the spectral features it uses (singular-vector cosine alignment to pretrained W0) are exactly the intruder dimension diagnostic. Validates that this measurement is meaningful for understanding adapter behavior.

## Key methodology
Extracts per-layer spectral signatures and trains a classifier on top. Can identify: alignment-based fine-tuning, RLHF, DPO, supervised instruction tuning from weight structure alone.
