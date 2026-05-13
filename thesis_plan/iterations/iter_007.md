# Iteration 7 — 2026-05-09

**Reorientation mid-iteration.** iter_007 was scheduled as the plan.md
absorption pass — apply eight queued edits to plan.md in dependency order.
Edits 1–6 were applied. During Edit 7 I reached for AskUserQuestion to
decide the headline criterion (1-of-4 vs 2-of-4 vs drop Move 8 from headline).

The user redirected:
> "no for now, main plan let it be like that you just update here in
> breakthroughs and all, when we will have things that are for sure and
> insights that will be very helpful then add bro, dont ask me"

The discipline being established: **plan.md is canonical and stays
untouched by the loop. BREAKTHROUGH.md is the running findings catalog.
The user — not the loop — decides when a finding is solid and helpful
enough to promote into plan.md. The loop does NOT initiate plan.md
edits and does NOT AskUserQuestion to decide them.**

This is the same lesson as the iter_002→iter_003 explorer-mode
correction: I keep wanting to "ship" findings into the canonical
document; the correct discipline is to accumulate findings in the
scratchpad until the user picks promotions. Saved as memory:
`feedback_plan_md_canonical.md`.

## Actions taken this iteration

1. **Reverted all six plan.md edits applied in this turn.** plan.md is
   back to its pre-iter_007 state, character-for-character on the affected
   sections.
2. **Saved `feedback_plan_md_canonical.md`** to memory and indexed it in
   `MEMORY.md` so future iterations do not repeat this failure mode.
3. **Rewrote BREAKTHROUGH.md** as a structured running findings
   catalog: Section A (in-scope depth moves A1–A9 with falsifiers),
   Section B (out-of-scope future-work candidates B1–B5), Section C
   (four-siblings `W/G` table), Section D (watchlist sweep status). The
   user reviews this to decide promotions. The loop does not initiate
   them.
4. **Aborted Edits 7 and 8.** They are now A8 and A1 in BREAKTHROUGH.md
   Section A, with the headline-criterion question logged inside A8 as
   a *paper-design decision the user should make explicitly if A8 is
   promoted* — not a question the loop asks during a wakeup.

## What was learned (beyond the rule)

- Edits 1–6 worked cleanly without conflict before the redirect — meaning
  the eight edits *would* have applied to plan.md without breaking it
  structurally. The technical discipline (Edit-tool replace, not Write
  rewrite; old_string match before new_string apply) held. The redirect
  is about the *governance* of plan.md, not the mechanics.
- BREAKTHROUGH.md is now substantially richer: nine A-section findings
  with named falsifiers, five B-section future-work pointers, the
  Section C four-siblings table the loop derived, and Section D
  watchlist that survives across iterations. This is the right shape
  for a running findings catalog the user can scan.

## What iter_008+ should do

- **No more queued plan.md absorption passes.** Strike that pattern.
- Continue exploration in iter_NNN.md (per-iteration logs) and
  consolidate strongest findings into BREAKTHROUGH.md Section A
  (in-scope) or B (out-of-scope) at end-of-iteration.
- Use real graphify queries; don't synthesize from imagination.
- Pull arxiv PDFs not summaries; no MD abstracts.
- Stay in plan.md scope (per "What I Will Not Do This Year" exclusions);
  the in-scope depth moves listed in BREAKTHROUGH.md Section A are the
  reservoir to draw from.
- Surface NEW non-obvious moves the loop has not yet produced. The bar:
  must clear A1–A9. Refining one of A1–A9 is fine *only* if the
  refinement is itself a substantive new finding.
- Do NOT ask the user via AskUserQuestion about plan.md changes.
- BREAKTHROUGH.md grows; plan.md does not.

## Status

iter_007 closed. plan.md reverted and untouched. BREAKTHROUGH.md
consolidated. Memory updated. iter_008 scheduled with the new
discipline.
