# Iteration 6 — 2026-05-08

**Discipline:** tighter still. One Move (corpus-forced, not parking-lot
default), one fallback resolution, one cost fix, one watchlist sweep.
Scientist phase: no code, no pseudocode, no halt declarations.

---

## 1. Move 5 — Karcher / Fréchet mean as `S(task)`

**Question entering iteration:** does the geodesic frame *force* a next
move other than the parking-lot α-trajectory?

**Real graphify queries run.** `graphify query` on (Karcher mean / Fréchet
mean / Grassmannian centroid for same-task LoRAs) returned 24 nodes,
including a decisive hit: **Synthesis 8 §3 — "Fréchet Averages:
Independent Confirmation of W/G from Model Merging"**, citing
**da Silva et al. (2604.27155, "Generalizing the Geometry of Model
Merging Through Fréchet Averages")**. Direct read of synthesis_night_run
_8_mechanistic_intruder_dims.md L119–155.

**Corpus's answer — decisive.** da Silva et al. prove that LoRA model
merging IS Fréchet averaging on the quotient manifold `W/GL_r`, and that
**Fisher merging = Fréchet average under the Fisher metric on `W/G`**.
This is exactly iter_004 §1's geodesic identification, derived
independently from a different motivation (model merging theory, not
fiber bundle theory). The corpus thus *forces* the centroid object on
`G(d_task, m)` to be the Fréchet/Karcher mean (the point minimizing sum
of squared Grassmannian distances), not the Euclidean mean.

**The depth move.** plan.md E1 (Section 4) currently treats `S(task)`
as the empirical *Euclidean* mean of canonical-form Region 2 subspaces.
Under the geodesic frame plus the Fréchet-average identification, the
correct centroid is the **Karcher mean on `G(d_task, m)`**: the unique
(within injectivity radius) minimizer of `Σ_i d_G²(L_i, S(task))` over
points `S(task) ∈ G(d_task, m)`.

Two operational consequences plan.md does not currently have:
1. **Within-task collapse measurement (C1) is biased by the wrong mean.**
   Euclidean mean of subspaces is not even a subspace in general — it
   is an arbitrary point in the ambient `R^{m×d_task}`, then
   re-orthogonalized at best. The Karcher mean stays on the manifold
   and minimizes the *Grassmannian* sum-of-squares — the natural
   loss for "how tight is the cluster of same-task LoRAs?". Reporting
   tight collapse with the Euclidean mean while the Karcher-mean radius
   is large is a Type-I error against LoRA-LMC; reporting loose collapse
   with the Euclidean mean while the Karcher-mean radius is small is a
   Type-II error.
2. **C3 (dual signal) becomes unconfounded by metric choice.** Under the
   Karcher mean, the C1 within-task radius and the Section 6 mergeability
   formula are both squared-Grassmannian quantities, *measured by the
   same instrument as Move 4's matched-arclength tangent overlap*. The
   geodesic frame promotes one geometric instrument across Sections 4,
   5, and 6.

**Falsifier.** For the 200-LoRA population, compute both centroids per
task: `S_euc(task) = empirical Euclidean mean of canonical Region 2
factors` and `S_karch(task) = Karcher mean on G(d_task, m)`. Then:
- The Karcher and Euclidean means agree (within the injectivity radius)
  iff same-task subspaces are tightly clustered — i.e., the cluster
  radius is small in the canonical Grassmannian metric.
- If they disagree materially (≥ ε in Grassmannian distance, ε to be
  set as a fraction of typical inter-task `d_G`), then C1 measurements
  with the Euclidean mean are biased and the paper must report Karcher
  results.
- **Headline falsifier for Move 5:** report C1 same-task vs different-
  task `d_G` ratio under both centroids. If the ratio survives the
  Karcher correction with > 5σ separation, the LoRA-LMC claim is
  robust to the centroid choice (good for the paper). If the ratio
  collapses, the original C1 is an artifact of the wrong mean (also a
  finding — explicitly publishable as "LoRA-LMC fails under the
  geometrically correct centroid"; would be a falsification result for
  the conjecture itself).
- **Regime caveat (asymmetric claim).** The Karcher-vs-Euclidean
  discrimination is informative only in the *moderate-spread* regime.
  For very tight same-task clusters (within injectivity radius, small
  `d_G`), the two means agree to high order by the manifold's local
  Euclidean structure — that's geometry, not evidence about LoRA-LMC.
  In that regime the Move 5 result reads "Karcher confirms Euclidean
  was good enough", which is a finding (centroid choice is a
  measurement no-op for tight clusters) but not the headline. The
  paper should report cluster-radius statistics first, then read the
  Karcher comparison conditional on that regime.

