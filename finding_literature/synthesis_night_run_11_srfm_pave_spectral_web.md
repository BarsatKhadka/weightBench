# Synthesis 11: The Spectral Web — SRFM, PAVE, Over-Accumulation, and the GradientSpace Dual

**Date:** 2026-05-07
**Session:** 4 (continued)
**Previous synthesis:** synthesis_night_run_10_horizontal_implementations_sheaf.md

---

## Overview

Five papers already in the corpus were examined for the first time in this session. Together
they form a "spectral web" — each paper observing the same underlying spectral geometry from
a different vantage point:

1. SRFM (2410.18938): ONE gradient step → spike formation in target direction → TRS origin
2. GradientSpace (2512.06678): gradient singular vectors = task fingerprint during training
3. Share (2602.06043): shared LoRA subspace across tasks = universal fiber directions
4. Spectral Over-Accumulation (2602.05536): aligned TRS spikes inflate during merging
5. PAVE (2510.14697): CO-SVD on W_FT · C = Fisher-metric TRS

None of these papers cites the others in the TRS/intruder-dim context. None uses fiber
bundle language. But they all describe the same underlying geometry.

---

## 1. SRFM: The Theoretical Origin of TRS Spikes

The Spiked Random Features Model (arXiv:2410.18938) proves that after one gradient descent step:

    W^1 = W^0 + u·v^T + Δ

where v ALIGNS with the target task direction w*. The spike u·v^T is the rank-1 prototype
of a genuine TRS direction. The rest Δ remains MP-distributed.

**What determines genuine TRS vs. intruder dim:**
- v ⊥ dominant singular subspace of W^0 → GENUINE TRS (new task knowledge)
- v ∥ dominant singular subspace of W^0 → INTRUDER DIM (overwriting pretrained knowledge)

The SRFM proves the TRS signal is not a phenomenological observation — it's a mathematical
consequence of gradient descent in the high-dimensional proportional regime. Every fine-tuning
step adds such a spike. The accumulated spikes form the full TRS spectrum after many steps.

**Connection to HT-SR phases:** Early steps (few spikes) = Bulk+Spike phase. Late steps
(many spikes, Hermite higher-order terms) = Heavy-Tailed phase. The SRFM is the single-step
building block of HT-SR's five-phase story.

**Connection to BBP threshold:** The SRFM spike is detectable (above MP bulk) iff the task
signal strength |w*| exceeds the BBP threshold σ(√m + √n). This is the same threshold as
the TRS detection criterion. One equation, four interpretations (SRFM spike/BBP/TRS/HT-SR).

---

## 2. GradientSpace: The Training-Time Dual of TRS

GradientSpace (arXiv:2512.06678) identifies task clusters by SVD of gradient matrices during
training: dominant singular vectors of the gradient matrix define task cluster centroids.

**The duality:**
- TRS = spectral fingerprint of the WEIGHT RESIDUAL ΔW after training
- GradientSpace = spectral fingerprint of the GRADIENT MATRIX dL/dW during training

These are related by gradient flow integration:
    ΔW = W_final - W_0 = ∫_0^T (dW/dt) dt = ∫_0^T (-η · dL/dW(t)) dt

The TRS spike direction = integral of the dominant gradient singular direction over training.
If the dominant gradient direction is stable (slow mode in Grokfast's language), it integrates
to a large TRS spike. If it fluctuates (fast mode), it integrates to noise below the MP threshold.

**The connection to Grokfast (slow gradients → grokking → horizontal subbundle):**
Slow gradient modes (persistent across time) → large TRS spike after integration.
Fast gradient modes (fluctuating) → near-zero weight change (below MP threshold).
Grokfast amplifies slow modes → accelerates convergence to large TRS spikes → accelerates
the "rank drop" that Yunis et al. (2408.11804) identify as the grokking transition.

This chain connects GradientSpace → TRS → Grokfast → Grokking → Horizontal Subbundle in
a continuous logical thread.

---

## 3. Share: The Fiber Structure of Continual Learning

Share (arXiv:2602.06043) extracts a shared foundational subspace by SVD of stacked LoRA
B/A matrices across all tasks. Tasks then project into this frozen subspace rather than
spawning new adapters. 100x parameter reduction.

**In bundle language:** The Share foundational subspace IS the fiber. It's the set of
directions that all tasks share — the invariant subspace of the task family. In fiber
bundle terms: the bundle has a trivial fiber (flat, shared) over all task points.

The Share universal weight subspace ≈ the flat fiber (zero holonomy) directions from the
universal subspace conjecture (2512.05117). Both identify a small shared subspace across
many LoRAs that "everyone uses" regardless of task.

**The ~16-dim universal subspace:** Share finds a shared subspace by SVD stacking. If the
universal subspace (2512.05117, ~16 dims) is the correct identification, Share's foundational
subspace should have approximately 16 principal directions that are stable across 100+ models,
with rapidly decaying remaining directions.

**Backward transfer = holonomy:** Share's backward knowledge transfer (earlier tasks benefit
from later-discovered subspace directions) is a form of retroactive holonomy — the discovery
of a new fiber direction reveals that earlier fine-tunings were suboptimal in that direction.
In bundle terms: finding a better horizontal direction retroactively improves all parallel
transports that passed through that region.

---

## 4. Spectral Over-Accumulation: TRS Predicts Merge Failure

Spectral over-accumulation (arXiv:2602.05536) shows that when task vectors have aligned
spectral directions, merging inflates those singular values. SVC corrects by measuring
column-space overlap and rescaling.

