---
source_url: https://arxiv.org/abs/2602.06043
captured_at: 2026-05-07
author: Kaushik, Vaidya, Chaudhari, Chellappa, Yuille (Feb 2026)
contributor: autonomous-loop
---
# Shared LoRA Subspaces for Almost Strict Continual Learning (Share) (arXiv:2602.06043)

## Core finding
A single dynamically updated **foundational low-rank subspace** extracted by SVD of stacked
LoRA B/A matrices across all tasks is sufficient for continual learning. Subsequent tasks
project into this frozen subspace rather than spawning new adapters. Achieves 100x parameter
reduction, 281x memory savings. Backward knowledge transfer: earlier tasks benefit from
subspace directions discovered for later tasks.

## Architecture
Phase 1 (Initialization): SVD of stacked LoRA matrices across initial task batch → extract
top-k principal basis vectors as the shared foundational subspace.
Phase 2 (Continual Adaptation): freeze the foundational subspace; new tasks project their
adaptation into this subspace only.
Phase 3 (Merging): merge task-specific projections with frozen subspace.

## Connection to fiber bundle / universal subspace
**The Share foundational subspace IS the fiber of the bundle.** In the fiber bundle framework:
- The fiber at W₀ = directions shared by all tasks = the "flat" directions (zero holonomy)
- The base space W/G = the quotient where GL_r acts on the fiber

Share empirically validates that such a shared fiber exists by finding it via SVD stacking.
The convergence of the foundational subspace across tasks = the universal weight subspace
hypothesis (2512.05117, ~16 dims shared by 1100+ models).

**Testable connection:** If Share's foundational subspace has approximately 16 stable principal
directions when computed over 100+ diverse tasks, that confirms the universal subspace paper's
~16-dim estimate. The two papers used different methods (Share: direct SVD stacking; universal:
ICA/PCA across pre-trained models) — convergence would be strong evidence.

## Backward knowledge transfer = retroactive holonomy
When Share discovers a new fiber direction for task t, it retroactively improves task t-1's
representation (backward transfer). In bundle terms: discovering a new horizontal direction
retroactively corrects the parallel transport for all earlier fine-tunings that passed through
that region. This is "retroactive holonomy correction" — updating earlier transports based on
a later-discovered connection coefficient.

## Connection to SRFM and gradient flow
SRFM (2410.18938) shows that each gradient step adds a rank-1 spike in the task direction.
Share shows that across many tasks, these spikes cluster in a low-dimensional subspace.
This means: the target directions w* for diverse tasks all lie in approximately the same
~16-dimensional subspace of the weight space. This is a consequence of:
1. Pre-training already encodes a compressed representation of the data distribution
2. Fine-tuning tasks are adjustments to this compressed representation
3. The adjustment directions are constrained by the geometry of the pre-trained model

## 100x parameter reduction implication
If all task-specific information can be represented as projections into a ~16-dim shared
subspace, then LoRA rank r = 16 is sufficient for any task for which a foundation model is
a reasonable prior. Ranks > 16 add intruder dims (above the fiber capacity) rather than
genuinely new task signal.

**Prediction from fiber bundle theory:** For well-pretrained foundation models, optimal LoRA
rank ≤ dim(universal fiber) ≈ 16. Ranks above this threshold primarily add intruder dims,
increasing forgetting without improving task performance. This is testable via the rank
tradeoff experiments in arXiv:2512.15634 (already in corpus).

## What this does NOT say
- No fiber bundle, connection, or holonomy language
- Does not explicitly identify the shared subspace with zero-holonomy directions
- No measurement of whether backward transfer comes from a specific holonomy structure
- The 100x compression is empirical; theoretical justification for why 16 dims suffice is not given
