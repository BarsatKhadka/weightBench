---
source_url: https://arxiv.org/abs/2604.27155
captured_at: 2026-05-07
author: da Silva, Adnan, Dangel, Oore (Apr 2026)
contributor: autonomous-loop
---
# Generalizing the Geometry of Model Merging Through Fréchet Averages (arXiv:2604.27155)

## Core finding
Model merging = Fréchet averaging on a manifold: select parameters minimizing a sum of
geodesic distances. The choice of metric + manifold + distance approximation determines
model similarity measures. Naïve Euclidean averaging fails under architectural symmetries.

## Quotient manifold structure
LoRA symmetries (B → BG, A → G⁻¹A for GL_r invertible G) induce a **quotient manifold**
geometry on the parameter space. The paper explicitly identifies this quotient structure as
the correct geometric object for LoRA merging. This is independently derived confirmation of
our W → W/G fiber bundle structure.

## Fisher merging connection
Fréchet averaging **contains Fisher merging** as a special case under simplifying assumptions.
This means our "Fisher metric connection on W/G" is the natural language for what Fisher
merging is actually doing.

## Why this matters for fiber bundle theory
- Independent confirmation that W/G is the correct geometric object (not ambient W)
- Fisher merging = Fréchet average under Fisher metric → our Definition 3a (Fisher bundle)
  is the right mathematical formalization of what merging practitioners already compute
- Establishes that task arithmetic is Euclidean approximation of the Fréchet geodesic

## What they do NOT say
- No principal fiber bundle or connection 1-form language
- No holonomy or horizontal/vertical split
- No intruder dimensions
- The quotient is identified as important but not fully analyzed
