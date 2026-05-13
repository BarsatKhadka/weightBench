# Thesis Plan — LoRA Trajectory Geometry

**Target:** ICLR 2027 main track (Sep 2026 deadline, ~3 months from May 2026)
**Author:** Florence
**Status:** Active, executable

---

## The Vision (one paragraph)

A fine-tuned model's weight is the *endpoint* of a trajectory through weight space. Every existing analysis of LoRA adapters — capability prediction, retrieval, merging, attribute classification — looks at endpoints. The path itself is unmeasured. This thesis claims that **the trajectory carries information the endpoint loses, and that information is the foundation for self-evolving agents that can introspect their own learning.** Concretely: we trace LoRA fine-tuning trajectories through the GL(r)-quotient subspace, formalize the **LoRA-LMC conjecture** (within-task collapse + between-task separation under invariance quotients), and show that trajectory geometry predicts properties — mergeability, forgetting, generalization — that endpoint analysis cannot. The eventual application is agents that read their own trajectory information at deployment to decide what they know, what they need, and where to go next.

---

## The Paper

**Title (working):** *Trajectory Geometry of LoRA Fine-Tuning: Within-Task Collapse and the LoRA-LMC Conjecture*

**Structure (ICLR-shaped):**
1. **Introduction** — the trajectory question, LoRA-LMC conjecture stated, contributions
2. **Background and prior work** — Linear Mode Connectivity (Frankle 2020, Lubana 2023), Weight Space Learning (Schürholt et al.), AsymmetryOfLoRA (Hayou 2024), Phase Transitions Zoo (Schürholt 2025)
3. **Method** — GL(r)-quotient π, TRS three-region decomposition, trajectory measurement protocol
4. **E1: Endpoint analysis (setup section)** — characterizes population, validates pipeline. Shows Region-2 carries behavior, dual signal beats single. *Section 4 is "endpoint baseline."*
5. **E2: Trajectory geometry (main contribution)** — same population *with checkpoints*; convergence dynamics, phase structure, path-vs-speed decomposition, prediction of endpoint from early trajectory. *Section 5 is the headline.*
6. **Predictive demonstration** — trajectory features predict mergeability and forgetting better than endpoint alone
7. **Discussion and self-evolving agents** — what this enables (capability gap detection, forgetting prediction, runtime introspection)

E1 and E2 are *one paper*, not two. E1 is the setup that validates the pipeline; E2 is the contribution. This is the clean ICLR shape.

---

## Three-Month Schedule

| Week | Milestone |
|---|---|
| W1–W2 (May) | Pipeline: LoRA training script with checkpointing every K steps. Eval pipeline (LM-Eval-Harness 8-task subset). TRS extraction (QR+SVD canonical, Region 1/2/3 split). |
| W3 (May) | Train first batch of 50 LoRAs (5 tasks × 5 seeds × 2 schedules) to validate pipeline. Compute endpoint TRS and benchmark vector. |
| W4 (May) | E1 endpoint analysis: same-task vs different-task Grassmannian distances, Region 2 vs full ΔW correlation with behavior. Decide: does within-task collapse hold at endpoint? |
| W5–W6 (June) | Scale up: 200–300 LoRAs (10 tasks × 6 seeds × 5 schedule/LR variations). Save checkpoints every 50 steps. |
| W7 (June) | E2 trajectory analysis: distance-to-centroid over time, phase detection, path-vs-speed decomposition. |
| W8 (June) | Predictive demonstration: trajectory features → mergeability, → forgetting. Train predictors, baseline against endpoint-only. |
| W9 (July) | Falsifier checks: BERT-style disconnection test (try a less-pretrained backbone too). Variance across schedules. Trajectory length normalization. |
| W10 (July) | Stretch: cross-architecture trajectory comparison (LLaMA vs Mistral, same task). |
| W11 (Aug) | First draft writeup. Figures. |
| W12 (Aug) | Revise, ablations, anonymize, polish. |
| W13 (early Sep) | ICLR 2027 submission. |

**Buffer:** if anything takes 50% longer than planned, drop the cross-arch stretch. The within-base-model trajectory result is the headline; cross-arch is a sub-result.

---

## E1 — Endpoint Setup (Section 4 of the paper)

### Question
For a population of LoRAs fine-tuned on the same base model across multiple tasks and seeds, does the post-quotient (GL(r)-canonical, Region-2-restricted) coordinate cluster by task with high separation? Does the dual signal (weights + behavior) carry information either alone misses?

