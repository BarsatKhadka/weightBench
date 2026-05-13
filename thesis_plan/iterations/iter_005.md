# Iteration 5 — 2026-05-08

**Discipline this iteration:** tighter than iter_004. One move written up,
one watchlist sweep, two gap logs, one queue. No code, no pseudocode, no
halt declarations.

---

## 1. Move 4 — Riemannian path-vs-speed within the geodesic frame

**Why this and not Move 5.** Move 4 directly exploits iter_004's geodesic
landing; Move 5 (α-trajectory triple signal) is incremental feature
addition. The user's standing instruction ("very non obvious, very
breakthroughs") favors the move that the geodesic frame *forces*, not
the one it merely permits.

**Where in plan.md.** Section 5 (E2 Trajectory Geometry), T2 ("Path vs
speed"). Currently uses Dynamic Time Warping on the scalar curve
`d_G(checkpoint_t, endpoint)` vs. step `t`. The DTW reduces a curve on
the Grassmannian to a single scalar profile, throwing away its
*direction* information.

**The depth move.** Under iter_004 §1, each LoRA training trajectory IS a
curve on `G(d_task, m)` after π. Two same-task trajectories that hit the
same endpoint are "the same path traversed at different speeds" iff,
after **arclength reparameterization** on the Grassmannian, their
**tangent subspaces at matched arclengths agree**. Operationally this
means: at each matched arclength position, each curve's tangent is a
horizontal-lift `d_task × (m − d_task)` matrix; compare the two via
**principal angles between these tangent subspaces** at the same base
point on `G(d_task, m)`. **No parallel transport** along the curves is
invoked — parallel transport on the Grassmannian is path-dependent
(holonomy), and the corpus's holonomy work is precisely the kind of
deep theory plan.md excludes from this paper. The operational definition
is a vector-valued test where DTW on `d_G` was scalar; the
parallel-transport-extended version is a future-work falsifier and is
explicitly NOT what Move 4 invokes.

Two operational consequences plan.md does not currently have:
1. **Same-path-different-speed becomes geometrically falsifiable, not
   threshold-tuned.** Tangent overlap at every matched arclength position
   is a curve in [-1, 1]; "same path" means this curve stays near 1.
   "Different paths" means it dips below some null-distribution
   threshold (the null is matched-arclength tangents from
   *different-task* trajectories). The threshold becomes a
   permutation-test number, not a hand-picked DTW cutoff.
2. **Speed itself becomes a signal.** Same-task trajectories that share
   a path but differ in speed give differential geometry information
   (Riemannian arclength rate vs. training step). Two same-path runs
   with different LR schedules will have different `dτ/dt` profiles
   on the geodesic — that *is* the curriculum signature. plan.md's
   Section 5 currently ignores this; the geodesic frame says it's the
   natural quantity to measure.

**Falsifier.** For 50 same-task LoRA pairs that hit the same endpoint
accuracy ±2%:
- Compute matched-arclength tangent overlap on `G(d_task, m)`.
- Compare the overlap-vs-arclength curve to the null distribution
  obtained from 50 different-task pairs.
- Same-path-different-speed claim holds if same-task curves stay above
  the 95th percentile of the null at every matched arclength position;
  fails if at any point they cross below.

**Cost on plan.md's compute budget.** Zero new training. Tangent vectors
on the Grassmannian are computed in closed form from consecutive
canonical-form Region 2 subspaces (the SVD of the difference); this
runs in CPU time on saved checkpoints. Falls inside the 120-GPU-hour
training budget already committed.

**Fusion with Move 1 made concrete.** Move 1's `Σ sin²(θ_i)` between two
*subspaces* is the squared Grassmannian distance; Move 4's tangent
vectors are the *velocities* along the geodesic between them. M1
measures the chord; M4 measures the velocity along it. Same object,
different temporal granularity.

---

## 2. Move 9 cost evaluation — parked in full form, kept in restricted form

**Full form (LLC over trajectory).** DevInterp's LLC estimator (Lau et
al. 2023) uses multi-temperature SGLD. Standard recipe: 200–1000 samples
per LLC estimate, ~30 s/sample for a LoRA-rank parameter set on top of a
7B base via natural-gradient SGLD on the loss.

