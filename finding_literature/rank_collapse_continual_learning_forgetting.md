---
source_url: https://arxiv.org/abs/2603.04580
captured_at: 2026-05-07
author: Yunqin Zhu, Jun Jin (Mar 2026)
contributor: autonomous-loop
---
# Why Do Neural Networks Forget: A Study of Collapse in Continual Learning (arXiv:2603.04580)

## Core finding
Structural collapse (measured as effective rank eRank of weight matrices and activations) is
strongly correlated with catastrophic forgetting. When weight matrices become low-rank during
continual learning, the network loses plasticity and cannot learn new tasks without overwriting
old representations.

## What they measure
**Weight matrix eRank** (effective rank = exp(H(σ/||σ||)) where H is entropy of normalized
singular value distribution) — NOT Fisher Information Matrix rank. This is an important
distinction: they measure the rank of W itself, not the curvature structure.

## Causal direction
rank_collapse(W) → loss of plasticity → catastrophic forgetting
The mechanism: a low-rank weight matrix cannot expand its feature space to accommodate new
task representations; new tasks overwrite the existing low-rank structure.

## Relevance to TRS
This paper measures rank collapse of W, not ΔW. But it supports the geometric picture:
as ΔW accumulates across tasks, W's singular subspace concentrates (rank effectively drops
in the null space of prior tasks). This is consistent with intruder dims accumulating as W
drifts from the W₀ fiber.

## What this does NOT resolve
Does not measure FIM rank — this is still a gap. The paper concerns weight rank not curvature.
Does not use fiber bundle or subspace alignment language.
