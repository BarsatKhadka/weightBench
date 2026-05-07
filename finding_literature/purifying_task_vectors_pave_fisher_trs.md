---
source_url: https://arxiv.org/abs/2510.14697
captured_at: 2026-05-07
author: Bang An, Yibo Yang, Philip Torr, Bernard Ghanem (Oct 2025)
contributor: autonomous-loop
---
# Purifying Task Vectors in Knowledge-Aware Subspace for Model Merging: PAVE (arXiv:2510.14697)

## Core finding
Task vectors (ΔW = W_FT - W_B) contain task-irrelevant redundancy that interferes with
model merging. PAVE removes this via CO-SVD:

    ΔW_PAVE = SVD_r(W_FT · C) · C^{-1} - W_B

where C = XX^T is the input activation covariance matrix (empirical Fisher) computed from
task-specific training samples. Lifts RoBERTa GLUE from 80.18% to 84.28% when combined
with EMR-Merging.

## PAVE CO-SVD = Fisher-Metric TRS
**This is the most important connection: PAVE is TRS computed in the Fisher metric.**

Euclidean TRS: above-MP singular values of ΔW (Euclidean inner product)
PAVE CO-SVD: above-MP singular values of W_FT · C (Fisher-weighted inner product, C = XX^T)

SVD_r(W_FT · C) finds directions where the weight change ALIGNS WITH THE DATA MANIFOLD.
C = XX^T is the empirical second-moment matrix of inputs = the Fisher information matrix
(up to the output gradient factor, which is constant for square loss).

In fiber bundle language:
- Euclidean TRS: measures departure from MP bulk in Euclidean geometry
- PAVE CO-SVD: measures departure from MP bulk in Fisher geometry (natural gradient)

The difference between Euclidean TRS and PAVE CO-SVD measures how much the data distribution
deviates from isotropic (C ≠ I). When data is isotropic (C = I): PAVE = Euclidean TRS.
When data is anisotropic (C ≠ I): PAVE reweights directions by data frequency, naturally
upweighting task-relevant directions and downweighting task-irrelevant ones.

## Connection to intruder dims
PAVE's "task-irrelevant redundancy" = our intruder dims. Both are above-MP components of ΔW
that don't correspond to genuine task signal. PAVE removes them by data-informed reweighting;
Shuttleworth removes them by W₀-alignment criterion.

These are COMPLEMENTARY selection criteria:
- W₀-alignment criterion (Shuttleworth/TRS): "is this direction novel relative to pretraining?"
- Data-alignment criterion (PAVE/CO-SVD): "is this direction activated by task-specific data?"

A direction can be:
- W₀-orthogonal AND data-aligned → genuine TRS (both criteria select this)
- W₀-orthogonal AND data-unaligned → possible intruder dim (TRS selects, PAVE rejects)
- W₀-aligned AND data-aligned → intruder dim that happens to match task data (both reject)
- W₀-aligned AND data-unaligned → pure noise (both reject)

The intersection of W₀-orthogonal AND data-aligned directions is the "purified TRS":
directions where the fine-tuning added genuinely new knowledge activated by task data.

## Practical implication
Computing both TRS and PAVE CO-SVD for the same LoRA reveals:
- The 2x2 categorization above for each above-MP singular vector
- The "purified TRS" = TRS ∩ PAVE = the theoretically optimal LoRA subspace

No paper has computed this intersection. It would directly validate the TRS claim that
the Shuttleworth criterion selects the task-relevant subspace.

## What this does NOT say
- No fiber bundle, connection, or holonomy language
- Does not explicitly identify the CO-SVD connection to Fisher information (but C = XX^T is the empirical Fisher)
- The W₀-alignment criterion is not mentioned
- Full merging pipeline (PAVE + EMR) required for best performance; PAVE alone shows modest improvement