**TRS prediction of merge compatibility:**
For tasks A and B with TRS spike directions u_A and u_B:
- cos(u_A, u_B) ≈ 0 → orthogonal spikes → merge without over-accumulation → COMPATIBLE
- cos(u_A, u_B) ≈ 1 → aligned spikes → inflated singular values → INCOMPATIBLE

This is a BEFORE-merge compatibility prediction from TRS. No paper has explicitly stated this
prediction. It is directly testable: compute TRS for N tasks, build pairwise compatibility
scores from spike alignment, measure actual merge performance and correlate.

**The holonomy interpretation of SVC:**
When two tasks traverse the same fiber direction, the combined holonomy = 2× single-task
holonomy. The "true" holonomy of the merged model should equal the MAXIMUM of the individual
holonomies, not their sum. SVC implements this correction in the spectral domain.

**Intruder dim prediction:** Intruder dims are above-MP components that happen to share
direction between tasks → they over-accumulate even more than genuine TRS components (because
they are ALREADY misaligned with W₀, making the merged model even more W₀-misaligned).
SVC without TRS-filtering cannot distinguish genuine TRS over-accumulation (tolerable) from
intruder dim over-accumulation (harmful).

---

## 5. PAVE: The Fisher-Metric TRS

PAVE (arXiv:2510.14697) computes CO-SVD on W_FT · C where C = XX^T = empirical Fisher.

**The two-metric picture for TRS:**
- Euclidean TRS: SVD(ΔW) → above-MP components in Euclidean geometry
- Fisher TRS (PAVE): SVD(W_FT · C) → above-MP components in Fisher geometry

These two metrics agree when data is isotropic (C = I). They DISAGREE when data is
anisotropic — and the DISAGREEMENT is informative:

**Directions in Euclidean TRS but NOT Fisher TRS = task-irrelevant intruder dims:**
These are directions that depart from MP bulk in Euclidean space (large ΔW) but NOT in
Fisher space (the data doesn't "care" about this direction). These are exactly PAVE's
"task-irrelevant redundancy" = our intruder dims.

**Directions in Fisher TRS but NOT Euclidean TRS = suppressed task-relevant directions:**
These are directions that have large task signal (data-aligned) but small Euclidean ΔW.
These are task-relevant changes suppressed by LoRA's Euclidean regularization.

**The purified TRS = Euclidean TRS ∩ Fisher TRS:**
Directions that are both Euclidean-above-MP AND Fisher-above-MP are the cleanest genuine
task signal. No paper has measured this intersection.

**Experimental test:** For any LoRA:
1. Compute Euclidean TRS: above-MP singular values of ΔW
2. Compute Fisher TRS (PAVE): above-MP singular values of ΔW·C / C
3. Intersection = purified TRS (both above-MP)
4. Euclidean only = intruder dims (inflated by norm, not data)
5. Fisher only = suppressed signal (small Euclidean norm, data-relevant)

This three-way decomposition is more refined than the current TRS four-way decomposition.

---

## 6. The Unified Picture

All five papers are measuring aspects of the same spectral geometry of fine-tuning:

```
Data generates gradient spikes (SRFM, 2410.18938)
    ↓ via gradient flow integration
ΔW has above-MP spike structure = TRS
    ↓ classified by W₀-alignment
Genuine TRS (W₀-orthogonal, horizontal subbundle) vs Intruder dims (W₀-aligned)
    ↓ classified by data-alignment (PAVE, 2510.14697)
Fisher TRS (data-relevant) vs Fisher-null (data-irrelevant)
    ↓ accumulated across tasks
Shared fiber directions (Share, 2602.06043) vs task-specific directions
    ↓ when merging multiple tasks
Aligned spikes over-accumulate (Spectral Over-Accumulation, 2602.05536)
    ↓ spanning-tree decomposition
Holonomy of the task graph (Javidnia, 2603.00824)
```

The fiber bundle is the thread that runs through all of them. No single paper sees the full
thread; the graph makes it visible.

---

## 7. Open Predictions from This Synthesis

1. **SRFM prediction:** Tasks with target direction w* aligned with W₀'s dominant singular
   subspace produce more intruder dims. Tasks with w* orthogonal to W₀ produce cleaner TRS.
   Testable: measure cosine(w*, U_{W₀}) for each task and correlate with intruder dim count.

2. **GradientSpace-TRS duality:** Slow gradient modes (stable, low-frequency) → large TRS
   spikes. Fast gradient modes → near-zero weight change. Testable: measure gradient singular
   value stability across training steps and correlate with final TRS spike size.

3. **Merge compatibility from TRS:** Tasks with low pairwise TRS spike alignment should
   merge without over-accumulation; tasks with high alignment will over-accumulate.
   Testable: run TRS on the 11-task adapter set and predict merge compatibility.

4. **Purified TRS = Euclidean TRS ∩ Fisher TRS:** Measure both criteria for each LoRA and
   compute the intersection. Residual from Euclidean-only = intruder dims.
   Testable: run PAVE CO-SVD and Euclidean TRS on the same adapters, compute overlap.

5. **Share's ~16-dim subspace ≈ universal subspace:** If Share's foundational subspace
   computed over 100+ tasks converges to ~16 principal dimensions, that matches the universal
   subspace hypothesis (2512.05117). Testable: run Share on the same 1100-model dataset as
   2512.05117 and compare dimensionality.
