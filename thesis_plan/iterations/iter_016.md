# Iteration 16 — 2026-05-09

**Path 1 landed** (cross-base-mergeability arxiv search). Level-1
returned Cui et al. **"Transport and Merge: Cross-Architecture
Merging for Large Language Models" (arxiv 2602.05495, Feb 2026)**,
which combines with corpus-internal Synthesis 26 to surface a clean
A16 at A2/A4 size. BIG_IDEAS.md fallback not invoked. A15 prose
calibration applied per advisor flag from iter_015.

---

## Why Transport-and-Merge is the right A16 source

Cui et al. propose cross-architecture LLM merging via **activation-
space optimal transport** — entropically-regularized Sinkhorn on a
correlation-based cost matrix between source and target activations,
then lift activation correspondences to weight-space neuron mixing.
This is a *different paradigm* than Cross-LoRA (A10's source):

| | Cross-LoRA (A10) | Transport-and-Merge (A16) |
|---|---|---|
| Alignment domain | weight-space (base-weight bases) | activation-space |
| Method | rank-truncated SVD + Frobenius-optimal linear `ρ_AB` | OT (Sinkhorn) on correlation matrix |
| Theoretical anchor | LoRA's GL_r quotient | Platonic Representation Hypothesis |
| Lifts to weight-space? | already there | yes, via activation→neuron correspondence |

Both end at cross-base weight-space fusion through different routes.
This isn't a competitor to Cross-LoRA — it's a *paradigm split*.

## The cross-paper synthesis (the genuine A16 content)

Reading Cui et al. alongside corpus-internal Synthesis 26 (Platonic
Region 1 + Aristotelian Region 2) yields a prediction neither paper
alone makes:

- **Region 1 (universal fiber) is Platonic** — metric convergence
  across architectures (Huh et al. 2024 Platonic Representation
  Hypothesis, which Transport-and-Merge cites). Activation-space
  alignment via OT works for Region 1 because activations share a
  cross-architecture metric.
- **Region 2 (task-specific signal) is Aristotelian** — topological/
  local, curved, *not* metric-convergent across architectures.
  Activation-space alignment cannot work for Region 2 because the
  activations don't share a common metric there.
- **A1's mergeability instrument operates on Region 2.** Therefore
  weight-space alignment (Cross-LoRA's `ρ_AB`) is the *theoretically
  forced* choice for A1, not activation-space alignment.

This is a genuinely-new structural claim. It explains *why* Cross-LoRA
works better than Transport-and-Merge for the cross-arch *task-specific*
mergeability case, and why Transport-and-Merge may work better than
Cross-LoRA for the *universal-fiber* / general-knowledge transfer case.
The two paradigms are complementary, partitioned by the Platonic /
Aristotelian split of the three-region decomposition.

## A16 falsifier (compound, A2/A4-sized)

On 4 plan.md tasks × 2 base models, compute post-merge accuracy under
three alignment paradigms (Cross-LoRA / Transport-and-Merge /
identity), then regress A1's `Σ sin²(θ_i)` against accuracy under
each. Predicted ordering: Cross-LoRA > Transport-and-Merge >
identity. If predicted ordering holds, A16 confirms Synthesis 26
empirically at the cross-arch alignment level. If Transport-and-Merge
wins, Region 2 has more Platonic character than Synthesis 26 claims.
Cost: ~5 GPU-hours stretch (already in A10's budget).

## A15 prose calibration applied (one sentence per advisor)

Updated A15's "local-trait factorization" bullet to clarify that
Rahamim averages over *random partners across tasks*, so A1's mean
factorization yields the **population** Karcher centroid, not the
**task** centroid (A5's quantity). F2 (the falsifier) tests the
right thing regardless: it regresses A1's per-LoRA mean against A5's
task-centroid distance, and if F2 lands, the population-vs-task
centroid relationship correlates strongly enough that the
factorization still picks up A5's signal. One-sentence calibration
inserted; A15 not rewritten.

## BIG_IDEAS.md fallback NOT invoked

Path 1 produced a clean A16, so the deferred BIG_IDEAS.md read with
the application-from-instrument-cluster thread was not needed this
iteration. BIG_IDEAS.md remains queued for a later iteration if the
loop hits a clean null and wants a god-node read with a specific
thread.

## Section C — paradigm-split note added inline

Section C's six-paper W/G-quotient table is about *gauge fixes* /
quotient constructions. Transport-and-Merge is not a gauge fix; it's
a different *paradigm* (activation-space alignment). Did NOT add
Transport-and-Merge to Section C's table because it would muddy
the table's coherent theme. Instead, added Transport-and-Merge to
Section D with the methodology summary and noted the paradigm-split
implication for A16.

## Watchlist (Section D) updated

Added Cui et al. (2602.05495) with the activation-space-OT methodology
summary and A16 connection.

## Graph state

`graphify update .` ran post-fetch. Graph: **2087 nodes / 2212 edges /
196 communities** (was 2074/2200/193). Cui et al. added 13 nodes, 12
edges, 3 communities — the OT machinery (Sinkhorn iterations,
entropic regularization, correlation cost matrix) is graph-novel.

## A2/A4-size discipline held

A16 is short bullets + comparison table + single-paragraph claim +
single-paragraph falsifier. Did not inflate to A12-size despite
having a genuinely-new structural claim. The cross-paper synthesis
(Cui + Synthesis 26) is captured in two short paragraphs, not a
multi-section treatise.

## Loop trajectory

iter_011 (A13) → iter_012 (A14) → iter_013 (consolidation) → iter_014
(small fold-in) → iter_015 (A15) → iter_016 (A16). The pattern is
holding: substantive findings cluster around 2-3 iterations apart,
with consolidations and fold-ins in between. The catalog is at 16
A-findings now. Cluster-2 (Grassmannian-instrument) is becoming
notably dense, with A1, A4, A5, A6, A15 (A1↔A5 unifier), A16
(paradigm-choice for cross-arch).

## What iter_017 should do

Three productive directions:
1. **Continued targeted arxiv** with a new query angle. The
   alignment-paradigm split surfaced in A16 raises a question:
   for Region 1 transfer (Platonic, universal fiber), does any
   2025–2026 paper directly test activation-space vs weight-space
   alignment? If yes, A17 = "Region 1 alignment is genuinely
   activation-space-better; complement to A16's Region 2 result."
2. **BIG_IDEAS.md finally read** with the
   application-from-instrument-cluster thread (deferred 7×). After
   16 A-findings the loop has enough specific applications to query
   against (A11 anchor experiment as standalone tool, A14 SLT-LLC
   as deployable diagnostic, A8 anti-grokking detector as runtime
   indicator). Worth one focused read pass.
3. **Section A consolidation update.** With A15 + A16 added since
   iter_013's index, the cluster-2 Grassmannian-instrument cluster
   has new sub-bullets (A1↔A5 unifier from A15; paradigm-choice from
   A16). Index could be touched up to reflect.

iter_017 priority: **(1) Region-1 alignment paradigm arxiv first**
(continues A16's structural-search payoff); fallback (2) BIG_IDEAS.md
with the thread; (3) Section A index touch-up if (1) and (2) yield
nothing substantive. Same null-permission discipline.

## Summary

iter_016 produced **A16 — alignment-paradigm split** (weight-space
Cross-LoRA for Region 2, activation-space Transport-and-Merge for
Region 1) by combining Cui et al. (2602.05495, fetched) with corpus-
internal Synthesis 26. Genuine cross-paper synthesis. **A15 prose
calibration applied** per advisor flag (population vs task centroid).
Section D updated with Transport-and-Merge entry. Graph: 2087/2212/
196. plan.md unchanged. iter_017 scheduled with Region-1-paradigm
arxiv as priority.
