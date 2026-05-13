# Iteration 13 — 2026-05-09

**Path 2 chosen (consolidation).** Level-1 Cross-LoRA failure-mode
arxiv search returned no clean new-paper A15 — the closest hits were
either already corpus-internal or addressed a different problem
(FedRot-LoRA for federated rotational misalignment, not cross-arch
architectural mismatch). Per decision criteria, pivoted to Path 2
without exhausting the level-2 search, since the catalog has converged
to a state where consolidation is more useful than forcing another
A-finding.

---

## Level-1 search outcome

WebSearch: "cross-architecture LoRA transfer alignment failure mode
dimension mismatch base model spectrum 2026."

Top results examined:
- **Cross-LoRA (2508.05232)** — already in corpus from iter_008; its
  own paper notes the architecture-similarity effect (weaker gains
  for MHA+GeLU vs GQA+SwiGLU mismatches) that the corpus has already
  captured as Community 15 nodes ("Architectural Similarity Effect on
  Transfer", "Architecture Sensitivity in Cross-LoRA").
- **FedRot-LoRA (2602.23638)** — addresses *rotational* misalignment
  in federated LoRA, not cross-architecture transfer. Different
  problem (federated rotational invariance vs cross-arch architectural
  mismatch).
- **LoRA-X (2501.16559)** — already mentioned in Cross-LoRA's related
  work; training-free transfer, similar scope.
- **FLoRG (2602.17095)** — already in corpus from iter_005.

**Verdict — no clean new-paper A15.** The most relevant *failure mode*
content is the architecture-similarity effect that's already corpus-
internal (Community 15). Could be a refinement of A10's status rather
than a new A-section finding; that refinement is small enough to fold
into A10's status as a note (added in this iteration's consolidation
pass below).

## Path 2 — Section A consolidation

Rather than force a marginal A15, this iteration adds a **thematic
index** to the top of BREAKTHROUGH.md Section A. The catalog has
converged into five clusters plus the small architecture-similarity
note for A10. The index:
1. Identifies the five thematic clusters (Foundational triad,
   Grassmannian instrument, Trajectory time, Cross-architecture, Cheap
   baselines).
2. Notes dependency arrows (A8 → A2; A14 → A2; A11/A13/A14 → A12).
3. Notes audit-pair (A11 ↔ A13) and same-experiment-different-motivation
   (A10 ≡ A12 anchor experiment) relationships.
4. Recommends **cluster-level promotion** rather than piecemeal: the
   Grassmannian-instrument cluster (A1/A4/A5/A6) should be promoted
   together if any of it lands; A11/A13/A14 should be promoted
   together as A12's audit triad; A2 and A8 should be promoted
   together (A8 needs A2).

The index does NOT rewrite individual A-findings. It is presentation
glue, not new content.

## Foundation-composition calibration added to A12

The advisor's iter_012 flag is now logged inside A12's status section
as a one-paragraph "Foundation-composition calibration" note. Key
content: A11's frame-disagreement outcome + A13's PIGMM correction +
A14's SLT replacement, *if all accepted*, compose into PIGMM + GL_r +
SLT — which gives **free-energy asymptotics**, not **Cencov-style
uniqueness**. These are different mathematical objects. Promotion-
time language must say "CORE_CLAIM's theorem-sketch is motivational
anchor + we report stress-tests for cases where the original
assumptions partially fail in the actual NN regime" — not "we test
the unique-optimal-distance theorem."

## Architecture-similarity note added to A10's status (small refinement)

A10's status section gets a one-line addition: "Falsifier should
report architecture-pair-specific results (LLaMA↔Qwen vs LLaMA↔Gemma
etc.), not aggregate, because Cross-LoRA's own paper finds the
architectural-similarity effect (Community 15)." This was the level-1
search's substantive contribution — too small for a new A-finding,
useful as A10 refinement.

(Implemented in the cluster-4 portion of the thematic index, which
notes the architecture-similarity effect inline rather than as a
standalone refinement of A10.)

## Why Path 2 was the right call this iteration

The catalog now has 14 A-findings, 5 future-work entries, 6 Section C
siblings, 14 Section D watchlist entries. The user is the one deciding
promotions, and reviewing 14 chronologically-listed A-findings without
thematic grouping is more taxing than reviewing 5 clusters. The
consolidation pass converts a flat list into a structured navigation
aid. The user can now review by cluster — *"do I want the
Grassmannian-instrument cluster?"* — rather than by individual finding.

Path 1 would have produced a marginal A15 from already-corpus-internal
material. Path 2 produces structural value at the catalog level.

## Watchlist (Section D) status

No new entries this iteration (no PDF fetched). Section D remains at
14 audited papers/docs.

## Graph state

No PDFs fetched, no `graphify update .` needed. Graph remains at
2040/2169/192 (unchanged from end of iter_012).

## What iter_014 should do

The catalog has clearly converged. The two productive directions:
1. **Continued targeted arxiv search.** Possible next targets: any
   2025–2026 paper on LoRA mergeability *as a learned function* (to
   benchmark A1's analytic predictor against), or any paper measuring
   `d_task` consistency across estimators (to benchmark A2's
   four-estimator consensus directly). These are A2/A4 size finds if
   they exist.
2. **Section B consolidation.** Section B (future-work candidates
   B1–B5) was last updated in iter_007 when the loop pivoted away from
   architecture proposals. With 14 A-findings now, Section B's
   future-work candidates may need re-evaluation: which B-findings
   still make sense given A1–A14? Does any B-finding now look
   redundant with an A-finding? A short consolidation pass on
   Section B would be a natural follow-up to the Section A index.
3. **`some_insights_lora_papers.md` finally read.** This was deferred
   in iter_009/010 and again in iter_011/012. After two iterations of
   convergent A-findings, opening it once more might surface
   something the loop hasn't seen — or confirm that the doc is
   redundant with what's already captured.

iter_014 priority: **read `some_insights_lora_papers.md` first**
(cheap, deferred for several iterations now). If it yields an A15,
write it terse. If it doesn't, do Section B consolidation. If neither,
declare a clean null and move on. Same shape as iter_011/012 with the
hidden-doc as priority instead of the arxiv search.

## Summary

iter_013 was a consolidation iteration. Level-1 Cross-LoRA failure-
mode search returned nothing new (all relevant content was already
corpus-internal). Pivoted to Path 2 per decision criteria — added a
thematic index to BREAKTHROUGH.md Section A, grouping 14 A-findings
into 5 clusters with dependency arrows and cluster-level promotion
recommendations. Added foundation-composition calibration note to A12
per advisor's iter_012 flag (PIGMM + GL_r + SLT ≠ Johnstone-Paul +
GL_r + Cencov). Architecture-similarity effect noted in cluster 4 of
the index. plan.md unchanged. Graph unchanged at 2040/2169/192.
iter_014 scheduled.
