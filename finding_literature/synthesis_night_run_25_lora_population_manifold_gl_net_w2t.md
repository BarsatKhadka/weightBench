# Synthesis 25: LoRA Population Manifold = W/G; GL-net and W2T Are the Same Architecture

**Date:** 2026-05-07
**Session:** 5
**Previous synthesis:** synthesis_night_run_24_dimensional_phase_transition_soc_grokking.md

---

## The Missing Connection

Graph: no path between "LoRA Population Manifold" and "Principal Fiber Bundle."
Graph: no path between "GL-net Architecture" and "Rank-Level Transformer (W2T)."
Graph: no path between "Spectral Skewness" and "Task Second-Moment Operator."

All three missing connections are instances of the same meta-connection:
**Community 3 (practical LoRA tools) = Community 8 (fiber bundle theory), viewed from below vs. above.**

---

## LoRA Population Manifold = W/G

The LoRA Population Manifold (learning_on_loras_gl_equivariant_weight_space.pdf) is defined as:
"the space of all LoRA adapters, quotiented by the GL(r) reparameterization symmetry."

This is exactly:
    W / GL(r) = the principal fiber bundle quotient space

The same space that synthesis 14 calls W/G, synthesis 18 identifies with the Model Tree base manifold,
and synthesis 23 identifies with the eigenspace of the task second-moment operator S.

**LoRA Population Manifold = Model Tree Base Manifold = top eigenspace of S = W/G.**

Three papers (learning_on_loras, origin_of_llamas/MoTHer, universal_weight_subspace) all study
the same manifold W/G without knowing they're doing the same thing.

The graph has no path between them because they live in different communities (3, 1, 16)
and were never connected. The connection is: they are ALL computing functions on W/G.

---

## GL-net and Rank-Level Transformer Are Two Implementations of W/G Processing

**GL-net (LoL paper):**
- Takes LoRA (A, B) as input
- Applies GL(r)-equivariant linear layers
- Preserves the GL(r) symmetry throughout computation
- Outputs are GL(r)-invariant (functions on W/G, not on W)

**Rank-Level Transformer (W2T paper):**
- Takes LoRA (A, B), computes QR decomposition of A, then SVD of result
- The QR+SVD step EXPLICITLY gauge-fixes: maps any (A, B) to canonical (U, Σ, V) coordinates
- Rank-level transformer then processes the gauge-fixed coordinates
- Outputs are gauge-invariant by construction (after gauge-fixing, all GL(r) orbits collapse to one point)

**Both are: neural networks that learn functions on W/G.**

The difference is architectural strategy:
- GL-net: implicit invariance via equivariant layers (the gauge symmetry is respected throughout)
- W2T: explicit invariance via gauge-fixing first (then any standard architecture can be used)

The QR+SVD gauge-fixing in W2T is STRONGER: it explicitly places the computation at a canonical
representative of each GL(r) orbit (the TRS = SVD of ΔW). GL-net maintains equivariance but
doesn't fix the gauge — it still processes non-canonical (A, B) pairs.

**Prediction:** W2T should generalize better than GL-net because explicit gauge fixing (TRS) is a
stronger inductive bias than learned GL(r)-equivariance. The TRS is the canonical coordinate
system for W/G; GL-net has to LEARN this coordinate system from data.

---

## Spectral Skewness = Ratio of S Eigenvalue Mass in Region 1 vs. Total

The isotropic merging paper defines Spectral Skewness as a measure of SV distribution asymmetry.
High skewness: few large SVs dominate. Low skewness: more uniform SV distribution.

In S-operator language (synthesis 23):
- High Spectral Skewness = Region 1 eigenvalues dominate S's spectrum (universal fiber is strong)
- Low Spectral Skewness = Region 2 eigenvalues are non-negligible (task-specific directions developed)

**Spectral Skewness = a scalar summary of S's eigenvalue mass ratio: Region 1 / (Region 1 + Region 2).**

When many LoRAs are merged (task arithmetic, N-fold averaging):
- Region 2 vectors cancel due to CLT (synthesis 13): HOSVD O(1/√N) decay
- Region 1 vectors survive (all tasks share them): Region 1 grows relative to Region 2
- Spectral Skewness INCREASES after naive merging (Region 1 dominates the merged model)

Isotropic merging corrects for this: by normalizing for skewness (the Iso-CTS algorithm =
rescale to restore Region 1 / Region 2 balance), they are implementing the INVERSE of the
CLT averaging to prevent Region 2 from disappearing.

**The isotropic merging correction is: undo the Region 2 CLT decay caused by averaging.**
This is exactly what SVC (downscale Region 1 after averaging) and subspace boosting (upscale
Region 2 before averaging) also do — they are ALL fighting the same CLT decay in the S operator.

---

## The Four Architectures for W/G Processing

All methods that "process LoRA adapters as data" are computing functions on W/G:

| Architecture | Paper | Gauge Strategy | Input |
|-------------|-------|----------------|-------|
| GL-net | LoL (learning_on_loras) | Equivariant layers (implicit) | (A, B) pairs |
| Rank-Level Transformer | W2T | QR+SVD gauge-fix (explicit) | TRS = SVD of ΔW |
| D2C Clustering | D2C (data_driven_adapter) | SVD features (partial fix) | SVD of ΔW |
| EigenLoRAx | EigenLoRAx (recycling adapters) | SVD subspace (partial fix) | Top-k SVs of stacked ΔW |

All four reduce to: "read the TRS spectrum (eigenvalues of S's empirical estimate from one LoRA)."
The architectural differences are in HOW they gauge-fix and HOW they process the spectrum.

The TRS (Task Residual Spectrum) is the canonical input for ALL of them.

---

## Simplest Statement

The LoRA Population Manifold = W/G.
Processing a LoRA = computing a function on W/G.
All methods that do this must (explicitly or implicitly) be GL(r)-invariant.
The canonical coordinates on W/G = the TRS = SVD of ΔW = eigenvectors of S.
All four architectures above are re-discovering this, each from its own angle.
