# Iteration 8 — 2026-05-09

**Discipline:** structural search — find an area A1–A9 doesn't touch.
plan.md untouched. BREAKTHROUGH.md is the running catalog. No code, no
pseudocode, no halt declarations. No AskUserQuestion about plan.md.

---

## Two candidate territories explored via real graphify queries

**Territory 1: Cross-architecture stretch + MoTHer.** `graphify query` on
"Cross-architecture LoRA transfer + MoTHer model tree + Region 2 transfer"
returned 21 nodes anchored on **Synthesis 18 ("The Model Tree IS the
Fiber Bundle Base Manifold")** — degree-6 node with rich subsections
(Geometric Identification, Distances on Model Manifold, Isotropic
Merging Perspective, Specialization Stage Paradox Resolved, Complete
Geometry Summary). Direct read of
`synthesis_night_run_18_model_tree_fiber_bundle_base_manifold.md`.

**Territory 2: Section 7 / agent-vision priors.** `graphify query` on
"TeleLoRA + ProbeLog + capability prediction + agent-side priors" returned
17 nodes mostly anchored on `experiment_design_reference_frame_measurement.md`
(an existing experiment design) and `some_insights_lora_papers.md`.
`graphify explain "TeleLoRA"` and `graphify explain "ProbeLog"` confirmed
both papers exist as graph nodes but with **degree 1** each — sparsely
connected stubs. Synthesis 18 has degree 6.

**Verdict — Territory 1 wins decisively.** The corpus has substantively
developed the cross-arch geometric handle (Synthesis 18 is a complete
section); the agent-vision priors are name-checked but not connected.
Pursuing Territory 2 would force forced-novelty work; Territory 1 has
real corpus material.

---

## A10 — Cross-architecture LoRA-LMC via Cross-LoRA's `ρ_AB` + the model tree as one base manifold

### What it claims

plan.md's stretch goal (T_cross-arch) names an **architecture-quotient
`ρ`** that aligns `S(task)` across base models without specifying its
construction. Two corpus inputs combined this iteration:

1. **Synthesis 18 / MoTHer** — the model tree of LLM lineage IS the
   base manifold `W/G` of the LoRA fiber bundle. Different base models
   (LLaMA, Mistral, Qwen, Gemma) are different *points* on the same
   manifold; lineage edges are geodesics; tangent spaces at different
   nodes are the local coordinate systems where a LoRA's Region 2
   lives.
2. **Cross-LoRA — Xia et al. 2508.05232** (fetched this iteration). Their
   "LoRA-Align" component constructs `ρ` *concretely*: rank-truncated
   SVDs of source and target base weights `W_s ≈ U_s Σ_s V_s^T` and
   `W_t ≈ U_t Σ_t V_t^T`, then **Frobenius-optimal linear transforms**
   `P̂_U = arg min ‖P U_s − U_t‖_F²` and `P̂_V = arg min ‖P V_s − V_t‖_F²`.
   These admit closed-form least-squares solutions; the aligned bases
   are `Ũ_s = P̂_U U_s` and `Ṽ_s = P̂_V V_s`. Cross-LoRA shows up to
   5.26% gain on ARC / OBQA / HellaSwag transferring LoRAs across
   LLaMA-3.2-3B, Qwen2.5-1.5B, Qwen2.5-5B, Gemma-2-2B.

The synthesis: Cross-LoRA provides empirical construction of `ρ_AB`,
the linear change-of-coordinates between tangent spaces at two model-
tree nodes A and B. Synthesis 18 provides the geometric reading: this
ρ_AB *should* exist if the model tree is one connected base manifold,
and same-task LoRAs *should* match across bases after applying it.
plan.md's stretch becomes:

**Cross-arch LoRA-LMC holds iff, after applying Cross-LoRA's `ρ_AB`,
same-task LoRAs from base A and base B collapse onto the same
Grassmannian ball on `G(d_task, m)` with the same `d_task` and the
same Karcher centroid (per A5, modulo ρ_AB's image).**

This is non-obvious because:
- plan.md treats `ρ` as a vague architecture quotient to be invented.
  Cross-LoRA *constructs* it from base-weight SVDs alone, no training.
- Cross-LoRA's paper measures **transfer accuracy**, not subspace
  collapse. They show transferred LoRAs *work* on the target — they
  don't measure whether same-task LoRAs across bases share a subspace.
  The geometric prediction has not been empirically tested.
- If the prediction holds, the model tree's "single connected base
  manifold" identification of Synthesis 18 gets first empirical
  confirmation at the cross-base-model level (it's currently
  established only for same-base lineage).

### What it would change in plan.md (if promoted — do not promote)

- Section 5 stretch (T_cross-arch). Currently: "There exists an
  architecture-quotient `ρ` that aligns `S(task)` across base models."
  Promoted version: "Apply Cross-LoRA's LoRA-Align construction as
  `ρ_AB` between any two base models in the population; test
  within-task vs between-task `d_G` post-ρ on `G(d_task, m)`."
- Section 2 / Background (related work). Cite Cross-LoRA (2508.05232)
  alongside CopRA-LA, FLoRG, RiemannLoRA in the four-temporal-scopes
  table — Cross-LoRA is a fifth scope (cross-base-model-transfer time)
  that Section C of BREAKTHROUGH.md doesn't yet name.

### Falsifier (named experiment, no code, no parameter counts)

For each of 4 plan.md tasks (subset of the 8), train 2 same-task LoRAs
each on 2 base models (LLaMA-3-8B and Qwen2.5-3B, or any adjacent pair
in the model tree). Total: 4 × 2 × 2 = 16 LoRAs, each ~1 GPU-hour =
~16 GPU-hours of stretch compute. Sits within plan.md's existing
cross-arch stretch budget.

For each LoRA, compute the canonical-form Region 2 subspace per layer
in its own base-model coordinates. For each base pair (A, B), apply
Cross-LoRA's LoRA-Align to bring all Region 2 subspaces into a common
target-coordinate space. Then measure:
- **Same-task post-ρ `d_G`** between LoRA-on-A and LoRA-on-B (4 pairs
  per task × 4 tasks = 16 pairs).
- **Different-task post-ρ `d_G`** between LoRA-on-A-task-i and
  LoRA-on-B-task-j (12 pairs per task = 48 pairs).

Headline test: same-task post-ρ d_G < different-task post-ρ d_G with
≥ 3σ separation. (Stretch threshold is weaker than within-base 5σ
because cross-base alignment is empirically harder.)

Three readings:
- Pass: cross-arch LoRA-LMC holds; the model tree is one connected
  base manifold for `S(task)` purposes; Cross-LoRA's `ρ` is the
  empirical realization. Section 5 stretch lands cleanly.
- Pass with caveat (separation < 3σ but mean still ordered): cross-
  arch holds in expectation but with high variance — discussion-section
  open question.
- Fail (no separation, or order reversed): the model tree is not a
  single manifold for `S(task)`, OR Cross-LoRA's `ρ` is empirically
  task-dependent (not architecture-intrinsic), OR LoRA-LMC fails
  cross-arch. Each case is a publishable finding.

### Status

**Strong candidate.** Two corpus inputs (Synthesis 18 + Cross-LoRA
2508.05232) combine into a concrete depth move. ρ is no longer a
vague invented map but a specific data-free linear construction. Cost
sits in plan.md's existing stretch budget. Falsifier is metric-natural
under iter_004's geodesic frame and uses iter_006's Karcher centroid.
Connects through to A1 (analytic mergeability via principal angles)
and A4 (matched-arclength tangent overlap) — same Grassmannian-distance
instrument applied across base-model boundary.

### Connections to existing A-section findings

- **A5 (Karcher mean)** is the right centroid to use *within each base
  model's coordinates* before applying `ρ`; `ρ` then maps centroids,
  and post-ρ Karcher means are compared.
- **A1 (analytic mergeability)** extends to cross-base mergeability:
  predict post-merge accuracy of LoRA(task, base A) merged into base B
  from `Σ sin²(θ_i)` between Region 2 subspaces *after applying `ρ_AB`*.
  Free corollary of A10 if A1 is also tested in stretch.
- **A4 (path-vs-speed tangent overlap)** at trajectory level extends to
  cross-base trajectories: do same-task LoRAs on different bases
  trace *the same path* on `G(d_task, m)` post-ρ, just at different
  speeds determined by base-model size?

A10 promotes the model tree from a structural metaphor (Synthesis 18) to
an empirically falsifiable invariance claim about same-task LoRAs across
the LLM lineage.

---

## Watchlist sweep — Cross-LoRA fetched, graph updated

Searched arxiv: "cross-architecture LoRA transfer base model TeleLoRA
LLaMA Mistral Qwen task subspace alignment."

- **Cross-LoRA (2508.05232)** — fetched this iteration. Direct depth-move
  enabler. Now in `finding_literature/cross_lora_data_free_transfer_2508_05232.pdf`.
- **TeleLoRA (2503.20228)** — was already in graph as `arxiv_2503_20228.md`
  stub (degree 1). Worth fetching the actual PDF in a future iteration to
  upgrade the stub to a fully-extracted node.
- **tLoRA (2602.07263)** — multi-LoRA training with elastic shared
  super-models. Different problem (efficiency, not cross-base transfer).
  Skip.
- **LoRA-X (Farhadzadeh 2025a)** and **ProLoRA (Farhadzadeh 2025b)** —
  named in Cross-LoRA's related work as subspace-constrained
  alternatives. Diffusion-model focus mostly. Worth a future targeted
  pull only if A10 promoted to plan.md.

`graphify update .` ran post-Cross-LoRA fetch. Graph: 1989 nodes / 2122
edges / **179 communities** (was 178 — Cross-LoRA's PDF added one
community). All 14 PDFs added across iterations 4–8 are now AST-indexed.

---

## What iter_009 should do

iter_008 produced one tight A-section finding (A10) by structural search.
The pattern works. iter_009 should:
- Pick a second territory A1–A9 doesn't touch. Two candidates the queries
  surfaced but did not develop:
  - **The `experiment_design_reference_frame_measurement.md` node** —
    appears in both Territory 1 and Territory 2 query results. It's
    an existing experiment plan in the corpus. Worth reading directly
    to see what depth move it enables that A1–A9 don't.
  - **Section 7 agent vision** revisited with sharper queries. The
    Territory 2 result was sparse but the failure could be query
    framing, not corpus emptiness. Try `graphify path` between
    "trajectory geometry" and "self-evolving agent" or between
    "capability prediction" and "agent-side priors."
- One arxiv watchlist sweep with new query terms.
- No plan.md edits; consolidate into BREAKTHROUGH.md Section A as A11.