| Quantity | Estimate |
|---|---|
| Per-checkpoint LLC | ~10–30 minutes GPU-time (200–1000 samples × 30 s) |
| Per-LoRA over trajectory | 30 checkpoints × ~20 min ≈ 10 GPU-hours |
| Population-wide | 200 LoRAs × 10 GPU-hours = **2,000 GPU-hours** |

plan.md's total budget is 120 GPU-hours. Move 9 in full form is **~17×
over budget**. **Park as deferred — requires a compute extension or a
later paper.**

**Restricted form (LLC at endpoint only).** For 200 endpoints, total
SGLD time is `200 × ~20 min ≈ 70 GPU-hours`, which is ~58% of the
budget. Too expensive to dedicate the whole budget to endpoint LLC.

**Restricted-restricted form (LLC at endpoint, sparse subset of 50
LoRAs).** `50 × ~20 min ≈ 17 GPU-hours`. Fits in 14% of the budget.
This is small enough to keep as a *checkpoint sanity test for Move 8*:
Synthesis 9 §5 predicts low LLC at well-trained endpoints in
`S(task)` and high LLC at anti-grokked endpoints. With 50 LoRAs split
~25 well-trained / ~25 deliberately overtrained, this is a clean
falsification check on Synthesis 9's "LLC measures horizontal subbundle
proximity" claim — done at endpoint, not trajectory, so the dynamical
Move-9 claim ("LLC anti-correlates with Fisher-metric trajectory speed")
remains scientifically deferred but a *static* corollary survives in
budget.

**Verdict.** Move 9 in scientifically interesting form (dynamical) is
parked. A 17-GPU-hour static corollary at endpoints survives as a
cheap consistency check on Move 8 and Synthesis 9. iter_006+ does NOT
need to revisit Move 9 unless the budget grows.

---

## 3. Known gaps logged (do not attempt to fix)

**3.1 Restriction-lemma gap.** iter_004 §1 claims:
> *Fisher-metric geodesic on W/G base manifold restricted to Region 2 IS
> the Grassmannian geodesic on `G(d_task, m)`.*

Synthesis 9 §4 ("Slow Fisher Mode Connection") + Synthesis 21
("Fisher-Rao = natural connection on the base") together *suggest* this
identification. The corpus does not prove it. plan.md's exclusion ("no
theoretical proof of LoRA-LMC; theory comes after") covers this — the
claim works as a guiding heuristic for the empirical paper. Logged here
so future-me does not silently upgrade "suggested by corpus" to
"proved by corpus" in later iterations.

**3.2 Move 8 t*-undefined edge case.** Anti-grokking detection
(post-π drift past `t*`) requires `t*` to fire — i.e., all four `d_task`
estimators within ε ≈ 0.5 of mean per Move 2's resolution. For LoRAs
where the slowest estimator (RLCT proxy) does not converge inside the
training horizon, `t*` is undefined and Move 8's drift signal cannot
be referenced. Falsifier specification in iter_004 needs to fall back:
- **Fallback 1:** drop those LoRAs from the Move 8 evaluation. Loses
  data but keeps the test clean.
- **Fallback 2:** use a 3-of-4 consensus (drop RLCT, since it is the
  slowest) — admits a slightly weaker `t*` but covers more LoRAs.
- **Fallback 3:** define `t*` as the step where `α` (the fastest
  estimator) plateaus, then check the *consistency* with the slower
  three at endpoint only.

iter_006 picks one. This is the kind of decision that should not be
made on autopilot — it changes Move 8's coverage and statistical
power.

---

## 4. Watchlist sweep — one PDF fetched

Searched arxiv for `LoRA + trajectory + Grassmannian` and `mode
connectivity LoRA 2026`. Surfaced (no MD abstracts written):
- `Randomized Gradient Subspaces for Efficient LLM Training` (2510.01878,
  GrassWalk / GrassJump). **Different setting** — Grassmannian methods
  for full-LLM pretraining subspace optimization, not LoRA fine-tuning
  trajectory geometry. Cousin not preemption; cite if E2 needs broader
  Grassmannian-on-LLM context.
- `Learning in the Fisher Subspace: A Guided Initialization for LoRA
  Fine-Tuning` (2605.01046). LoRA initialization in Fisher subspace.
  **Initialization, not trajectory.** Already in corpus as FILet
  (Community 10).
