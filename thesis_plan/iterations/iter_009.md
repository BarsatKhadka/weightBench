# Iteration 9 — 2026-05-09

**Discipline held:** scientist phase, no code, no pseudocode, no plan.md
edits, no AskUserQuestion about plan.md. Tighter than iter_008 — one
existing-doc read, one A-section addition, one A10 caveat. No PDF fetch
needed; no new graphify update needed.

---

## What was read this iteration

**`finding_literature/experiment_design_reference_frame_measurement.md`
(342 lines, read directly).** This is a pre-existing experiment design
in the corpus that the loop had never opened, despite it appearing in
*both* of iter_008's territory queries. iter_008 flagged it for first
read this turn; the choice paid off.

**Outcome (a) per the priority spec.** The experiment doc already
proposes what an A11 would propose. iter_009 does NOT need to invent a
new finding — it surfaces the existing one with the geodesic / Karcher /
Cross-LoRA framing from A1–A10 and locates it as the foundational
pre-flight check.

## What the experiment doc actually proposes

A single, very cheap discriminating measurement: compute principal
angles between

- **U_W₀** — top-k left singular vectors of LLaMA-3-8B's pretrained
  weight matrix.
- **U_S\*** — top-k eigenvectors of the cross-LoRA second-moment
  operator `S = (1/K) Σ_i ΔW_i ΔW_i^T` over K = 11 named LLaMA-3-8B
  LoRA adapters (HuggingFace IDs resolved in the doc).

The doc enumerates four named outcomes, each with publication-ready
interpretation: angles ≈ 0° (frames same — unifies two literatures),
angles ≈ 90° (frames orthogonal — exposes confound), U_S* ⊂ U_W₀_bottom
(MiLoRA correct), U_S* ⊂ U_W₀_top (PiSSA correct). Cost: ~30 min CPU,
~$0. Status in the doc itself: "design only — NOT YET RUN."

## Why this is the foundational A-section finding

Every A1–A10 claim implicitly assumes a single well-defined "Region 2"
on `G(d_task, m)`. But the corpus's TRS three-region story is read
relative to *two* reference frames the corpus has never directly
compared: U_W₀ (pretrained spectrum) and U_S* (cross-LoRA covariance).
Synthesis 23 ("Task Second-Moment Operator S") reads the three regions
from S; Shuttleworth's "intruder dim" criterion reads them from W₀.
These have been treated as the same subspace throughout the project's
syntheses, but the principal angles `θ_j(U_W₀, U_S*)` have never been
measured.

If the angles are small, the conflation is harmless and A1–A10 land
cleanly. If the angles are large, A1–A10 must specify which frame they
operate in, and the answers may differ between frames. Either reading
is publishable; the experiment doc already enumerates the four
interpretation paths.

The cost is extraordinarily low: ~$0 and ~30 min on CPU. This is the
cheapest experiment in the entire thesis_plan and it conditions every
other claim. Running it is the structural-pre-flight equivalent of a
sanity check.

## A11 added to BREAKTHROUGH.md Section A

A11 is now the highest-priority recommendation in the catalog: "the
U_W₀ vs U_S* alignment experiment is the foundational pre-flight check
that all of A1–A10 depend on." Falsifier is the existing four-outcome
enumeration. Source is the corpus's own
`experiment_design_reference_frame_measurement.md`. Connections to A1
(mergeability is frame-dependent if frames differ), A2 (two of four
estimators read U_W₀ — `t*` is frame-conditional if frames differ), A5
(Karcher mean is on a different Grassmannian per frame), A8
(anti-grokking detector is frame-conditional), A10 (Cross-LoRA's
ρ_AB aligns *base-weight* bases, so A10 is sensitive to which frame
matters).

## A10 caveat added per advisor flag (iter_008 review)

One-line caveat appended to A10's Status section: "The model tree is
one connected base manifold" is Synthesis 18's interpretation of
MoTHer's evidence, not Synthesis 18's evidence itself. MoTHer recovers
a discrete tree of finite vertices; the continuous-manifold reading
is extrapolation. The A10 falsifier tests cross-base subspace
agreement after `ρ_AB` — sound regardless of whether the underlying
space is a continuous manifold. If A10 is ever promoted into plan.md,
the language should be calibrated. Falsifier unchanged.

## TeleLoRA fetch deferred

The fallback candidate (TeleLoRA 2503.20228 PDF fetch) is NOT pursued
this iteration because A11 fell out cleanly from the existing
experiment doc. TeleLoRA remains a stub in the graph (degree 1) and
remains a candidate for a future iteration if the loop wants to extend
Section C with a seventh temporal scope (cross-base-model-generation).
Defer to iter_010 or later only if there's a specific reason to fetch.

## Watchlist (Section D in BREAKTHROUGH.md) updated

Added one entry: the existing
`experiment_design_reference_frame_measurement.md` doc, with explicit
"design only — NOT YET RUN" status flag and ~$0 cost.

## Graph state

No PDFs fetched this iteration; no `graphify update .` needed. Graph
remains at 1989 nodes / 2122 edges / 179 communities (unchanged from
end of iter_008).

## What iter_010 should do

iter_009 closed the loop on a corpus document that had been hiding in
plain sight. iter_010 should look for *other hidden corpus documents*
the A1–A10 / A11 framing reaches across but the loop hasn't read.
Specific candidates:
- `BIG_IDEAS.md` (god-node level) — surfaced in early iterations as
  highly connected; never opened directly.
- `CORE_CLAIM.md` (in `finding_literature/` per the experiment doc's
  reference at L330) — referenced by A11's experiment doc but never
  read directly.
- `some_insights_lora_papers.md` — appeared in iter_008 Territory 2
  query; flagged but not read.

The pattern iter_009 just demonstrated: existing corpus content can
land an A-section finding cleanly, no new arxiv fetch needed. iter_010
should test this pattern once more before resuming arxiv-side
exploration.
