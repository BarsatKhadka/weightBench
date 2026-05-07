---
source_url: https://arxiv.org/abs/2602.05536
captured_at: 2026-05-07
author: Yayuan Li, Ze Peng, Jian Zhang, Jintao Guo, Yue Duan, Yinghuan Shi (Feb 2026)
contributor: autonomous-loop
---
# When Shared Knowledge Hurts: Spectral Over-Accumulation in Model Merging (arXiv:2602.05536)

## Core finding
When multiple fine-tuned models share aligned spectral directions (overlapping column spaces
in their task vectors), linear merging inflates the singular values of those shared directions.
**Singular Value Calibration (SVC)** measures this column-space overlap and rescales inflated
singular values, improving Task Arithmetic by 13% without training or data.

## The mechanism: spectral over-counting
If task vectors ΔW_1 and ΔW_2 both have above-MP spikes in the SAME direction, then:
    ΔW_1 + ΔW_2 = spike_1 + spike_2 + noise_1 + noise_2

The shared spike direction gets doubled → singular value 2σ instead of σ → biases the
merged model toward that shared direction at the expense of task-specific components.

This is "spectral over-accumulation": repeated alignment of spikes inflates the merged model's
singular spectrum beyond what any individual task requires.

## What TRS predicts about merge failure
**TRS can predict spectral over-accumulation BEFORE merging** by checking spike-direction
overlap between task residuals. If task_A and task_B have genuine TRS spikes in the same
direction:
    cos(u_{TRS_A}, u_{TRS_B}) ≈ 1 → spectral over-accumulation predicted → merge will fail

This is a testable prediction: compute TRS for each task, measure pairwise spike alignment,
predict merge compatibility. Tasks with orthogonal TRS (low cosine similarity between spikes)
should merge without over-accumulation.

## Connection to holonomy / fiber bundle
SVC's calibration = removing the accumulated curvature from repeated traversal of the same
fiber direction. In bundle language: when two parallel transports follow the same path in
fiber space, the combined holonomy is just twice the individual holonomy — but the TOTAL
accumulated rotation is the physical quantity, not twice the single-task value.

SVC corrects for this by rescaling: it detects that the combined singular value is 2σ
(over-counted) and rescales back toward σ (the true per-task signal). This is the discrete
analog of holonomy renormalization.

## Connection to intruder dims
The shared spectral directions that over-accumulate are a mix of:
- Genuine TRS aligned between tasks → truly shared knowledge → SVC should preserve these
- Intruder dims that happen to align between tasks → spurious co-interference → SVC should reduce these

SVC doesn't distinguish the two. A TRS-aware SVC would: correct intruder dim over-accumulation
but preserve genuine TRS alignment.

## Performance
Improves Task Arithmetic by 13% on standard benchmarks without any training or additional data.
Compatible with TIES, DARE, TSV-Merge.

## What this does NOT say
- No fiber bundle, connection, or holonomy language
- Does not distinguish genuine TRS from intruder dims in the shared directions
- The calibration is post-hoc; does not prevent over-accumulation during fine-tuning
