---
source_url: https://arxiv.org/abs/2412.09250
captured_at: 2026-05-07
author: Ed-dib, Datbayev, Aboussalah (NYU/Nace.AI), EMNLP 2025 Findings
contributor: autonomous-loop
---
# GELoRA: Geometric Adaptive Rank for LoRA Fine-tuning (arXiv:2412.09250)

## Core finding
**LoRA rank has a geometric lower bound: r_i ≥ max(d_{i+1} − d_i, 0)**
where d_i is the intrinsic dimensionality of the data manifold at the input to transformer
block i. The adaptive rank formula is: **r_i = max(d_{i+1} − d_i, 0) + 1**.

## The rank bound theorem (informal)
Fine-tuning task φ requires rank r_i such that:
    rank(ΔW_i) ≥ intrinsic_dim(φ at layer i) — intrinsic_dim(φ at layer i+1)

The intuition: if the data manifold expands from layer i to layer i+1 (d_{i+1} > d_i),
extra rank is needed to represent the expansion. If it contracts, rank 1 suffices.
The FIM defines "local dimensionality" as the rank of I(φ) — the effective number of
independently influential parameters.

## Connection to TRS / intruder dims

**GELoRA's intrinsic dimension = number of genuine TRS directions**

The genuine TRS count for a task = number of independent directions the task requires
beyond the pretrained representation = intrinsic dimensionality of the task adjustment.

**Corollary:** Intruder dim count ≈ r − d_task (approximately)
If LoRA uses rank r > intrinsic dimension of the task:
- First d_task components: genuine TRS (one per independent task dimension)
- Remaining r − d_task components: intruder dims (rank exceeds task need → spurious)

This gives a geometry-based criterion for expected intruder dim count before measuring it.
Testable: for tasks with known intrinsic dimension, measure intruder Frobenius energy at rank r
and verify it scales with r − d_task.

## Conjecture 3.1: convergence during fine-tuning
"The gap between intrinsic dimension and transformer rank decreases as fine-tuning progresses."

In TRS language: as fine-tuning proceeds:
- More genuine TRS directions accumulate (rank increases toward intrinsic dim)
- If training continues past this point: extra components become intruder dims
- Early stopping at rank ≈ intrinsic dim gives pure genuine TRS, no intruder dims

This provides a NEW STOPPING CRITERION: stop fine-tuning when rank(ΔW) ≈ intrinsic_dim(task).
Any further training adds intruder dims without task signal.

## TwoNN intrinsic dimension estimator
GELoRA uses the TwoNN method: measure intrinsic dimensionality of hidden state distributions
at each transformer layer. The transition layers where d_{i+1} > d_i need higher LoRA rank;
layers where d_i decreases need lower rank (or rank = 1).

In fiber bundle terms: the data manifold dimension changes across transformer layers —
layers with high d_i have a higher-dimensional task adjustment space (larger fiber).

## GLUE results
DeBERTaV3-base: 87.92 GLUE average. Competitive with fixed-rank LoRA while being adaptive
and geometrically principled.

## What this does NOT say
- No fiber bundle, connection, or holonomy language
- Uses FIM for local dimensionality definition but not as a metric for LoRA parameter space
- The W₀-alignment criterion is not applied
- No measurement of whether intruder dims scale with r - d_task (untested conjecture)
