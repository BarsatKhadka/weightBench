# Running Findings Catalog (BREAKTHROUGH.md)

**Date:** 2026-05-09
**Discipline:** plan.md is canonical and untouched by the loop. This file is
the running summary of findings the loop has produced. The user reviews this
to decide what (if anything) to promote into plan.md. The loop does not
initiate plan.md edits; it accumulates findings here.

Each finding is structured: **what it claims**, **what plan.md section it
would change if promoted**, **falsifier**, **status** (proposal /
candidate / strong / corrobor­ated by N corpus papers).

---

## Section A — Depth moves for the in-scope ICLR 2027 paper

These are findings that would *strengthen* the existing plan.md without
adding new architecture / new compute / theoretical proof.

### Thematic index (added iter_013 — chronological order in entries below)

After 14 entries, the catalog has converged on five thematic clusters
plus two singletons. Each cluster's findings share a measurement
instrument or theoretical framework. Dependency arrows mean *upstream
finding conditions or sharpens downstream finding*; "↔" means *audit
pair*; "≡" means *same instrument under a different motivation*.

**1. Foundational triad (theoretical anchor).**
The theorem-sketch and its applicability audits.
- **A12** (CORE_CLAIM theorem-sketch: Grassmannian + Fisher-Rao + TRS = unique invariant task distance, given assumptions)
- **A11** ↔ **A13** (foundation-1 audit pair: A11 signal-side, A13 noise-side; together stress-test Johnstone-Paul spiked covariance)
- **A14** (foundation-3 framework: Fisher non-degeneracy fails generically; SLT/LLC handles)
- **Promotion calibration:** if A11/A13/A14 all promoted, the composed framework is PIGMM + GL_r + SLT, which gives free-energy asymptotics rather than the Cencov-style uniqueness CORE_CLAIM cites. Acknowledge in promotion language.

**2. Grassmannian-instrument cluster (operational measurements).**
All inherit Cencov-uniqueness from A12; all on the same `G(d_task, m)`.
- **A1** (analytic mergeability via `Σ sin²(θ_i)` with sin²=1 padding for cross-dim)
- **A4** (matched-arclength tangent-subspace overlap, no parallel transport)
- **A5** (Karcher / Fréchet mean as `S(task)` centroid, vs Euclidean mean — regime caveat in moderate-spread case)
- **A6** (LoRA-LMC restated as Grassmannian-geodesic connectivity — the *category* shift Frankle-LMC misses)
- A1 ≡ squared Grassmannian distance; A4 ≡ tangent of the geodesic A1 measures; A5 ≡ centroid the Grassmannian metric minimizes; A6 ≡ the geometric category all four live in.
- **A1 ↔ A5 unifier (added iter_015 from A15).** Rahamim et al.'s "mergeability is a local trait of the LoRA" finding predicts that A1's pair formula `Σ sin²(θ_i)(L_i, L_j)` averaged over `j` reduces to L_i's mean-squared-Grassmannian-distance to its task neighbors — which IS A5's Karcher-distance-to-centroid up to a factor. If empirically confirmed (A15 falsifier F2), A1 and A5 unify at the per-LoRA level and cluster 2 has *one* per-LoRA scalar (Karcher distance) plus *one* pair instrument (principal-angle sum) reading the same geometric object.
- **Cluster-2 methodological refinements (added iter_014 from `some_insights_lora_papers.md`).** The Grassmannian instrument is well-defined whether read from full ΔW = BA or from B-only. Four refinements that sharpen E1's setup without changing the cluster-2 instruments:
  - **B-only coordinate when A is fixed-init across the population.** AsymmetryOfLoRA finding: B clusters by task, A doesn't. Under fixed A init (the default for plan.md's controlled population), variance is concentrated in B; using B-only or B's singular value spectrum gives a cleaner read than full ΔW = BA without changing the geometry.
  - **Three-metric ablation in Methods section** (raw Euclidean / GL_r-invariant / O(r)-invariant). plan.md's Method already commits to GL_r-invariant via π. Reporting the three-metric ablation makes it a *demonstrated* methodological choice rather than an asserted one — strengthens A12's uniqueness narrative empirically.
  - **Effective rank as covariate.** AdaLoRA finding: nominal rank r ≠ effective rank (singular values above ε threshold). Two LoRAs at nominal rank 16 may use very different effective ranks. Reporting effective-rank-controlled results disambiguates "same parameterization" from "same information content" — matters for A1's mergeability prediction.
  - **Layer-grouped representation (bottom/mid/top).** AdaLoRA + AsymmetryOfLoRA agreement: FFN layers > attention layers; top layers > bottom layers in task-specific signal density. Layer-grouped reads sharpen task clustering at the cost of presentation density. Useful as an ablation in E1, not a primary instrument.

  These are *methodological refinements*, not new findings — they sharpen how cluster-2 instruments get computed, not what they measure. None is A-section sized.

**3. Trajectory-time cluster.**
Phase-transition + drift detection; uses A1's instrument over time.
- **A2** (consensus `t*` from four `d_task` estimators: GELoRA-TwoNN, α via WeightWatcher, TRS-MP-count, RLCT proxy)
- **A8** (anti-grokking detector: post-π drift away from `S(task)` past `t*`)
- **A2 → A8** (A8 needs `t*` to define the window).
- **A14 → A2** (RLCT-proxy as foundation-3 signature; consensus interpretation under SLT.)

**4. Cross-architecture (singleton + corpus tie-back).**
- **A10** (Cross-LoRA's `ρ_AB` as concrete construction of plan.md's vague architecture-quotient `ρ`).
- **A10 ≡ A12 anchor experiment** under different motivation. Same falsifier (~16 GPU-hours stretch).
- *Failure-mode note (iter_013 search):* the architecture-similarity effect (Community 15) — Cross-LoRA's own paper finds weaker gains when source/target architectural primitives differ (e.g., Gemma's MHA+GeLU vs LLaMA's GQA+SwiGLU). A10's falsifier should report architecture-pair-specific results, not aggregate.

