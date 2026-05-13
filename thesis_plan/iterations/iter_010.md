# Iteration 10 — 2026-05-09

**Discipline held:** scientist phase, no code, no pseudocode, no plan.md
edits, no AskUserQuestion about plan.md, no arxiv fetch (no fallback
needed). Same shape as iter_009: one existing-doc read, one A-section
addition, one prior-finding calibration.

---

## What was read this iteration

**`finding_literature/CORE_CLAIM.md` (154 lines, never opened before).**
Read directly per iter_009's advisor priority. The doc bills itself as
"THE CORE CLAIM — The One Unbreakable Idea, written: May 2026 — after
stripping all conjectures." It is the project's strongest single
mathematical statement.

The doc structure: a single headline theorem, three classical
foundations (Johnstone-Paul 2001/2007 spiked covariance + GL_r
invariance + Cencov 1982), a unified-claim sketch, an anchor experiment
(10+10 cross-arch LoRAs), and a labeled "Conjectures for Future Work"
section listing what is *not* part of the unbreakable core.

## Why CORE_CLAIM is decisive (outcome (a) per the priority spec)

CORE_CLAIM is exactly outcome (a): the project's actual headline
mathematical claim, with classical pre-2024 foundations. Reading it
forced one of the strongest A-section findings the loop has surfaced.
The claim is uniqueness: under spiked-covariance + GL_r + Cencov, the
Grassmannian geodesic distance under Fisher-Rao metric is the *unique*
statistically-optimal reparametrization-invariant task distance, and
TRS (above-MP singular subspace) is the min-MSE estimator of the task
signal.

Critically, this is a *uniqueness theorem*, not just a methodological
preference. Any GL_r-invariant + statistically-optimal task distance
*must* reduce to Grassmannian distance on TRS subspaces. The corollary
is sharper: any method ignoring TRS or using a non-Grassmannian
distance is provably suboptimal under the assumptions.

## A12 added — the structural significance for A1–A11

A1, A4, A5, A6, A10 are now not heuristic depth moves; under
CORE_CLAIM's three-foundation theorem they are the *unique forced
answers* to "how do you measure things in this setting":
- A1's `Σ sin²(θ_i)` mergeability formula is the squared Grassmannian
  distance (Foundation 3's unique invariant metric).
- A4's matched-arclength tangent overlap inherits the differential
  structure from Foundation 2 + 3.
- A5's Karcher mean under Fisher-Rao IS the unique invariant centroid
  by Cencov; the Euclidean mean is provably suboptimal.
- A6's geodesic restatement of LoRA-LMC uses Foundation 3's Fisher-Rao
  geodesic — the only correct curve.
- A10's Cross-LoRA `ρ_AB` aligns Region 2 subspaces; under CORE_CLAIM,
  the post-`ρ` comparison is on the same Grassmannian and inherits the
  unique-distance result.

**This sharpens plan.md's intellectual positioning** from "empirical
exploration of LoRA trajectory geometry" to "empirical test of a
uniqueness theorem with classical statistical foundations." The
empirical paper retains its empirical character (no theoretical proof
of LoRA-LMC), but the measurement instruments inherit Cencov's
uniqueness as theoretical justification.

## A12 ↔ A11 chain

A11 is precisely the test of whether CORE_CLAIM's spiked-model
assumption applies in practice (the A11 experiment doc explicitly
references CORE_CLAIM at L330: "If U_W₀ ≈ U_S* (aligned),
CORE_CLAIM.md's Grassmannian framework is valid"). The chain:

1. **A12 (foundational theorem):** under spiked covariance + GL_r +
   Cencov, the Grassmannian framework is unique-optimal.
2. **A11 (applicability check):** measure U_W₀ vs U_S* angles to
   verify the spiked-covariance frame is valid for LoRA in practice.
3. **A1–A10 (forced consequences):** if A11 passes, A1–A10 are not
   methodological choices but unique-invariant-instrument readings.
4. **plan.md sections 4–6 (empirical claims):** test whether the
   actual data lands the predictions A1–A10 make.

This is a clean dependency tree. CORE_CLAIM is the root; A11 conditions
applicability; A1–A10 are the operational instruments; plan.md's
experiments are the empirical readings. iter_010 makes all four
levels explicit for the first time.

## Anchor experiment overlap with A10

CORE_CLAIM's "anchor experiment" (10 same-task LoRAs across LLaMA/Mistral
+ 10 diff-task pairs, compute `d_G`, predict same-task ≪ diff-task) is
**the same experiment as A10's falsifier under a different motivation.**
A10 derives the cross-arch test from Synthesis 18 + Cross-LoRA;
CORE_CLAIM derives it from the three foundations. Either reading
produces the same falsification protocol. Passing the experiment
validates A10's empirical cross-arch claim AND CORE_CLAIM's
unique-distance theorem in one shot. Cost ~5 GPU-hours of stretch
training (Mistral-side adapters; LLaMA side already in plan.md's
planned 200-LoRA population) plus zero SVD compute.

## Backup task: A11 connection-prose calibrated

Per iter_009 advisor flag, A11's "Connections to A1–A10" bullet list
slightly overclaimed — implying A1, A2, A5 would be undefined or
needing two Grassmannians under frame disagreement. iter_010 rewrote
the bullets:
- A1 mergeability is well-defined per frame; the formula picks which
  frame predicts merge accuracy better.
- A2's `t*` consensus degrades from 4-of-4 to 3-of-4 (TwoNN and RLCT
  are frame-independent), it doesn't become undefined.
