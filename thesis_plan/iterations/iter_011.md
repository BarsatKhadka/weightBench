# Iteration 11 — 2026-05-09

**Discipline held.** Arxiv-first targeted query (advisor flip from
iter_009/010 hidden-doc ordering), one PDF fetch, one A-section
finding at A2/A4 size (no inflation), one A12 prose calibration. No
hidden-doc fallback needed.

---

## Targeted arxiv hit

WebSearch query: "spiked covariance neural network weight matrix
Marchenko-Pastur empirical test deviation Gaussian universality."
Strongest match: **Hirst & Ramgoolam, "Approximate Gaussianity Beyond
Initialisation in Neural Networks" (arxiv 2510.05218, Oct 2025).**
Fetched as `approximate_gaussianity_beyond_init_2510_05218.pdf`. Read
pp. 1–4 directly.

Their headline result: ensembles of trained MNIST classifier weight
matrices show that a simple Gaussian (i.i.d. matrix variables) fits
*initialised* weights but fits *poorly post-training*; a more general
13-parameter permutation-invariant Gaussian matrix model (PIGMM) is
the smallest fix that captures the post-training distribution. They
quantify the deviation via low-order permutation-invariant matrix
invariants (linear, quadratic, cubic, quartic) and Wasserstein distance
between the empirical and PIGMM-predicted distributions.

This is exactly the empirical question CORE_CLAIM honestly flagged at
"What would break it: if B-matrices systematically violate the spiked
model." Hirst-Ramgoolam say: yes, post-training, the simple model does
break — and the 13-parameter PIGMM is the honest minimum-complexity
alternative.

## A13 added (terse, A2/A4-sized)

A13 in BREAKTHROUGH.md Section A: trained LoRA B-matrices likely
violate the simple Gaussian assumption A12 cites; PIGMM noise model is
the honest bound. Falsifier: compute Hirst-Ramgoolam's low-order
invariants on plan.md's planned 200 trained LoRA B-matrices, compare
to simple-Gaussian and PIGMM predictions. Cost: ~$0 on existing
checkpoints.

Honest caveats logged in A13: Hirst-Ramgoolam study full MNIST
classifier weights, not LoRA factors. Different symmetry group too —
S_n permutation symmetry between layers, not GL(r) gauge. Result is
*suggestive of* a similar gap for LoRA B, not direct evidence. The A13
falsifier is the direct test.

## A11 + A13 fully audit A12's two foundations

The framework now has paired stress-tests:
- **A11** tests the *signal-side* assumption — does the cross-LoRA
  covariance basis U_S* coincide with the pretrained spectrum basis
  U_W₀? (frame disambiguation)
- **A13** tests the *noise-side* assumption — does the residual after
  the rank-r signal really look Gaussian, or does it have permutation-
  symmetric structure that the simple Gaussian misses? (distribution
  bound)

Together they cover both pillars of CORE_CLAIM's spiked-covariance
foundation. A12 stays load-bearing; A11 and A13 are its honest
applicability checks.

## A12 prose calibrated (advisor backup)

Three places updated:
- **Header** changed from "theorem proves" to "theorem-sketch proves"
  to match CORE_CLAIM's own wording ("Theorem (sketch)").
- **Claim section** explicitly calls out CORE_CLAIM's "Assumptions to
  state honestly" and "What would break it" subsections, and adds:
  "The 'sketch' qualifier matters — CORE_CLAIM is internal project
  notes, not a peer-reviewed formal proof. Promotion-time language
  must say 'we cite a uniqueness theorem-sketch from prior project
  notes that grounds our measurement choices,' not 'we test the
  unique-optimal-distance theorem.'"
- **Status section** uses "sketch-level" qualifier and connects A13
  as the noise-side companion to A11's signal-side test.

## Watchlist updated

Added Hirst-Ramgoolam (2510.05218) to BREAKTHROUGH.md Section D with
the methodology summary. CORE_CLAIM's "theorem" wording in Section D
also calibrated to "theorem-sketch."

## Graph state

`graphify update .` ran post-Hirst-Ramgoolam fetch. Graph: **2027 nodes
/ 2157 edges / 192 communities** (was 1989/2122/179). The new PDF added
13 communities — likely because the paper's PIGMM formalism, Wasserstein
machinery, and matrix-invariant terminology are graph-novel relative to
the existing corpus.

## Pacing held

A13 is A2/A4-sized as the prompt required: short bullet list, single-
paragraph claim, single-paragraph falsifier, named caveats. Did not
inflate to A12-size despite A13 strengthening A12's foundation. Pattern
working: arxiv-targeted query + small A-section finding + prior-finding
calibration in one iteration.

## What iter_012 should do

The framework foundations are now reasonably bracketed:
- **Theory:** A12 (CORE_CLAIM theorem-sketch).
- **Signal-side stress test:** A11 (U_W₀ vs U_S*).
- **Noise-side stress test:** A13 (Gaussian vs PIGMM).
- **Operational instruments:** A1, A4, A5, A6 (forced by A12).
- **Cross-arch:** A10 (Cross-LoRA ρ_AB).
- **Trajectory:** A2 (consensus t*), A4, A8 (anti-grokking), A7
  (spectrum baseline).
- **Cheap side experiments:** A9 (LLC at endpoint).

Two productive directions for iter_012:
- **Hidden-doc pattern resumed.** The remaining unread doc is
  `some_insights_lora_papers.md` (partially surfaced in iter_008).
  Worth one read pass to see if it yields a clean A14 — but expect
  lower yield than CORE_CLAIM gave because of the partial visibility.
  `BIG_IDEAS.md` still deferred.
- **Targeted arxiv query (continued).** A12's third foundation (Cencov
  + Fisher-Rao on the Grassmannian) was not stress-tested this round.
  Worth a targeted query: any 2025–2026 paper measuring Fisher
  information rank on real LoRA fine-tunes, particularly checking the
  non-degeneracy assumption CORE_CLAIM lists at L62 ("Fisher metric
  non-degenerate on the task subspace; may fail for degenerate/
  uninformative tasks"). If a paper exists, A14 = "the third-foundation
  applicability check, paired with A11 and A13 to fully audit A12."

iter_012's priority: **arxiv-first again** with the Fisher-Rao /
Fisher-information non-degeneracy target, hidden-doc fallback to
`some_insights_lora_papers.md`. Same shape as iter_011.

## Summary

iter_011 produced **A13** by targeted arxiv search, calibrated **A12**
prose per advisor flag, and confirmed A11+A13 form a complete
applicability audit of A12's spiked-covariance foundation (signal +
noise sides). plan.md unchanged. BREAKTHROUGH.md updated. Graph
expanded to 2027/2157/192. iter_012 scheduled.