**Cost.** Zero new training. Karcher mean on `G(d_task, m)` is a few
iterations of Riemannian gradient descent on saved Region 2 subspaces
(closed-form retraction on the Grassmannian, ~milliseconds per task
per layer at SD-LLM scale). CPU only.

**Connection back into the framework.**
- Move 1's mergeability formula `Σ sin²(θ_i)` between two adapter
  Region 2 subspaces is *exactly* the squared Grassmannian distance
  the Karcher mean minimizes. M5 and M1 are facets of one object.
- Move 4's matched-arclength tangent overlap can be measured against
  the Karcher-mean's geodesic structure rather than the Euclidean
  centroid's — the same vector-valued test, now metric-consistent.
- Move 8's anti-grokking detector measures `d_G(checkpoint_t, S(task))`;
  using the Karcher mean for `S(task)` makes the drift signal
  geometrically meaningful rather than artifactual.

This is the most non-obvious depth move iter_006 surfaces because it
*invalidates* a measurement plan.md currently takes for granted (the
empirical mean of subspaces) and replaces it with a corpus-forced
correct one (the Karcher mean from Synthesis 8 §3 / da Silva
2604.27155). The α-trajectory parking-lot move would have been
incremental; this is structural.

---

## 2. Move 8 t* fallback — drop LoRAs without four-estimator consensus

**Three options enumerated in iter_005 §3.2:**
- (1) Drop those LoRAs from Move 8 evaluation.
- (2) 3-of-4 consensus dropping RLCT proxy.
- (3) α-plateau as `t*` with endpoint consistency check.

**Default suggested in iter_005:** option (2). On corpus-grounded
review, that default is *wrong*. Switch to **option (1): drop**.

**Corpus-grounded justification.** Synthesis 9 §5 says explicitly:
> *LLC measures horizontal subbundle proximity. Low LLC = near ker(ω) =
> generalization basin.*

RLCT proxy (the slowest estimator) is precisely the SLT quantity that
identifies the singular basin. If RLCT does not converge inside the
training horizon for a particular LoRA, that LoRA *has not reached a
generalization basin in the SLT sense*. Move 8's anti-grokking premise
("post-π drift away from `S(task)`") presumes a generalizing `S(task)`
exists — a low-LLC, horizontal-subbundle-anchored point. If RLCT proxy
hasn't converged, that anchor doesn't exist. 3-of-4 consensus would
declare `t*` based on the three faster estimators having stabilized,
producing a *fake* `S(task)` for a LoRA still in the vertical fiber of
the bundle — and Move 8's drift signal would be polluted (drift from a
non-anchor is meaningless).

Dropping such LoRAs is the only corpus-consistent choice. The cost is
sample size, not validity. Synthesis 9's "horizontal subbundle = ker(ω)
= generalization" identification is load-bearing for the whole frame.

**Updated falsifier for Move 8.** The 200-LoRA population has 4
estimators × 30 checkpoints per LoRA. Define `t*` as the smallest step
where all four are within ε ≈ 0.5 of mean. For LoRAs without such a
step (RLCT did not converge), Move 8 is undefined and they are excluded
from the anti-grokking analysis. Report the exclusion fraction; if it
exceeds 30%, plan.md's training horizon is too short for the SLT-LLC
machinery and the budget needs longer runs (separate concern, separate
paper).

---

## 3. Move 9-restricted cost fix — over-trained subset comes for free

**iter_005's accounting missed extra training cost** for "deliberately
overtraining 25 LoRAs." This was overcounted: plan.md's planned
population is 8 tasks × 5 seeds × 5 schedule/LR variations = 200 LoRAs,
sweeping LR ∈ {high, mid, low} × schedule ∈ {short, mid, long, mid+wd, no-wd}.
Some of these combinations will, by construction, run past their
optimum (long schedule + high LR; no-weight-decay variants per Synthesis
9 §3 prediction). Selecting *post-hoc* the 25 LoRAs whose held-out
accuracy peaked early then degraded gives the over-trained subset
**for free** — no additional training compute.

**Corrected Move 9-restricted cost: ~17 GPU-hours** (LLC SGLD only,
unchanged). The over-trained subset is selected from existing
checkpoints rather than separately trained. Move 9-restricted stays
within budget; iter_005 §2's parking decision for full-form Move 9
stands.

---

## 4. Watchlist sweep — RiemannLoRA fetched

