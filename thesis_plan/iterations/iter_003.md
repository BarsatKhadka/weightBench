# Iteration 3 — 2026-05-08

**Reorientation this turn.** User redirect: "align with thesis_plan/plan.md and
make that better by going very non-obvious places and deep — that's a good thing."

Re-reading plan.md I see what iter_001 and iter_002 missed. plan.md explicitly
declares **what will NOT be done this year**:
- "No new architecture proposal (no GrassmannLoRA, **no Capability-Reserved
  Pretraining**)"
- "No LS-Merge style autoencoder"
- "No self-evolving agent implementation (only argued for in discussion)"
- "No theoretical proof of LoRA-LMC (empirical paper; theory comes after)"

The candidate iter_002 surfaced (GE-LoRA-Hyper-CL) is a *new architecture
proposal* — explicitly excluded for this year's paper. The "pre-training
surgery" direction in BREAKTHROUGH.md is *Capability-Reserved Pretraining* —
also explicitly excluded. Both are genuinely interesting future-work targets;
neither is in scope for ICLR 2027.

**iter_003 therefore re-focuses on plan.md itself**: which non-obvious deep
moves strengthen the actual paper that the user has committed to. Per the
explorer-mode rule, no code, no pseudocode. Architectural concepts okay,
implementation detail not.

The candidate from iter_002 (GE-LoRA-Hyper-CL) and the alternatives in
BREAKTHROUGH.md are demoted to "future-work directions argued for in the
Discussion section, NOT in-scope for the paper."

---

## Three non-obvious deep moves into plan.md

### Move 1 — Mergeability becomes ANALYTIC, not a regression target

**Where in plan.md:** Section 6 (Predictive Demonstration), Target 1
("Mergeability prediction"). Currently treated as a learned regressor over
endpoint / endpoint+behavior / endpoint+trajectory+behavior features.

**The depth move.** Synthesis 16 (corpus) says: merge interference between
two LoRAs IS the projection mismatch between their Region 2 subspaces. The
"five methods, one constraint" result (OSRM, EBLoRA, OPLoRA, mtLoRA, Share)
all reduce to: minimize `sin²(θ)` between adapter subspaces. So Section 6's
post-merge accuracy drop should be *analytically predicted* from principal
angles between Region 2 subspaces — no learned regressor needed.

**Concretely (still no code):** for a pair of adapters `(L_a, L_b)`, compute
the principal angles `{θ_i}` between their Region 2 subspaces (after π
canonicalization). Predict the post-merge accuracy drop as a *monotone
function* of `Σ sin²(θ_i)` — fitted with two scalar coefficients (slope and
intercept), nothing learned with capacity. If this 2-parameter analytic
prediction matches a learned regressor's R² on held-out adapter pairs, the
paper's section 6 becomes a *theorem-with-empirical-confirmation* result
instead of a feature-engineering result. That is qualitatively stronger.

**Why non-obvious.** plan.md treats mergeability as a downstream prediction
target. The corpus has the closed-form story (Synthesis 16, Synthesis 23 —
Task Second-Moment Operator S three-region decomposition is the Region-2
subspace) but plan.md doesn't reach for it.

**Falsifier.** Pearson r between `Σ sin²(θ_i)` and post-merge accuracy drop,
on the 200 random adapter pairs already required by the plan. If r > 0.85
the analytic predictor wins the section. If 0.5 < r < 0.85 the analytic
predictor is a strong baseline the regressors must beat. If r < 0.5 the
mechanism is wrong and Synthesis 16 is empirically refuted — also
publishable.

**Cost on the plan's compute budget:** zero new training. Adapter pairs
are already merged for the regression targets.

---

### Move 2 — `d_task` trajectory IS the native phase statistic

**Where in plan.md:** Section 5 (E2 Trajectory Geometry), T1
("Convergence dynamics", "phase-transition statistic"). Currently borrows
Schürholt's full-network phase machinery (2504.18072) and "From Spikes to
Heavy Tails" (5+1 phases).

