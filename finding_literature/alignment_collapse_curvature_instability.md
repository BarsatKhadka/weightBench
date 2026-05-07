---
source_url: https://arxiv.org/abs/2602.15799
captured_at: 2026-05-07
author: Springer, Lee, Metevier, Castleman, Turbal, Jung, Shen, Korolova (Feb 2026)
contributor: autonomous-loop
---
# The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety (arXiv:2602.15799)

## Core finding
Orthogonality to safety-critical directions is **structurally unstable** under gradient descent.
Fine-tuning on benign tasks systematically degrades safety mechanisms even when updates are
initialized orthogonally. Alignment loss grows as the **fourth power of training time**.

## The mechanism
Gradient descent generates "second-order acceleration that systematically steers trajectories
into alignment-sensitive (non-horizontal) subspaces." Three geometric properties jointly cause
this — formalized as the "Alignment Instability Condition."

## The quartic scaling law
alignment_loss(t) ∝ t^4 × sharpness × curvature_coupling

The quartic exponent comes from second-order effects: the curvature of the loss landscape at
the initialization point couples to the gradient direction, accelerating the drift out of the
orthogonal complement with each step.

## Critical implication for fiber bundle theory
This is the mechanistic explanation for WHY intruder dims appear even with horizontal
initialization (e.g., FILet):
1. FILet initializes horizontally (in ker(ω))
2. Gradient descent on the task loss has nonzero curvature coupling at the horizontal manifold
3. This curvature coupling drives the trajectory into non-horizontal (intruder dim) directions
4. The quartic law predicts the rate of intruder dim accumulation during training

Combined with OPLoRA (2510.13003): orthogonal initialization is the right geometric target,
but staying there requires either constrained optimization or very few training steps.

## Connection to Conjecture 2 (holonomy-intruder)
The "alignment loss" in this paper ≈ our intruder dim Frobenius energy.
The quartic law gives a DYNAMICAL PREDICTION: intruder Frobenius energy ∝ training_steps^4
for standard gradient descent, governing forgetting independently of rank.

## What they do NOT say
- No fiber bundle, holonomy, or connection language
- Safety context (alignment ≠ catastrophic forgetting exactly), but the mechanism is the same
- Does not identify intruder dimensions by name, but the phenomenon is identical