### Setup
- **Base model:** LLaMA-3-8B (popular, has existing LoRA hub, manageable size)
- **Tasks (8):** ARC-Challenge, ARC-Easy, BoolQ, HellaSwag, GSM8K, MBPP, MMLU-subset, OpenBookQA
- **Population:** ~200 LoRAs total — 8 tasks × 5 seeds × 5 (LR, batch, schedule) variations
- **LoRA config:** rank=16 fixed, alpha=32, dropout=0.05, target=all linear in attention + MLP
- **Behavior coordinate:** 8-dim vector of per-task accuracies on held-out splits
- **Weight coordinate:** for each LoRA, compute QR+SVD canonical decomposition (W2T-style) per layer; project onto Region 2 (above-MP, W₀-orthogonal) per layer; flatten or aggregate via attention pooling

### Measurements
- **C1.** Grassmannian geodesic distance d_G(L_i, L_j) for all pairs. Test: same-task d_G < different-task d_G with > 5σ separation.
- **C2.** Region 1 vs Region 2 vs Region 3 correlation with benchmark vector (per-region partial correlation).
- **C3.** Dual-signal demonstration: train regressor (weight features → merge-compatibility score for held-out adapter pairs), compare weight-only / behavior-only / dual-signal R² and Pearson on test set.

### Closest priors (knowledge-graph anchors)
- **W2T (2603.15990)** — provides QR+SVD canonical decomposition. Use their machinery directly.
- **AsymmetryOfLoRA / Hayou 2406.08447** — proves B clusters by task across seeds; predicts C1 will hold.
- **Structure Is Not Enough (Meynent et al. 2503.17138)** — argues structure-only is insufficient; predicts C3 (dual signal beats either alone).
- **ViT Model Zoo (Schürholt 2504.10231)** — same set-up philosophy, different domain. Direct prior to differentiate from.
- **Learning on LoRAs / GLNet (Putterman 2410.04207)** — equivariant baseline; we beat or match without learned encoder.

### Why this is a workshop-grade result
Each of C1, C2, C3 is a clean falsifiable claim with corpus-based predictions. Two of three holding cleanly = strong workshop submission. All three holding = also a section of the ICLR paper.

---

## E2 — Trajectory Geometry (Section 5, the main contribution)

### Question
Given the same LoRA population *with checkpoints*, how does each adapter's post-quotient coordinate evolve over training? Is convergence to the task-shared subspace monotonic, abrupt, or path-dependent? Does the trajectory's *shape* (not just its endpoint) predict downstream properties?

### Setup additions over E1
- Same training runs, but **save checkpoints every 50 steps** (so each LoRA gives 10–30 trajectory points depending on training length)
- Total trajectory points: ~3000–6000 across the population
- **Per-checkpoint measurements:** TRS subspace at that step, alpha (HT-SR power-law exponent — use **WeightWatcher** tool), d_task estimate, Grassmannian distance from current state to (a) initialization, (b) endpoint of same run, (c) population centroid

### Headline measurements
- **T1. Convergence dynamics.** Plot d_G(checkpoint_t, endpoint) vs. t for many runs. Shape: monotonic? Step-function (phase transition)? Path-dependent? Quantify with a phase-transition statistic.
- **T2. Path vs speed.** For pairs of same-task runs that hit identical final accuracy, are their trajectories *the same path traversed at different speeds*, or *different paths*? Use Dynamic Time Warping on Grassmannian distance vs. step.
- **T3. Early-trajectory predictor.** Train a regressor: trajectory features at step T (where T = 25%, 50% of total training) → endpoint TRS subspace identity. If it predicts well at T=25%, you've shown trajectory carries early-emerging task signal.
- **T4. Trajectory features predict downstream.** Beyond endpoint, do trajectory features predict (a) mergeability of two adapters, (b) forgetting on held-out tasks, (c) generalization? Compare against endpoint-only baselines.

### Closest priors (knowledge-graph anchors)
- **A Model Zoo on Phase Transitions in Neural Networks (Schürholt 2504.18072)** — phase definitions for full models. Borrow their phase machinery, extend to LoRA trajectories. THE prior to directly cite as foundation.
- **From Spikes to Heavy Tails (corpus, 2406.04657)** — describes 5+1 spectral phases of training. Operationalize on LoRAs; show LoRA trajectories pass through these phases too.
- **AlphaLoRA HT-SR Layer Quality (corpus, 2410.10054)** — alpha as quality metric. Use WeightWatcher to compute alpha per checkpoint per layer.
- **Linear Mode Connectivity (Frankle 1912.05671)** — full-network LMC. Frame ours as LoRA-LMC.
- **Mechanistic Mode Connectivity (Lubana 2211.08422)** — connects connectivity to mechanism similarity. Cite for the "trajectory implies mechanism" framing.
- **Linear Connectivity Reveals Generalization Strategies (Juneja 2205.12411)** — BERT fine-tunes can be linearly disconnected. The honest falsifier; we're testing whether LoRA fine-tunes on well-pretrained backbones are connected.
- **Spectral Dynamics of Weights (corpus, 2408.11804)** — spectrum evolution during training. Most direct full-network analog.
- **NN as Spin Models (corpus, 2408.06421)** — physics-grounded phase-transition framing for cross-domain depth.
- **Implicit Regularization Matrix Factorization Gunasekar (corpus, 1705.09280)** — theoretical: GD on factorized matrix → sparse spectrum. Predicts which directions show up first in trajectory.
- **EigenLoRAx (corpus, 2502.04700)** — task-invariant principal subspaces; their endpoint observation is consistent with LoRA-LMC.
- **Compress then Serve (corpus, 2407.00066)** — joint diagonalization across thousands of LoRAs; confirms shared subspace structure exists.