**The depth move.** plan.md already names *four independent corpus
estimators of `d_task`*: GELoRA Theorem 3.2, AlphaLoRA's α, TRS singular-
value count above MP, Watanabe RLCT. plan.md uses them at *endpoints* to
size Region 2. But the corpus says all four estimators converge on the
same `d_task` at the optimum. Tracking *all four over training time* gives
a per-checkpoint *consensus signal* that is native to LoRA's GL(r) quotient
— it does not need Schürholt's full-network phase machinery imported.

The phase transition is operationally: the step `t*` at which the four
estimators agree to within a tolerance ε. Before `t*`, the network is
exploring; after `t*`, it has committed to a `d_task`-dimensional task
subspace. This `t*` is the LoRA-native phase boundary.

**Why non-obvious.** No corpus paper tracks all four `d_task` estimators
over a training trajectory — they appear in different papers (Synthesis 15
unifies them but only at the endpoint). The four-estimator-consensus phase
detector is a free contribution of plan.md that plan.md itself does not
yet name.

**Falsifier.** For ≥ 80% of LoRAs in the population, `t*` (four-estimator
consensus) lands inside the convex hull of phase transitions detected by
Schürholt's borrowed statistic. If yes, the LoRA-native phase detector
*replaces* the borrowed one in the headline plot of Section 5. If no,
the four estimators may not actually converge to the same `d_task` along
trajectories — also a finding (Synthesis 15 is a snapshot result, not a
trajectory result).

**Cost:** zero new training. WeightWatcher already gives α per checkpoint;
GELoRA's TwoNN, MP-count, and RLCT-proxy run on saved checkpoints in CPU.

---

### Move 3 — CoTo collapses from competitor to corroboration

**Where in plan.md:** Introduction novelty positioning + Risk row "Reviewer
pattern-matches to CoTo". Plan currently distinguishes *measure* (us) from
*promote* (CoTo) — defensive framing that concedes overlap.

**The depth move.** CoTo's stochastic adapter deactivation can be read
as: regularize the optimization trajectory toward the geodesic on
`G(d_task, m)`. If LoRA-LMC holds for *vanilla* LoRA (our claim), then
CoTo-trained adapters should collapse onto `S(task)` *with strictly smaller
variance* than vanilla. CoTo therefore becomes a *prediction* of the
LoRA-LMC theory: the theory says vanilla LoRAs already collapse; CoTo's
trick squeezes the collapse tighter. This reframes the introduction from
"we differ from CoTo" to "the LoRA-LMC theory predicts the CoTo result".

**Why non-obvious.** The standard novelty defense ("measure vs promote")
admits we are doing the same kind of thing in a different mode. The
collapse-to-corroboration framing claims the LoRA-LMC theory *contains*
CoTo as a special case. That is a stronger introduction.

**Falsifier.** Train 20 CoTo-style adapters on 4 of our 8 tasks (small
add-on to the population), measure their post-π Region 2 collapse on
`G(d_task, m)`. Prediction: same `S(task)` as vanilla but tighter, AND
identical inter-task separation. If CoTo lands on a *different* `S(task)`
or has *less* between-task separation than vanilla, then CoTo is doing
something LoRA-LMC doesn't predict, and the framing reverts to plan.md's
defensive version. If predictions hold, CoTo becomes a corroborator and
the paper's contribution is sharper.

**Cost:** 20 extra LoRA training runs (~10 GPU-hours), well within the
plan's 120 GPU-hour total budget.

---

## Three more depth moves named for future iterations (not pursued today)

These follow the same pattern (named application, falsifier) but iter_003
focuses on the three above to keep the iteration scoped.

- **Move 4 — Path-vs-speed sharpens to Riemannian gradient flow on
  `G(d_task, m)`.** Replace DTW-on-scalar (current plan T2) with curve-
  alignment on the Grassmannian: same path different speed iff after
  arclength reparameterization the two curves' tangent vectors at matched
  arclengths are aligned in the Grassmannian's tangent bundle. Vector-
  valued test where DTW is scalar.