**5. Cheap baselines.**
Auxiliary tests at zero or low extra compute.
- **A7** (TRS-spectrum-only as a fourth feature set in Section 6 — empirical test of Synthesis 19's sufficient-statistic claim)
- **A9** (LLC at endpoints, ~17 GPU-hours, 50-LoRA subset — Move 9-restricted; A9 ≡ A14's empirical signature)

**6. Application cluster (singleton, structurally distinct).**
Pulls instruments from clusters 1–5 into a deployable diagnostic.
- **A17** (Zero-Shot LoRA Audit Tool from BIG_IDEAS.md Idea 13 — six audit outputs each mapping to a specific instrument: A1+A5 → task label; A2 → training-data characteristics; A14+A1 → performance estimate; A8 → harmful-fine-tune detection; A10+A16 → cross-arch compatibility; A11 → pre-flight applicability)
- **Cascade dependency:** A17 deploys cleanly iff A1, A5, A8, A10, A11, A14, A15, A16 all pass their falsifiers first. None of those has been empirically run yet — A17 is an *argument that the cluster could ground a deployable audit tool*, not a claim that the tool exists. Promotion-time language must reflect this conditional structure (similar to A12 theorem-sketch and A16 conditional-reading discipline).
- **Where A17 lands in plan.md:** Section 7 (Discussion / Self-Evolving Agent Vision) argumentation grounding, NOT empirical paper sections. plan.md's "no self-evolving agent implementation" exclusion holds — A17 is a passive diagnostic argument, not implementation.

**Cross-cluster dependency map:**
- A1 / A4 / A5 / A6 / A8 / A10 all use the Grassmannian-distance instrument; promoting one without ensuring the metric is consistent invites internal contradiction. **Promote cluster 2 as a unit** if any of it lands.
- A11 + A13 + A14 should be promoted together as the *audit triad* of A12's foundations; promoting A12 alone without these stress-tests would overclaim uniqueness.
- A7 and A9 are independent of each other; either may be promoted alone.
- A2 and A8 should be promoted together (A8 needs A2).

The user reviews this index to decide which clusters (not individual
findings) to promote into plan.md. The catalog is now at a state where
**cluster-level promotion** is the natural next move — promoting one
cluster lands an internally-coherent set of changes; piecemeal
promotion risks inconsistency.

---

### A1 — Mergeability is analytic, not regressed

- **Claim.** Section 6 Target 1 (mergeability prediction) can be predicted
  *analytically* from `Σ sin²(θ_i)` between the two adapters' Region 2
  subspaces with two scalar coefficients fitted (slope + intercept), instead
  of a learned regressor.
- **Where it lands.** plan.md Section 6, Target 1.
- **Source.** Synthesis 16's "five methods, one constraint" plus Synthesis
  23's Task Second-Moment Operator decomposition: merge interference IS
  the principal-angle mismatch on Region 2.
- **Cross-dim handling.** When `d_a ≠ d_b`, pad with `sin² = 1` for the
  `|d_a − d_b|` extra principal angles — this is the canonical Grassmannian
  principal-angle metric for unequal-dimension subspaces, *dictated* by
  geometry, not a free pick.
- **Falsifier.** Pearson r between `Σ sin²(θ_i)` and observed post-merge
  accuracy drop on the 200 random adapter pairs already required by the
  plan. r > 0.85 → analytic predictor wins; 0.5 < r < 0.85 → strong
  baseline the regressors must beat; r < 0.5 → mechanism wrong, Synthesis
  16 falsified.
- **Status.** Strong. Multiple corpus papers (OSRM, EBLoRA, OPLoRA, mtLoRA,
  Share) operationally confirm the constraint. Zero new compute. Result is
  *theorem-with-empirical-confirmation* if it holds — qualitatively
  stronger than a regressor.

- **REALIZED FIRST-CUT (iter_021, 2026-05-09).** A01's structural
  half (the geometric instrument, no merge ground truth yet) ran on
  10 of the original 11 cached LoRAs (felixml dropped: rank-256
  ~3.4 GB safetensors triggered a hard segfault inside safetensors
  Rust mmap on the user's 8 GB-VRAM/16 GB-RAM Windows box, uncatchable
  from Python). Cost: ~$0; ~1 min CPU after a refactor to factor-form
  SVDs (B,A held separately; never materialize `dW = B@A` — drops
  per-layer memory from ~64 MB to ~256 KB).
  - **45 pairs × 10 layers** of `Σ sin²(θ_i) / max(r_i, r_j)`.
  - A01 mean across pairs: **0.975**, median 0.983, min 0.849
    (instruct-safety, both lovepon q,v r=8), max 0.990 (summ-finance).
  - **The top 8 most-aligned pairs are all "lovepon q,v r=8" same-
    setup pairs** regardless of task (instruct, code, safety,
    math-CoT). The same-task math/math pair (yspkm-math r=32 all-7-
    proj vs lovepon-numinamath r=8 q,v) ranks **27 / 45** — *less*
    aligned than median. Their Region 2 subspaces literally inhabit
    different ambient dimensions.
  - **Reading: rank/target-module confound dominates task signal on
    this uncontrolled pool. Not a falsification of A1 — a confirmation
    of plan.md's E1 design choice.** plan.md mandates "rank=16 fixed,
    alpha=32, dropout=0.05, target=all linear in attention + MLP" for
    exactly this reason: with parameterization held constant, the
    geometric instrument is freed up to read task signal. With
    parameterization varying, the dominant variation axis is setup,
    not task.
  - **Q vs V asymmetry corroborated again (3rd time).** Q-layers mean
    A01 = 0.971, V-layers = 0.978; V-projections more diverse across
    tasks than Q. Consistent with A11's Q/K depth-dependent vs V/O
    uniform pattern and Synthesis 22's prediction.
  - **Depth pattern:** for both Q and V, layer 0 and layer 31 (the
    extremes) show notably lower A01 (more cross-task alignment)
    than middle layers (8/16/24). Middle attention is where the most
    task-specific subspaces live.
  - **A07 spectrum-only baseline ran for free.** L2 distances between
    sorted singular value vectors are available per pair. Notable:
    A07 does NOT order the pairs the same way as A01 — the two
    instruments capture different geometric facets (subspace
    *direction* vs subspace *magnitude*).
  - **Raw data:** `thesis_plan/test_experiments/a01_analytic_
    mergeability/results/results.json` — full per-layer per-pair
    A01 + A07 numbers + adapter ranks + structural callouts.
  - **What's still pending for the full A1 falsifier:** ground-truth
    post-merge accuracy. This run gives the geometric *instrument*;
    the regression of `Σ sin²(θ_i)` against measured merge accuracy
    requires actually merging adapter pairs and running inference on
    a benchmark — separate work, plan.md scope.

- **REALIZED CONTROLLED-POOL RESULT (iter_022, 2026-05-09).**
  iter_021 surfaced the rank/setup confound. iter_022 trained a
  controlled pool that removes that confound: 15 LoRAs (3 synthetic
  tasks × 5 seeds) on Qwen-2.5-0.5B-Instruct, all at fixed `r=16,
  α=32, dropout=0.05, target=all 7 linear modules`. ~30 min wall-clock
  on RTX 5060 (after a CPU/CUDA-wheel snafu — see iter_022.md). Tasks:
  `add_mod` (a+b mod 17), `mul_mod` (a*b mod 17), `max(a,b)`.

  **plan.md C1 prediction holds.** Same-task vs different-task A01:

  | | n | mean | std |
  |---|---|---|---|
  | same-task | 30 | **0.8458** | 0.018 |
  | diff-task | 75 | **0.9010** | 0.012 |
  | gap | | **0.0552** | **3.52σ pooled** |

  **13 of 15 closest pairs are same-task.** plan.md's C1 specification
  is "same-task d_G < diff-task d_G with > 5σ separation"; we get
  3.52σ on the smaller pool (105 pairs vs plan.md's 200 LoRAs ~
  19,900 pairs would give proportionally tighter sigma).

  **The instrument that read parameterization in iter_021's mixed
  pool reads task identity in the controlled pool.** This is the
  cleanest empirical confirmation that plan.md's E1 controlled-pool
  design choice is the right one — the design choice was empirically
  necessary, not stylistic.

  **Within-task structure is itself a training-dynamics signal**
  (free observation):

  | task | within-task A01 mean | std | reading |
  |---|---|---|---|
  | add_mod | **0.827** (tightest) | 0.008 | smooth convergence → tight cluster |
  | max | 0.851 | **0.019** | no real learning (loss=0 from start) → noise-like, variable |
  | mul_mod | 0.859 (loosest) | 0.006 | grokking at different steps per seed → consistently loose |

  mul_mod has the *highest mean distance* but *lowest std* —
  consistent with the standard grokking pattern (every seed transitions,
  but at different times, ending up in similar-but-distinct subspaces).
  max has *middle mean* but *highest std* — random-walk pattern when
  the LoRA was barely needed. add_mod is tight in both — clean
  memorization with similar trajectories.

  **This is direct empirical support for plan.md's E2 (trajectory
  geometry) section before we even run trajectory analysis.** The
  endpoint variance pattern across tasks tracks training-dynamics
  differences (smooth vs grokking vs no-signal). E2's claim that
  trajectory shape predicts properties endpoint-only analysis cannot
  recover gets a positive prior from this data.

  - **Raw data:** `thesis_plan/test_experiments/controlled_pool_qwen/results/results.json`
    — full 105-pair × 168-layer A01 + A07 numbers + per-pair tags.
  - **Pool:** 15 LoRAs in `thesis_plan/test_experiments/controlled_pool_qwen/pool/`
    with adapter weights, training logs, final eval accuracies.
  - **Eval accuracies:** add_mod 97-100%, mul_mod 93-100%, max 100%
    across all 5 seeds × 3 tasks.

- **REALIZED SUBSTEP + REGION-EMERGENCE (iter_025, 2026-05-09).**
  Pivot from the mergeability detour back to plan.md's headline
  E2 / Section-5 trajectory work. Two findings:
  **(1) Substep T2 — σ peaks at step 14, then erodes.** Substep
  training (3 tasks × 3 seeds × 30 steps, save every 2 steps, lean
  save format) shows the same-task vs diff-task pooled-std σ:
  - step 2 (after 32 examples): 3.17
  - step 14: **4.12 (peak)**
  - step 30: 3.50 (consistent with iter_023's step-25 reading 3.74)
  **Lock-in begins at step 2, peaks at step 14, then erodes through
  training.** iter_023's "by step 25" missed the peak entirely.
  Continued training pushes both same-task and diff-task LoRAs
  slightly toward common ground (diff-task d_G drops 0.919 → 0.899
  over training; same-task barely moves). E1's endpoint analysis is
  mildly suboptimal — peak-σ checkpoint is at step ~14.
  **(2) Region split is at random-baseline; spectral concentration
  genuinely emerges (corrected after advisor catch).**
  Initial framing said "R1/total = 0.30 is architectural pinning."
  Advisor caught the missing baseline: random k=64-dim projection of
  dW from R^896 has expected ratio √(64/896) = 0.267. Observed 0.30 =
  **1.10–1.17× random**, not "architectural." Re-ran on substep pool
  to test pre-step-25 behavior; confirmed R1/total is at random-baseline
  level **from step 2 onward**.
  **What IS genuinely emergent:** the spectral concentration within
  orth-to-W₀-top, measured by top1/bulk-mean ratio of singular values.
  Across the substep pool (step 2 → step 30):
  - add_mod (smooth): 433 → 539 (+24%)
  - mul_mod (grokking): 428 → 639 (**+49%**)
  - max (no real learning): 439 → 491 (+12%)
  **The spectrum sharpens during training, more for harder tasks.**
  This is what plan.md's three-region decomposition should center on
  — the spectrum within orth-to-R1, not the R1-vs-not-R1 split.
  **Caveats.** Substep n=9 LoRAs (small); σ-degradation is real but
  small in absolute size (4.12 → 3.50 over 30 steps); spectral
  concentration trends are clean and monotonic per task.
  **Implications.**
  - **A2** (4-estimator phase statistic t*) — substep σ peak at step
    14 is a single-estimator candidate; full A2 should test whether
    other 3 estimators converge near step 14.
  - **E1** endpoint analysis is suboptimal; early-checkpoint analysis
    would be strictly better for task-ID purposes.
  - **Section 3** three-region framing should be a *spectrum-shape*
    claim (top1/bulk concentration in orth-to-W₀-top), not a
    W₀-alignment claim.
  - **Grokking has a spectral fingerprint:** the rate of top1/bulk
    growth over training distinguishes the three dynamical regimes
    (49% mul_mod vs 12% max).
  Raw: `substep_lockin_qwen/results_traj/results.json` and
  `substep_lockin_qwen/results_region_emergence/region_emergence.json`.

- **FIRST-CUT REAL-TASK LMC INTERPOLATION (iter_028, 2026-05-10;
  n=6, real-task pool).** Replicated iter_027's protocol on iter_024's
  pool (BoolQ, AGNews, RT). Verified baselines first: base alone
  scores 0.41/0.38/0.37 — real tasks much harder than synthetic.
  **Same-task LMC replicates.** All 3 same-task pairs preserve
  accuracy through midpoint. boolq+boolq 0.56→0.57→0.60;
  agnews+agnews 0.87→0.84→0.83; rt+rt 0.81→**0.85**→0.72 (midpoint
  exceeds both endpoints, again).
  **Diff-task plateau-then-cliff IS synthetic-specific.** Real-task
  diff-pair curves are smooth monotonic crossfades, not plateau-then-
  cliff. Drop iter_027's "plateau-then-cliff" framing as a general
  claim — it was a property of strongly-specialized synthetic LoRAs.
  **Most surprising finding: cross-task LoRAs sometimes outperform
  same-task LoRAs on the target task.** Pure agnews_42 → 0.68 on
  boolq, vs pure boolq_42 → 0.55 on boolq. Likely explanation: at
  300 steps × bs=4, real-task LoRAs aren't fully specialized; any
  reasonable adaptation transfers positively. Needs more seeds to
  confirm.
  **Catastrophic forgetting is task-direction-specific.** boolq_42
  destroys rt (0.37 → 0.08); agnews_42 helps rt (0.37 → 0.73).
  Forgetting isn't a generic side-effect of fine-tuning.
  **Implications for plan.md.**
  - **iter_027's "plateau-then-cliff" claim downgraded.** Synthetic
    only; real tasks at this training budget show smooth crossfades.
  - **Same-task linear-in-dW LMC is the most robust finding** across
    both substrates. Most stable thing to build A1 + A6 framings on.
  - **A1 needs substrate-specific calibration.** The Σ sin²θ →
    merge-curve relationship has different shape on synthetic vs real.
  - **Real-task substrate may need longer training before merge-curve
    questions become well-posed.** iter_029 candidates: 1000-step
    training of real-task pool to test whether plateau-then-cliff
    appears post-specialization.
  **Caveats.** n=6 pairs; 100 eval/cell; 300-step LoRAs (light for
  real tasks); 0.5B base. Cross-task improvement finding is the most
  surprising and needs replication with more seeds.
  Raw: `lmc_interp_real/results/interp_real_results.json`.

- **FIRST-CUT LMC INTERPOLATION (iter_027, 2026-05-09; n=6, synthetic
  only).** Linear dW interpolation between LoRA pairs at
  α ∈ {0, 0.25, 0.5, 0.75, 1}, applied additively to Qwen-2.5-0.5B
  base model. Three findings, with the original framing tightened
  after advisor review.
  **(a) No midpoint accuracy collapse for same-task pairs.** Midpoint
  accuracy ≥ endpoint accuracy in all 3 same-task pairs:
    - add_mod_42 + add_mod_123: α=0.5 acc=1.00 (endpoints 0.98, 1.00)
    - mul_mod_42 + mul_mod_123: α=0.5 acc=0.99 (endpoints 0.97, 1.00)
    - max_42 + max_123: α=0.5 acc=1.00 (endpoints 1.00, 1.00)
  This is **linear-in-dW LMC** between same-task endpoints, which is
  consistent with plan.md A6 and stronger than A6's original claim.
  **A6 itself (Grassmannian-geodesic) is still untested** — linear-
  in-dW and Grassmannian-geodesic interpolation are distinct
  operations, and we ran only the former. Full A6 needs a geodesic-
  vs-linear comparison.
  **(b) Diff-task interpolation: no midpoint collapse, threshold-like
  tradeoff.** Across-task interpolation does NOT show a "valley of
  bad performance" — but it's NOT linear capability addition either.
  Pattern is closer to *plateau then cliff*: capability A is preserved
  near α=0 then drops sharply. Example, add_mod_42 + mul_mod_42:
    - add_mod accuracy: 0.98 → 1.00 → 0.98 → 0.78 → 0.48
      (flat through α=0.5, sharp drop α=0.5 → 1.0)
    - mul_mod accuracy: 0.29 → 0.40 → 0.78 → 0.96 → 0.97
      (rising throughout)
  At α=0.5 the merged LoRA achieves 98% add_mod + 78% mul_mod
  simultaneously — informative for merge-as-multi-task, but the
  underlying curve shape is non-linear and asymmetric.
  **(c) Catastrophic forgetting on max is real and reversible.** Base
  Qwen alone scores **0.995** on max (verified via direct base-model
  eval, no LoRA). add_mod_42 alone reduces max accuracy to 27%.
  Adding ¼ of max_42's dW restores it to 98%. The forgetting story
  holds for max specifically because base accuracy is high. For
  add_mod and mul_mod, base accuracies are 0.38 and 0.22 respectively
  — there's no real "forgetting" to talk about, and what looked like
  cross-task forgetting is mostly cross-task signal level.
  **Asymmetric cross-task transfer (advisor catch).** mul_mod_42
  alone scores 0.48 on add_mod (base alone 0.38 → +0.10 positive
  transfer). add_mod_42 alone scores 0.29 on mul_mod (base alone
  0.22 → only +0.07 transfer). The asymmetry suggests mul_mod's
  trained subspace contains add-mod-relevant structure more than
  vice versa. Unexplained but worth following up.
  **Implications.**
  - **A1 mergeability prediction REFRAMED.** Target isn't "merge
    accuracy drop" — it's the capability-tradeoff curve shape (which
    looks plateau-then-cliff in our data, not linear). Σ sin²(θ) high
    (orthogonal subspaces) → no midpoint collapse. The 2-parameter
    analytic predictor plan.md A1 wants needs to fit the curve shape,
    not just the drop magnitude.
  - **A6 NOT directly confirmed.** Linear-in-dW LMC was confirmed;
    Grassmannian-geodesic version still untested.
  - **Section 6 mergeability** moves from "does it merge well?" to
    "what's the tradeoff curve?" — but the curve isn't linear, so
    the practical implications are more nuanced.
  - **Continual-learning narrative grounded.** max forgetting is
    real and reversible by merge. Concrete mechanism for plan.md's
    "Beyond ICLR" section.
  **Caveats.** n=6 pairs (smoke-test-grade); synthetic tasks only;
  0.5B base; the threshold-tradeoff might be a small-model artifact;
  α-asymmetry is unexplained. iter_028 priority: replicate on
  iter_024's real-task pool.
  Raw: `lmc_interp_qwen/results/interp_results.json`.

- **REALIZED REAL-TASK GENERALIZATION (iter_024, 2026-05-09).** The
  intentional falsification test. 14 LoRAs trained on real NLP tasks
  (BoolQ QA, AGNews topic, Rotten Tomatoes sentiment) at the same
  fixed `r=16, α=32, all-7-target` parameterization. Three
  categorically different task types — chosen specifically because
  they share less deep structure than three flavors of mod-17
  arithmetic. **C1 holds at pooled-std separation ≈ 11** (Cohen's
  d-like; not a p-value — 91 pairs come from 14 LoRAs and are
  correlated, effective independent sample size ~14). All top-15
  closest pairs in the pool are same-task.
  **Output-vocabulary hypothesis refuted via per-module diagnostic
  (`diagnose_layers.py`):**
  - attention layers separate same vs diff *more* than MLP layers
    (sep 10.84 vs 9.87); output-vocab predicts the opposite
  - MLP A01 magnitudes are 0.93–0.99 across all pairs (near-orthogonal
    regardless of task) — the absolute same-task overlap lives in
    *attention*, not MLP
  - depth pattern: mid ≈ late > early (10.95, 10.56, 8.20) — task
    circuits live in mid-late layers, NOT a late-only "output
    decision" pattern
  - The C1 signal reads task semantics, not shared output vocab.
  **Honest comparison to synthetic.** Earlier framing called real-task
  separation "stronger than synthetic" (11 vs 3.52). That comparison
  is partly synthetic-pool flaws — synthetic included a no-learning
  task (`max`) inflating same-task std, and add_mod/mul_mod share
  algebraic structure inflating diff-task std. Drop the comparison;
  keep both as independent confirmations of C1 on different
  substrates.
  Operational notes for the log: Qwen-2.5 + fp16 NaNs immediately on
  long sequences (bf16 required), per-LoRA subprocess loop avoids
  Windows GPU memory fragmentation, boolq_789 OOM'd reproducibly on
  long-passage batches and was dropped (14 LoRAs total). **What this
  still doesn't validate:** Section 6's applied mergeability claim.
  C1 is necessary but not sufficient — A1's full falsifier is
  `Σ sin²θ` → accuracy-drop regression, which requires actual
  adapter merges + held-out eval. That's iter_025.
  Raw: `real_tasks_pool_qwen/results/results.json`. Diagnostic:
  `real_tasks_pool_qwen/diagnose_layers.py`.

- **REALIZED TRAJECTORY EXTENSION (iter_023, 2026-05-09).** Re-trained
  iter_022's pool with `--save_every 25` (11 intermediate checkpoints +
  endpoint per LoRA). Ran T2 (same-task vs diff-task d_G across training)
  and T3 (early-trajectory task-ID prediction) on the 168-layer × 12-
  timepoint dataset. **The C1 collapse signal is present at the very
  first checkpoint (step 25, ~8% of training) at 3.74σ — it doesn't
  build over training, it locks in fast.**

  | step | same-task d_G | diff-task d_G | σ |
  |---|---|---|---|
  | 25  (8%)   | 0.826 ± 0.023 | 0.899 ± 0.014 | **3.74** |
  | 100 (33%)  | 0.839 ± 0.020 | 0.899 ± 0.013 | 3.52 |
  | 276 (end)  | 0.846 ± 0.018 | 0.901 ± 0.012 | 3.52 |

  **T3 nearest-neighbor task ID at t=33% checkpoint: 15/15 = 100%
  accuracy** (random baseline 28.6%). Every LoRA's nearest neighbor
  in subspace distance at one-third of training is a same-task LoRA.

  **Practical implication for A1's Section 6 use.** The analytic
  mergeability instrument doesn't require fully-trained LoRAs as input.
  An *early-trajectory* `Σ sin²(θ)` computed at t=25–33% should already
  predict pairs' structural mergeability, since the Region 2 subspace
  is already settled. Future iter_024 priority: regress merge-accuracy
  on early-trajectory `Σ sin²(θ)` to test this directly.

  Raw: `controlled_pool_qwen/results_traj/results.json`.

