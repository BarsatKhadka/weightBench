---
source_url: https://arxiv.org/abs/2602.18523
captured_at: 2026-05-07
author: Yongzhong Xu (Feb 2026)
contributor: autonomous-loop
---
# The Geometry of Multi-Task Grokking: Transverse Instability, Superposition, and Weight Decay Phase Structure (arXiv:2602.18523)

## Core finding
Multi-task grokking solutions (generalization after memorization) occupy only **4-8 principal
trajectory directions** while remaining distributed across full-rank weights. Optimization is
"confined to an empirically invariant low-dimensional execution manifold."

## Key geometric claims
- "Holographic incompressibility": solutions live in a low-dimensional manifold but cannot be
  compressed without loss (the full weight matrix is needed, just most dimensions are frozen)
- "Commutator defects orthogonal to this manifold" — interference between tasks produces
  residuals orthogonal to the invariant manifold
- Curvature depth varies with weight decay; weight decay = phase transition parameter

## Connection to fiber bundle theory
The "invariant low-dimensional execution manifold" ≈ the horizontal subbundle of our bundle.
"Commutator defects orthogonal to this manifold" = intruder dims that have escaped the fiber.
The 4-8 principal directions ≈ genuine TRS (above-MP, fiber-aligned) directions.

This paper provides the most explicit language connecting multi-task optimization dynamics to
a low-dimensional manifold geometry, consistent with our bundle picture.

## What they do NOT say
- No fiber bundle, holonomy, or connection language
- "Commutator" language from algebra, not differential geometry
- No connection to Fisher metric or LoRA specifically
- No forgetting measurement; grokking ≠ catastrophic forgetting exactly
