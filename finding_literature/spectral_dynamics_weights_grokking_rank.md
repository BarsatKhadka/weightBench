---
source_url: https://arxiv.org/abs/2408.11804
captured_at: 2026-05-07
author: Yunis, Patel, Wheeler, Savarese, Vardi, Livescu, Maire, Walter (Aug 2024)
contributor: autonomous-loop
---
# Approaching Deep Learning through the Spectral Dynamics of Weights (arXiv:2408.11804)

## Core finding
Weight matrix singular values and vectors evolve in characteristic, architecture-agnostic
patterns during training. The central empirical result: **grokking coincides precisely with
a drop in effective rank**. Generalizing networks converge to low-rank weight solutions;
memorizing networks (random labels) remain high-rank. This is confirmed across ConvNets,
LSTMs, Transformers, and UNets.

## Key empirical findings
- Effective rank consistently decreases throughout training for generalizing networks
- **Top singular vectors stabilize in direction early in training**, before optimization converges
  — the direction of task signal crystallizes before the magnitude settles
- True labels → low-rank W; random labels → high-rank W (memorization signature)
- **Weight decay amplifies the low-rank bias** beyond simple norm regularization: it selectively
  enhances dominant singular values while suppressing near-zero ones
- Linear mode connectivity between two solutions correlates with shared top singular vectors

## Connection to TRS / intruder dim theory
Grokking = rank minimization = transition from high-intruder-dim (vertical fiber) to
low-intruder-dim (horizontal subbundle) solution.

**The memorization solution is a vertical fiber solution:** many above-MP singular values
(intruder dims) are active, encoding spurious task-label correlations. **The generalization
solution is a horizontal subbundle solution:** only the genuine TRS survives (few above-MP
components, aligned with W₀ fiber structure).

Weight decay = the force that pushes toward the horizontal subbundle (by suppressing
intruder-dim singular values below the MP threshold).

Anti-grokking (late-stage generalization collapse, also in corpus) = intruder dims re-emerging
and overwhelming genuine TRS, causing the network to drift back into the vertical fiber.

## Companion paper connection
arXiv:2410.17770 (Small Singular Values Matter, already in corpus) uses Marchenko-Pastur as
the explicit null hypothesis. Both ends of the spectrum carry information: the top (signal
outliers above MP bulk) and the bottom (unexpected structure in small SVs) deviate from MP.
This challenges "only top-k SVs = signal" — the full departure from MP matters.

## What this does NOT say
- No Fisher Information analysis
- No fiber bundle, connection, or holonomy language
- The rank-minimization mechanism is empirical, not derived from a variational principle
  (Gunasekar 1705.09280 provides the variational principle: nuclear norm minimization)