- **Move 5 — Triple signal: add per-layer α-trajectory as a third
  coordinate.** plan.md's dual signal (weights + behavior) is already
  motivated by Meynent. The α trajectory (HT-SR over training time) is a
  third coordinate WeightWatcher already produces. Triple signal R² ≥ dual
  signal R² strengthens C3.
- **Move 6 — MoTHer-ed cross-arch stretch.** Synthesis 18's "model tree
  IS the fiber bundle base manifold" gives cross-arch the right ambient
  manifold. Cross-arch trajectory comparison projects both architectures'
  trajectories into the MoTHer-recovered base before measuring `d_G`.
- **Move 7 — TRS spectrum alone as a Section 6 baseline.** (Surfaced from
  vetting BREAKTHROUGH.md's "spectrum-as-fingerprint" direction against
  plan.md's scope: not a new architecture, not Capability-Reserved
  Pretraining, so not excluded. It's a *baseline* over experiments plan.md
  already commits to.) Synthesis 19 claims TRS spectrum is a *complete
  sufficient statistic* for the task. Section 6 currently compares
  endpoint-only / endpoint+behavior / endpoint+trajectory+behavior. Add a
  fourth feature set: **TRS spectrum only** — `r × L` numbers per LoRA, no
  subspace, no behavior, no trajectory. If spectrum-only matches or beats
  endpoint full `ΔW` on mergeability / forgetting / OOD prediction, that
  is empirical confirmation of Synthesis 19 obtained as a *free corollary*
  of Section 6. If trajectory-aware features beat spectrum-only, the
  paper's headline trajectory claim is sharpened (the spectrum-as-
  sufficient-statistic story is empirically refuted *at the trajectory
  level*). Either reading strengthens the paper. Cost: zero new training;
  TRS spectra are computed for free during the existing Region-2
  extraction.

---

## Prior-art audit done this iteration

Searched arxiv with queries on: capability prediction from weights alone;
pretraining shape spectrum for adapters; task fingerprint LoRA registry;
LoRA fine-tuning trajectory phase transition mode connectivity. Pulled
PDFs (no markdown abstracts):
- `compress_then_serve_2407_00066.pdf` — joint diagonalization of 1000s of
  LoRAs into shared basis + scaling. Storage compression, not fingerprint
  registry. Strengthens Region-1 corroboration in plan.md's E1 setup.
- `tensorized_clustered_lora_2508_03999.pdf` — clusters LoRAs by tensor
  decomposition for multi-task merging. Not a trajectory paper; not a
  threat to E2.
- `future_continual_learning_foundation_2506_03320.pdf` — survey of CL +
  foundation models; mentions C-LoRA / DualLoRA / orthogonal subspaces.
  Standard prior; no architectural overlap with plan.md scope.
- `behavioral_phase_transitions_llms_2508_20015.pdf` — phase transitions in
  LLM *behavior* during LoRA fine-tuning, detected by KL between output
  distributions across checkpoints. Methodological cousin to plan.md's T1.
  **Adds depth move 2's case**: their behavioral phase detector should
  align with our weight-side `d_task` consensus phase detector at `t*`.
  If both fire at the same step, plan.md gets a *behavior-side
  corroboration* of T1 for free — citing their detector as the behavioral
  shadow of the weight-side one.

No paper found that does (LoRA + GL(r)-quotient + trajectory geometry +
LMC) as plan.md does. The novelty wedge in plan.md's Section 5 holds.

`graphify update .` ran (AST only, no LLM key in env). Semantic
re-extraction of the four new PDFs is pending and recoverable.

---

## Status check (no halt this iteration; explorer mode)

The strongest candidate the loop has surfaced (GE-LoRA-Hyper-CL) is **out
of scope for the ICLR 2027 paper** by plan.md's explicit exclusions. It
remains a strong *future-work* candidate, to be argued for in the paper's
Discussion section.