### A2 — `d_task` consensus `t*` as the LoRA-native phase statistic

- **Claim.** Section 5 T1's phase-transition statistic should be
  LoRA-native, not borrowed from Schürholt's full-network machinery.
  Define `t*` = smallest training step at which all four corpus
  estimators of `d_task` (GELoRA / TwoNN; AlphaLoRA's α via
  WeightWatcher; TRS singular-value count above MP; RLCT proxy via
  DevInterp) are within ε ≈ 0.5 of their mean. Before `t*` exploring;
  after `t*` committed to a `d_task`-dim task subspace.
- **Consensus definition picked.** All-four-within-ε-of-mean, not
  pairwise max gap and not std-dev. Synthesis 15 says all four estimators
  measure the *same* `d_task` at the optimum; consensus moment is when
  the claim becomes empirically true on a given trajectory.
- **Where it lands.** plan.md Section 5, T1.
- **Source.** Synthesis 15 (four estimators converge); Synthesis 9 §5
  (LLC measures horizontal-subbundle proximity = generalization).
- **Falsifier.** Per LoRA, check `t*` lands inside the convex hull of
  phase transitions Schürholt's borrowed statistic detects. If yes,
  ship LoRA-native as headline. If no, Synthesis 15 is refuted at the
  trajectory level (also a finding).
- **Status.** Strong. Four estimators all in corpus; native to the LoRA
  setting; replaces a borrowed full-network statistic.

#### REALIZED (iter_023, 2026-05-09) — partial proxy for A2's phase statistic

A2's full claim (4-estimator consensus `t*`) requires GELoRA + AlphaLoRA
+ TRS-count + RLCT all measured per-trajectory — heavy. iter_023 ran
a **lightweight T1 proxy on the controlled Qwen-0.5B pool**: per-LoRA
maximum single-step `d_G(t, t-1)` drop, captured at 12 checkpoint steps
across 15 LoRAs. This is one face of A2's "trajectory has a phase
transition" claim, narrowed to one estimator.

**Per-task inter-seed std on max-drop:**
- add_mod (smooth): 0.020
- mul_mod (grokking): 0.016 — but max-drop *step* varies (50, 75, 125, 50, 275)
- max (no learning): **0.105** (5× larger)

**Reading.** mul_mod's per-seed-different-step grokking signature is
exactly the kind of phase-transition behaviour A2 is meant to detect.
The full 4-estimator t* will be tighter; the single-estimator version
already separates 3 dynamical regimes cleanly. Strong corroboration
of A2's premise that trajectory-level statistics carry information
endpoint analysis hides. Raw: `controlled_pool_qwen/results_traj/results.json`.

### A3 — CoTo and CopRA reframe from competitor to corroboration

- **Claim.** plan.md's Risks-row "Reviewer pattern-matches to CoTo" frames
  CoTo as a novelty threat distinguished by *measure* (us) vs *promote*
  (CoTo) — defensive. Stronger frame: CoTo's stochastic adapter
  deactivation regularizes optimization toward the geodesic on
  `G(d_task, m)`, so CoTo is a *prediction* of the LoRA-LMC theory, not a
  competitor. Same applies to CopRA (older twin).
- **Where it lands.** plan.md Section 1 (Introduction) novelty positioning
  + Section 5 closest-priors row + Risks-row.
- **Source.** Reading CoTo (2506.05713) and CopRA (2410.22911) directly
  in iter_003 and iter_004.
- **Falsifier.** Train 20 CoTo-style adapters on 4 of the 8 plan.md
  tasks, measure post-π Region 2 collapse on `G(d_task, m)`. Prediction:
  same `S(task)` as vanilla LoRAs, tighter variance under the dropping
  schedule, identical inter-task separation. If CoTo lands on a *different*
  `S(task)` or has *less* between-task separation, the corroboration
  framing fails and plan.md reverts to the defensive measure-vs-promote.
- **Status.** Candidate. ~10 GPU-hours of extra training.

### A4 — Path-vs-speed sharpens within the geodesic frame

- **Claim.** plan.md Section 5 T2 currently uses Dynamic Time Warping on
  the scalar curve `d_G(checkpoint_t, endpoint)`. Replace with **principal
  angles between tangent subspaces at matched arclength positions on
  `G(d_task, m)`**. Vector-valued test where DTW is scalar; permutation-
  test threshold against different-task null instead of hand-picked DTW
  cutoff. Speed (`dτ/dt` on the geodesic) becomes a separately measurable
  curriculum signature.
- **Operational definition.** Compare tangent subspaces *at the same base
  point* on `G(d_task, m)` (each tangent is a `d_task × (m − d_task)`
  horizontal-lift matrix). **No parallel transport invoked.** Parallel-
  transport-extended version is path-dependent (holonomy) and is the kind
  of deep theory plan.md excludes.
- **Where it lands.** plan.md Section 5, T2.
- **Falsifier.** For 50 same-task pairs with matched final accuracy, the
  tangent-overlap-vs-arclength curve must stay above the 95th-percentile
  null (50 different-task pairs) at every matched arclength position
  for the "same-path" claim. If it dips below at any position, the
  trajectory differs in path, not just speed.
- **Status.** Strong. Zero new compute (tangents on Grassmannian compute
  in CPU from saved checkpoints).

#### REFRAMED via MDS embedding (iter_026, 2026-05-09) — same-task = neighborhood, not same-path

iter_026 ran a direct test of A4's "same-path" assumption. 144 (LoRA,
step) points (9 substep LoRAs × 16 ckpts) were pairwise distance-computed
on Region 2 subspaces (3 probe layers), MDS-embedded to 2D, and plotted
as 9 trajectories. **Result: same-task LoRAs do NOT walk the same path,
do NOT arrive at the same point. They land in the same *region*, via
different paths to different endpoints within that region.**

Concretely:
- Three mul_mod seeds end at MDS coordinates (0.35, 0.4), (0.05, 0.5),
  (-0.3, 0.4). All in the upper region but visibly distinct.
- Their paths point in different directions (not co-linear in 2D).
- Each individual LoRA's path is short and smooth (no oscillations).

**A4's framing should weaken from "same-path" to "same-neighborhood."**
Within-cluster spread is itself informative — max LoRAs have tight
clusters (no learning); mul_mod LoRAs have loose clusters (grokking →
different specific endpoints per seed). The training-dynamics signature
iter_022 detected in within-task variance has a path-geometry mechanism
in this picture.

This also sharpens A6 (Grassmannian-geodesic interpolation): since
same-task LoRAs are at distinct points, the geodesic between two of
them is a non-trivial curve through the cluster region. Whether
interpolated subspaces also solve the task is testable — iter_027.

Raw: `substep_lockin_qwen/results_traj_embedding/trajectory_embedding.json`.
Plot: `plots/5_trajectory_embedding.png`.

#### Scalar-level precursor only (iter_023, 2026-05-09) — full A4 tangent test still pending

iter_023 ran the **scalar** `d_G(checkpoint_t, endpoint)` over 12
checkpoints on the 15-LoRA controlled pool. **This is NOT A4's tangent-
subspace test** — it's a same-task vs diff-task scalar-distance check.
A4 specifically asks whether *tangent subspaces at matched arclength
positions* between two trajectories overlap; two LoRAs can have
identical scalar distance-to-endpoint while taking completely different
paths there.

What the scalar test does show: same-task vs diff-task separation at
~3.5σ across all 12 checkpoint steps (3.74 at step 25, 3.52 at
endpoint). Path consistency at the scalar level holds. **The full
tangent-subspace A4 falsifier still needs to run.**

Raw: `controlled_pool_qwen/results_traj/results.json`.

### A5 — Karcher mean is the geometrically correct centroid for `S(task)`

- **Claim.** plan.md Section 4 (E1) currently treats `S(task)` as the
  empirical Euclidean mean of canonical Region 2 subspaces. **The corpus
  forces the Karcher (Fréchet) mean on `G(d_task, m)` instead** — direct
  citation: Synthesis 8 §3 / da Silva et al. 2604.27155
  ("Generalizing the Geometry of Model Merging Through Fréchet Averages").
  da Silva's Fisher merging = Fréchet average under Fisher metric on `W/G`
  is the same identification iter_004's geodesic landing arrived at from
  the bundle direction.
- **Regime caveat.** Karcher and Euclidean means agree to high order in
  the *tight-cluster* regime (within injectivity radius); they diverge
  measurably in the *moderate-spread* regime. Report cluster-radius
  statistics first; the Karcher comparison is informative only when
  clusters are not very tight.
- **Where it lands.** plan.md Section 4 (E1) Measurements C1.
- **Falsifier.** Report C1 same-task vs different-task `d_G` ratio under
  both `S_euc(task)` and `S_karch(task)`. > 5σ separation under Karcher
  → robust collapse. If the ratio collapses under Karcher, the
  Euclidean-mean C1 is an artifact of the wrong centroid; LoRA-LMC fails
  under the geometrically correct centroid (publishable falsification).
- **Status.** Strong. Direct corpus citation forces this.

### A6 — Geodesic restatement of LoRA-LMC

- **Claim.** Frankle 2020 LMC asks for *line connectivity* in flat
  ambient space; LoRA-LMC under the GL(r) quotient asks for **geodesic
  connectivity in the Riemannian quotient `W/G`**, restricted to Region 2
  yielding **Grassmannian-geodesic connectivity on `G(d_task, m)`**.
  Different geometric category. Sharpens novelty wedge over CoTo / CopRA
  / Frankle.
- **Where it lands.** plan.md Section 1 (Introduction novelty
  positioning) + LMC and LoRA-LMC subsection in Concepts and Notation
  + Section 5 ICLR-contribution paragraph.
- **Source.** Synthesis 9 §4 ("Slow Fisher Mode Connection"): Fisher-
  metric geodesics on the W/G base manifold align with the horizontal
  subbundle of the LoRA fiber bundle. Restricted to Region 2, this IS
  the Grassmannian geodesic on `G(d_task, m)`.
- **Falsifier.** For 50 same-task LoRA endpoint pairs, evaluate test
  loss along (i) linear interpolation of canonical-form factors,
  (ii) Grassmannian-geodesic interpolation between Region 2 subspaces.
  If (i) shows a barrier and (ii) doesn't, geodesic is the right curve;
  if both show no barrier, π canonicalization alone resolves LoRA-LMC;
  if both show barriers, LoRA-LMC fails (publishable falsification).
