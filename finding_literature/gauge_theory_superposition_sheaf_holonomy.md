---
source_url: https://arxiv.org/abs/2603.00824
captured_at: 2026-05-07
author: Hossein Javidnia (Feb 2026)
contributor: autonomous-loop
---
# A Gauge Theory of Superposition: Toward a Sheaf-Theoretic Atlas of Neural Representations (arXiv:2603.00824)

## Core finding
A sheaf-theoretic atlas of neural representations where each context cluster has a local
semantic chart with a Fisher/Gauss-Newton metric. Three measurable geometric obstructions
to clean representation geometry: (O1) local jamming, (O2) proxy shearing, (O3) nontrivial
holonomy over fundamental cycles in the context graph.

**Theorem 5.1 (Spanning-Tree Gauge Identity):** chord residuals equal the holonomy of their
fundamental cycle. This means: holonomy of a loop = product of pairwise transport matrices
along the spanning tree, computable from pairwise LoRA distances WITHOUT traversing the loop.

## Relevance to GAP 1 (Fisher Degeneracy) — Sheaf as the Correct Framework

The principal fiber bundle W → W/G assumes constant fiber dimension everywhere (uniform
GL_r action). GAP 1 (Fisher degeneracy) occurs because rank(F) varies across W — the
Fisher metric is degenerate at some points (rank < full), making ker(ω) non-uniform.

A **sheaf** over weight space assigns to each point W a local fiber space whose dimension
can vary. The sheaf condition (consistency of overlapping local sections) generalizes the
bundle condition. For weight space:
- At "generic" W where rank(F) = full: fiber = GL_r, bundle structure holds
- At "singular" W where rank(F) < full: fiber = lower-dimensional subgroup, sheaf handles this

**The sheaf-theoretic atlas resolves GAP 1 without Tikhonov regularization.** Instead of
regularizing F to be everywhere full-rank (Defense B, Tikhonov F_ε), we accept that the
fiber dimension varies and use a sheaf. The horizontal subbundle ker(ω) becomes a sheaf
of horizontal subspaces with varying dimension — mathematically honest and more general.

This is preferable to Defense B because:
- Defense B (Tikhonov) makes the algebra work but loses the geometric meaning of ε → 0
- Sheaf theory IS the correct mathematical framework for varying-rank connections
- The paper demonstrates this works computationally in representation space

## Three Geometric Obstructions in Weight Space
Mapping Javidnia's three obstructions to fine-tuning/LoRA context:

**(O1) Local Jamming** = rank(ΔW) > dim(ker(ω)) at the current W₀
Meaning: more LoRA directions than available "bandwidth" in the horizontal subbundle.
LoRA rank r > effective rank of ker(ω) → jamming → some LoRA components must be in
vertical fiber → intruder dims are unavoidable.

**(O2) Proxy Shearing** = geometric mismatch between task LoRAs when merged
Meaning: LoRA_A and LoRA_B are in different charts of the sheaf → their sum (task
arithmetic) involves a cross-chart transport → mismatch energy = Javidnia's D_shear.
Task arithmetic failures = proxy shearing in the sheaf atlas.

**(O3) Nontrivial Holonomy** = our Conjecture 2 (holonomy-intruder correspondence)
Over a loop in task space (multiple sequential fine-tunings returning to base), the
holonomy measures accumulated rotation in the fiber = total intruder dim energy.

## Spanning-Tree Holonomy Algorithm
Theorem 5.1 gives a PRACTICAL ALGORITHM for computing holonomy without explicit loop traversal:

For a set of LoRA checkpoints {ΔW_1, ..., ΔW_T} from sequential fine-tuning:
1. Build a spanning tree on the T checkpoints based on pairwise distances (e.g., Frobenius)
2. For each chord (off-tree edge), compute the chord residual = mismatch between ΔW_i
   transported along the spanning tree path and ΔW_j directly
3. The holonomy of the fundamental cycle (i → ... → j → i) = the chord residual

This means: **holonomy can be computed from pairwise LoRA adapter distances, without
running the actual sequential fine-tuning loop.** This is computationally O(T²) instead
of O(T·training_time).

## Connection to Sevetlidis (2601.21653)
Sevetlidis operates in representation/feature space (input-space loops).
Javidnia also operates in representation/context space.
Both are measuring holonomy in the "wrong" space for our framework (weight space).

But Javidnia's Theorem 5.1 is ARCHITECTURE-INDEPENDENT — the spanning-tree decomposition
works for any connection on any sheaf, including the weight-space connection ω.

If we adapt Theorem 5.1 to weight space:
- Context clusters → task clusters (different fine-tuning tasks)
- Local feature chart → LoRA adapter neighborhood in weight space
- Spanning tree → shortest path in the task similarity graph
- Chord residual → intruder Frobenius energy between LoRA pairs

This gives a weight-space holonomy algorithm from pairwise LoRA distances. The rep-space
↔ weight-space isomorphism is NOT needed — Theorem 5.1 is a general sheaf theorem.

## What this does NOT say
- Paper operates in representation/activation space, not weight space directly
- No LoRA or fine-tuning context — applies to activations/context clusters
- No proof that the weight-space sheaf connection has the same structure as the rep-space one
- Sheaf theory requires working out the formal patching conditions for weight space
