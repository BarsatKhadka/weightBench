# Observations: The LoRA-LMC Program

**Date:** 2026-05-07
**Status:** Working hypothesis + paper plan
**Authors:** autonomous-loop

---

## The Ultimate Goal

**LoRA-LMC Conjecture (the thing we're building toward).**

> Let θ_1, …, θ_K be K independent LoRA fine-tunes of the same base model W₀, on the same task, with varying seed / learning-rate schedule / batch order / data shuffling. Let π denote the canonical quotient: QR+SVD canonical decomposition (resolving GL(r)) followed by Frobenius normalization (resolving scale). Then:
>
> 1. **Within-task collapse:** π(θ_1), …, π(θ_K) all lie within ε-distance of a single d_task-dimensional subspace S(task) on the Grassmannian G(d_task, m), where d_task is the task's intrinsic dimension (GELoRA Theorem 3.2).
>
> 2. **Between-task separation:** for distinct tasks T_a ≠ T_b, the subspaces S(T_a) and S(T_b) are well-separated in Grassmannian geodesic distance.
>
> 3. **Cross-architecture extension (the hard claim):** for the same task fine-tuned on different base models W₀^(A), W₀^(B), there exists an architecture-quotient ρ such that ρ(S^(A)(task)) ≈ ρ(S^(B)(task)) — the task-shared subspace survives cross-architecture comparison.

This is the LoRA analog of Linear Mode Connectivity (Frankle, Dziugaite, Roy, Carbin 2020), with **GL(r) reparameterization invariance substituted for permutation invariance**, and the natural extension to cross-architecture under an architecture-quotient.

If LoRA-LMC holds, three things follow immediately:

- The post-quotient weight-space coordinate is a **near-sufficient statistic for task identity**.
- Behavioral score variance across same-task LoRAs measures **residual trajectory information** (where on the subspace each run landed) — this is *exactly* why dual signal (weight + behavior) carries information weight alone doesn't.
- Cross-architecture transfer of LoRAs reduces to cross-architecture alignment of S(task) — the question becomes geometric, not behavioral.

If LoRA-LMC fails, that is *also* a finding. Either direction is a paper.

---

## Why This is the Right Central Claim

The corpus's strongest empirical anchors all point at LoRA-LMC even though no paper states it:

- **ρ = 0.971** (Shuttleworth, intruder dim count → forgetting, causal). Task-specific subspace is sharply identifiable.
- **89%** (mtLoRA: top-20% SVs share inter-task alignment). Region 1 = universal fiber, leaving Region 2 = task-shared subspace.
- **74%** (Pythia↔Mamba MPPC). Cross-architecture invariance at feature level.
- **AsymmetryOfLoRA** (B clusters by task across seeds, A doesn't). Direct empirical observation of within-task collapse, restricted to B.
- **Four independent estimators converge on d_task** (GELoRA / AlphaLoRA / TRS-count / SLT-RLCT). The "small number of subspaces" piece is internally cross-validated.

The corpus has been building scaffolding for a hypothesis it never named. LoRA-LMC names it.

It also gives reviewers a familiar handle. "Linear Mode Connectivity for LoRA under GL(r) quotient" is one sentence anyone in the field already understands the shape of.

---

## E1 — Within-Model Test of LoRA-LMC (NeurIPS Workshop)

**Question:** Does LoRA-LMC's *within-task collapse + between-task separation* hold for a real LoRA population on a single base model?

**Setup:** one base model (LLaMA-3-8B or Qwen3-7B). 8–15 tasks from LM-Eval-Harness. For each task, 10–20 LoRAs at varied seed / LR schedule / batch order. ~150–250 LoRAs total.

**Three sub-claims, each testable in isolation:**

| Sub-claim | Test | Result that matters |
|---|---|---|
| **C1.** Same-task LoRAs collapse to a shared subspace after π | Compute Grassmannian geodesic distance between π(θ_i), π(θ_j) for same-task vs different-task pairs | Same-task d_G ≪ different-task d_G with separation > 5σ |
| **C2.** Behavioral signal lives in Region 2 only | Decompose ΔW into Regions 1/2/3, regress benchmark vector on each separately | Region 2 alone explains > 90% of behavior variance; Region 1 + 3 explain ≈ 0 |
| **C3.** Trajectory variation at fixed final accuracy → residual TRS variation | Train K LoRAs to identical accuracy with varied schedules, compare TRS subspaces | Subspaces differ measurably; this residual *is* what dual signal captures |

**The dual-signal demonstration becomes a corollary of C2 + C3:** behavior is in Region 2; trajectory is in residual subspace differences. Combined signal beats either alone *because* of the structure LoRA-LMC predicts.

**Workshop chance estimate:** 70%+ if at least 2 of (C1, C2, C3) hold cleanly.

---

## E2 — Cross-Model Test of LoRA-LMC (ICLR)

**Question:** Does LoRA-LMC's *cross-architecture extension* hold? Specifically: do matched-benchmark LoRAs across base models occupy the same task-shared subspace under an architecture-quotient ρ, or different subspaces?

**Setup:** LLaMA-3-8B, Mistral-7B, plus a same-family-different-size baseline (e.g., Qwen3-7B vs Qwen3-14B) to isolate the tokenizer confound. Same task suite as E1. ~50–100 LoRAs per (task, model).

**The architecture-quotient ρ is the load-bearing methodological choice.** Five candidates now, all from recent (2024–2026) literature, all testable on the same data:

1. **Linear / TRS-Grassmannian:** project both models' Region 2 into a *common* subspace via Procrustes alignment of base-model SVDs. Cheap. Tests linear universality.
2. **Cross-LoRA's LoRA-Align (2508.05232):** SVD subspace alignment + Frobenius-optimal linear transform. Ready-made tool from corpus.
3. **OrthoMerge (Yang, Shi, Liu, 2602.05943, Feb 2026):** Riemannian-orthogonal-group merging via orthogonal Procrustes + Orthogonal-Residual Decoupling. Most principled linear ρ. Probably the single best ρ to start with.
4. **Multi-Way Representation Alignment (2602.06205, Feb 2026):** Generalized Procrustes Analysis for shared-orthogonal-universe alignment. Designed for model stitching. Direct competitor methodology.
5. **CAST / Activation Manifold Projection (2510.17902):** activation-space, not weight-space. Tests whether the "right" cross-arch coordinate is functional rather than structural.
6. **LS-Merge encoder-based (ICLR 2026):** non-linear autoencoder embedding the weight manifold. Tests LS-Merge's claim that linear is insufficient.

**Run all three.** The cleanest paper outcome is one of:

- **Type 1 (Universalist):** all three quotients yield ρ(S^(LLaMA)(task)) ≈ ρ(S^(Mistral)(task)). Strong Platonic-confirmation result.
- **Type 2 (Mechanistic divergence):** none of the quotients align matched-benchmark LoRAs. Behavioral equivalence does *not* imply mechanistic equivalence.
- **Type 3 (Method-dependent):** linear methods fail, non-linear succeeds, or vice versa. The result is a **falsification** of one camp's hypothesis. Equally publishable.

**ICLR chance estimate:** 50–60% conditional on a stark Type 1/2/3 result; <20% if results are noisy.

**Two technical risks to address up front:**

- **Tokenizer confound** — the same-family-different-size baseline isolates this. If LLaMA-7B↔Mistral-7B disagree more than LLaMA-7B↔LLaMA-13B, you've measured architecture; less, you've measured tokenization.
- **Different layer counts / head dims** — handle by per-layer alignment with optimal-transport between layers, not naive layer-id matching.

---

## What to Read, in Priority Order

### Tier 0 — re-read with LoRA-LMC framing in mind (1 day)

Re-reading these is fastest because you already know them; the new framing changes what's salient.

- `finding_literature/grounded_picture_v1.md` — Step 11 specifies the cross-arch Grassmannian test. Run it first. ~30 min CPU experiment.
- `finding_literature/synthesis_night_run_19_trs_spectrum_sufficient_statistic.md` — claims TRS = sufficient statistic. LoRA-LMC says this is *almost* true; the "almost" is the residual that justifies dual signal.
- `finding_literature/synthesis_night_run_25_lora_population_manifold_gl_net_w2t.md` — already names the LoRA Population Manifold = W/G. Half the LoRA-LMC machinery.
- `finding_literature/CORE_CLAIM.md` — Grassmannian as the canonical task space.

### Tier 1 — load-bearing for the conjecture itself (this week)

These are the papers your formal statement depends on.

- `arxiv_1912_05671.md` — **Linear Mode Connectivity** (Frankle, Dziugaite, Roy, Carbin 2020). Your formal cousin. Read carefully; the proof structure adapts.
- `arxiv_2209_04836.md` — **Git Re-Basin** (Ainsworth et al. 2022). Permutation-quotient version. Tells you how to write the GL(r)-quotient version.
- `arxiv_2110_06296.md` — **Role of Permutation Invariance in LMC** (Entezari et al. 2021). The empirical core for full networks.
- `arxiv_2205_12411.md` — **Linear Connectivity Reveals Generalization Strategies** (Juneja et al. 2022). Connects LMC to generalization — relevant if you want to extend to behavior. Also: **shows BERT fine-tunes can be linearly disconnected** — the falsifier we now know about.
- `arxiv_2211_08422.md` — **Mechanistic Mode Connectivity** (Lubana, Bigelow, Dick, Krueger, Tanaka, ICML 2023). The exact formal machinery for E2. "Lack of linear connectivity ⟹ dissimilar mechanisms." This is the framework we stand on.
- `arxiv_2406_08447.md` — **The Impact of Initialization on LoRA Finetuning Dynamics** (Hayou, Ghosh, Yu, NeurIPS 2024). The actual AsymmetryOfLoRA paper, proving the asymmetry is intrinsic and theoretical, not coincidence. Read first.
- `finding_literature/lora_vs_fullft_intruder_dimensions.md` — Shuttleworth's ρ = 0.971 result. Your strongest empirical anchor.
- `finding_literature/some-insights.md` — corpus's notes on AsymmetryOfLoRA's empirical implications.
- `finding_literature/implicit_regularization_matrix_factorization_gunasekar.md` — Gunasekar 2017. The theoretical foundation for "small number of consistent subspaces."

### Tier 2 — methods for E1 / E2 execution (next 2 weeks)

- `finding_literature/w2t_lora_weights_know_capabilities.pdf` — QR+SVD canonical decomposition. The π map for E1.
- `finding_literature/cross_lora_transfer_heterogeneous_llms.pdf` — LoRA-Align is candidate ρ #2 for E2.
- `arxiv_2602_05943.md` — **OrthoMerge** (Feb 2026). Riemannian-orthogonal-Procrustes ρ for E2. Probably the best linear-quotient choice to start with.
- `arxiv_2602_06205.md` — **Multi-Way Representation Alignment** (Feb 2026). Generalized Procrustes Analysis for shared-orthogonal-universe — designed for model stitching, applicable to LoRA cross-arch.
- `arxiv_2510_17902.md` — **CAST / Activation Manifold Projection**. The activation-space rival to weight-space cross-arch. Critical baseline for E2.
- `finding_literature/learning_on_loras_gl_equivariant_weight_space.pdf` — Putterman GLNet, GL(r)-equivariant baseline.
- `finding_literature/sane_scalable_versatile_weight_space_learning.pdf` — Schurholt SANE, autoencoder weight-space embedding.
- `arxiv_2504_10231.md` — **ViT Model Zoo** (Schurholt 2025 ICLR Workshop). Closest prior for E1 setup. Differentiate carefully.
- `arxiv_2407_00066.md` — **Compress then Serve**. Joint diagonalization across thousands of LoRAs. Confirming signal that shared subspaces exist; methodology for finding them at scale.
- `arxiv_2512_01759.md` — **Weight Space Representation Learning with Neural Fields** (Dec 2025). Most recent frontier in weight-space embedding. Mentions optimal-transport-based neuron alignment as alternative to Procrustes.
- `finding_literature/spectrum_snr_marchenko_pastur_training.pdf` — SNR per layer for choosing E1's per-layer ranks.

### Tier 3 — frame and depth (when writing)

- `arxiv_1811_08298.md` — Marchenko-Pastur from spin glass. Cross-domain depth for the noise-floor argument.
- `arxiv_2408_06421.md` — NN as Spin Models. Hidden-order phase transition framing.
- `arxiv_2512_05117.pdf` (universal_weight_subspace_hypothesis.pdf in your corpus) — Universal Weight Subspace, 1100+ models. Your null hypothesis for E2.
- `arxiv_2503_10633.md` — "We Should Chart an Atlas of All the World's Models." Visionary framing for the program.
- `arxiv_2504_18072.md` — Phase Transitions Model Zoo. Direct prior for measuring training-phase position.
- LS-Merge ICLR 2026 PDF (OpenReview) — full text of the non-linearity argument; needed for E2's Type 3 result.

### Tier 4 — open questions where corpus is thin

These probably need more reading:

- **Tokenizer/vocabulary effects on weight-space structure** — corpus has zero edges here. Partially addressed: tokenizer choice IS impactful for small models; with sufficient fine-tuning data (>50B tokens) the impact becomes negligible. So the tokenizer-confound for E2 likely *shrinks* the more LoRA training data we use. Read: `arxiv_2402_01035.md` (Getting the Most Out of Your Tokenizer).
- **Linear-mode-connectivity for fine-tuning specifically** — partially addressed: LMC for fine-tuned LLMs is empirically *mixed*. BERT often disconnected, RoBERTa/T5 connected. Pretraining quality is the discriminator. Read: arxiv 2205.12411 (Juneja et al.) and Mechanistic Mode Connectivity (OpenReview NZZoABNZECq).
- **Procrustes / optimal transport between weight spaces** — exact methodology for cross-arch ρ. Cross-LoRA's LoRA-Align uses Frobenius-optimal linear transform = Procrustes. CAST uses learned bidirectional projection. LS-Merge uses learned autoencoder. *Three* candidate ρ's, all justified.
- **Trajectory-dependent vs endpoint-only sufficient statistics** — corpus has implicit hints (3-node communities on "singular vector reorientation," "invariant execution manifold") but no explicit framing. Genuine gap; could become a sub-result of E1 (C3).
- **Path-dependence in LLM fine-tuning** (alignmentforum: "Speculative inferences about path dependence in LLM fine-tuning"). Worth reading even though informal — frames the trajectory question.

---

## Open Falsifiers — Things That Would Kill LoRA-LMC

Be honest about what would break this:

1. **AsymmetryOfLoRA's seed-clustering is rank-rank artifact.** If "B clusters by task" is actually just "B has fewer seed-explored degrees of freedom than A," then within-task collapse is trivial. **Test in C1:** vary not just seed but LR schedule, batch order, optimizer; if collapse persists, the clustering is real.

2. **d_task is not stable.** If GELoRA's d_task estimate varies wildly with rank, batch size, or training duration, the "small number of subspaces" claim has no fixed dimension. **Mitigate:** measure d_task at multiple ranks, report stability.

3. **Region 2 isn't where behavior lives.** If C2 fails — e.g., behavior correlates with Region 1 (universal) variation, or with Region 3 (noise) — the three-region story is wrong as stated. The corpus doesn't survive this; it's the falsifier with the highest leverage.

4. **Cross-architecture quotient is undefined.** If no version of ρ aligns same-task LoRAs across architectures (Type 2 result), LoRA-LMC's strong form fails. The within-task version still holds; E1 is fine; E2's headline is "behavioral equivalence ≠ mechanistic equivalence" rather than "universalism."

5. **LS-Merge is right that the manifold is non-linear.** If autoencoder embeddings outperform any linear quotient in cross-arch alignment, the entire spectral framework is operating on the wrong coordinates. The corpus has to be re-read with the autoencoder as ground truth.

6. **LMC-for-fine-tuning is base-model-dependent.** This is the most important *new* falsifier surfaced this session. Linear Connectivity Reveals Generalization Strategies (Juneja et al. 2022, arxiv 2205.12411) found that *different BERT fine-tunes on the same task are often linearly disconnected*; RoBERTa and T5 fine-tunes ARE connected. The factor distinguishing them appears to be pretraining quality / convergence — better-pretrained backbones support LMC, weaker ones don't. **Implication for our work:** LoRA-LMC may hold on well-pretrained backbones (LLaMA-3, Qwen3, Mistral-7B) and *fail* on under-pretrained ones (small models, early checkpoints). This is actually a genuine research opening — the question is open in the literature, the answer for LoRA specifically isn't predetermined. Pick base models for E1 from the well-pretrained side; if LoRA-LMC holds there, that's a real result. If it fails even on well-pretrained backbones, that's also a real result and it tells you something stronger than the full-network case.

## What's Already Empirically Suggesting LoRA-LMC Holds (confirming signals)

Beyond AsymmetryOfLoRA, several recent papers are operationally finding what LoRA-LMC predicts without naming it:

- **Hayou, Ghosh, Yu 2406.08447 (NeurIPS 2024) — "The Impact of Initialization on LoRA Finetuning Dynamics."** This is *the* AsymmetryOfLoRA paper. They prove (not just observe) that B-zero/A-random vs A-zero/B-random lead to fundamentally different training dynamics in the large-width limit, with optimal learning rates scaling as Θ(n^{-1/2}) vs Θ(n^{-1}). The asymmetry is *intrinsic* and *theoretical*, not just empirical clustering. **This is our hardest evidence that the post-quotient subspace is task-determined — A and B carry different roles by theorem, not by coincidence.** Read first among the LoRA-specific Tier 1 set.
- **Compress then Serve** (Brüel-Gabrielsson et al. 2407.00066) uses *joint diagonalization* to find subspaces shared across many LoRA adapters at serving time. Their compression works because LoRAs share subspaces — exactly the LoRA-LMC prediction restricted to endpoints.
- **EigenLoRAx** (Kaushik et al. 2502.04700) finds *task-invariant principal subspaces* across LoRAs and recycles them for new-task adaptation. Same observation: shared subspace exists empirically.
- **D2C** (2601.17441) clusters LoRAs by task using SVD features.
- **Preference-Aligned LoRA Merging** (2603.26299) mentions "subspace coverage" and "directional anisotropy" in LoRA populations — direct LoRA-LMC vocabulary.

So four independent groups (Hayou, Brüel-Gabrielsson, Kaushik, the D2C team) have empirically or theoretically observed pieces of LoRA-LMC's within-task collapse + between-task separation. None state the conjecture as such. **Stating it cleanly is the wedge.**

## The E2 Framework We Stand On: Mechanistic Mode Connectivity

For E2, the formal machinery already exists in the literature:

**Lubana, Bigelow, Dick, Krueger, Tanaka — "Mechanistic Mode Connectivity" (ICML 2023, arxiv 2211.08422).**

Their core formalism:
- *Mechanistic similarity* = shared invariances to input transformations
- *Theorem-shaped result:* lack of linear mode connectivity between two models implies they use dissimilar mechanisms
- *Practical consequence:* models with the same task accuracy can still be mechanistically distinct, and naive fine-tuning may fail to alter underlying mechanism

**Why this is load-bearing for E2:**
Our E2 question — "do matched-benchmark LoRAs across architectures share mechanism?" — maps directly onto their framework. The cross-arch ρ-quotient version of Mechanistic Mode Connectivity is what E2 measures. Their connectivity-based fine-tuning (CBFT) is also a deployable downstream consequence: if E2 finds Type-2 (different mechanisms despite same benchmark), CBFT becomes a way to fix that.

**The exact E2 sentence becomes:** *"We extend Mechanistic Mode Connectivity to the cross-architecture, GL(r)-quotient regime for LoRA adapters, and find ___."* That is an ICLR sentence. The framework is real, the cousin papers are real, the result is what we measure.

---

## Beyond E1 + E2: What This Builds Toward

If LoRA-LMC holds in the strong form, three downstream lines open up:

1. **A LoRA capability index.** The S(task) subspace of a LoRA is its task fingerprint. HuggingFace adapters become indexable by Grassmannian point, searchable by task subspace.
2. **Cross-architecture portable adapters.** ρ is invertible — LoRAs migrate across base models by Grassmannian rotation, not retraining.
3. **Trajectory-aware fine-tuning.** Knowing where on S(task) you've landed says something about *how* you learned the task, which predicts mergeability, transfer, and forgetting.

These are not for E1 / E2. They're what the program produces if E1 + E2 land.

---

## Closest Priors and How We Differentiate

Three papers are uncomfortably close to E1's framing. They're all from the Schürholt group, building a coherent program. We have to differentiate cleanly or lose to obvious-prior-art in review.

### Schürholt-group prior 1: ViT Model Zoo (`arxiv_2504_10231.md`, ICLR 2025 Workshop)
- 250 ViT-S models, weight statistics + behavioral metrics, validated for diversity.
- **Differentiator:** language not vision; LoRA not full models; TRS-region-aware features, not skewness/kurtosis/L2; explicit predictive demonstration tied to a downstream task (merging).

### Schürholt-group prior 2: Phase Transitions Model Zoo (`arxiv_2504_18072.md`, ICLR 2025 Workshop)
- 12 model zoos systematically covering phase-transition states; combines model zoos with statistical-physics phases.
- **Differentiator + use:** their phase framework is *exactly* what we need for C3 (trajectory residual). Don't ignore it — *use* their phase definition to characterize where our LoRAs land. Cite as foundation; our addition is "we extend phase-zoo to LoRAs and connect phases to TRS-region-2 subspace identity."

### Schürholt-group prior 3 (closest, most dangerous): "Structure Is Not Enough" (`arxiv_2503_17138.md`, ICLR 2025 Workshop)
- Meynent, Schürholt, Borth et al. literally argue: "structural loss using Euclidean distance between original and reconstructed weights fails to capture features critical for reconstructing high-performing models." They use weight-space autoencoders and find behavior signal is needed.
- **Differentiator:** they do *weight reconstruction* (autoencoder-style); we do *task-prediction and merge-compatibility forecasting*. They use Euclidean-distance structural loss; we use TRS-canonical, GL(r)-quotient structural representation (which their own framing implicitly criticizes — Euclidean-on-weights ignores the GL(r) symmetry). Our hypothesis is that the right structure (TRS-canonical Region-2) plus behavior, applied to the LoRA-LMC framework, predicts merge compatibility specifically — a downstream task they don't address.

The cleaner E1 sentence becomes: **"Meynent et al. (2025) showed structural Euclidean reconstruction loss is insufficient for full-model autoencoders. We test whether GL(r)-canonical Region-2 structural coordinates (which respect the corpus's invariance results) suffice for LoRA populations under the LoRA-LMC hypothesis, and show that the residual gap between structure and behavior corresponds exactly to trajectory variation at fixed final accuracy."**

That's a sharp positioning that *uses* their finding rather than competing with it.

### Cross-arch LoRA prior: TeleLoRA (`arxiv_2503_20228.md`)
- Lin, Acharya, Roy, Jha. Cross-LLM LoRA alignment teleportation for Trojan mitigation. Uses local activation info + permutation symmetry.
- **Differentiator for E2:** they don't quotient by GL(r); they don't measure subspace overlap; they don't compare matched-benchmark LoRAs. Their goal is *transferring* alignment, ours is *measuring whether mechanism is shared*. Different question, same arena.

### Functional-probing prior: ProbeLog (`arxiv_2502_09619.md`)
- Kahana, Nathan, Horwitz, Hoshen. Zero-shot model search via probe-based descriptors.
- **For our work:** ProbeLog is an *alternative coordinate* — functional probes instead of weight-space coordinates. Worth comparing against TRS-coordinate as a baseline in E1's predictive-demonstration step. If ProbeLog beats TRS, we know the coordinate is wrong; if TRS+behavior beats ProbeLog+behavior, the structural coordinate adds information functional probing cannot recover.

## Status Check

- 25+ papers added to corpus this session (Tier 1, 2, 3 above)
- Graph rebuilt: 1761 nodes / 1909 edges / 169 communities
- Ultimate goal stated formally
- E1, E2 reframed as conjecture-testing (not framing-validation)
- Falsifiers explicit
- Reading list ordered

Next moves I'm running while you review:
- Read AsymmetryOfLoRA's exact seed-clustering claim — how strong is the evidence for C1?
- Look for fine-tune-specific LMC work (full-network LMC ≠ fine-tune LMC)
- Look for tokenizer-effects-on-weight-geometry literature (currently corpus-empty)
- Pull LS-Merge full PDF for the non-linearity argument

---

## Prior Art Audit — 2026-05-07

A deep prior-art search asked: *has anyone done the full assembly* (GL(r)-quotient + TRS three-region + LoRA trajectory + LoRA-LMC + downstream prediction)? Verdict: **no — the integration is genuinely open.** "LoRA-LMC" returns zero hits as a named conjecture. Five papers came back as the closest competitors; all are class B (adjacent component), none class A (direct overlap).

### Five candidates and how they connect to LoRA-LMC

- **CoTo — Come Together, But Not Right Now** (`arxiv_2506_05713.md`, arXiv 2506.05713, ICLR 2026). The biggest novelty threat. *Promotes* LoRA LMC via stochastic adapter deactivation during training, evaluates via interpolation barrier on the endpoint pair. **Differentiator:** CoTo prescribes a training intervention to *make* LMC hold; LoRA-LMC *measures* whether vanilla LoRAs already exhibit within-task collapse under the GL(r)-quotient. No GL(r) gauge fix, no Region 1/2/3, no trajectory analysis in CoTo.
- **CopRA — Progressive LoRA Training** (`arxiv_2410_22911.md`, arXiv 2410.22911). Same shape as CoTo, older. Cite alongside it in related work as "training-method approaches to LoRA mergeability."
- **Spectral Edge Dynamics of Training Trajectories** (`arxiv_2603_15678.md`, arXiv 2603.15678, Mar 2026). Methodologically the closest cousin: rolling-window SVD over parameter updates, three-phase pattern (rise / plateau / collapse), early-warning prediction of grokking. **Differentiator:** full-network, not LoRA; no GL(r); no three-region. **Use:** borrow their rolling-window spectral-edge statistic for the T1 phase-detection instrument. Set a weekly arXiv alert on this group — if they publish a LoRA follow-up, it becomes class A.
- **Universal Weight Subspace Hypothesis (UWSH)** (`arxiv_2512_05117.md`, arXiv 2512.05117, Dec 2025). 500 Mistral-7B LoRAs + 500 ViTs + 50 LLaMA-8B; HOSVD + Grassmannian principal angles; argues all fine-tunes concentrate in a single low-dim universal subspace. **Differentiator:** UWSH's "universal subspace" ≈ Region 1 of the TRS three-region decomposition. UWSH is endpoint-only, conflates Region 1 and Region 2, and makes no LMC claim. **Use:** baseline for C2 — regress benchmark vector on UWSH-style universal subspace alone, expect ≈ 0 explained variance, validating Region 2 as the behavioral coordinate.
- **Generalized Linear Mode Connectivity for Transformers** (`arxiv_2506_22712.md`, arXiv 2506.22712, Jun 2025). Four-symmetry-class LMC taxonomy for full transformers (permutation / sign / scaling / general invertible map). **Differentiator:** full-network, not LoRA factorization. **Use:** position GL(r) cleanly within their taxonomy as the "general invertible map" class restricted to the LoRA `(B, A)` factorization.

### Risk and recommendation

Risk level: **low-to-medium**. The wedge holds. Two real concerns:
- *Medium:* CoTo will pattern-match to LoRA-LMC for any reviewer; lead the introduction by contrasting *measure* (this thesis) vs *promote* (CoTo).
- *Medium:* fast-follow risk — every component is assembled in the literature; a 2026 group with the right compute could ship the same paper in ~6 weeks. The September deadline is the right urgency.

Read order this week: Spectral Edge Dynamics → CoTo → UWSH → CopRA → Generalized LMC.

### Open questions surfaced (corpus-empty)

- Has any 2026 paper combined CoTo's training intervention with trajectory measurement? (Not yet.)
- Is there a published LoRA version of Spectral Edge Dynamics in flight? (Watchlist.)
- Does UWSH's universal subspace coincide layer-by-layer with mtLoRA's top-20% high-alignment subspace? (If yes — strong cross-validation that Region 1 = UWSH = mtLoRA-shared.)
