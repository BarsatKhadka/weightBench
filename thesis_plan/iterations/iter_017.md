# Iteration 17 — 2026-05-09

**Path 1 landed.** BIG_IDEAS.md (read directly with the
application-from-instrument-cluster thread, after 7 deferrals) yielded
**A17 — the loop's first explicit application finding**, connecting
the A1+A5+A8+A10+A11+A14+A15+A16 instrument cluster to BIG_IDEAS.md's
named "Zero-Shot LoRA Audit" application (Idea 13). Region-1 paradigm
arxiv fallback NOT invoked. A16 prose calibration applied per advisor
flag from iter_016.

---

## What BIG_IDEAS.md actually contained

30KB document with 26 numbered ideas across multiple iteration-log
entries. Most ideas (1–12, 14–26) are *theory* or *measurement*
proposals already internalized as A1–A16:
- Ideas 17, 18 → corpus's three-region split (already in A1's setup).
- Idea 22 → intruder dims as holonomy (Synthesis 9 §4 / A14 territory).
- Idea 25 → sheaf-bundle holonomy (corpus theory; not in scope per
  plan.md's "no theoretical proof" rule).
- Idea 26 → universal subspace as flat Fisher directions (corpus
  theory).
- Idea 24 → optimal rank ≈ √N (NTK theory; corpus background).

The *applications* in BIG_IDEAS.md are sparser. The strongest:
- **Idea 13: Zero-Shot LoRA Audit via LoL + TRS** — explicitly framed
  as productizable, with six named outputs and venue ambition
  ("NeurIPS workshop paper → ICLR 2027 full paper").
- Idea 6: spectral genealogy (provenance tool).
- Idea 7: universality threshold (diagnostic).
- Idea 15: task sequencing for continual learning curriculum.

A17 focuses on Idea 13 because each of its six outputs maps cleanly
to an instrument the loop has now catalogued. The other named
applications are secondary — Ideas 6/7/15 are mentioned in A17's
status note but not given separate A-section entries.

## Why Idea 13 was deferred for 7 iterations

When BIG_IDEAS.md was written (corpus iteration 2, May 2026, before
the loop's iter_001), the audit's measurement instruments were not
yet defined. Idea 13's outputs required:
- Task label → A1+A5 (mergeability + Karcher distance) → defined
  iter_003 (M1) + iter_006 (M5).
- Training-data characteristics → A2 (consensus `t*`) → defined
  iter_003 (M2).
- Estimated held-out performance → A14 (LLC) → defined iter_012.
- Harmful fine-tune detection → A8 (anti-grokking) → defined iter_004.
- Cross-architecture compatibility → A10 (Cross-LoRA `ρ_AB`) +
  A16 (paradigm choice) → defined iter_008 + iter_016.
- Pre-flight applicability → A11 (U_W₀ vs U_S* alignment) → defined
  iter_009.

So the BIG_IDEAS.md → A17 chain required 17 iterations. The deferral
was correct: opening BIG_IDEAS.md in iter_009 (when A11 was just
landing) wouldn't have produced A17 because A14, A16, A10 weren't
yet defined.

## A17's structural significance

A17 is the loop's *first application-tier finding*. A1–A16 are all
either measurement instruments (A1, A4, A5, A6, A7, A8, A9, A10,
A11) or theoretical anchors (A12, A13, A14) or audit pairs (A15, A16).
A17 pulls the cluster together into a deployable diagnostic tool.

This is structurally distinct from the rest of the catalog. Where
A1–A16 strengthen plan.md's *empirical paper*, A17 strengthens
plan.md's *Section 7 / Self-Evolving Agent Vision* by providing
concrete grounding for Discussion-section argumentation: the
trajectory measurement instruments E1+E2 build are exactly what an
audit tool needs.

A17 does NOT violate plan.md's "no self-evolving agent
implementation" exclusion — audit is a passive diagnostic tool, not
an agent. The Discussion section gets the application-grounded
argument it currently lacks.

## A17 falsifier (compound, A2/A4-sized)

Build a minimal audit tool combining the A-cluster instruments. Test
on ~50 held-out HuggingFace LoRAs with known task / training-data
labels. Each of six audit outputs measured against ground truth.
Pass criterion: ≥ 3 of 6 outputs achieve > 0.8 accuracy/correlation.
Fail criterion: ≤ 1 of 6 — instrument cluster insufficient for
deployment, A17 refuted at the productization level.

Cost: ~$0 SVD + A9 LLC budget (~17 GPU-hours endpoint) + modest
inference cost for ground-truth labeling. Total: well within plan.md's
stretch envelope, runs alongside A10's existing falsifier on the same
LoRA pool.

## A16 prose calibration applied

Per iter_016 advisor flag, A16's "interesting structural claim"
section now begins **"If Synthesis 26's Platonic-Region-1 /
Aristotelian-Region-2 reading is correct — itself a corpus
*interpretation* of the Platonic Representation Hypothesis (Huh et
al. 2024) applied to LoRA's three-region decomposition, *not* a
Cencov-style proved theorem — *then* the alignment-paradigm choice
splits cleanly..."** One sentence change, calibrating "theoretically
forced" to "conditionally forced under Synthesis 26's reading."

Three calibration items now logged in BREAKTHROUGH.md as
promotion-time discipline:
- A12: theorem → theorem-sketch (CORE_CLAIM's own wording).
- A15: task-neighbors → population centroid (Rahamim's setup uses
  random partners across tasks).
- A16: theoretically forced → conditionally forced under Synthesis
  26's interpretation.

These are language-tightening matters for if/when the user promotes
findings to plan.md, not corrections to the falsifiers.

## Section A thematic-index update needed (queued, not done now)

A17 is the catalog's first application-tier finding. The thematic
index (added in iter_013) groups A1–A16 by theme; A17 doesn't fit
any existing cluster — it's a *cross-cluster pull-through*. The
index could grow a sixth entry: "Application cluster (A17 alone) —
pulls instruments from clusters 1–5 into a deployable audit tool."

Queued for iter_018 if the iteration is otherwise short.

## Watchlist (Section D) updated

Added BIG_IDEAS.md entry with the 7-deferral note and the Idea-13
focus.

## Graph state

No PDFs fetched (BIG_IDEAS.md was already in the graph as a node).
Graph remains at 2087/2212/196 (unchanged from iter_016).

## Pacing held

iter_017 is the right size: one specific-thread Read of a hidden
corpus doc, one A-section finding, one prior-finding calibration.
Same shape as iter_009 (CORE_CLAIM.md → A12) and iter_010 (experiment
doc → A11): god-node-grade hidden doc + specific thread = strong
A-finding.

## Loop trajectory observation

The pattern across iterations:
- **Hidden corpus doc reads:** A11 (iter_009), A12 (iter_010), A14
  (iter_012, partial), **A17 (iter_017)**.
- **Targeted arxiv hits:** A10 (iter_008), A13 (iter_011), A14 (iter_012,
  partial), A15 (iter_015), A16 (iter_016).
- **Cross-paper synthesis:** A14 (corpus + Lakkapragada), A16
  (corpus + Cui et al.), A17 (corpus + cluster).

Hidden-doc reads and arxiv hits each produced ~half the catalog. The
A-findings differ in flavor: hidden-doc reads tend to surface
*foundational* findings (theorem-sketches, applications);
arxiv hits tend to surface *empirical benchmarks* and *comparison
points*.

## What iter_018 should do

Two productive directions:
1. **Targeted arxiv on Region-1 alignment paradigm** (deferred from
   iter_017's queue). Could surface an A18 confirming or refuting
   A16's Region-1 / activation-OT claim. Per advisor's iter_016
   note, this is *complementary* to A16 rather than structurally new
   — would be a confirmation finding, not a structural extension.
2. **Section A index touch-up** to add an "Application cluster"
   entry for A17. Small consolidation work, similar to iter_013's
   thematic-index pass but additive. Could combine with (1) in one
   iteration.
3. **Section B mini-refresh** (deferred from iter_014's queue).
   With 17 A-findings, B1 (GE-LoRA-Hyper-CL) is increasingly
   subsumed by A12+A14+A16 etc. One paragraph noting which
   B-findings are now A-supported future-work vs still distinct
   would close that loose thread.

iter_018 priority: **arxiv on Region-1 paradigm first** (continues
the productive search pattern); fallback combined Section A index
touch-up + Section B mini-refresh as a small consolidation if (1)
returns nothing close. Same null-permission discipline.

## Summary

iter_017 produced **A17 — Zero-Shot LoRA Audit Tool from BIG_IDEAS.md
Idea 13, now testable from the loop's instrument cluster**. The
loop's first explicit application-tier finding. **A16 prose
calibration applied** per advisor flag (Synthesis 26 = corpus
interpretation, not theorem). BIG_IDEAS.md read with the specific
thread; 7-iteration deferral was correct given Idea 13 needed
A11/A14/A16/A10 to be defined first. plan.md unchanged. Section D
updated. Graph unchanged at 2087/2212/196. iter_018 scheduled.
