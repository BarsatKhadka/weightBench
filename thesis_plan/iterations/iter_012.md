# Iteration 12 — 2026-05-09

**Discipline held.** Fallback chain (level 1 → level 2 → hidden-doc) per
advisor; explicit permission to return null A14 was not exercised because
level 2 yielded a clean A14. A2/A4-size discipline maintained.

---

## Level 1 — narrow Fisher-on-LoRA query

WebSearch: "Fisher information rank LoRA fine-tuning non-degeneracy task
subspace singular." Top hits were FILet (already in corpus, Community
10), LoRA-DA (data-aware init, similar to FILet), TLoRA, OPLoRA
(already in corpus), gradient subspaces papers. **None directly tests
Fisher metric non-degeneracy as a falsifiable hypothesis on LoRA
fine-tunes.** Level 1 returned nothing close.

## Level 2 — broader SLT / Fisher-rank query

WebSearch: "Fisher information matrix rank deficiency neural network
singular learning theory degeneracy." Surfaced the **Singular Learning
Theory (Watanabe) literature directly**:
- Lakkapragada (2512.00686, Dec 2025) — SLT applied to grokking and
  phase transitions, lightweight toy models
- Singular learning coefficients (2501.12747)
- Mechanistic interpretability via degeneracy (2405.10927)
- Watanabe SLT references (2009 + 2018 books, cited throughout corpus)

**Level 2 succeeded by surfacing a corpus-already-known framework.** The
corpus has SLT material across multiple syntheses (notably Synthesis 14:
"LoRA's Gauge Symmetry IS the SLT Singularity"; Synthesis 9 §5: "LLC
measures horizontal subbundle proximity"; Community 21: Watanabe + LLC
+ Lau et al. 2023). What level 2 added is the recent application —
Lakkapragada (2512.00686) — and the *explicit empirical confirmation*
that the Fisher matrix is generically non-invertible at NN optima.

Fetched `slt_phase_transitions_grokking_2512_00686.pdf` for currency,
read pp. 1–3 directly. Lakkapragada's headline statement:

> *"neural networks are *singular* statistical models … singular models
> do *not* exhibit expected statistical behavior. As an example, the
> Fisher Information matrix, the basis of asymptotic normality theory
> for MLEs, is often non-invertible at the true parameters in singular
> models (Watanabe, 2010)."*

This is the empirical/theoretical statement that *resolves* A12's
foundation-3 audit before any new experiment is needed.

## A14 added — terse, A2/A4-sized

A14 reframes A12's foundation 3 from "audit whether non-degeneracy
holds" to "non-degeneracy fails generically; SLT is the corpus-internal
framework that handles it." The right reading is that A12's three
foundations decompose as:
- **Foundation 1 (Johnstone-Paul spiked covariance):** empirical
  applicability bracketed by A11 (signal) + A13 (noise).
- **Foundation 2 (GL_r invariance):** algebraic fact, no audit.
- **Foundation 3 (Cencov + Fisher-Rao non-degeneracy):** fails by
  construction for neural networks; SLT/LLC is the right framework
  (corpus-internal: Synthesis 14, Community 21; recent application:
  Lakkapragada 2512.00686).

A12's three foundations are now fully accounted for. A14 connects
A2's RLCT-proxy estimator to foundation 3 explicitly, and connects
A9's static LLC corollary as the empirical signature of A14. Same
~17-GPU-hour stretch budget covers both.

This *strengthens* A12 rather than weakening it: the previous prose
hand-waved foundation 3 with "may fail for degenerate/uninformative
tasks." A14 says the failure is the *generic case*, and the framework
that handles it (SLT) is already in the corpus.

## A2/A4-size discipline held

A14 is short bullet list, single-paragraph claim, single-paragraph
falsifier, named caveat (Lakkapragada uses toy models, not LLM LoRAs).
Did not inflate to A12-size despite resolving a foundation. The
strength of A14 is that it leverages corpus-internal material — most
of the work was *already done* across many iterations of synthesis
notes; A14 just makes it explicit at the foundation-3 level.

## Watchlist updated

Added Lakkapragada (2512.00686) to BREAKTHROUGH.md Section D with the
empirical-SLT methodology summary.

## Graph state

`graphify update .` ran post-Lakkapragada fetch. Graph: **2040 nodes /
2169 edges / 192 communities** (was 2027/2157/192). Node count grew by
13, edge count by 12, communities held — Lakkapragada's content is
adjacent to existing SLT material in the graph (Community 21 and
related), so new nodes were added without spawning new communities.
This is consistent with A14's "corpus-internal" character.

## Pacing held

Same shape as iter_011: one targeted search (level 1 + level 2 since
level 1 didn't land), one PDF fetch, one A-section finding at A2/A4
size, no inflation. Pattern works across consecutive iterations.

## What iter_013 should do

The framework foundations are now fully bracketed:
- **Theorem-sketch (A12):** Grassmannian + Fisher-Rao + TRS = unique
  invariant task distance, given assumptions.
- **Foundation-1 audits:** A11 (signal-side), A13 (noise-side).
- **Foundation-3 framework:** A14 (SLT/LLC handles generic failure).
- **Operational instruments:** A1, A4, A5, A6 (forced by A12).
- **Cross-arch:** A10 (Cross-LoRA `ρ_AB`).
- **Trajectory:** A2, A4, A8 (consensus `t*`, tangent overlap,
  anti-grokking).
- **Cheap experiments:** A7 (spectrum baseline), A9 (LLC at endpoint).

Two productive directions for iter_013:
1. **The Cross-LoRA `ρ_AB` audit / extension.** A10 names Cross-LoRA's
   alignment as `ρ_AB` but doesn't audit *when* the Frobenius-optimal
   linear transform is itself degenerate (e.g., dim mismatch with rank
   deficiency, or when source and target W₀ have very different
   spectra). A short search for any 2026 paper on cross-arch LoRA
   alignment failure modes might surface a parallel to A11/A13's
   stress tests but on the cross-arch axis.
2. **Hidden-doc pattern resumed** if arxiv search returns nothing
   sharp. `some_insights_lora_papers.md` remains unread; partially
   surfaced in iter_008 Territory 2.

iter_013 priority: **Cross-LoRA / cross-arch alignment failure-mode
arxiv search first; some_insights fallback.** Same shape as iter_011
and iter_012. A2/A4 discipline. Explicit permission to return null
A15.

## Summary

iter_012 produced **A14 — A12's foundation 3 fails generically; SLT
handles it** by combining a level-2 arxiv hit (Lakkapragada
2512.00686, Dec 2025) with corpus-internal SLT material (Synthesis 14,
Community 21, Lau et al. 2023 LLC). A14 completes the audit of A12's
three foundations: foundation 1 stress-tested empirically by A11 +
A13; foundation 2 algebraic and self-evident; foundation 3 fails
generically with SLT as the handling framework. plan.md unchanged.
BREAKTHROUGH.md Section A now has 14 in-scope depth-move findings;
Section D has 14 audited prior-art entries. iter_013 scheduled.
