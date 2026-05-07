---
source_url: https://arxiv.org/abs/2502.09376
captured_at: 2026-05-07
author: Kim et al. (Feb 2025)
contributor: autonomous-loop
---
# LoRA Training Provably Converges to a Low-Rank Global Minimum (arXiv:2502.09376)

## Core finding
LoRA fine-tuning with zero-initialization of B (standard practice: B=0, A random) and
weight decay converges to low-rank global minima via the implicit regularization bias
established by Gunasekar et al. (1705.09280). This provides a formal proof that LoRA's
convergence to low-rank solutions is not merely a consequence of its low-rank parameterization
but of the interaction between parameterization, weight decay, and gradient descent dynamics.

## What this proves for the TRS framework
Standard LoRA training (zero-init B, weight decay) implicitly enforces:
    argmin ||ΔW||_*  subject to task loss constraints

This means LoRA's update ΔW = BA is implicitly pushed toward minimum nuclear norm =
minimum total singular value mass = sparse spectrum = few above-MP components.

Combined with Shuttleworth (2410.21228): the above-MP components that DO appear are a mix
of genuine TRS (W₀-aligned) and intruder dims (W₀-misaligned). Implicit regularization
minimizes their total count; the split between genuine vs intruder is determined by the
optimization trajectory and initialization.

## Connection to OPLoRA / horizontal subbundle
OPLoRA (2510.13003) enforces ΔW ∈ U_W₀^⊥ by explicit projection.
Implicit regularization pushes toward minimum nuclear norm (sparse above-MP spectrum).
These are complementary but different constraints:
- Implicit reg: minimize NUMBER of above-MP components
- OPLoRA: ensure W₀-alignment of whatever above-MP components exist

Together they give: few above-MP components, all W₀-aligned = pure genuine TRS, zero intruder dims.

## What this does NOT say
- No fiber bundle or holonomy language
- Does not distinguish TRS from intruder dims in the above-MP subset
- The "low-rank global minimum" is global in the sense of training objective, not in
  the sense of W₀ geometry (no alignment analysis)
