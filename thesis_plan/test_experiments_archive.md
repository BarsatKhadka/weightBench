# Test Experiments Archive — Consolidated Findings

> Snapshot before deletion of `thesis_plan/test_experiments/`.
> Captures every result, parameter, and reading required to reconstruct
> or cite these runs without the code. Source of truth was
> `thesis_plan/test_experiments/INDEX.md` plus per-experiment `results/`.

## Common substrate

- **Base model (most runs):** Qwen/Qwen2.5-0.5B-Instruct, bf16 (fp16 NaNs on long sequences).
- **LoRA config (controlled pools):** r=16, α=32, dropout=0.05, target = all 7 linear modules (q,k,v,o,gate,up,down).
- **Hardware:** Windows + 8GB CUDA GPU + ≥16GB RAM. Bottleneck = system RAM, not VRAM. Adapter files ~50MB each.
- **Discipline:** plan.md untouched. Findings only promoted on user trigger.
- **Reference-frame outcomes** (A11) condition every higher-level claim in A1–A10.

---

## 1. A11 — Reference Frame Alignment  *(Tier 1, CPU, ~9 min, ~$0)*

**Falsifies:** conditions A1–A10. **Status:** DONE — Outcome (2) frames orthogonal.

- Mean principal angle θ(U_W₀, U_S*) = **84.03°** across 10 layers (range 81.6–86.4°).
- U_S* lives in W₀'s **middle** (top-256 alignment 0.185; bottom-256 alignment 0.170; near-equal).
  → **Refutes PiSSA (top-W₀) and MiLoRA (bottom-W₀) initialization rationales** on average.
- U_S* captures **68 %** of cross-LoRA ΔW variance.
- Q vs V asymmetry corroborated: q_proj depth-dependent with low bottom-W₀ alignment; v_proj roughly symmetric.
- **Cascade:** Cross-LoRA's `ρ_AB` aligns *W₀* bases, but A11 says LoRA signal lives in U_S* ⊥ W₀ top → forces revision of A10/A16's cross-arch story.

---

## 2. A01 + A07 — Analytic Mergeability + Spectrum Baseline  *(Tier 1, CPU, ~1 min, K=10)*

Geometric instrument only — merge-accuracy ground truth deferred to `mergeability_qwen`. felixml dropped (rank-256 safetensors → uncatchable Rust mmap segfault on Windows). 45 pairs × 10 layers.

- **A01 mean 0.975, median 0.983, range 0.849–0.990.** Most pairs near-orthogonal in Region 2.
- Top 8 most-aligned pairs all "lovepon q,v r=8" same-setup pairs regardless of task. The same-task math/math pair ranks 27/45 — different rank + target modules ⇒ different ambient subspace.
- **Reading: rank/target-module confound dominates task signal on uncontrolled pools.** Validates plan.md E1's fixed-parameterization mandate empirically.
- Q vs V asymmetry corroborated 3rd time (A11 + Synth 22 + here). V-layers mean A01 = 0.978 > Q-layers 0.971.
- Depth pattern: layers 0 and 31 lower A01 (more alignment) than middle 8/16/24 — middle attention most task-specific.
- **A07** spectrum-only baseline ranks pairs differently from A01 → captures magnitude rather than direction.

---

## 3. Controlled-pool C1 (synthetic)  *(iter_022, Tier 2, CUDA, ~30 min train + ~15 s analysis)*

15 LoRAs on Qwen-0.5B-Instruct, tasks {add_mod, mul_mod, max}, 5 seeds each. Eval acc 93–100 % across all 15.

- same-task pairs (n=30): A01 mean **0.846 ± 0.018**
- diff-task pairs (n=75): A01 mean **0.901 ± 0.012**
- gap 0.055, pooled-std **σ = 3.52**, 13/15 closest pairs same-task.

**Per-task within-cluster structure encodes training dynamics:**
- add_mod (smooth convergence) — tightest cluster, lowest std.
- max (loss=0 from start, no learning) — noise-like, highest std.
- mul_mod (grokking transitions) — consistently loose cluster.

---

## 4. E2 Trajectory  *(iter_023, Tier 2, CUDA, re-train +30 min, analysis ~3 min)*

Same pool re-trained with `--save_every 25` ⇒ 11 intermediate ckpts + endpoint per LoRA. 168 layers × 12 timepoints.

**T2 same vs diff d_G across training:**
| step | same μ±σ | diff μ±σ | gap | σ |
|---|---|---|---|---|
| 25 (8 %) | 0.826 ± 0.023 | 0.899 ± 0.014 | +0.073 | **3.74** |
| 100 (33 %) | — | — | +0.060 | 3.52 |
| 276 (endpoint) | — | — | +0.055 | 3.52 |

