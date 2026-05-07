---
source_url: https://arxiv.org/abs/1705.09280
captured_at: 2026-05-07
author: Gunasekar, Woodworth, Bhojanapalli, Neyshabur, Srebro (2017)
contributor: autonomous-loop
---
# Implicit Regularization in Matrix Factorization (arXiv:1705.09280)

## Core finding
Gradient descent on an underdetermined quadratic objective via full-dimensional factorization
W = UV^T, with small step size and initialization near zero, converges to the **minimum
nuclear norm solution** — without any explicit regularization. The nuclear norm ||W||_* =
Σᵢ σᵢ(W) is the implicit regularizer induced by the factorized parameterization and GD dynamics.

## Main theorem (informal)
For the objective min_{U,V} ||A(UV^T) - b||² with full-dimensional U,V matrices, gradient
descent converges to:
    argmin ||W||_*  subject to  A(W) = b
provided step size is small and initialization is near origin.

Proven in special cases (rank-1, diagonal); the full-rank case was conjectured (later confirmed
by extension papers including arXiv:2502.09376 which proves it for LoRA specifically).

## Connection to Marchenko-Pastur / TRS
The MP bulk = the "null" (no signal, pure noise singular value distribution).
Nuclear norm minimization = GD escapes the MP bulk as quickly as possible = sparse spectrum.
The minimum nuclear norm solution has as few above-MP singular values as needed to fit the
data — this is exactly the TRS criterion for the genuine signal.

**Implicit regularization IS the variational principle for TRS signal selection.**
Without explicit constraints, GD still finds solutions where only a few singular values exceed
the MP threshold — because nuclear norm minimization rewards sparsity in the singular spectrum.

## Connection to LoRA
arXiv:2502.09376 (in corpus) proves: LoRA training with zero-initialization and weight decay
converges to low-rank global minima via exactly this implicit bias mechanism. LoRA's explicit
low-rank constraint + implicit regularization together enforce horizontal subbundle conditions.

## Why this is foundational for the TRS framework
The TRS framework identifies the genuine signal as above-MP singular values. Gunasekar explains
WHY GD produces sparse above-MP spectra: nuclear norm minimization is the implicit regularizer.
The fiber bundle framework provides the GEOMETRY; implicit regularization provides the
VARIATIONAL DYNAMICS that enforce this geometry without explicit constraints.

## What this does NOT say
- No fiber bundle, connection, or holonomy language
- Does not distinguish genuine TRS from intruder dims (both are above-MP)
- The LoRA-specific application requires the extension papers
