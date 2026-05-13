# Iteration 15 — 2026-05-09

**Path 1 landed.** Targeted level-1 arxiv search returned **Rahamim et
al. "Will it Merge? On The Causes of Model Mergeability"
(arxiv 2601.06672, Jan 2026)** — a direct empirical benchmark for A1's
analytic mergeability formula. A15 added to BREAKTHROUGH.md Section A
at A2/A4 size. Fallbacks (Section B refresh, BIG_IDEAS.md) not needed
this iteration.

---

## Why this paper is the right A15

Rahamim et al. operationalize a concrete *mergeability score* —
post-merge accuracy averaged over random other-update partners — and
investigate what predicts it. They test:
- Base-model task knowledge (`Δ_base = p_max - p_correct`): **r = 0.892
  on PopQA, 0.845 on Lots-of-LoRAs**.
- Weight properties (`‖W‖`, `σ_max`, perplexity, context length): all
  weak (≤ 0.21).
- Domain knowledge: not as strong as task-specific knowledge.

**They did NOT test principal angles between Region 2 subspaces.**
That's the gap A1 fills. A1 thus has the geometric-instrument lane
uncontested in the corpus's strongest mergeability paper — A1 just
needs to beat or tie `Δ_base = 0.892` to justify the analytic-mergeability
framing for plan.md Section 6.

## Two empirical implications for A1 (free)

1. **Direct benchmark.** A1's `Σ sin²(θ_i)` formula must achieve
   Pearson r ≥ 0.85 against post-merge accuracy on Rahamim's PopQA
   data to be competitive with `Δ_base`; r ≥ 0.92 to beat it; r ≤ 0.5
   to be falsified.
2. **Local-trait factorization (free unifier with A5).** Rahamim et
   al.'s strongest qualitative finding: *"mergeability is a LOCAL
   trait of the model update"* — a highly-mergeable LoRA stays
   mergeable regardless of partner. This algebraically *predicts*
   that A1's pair formula has a per-LoRA factorization: the mean of
   `Σ sin²(θ_i)(L_i, L_j)` over partners `j` is approximately L_i's
   *Karcher-distance-to-task-centroid* (A5's centroid object).
   If F2 (per-LoRA factorization Pearson r ≥ 0.8) lands, A1 and A5
   unify at the per-LoRA level — they become two readings of the
   same geometric quantity (pair-distance vs. mean-distance-to-Karcher).

The local-trait factorization claim is *new content* that A1's
original write-up (iter_003) did not surface. Rahamim's empirical
finding *predicts* it as a consequence of A1's mathematical form
combined with A5's centroid story.

## Cluster-2 thematic-index update

The thematic index for cluster 2 (Grassmannian-instrument) gets a new
sub-bullet noting the A1↔A5 unifier predicted by A15. If F2 lands,
cluster 2 contains *one* per-LoRA scalar (Karcher distance, A5) plus
*one* pair instrument (principal-angle sum, A1) reading the same
geometric object. The cluster's internal coherence sharpens.

## Cost

A15's empirical falsifier costs ~$0 — Rahamim's PopQA + Lots-of-LoRAs
datasets are public and their adapter pool is open. plan.md's
existing cluster-2 SVD pipeline runs A1 + A5 on Rahamim's data
without any new training. Falsifier (F1 + F2) is therefore the
cheapest experiment in the entire catalog after A11.

## A2/A4-size discipline held

A15 is short bullets, two falsifiers (F1 = direct benchmark; F2 =
factorization), zero new compute. The conceptual surprise (A1↔A5
unifier prediction from a behavioral mergeability paper) is captured
in the thematic-index sub-bullet rather than expanded into A12-style
prose.

## Watchlist (Section D) updated

Added Rahamim et al. (2601.06672) to BREAKTHROUGH.md Section D with
the methodology summary and the A1-uncontested-lane note.

## Graph state

`graphify update .` ran post-fetch. Graph: **2074 nodes / 2200 edges /
193 communities** (was 2040/2169/192). Rahamim et al. added 34 nodes,
31 edges, 1 community — the mergeability-score apparatus and PopQA
+ Lots-of-LoRAs benchmark machinery extended the corpus measurably.

## Pacing / loop trajectory

iter_015 returns the loop to substantive A-finding production after
iter_013 (consolidation) and iter_014 (small fold-in). The pattern
the advisor noted is holding: substantive → substantive →
consolidation → small → substantive. iter_016 is positioned to either
continue or hit another small/null result.

## What iter_016 should do

A15 surfaced two new threads worth pursuing:
1. **Other behavioral predictors of mergeability** that aren't in
   Rahamim et al. — could inform A1's benchmark setup further. But
   diminishing returns on yet another mergeability paper; A15's
   benchmark is concrete enough.
2. **Mergeability of *cross-base* adapter pairs** (e.g., LLaMA-LoRA
   merged with Qwen-LoRA). A10 names Cross-LoRA's `ρ_AB` for cross-
   arch alignment but doesn't directly address mergeability after
   `ρ`. A15 + A10 compose: predict cross-base mergeability from
   `Σ sin²(θ_i)` between *post-ρ* Region 2 subspaces. If a paper
   exists testing this, A16 candidate.

iter_016 priority: targeted arxiv on **cross-base-model adapter
merging / mergeability** to close the A10 ↔ A15 gap. Fallback: open
**`BIG_IDEAS.md`** at long last with the specific thread: "does any
application named in BIG_IDEAS.md become testable from the
A1+A5+A10+A15 instrument cluster?" Same null permission as iter_014.

## Summary

iter_015 produced **A15 — Rahamim et al.'s mergeability paper provides
a concrete benchmark for A1 and predicts an A1↔A5 unifier at per-LoRA
level**. Direct fetch + read; A2/A4 size; ~$0 cost on public data;
cluster-2 thematic index updated with the unifier sub-bullet. plan.md
unchanged. Graph: 2074/2200/193. iter_016 scheduled with cross-base-
mergeability arxiv search as priority.