- **Collapse signal fully present at step 25; does not grow.** σ actually shrinks 3.74 → 3.52.
- **T3 task-ID prediction at 33 %:** 15/15 (random 28.6 %). Corollary of T2, not independent.
- **T1 per-task convergence shape** distinguishes 3 dynamical regimes — per-seed max single-step d_G drop std: add_mod 0.020, mul_mod 0.016 (but max-drop *step* varies 50/75/125/50/275), max **0.105** (5× larger, pure noise).
- mul_mod's per-seed-different-step grokking is exactly what endpoint-only analysis misses.
- **A4 (tangent subspaces at matched arclength) still untested.** Needs a 30+ LoRA pool to confirm σ-shrink as headline.
- **Applied use-case:** adapter-pool registries / merge-pool curation at scale — read early-trajectory subspace once instead of running inference per adapter.

---

## 5. Real-task C1  *(iter_024, Tier 2, CUDA, ~75 min train + ~30 s analysis)*

14 LoRAs (4 boolq + 5 agnews + 5 rt; boolq_789 OOM-dropped on long passages). Same fixed param.

- same-task pairs (n=26): A01 **0.861 ± 0.009**
- diff-task pairs (n=65): A01 **0.925 ± 0.004**
- pooled-std sep **≈ 11** (Cohen's-d-like; not a p-value — 91 pairs from 14 LoRAs are correlated).
- **All top-15 closest pairs same-task** (synthetic was 13/15).

**Output-vocabulary hypothesis refuted** via per-module/per-depth diagnostic:
- attention separates same vs diff *more* than MLP (sep 10.84 vs 9.87) — opposite of output-vocab prediction.
- MLP A01 0.93–0.99 across pairs (near-orthogonal regardless of task); same-task overlap lives in attention.
- depth: mid ≈ late > early (10.95 / 10.56 / 8.20) — task circuits mid-late, not "output decisions in late".

**Honest comparison to synthetic:** earlier framing called σ "stronger than synthetic" — that's partly synthetic-pool flaws (max no-learning inflates same-task std; add_mod/mul_mod share algebra inflates diff-task std). Fair statement: C1 holds on both, well above plan.md's 5σ-on-200-LoRAs target.

**Pending:** `Σ sin²θ → accuracy-drop` regression still needs actual merges + held-out eval.

---

## 6. Substep Lock-in + Region Emergence  *(Tier 2, CUDA ~3 min train + ~25 min CPU)*

- **Lock-in at step 2** (faster than iter_023's step 25 finding on synthetic).
- **σ peaks at step 14 (4.12)**, then erodes through training.
- **R1/total constant at 0.30 from step 25** — three-region emergence: universal fiber stable share early.

---

## 7. Trajectory MDS  *(Tier 1, CPU, ~30 s)*

2D embedding of 144 (LoRA, step) points.

- **Task identity = neighborhood, not point.** Same-task seeds walk different paths to different endpoints *within* shared regions.
- Reframes plan.md A4 from "path vs speed" to "neighborhood vs trajectory".

---

## 8. LMC interp (synthetic, n=6)  *(Tier 2, CUDA ~15 min)*

Linear interp of dW between LoRA pairs.

- Same-task: **no midpoint collapse.**
- Diff-task: **plateau-then-cliff** (NOT linear addition).
- Forgetting on max real and reversible.
- **A6 (Grassmannian-geodesic) NOT confirmed.**

## 9. LMC interp (real tasks, n=6 on iter_024 pool)  *(Tier 2, CUDA ~10 min)*

- Same-task LMC replicates.
- Diff-task **plateau-then-cliff is synthetic-specific** — real curves are *smooth crossfades*.
- Cross-task LoRA sometimes beats same-task on target task.
- A1 framing depends on training regime.

---

## 10. Cross-task help probe  *(iter_028 surprise, Tier 1 CPU ~5 min)*

Diagnostic on n=14 pool.

- Magnitude only partial signal.
- Shared-direction hypothesis **ruled out.**
- **Same-task LoRAs LESS vec-cosine-aligned than diff-task** — new geometric distinction: direction-set vs pattern.
- Mechanism not yet explained.

## 11. Cross-task matrix (14 × 3 accuracy matrix)  *(Tier 2, CUDA ~10 min)*

- Cross-task help on boolq replicates at population level (agnews mean 0.65 > boolq 0.58).
- rt best is a **tie:** rt_456 = boolq_456 = 0.87.
- Seed variance enormous: boolq seeds span 0.41–0.74 on own task; 0.08–0.87 on rt.
- **"Destructive vs preserving" LoRAs are seed-driven, not task-driven.**

---

## 12. Destructive vs preserving (geometric probe, n=2 contrast)  *(Tier 1, CPU ~3 min)*

Why is boolq_42 destructive?

- **Mid-network MLP ||dW|| signature** for destructive: L12–L13 gate/up_proj **+0.12–0.17 larger**.
- vec-cosine seed-locked not task-locked (~30× same-seed alignment).
- Subspace overlap (A01) doesn't predict behavior alone — need magnitude predictor.

## 13. Destructive intervention (causal MLP scaling)  *(Tier 2, CUDA ~5 min)*

**Causal test:** zero ALL MLP from boolq_42.

| Model | boolq | agnews | rt |
|---|---|---|---|
| M0 base | 0.41 | 0.38 | 0.37 |
| M1 boolq_42 full | 0.56 | 0.14 | 0.08 |
| **M2 boolq_42 zeroMLP** | **0.51** | **0.34** | **0.26** |
| M3 rt_1024 full | 0.03 | 0.51 | 0.86 |
| M4 rt_1024 zeroMLP | 0.43 | 0.49 | 0.84 |
| M5 both full | 0.55 | 0.34 | 0.70 |
| M6 both zeroMLP | 0.54 | 0.36 | 0.84 |
| M7 boolq_zeroMLP + rt_full | 0.58 | 0.35 | 0.86 |

**Reading:** Zeroing MLP preserves **91 %** of boolq (0.56 → 0.51), recovers agnews to near-base (0.14 → 0.34), partially recovers rt (0.08 → 0.26).
**Attention carries task signal; MLP carries destructive interference.** Asymmetric recipe (M7) is the best of all worlds.

---

## 14. Continual learning recipe (extension of #13)

- `continual.json` replays #13's M0–M7 numbers.
- **Five-way `K3_asym_recipe`** (zero-MLP boolq + full rt + agnews handled accordingly): boolq 0.46, agnews **0.85**, rt **0.86**. Beats both K1 all-full (0.47/0.78/0.48) and K2 all-zeroMLP (0.49/0.80/0.88) on aggregate.
- **Ensemble runs:**
  - agnews_ensemble_full: 0.0 / 0.84 / 0.0 (collapses all but agnews)
  - **agnews_ensemble_zeroMLP: 0.65 / 0.87 / 0.57** (preserves base capability!)
  - rt_ensemble_zeroMLP: 0.29 / 0.62 / 0.82
  - boolq_ensemble_zeroMLP: 0.59 / 0.21 / 0.82
- **Generalization:** "zero MLP, keep attention" recipe is a reusable continual-learning trick — preserves base capability across tasks, attention LoRAs compose, MLP LoRAs interfere.

---

## 15. Mergeability (linear-additive dW merge, n=6 pairs, 100 eval samples each)

Solo→merged drops for 0.5/0.5 weighted dW sum:

| Pair (a01) | task_a | task_b | agg_drop | notes |
|---|---|---|---|---|
| agnews_123 + agnews_42 (0.859) | same | — | **0.010** | tight |
| agnews_456 + boolq_1024 (0.929) | diff | — | 0.020 | |
| agnews_789 + rt_42 (0.927) | diff | — | **−0.020** | *gain* |
| boolq_42 + boolq_456 (0.850) | same | — | **0.000** | |
| boolq_123 + rt_789 (0.920) | diff | — | **−0.060** | *gain* |
| rt_1024 + rt_456 (0.868) | same | — | **−0.015** | *gain* |

- **Half of pairs gain accuracy under merge** (negative drop). LMC merges robust at this scale.
- a01 ↔ merge-drop correlation weak in n=6; needs ≥30 pairs for the Σ sin²θ regression headline.

---

## 16. Path Decomposition  *(Tier 2, CUDA, dense ckpts)*

After iter_023's step-25 lock-in, decomposes Phase B (post-lock-in) path into independent measurables to discriminate three hypotheses:

1. Pure magnitude scaling (subspace fixed, ||dW|| grows)
2. Spectrum redistribution toward HTSR α ≈ 2 + rank-collapse event
3. Slow direction drift

**Theory anchors:** Yunis et al. 2024 (direction stabilizes early, magnitude late); Martin–Mahoney HT-SR 5+1 phases; Synth 24 (grokking as simultaneous D↘1, α↘2, LLC drop, rank collapse); Synth 17 (R1 universal vs R2 task-specific).

**Setup:** Qwen-0.5B; r=16, α=32, all-7-target; tasks boolq/agnews/rt; seeds 42, 123; 300 steps each. Dense ckpts: every 2 steps to 50, every 10 to 150, every 25 to 300. 6 probe layers (attn + mlp at depth 0/11/23 of 24).

**Measurements per ckpt × layer:**
| ID | What | Formula |
|---|---|---|
| D1 | Canonical subspace | left SVs of dW = scaling·B·A |
| D2 | Full spectrum | σ_i(dW) |
| D3 | MP-threshold + above-MP count | σ_noise·(√m + √n) |
| D4 | HTSR α | power-law MLE on top half of σ² |
| D5 | R1/R2 split | project onto W₀ top-64 left subspace |
| D6 | d_G(t, T) | Grassmannian dist to endpoint |
| D7 | velocity d_G(t-1, t) | step-to-step subspace change |
| D8 | spectrum dist to endpoint | ‖σ(t) − σ(T)‖ / ‖σ(T)‖ |
| D9 | cross-LoRA d_G(t) | same vs diff at every step |

**Outcome key (paper headlines):**
| Pattern | Reading |
|---|---|
| D6 ↘ fast, D8 stays high | Direction-magnitude separation confirmed for LoRA |
| D5: R1 half-step ≪ R2 | Universal fiber locks in before task signal |
| D4 α monotone ↘ 2 | LoRA reaches HTSR Phase 5 — universal stopping criterion |
| D3 count peaks then drops | Rank-collapse event directly observed (first measurement) |
| All three | **HEADLINE:** two-phase commit-then-polish with measurable markers |

**Bad outcomes — interpretations preserved:**
- Everything noise → wrong probe layers or r too low.
- Direction & magnitude lock together → Yunis fails for LoRA, important null.
- α never approaches 2 → undertrained, retry 600–1000 steps or higher LR.
- No rank-collapse → matches Alignment Collapse's t⁴ intruder-dim growth.

---

## Cross-experiment claim ledger (what survives, what's pending)

**Validated:**
- C1 same-vs-diff subspace collapse on both synthetic (3.52σ) and real-task (~11 pooled-std).
- Step-25 lock-in (extended to step-2 on substep run).
- Asymmetric "zero MLP, keep attention" recipe — destructive interference is MLP-localized, attention composes.
- Q vs V asymmetry (3 independent runs: A11, A01, Synth 22).
- Mid-attention carries the most task-specific subspace.
- LMC merges robust on real-task pool (half of 6 pairs gain accuracy).
- Diff-task LMC plateau-then-cliff is **synthetic-specific**; real tasks crossfade.
- PiSSA/MiLoRA top-vs-bottom-W₀ rationales refuted (U_S* sits in middle).

**Pending / needs more pairs:**
- A4 tangent-subspaces-at-matched-arclength test.
- A6 Grassmannian-geodesic LMC.
- Σ sin²θ → merge-accuracy-drop regression (need ≥30 pairs).
- σ-shrink across training as headline (need 30+ LoRA pool).
- A2 four-estimator t*, A5 Karcher mean, A8 anti-grokking detector, A9 LLC, A10 Cross-LoRA ρ_AB, A13 PIGMM, A17 audit tool.

**Refuted / reframed:**
- Output-vocabulary explanation of C1.
- Shared-direction hypothesis for cross-task help.
- "Destructive vs preserving" as task property — it's seed-driven.
- Cross-LoRA ρ_AB cross-arch story (A11 forces revision).

---

## File-level provenance (what was where)

```
test_experiments/
├── INDEX.md                            ← status table + per-result writeups
├── a01_analytic_mergeability/          ← K=10, 45 pairs, A01+A07 raw json
├── a07_spectrum_baseline/              ← spectrum-only baseline (paired with A01)
├── a11_reference_frame_alignment/      ← θ(U_W₀,U_S*), 10 layers, results.json
├── controlled_pool_qwen/               ← iter_022 + iter_023 trajectory pool
│   ├── results/results.json
│   └── results_traj/results.json
├── real_tasks_pool_qwen/               ← iter_024, 14 LoRAs, results.json
├── substep_lockin_qwen/                ← step-2 lock-in + region emergence
│   ├── results_region_emergence/
│   ├── results_region_substep/
│   └── results_traj_embedding/
├── lmc_interp_qwen/                    ← synthetic LMC n=6
├── lmc_interp_real/                    ← iter_024 LMC n=6
├── cross_task_help_qwen/               ← mechanism probe (n=14)
├── cross_task_matrix/                  ← 14×3 accuracy matrix
├── destructive_intervention/           ← causal MLP zeroing
│   └── results/intervene.json          ← M0–M7 numbers
├── continual_learning_recipe/          ← extension: continual/ensemble/five-way
│   └── results/*.json
├── mergeability_qwen/                  ← n=6 LMC merges + 100-sample eval
│   └── results/merge_results.json
└── path_decomposition/                 ← Yunis + HTSR + region split
    ├── README.md                       ← protocol
    └── INTERPRETATION.md               ← outcome key (preserved above)
```

Original status table and prose in `test_experiments/INDEX.md` — every
number above is traceable to a `results/*.json` in the corresponding
subfolder.
