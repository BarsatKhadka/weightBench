# Iteration 26 — 2026-05-09 — Trajectory MDS embedding: same-task = same *region*, not same path

iter_023 / iter_024 / iter_025 established that same-task LoRAs cluster
in subspace space at high σ. iter_026 actually *visualizes* the
trajectories: 9 substep-pool LoRAs × 16 checkpoints = 144 (LoRA, step)
points, pairwise Grassmannian distance computed across 3 representative
layers (q_proj, v_proj, down_proj at L11), then MDS-embedded to 2D and
plotted as 9 paths colored by task.

The picture is more nuanced than the σ numbers suggested.

---

## The plot

`plots/5_trajectory_embedding.png`

Three observations from the visualization:

**1. Tasks occupy distinct *regions*, not points.** mul_mod (orange)
trajectories all end in the upper half (y > 0.35) but at three
visibly different x positions (-0.3, 0.05, 0.35). add_mod (blue) ends
on the right side at three different y positions. max (green) ends on
the left at three different y positions. **Same-task LoRAs cluster in
*neighborhoods*, not at a single point.**

**2. Within a task, paths point in different directions.** Each LoRA
traces a short, smooth path from start to endpoint. Three mul_mod seeds
do *not* walk along the same path; each takes a distinct trajectory
within the upper region. The C1 cluster signal isn't "same-task LoRAs
follow the same geodesic" — it's "same-task LoRAs end up in the same
neighborhood after walking different paths within that neighborhood."

**3. Max trajectories are visibly shorter.** Three green clusters are
small, tightly bunched within each LoRA. Consistent with the "no real
learning" magnitude-plateau finding from iter_025 plot 4 — when the
gradient signal dies, the LoRA stops moving in subspace space too.

## What this changes about plan.md A4

Before iter_026, plan.md's A4 ("path-vs-speed sharpens within the
geodesic frame") was implicitly committed to a strong same-path claim:
same-task LoRAs trace overlapping curves through subspace space, and
the curve coincidence is the signal A4 detects. The MDS embedding
shows this is false at the per-seed level. **Same-task seeds end at
different specific points, reached via different paths, all within
the same regional cluster on the Grassmannian.**

A4's right framing is weaker but still substantive:

- **Cluster geometry is what C1 detects.** Same-task seeds end up
  geographically close (same color region) without walking the same
  path. This is the "task identity = neighborhood, not point" version.
- **Within-cluster spread is informative.** Some clusters are tight
  (max — tiny spread), some loose (mul_mod — spread across upper third).
  This within-cluster spread is what iter_022's "training-dynamics
  signature" finding detected at endpoint, now visible as path geometry.
- **The "geodesic interpolation between two same-task LoRAs" question
  becomes well-posed:** since they're in different points, you can
  actually interpolate. plan.md's A6 (Grassmannian-geodesic
  interpolation) gets a cleaner formulation: two same-task LoRAs are
  *not* the same point, so the interpolation is between two distinct
  points within a shared region — and the question of whether the
  interpolated subspaces also belong to that region is testable.

## Methodological caveats

- **Only 3 probed layers** (L11 q_proj, v_proj, down_proj). Other
  layers might cluster differently. A full 168-layer aggregation
  would be more robust but would make the pairwise computation
  ~50× slower. The 3-layer probe is enough to see qualitative
  structure.
- **MDS lossy.** The 2D embedding preserves distances approximately.
  Distances close in 2D are close in the original; the converse is
  not strictly guaranteed, but within-cluster vs between-cluster
  separation is robust to embedding choice.
- **9 LoRAs is small.** With 5 seeds per task instead of 3, the
  within-region spread would be sampled better. Future runs.

## What iter_027+ should consider

1. **Geodesic interpolation between two same-task endpoints.**
   Now that we know same-task LoRAs are at different points, ask:
   does the linear-interpolated subspace ALSO solve the task? If
   yes, the same-task region is a connected manifold (LoRA-LMC at
   the cluster level). If no, the region has internal barriers.
   Cost: ~2 GPU-hours (a few interpolation points × eval).

2. **Real-task substep + MDS.** Re-run iter_024's real-task pool with
   substep checkpoints, MDS-embed. Same regional structure, or
   different? Tests whether "task = region not point" generalizes
   beyond synthetic.

3. **Within-region structure.** What distinguishes the three mul_mod
   endpoints from each other within their shared region? Is it
   correlated with anything observable (e.g., per-seed grokking step,
   final accuracy)? Could give a "what does within-cluster spread
   encode" answer.

4. **Compare regions across base models.** Train the same task on a
   different base, do the regions occupy similar relative positions
   in the MDS plot? Tests whether the cluster GEOMETRY is shared
   across architectures.

iter_027 priority recommendation: **option 1 (geodesic interpolation).**
This is the cleanest test of whether "same-task region" is a flat
LMC-like neighborhood or a structured manifold with barriers — and
directly informs plan.md's Section 6 mergeability claim, since
mergeability of two same-task LoRAs = does the geodesic between them
preserve task accuracy.

## Catalog state after iter_026

- A11 (iter_020): frames orthogonal at 84°.
- A01+A07 first-cut (iter_021): instrument confound on uncontrolled.
- C1 synthetic (iter_022): pooled-std sep 3.52.
- E2 trajectory (iter_023): T2 3.74 at step 25; T1 distinguishes 3 regimes.
- C1 real-task (iter_024): pooled-std sep ~11; output-vocab refuted.
- iter_025 substep + region: lock-in at step 2; σ peaks at step 14;
  spectral concentration is the genuinely-emergent quantity.
- **iter_026 trajectory embedding:** task identity = *neighborhood* on
  Grassmannian, not point. Same-task seeds walk different paths to
  different endpoints, all within shared regions. plan.md A4 reframed
  from same-path to same-neighborhood; A6 (Grassmannian interpolation)
  gets cleaner formulation.

Seven iters, ~$0 spend, ~3 GPU-hours total. plan.md unchanged.
