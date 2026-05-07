---
source_url: https://arxiv.org/abs/2410.21228
captured_at: 2026-05-07
author: Shuttleworth et al. (Oct 2024)
contributor: autonomous-loop
---
# LoRA vs Full Fine-tuning: An Illusion of Equivalence (arXiv:2410.21228)

## Core finding — THE FOUNDATION PAPER
LoRA introduces **intruder dimensions**: novel high-ranking singular vectors of ΔW that are:
1. Absent in the base model W₀ (new directions, not present in pretrained representation)
2. Absent in full fine-tuning ΔW (full FT does not create these same novel directions)
3. Above the Marchenko-Pastur threshold (above noise)
4. Causally linked to catastrophic forgetting: reducing their singular values improves
   pre-training distribution retention with minimal task performance drop

## Definition of intruder dimensions
A singular vector u of ΔW = BA is an intruder dimension if:
    max_j cos(u, u_j^{W₀}) < threshold  (typically ~0.3)
where u_j^{W₀} are the top-k right singular vectors of W₀.

**In geometric language:** u is an intruder dim iff it lies outside the dominant singular
subspace of W₀ = it is NOT in the horizontal subbundle ker(ω).

## The causal claim
Reducing intruder dimension singular values (via intervention) → reduced forgetting, minimal
task performance drop. This is a CAUSAL experiment, not just correlation.

The mechanism: intruder dims overwrite W₀'s dominant singular subspace with novel directions
from the LoRA parameterization. This overwrites pretrained knowledge → forgetting.

## Why LoRA produces intruder dims but full FT does not
Full FT gradient descent implicitly regularizes toward minimum nuclear norm (Gunasekar 1705.09280),
distributing updates across the existing spectral structure. LoRA forces ΔW = BA (rank r),
which concentrates updates into r singular directions. When those r directions don't align
with W₀'s structure, they become intruder dims.

## Connection to everything else in the corpus

**SRFM (2410.18938):** After one GD step, W^1 = W^0 + uv^T + Δ. The spike uv^T is the
intruder dim prototype. Whether v aligns with W₀ determines genuine TRS vs. intruder.

**OPLoRA (2510.13003):** Directly implements the anti-intruder constraint: ΔW ∈ U_{W₀}^⊥.

**EBLoRA (2602.00722):** Flat singular values + gradient orthogonality = reduces intruder dims
by forcing equal energy across directions + avoiding previous task directions.

**Alignment Collapse (2602.15799):** Provides the dynamical explanation for why intruder
dims appear even with horizontal initialization: quartic curvature coupling t^4.

**TRS (this project):** The intruder dimensions are the above-MP, W₀-misaligned subset of
the four-way spectral decomposition: Genuine TRS (above-MP, aligned) / Intruder dims
(above-MP, misaligned) / MP bulk (noise) / Suppression (below zero).

## The revised five-region view (from synthesis 12)
In the three-region spectral decomposition:
- Region 1 (very large SV, universal fiber): NO intruder dims here (these are W₀-aligned shared directions)
- Region 2 (moderate above-MP, task-specific): INTRUDER DIMS live here (W₀-misaligned) + genuine TRS (W₀-orthogonal)
- Region 3 (below MP): noise

## What this does NOT say
- No fiber bundle, connection, or holonomy language
- The paper doesn't propose a solution (OPLoRA, EBLoRA solve it; this paper diagnoses it)
- The W₀-alignment threshold (0.3) is empirical, not derived from theory
- No explicit connection to the universal subspace or fiber directions