Searched arxiv for `LoRA Karcher mean Fréchet Grassmannian Riemannian
center mass`. Surfaced three relevant items (one PDF max fetched):
- **Fréchet Averages (2604.27155)** — already in corpus (Synthesis 8 §3).
- **Scales of Fréchet means and Karcher quasi-arithmetic means
  (2511.21173)** — pure differential-geometry paper, not LoRA. Skip.
- **RiemannLoRA — LoRA meets Riemannion (2507.12142, Oct 2025).**
  Fetched `riemann_lora_2507_12142.pdf`. Read pp. 1–3.

**RiemannLoRA reading.** Bogachev et al. parametrize LoRA as direct
optimization on the **fixed-rank matrix manifold** `M_r = {X ∈ R^{m×n} :
rank(X) = r}` — i.e., they train `ΔW` directly without ever forming the
ambiguous `(B, A)` factorization. Propose "Riemannion," a Muon-style
optimizer ported to `M_r`. Show convergence-speed and final-task gains
on LLM and diffusion fine-tuning.

**What RiemannLoRA does:** training-time gauge fix (optimize on the
quotient manifold directly, never see the GL(r) ambiguity).
**What it does NOT do:** trajectory geometry, within-task collapse, mode
connectivity, Grassmannian distance for analysis. They are an
*optimizer*, not a measurement instrument.

**Conclusion — sibling, not preemption.** plan.md's gauge-fix story now
has *four* siblings at different temporal scopes, all confirming the
W/G quotient is the right object:

| Paper | Scope | Mechanism |
|---|---|---|
| RiemannLoRA (2507.12142) | training time | optimize directly on `M_r` |
| W2T / plan.md π (2603.15990) | measurement time | QR + SVD canonical |
| CopRA-LA (2410.22911) | merge time | learn invertible `P` per pair |
| FLoRG (2602.17095) | federated-merge time | Procrustes alignment |
| Fréchet Averages (2604.27155) | merge / averaging | Fréchet mean on `W/G` |

This convergence is *itself a paper-level result*: five independent
papers across four different temporal scopes of the LoRA pipeline have,
without coordination, derived the same geometric object. plan.md
absorbs this as a Section 2 (Background) framing — the W/G quotient is
not a stylistic choice; it is the empirically convergent right answer.

---

## 5. Queued plan.md absorption pass — now eight edits, prioritize

iter_005 §5 listed seven edits. iter_006 adds an eighth (the four-
sibling table above) and tightens one (Move 5 / Karcher mean):

**The eight edits queued for iter_007 OR 008:**
1. **Section 1 + Section 5:** restate LoRA-LMC as Grassmannian-geodesic
   connectivity (iter_004 §1). Sharpens novelty wedge.
2. **Section 2 (Background) NEW SUBSECTION:** "The W/G quotient as the
   empirically convergent right object" — present the four-siblings
   table, framing it as why our measurement-time choice is robust.
3. **Section 3 (Method):** cite CopRA-LA + FLoRG + RiemannLoRA when
   introducing π. Three-siblings citation, not just two.
4. **Section 4 (E1):** swap Euclidean mean for Karcher mean as
   `S(task)`; report C1 ratio under both. Move 5 above.
5. **Section 5 (E2), T1:** four-estimator consensus `t*` with
   all-four-within-ε-of-mean (iter_004 §3) replaces Schürholt's
   borrowed full-network statistic.
6. **Section 5 (E2), T2:** matched-arclength tangent overlap
   (operational, no parallel transport) replaces DTW-on-scalar. Move 4.
7. **Section 6:** four downstream targets become five — add Move 7
   (TRS-spectrum-only baseline) and Move 8 (anti-grokking detector
   from post-π drift past `t*`, with drop fallback for non-converged-
   RLCT LoRAs from §2 above).
8. **Section 6, Target 1:** restate mergeability as analytic
   `Σ sin²(θ_i)` formula with two scalar coefficients fitted (Move 1)
   — theorem-with-empirical-confirmation.

iter_006 has now produced two iterations' worth of unabsorbed edits.
**Recommend iter_007 BE the absorption pass.** It is a focused turn
that touches plan.md and only plan.md, applying edits 1–8 in one
coherent edit, with no new exploration. After iter_007 the loop returns
to iter_NNN.md exploration in iter_008+.

---

## What iter_007 should do

**Absorption pass.** Open `plan.md`, apply edits 1–8 in one coherent
revision, commit nothing controversial that wasn't surfaced in iter_001
through iter_006. No new exploration this iteration; tight discipline.
Do call advisor at start (this is a high-leverage edit and worth
checking the order/wording before touching the canonical document).
After absorption, re-read plan.md end-to-end and verify nothing in the
"What I Will Not Do This Year" section has been violated by the edits.
Schedule iter_008 to resume exploration.