- **Known gap.** The Fisher-metric-geodesic-on-W/G *restricted to Region
  2* equals the Grassmannian geodesic on `G(d_task, m)` is *suggested*
  by Synthesis 9 §4 + Synthesis 21 (Fisher-Rao = natural connection on
  the base) but **not proved** by the corpus. plan.md's "no theoretical
  proof of LoRA-LMC; theory comes after" exclusion covers this.
- **Status.** Strong empirically; theoretical reduction is unproven.

### A7 — TRS-spectrum-only as a Section 6 baseline

- **Claim.** Add a fourth feature set in Section 6 — TRS spectrum only
  (`r × L` numbers per LoRA, no subspace, no behavior, no trajectory).
  Synthesis 19 says TRS spectrum is a complete sufficient statistic for
  the task. Section 6 becomes a free empirical test of that claim.
- **Where it lands.** plan.md Section 6 — adds a column ("spectrum-only")
  to all three existing target tables.
- **Source.** Synthesis 19.
- **Falsifier.** Three readings:
  - spectrum-only matches/beats endpoint full ΔW → Synthesis 19 confirmed
  - trajectory features beat spectrum-only → headline trajectory claim
    sharpened, Synthesis 19 refined to "spectrum is sufficient at the
    endpoint, not at the trajectory level"
  - everything beats spectrum-only → Synthesis 19 refuted, also a
    finding
- **Status.** Strong. Zero new compute; zero risk; only adds a column.

### A8 — Anti-grokking detector from post-π trajectory drift

- **Claim.** Add a fourth Section 6 prediction target: detect overtrained
  LoRAs from weights alone. Past `t*` (the consensus phase from A2),
  measure `d_G(checkpoint_t, S_karch(task))`. If the signal goes nonzero
  and grows, the LoRA has drifted out of the horizontal subbundle into
  intruder dimensions — anti-grokking.
- **Where it lands.** plan.md Section 6, new Target 4.
- **Source.** Synthesis 9 §3 + Alignment Collapse quartic law (2602.15799):
  curvature coupling pushes ΔW out of `S(task)` into intruder dims after
  generalization is reached.
- **Fallback for LoRAs without t\* (RLCT not converged):** drop those
  LoRAs from Move 8 evaluation. If RLCT proxy doesn't converge, the
  LoRA hasn't reached the SLT-generalization basin (Synthesis 9 §5: LLC
  = horizontal-subbundle proximity = generalization), so the
  anti-grokking premise (drift away from a generalizing `S(task)`) is
  invalid.
- **Headline-criterion implication.** plan.md currently says "≥ 1 of 3
  prediction tasks significant for headline." Adding A8 makes it 1 of 4.
  Whether to keep the bar at 1 of 4 or tighten to 2 of 4 is a paper-design
  decision the user should make explicitly *if* A8 is promoted.
- **Falsifier.** Does the post-`t*` `d_G(checkpoint_t, S_karch(task))`
  signal correlate with held-out forgetting beyond what endpoint
  forgetting alone explains?
- **Status.** Candidate. Zero new training (uses existing
  run-past-optimum schedule combinations in plan.md's 200-LoRA
  population). Depends on A2 (t*) and A5 (Karcher centroid) being
  promoted first.

#### Related-instrument candidate (iter_023, 2026-05-09) — A8's actual mechanism still untested

iter_023's data shows that **inter-seed std of single-step max-drops**
discriminates `max` (no real learning, base already solved it; std
0.105) from `add_mod`/`mul_mod` (real learning happened; std ~0.016–0.020).
The instrument shape (std of trajectory drops) is *similar* to what A8
would need.

**But A8's actual mechanism is different.** A8 detects post-grokking
*drift OUT of S(task) into intruder dimensions* at the *end* of
overtraining. iter_023 is detecting *noise from absence of training
signal at the start*. Different phenomenon, accidentally similar
signature. Calling this "A8 realized" would be the kind of synthesis
overreach the north star warns against.

What's real: the std-of-trajectory-drops instrument has at least one
discriminative use case ("is fine-tuning even helping?"). A8's actual
falsifier — correlate post-`t*` `d_G` drift with held-out forgetting
beyond endpoint forgetting alone — still requires the full A2 `t*`
machinery + run-past-optimum trajectories.
Raw: `controlled_pool_qwen/results_traj/results.json`.

### A17 — BIG_IDEAS.md's "Zero-Shot LoRA Audit Tool" (Idea 13) is now testable from the A1+A5+A8+A10+A11+A14+A15+A16 instrument cluster

- **Claim.** **`finding_literature/BIG_IDEAS.md`** (read directly in
  iter_017 with the application-from-instrument-cluster thread, after 7
  deferrals) names *"Zero-Shot LoRA Audit via LoL + TRS"* as Idea 13 —
  a productizable application explicitly framed as "NeurIPS workshop
  paper → ICLR 2027 full paper on LoRA audit via task residual
  spectrum." When BIG_IDEAS.md was written the audit's measurement
  instruments were not yet available. **The loop's catalog now
  provides them.** Each named audit output maps to a loop instrument:

  | Audit output (BIG_IDEAS.md Idea 13) | Loop instrument(s) |
  |---|---|
  | Task label | A1 (mergeability) + A5 (Karcher distance to labeled task centroids) |
  | Training-data characteristics | A2 (four-estimator `t*`; covers spectral-maturity stage) |
  | Estimated held-out performance | A14 (LLC at endpoint) + A1 |
  | Harmful fine-tune detection | A8 (post-π drift past `t*` = anti-grokking signature) |
  | Cross-architecture compatibility | A10 (Cross-LoRA `ρ_AB`) + A16 (paradigm choice for Region 2 vs Region 1) |
  | Pre-flight applicability check | A11 (U_W₀ vs U_S* alignment) |

- **Where it lands.** plan.md Section 7 (Discussion / Self-Evolving
  Agent Vision) gets a sharper argument: the trajectory measurement
  instruments E1+E2 build are *exactly* what an audit tool needs.
  TeleLoRA, ProbeLog, Atlas of Models (already named in plan.md
  Section 7) become the prior-art landscape; A17 = "the loop's
  cluster supplies what those papers reach for." Does NOT violate
  plan.md's "no self-evolving agent implementation" exclusion —
  audit is a *diagnostic tool*, not an agent, and Section 7 is
  argumentation only.
- **Source.** BIG_IDEAS.md Idea 13 (the named application);
  A1/A5/A8/A10/A11/A14/A15/A16 (the instrument cluster the loop has
  catalogued).
- **Falsifier.** Build a minimal audit tool combining the instruments,
  test on ~50 held-out LoRAs from HuggingFace with known task /
  training-data labels. Each audit output measured against ground
  truth: task-label accuracy, harmful-fine-tune ROC, cross-arch
  compatibility correlation with Cross-LoRA transfer accuracy. If
  ≥3 of 6 audit outputs achieve > 0.8 accuracy/correlation, A17 is
  practically validated. ≤1 of 6 → the instrument cluster is
  insufficient for the audit application; A17 refuted at deployment.
- **Cost.** ~$0 SVD + A9's LLC budget (~17 GPU-hours endpoint) +
  modest inference cost for ground-truth labeling on the held-out
  pool. Total: well within plan.md's stretch envelope.
- **Connections.** This is the loop's *first explicit application
  finding* — pulling measurement instruments together into a
  deployable product. All earlier A-findings (A1–A16) were
  measurement instruments or theoretical anchors; A17 is the *use
  case* for the cluster. If validated, A17 grounds plan.md's Section
  7 self-evolving-agent argumentation in an empirically-realized
  diagnostic tool, not just future-work language.
- **Status.** Solid, A2/A4-sized. The loop's first connection from
  measurement-instrument cluster to deployable application.
  BIG_IDEAS.md's Idea 13 is now testable; the deferral cost was
  small because the prerequisite instruments (A11 / A14 / A8 / A16)
  weren't surfaced until iter_009–iter_016.
- **Cascade-dependency calibration (added iter_018, promotion-time
  discipline).** A17's claim "the cluster *now provides* the
  instruments" is logically *conditional*: A17 deploys cleanly iff
  A1, A5, A8, A10, A11, A14, A15, A16 all pass their respective
  falsifiers first. None of A1–A16 has been empirically run against
  its falsifier yet — they are findings in BREAKTHROUGH.md, not
  validated results. The honest reading is "the cluster *would
  provide* the instruments if A1–A16's falsifiers all pass." If A11
  fails (frames orthogonal), the audit's pre-flight-applicability
  output is undefined. If A1 fails (mergeability r < 0.5), the
  task-label output is unreliable. Etc. Promotion-time language must
  reflect this cascade dependency: A17 is a *Discussion-section
  argument that the cluster could ground the audit tool*, not a
  deliverable claim that the audit tool exists.

### A16 — Cross-arch alignment paradigms split: weight-space (Cross-LoRA) vs activation-space (Transport-and-Merge); Region 2's Aristotelian character forces the weight-space choice for A1

- **Claim.** **Cui et al. "Transport and Merge: Cross-Architecture
  Merging for Large Language Models" (arxiv 2602.05495, NUS + UESTC +
  USTC, Feb 2026)** — fetched in iter_016 — proposes cross-architecture
  merging via **activation-space optimal transport** (entropically-
  regularized Sinkhorn-iteration OT on correlation-based cost matrix
  between source and target activations), then lifts activation
  correspondences to weight-space neuron-mixing. This is a *different
  paradigm* than Cross-LoRA's weight-space SVD-Frobenius alignment
  (A10): Transport-and-Merge aligns activations and lifts; Cross-LoRA
  aligns base-weight bases directly. Both end at weight-space fusion;
  the route differs.