Three non-obvious deep moves *for the in-scope paper*:
- Move 1 turns Section 6's mergeability prediction into an analytic
  prediction grounded in Synthesis 16.
- Move 2 replaces Section 5's borrowed phase statistic with a LoRA-native
  one based on `d_task` estimator consensus.
- Move 3 reframes the introduction's CoTo distinction from defensive
  "measure vs promote" to "LoRA-LMC predicts CoTo as a special case".

Each move strengthens a specific section of plan.md without requiring new
training compute beyond what the plan already commits to. Each has a
named falsifier.

**Decision: continue exploring. Schedule iter_004.** The next iteration
should pick *one* of moves 4/5/6, and add at least one further non-obvious
move that none of iters 1–3 have surfaced. Halt criterion is unchanged but
the operative goal is now "make the paper land harder", not "name a new
architecture".

---

## Operational concerns logged for iter_004 (post-iteration review)

1. **Move 1 cross-dimensional subspace.** Region 2 dimension is per-LoRA
   (varies with `d_task`). Principal angles between subspaces of different
   dimensions yield only `min(d_a, d_b)` non-trivial angles. `Σ sin²(θ_i)`
   summed over different-length lists isn't comparable across 200 adapter
   pairs without a normalization choice — restrict to same-task (`d`s
   match), pad with `sin² = 1` for missing dims, or divide by
   `min(d_a, d_b)`. Each choice changes the falsifier. iter_004 picks one.
2. **Move 2 "consensus" needs a definition.** Four estimators (GELoRA,
   AlphaLoRA-α, TRS count, RLCT) agreeing "within ε" — pairwise max gap?
   std-dev across four? all four within ε of the mean? Estimators fire at
   different speeds (α likely fastest, RLCT proxy slowest), so the
   definition determines whether `t*` is dominated by the slowest or is a
   true consensus moment. iter_004 picks one explicitly.
3. **Residual prior-art risk.** iter_003 audited CoTo (Move 3) but only
   cited Spectral Edge Dynamics (2603.15678) and CopRA (2410.22911) from
   plan.md's watchlist without re-fetching them. plan.md flagged both as
   novelty risks. iter_004 fetches both and runs the same novelty
   sharpener used on CoTo.
4. **Non-obvious deep candidate for iter_004.** Under the π canonical-
   ization, weight-space lines and Grassmannian geodesics on `G(d_task, m)`
   are NOT the same curve. Frankle 2020's LMC is linear connectivity in
   weight space; plan.md asks the LoRA analog under π. Which curve is the
   right object — the linear interpolant of `(B,A)` after π, or the
   Grassmannian geodesic between Region 2 subspaces? Synthesis 16's
   triple constraint and Move 1's analytic mergeability formula both live
   on the Grassmannian; if the right object is the geodesic, Move 1
   (mergeability) and Move 4 (path-vs-speed) merge into a single
   theoretical identification of LoRA-LMC with Grassmannian geodesic
   connectivity. This is exactly the "non-obvious deep" the user
   pointed at — plan.md does not currently take a stance.

**Novelty hedge:** the claim "no paper found that does (LoRA + GL(r)-
quotient + trajectory + LMC) as plan.md does" is supported by *this
iteration's audit only* (four queries, four PDFs). The watchlist stays
live; iter_004 broadens.

---

## Stale-wakeup note (post-iteration)

A duplicate explorer-mode iter_003 wakeup, scheduled before the user's
plan.md redirect, fired late after iter_003 had already been completed in
plan.md-aligned form. Per advisor guidance, the duplicate was handled by
appending Move 7 above (the one substantive item it surfaced — TRS
spectrum-only-as-Section-6-baseline, which plan.md does not exclude) and
NOT by writing a supplement file, NOT by rescheduling, NOT by redoing
exploration. iter_004 is the next firing wakeup; the loop discipline is
preserved.
