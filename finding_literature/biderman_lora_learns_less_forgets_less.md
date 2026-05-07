---
source_url: https://arxiv.org/abs/2405.09673
captured_at: 2026-05-07
author: Biderman et al.
contributor: autonomous-loop
---
# LoRA Learns Less and Forgets Less (arXiv:2405.09673, TMLR 2024)

## Core finding
Lower rank LoRA learns less task-specific knowledge AND forgets less pretrained knowledge. The tradeoff is monotonic across r ∈ {16, 64, 256}. Full fine-tuning learns weight perturbations with rank 10–100× greater than typical LoRA.

## Rank-forgetting relationship
Monotonic: r=16 < r=64 < r=256 ≤ full fine-tuning in forgetting magnitude. Does not test r < 16.

## Mechanism claimed
Parameter count constraint — LoRA's limited capacity prevents large deviation from pretrained manifold. Does NOT analyze intruder dimensions or spectral structure.

## Relevance to intruder dimensions
Direct tension with Shuttleworth 2410.21228: low rank → more intruder dims (Shuttleworth) yet less forgetting (Biderman). Possible resolution: intruder_dim_magnitude not intruder_dim_count is the mediating variable.

## Key tables
Figure 2 shows rank vs. forgetting curves for code and natural language tasks separately. Code is more sensitive to rank than NL.