- **The interesting structural claim.** **If** Synthesis 26's
  Platonic-Region-1 / Aristotelian-Region-2 reading is correct —
  itself a corpus *interpretation* of the Platonic Representation
  Hypothesis (Huh et al. 2024) applied to LoRA's three-region
  decomposition, *not* a Cencov-style proved theorem — *then* the
  alignment-paradigm choice splits cleanly:
  - **Region 1 (universal fiber)** is *Platonic* — metric convergence
    across architectures (per the Platonic Representation Hypothesis,
    Huh et al. 2024, which Transport-and-Merge cites at p.2). For
    Region 1, activation-space alignment (Transport-and-Merge's OT)
    is appropriate because the activations of different architectures
    converge.
  - **Region 2 (task-specific signal)** is *Aristotelian* —
    topological/local, curved, *not* metric-convergent across
    architectures. For Region 2, activation-space alignment cannot
    work because the activations don't share a common metric across
    architectures. **Weight-space alignment (Cross-LoRA's `ρ_AB`) is
    the correct choice for Region 2.**
  This means A1's `Σ sin²(θ_i)` mergeability formula, applied to
  *post-`ρ`* Region 2 subspaces from Cross-LoRA, is theoretically
  forced as the cross-arch mergeability instrument — Transport-and-
  Merge's activation-OT alignment is the *wrong* paradigm for
  Region 2 by Synthesis 26's reading.
- **Where it lands in plan.md.** Sharpens A10's framing: Cross-LoRA's
  `ρ_AB` is not just a convenient tool; it's the *right* paradigm for
  Region 2 alignment under Synthesis 26. Transport-and-Merge becomes
  a *Region-1*-side comparison candidate (worth running as a
  baseline), not a competitor. Section 3 (Method) or Section 5 (E2)
  cross-arch stretch language.
- **Source.** Cui et al. (2602.05495), pp. 1–4 read directly; combined
  with Synthesis 26 (corpus, "Platonic = Region 1, Aristotelian =
  Region 2"); combined with the Platonic Representation Hypothesis
  (Huh et al. 2024) that Transport-and-Merge cites at p.2.
- **Falsifier (compound).** On 4 plan.md tasks × 2 base models (LLaMA-
  3-8B, Qwen-2.5-3B), compute post-merge accuracy under three
  alignment paradigms:
  - (i) Cross-LoRA `ρ_AB` (weight-space Frobenius)
  - (ii) Transport-and-Merge OT (activation-space)
  - (iii) Identity (no alignment, raw weight overlap)
  Then regress A1's `Σ sin²(θ_i)` (computed on Region 2 subspaces
  post each alignment) against post-merge accuracy. Prediction
  (Synthesis 26-driven): Cross-LoRA's alignment yields the highest
  Pearson r between A1's formula and accuracy; Transport-and-Merge's
  yields lower; identity is worst. If the predicted ordering holds,
  A16 confirms Synthesis 26 empirically at the cross-arch alignment
  level. If Transport-and-Merge wins, Region 2 has more Platonic
  character than Synthesis 26 claims (Synthesis 26 partially
  refuted; A1's instrument should incorporate activation-space
  alignment).
- **Cost.** ~5 GPU-hours (Mistral-side / Qwen-side training of 8 LoRAs)
  + ~$0 SVD / OT computation. Sits in plan.md's existing cross-arch
  stretch budget alongside A10's falsifier (in fact, runs on the same
  data).
- **Connections.** A10 (Cross-LoRA's `ρ_AB`); A1 (mergeability
  formula); A15 (mergeability prediction setting); Synthesis 26
  (Platonic vs Aristotelian split); Section C four-temporal-scopes
  table (Transport-and-Merge as an *alternate paradigm* sibling at
  cross-base-merge scope).
- **Status.** Solid, A2/A4-sized. Genuinely cross-paper synthesis —
  combines Cui et al. with corpus-internal Synthesis 26 to make a
  prediction neither paper alone makes.

### A15 — Rahamim et al. provide a concrete mergeability benchmark for A1; their "local-trait" finding predicts A1's pair formula factorizes per-LoRA

- **Claim.** **Rahamim et al. (Technion + IBM Research + MIT-IBM Watson,
  arxiv 2601.06672 "Will it Merge? On The Causes of Model Mergeability,"
  Jan 2026)** — fetched in iter_015 — provides A1's benchmark and
  surfaces a free conceptual extension. They define a *mergeability
  score* `S(θ_Δ) = E_{θ_Δj~D}[f(θ + M({θ_Δ} ∪ {θ_Δj}); x, y)]` (post-
  merge accuracy averaged over random other-update partners) and find:
  - **Base-model task knowledge dominates** mergeability (correlation
    `r = 0.892` on PopQA, `0.845` on Lots-of-LoRAs).
  - **Structural weight properties** (`‖W‖`, `σ_max`, perplexity,
    context length) correlate *weakly* (0.108, 0.088, 0.202, etc.).
  - **Mergeability is a LOCAL trait** of the LoRA, not of the pair —
    a highly-mergeable LoRA stays mergeable regardless of which
    partner it merges with.
  - They did NOT test principal angles between Region 2 subspaces
    (A1's instrument).
- **Implications for A1 — two-fold.**
  - **Direct benchmark.** A1's `Σ sin²(θ_i)` formula must beat or tie
    Rahamim et al.'s base-model-knowledge predictor (`Δ_base = p_max
    - p_correct`) on the same datasets to justify A1 as the
    geometric mergeability instrument. If A1 ties, A1 is geometric
    confirmation of the behavioral story. If A1 beats it, A1 captures
    information the behavioral predictor misses. If A1 loses, A1's
    geometric framing is incomplete and Rahamim's behavioral
    predictor must be incorporated.
  - **Local-trait factorization (free extension of A1).** Rahamim's
    "mergeability is local, not pair-dependent" implies A1's pair
    formula has a per-LoRA factorization: `S(L_i) ≈ mean_j Σ sin²(θ_i)
    (L_i, L_j)`. **Calibration (added iter_016 per advisor flag):**
    Rahamim's setup averages over *random* partners *across tasks*, so
    A1's mean is L_i's distance to the **population** Karcher centroid,
    not the task-specific Karcher centroid that A5 (cluster-2) uses.
    These are different geometric objects; whether they correlate
    strongly in plan.md's controlled population is itself an empirical
    question. F2 (the falsifier) tests the right thing regardless: it
    regresses A1's per-LoRA mean against L_i's Karcher distance to
    *its task* centroid, which IS the A5 quantity. If F2 lands, the
    population and task centroids correlate strongly enough that A1's
    population-mean factorization picks up A5's task-centroid signal.
- **Where it lands.** plan.md Section 6 Target 1 (mergeability), as a
  benchmark + a per-LoRA factorization claim. Rahamim's PopQA + Lots-
  of-LoRAs datasets are public, so the benchmark is data-free for the
  loop's purposes.
- **Source.** Rahamim et al. 2601.06672, fetched in iter_015. PDF read
  pp. 1–4 directly.
- **Falsifier (compound).**
  - **(F1)** Pearson r between A1's `Σ sin²(θ_i)` and observed
    post-merge accuracy on Rahamim's PopQA setup. Compare to their
    `Δ_base = 0.892`. If A1 ≥ 0.85, A1 is competitive. If A1 ≥ 0.92,
    A1 wins. If A1 ≤ 0.5, A1's geometric framing is empirically
    refuted.
  - **(F2)** Per-LoRA factorization: regress A1's mean `Σ sin²(θ_i)`
    against L_i's Karcher distance to centroid (A5). If `r ≥ 0.8`,
    A1 and A5 are unified at the per-LoRA level — local-trait
    finding confirmed for the geometric instrument. If `r ≤ 0.3`,
    the factorization fails and A1's pair formula is genuinely
    pair-specific (against Rahamim's local-trait observation).
- **Cost.** ~$0 SVD on existing checkpoints. Rahamim's PopQA + Lots-
  of-LoRAs are public; falsifier runs on their data alongside plan.md's
  200-LoRA population.
- **Connections.** A1 (the predictor being benchmarked); A5 (the
  Karcher-centroid distance the local-trait factorization predicts);
  **A15 unifies cluster-2 (Grassmannian-instrument) at the per-LoRA
  level** if F2 lands — A1 and A5 become two readings of the same
  quantity (pair-Grassmannian-distance vs. mean-Grassmannian-distance-
  to-task-Karcher-centroid).
- **Status.** Solid, A2/A4-sized. Provides the loop's first concrete
  empirical benchmark for an A-finding (A1) and surfaces a free unifier
  between A1 and A5.

### A14 — A12's foundation 3 (Fisher non-degeneracy) FAILS generically at NN optima; SLT/LLC is the corpus's already-existing framework that handles the failure

- **Claim.** CORE_CLAIM's foundation 3 lists Fisher-Rao non-degeneracy
  on the task subspace as an assumption ("may fail for degenerate/
  uninformative tasks"). **Lakkapragada (2512.00686, Dec 2025) and
  Watanabe's SLT establish that this assumption fails *generically*
  for neural networks** — singular models, including all LoRA fine-
  tunes, have non-invertible Fisher information at optima by
  construction. The right reading is not "audit whether foundation 3
  holds" but "foundation 3 fails generically; the appropriate framework
  is Watanabe's Singular Learning Theory, which generalizes the
  Cencov + Fisher-Rao machinery to singular manifolds via the Local
  Learning Coefficient (LLC) `λ_α`."
- **Where it lands.** Updates A12's foundation-3 statement *if A12 is
  promoted*: from "non-degeneracy holds (assumed)" to "non-degeneracy
  fails; SLT/LLC handles." This actually *strengthens* A12 — foundation
  3 doesn't need an empirical applicability check the way foundation 1
  does (A11 + A13); SLT replaces the strict invariant-metric framework
  with one explicitly designed for singular models.
- **Source.** Lakkapragada (2512.00686, Yale, Dec 2025) — recent
  empirical SLT application to grokking and phase transitions, fetched
  in iter_012. Foundational corpus papers: Lau et al. 2023 LLC (already
  in graph as Community 21), Watanabe 2009/2018 (cited throughout
  corpus), Synthesis 14 ("LoRA's Gauge Symmetry IS the SLT Singularity"),
  Synthesis 9 §5 ("LLC measures horizontal subbundle proximity").
- **Falsifier.** Same experiment as A9 (Move 9-restricted): LLC at
  endpoint via DevInterp SGLD on a 50-LoRA subset. If LLC values are
  bounded away from 0 with structured task-dependent variation, SLT is
  the right framework and A14 lands. If LLC ≈ 0 uniformly, SLT is
  trivializing on this domain (LoRA may be in a non-singular regime
  per the small-rank constraint). Cost: ~17 GPU-hours, already in
  A9's stretch budget.
- **Connections.** A12's three foundations now have explicit handling:
  foundation 1 = stress-tested by A11 (signal) + A13 (noise);
  foundation 2 = algebraic, no audit; foundation 3 = generically
  fails, SLT/LLC handles it. A2's four-estimator t\* already includes
  RLCT proxy — A14 makes the SLT connection in the consensus
  estimator explicit. A9's static LLC corollary is the empirical
  signature of A14.
- **Caveat.** Lakkapragada's experiments are on toy models (modulo
  arithmetic, polynomial regressors, low-rank linear, low-rank
  autoencoders, Anthropic's superposition). LLC behavior on a
  realistic LLM LoRA fine-tune is the open question A9's experiment
  answers.
- **Status.** Solid, A2/A4-sized, corpus-internal. Paired with
  Lakkapragada (2512.00686) for currency.

### A13 — Trained LoRA B-matrices likely violate the simple Gaussian assumption A12 cites; PIGMM noise model is the honest bound

- **Claim.** A12's foundation 1 (Johnstone-Paul spiked covariance) assumes
  Gaussian-like noise around a low-rank signal. **Hirst & Ramgoolam (Oct
  2025, arxiv 2510.05218 "Approximate Gaussianity Beyond Initialisation
  in Neural Networks")** — fetched in iter_011 — show empirically that
  for trained MNIST classifier weight matrices the simple Gaussian fits
  *initialised* weights but fits *poorly post-training*. A 13-parameter
  permutation-invariant Gaussian matrix model (PIGMM) is the smallest
  fix that captures the post-training distribution. This stress-tests
  CORE_CLAIM's honest caveat ("what would break it: if B-matrices
  systematically violate the spiked model").
- **Where it lands.** plan.md Risks table — adds a row "Trained LoRA
  B-matrices may have non-Gaussian residual structure that breaks the
  simple spiked-covariance assumption" with mitigation: fit PIGMM
  invariants alongside MP fit and report deviation. Free corollary, no
  separate experiment required.
- **Source.** Hirst-Ramgoolam (2510.05218), pp. 1–4 read directly.
  Methods: compute permutation-invariant matrix invariants up to order 4
  (linear, quadratic, cubic, quartic) on weight ensembles before vs after
  training; use Wasserstein distance to quantify distributional movement.
- **Falsifier.** On plan.md's planned 200-LoRA population, compute the
  same low-order invariants on the trained LoRA B-matrices. Compare to
  predicted values from (a) simple Gaussian baseline (A12's assumption),
  (b) 13-parameter PIGMM. If (a) deviates significantly while (b)
  matches within standard error, A12's spiked-covariance foundation
  needs the PIGMM correction; otherwise A12's simple-Gaussian assumption
  holds for LoRA B-matrices specifically.
- **Cost.** ~$0. Compute on existing checkpoints during the Region 2
  extraction pass. No new training, no SGLD, no inference.
- **Caveats (honest).** Hirst-Ramgoolam study *full* weight matrices on
  MNIST, not LoRA factors. Different symmetry group too — they use
  S_n permutation symmetry between layers; LoRA has GL(r) gauge. The
  result is *suggestive of* a similar gap for LoRA B-matrices, not
  *direct evidence*. The falsifier proposed here is the direct test.
- **Connections.** A11 stress-tests A12 on the *signal* side (U_W₀ vs
  U_S* alignment); A13 stress-tests A12 on the *noise* side (Gaussian
  vs PIGMM residual). Together they fully audit A12's two foundations.
  A1's mergeability formula's calibration coefficients (slope +
  intercept) absorb whatever residual non-Gaussianity exists; A13's
  empirical bound on PIGMM-vs-Gaussian gap quantifies how much
  calibration A1 actually needs.
- **Status.** Solid, terse, A2/A4-sized. Strengthens A12's foundation
  by providing an honest quantitative path to bound the spiked-model
  assumption rather than asserting it.

### A12 — The Cencov + Johnstone-Paul + GL_r theorem-sketch proves A1, A4, A5, A6, A10 are FORCED, not heuristic

- **Claim.** `finding_literature/CORE_CLAIM.md` (read directly in iter_010,
  154 lines) is the project's strongest single mathematical statement:
  **"The space of fine-tuning tasks is a subset of the Grassmannian. TRS
  finds the correct point. Grassmannian distance is the only valid way
  to compare tasks."** CORE_CLAIM presents this as a **uniqueness
  theorem-sketch** (its own wording — "Theorem (sketch)") with honest
  caveats listed under "Assumptions to state honestly" and "What would
  break it" subsections. The sketch is grounded in three pre-2024,
  classical results:
  1. **Spiked covariance model (Johnstone 2001; Paul 2007):** under the
     Gaussian spiked model, the above-MP singular subspace IS the
     min-MSE estimator of the rank-r signal. → TRS is the optimal
     statistical estimator of the task signal.
  2. **GL_r invariance (algebraic fact):** the only reparametrization-
     invariant function of `(B, A)` is the *column space* of `ΔW = BA`,
     which is a point on the Grassmannian `G(r, m)`. → the Grassmannian
     is the right ambient object for any GL(r)-symmetric measurement.
  3. **Cencov's theorem (1982):** the Fisher-Rao metric is the *unique*
     Riemannian metric on the statistical manifold invariant under
     sufficient statistics. Pulled back to weight space, this is the
     unique invariant metric on `G(r, m)`. → the Grassmannian *geodesic*
     distance under Fisher-Rao is the unique optimal task-distance.

  **The unified statement (theorem-sketch, CORE_CLAIM's own wording):**
  under the spiked covariance assumption, *every* GL_r-invariant
  statistically-optimal task distance must reduce to Grassmannian
  geodesic distance on TRS subspaces. **Corollary (also sketch-level):**
  any method that ignores TRS or uses a non-Grassmannian distance is
  provably suboptimal under those assumptions. The "sketch" qualifier
  matters — CORE_CLAIM is internal project notes, not a peer-reviewed
  formal proof. Promotion-time language must say "we cite a uniqueness
  theorem-sketch from prior project notes that grounds our measurement
  choices," not "we test the unique-optimal-distance theorem."

  **What this means for A1–A11.** A1, A4, A5, A6, A10 are not heuristic
  methodological picks; under CORE_CLAIM's three-foundation theorem they
  are the *forced* answers to "how do you measure things in this setting":
  - **A1's `Σ sin²(θ_i)` mergeability formula** is the squared
    Grassmannian distance — Foundation 3's unique invariant metric.
    Mergeability prediction inherits Cencov's uniqueness.
  - **A4's matched-arclength tangent overlap** lives on the same
    Grassmannian; tangent-subspace comparison is the natural
    differential structure inherited from Foundation 2 + 3.
  - **A5's Karcher (Fréchet) mean** under Fisher-Rao IS the unique
    invariant centroid by Cencov; the Euclidean mean is provably
    suboptimal as a centroid (corollary of CORE_CLAIM).
  - **A6's geodesic restatement of LoRA-LMC** uses Foundation 3's
    Fisher-Rao geodesic — the only correct curve under the theorem.
  - **A10's Cross-LoRA `ρ_AB`** aligns Region 2 subspaces; under CORE_
    CLAIM, the post-`ρ` comparison is on the same `G(d_task, m)` and
    inherits the unique-distance result.

- **Where it lands in plan.md (if promoted — do not promote).**
  - **Section 2 (Background):** new subsection "Three Foundations
    (Johnstone-Paul, GL_r, Cencov)" giving the unique-optimal-distance
    theorem as the *theoretical anchor* the empirical paper tests.
    plan.md currently presents the Grassmannian as a measurement choice;
    CORE_CLAIM elevates it to a *forced* choice under the theorem's
    assumptions.
  - **Section 1 (Introduction):** novelty positioning sharpens from "we
    test LoRA-LMC under GL(r) quotient" to "we test the unique-optimal
    task-distance theorem (CORE_CLAIM) empirically — Grassmannian
    geodesics, Fisher-Rao metric, TRS subspaces — and report which
    paper-level claims are validated."
  - **Section 5 (E2) + Section 6:** every measurement instrument in
    these sections inherits the uniqueness from CORE_CLAIM. The paper
    can claim "we measure with the unique invariant instrument" rather
    than "we choose this instrument because the corpus uses it."

- **Crucial: this does NOT violate plan.md's "no theoretical proof of
  LoRA-LMC" exclusion.** CORE_CLAIM's theorem proves: *if* the spiked
  covariance + GL_r + Cencov assumptions hold, *then* the Grassmannian
  framework is unique-optimal. The empirical paper still tests whether
  the assumptions actually hold for LoRA fine-tuning (this is exactly
  what A11's pre-flight check does — verifying the spiked-model frame
  is valid via U_W₀ vs U_S* angles). LoRA-LMC itself remains an
  empirical claim. CORE_CLAIM gives the *theoretical justification* for
  the measurement instruments, not a proof of the empirical claim.

- **Source — corpus-internal, never opened before.** CORE_CLAIM.md was
  in `finding_literature/` since project inception (per its header,
  "Written: May 2026 — after stripping all conjectures") but the loop
  had never read it directly. iter_010's hidden-doc pattern surfaced
  it. Its existence in the corpus means iter_001–iter_009 implicitly
  relied on this theorem without naming it; iter_010 makes the
  reliance explicit.

- **Falsifier — the corpus's own anchor experiment.** CORE_CLAIM
  proposes one concrete test (L110-L132): take 10 same-task LoRAs (5
  from LLaMA-3-8B, 5 from Mistral-7B, same task e.g. GSM8K) and 10
  different-task LoRAs (same 5 LLaMA models + 5 random tasks). Compute
  `d_G(same-task pairs)` and `d_G(diff-task pairs)`. **Prediction:**
  `d_G(same-task) << d_G(diff-task)`. Cost: ~$0 SVD + ~5 GPU-hours of
  Mistral-side training (LLaMA-3-8B LoRAs already exist in plan.md's
  planned 200-LoRA population). This experiment is **the same
  experiment as A10's falsifier under a different motivation** — A10
  derives it from Synthesis 18 + Cross-LoRA; CORE_CLAIM derives it
  from the three foundations. Either reading produces the same test;
  passing it validates both A10's cross-arch claim and CORE_CLAIM's
  unique-distance theorem in one shot.

- **Status — foundational and theoretical (sketch-level).** This is the
  strongest single A-section finding the loop has produced because it
  provides the *theoretical uniqueness* (at theorem-sketch level) that
  A1–A11 inherit. A1–A10 are now not just "depth moves we picked"; they
  are "the unique invariant measurements that follow from classical
  pre-2024 results IF the assumptions hold." A13 (iter_011 finding)
  stress-tests one of those assumptions (Gaussianity) on real trained
  weights and surfaces a likely PIGMM correction. plan.md's
  intellectual positioning sharpens from "empirical exploration of LoRA
  trajectory geometry" to "empirical test of a uniqueness
  theorem-sketch with classical statistical foundations, including
  honest assumption-stress-tests via A11 and A13."
- **Foundation-composition calibration (added iter_013, promotion-time
  discipline).** A11's potential outcomes (frame disagreement) and
  A13's likely outcome (PIGMM correction needed) and A14's framework
  swap (SLT replaces Cencov for foundation 3) — *if all are accepted*
  — compose into a different theoretical framework than CORE_CLAIM's
  original Johnstone-Paul + GL_r + Cencov: the composed framework
  becomes **PIGMM + GL_r + SLT**, which gives **free-energy
  asymptotics (Watanabe)** rather than **Cencov-style uniqueness**.
  These are different mathematical objects: Cencov gives a unique
  invariant metric on regular statistical manifolds; SLT's free-energy
  story holds on singular manifolds but does not assert uniqueness of
  any metric. So **promotion-time language must say:** "we cite
  CORE_CLAIM's theorem-sketch as theoretical motivation for our
  measurement instruments, *and* we report assumption-stress-tests
  (A11 / A13) plus framework-replacement (A14 / SLT) for the cases
  where the original assumptions partially fail in the actual NN
  regime." plan.md's empirical paper still tests whether the
  measurement instruments work; the theorem-sketch's role is
  motivational anchor, not load-bearing proof of uniqueness in the
  realized regime.

- **Connections to A11 (pivotal).** A11's experiment doc explicitly
  references CORE_CLAIM at L330: *"If the result shows U_W₀ ≈ U_S*
  (aligned), CORE_CLAIM.md's Grassmannian framework is valid."* So
  A11 is precisely the verification that CORE_CLAIM's spiked-model
  assumption applies to LoRA in practice. A11 + A12 together: A12
  states the theorem; A11 tests its applicability; A1–A10 are forced
  consequences if both pass. This is a clean chain: foundational
  theorem (A12) → applicability check (A11) → measurement instruments
  (A1–A10) → empirical claims (plan.md sections 4–6).

### A11 — The U_W₀ vs U_S* alignment is the foundational pre-flight check that all of A1–A10 depend on

- **Claim.** Every A1–A10 finding implicitly assumes Region 2 is a
  well-defined object on `G(d_task, m)`. Region 2 is defined relative to
  *two* reference frames the corpus has never directly compared:
  - **U_W₀**: top-k left singular vectors of the pretrained weight matrix.
    Shuttleworth's "intruder dim" criterion is alignment-with vs
    orthogonality-to U_W₀.
  - **U_S\***: top-k eigenvectors of the cross-LoRA second-moment
    operator `S = (1/K) Σ_i ΔW_i ΔW_i^T`. Synthesis 23's "Task Second-
    Moment Operator" three-region decomposition is read from S.
  These two frames are treated *as if* they are the same subspace
  throughout the A1–A10 derivations, but no paper has measured the
  principal angles `θ_j(U_W₀, U_S*)` directly. Either reading is
  consistent with the corpus: if angles ≈ 0°, the frames coincide and
  A1–A10 land cleanly. If angles ≈ 90°, the corpus has been conflating
  two distinct geometric objects, and A1–A10 need to specify which
  frame they live in (and may give different answers under each).
- **Where it lands.** plan.md Section 3 (Method) preamble, BEFORE
  Section 4 (E1) actually runs. plan.md's TRS three-region story
  silently uses both frames; the alignment measurement determines
  whether Region 2 is one object or two and therefore conditions every
  measurement E1, E2, and Section 6 make.
- **Source — existing in corpus already.**
  `finding_literature/experiment_design_reference_frame_measurement.md`
  is a pre-existing experiment design (status: NOT YET RUN) that
  specifies the exact measurement: 11 named HuggingFace LoRA adapters
  on LLaMA-3-8B (HuggingFace IDs resolved), 5 layers per LoRA, k=16,
  scipy `subspace_angles` between U_W₀ and U_S*. The loop did not have
  to invent A11 — the corpus already has it as a sketched experiment.
  iter_009 surfaces it as the **highest-priority pre-flight check**
  for plan.md's framework.
- **Falsifier — four named outcomes (from the existing doc):**
  1. Angles ≈ 0° (frames same): unifies Shuttleworth's intruder-dim
     literature with Kaushik's secondary-subspace literature; A1–A10
     remain coherent; CORE_CLAIM.md's Grassmannian framework valid.
  2. Angles ≈ 90° (frames orthogonal): exposes a hidden confound in
     existing methods; A1–A10 need disambiguation per frame; possibly
     publishable as "two reference frames have been conflated."
  3. U_S* ⊂ U_W₀_bottom (minor subspace): MiLoRA's intuition correct;
     fine-tuning universally moves in W₀'s minor singular directions.
  4. U_S* ⊂ U_W₀_top (principal subspace): PiSSA's intuition correct;
     pretraining already encodes the task directions.
- **Cost — extraordinarily cheap.** ~30 min CPU on 32GB RAM (or ~5 min
  on a GPU). Loads base model weights and 11 LoRA adapter weight files
  only — no inference, no forward passes. Total cost: ~$0 (or ~$5–10
  for cloud CPU). This is the cheapest experiment in the entire
  thesis_plan and resolves the most foundational ambiguity. It should
  run before any of plan.md's 120-GPU-hour empirical work begins.
- **Connections to A1–A10 — frame-conditional in Region 2 *identity*, not in metric *structure*.** (Calibrated post-iter_009 advisor flag.) Under frame disagreement, A1–A10 do not become undefined or move to two-different-Grassmannians; they become *parameterized by which frame defines Region 2*. Specifically:
  - **A1 mergeability formula.** `Σ sin²(θ_i)` is computed *per pair*; the formula is well-defined regardless of frame. The frame conditions *which* `Σ sin²(θ_i)` (the W₀-frame version vs the S*-frame version) is the better predictor of post-merge accuracy. Both are well-defined Grassmannian distances; A1 reports both, picks the one with higher Pearson r.
  - **A2 four-estimator `t*`.** Two estimators (`α via WeightWatcher`, `TRS count above MP`) read W₀'s spectrum; two (`GELoRA TwoNN`, `RLCT proxy`) are frame-independent. Under frame disagreement, consensus degrades from 4-of-4 to 3-of-4 or 2-of-4 (the two frame-independent estimators still anchor the consensus in one frame). `t*` is not undefined — it has slightly lower statistical power per frame, with a separate `t*_{W₀}` and `t*_{S*}` if the user wants to disambiguate.
  - **A5 Karcher mean.** Always on `G(d_task, m)` — same Grassmannian, same Fisher-Rao metric (Cencov). What changes under frame disagreement is *which point* on `G(d_task, m)` is `S(task)`: the W₀-frame Karcher mean and the S*-frame Karcher mean are two different points on the *same* Grassmannian. The metric structure is preserved; only the centroid identity is frame-conditional.
  - **A8 anti-grokking detector** drifts from a frame-dependent `S(task)` but on the same Grassmannian; same as A5.
  - **A10 cross-arch `ρ_AB`** via Cross-LoRA's truncated-SVD aligns *base-weight* (W₀) bases. If the alignment-relevant frame is U_S*, Cross-LoRA's procedure may be aligning the wrong subspace direction. Outcomes (3) and (4) of A11 distinguish: outcome (4) (U_S* ⊂ U_W₀_top) = Cross-LoRA's top-r truncation is correct; outcome (3) (U_S* ⊂ U_W₀_bottom) = Cross-LoRA needs bottom-r alignment, a 1-line change to its truncation step.
- **Status.** Strong, foundational, and uniquely cheap. A11 is the
  finding the loop *should have surfaced first* — it sits beneath
  A1–A10 conceptually and costs orders of magnitude less than any of
  them.

- **REALIZED RESULT (iter_020, 2026-05-09).** A11 was run on the
  user's local hardware (8 GB CUDA + 16 GB RAM, CPU-side SVD after a
  streaming-load fix that dropped peak memory from ~7 GB to ~300 MB).
  Cost: ~$0; ~7 min download + ~2 min compute on warm cache. Result:
  **Outcome (2) — frames are decisively orthogonal.**
  - Overall mean angle `θ(U_W₀, U_S*)` = **84.03°** across 10 attention
    projection layers (range 81.6–86.4°). All 10 layers fall in the
    same orthogonal band.
  - Mean alignment with W₀'s top-256 = **0.185**; bottom-256 = **0.170**.
    Top and bottom are roughly equal → U_S* is **in W₀'s middle, not
    top, not bottom**. Refutes both PiSSA's top-W₀ initialization
    rationale (outcome 4) and MiLoRA's bottom-W₀ rationale (outcome 3)
    on average.
  - U_S* captures **68% of cross-LoRA ΔW variance** (range 61–75%) —
    the cross-LoRA covariance basis is real signal, just orthogonal
    to W₀'s top.
  - **Free corroboration of Synthesis 22 (Q/K vs V/O asymmetry):**
    q_proj layers show *low* bottom-256 alignment (0.003–0.084) but
    variable top-256 (0.07–0.31); v_proj layers are roughly symmetric
    top vs bottom (~0.23–0.29 each). Q/K depth-dependent vs V/O uniform
    spectrum compression — exactly what Synthesis 22 predicts.
  - **Implications cascade through the catalog:**
    - Validates the three-region decomposition's *premise* (Region 1
      = W₀ top, Region 2 = U_S* ⊥ W₀ top, Region 3 = W₀ bottom / MP
      noise are *empirically distinct* objects, not the same thing
      under a different name).
    - **Forces a revision of A10/A16's cross-arch claim.** Cross-LoRA's
      `ρ_AB` aligns *W₀* bases via SVD truncation. But A11 says the
      LoRA signal lives in U_S*, which is orthogonal to W₀'s top — so
      Cross-LoRA's ρ may be aligning the *wrong* subspace. The right
      cross-arch alignment for Region 2 likely requires aligning the
      U_S* bases (per-architecture cross-LoRA covariance) directly,
      not U_W₀ bases. **This is a paper-level finding** the loop
      surfaced and A11 just made empirical.
    - A1's mergeability formula on Region 2 subspaces is well-defined
      and operates in U_S*'s frame; the formula remains correct as
      stated.
    - A12's foundation 1 (Johnstone-Paul spiked covariance) is
      operating on the cross-LoRA covariance S, not on W₀ — the spike
      structure A12 cites is in U_S*'s eigenspectrum, distinct from
      W₀'s. Strengthens A12's framing.
  - **Raw data:** `thesis_plan/test_experiments/a11_reference_frame_
    alignment/results/results.json` — full per-layer principal angles,
    spectrum projections, variance-explained, and W₀ + U_S* eigenvalue
    spectra.

  **A11 is the first realized A-finding in the catalog.** Its outcome
  conditions every higher-level claim and produces an immediate paper-
  level revision (the A10/A16 cross-arch alignment story).

### A10 — Cross-arch LoRA-LMC via Cross-LoRA's `ρ_AB` + the model tree as one base manifold

- **Claim.** plan.md's stretch (T_cross-arch) names a vague "architecture-
  quotient `ρ`" that aligns `S(task)` across base models. Two corpus
  inputs combine to make `ρ` concrete and the cross-arch claim
  empirically falsifiable:
  - **Synthesis 18 / MoTHer (origin_of_llamas):** the model tree of
    LLM lineage IS the base manifold `W/G` of the LoRA fiber bundle.
    Different base models are different *points* on the same manifold.
  - **Cross-LoRA — Xia et al. 2508.05232 (fetched in iter_008):**
    constructs `ρ_AB` *concretely* as Frobenius-optimal linear
    transforms between rank-truncated SVDs of source and target base
    weights — closed-form least-squares, no training data, no
    fine-tuning. Empirically yields up to 5.26% gains on transferring
    LoRAs across LLaMA / Qwen / Gemma.
  Combined: cross-arch LoRA-LMC holds iff, after applying Cross-LoRA's
  `ρ_AB`, same-task LoRAs from base A and base B collapse onto the same
  Grassmannian ball on `G(d_task, m)` with the same `d_task` and the
  same Karcher centroid (per A5, modulo `ρ_AB`'s image).
- **Where it lands.** plan.md Section 5 stretch (T_cross-arch); related
  work in Section 2 / 3 cites Cross-LoRA as a fifth temporal scope
  in the W/G-quotient siblings table (cross-base-model-transfer time)
  alongside training, measurement, pairwise-merge, federated-merge,
  averaging.
- **Source.** Synthesis 18 read directly; Cross-LoRA PDF fetched and
  read directly.
- **Falsifier.** Train 16 LoRAs (4 tasks × 2 seeds × 2 base models —
  e.g. LLaMA-3-8B and Qwen2.5-3B). For each base pair, apply Cross-
  LoRA's LoRA-Align to bring all Region 2 subspaces into common
  target-coordinate space. Test: same-task post-`ρ` `d_G` < different-
  task post-`ρ` `d_G` with ≥ 3σ separation (weaker than within-base
  5σ because cross-base alignment is harder). Pass → cross-arch
  LoRA-LMC holds, model tree is one connected base manifold, Cross-
  LoRA's `ρ` is the empirical realization. Fail → either model tree
  isn't connected for cross-arch purposes, OR `ρ` is task-dependent,
  OR LoRA-LMC fails cross-arch.
- **Cost.** ~16 GPU-hours of stretch compute. Sits in plan.md's
  existing cross-arch stretch budget (already allowed-when-budget-
  permits in the schedule).
- **Connections.** A5 Karcher mean is the right centroid before/after
  `ρ`. A1 mergeability formula extends to cross-base mergeability
  with `ρ`-aligned principal angles. A4 tangent-overlap test extends
  to cross-base trajectories on `G(d_task, m)` post-`ρ`.
- **Status.** Strong. Two corpus inputs converge cleanly. ρ goes from
  "vague map to invent" → "specific data-free linear construction
  validated empirically by Cross-LoRA." Stretch of plan.md becomes
  a falsifiable claim, not aspirational language.
- **Caveat (advisor-flagged 2026-05-09).** "The model tree is one
  connected base manifold" is Synthesis 18's *interpretation* of MoTHer's
  empirical evidence, not Synthesis 18's evidence itself. MoTHer
  recovers a discrete tree of finite vertices; the continuous-manifold
  reading is an extrapolation. The A10 falsifier tests cross-base
  subspace agreement after applying `ρ_AB` — which is sound regardless
  of whether the underlying space is a continuous manifold or just
  finitely many tree vertices. If A10 is ever promoted into plan.md,
  the language should say "the model tree's vertices are points
  where the LoRA bundle's quotient projects to" rather than "the
  model tree is a connected manifold." This is a calibration item,
  not a falsifier change.

### A9 — Static LLC corollary at endpoints (Move 9-restricted)

- **Claim.** Per Synthesis 9 §5, LLC measures horizontal-subbundle
  proximity. Cheap consistency check: compute LLC at endpoint for a
  ~50-LoRA subset (well-trained vs run-past-optimum). Prediction: LLC
  low at well-trained, high at anti-grokked. Falsifies/confirms
  Synthesis 9 §5 directly without trajectory-level LLC tracking.
- **Where it lands.** Side experiment, not a Section 6 target.
- **Cost.** ~17 GPU-hours (LLC SGLD only); over-trained subset comes
  for free from plan.md's existing run-past-optimum schedule
  combinations.
- **Status.** Candidate. Optional side experiment.

---

### A18 — Module-type division of labor + continual-learning recipe (iter_032-041 consolidated)

- **Claim.** In LoRA fine-tuning at modest training budget on Qwen-2.5-0.5B,
  attention-layer dW updates carry the task-specific signal; MLP-layer
  dW updates carry cross-task destructive interference (output-token
  bias accumulation). Zeroing the MLP component of a destructive LoRA
  preserves >90% of its trained-task accuracy while restoring base
  capabilities on out-of-task evaluation.

- **Mechanism source.** This is **NOT a novel mechanism finding.** Geva
  et al. (2020, *Transformer Feed-Forward Layers Are Key-Value
  Memories*) and follow-ups establish the attention-as-routing,
  MLP-as-key-value-memory division. The iter_032-041 contribution is
  replicating this division in the LoRA-merge setting and using it for
  a continual-learning recipe.

- **Where it would land.** Potential new plan.md Section 7 ("Practical
  continual learning via auditing + partial merging"); A1 reframing
  ("MLP magnitude is a per-LoRA destructive predictor on top of
  Σ sin²θ subspace overlap"); A17 audit-tool concrete metric
  (MLP ||dW|| profile + behavioral check on output-token distribution).

- **Empirical support — 4-way confirmation at 0.5B scale.**
  - Correlational (iter_031): destructive vs preserving boolq LoRAs
    differ in mid-network MLP ||dW||.
  - Forward intervention (iter_032): zeroing all MLP submodules of
    boolq_42 (destructive) recovers agnews 0.14 → 0.34 and rt
    0.08 → 0.26, with only 5pp boolq accuracy loss.
  - Replication (iter_033): same recipe on rt_1024 (also destructive)
    recovers boolq 0.02 → 0.42, with only 4pp rt accuracy loss.
  - Reverse intervention (iter_034): amplifying preserving LoRA's
    MLP scales destruction monotonically (rt 0.87 → 0.19 at 2× MLP,
    → 0.00 at 5× MLP).

- **Continual-learning recipe (deployable at the scale tested).**
  ```
  for each new task LoRA L_i:
    audit_score_i = mean accuracy of L_i on held-out tasks
    if audit_score_i < base_alone_score: L_i is destructive
    if destructive: zero ALL three MLP submodules (gate, up, down)
    sum into running merged base
  ```
  - **Critical detail (iter_040+041):** must zero ALL THREE MLP
    submodules. Single-submodule ablation (zeroing gate alone, up
    alone, or down alone) does nothing — the destructive bias is
    holographically distributed across gate/up/down which compensate
    for each other under partial ablation. Confirmed on rt_full and
    boolq_full ensembles (4-way confirmation at ensemble scale).

- **Demonstrated at k ≤ 3 (iter_035 + iter_036).**
  - k=2 (boolq_42 + rt_1024 zeroMLP): boolq 0.54, agnews 0.36, rt 0.84
    — multi-task model from independent fine-tunes.
  - k=3 asymmetric (boolq_42 + rt_1024 zeroMLP, agnews_42 full): boolq
    0.66, agnews 0.86, rt 0.85 — all near-best solo accuracies.
  - **k=5 (iter_037):** recipe rule shifts from asymmetric-best at k=3
    to uniform-zeroMLP-comparable at k=5. Recipe degrades on boolq
    specifically (0.66 → 0.46). The exact k-dependence is undermapped.

- **Does NOT replace A1.** plan.md A1 is a *predictive* claim
  (Σ sin²θ predicts merge accuracy drop). The recipe is a *forcing*
  intervention (post-hoc surgery yields mergeable LoRAs). Different
  theses; complementary. A1's analytic-predictor falsifier was NOT
  run in this code-phase. If the user wants the A1 result, that's a
  separate experiment.

- **Falsifier.** Recipe should preserve trained-task accuracy ≥ 80%
  while recovering out-of-task to within 0.05 of base on a held-out
  pool of LoRAs at the scale tested. Met at 0.5B for boolq_42,
  rt_1024 individually and at k=2,3 merges. Untested at 8B.

- **Scale caveat (mandatory).** Everything tested at Qwen-2.5-0.5B,
  300 training steps, 100 eval examples per cell. plan.md's intended
  scale (LLaMA-3-8B, 200 LoRAs, 8 tasks) untested. Larger models with
  richer MLP layers may carry task-relevant information in MLP that
  the recipe destroys. **Do not promote to plan.md without 8B
  validation.**

- **Status.** Strong at the scale tested; weak on generalization.
  Recipe is genuinely deployable at 0.5B + 3-task setup. Not a
  research-level claim until an 8B replication runs.

---

## Section B — Future-work candidates (post-ICLR 2027 / Discussion only)

These do NOT belong in the in-scope paper per plan.md's "What I Will Not Do
This Year" exclusions. They are arguments-for in the Discussion section.

### B1 — Gauge-Equivariant LoRA Hypernetwork with Continual Learning (GE-LoRA-Hyper-CL)

Original iter_001/002 candidate. Text-conditioned generator of LoRA
adapters that is gauge-equivariant under `(S_n × S_n) × GL(r)` and
structurally non-interfering against an open registry of prior adapters.
Catastrophic forgetting becomes architecturally impossible in the
LoRA-only regime. Out of scope for ICLR 2027 (new architecture).

Open issues if revisited: projection-head Region 1 sign per Synthesis 16
triple constraint (project AWAY from W₀'s top subspace); registry
saturation at K ≈ d_R2 / r (~115 for SD1.4 at rank 4); merged-adapter
CLIP retention as the right continual-learning metric.

### B2 — Self-introspecting weights via W2T inversion

W2T's encoder reads adapter weights → predicts task description. Inverting
the encoder gives a deployable capability-introspector tool. Out of scope
for ICLR 2027 (separate product). Discussion-section pointer.

### B3 — Three-region surgery as a pre-training intervention

Rather than fixing forgetting at fine-tuning time, *pre-train* the base
model to expose a clean Region 2 subspace per layer. Out of scope
(Capability-Reserved Pretraining, explicitly excluded by plan.md).

### B4 — Continual learning across base architectures

MoTHer's "model tree IS fiber bundle base manifold" lets cross-arch
continual learning project both architectures into the MoTHer-recovered
base. Out of scope for ICLR 2027 except as the cross-arch *stretch*.

### B5 — Spectrum-as-fingerprint registry

Different from A7 (Section 6 baseline). Storage product: store only TRS
spectra (~`r × L` numbers per LoRA) as an adapter library, look up by
spectrum. Out of scope (deployable product, not a measurement
contribution).

### Status update (iter_018)

After 17 A-findings, B1–B5 are partially subsumed or refined:
- **B1 (GE-LoRA-Hyper-CL)** is now substantially A-supported as
  future-work: A12 (theorem-sketch) gives the gauge-uniqueness
  underpinning the gauge-equivariant generator was reaching for; A14
  (SLT/LLC) gives the singular-learning-theory framework that
  justifies the generator's behavior on singular models; A16
  (alignment paradigms) gives the cross-arch generalization mechanism;
  Section C six siblings give the W/G quotient context. **B1's
  intellectual underpinning is now in the catalog;** the missing
  piece is the architecture itself (which plan.md's exclusion
  forbids). When B1 is eventually pursued post-ICLR-2027, it should
  cite A12 + A14 + A16 + Section C as theoretical foundation.
- **B2 (W2T-inversion introspector)** is now subsumed by **A17
  (LoRA Audit Tool)** at the application level. A17's audit
  protocol IS the W2T-inversion deployed; B2 should be merged into
  A17's future-work framing rather than maintained as a separate
  entry.
- **B3 (pre-training surgery)** unchanged. Capability-Reserved
  Pretraining remains explicitly excluded by plan.md and out of A1–A17
  scope. The corpus's three-region decomposition (Synthesis 12) gives
  the *target* for B3; no A-finding speaks to the pre-training
  intervention itself. B3 stays distinct.
- **B4 (continual learning across base architectures)** is partially
  refined by A10 (Cross-LoRA's `ρ_AB`) and A16 (alignment paradigms),
  which give the cross-arch *measurement* tools but not the *continual
  learning* mechanism. B4 stays distinct as the continual-learning
  application of those tools.
- **B5 (spectrum-as-fingerprint registry)** is partially refined by
  A7 (TRS-spectrum-only baseline) — A7 demonstrates the spectrum is
  empirically sufficient for prediction; B5 takes that further into a
  deployable storage product. B5 stays distinct as the
  productization angle.

**Net change:** B2 should be merged into A17 future-work framing.
B1's foundations now exist in catalog. B3, B4, B5 stay distinct.
This is a presentation refresh, not a Section B rewrite.

---

## Section C — The four-siblings table (corpus-level finding)

Five independent papers across four temporal scopes of the LoRA pipeline
have, without coordination, derived the same geometric object — the
quotient manifold `W/G`:

| Paper | Scope | Mechanism |
|---|---|---|
| RiemannLoRA (2507.12142) | training time | optimize directly on the fixed-rank manifold `M_r` |
| W2T / plan.md `π` (2603.15990) | measurement time | global QR + SVD canonical form |
| CopRA-LA (2410.22911) | merge time | learn invertible `P` per pair |
| FLoRG (2602.17095) | federated-merge time | Procrustes alignment |
| Fréchet Averages — da Silva (2604.27155) | merge / averaging | Fréchet mean on `W/G` |
| Cross-LoRA — Xia et al. (2508.05232) | cross-base-model-transfer time | Frobenius-optimal linear `ρ_AB` between rank-truncated SVDs of base weights |

This convergence is itself a paper-level finding worth foregrounding if
plan.md gets a related-work / framing edit. Each paper re-derives `W/G`
from a different motivation. The choice of `π` for measurement is
empirically forced, not stylistic. **Six papers now, six scopes** — the
Cross-LoRA addition (iter_008) extends the table to cross-base-model
transfer, which empirically constructs the `ρ_AB` that plan.md's
stretch goal vaguely names; A10 in Section A operationalizes this for
the cross-arch within-task collapse claim.

---

## Section D — Watchlist sweep status (as of 2026-05-09)

Searched and read directly (no MD abstracts):
- **CoTo (2506.05713)** — promotes LMC via stochastic adapter dropping
  (training-time). Cousin not preemption. A3 reframe applies.
- **CopRA (2410.22911)** — older twin of CoTo. Cousin not preemption.
- **Spectral Edge Dynamics (2603.15678)** — full-network parameter
  trajectory rolling-window SVD. Methodological cousin already named in
  plan.md's reading list.
- **Compress then Serve (2407.00066)** — joint diagonalization for
  serving thousands of LoRAs. Storage compression, not trajectory.
- **Tensorized Clustered LoRA Merging (2508.03999)** — tensor decomposition
  for multi-task merging. Not trajectory.
- **Future of Continual Learning in Foundation Models (2506.03320)** —
  survey; mentions C-LoRA / DualLoRA / orthogonal subspaces. No overlap.
- **Behavioral Phase Transitions in LLMs (2508.20015)** — KL-based
  behavioral phase detector during LoRA fine-tuning. Free behavior-side
  corroborator for A2 (`t*`).
- **FLoRG (2602.17095)** — Procrustes alignment for federated LoRA. Sibling
  in Section C table.
- **RiemannLoRA (2507.12142)** — fully Riemannian fixed-rank parametrization.
  Sibling in Section C table.
- **Cross-LoRA (2508.05232)** — data-free LoRA transfer between heterogeneous
  LLMs via rank-truncated SVD + Frobenius-optimal linear alignment of base-
  weight bases. Provides empirical construction of `ρ_AB` for plan.md's
  cross-arch stretch. Sibling at *cross-base-model-transfer* scope in the
  Section C table — a fifth temporal scope alongside training, measurement,
  pairwise-merge, federated-merge, averaging.
- **`experiment_design_reference_frame_measurement.md`** (already in
  corpus, never run) — pre-existing experiment design that measures
  principal angles between U_W₀ (top SVs of pretrained weights) and U_S*
  (top eigenvectors of cross-LoRA covariance) across 11 named LLaMA-3-8B
  LoRAs. Status: "design only — NOT YET RUN." Surfaced in iter_009 as
  the foundational pre-flight check on which A1–A10 implicitly depend
  (now A11 in Section A). Cost ~30 min CPU, ~$0.
- **`CORE_CLAIM.md`** (already in corpus, read directly in iter_010) —
  154-line statement of the project's headline mathematical
  theorem-sketch (its own wording): Grassmannian geodesic distance
  under Fisher-Rao is the unique reparametrization-invariant
  statistically-optimal task distance, grounded in Johnstone-Paul
  (2001/2007) spiked covariance, GL_r invariance, and Cencov's theorem
  (1982). Provides theoretical uniqueness foundation for A1, A4, A5,
  A6, A10 (A12 in Section A). Includes a concrete anchor experiment
  (10 same-task vs 10 diff-task cross-arch LoRAs) which is the same
  experiment as A10's falsifier under a different motivation.
- **Hirst & Ramgoolam — Approximate Gaussianity Beyond Initialisation
  (2510.05218, Oct 2025)** — fetched in iter_011. Empirically tests
  whether trained NN weight matrices satisfy a simple Gaussian (i.i.d.
  matrix variables) assumption. Finding: simple Gaussian fits at
  initialisation but fits poorly post-training; a 13-parameter
  permutation-invariant Gaussian matrix model (PIGMM) fits better.
  Studies MNIST classifier weights, not LoRA factors directly — but the
  test methodology (low-order matrix invariants up to order 4 +
  Wasserstein distance) is portable. Stress-tests A12's spiked-
  covariance foundation on the *noise-distribution* side; A13 in
  Section A operationalizes this for LoRA B-matrices.
- **Lakkapragada — Using physics-inspired SLT to understand grokking &
  other phase transitions (2512.00686, Yale, Dec 2025)** — fetched in
  iter_012. Empirical SLT application to grokking, modulo arithmetic,
  toy models. Confirms that "the Fisher Information matrix is often
  non-invertible at the true parameters in singular models" — the
  generic failure of A12's foundation 3 (Fisher non-degeneracy) for
  neural networks. Tests Arrhenius-style rate hypothesis for grokking
  via free energy `F_n ≈ min_α [n L_n(w*_α) + λ_α log n]` and LLC
  scaling. A14 in Section A reframes A12's foundation 3 around this
  result: the failure isn't an applicability gap to audit but the
  *defining feature* of singular models that SLT explicitly handles.
- **`some_insights_lora_papers.md`** (corpus-internal, read directly in
  iter_014 after 6 deferrals). Methodological-refinement doc covering
  insights from AsymmetryOfLoRA (B clusters by task, A doesn't),
  AdaLoRA (FFN > attention, top > bottom in task-signal density),
  SymmetriesInWSL (distance metric must match prediction target —
  GL_r vs O(r) vs raw). Outcome (b) — partially useful, folded as
  cluster-2 methodological-refinement note in the thematic index.
  Provides E1-tier setup refinements (B-only coordinate, three-metric
  ablation, effective-rank covariate, layer grouping) but no A-section-
  sized finding. Six deferrals were a small mistake; the loss is small
  because these are setup tweaks, not foundational depth moves.
- **Rahamim, Yehudai, Carmeli, Choshen, Mass, Belinkov — Will it Merge?
  On The Causes of Model Mergeability (2601.06672, Technion + IBM +
  MIT-IBM Watson + Hebrew Univ + Kempner, Jan 2026)** — fetched in
  iter_015. Defines a concrete *mergeability score* averaging post-
  merge accuracy over random other-update partners. Tests on PopQA
  (entity-level) and Lots-of-LoRAs (task-level) using LLaMA-3.2-3B,
  Qwen-2.5-3B, Mistral-7B-Instruct. Headline: base-model knowledge
  correlates with mergeability at r = 0.892 (PopQA) / 0.845 (Lots);
  weight-norm and σ_max correlate weakly (≤ 0.21). Did NOT test
  principal angles between Region 2 subspaces (A1's instrument), so
  A1 has the entire geometric-instrument lane uncontested. Their
  "mergeability is a LOCAL trait of the LoRA, not a pair property"
  finding predicts A1's pair formula factorizes per-LoRA — A15 in
  Section A operationalizes this as a free unifier between A1 and A5.
- **Cui, Yang, Shen, Chen, Zheng, Wang, Zhang, Chua — Transport and
  Merge: Cross-Architecture Merging for Large Language Models
  (2602.05495, NUS + UESTC + USTC, Feb 2026)** — fetched in iter_016.
  Cross-architecture merging via *activation-space* optimal transport
  (entropically-regularized Sinkhorn on correlation-based cost
  between source and target activations); lifts activation
  correspondences to weight-space neuron mixing for selective top-k
  fusion. Tested on low-resource languages (Cantonese, Malaysian,
  Thai, Indonesian) and specialized domains (Medical, Finance).
  **Activation-space paradigm** distinct from Cross-LoRA's
  weight-space Frobenius alignment. A16 in Section A combines this
  with corpus's Synthesis 26 (Platonic Region 1 vs Aristotelian
  Region 2) to predict the choice point: activation-space alignment
  works for Region 1 (Platonic, metric-convergent across
  architectures) but not Region 2 (Aristotelian, no shared metric);
  Cross-LoRA's weight-space alignment is therefore theoretically
  forced for A1's mergeability instrument operating on Region 2.
- **`finding_literature/BIG_IDEAS.md`** (corpus-internal, read directly
  in iter_017 with the application-from-instrument-cluster thread,
  after 7 deferrals across iter_009–016). 30KB document with 26
  numbered ideas, multiple iteration-log entries (Iteration 2, 4, 5,
  6 night runs). Most ideas are corpus theory now internalized as
  A1–A16 (e.g., Idea 17 = three-region split, Idea 22 = intruder dims
  as holonomy, Idea 26 = universal subspace as flat directions).
  The standout *application* is **Idea 13 — Zero-Shot LoRA Audit via
  LoL + TRS** — a productizable diagnostic tool with six named
  outputs (task label, training data, performance estimate,
  harmful-fine-tune detection, cross-arch compatibility, pre-flight
  applicability). When BIG_IDEAS.md was written the measurement
  instruments for these outputs were not yet defined; the loop's
  A1+A5+A8+A10+A11+A14+A15+A16 cluster now provides them all. A17 in
  Section A operationalizes this connection. Other named applications
  (Idea 6 spectral genealogy, Idea 7 universality threshold, Idea 15
  task sequencing) are secondary — A17 focuses on Idea 13 as the
  cleanest match. Seven-iteration deferral cost was small because
  Idea 13's instrument cluster wasn't available until iter_009–016.

**No paper found in any sweep does (LoRA + GL(r)-quotient + trajectory
geometry + LMC) as plan.md does.** Watchlist remains live.

---

## What plan.md should NOT change

Per plan.md's "What I Will Not Do This Year": no new architecture, no
Capability-Reserved Pretraining, no LS-Merge style autoencoder, no
self-evolving agent implementation, no theoretical proof of LoRA-LMC.
The findings above respect all five exclusions.

---

## How to use this document

This is a **review queue**, not a delivery queue. The user reads Section A
and decides which findings (if any) are solid and helpful enough to
promote into plan.md. The loop does NOT initiate plan.md edits.