- A5's Karcher mean is on the *same* `G(d_task, m)` regardless of
  frame; only the centroid identity is frame-conditional.
- A10's Cross-LoRA truncated-SVD aligns the W₀-frame; outcome (3)
  (U_S* ⊂ W₀_bottom) requires a 1-line change to bottom-r truncation.

The metric structure is preserved across frames; only the
identity-of-Region-2 changes. This is the more accurate reading.

## Watchlist (Section D) updated

Added `CORE_CLAIM.md` as a corpus-internal load-bearing document
referenced by A11's experiment doc and by plan.md's project memory.
Status: read in iter_010, A12 produced.

## Graph state

No PDFs fetched; graph unchanged at 1989 nodes / 2122 edges / 179
communities. Two corpus markdowns read directly across iter_009 and
iter_010 (`experiment_design_reference_frame_measurement.md`,
`CORE_CLAIM.md`); both already in graph as nodes.

## Pattern observations

iter_009 + iter_010 demonstrate a robust pattern: the corpus contains
load-bearing markdown documents that are graph nodes but were never
opened. When opened, they yield A-section findings without arxiv work.
The mechanism is the same across both iterations:
1. A graph query surfaces an existing corpus doc.
2. The doc is "design only" or "load-bearing claim" but not promoted
   to plan.md.
3. Reading it directly converts the corpus's hidden structure into an
   A-section finding for BREAKTHROUGH.md.

This pattern has yielded A11 (foundational pre-flight) and A12
(uniqueness theorem). Both are stronger than the average arxiv-derived
A-section finding because they were already corpus-grounded and
peer-reviewed (by the project's prior author/iteration) before this
loop touched them.

## What iter_011 should do

The hidden-doc pattern still has runway. Remaining candidates:
- **`some_insights_lora_papers.md`** — partially surfaced in iter_008
  Territory 2 query; lower expected value because of the partial
  visibility.
- **`BIG_IDEAS.md`** — god-node status; risks sprawl unless the loop
  picks one specific thread to follow rather than try to extract
  everything.

If the hidden-doc pattern is exhausted, iter_011 should resume
arxiv-side exploration, ideally targeted at A12's three foundations
(any 2026 paper that strengthens or refines Johnstone-Paul's spiked
covariance, GL_r invariance, or Cencov's theorem in the LoRA setting?).

Specifically worth considering: does any 2025-2026 paper extend
Johnstone-Paul's spiked covariance result to the *non-Gaussian* noise
case relevant to neural-network weights? CORE_CLAIM honestly flags
that "B-matrices of real LoRAs have approximately Gaussian noise
(reasonable: by RMT universality, the noise distribution converges to
the same MP limit regardless of exact distribution for large
matrices)" — but the universality claim itself is testable, and a
recent paper might give a sharper quantitative bound. This would
strengthen A12's theoretical foundations.

## Summary

iter_010 produced **A12 — the strongest A-section finding the loop has
surfaced**. CORE_CLAIM.md gives plan.md a uniqueness theorem with
classical pre-2024 foundations as theoretical anchor, and reframes
A1–A10 from heuristic depth moves to forced consequences of the
theorem. A11's pre-flight check is now explicitly the test of the
theorem's applicability. plan.md unchanged. BREAKTHROUGH.md updated.
iter_011 scheduled.
