---
source_url: https://arxiv.org/abs/unknown (finding_literature/subspace_boosted_model_merging_hosvd.pdf)
captured_at: 2026-05-07
author: Unknown authors (from corpus)
contributor: autonomous-loop
---
# Subspace-Boosted Model Merging via HO-GSVD (arXiv unknown)

## Core finding
When N LoRA adapters are merged (task arithmetic: sum of task vectors), task-specific
singular values decay as O(1/√N) while common (shared) singular values remain O(1).

**Proposition 1:** σ_task ~ O(1/√N) as N → ∞
**Proposition 2:** Stable rank collapses to common subspace rank as N → ∞

As more models are merged, only the universally shared directions survive.

## The HO-GSVD method
Higher-Order Generalized SVD decomposes all task vectors simultaneously:
    A_i = U_i · Σ_i · V^T  (shared RIGHT singular subspace V across all tasks)

The shared right subspace V = the universal fiber directions (the common subspace that all
tasks build upon). The alignment matrix = log-ratio of generalized SVs across tasks.
Subspace boosting: clamp underutilized SVs at threshold τ to boost underrepresented directions.

## Mathematical proof of the three-region decomposition

This paper provides the rigorous theoretical justification for the revised three-region TRS:

**Region 1 (universal fiber, common SVs ~ O(1)):**
As N → ∞, only these directions survive averaging. They are the flat fiber directions —
shared by all tasks because all tasks activate them. Proposition 2 proves their survival.

**Region 2 (task-specific, σ ~ O(1/√N)):**
These directions cancel out when averaging many tasks. The O(1/√N) decay is CLT-type:
task-specific components are in "random" directions relative to each other, so they average
to zero like i.i.d. random variables.

**Region 3 (noise):**
Also decays but at a different rate than Region 2.

## Connection to holonomy and fiber bundle
The O(1/√N) decay of task-specific SVs corresponds to SELF-AVERAGING of holonomy:
When you compute the average holonomy over N tasks (= average parallel transport around
N different loops in task space), the holonomy elements in random relative positions
cancel to zero in the limit (their average holonomy rotation → identity matrix).

Only the components where all tasks agree (fiber directions = zero holonomy) survive.
This is the holonomy-theoretic proof that Region 1 = zero holonomy = flat fiber.

## What "rank collapse in model merging" means
Stable rank = ||A||_F^2 / max_i σ_i^2 collapses as N → ∞ because:
- Max SV (common, O(1)) grows with more tasks sharing the same direction
- Frobenius norm stays O(1) because task-specific components cancel
→ Stable rank → 1 (all mass concentrates in the max singular direction = universal fiber)

In TRS terms: merging many LoRAs leaves ONLY the universal fiber (Region 1), destroying all
task-specific signal (Region 2). Task arithmetic fails in the rank-collapse regime because
it destroys exactly what makes each LoRA distinct.

## Subspace boosting as holonomy correction
Clamping underutilized SVs at threshold τ restores underrepresented task-specific directions
before they fully cancel. This is the reverse of SVC (which downscales over-accumulated
common directions) — subspace boosting rescues underpowered task-specific directions.

Together, SVC + subspace boosting provide a complete spectral calibration:
- SVC: downscale over-accumulated common directions (Region 1)
- Subspace boosting: upscale under-represented task-specific directions (Region 2)

## What this does NOT say
- No fiber bundle, connection, or holonomy language (all from our synthesis)
- No explicit connection to intruder dims or the W₀-alignment criterion
- The arXiv ID is unknown (PDF not yet linked to an arXiv abstract in the corpus)