### Why this is the ICLR contribution
LMC is well-studied for full networks. Trajectories of full networks are well-studied (Saxe, Hanin, Mahoney). But **trajectories of LoRAs in the GL(r)-quotient regime are not yet a literature**. The corpus has *every component* — phase transitions (Schürholt), spectral evolution (Martin-Mahoney), GL(r) invariance (Putterman, Hayou) — but no one has assembled them into a clean trajectory study with the LoRA-LMC framing. **The wedge is the assembly.**

---

## Predictive Demonstration (Section 6)

The dual-signal claim isn't just "weights + behavior > weights alone." It is "*trajectory* features add information that endpoint+behavior together miss." Test on three downstream tasks:

1. **Mergeability prediction.** Pick 200 random adapter pairs from the population. Actually merge them; measure post-merge accuracy drop. Train predictors: (a) endpoint-weights-only, (b) endpoint-weights + behavior, (c) endpoint + trajectory + behavior. The trajectory variant must beat (b) measurably for the headline claim.
2. **Forgetting prediction.** For each LoRA, measure forgetting on held-out tasks. Predict from same three feature sets. Trajectory variant predicts where the path *crossed into W₀'s top-SV space* even if endpoint looks clean.
3. **Out-of-distribution generalization.** Hold out a task variant; predict performance. Trajectory variant captures *generalization strategy* differences (Juneja 2022 evidence that trajectory-shape encodes strategy).

If at least 1 of 3 has trajectory > endpoint+behavior with statistical significance, the headline result holds.

---

## Risks and Falsifiers (be honest)

| Risk | What kills the paper | Mitigation |
|---|---|---|
| Same-task collapse fails at endpoint (C1 negative) | LoRA-LMC's premise is wrong | Try multiple base models; check with GELoRA's d_task estimate; if all fail, reframe paper around the falsification result (still publishable as "LoRA-LMC fails for these reasons") |
| Region 2 doesn't carry behavior (C2 negative) | Three-region story is wrong | Use whole canonical ΔW; lose the elegant decomposition; paper still works on dual-signal claim |
| Trajectory looks identical across all runs (T1 trivially monotonic) | "Path vs speed" reduces to just speed | This is *also* a finding — "same task, same path, different speeds" is a clean result. Pivot section 5 framing. |
| Trajectory features don't predict downstream (Section 6 negative) | Headline claim sinks | Workshop fallback with E1 only; come back to E2 next year |
| Cross-arch comparison fails (stretch dies) | Lose stretch goal | Drop cross-arch from paper; section 5 is enough |
| Compute budget overruns | Can't train 200 LoRAs | Drop to 100 (5 tasks × 4 seeds × 5 variations); use Qwen2.5-3B instead of LLaMA-3-8B for half the cost |

The most important risk is the *first* — same-task collapse must hold at endpoint. AsymmetryOfLoRA + EigenLoRAx + Compress-then-Serve all suggest it does. If it doesn't hold for our specific setup, falsification is the paper.

---

## Compute Budget

- 200 LoRAs × ~30 min per training run on a single A100 = ~100 GPU-hours
- Eval (LM-Eval-Harness, 8 tasks per LoRA) = ~5 min per LoRA × 200 = ~17 GPU-hours
- Checkpoint storage: ~50MB per LoRA × 30 checkpoints × 200 = ~300 GB (manageable)
- Analysis (CPU): SVD, Grassmannian distance, alpha computation = trivial

**Total: ~120 GPU-hours**, achievable on a single A100 over 3 months at ~14 hours/week or one rental burst.

---

## Tools to Use