- `LoRA-One: One-Step Full Gradient Could Suffice` (2502.01235).
  Restates SRFM (Synthesis 29) — single-step gradient predicts LoRA's
  task subspace. Already in corpus.
- `FLoRG: Federated Fine-tuning with Low-rank Gram` (2602.17095).
  **Procrustes alignment for federated LoRA aggregation.** Procrustes is
  the orthogonal-restriction of CopRA-LA's invertible matrix alignment
  and a special case of W2T's π. Direct sibling of plan.md's
  canonicalization at federated-merge time. Fetched (`florg_federated_
  lora_gram_2602_17095.pdf`); confirms but does not preempt.

**Conclusion.** Sweep clean. No 2026 paper does (LoRA + GL(r)-quotient
+ trajectory geometry + LMC) as plan.md does. Watchlist remains live.

---

## 5. Queued plan.md absorption pass (for iter_006 or 007 — DO NOT execute now)

Edits plan.md will need once one or two more iterations have closed:

- **Section 1 (Introduction) and Section 5 (E2):** restate the
  LoRA-LMC conjecture in **Grassmannian-geodesic** language, not
  linear connectivity. Frankle 2020 LMC asks for line connectivity in
  flat ambient space; LoRA-LMC under GL(r) quotient asks for
  *geodesic* connectivity in the W/G base manifold's Riemannian
  category. This reframe is the iter_004 §1 result and is the paper's
  sharpened novelty wedge.
- **Section 3 (Method):** cite **CopRA-LA (2410.22911)** and **FLoRG
  (2602.17095)** when introducing the π canonicalization. CopRA-LA does
  pairwise GL(r)-alignment at merge time; FLoRG does Procrustes (an
  orthogonal subgroup of GL(r)) at federated-aggregation time; plan.md
  applies W2T's π globally at measurement time. The three are siblings
  with different scopes.
- **Section 5 (E2), T1 (phase transition statistic):** swap Schürholt's
  borrowed full-network phase machinery for the LoRA-native
  four-estimator-consensus `t*` per iter_003 Move 2, with the
  all-four-within-ε-of-mean consensus definition resolved in
  iter_004 §3. Cite Synthesis 15 explicitly.
- **Section 5 (E2), T2 (path vs speed):** replace DTW-on-scalar with
  the matched-arclength tangent overlap on `G(d_task, m)` per Move 4
  above. Falsifier becomes a permutation test against different-task
  null, not a hand-picked DTW cutoff.
- **Section 6 (Predictive Demonstration):** add **Move 7 (TRS-spectrum-
  only baseline)** and **Move 8 (anti-grokking detector)** as fourth
  and fifth downstream targets. Both use the same Grassmannian-
  distance instrument as Move 1; same compute envelope.
- **Section 6, Target 1 (mergeability):** restate the prediction as
  the analytic `Σ sin²(θ_i)` formula (per iter_003 Move 1, with iter_004
  §2's canonical Grassmannian principal-angle metric for `d_a ≠ d_b`)
  with two scalar coefficients fitted, NOT a learned regressor. The
  result becomes a theorem-with-empirical-confirmation rather than a
  feature-engineered regression score.
- **Beyond ICLR 2027 — Self-Evolving Agent Vision section:** add a
  short paragraph noting that the same Grassmannian-distance
  instrument naturally extends to a *capability-introspector tool*
  (BREAKTHROUGH.md future-work direction) — the paper's measurement
  methodology is the seed of the deployable tool the project's
  long-term north star asks for.
- **What I Will Not Do This Year section:** keep all four exclusions
  intact. iter_004's geodesic claim does not require a theoretical
  proof of LoRA-LMC; the empirical wedge stands without it.

These are seven concrete edits. They should be done in *one focused
turn*, not spread across iterations. iter_006 or iter_007 absorbs them.

---

## What iter_006 should do

- Pick **Move 5** (α-trajectory triple signal) — the remaining iter_003
  parking-lot move — and write at M1/M2/M3 depth, exploiting the
  geodesic frame.
- Resolve the Move 8 t*-undefined fallback (3-of-4 consensus is the
  default unless iter_006 finds a corpus-grounded reason otherwise).
- One more arxiv watchlist sweep (different query terms each time, to
  cover blind spots).
- Do NOT yet execute the plan.md absorption pass — that is iter_007 or
  later, in a focused turn dedicated to it.
