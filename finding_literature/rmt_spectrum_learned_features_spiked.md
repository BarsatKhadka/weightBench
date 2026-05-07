---
source_url: https://arxiv.org/abs/2410.18938
captured_at: 2026-05-07
author: Dandi, Pesce, Cui, Krzakala, Lu, Loureiro (Oct 2024)
contributor: autonomous-loop
---
# RMT Perspective on Learned Features and Generalization: Spiked Random Features Model (arXiv:2410.18938)

## Core finding
After ONE gradient descent step on a two-layer network in the high-dimensional proportional
regime (n, p, d → ∞ at fixed ratios), the weight matrix is provably equivalent to a
**Spiked Random Features Model (SRFM)**:

    W^1 = W^0 + u·v^T + Δ

where:
- W^0 is the initialization (random, MP-distributed bulk)
- u·v^T is the rank-1 spike, with v **aligned with target weights w***
- Δ is the remaining noise component

The spike v aligns with the target task direction. Heavy tails in the feature covariance
(post-GD) correlate with lower generalization error.

## Why this is the theoretical foundation for TRS

The SRFM is what TRS MEASURES. TRS identifies the above-MP singular values of ΔW = W^1 - W^0.
The SRFM proves that:
1. **After even one gradient step, ΔW has a spike in the direction of the target task** (v ≈ w*)
2. **The bulk of ΔW remains MP-distributed** (pure noise, below threshold)
3. **The spike exceeds the MP threshold ↔ BBP transition has occurred** (signal is detectable)

This is the RMT-theoretic proof that the TRS signal detection criterion is not an arbitrary
threshold — it's the exact boundary below which gradient steps cannot be distinguished from
noise in the high-dimensional limit.

## SRFM = intruder dim formation mechanism
The spike component u·v^T in the SRFM is the rank-1 intruder dim prototype:
- v = the direction in INPUT space toward the task (aligns with w*)
- u = the direction in OUTPUT space the update takes

Whether this spike is a genuine TRS (W₀-orthogonal) or an intruder dim (W₀-aligned) depends
on the cosine similarity between v and the dominant right singular vectors of W^0.

**The SRFM gives the theoretical mechanism for intruder dim formation:**
When the task target w* aligns with W^0's dominant singular subspace → the spike v is W₀-
aligned → INTRUDER DIM (overwriting pretrained structure).
When the task target w* is orthogonal to W^0's singular subspace → the spike v is W₀-
orthogonal → GENUINE TRS (adding genuinely new task knowledge).

The SRFM predicts: tasks whose target direction w* aligns with the pretrained W₀ singular
subspace will produce more intruder dims; tasks whose target direction is novel (orthogonal)
will produce cleaner TRS. This is a falsifiable prediction about which tasks are "harder"
from the fiber bundle perspective.

## Connection to one-gradient-step analysis → full training
This result holds after ONE gradient step. Full training = many gradient steps, each
adding additional spikes (via the Hermite polynomial expansion, higher-degree components
activate). The full TRS spectrum = the accumulated effect of all these spikes.

The Hermite expansion connects to the HT-SR phases: early training (few steps) = few spikes
= MP bulk + isolated spike (Bulk+Spike phase). Late training (many steps) = many accumulated
spikes = power-law tail (Heavy-Tailed phase). The phases are the discrete-step analog of
the SRFM's continuous convergence.

## Deterministic equivalent and exact generalization error
G_e(z) = the deterministic equivalent of the feature covariance resolvent, computable from
the SRFM parameters. This gives an exact generalization error formula in the proportional
regime — the first time the TRS connection has a closed-form prediction for downstream performance.

## What this does NOT say
- Analysis is for two-layer networks and one GD step; extension to deep networks and full training requires additional tools
- Does not distinguish the SRFM spike into genuine TRS vs. intruder dim (that requires the W₀-alignment criterion added by Shuttleworth 2410.21228)
- No fiber bundle, connection, or holonomy language