### Critical
- **WeightWatcher** (Charles Martin / Mahoney) — open-source diagnostic tool. Computes HT-SR alpha, ESD, layer quality metrics per layer. The deployable version of the alpha=2 criterion in the corpus. Already used by AlphaLoRA, "From Spikes to Heavy Tails," etc. **Direct line to your trajectory measurements per checkpoint.** GitHub: CalculatedContent/WeightWatcher. We will use this for per-checkpoint per-layer alpha tracking — that's how T1 (phase detection) and T3 (early-trajectory prediction) become measurable. Mahoney is at Berkeley, his group co-authored SANE in our corpus, and WeightWatcher is the bridge from theory to deployable measurement.
- **PEFT (HuggingFace)** — LoRA training infrastructure
- **LM-Eval-Harness** — standardized benchmarks
- **W2T's QR+SVD code** — if released; otherwise reimplement (it's ~50 lines)

### Nice-to-have
- **Geoopt** (Riemannian optimization library) — for Grassmannian distance computation
- **Anaconda + Wandb** — experiment tracking
- **A100 / H100 access** — single GPU sufficient

---

## Beyond ICLR 2027 — The Self-Evolving Agent Vision

The 3-paragraph PhD research statement writes itself once E2 is in hand:

**Paragraph 1 (what I did):** *I formulated and tested the LoRA-LMC conjecture: under the GL(r)-quotient, fine-tuning trajectories on the same task collapse onto a shared low-dimensional subspace. Empirical results show this holds on well-pretrained LLM backbones. The trajectory's shape — beyond just its endpoint — predicts mergeability, forgetting, and generalization that endpoint analysis cannot recover.*

**Paragraph 2 (what this opens):** *Trajectory geometry is a measurement instrument for fine-tuning. It enables cheap pre-flight prediction of training outcomes, structural understanding of when capabilities emerge, and a path toward weight-space explanations of model behavior that don't require behavioral evaluation.*

**Paragraph 3 (the long-term vision):** *I want to extend this toward agents that read their own trajectory information at deployment time — to predict capability gaps, anticipate forgetting before it happens, decide what to learn next, and ground self-knowledge in measurable structure rather than behavioral guesswork. This is foundational infrastructure for self-evolving systems.*

That paragraph hits **training dynamics** (Saphra, Hanin, Mahoney), **mechanistic interpretability** (Bau, Anthropic), and **agents** (Levine, Finn, Salakhutdinov) simultaneously.

---

## Where the Knowledge Graph is Loud (read these in order)

For E1 (endpoint section), priority reading:
1. `arxiv_2503_17138.md` — Structure Is Not Enough (THE prior to differentiate)
2. `w2t_lora_weights_know_capabilities.pdf` — provides QR+SVD machinery
3. `arxiv_2406_08447.md` — Hayou AsymmetryOfLoRA (theoretical anchor)
4. `arxiv_2504_10231.md` — ViT Model Zoo (closest setup philosophy)

For E2 (trajectory section), priority reading:
1. `arxiv_2504_18072.md` — Phase Transitions Zoo (THE foundation for phase machinery)
2. `arxiv_1912_05671.md` — Frankle LMC (formal cousin)
3. `arxiv_2211_08422.md` — Mechanistic Mode Connectivity (framework E2 sits inside)
4. `arxiv_2205_12411.md` — Juneja LMC reveals generalization (confirms trajectory carries strategy info)
5. `from_spikes_to_heavy_tails_spectral_evolution.pdf` — 5+1 phases of training spectrum
6. `implicit_regularization_matrix_factorization_gunasekar.md` — implicit bias of GD; predicts spectrum sparsity

For the agent vision (PhD pitch), priority reading:
1. `arxiv_2503_20228.md` — TeleLoRA (cross-LLM alignment teleportation; closest existing "agent uses LoRA structure" work)
2. `arxiv_2502_09619.md` — ProbeLog (zero-shot model search from weights; capability lookup ancestor)
3. `arxiv_2503_10633.md` — Atlas of Models (visionary positioning paper)

---

## What I Will Not Do This Year

To stay focused:
- No cross-architecture comparison as headline (only as stretch)
- No new architecture proposal (no GrassmannLoRA, no Capability-Reserved Pretraining)
- No LS-Merge style autoencoder (linear methods only; cite LS-Merge as future-work alternative)
- No self-evolving agent implementation (only argued for in discussion section)
- No theoretical proof of LoRA-LMC (empirical paper; theory comes after)

These are explicitly **future work** — they are paragraph 2 and 3 of the research statement, not paper sections.

---

## Status

- **Plan:** committed
- **Corpus:** 96+ papers, 1761/1909/169 graph
- **Observations doc:** `weightBench/finding_literature/observations_lora_lmc_program.md` (companion document)
- **Next action:** Set up the LoRA training pipeline. Pick the 8 tasks. Start week 1.

---

*Last updated 2026-05-07.*
