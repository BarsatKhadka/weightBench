# Iteration 4 — 2026-05-08

**Goal this iteration (per scheduled prompt):** five deliverables, all in
plan.md scope, all without code/pseudocode. Item 1 (geodesic-vs-linear) is
the most consequential and was attacked first; if it lands, items 2 and 5
collapse partly into it.

---

## Item 1 — Geodesic-vs-linear: the corpus answers cleanly

**The question.** Under W2T's π canonicalization, what curve connects two
same-task LoRA endpoints? Frankle 2020 LMC asks for a *linear interpolant
in weight space*. plan.md asks the LoRA analog under π but does not
declare which curve (linear interpolant of `π(B,A)` vs Grassmannian
geodesic between Region 2 subspaces) is the right object.

**Real graphify queries run.** `graphify query` on (LoRA + π + linear vs
Grassmannian + mode connectivity) returned 28 nodes, including:
Synthesis 9 ("Grand Chain — Implicit Reg, BBP, Grokking as Horizontal
Subbundle Return"), Synthesis 12 (Three-Region), and the explicit node
"4. The Slow Fisher Mode Connection". The decisive content was read
directly from `synthesis_night_run_9_implicit_reg_bbp_grokking.md`
(L149–171).

**Corpus's answer.** Synthesis 9 §4 ("Slow Fisher Mode Connection")
identifies the natural metric on the LoRA parameter space as the **Fisher
information metric**. Its slow modes (low Fisher eigenvalues) are
directions near `ker(F)`, which equal directions near the horizontal
subbundle `ker(ω)` of the LoRA fiber bundle `W → W/G`. Synthesis 9 §1–§4
unifies several corpus claims:
- Nuclear-norm minimization (Gunasekar) selects the horizontal subbundle.
- Grokking = transition from vertical fiber to horizontal subbundle.
- Anti-grokking = escape from horizontal subbundle post-generalization
  (Alignment Collapse, 2602.15799).
- LLC measures horizontal subbundle proximity (Synthesis 9 §5,
  SLT/LLC community connection).

In the gauge-fixed canonical form (W2T's π), points lie on the
horizontal subbundle. The natural curve between two horizontal-subbundle
points is the **Fisher-metric geodesic on the W/G base manifold**.
Restricted to Region 2 (the Synthesis 12 / 23 "task-specific" component),
this Fisher-metric geodesic IS the **Grassmannian geodesic on
`G(d_task, m)`**. Frankle's LMC framing assumes flat ambient space (modulo
permutation); LoRA has GL(r) gauge — its ambient curves are *not*
Euclidean lines, they are Fisher / Grassmannian geodesics.

**Verdict: the corpus points to the geodesic answer.** Linear
interpolation in canonical-form weights is *not* the right object for
LoRA-LMC. The right object is the Grassmannian geodesic between Region 2
subspaces, with σ-magnitudes interpolated separately.

**Distinguishing experiment (named, no code).** For 50 same-task LoRA
endpoint pairs `(θ_a, θ_b)`:
- evaluate test loss along (i) the linear interpolation of canonical-form
  factors `(1−t)·π(θ_a) + t·π(θ_b)`, and (ii) the Grassmannian geodesic
  interpolation between Region 2 subspaces with linearly interpolated σ.
- Diagnostic: if (i) shows a barrier and (ii) doesn't, the geodesic is the
  right curve — which is what the corpus predicts. If both show no
  barrier, π canonicalization alone resolves LoRA-LMC and the geodesic
  framing is at most a notational convenience. If both show barriers,
  same-task LoRAs do not collapse and LoRA-LMC fails (publishable as a
  falsification result).

**What changes in plan.md if it is the geodesic (which the corpus
says).**
- The LoRA-LMC conjecture is restated *not* as linear connectivity but as
  **Grassmannian-geodesic connectivity**: same-task LoRAs lie inside a
  small Grassmannian ball on `G(d_task, m)`, and any pair is connected by
  a low-loss Grassmannian geodesic (with separate σ interpolation). This
  is the wedge that distinguishes from Frankle 2020 (linear).
- **Move 1 (analytic mergeability) and Move 4 (Riemannian path-vs-speed)
  fuse** into one theoretical identification: principal angles between
  Region 2 subspaces are the *coordinates* of the Grassmannian geodesic;
  the squared sum `Σ sin²(θ_i)` is the squared Grassmannian distance;
  trajectory tangent vectors are at-the-arclength-rate of that geodesic.
  Section 6 mergeability and Section 5 path-vs-speed are different
  measurements *of the same geometric object*.
- The novelty wedge sharpens: "full LMC" is a statement in a flat
  category; "LoRA-LMC under GL(r) quotient" is a statement in a
  Grassmannian / Fisher-Riemannian category. Different geometric kind.
  This is the most non-obvious lift this loop has produced for plan.md,
  and it is grounded in corpus theory the loop did not synthesize from
  imagination.

---

## Item 2 — Move 1's cross-dim handling collapses into item 1

The geodesic answer dictates the normalization:

When `d_a ≠ d_b`, the canonical Grassmannian principal-angle treatment
embeds the smaller subspace in the larger and assigns `|d_a − d_b|` extra
principal angles equal to **π/2**, contributing `sin² = 1` each. So:

> `||θ_a − θ_b||²_{Gr} = Σ_{i=1}^{max(d_a,d_b)} sin²(θ_i)` with the last
> `|d_a − d_b|` angles set to π/2.

This is **not a free pick** — it is the canonical Grassmannian principal-
angle metric for unequal-dimension subspaces. Synthesis 16 (and OPLoRA /
EBLoRA in the corpus) implicitly use this when projecting a smaller
adapter subspace against a larger pretrained subspace.

**Updated falsifier for Move 1.** Pearson r between `Σ sin²(θ_i)`
(canonical Grassmannian distance, padded as above) and post-merge
accuracy drop, on the 200 random adapter pairs. Same thresholds as
iter_003 (>0.85 wins; 0.5–0.85 strong baseline; <0.5 mechanism wrong).
The cross-dim case is now well-defined.

---

## Item 3 — Move 2 consensus definition

The four `d_task` estimators have different convergence speeds:
- α via WeightWatcher: fastest (computed per checkpoint per layer in
  closed form from the layer ESD).
- TRS count above MP: sharp once the spectrum is computed; converges as
  soon as the bulk-spike split stabilizes.
- GELoRA TwoNN: moderate, requires k-NN over activations or representation.
- RLCT proxy (Watanabe / DevInterp): slowest, needs multi-temperature
  sampling.

Synthesis 15 says all four converge on the *same* `d_task` at the
optimum. The consensus moment `t*` should therefore be defined as
**all-four-within-ε-of-their-mean**, not pairwise max gap, not std-dev:
- Pairwise max gap is dominated by the slowest estimator (RLCT) being
  far from the others; you'd be measuring "RLCT has caught up" rather
  than "all four agree".
- Std-dev across four can be small even when one estimator is
  systematically biased (three close + one offset close to the others'
  cluster boundary).
- All-four-within-ε-of-mean enforces the corpus claim that all four
  measure the *same* `d_task` once converged — and t* is the earliest step
  where that claim becomes empirically true.

**Updated falsifier for Move 2.** Define `t*` per LoRA as the smallest
step at which all four estimators are within ε = 0.5 of their mean (ε is
in d_task units; d_task is integer-ish so 0.5 is roughly "all four
estimators rounded to the same integer"). Then check whether `t*` lands
inside the convex hull of phase-transition steps detected by Schürholt's
borrowed full-network statistic. If yes, the LoRA-native phase detector
replaces the borrowed one; if no, the corpus's claim that all four
estimators measure the same `d_task` is empirically refuted at the
trajectory level (also a finding).

---

## Item 4 — Novelty audit: Spectral Edge Dynamics + CopRA

Both PDFs fetched fresh, both read methods sections directly (not just
abstracts). No markdown abstracts written.

**Spectral Edge Dynamics (Xu, 2603.15678, Mar 2026).** Operates on
*full-network* parameter deltas `δ_t = θ_{t+1} − θ_t`. Builds rolling-
window trajectory matrix, Gram matrix `XX^T`, computes spectral edge
ratio `σ_k/σ_{k+1}`. Tested on TinyStories 51M and GPT-2 124M trained
from scratch. Three-phase pattern (rise, plateau, collapse), distribution-
shift detection, Johnson-Lindenstrauss scaling.
- **NOT on LoRA factors.** No GL(r) quotient, no canonicalization, no
  Region 2 / Grassmannian. Their `δ_t` is the entire model's parameter
  delta, not `(B,A)` factor deltas.
- **Methodological cousin** to plan.md's E2 rolling-window analysis,
  exactly as plan.md's reading list already names.
- **Free corroborator** of plan.md's RMT-based three-region story (BBP
  phase transition) and the universal three-phase pattern in trajectories
  generally.
- **Does not preempt** plan.md's contribution: LoRA-LMC under GL(r)
  quotient + trajectory geometry on `G(d_task, m)` is a different object.
- One borrowable artifact for plan.md: their Property 4 (distribution-
  shift detection within `O(W)` steps via spectral edge change). When
  ported to π-canonicalized LoRA rolling deltas, this becomes an *anti-
  grokking detector* — see Item 5 / Move 8 below.

**CopRA (Zhuang et al., 2410.22911, Oct 2024).** Progressive LoRA
training strategy with random adapter dropping (Bernoulli probability
that grows over training). Goal: produce LoRAs that exhibit linear mode
connectivity for fusion / federated learning / multi-task merging.
- *Older twin of CoTo* (CoTo is 2506.05713). Same family: training-time
  intervention to *promote* LMC.
- They also propose **LoRA Align (LA)**: minimize a fusion-vs-mixture
  upper bound by fitting an invertible matrix `P` so that `(B_2 P,
  P^{-1} A_2)` aligns with `(B_1, A_1)`. This is exactly a GL(r) gauge
  alignment, but applied **pairwise at merge time** rather than as a
  global canonicalization at measurement time.
- **Does not do trajectory geometry.** Endpoints only.
- **Does not preempt** plan.md's E2: training intervention vs.
  measurement of vanilla LoRA trajectory geometry.
- **Reframes under iter_003 Move 3.** The Move 3 reframe ("CoTo as
  corroborator, not competitor") extends to CopRA: under the LoRA-LMC
  geodesic statement (item 1 above), CopRA's claim "LoRA training can be
  made LMC" is *predicted* by the theory — same `S(task)` collapse,
  tighter variance under their dropping schedule. Both watchlist papers
  are corroborators under the geodesic framing.
- **Direct citation in plan.md's Section 3 (Method).** CopRA-LA is the
  closest published cousin to W2T's π canonicalization for the
  *merge-time* case. plan.md should cite CopRA-LA when introducing π:
  "Where CopRA aligns two LoRAs by fitting a per-pair invertible `P`,
  we apply W2T's global gauge fix π once and measure all LoRAs in the
  shared canonical form."

**Conclusion.** Both named threats in plan.md's risk row are confirmed
*not* preemptive on the audited reading. The watchlist remains live;
recommend a recurring weekly arXiv alert on `LoRA + trajectory +
Grassmannian` (per plan.md's own risk-mitigation note).

---

## Item 5 — Move 8: anti-grokking detection from post-π trajectory drift

**The bar this must clear.** "Triple signal by adding α-trajectory" was
in iter_003's parking lot. Move 8 must be substantively deeper than
that — i.e., add a *new prediction target*, not just a new feature.

**The move.** Synthesis 9 §3 + the Alignment Collapse quartic law
(2602.15799) predict that LoRA trajectories trained past the optimum
exhibit **anti-grokking**: they leave the horizontal subbundle, drifting
from `S(task)` into intruder-dim directions. Under the geodesic answer
to Item 1, this manifests as a measurable signal in the trajectory: the
post-π canonical Region 2 subspace at checkpoint `t` *moves away from*
its centroid `S(task)` after some `t_anti > t*`. Three immediate consequences:
- The signal is **weight-only** — no held-out evaluation needed to
  detect overtraining.
- It is a **trajectory** signal — endpoint analysis cannot recover it
  (the endpoint just looks "off-task" without knowing whether it was
  ever on-task).
- It generates a **new Section 6 prediction target**: "did this LoRA
  overtrain?" detected from weights alone. Adds to mergeability,
  forgetting, OOD generalization.

**Where in plan.md.** Section 6 currently has three downstream prediction
targets (mergeability, forgetting, OOD). Move 8 adds a fourth:
**anti-grokking / overtraining detection**. plan.md's Section 5 already
saves checkpoints every 50 steps; the additional measurement is just
`d_G(checkpoint_t, S(task))` after `t*` (the consensus phase-transition
moment from Move 2). If this signal goes nonzero past `t*`, the LoRA is
overtrained. Falsifier: does this weight-only signal correlate with
held-out forgetting beyond what endpoint forgetting alone explains?

**Why non-obvious.** plan.md's risk row mentions anti-grokking only as
"trajectory looks identical across all runs". The *opposite* is also a
finding: trajectories that come back out of `S(task)` after entering it
are diagnostically rich. The Alignment Collapse paper (2602.15799) is in
the corpus but plan.md does not currently use it as a Section 6 target.

**Cost.** Zero new training: anti-grokking can be detected on the same
200 LoRAs, same checkpoints. The new measurement is `d_G(checkpoint_t,
centroid)` over `t > t*` per LoRA, computed for free during Region 2
extraction.

**Connections back into the framework.**
- Move 1's `Σ sin²(θ_i)` formula reapplied: `d_G(checkpoint_t, centroid)
  = Σ sin²(θ_i)`. Anti-grokking detection IS a per-checkpoint application
  of the analytic mergeability instrument.
- Move 2's `t*` defines the start of the anti-grokking window: anti-
  grokking can only be diagnosed after the four estimators have agreed
  on `d_task` (otherwise `S(task)` itself is undefined).
- Move 7's spectrum-only baseline can be evaluated on the same target:
  does the TRS spectrum alone predict anti-grokking, or does the
  trajectory-level subspace drift carry information the spectrum
  doesn't?

The geodesic answer (item 1) makes Moves 1, 2, 7, and 8 facets of one
geometric object: the Grassmannian distance. plan.md gains a unified
measurement instrument used across Sections 5 and 6.

---

## What this iteration leaves for iter_005

- **One** of moves 4 (Riemannian path-vs-speed sharpening) or 5 (α-
  trajectory triple signal) — both are now refinements *within* the
  geodesic frame. Pick one and write it up.
- **The Fisher-metric trajectory speed candidate** (LLC anti-correlated):
  candidate Move 9, mentioned but not pursued. Worth a graphify query
  next iteration.
- **Continue the watchlist.** Spectral Edge Dynamics + CopRA cleared
  this round; iter_005 should sweep arxiv once more for "LoRA trajectory"
  or "GL(r) quotient" papers in 2026.
