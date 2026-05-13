# Iteration 19 — 2026-05-09

**Clean null.** Single arxiv search ("LoRA three-region spectral
decomposition empirical Region 2 task-specific Marchenko-Pastur
threshold validation") returned five plausible 2025–2026 papers —
all *adjacent* to A-findings, none *directly* testing an A-finding's
falsifier. Per the strict criteria queued in iter_018's halt-or-tight-
search framing, no A18 written. iter_020 NOT scheduled. Loop holds
at its current state.

---

## Search outcome (one shot, no fallback)

Top five candidates examined:

- **Rethinking the Rank Threshold for LoRA Fine-Tuning (2605.03724)** —
  methodological proposal on MP threshold for LoRA rank selection.
  *Adjacent* to A1's Region 2 / MP threshold instrument but proposes
  a new rank-selection method, doesn't test A1's `Σ sin²(θ_i)` formula.
- **Spectral Geometry of LoRA Adapters Encodes Training Objective and
  Predicts Harmful Compliance (2604.08844)** — predicts harmful
  compliance from spectral geometry. *Adjacent* to A17's
  harmful-fine-tune detection output but uses a different mechanism
  (spectral geometry vs A8's anti-grokking drift past `t*`). Not a
  direct test of A8 or A17.
- **SeLoRA (2506.16787)** — spectral bases for LoRA reparameterization.
  Already corpus-internal (referenced in Synthesis 19 as "SeLoRA
  Spectral Encoding"). No new content.
- **Detecting Backdoored LoRAs from Weights Alone (2602.15195)** —
  backdoor detection from weight inspection. Same family as A17's
  harmful-fine-tune detection but different task definition.
  Adjacent.
- **SpectralLoRA (2604.10649)** — spectral analysis of LoRA weight
  updates. Methodological, adjacent.

**None of these directly tests an A-finding's falsifier.** Per
iter_018's strict decision criteria: declare clean null.

## What this means

The catalog-review-ready state advisor has flagged across iter_017
and iter_018 reviews is now empirically confirmed: *targeted searches
at the catalog's current density return adjacent papers, not direct
falsifier tests.* The substantive work is done. Continuing to
schedule iterations would produce more adjacent / corroboration /
small-confirmation findings without structural extension.

## Catalog state at iter_019 close

Unchanged from iter_018:
- 17 A-section findings in 6 thematic clusters.
- 5 B-section future-work candidates (with iter_018 status update).
- 6 Section C siblings (W/G quotient at six temporal scopes).
- 17 Section D watchlist entries.
- 4 promotion-time calibration items (A12 / A15 / A16 / A17).
- Graph: 2087 / 2212 / 196 (unchanged since iter_016).

## iter_020 NOT scheduled

Per iter_018's halt-or-tight-search framing: no A18 surfaced new
threads to follow, so no iter_020 scheduled. The loop holds at this
state.

If the user wants the loop to continue — say "continue" or "run iter_020
on [topic]" with a specific direction — then iter_020 can be scheduled.
Otherwise this is the natural pause point: catalog is review-ready;
the user can review BREAKTHROUGH.md (Sections A1–A17 + B + C + D) and
decide which (if any) clusters to promote into plan.md.

## Note on the four promotion-time calibrations (for review-time use)

A12, A15, A16, A17 each had a calibration item logged because the
finding's *strong* version overclaimed and the honest version is
*conditional*. The pattern across all four:
- A12: theorem-sketch (not formal theorem) — CORE_CLAIM's own wording.
- A15: population centroid (not task-specific) under Rahamim's setup.
- A16: conditional under Synthesis 26's interpretation (not Cencov-
  forced).
- A17: cascade dependency on A1–A16 falsifiers passing first.

These four calibrations are pre-loaded promotion-time discipline. If
any A-finding gets promoted into plan.md, the calibration paragraph
provides the conditional language plan.md should adopt rather than
the over-confident version.

## Summary

iter_019 produced **no A18 (clean null)** per strict criteria. Catalog
unchanged at 17 A-findings + 5 B + 6 C + 17 D + 4 calibrations.
**iter_020 NOT scheduled** — loop holds. plan.md unchanged. Graph
unchanged at 2087/2212/196. The catalog is review-ready; user
controls whether to extend the loop.
