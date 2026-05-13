# Iteration 14 — 2026-05-09

**Outcome (b) — partially useful.** `some_insights_lora_papers.md`
(deferred 6× across iter_009–013) is a methodological-refinement doc.
Not redundant with A1–A14, but not A15-shaped either. The refinements
are setup-level tweaks for plan.md's E1, not new geometric or
theoretical findings. Folded as a cluster-2 methodological-refinement
note in BREAKTHROUGH.md's thematic index.

---

## What the doc actually contains

Six tightly-scoped insights drawn from three corpus papers:

- **AsymmetryOfLoRA** (Hayou): B matrices cluster by task, A matrices
  don't (when init is fixed). → use B-only as weight-space coordinate
  for plan.md's controlled population.
- **AdaLoRA** (Zhang et al.): FFN layers carry more task-specific
  adaptation than attention; top layers carry more than bottom. →
  layer-grouped representation (bottom/mid/top) sharpens task
  clustering. Add `up_proj/down_proj` to target modules.
- **SymmetriesInWSL** (Schurholt et al.): distance metric must match
  prediction target. Zero-order features (task identity) are GL_r-
  invariant; sensitivity/Hessian features are only O(r)-invariant;
  coordinate-specific features have no symmetry. → three-metric
  ablation (raw Euclidean / GL_r-invariant / O(r)-invariant) in
  Methods section. plan.md's Method already commits to GL_r via π;
  the ablation *demonstrates* the choice empirically.
- **Effective rank as covariate.** AdaLoRA shows nominal rank ≠
  effective rank. → control for effective rank in mergeability /
  forgetting predictions; matters for A1's analytic mergeability.
- **B-only + singular value spectrum is the canonical Experiment 1
  representation.** Cross-paper synthesis of the above three.
- **Concrete Experiment 1 changes table** with five before/after rows.

## Why outcome (b), not (a) or (c)

**Not (a) — clean A15.** None of the insights is sized like A1–A14.
They are *experimental-setup refinements* for E1, not new geometric
instruments or theoretical findings. Adding them as A15 would inflate
the catalog with sub-finding-level material.

**Not (c) — redundant.** The insights are *not* explicit in A1–A14.
The Grassmannian-instrument cluster (A1+A4+A5+A6) presupposes a
weight-space coordinate; the doc says "use B-only when A is fixed-init,"
which sharpens *how* the coordinate gets computed. A1's mergeability
formula is well-defined under either ΔW = BA or B-only readings of
Region 2; the doc says B-only is cleaner under fixed A init. This
isn't redundant — it's a refinement layer A1–A14 don't make explicit.

**(b) is right.** Folded as a cluster-2 methodological-refinement note
in the thematic index. Four refinements named: B-only coordinate,
three-metric ablation, effective-rank covariate, layer-grouping.
Section D updated with the doc-read entry and an honest note that
six deferrals were a small mistake (the loss is small because these
are setup tweaks, not depth moves).

## Six deferrals weren't catastrophic

The doc was deferred from iter_009 onward, in part because the loop
was producing strong A-findings from other hidden docs (CORE_CLAIM,
the experiment-design doc) and continuing those reads paid better
than this one would have. The cost of the delay: the methodological
refinements weren't available when E1's Methods setup was first
discussed in early iterations. The loss is small — those discussions
are still in BREAKTHROUGH.md as candidates, not in plan.md, and the
refinements can be incorporated when (if) the user promotes any
cluster-2 finding into plan.md.

## Pacing — small iteration, honest

iter_014 was deliberately small: one Read, one fold-in, one Section D
update. No new A-finding, no PDF fetch, no graph update. Per advisor's
explicit null permission, this is a clean small iteration shape.

## Watchlist (Section D) updated

Entry added for `some_insights_lora_papers.md`. Doc is now read; six
deferrals settled.

## Graph state

No PDFs fetched; no `graphify update .` needed. Graph remains at
**2040 nodes / 2169 edges / 192 communities** (unchanged from end of
iter_012; iter_013 didn't fetch either).

## What iter_015 should do

Three productive directions, in order of expected yield:

1. **Continued targeted arxiv search** for any 2026 paper on LoRA
   *mergeability as a learned predictor* — to give A1's analytic
   formula a concrete benchmark. If a paper exists that trains a
   mergeability regressor on adapter pairs, A1's `Σ sin²(θ_i)` should
   be benchmarked against it, and the result becomes a refinement
   note for A1.
2. **Section B mini-refresh.** With A1–A14 in catalog and A12+A14
   characterizing the gauge structure deeply, B1 (GE-LoRA-Hyper-CL)
   is now over-specified by Section A: A12's uniqueness theorem-sketch
   plus A14's SLT framework give the gauge-equivariant generator's
   theoretical underpinning that B1 was reaching for. Worth one
   paragraph noting B1 is now A-section-supported as future-work
   rather than freestanding. Other B-findings (B2–B5) less affected.
3. **`BIG_IDEAS.md` opened with a specific thread to follow.** This
   has been deferred since iter_009 with the rationale "god-node
   risks sprawl." After 14 A-findings, the loop now has specific
   threads to follow when reading it: e.g., does BIG_IDEAS.md propose
   any application that A1–A14's measurement instruments now make
   testable? If yes, that's an A-section finding via the
   instrument→application connection. If no, BIG_IDEAS.md is
   redundant with the syntheses already absorbed.

iter_015 priority: **(1) targeted arxiv on mergeability regressors**;
fall back to (2) Section B mini-refresh if (1) returns nothing; fall
back to (3) BIG_IDEAS.md opened with the application-from-instrument
thread if (2) doesn't yield substantive content. Same shape as iter_011
arxiv-first ordering. Explicit null permission preserved.

## Summary

iter_014 settled the 6×-deferred `some_insights_lora_papers.md`. Outcome
(b) — partially useful, four E1-setup methodological refinements folded
into the cluster-2 note of the thematic index. plan.md unchanged.
BREAKTHROUGH.md updated with the cluster-2 refinement note and Section
D entry. Graph unchanged at 2040/2169/192. iter_015 scheduled with a
mergeability-regressor arxiv search as priority.
