# WeightWatcher — Reference for the LoRA Region-Anatomy Project

Practical reference for using WeightWatcher (WW) inside this project. WW is
*the* tool for the spectral-scalar side (per-layer α, MP fits, ESD plots). It
does **not** cover the geometric side (Grassmannian, region split, population
analysis) — those we write ourselves. Together they cover the full anatomy.

GitHub: <https://github.com/CalculatedContent/WeightWatcher>
Theory: Martin & Mahoney, *"Implicit Self-Regularization in Deep Neural Networks"* (JMLR)
        Martin et al., *"Predicting Trends in the Quality of State-of-the-Art Neural Networks"* (Nature 2021)

---

## TL;DR — what it does for us

For each checkpoint, for each LoRA layer, compute **one scalar** that
characterizes how "well-trained" that layer is, via Heavy-Tailed
Self-Regularization (HT-SR) theory:

- `alpha` — power-law exponent of the layer's spectrum. **α ≈ 2 ⇒ well-trained.**
- `alpha_weighted` — scale-adjusted α (multiplies α by log of the top eigenvalue)
- `stable_rank` — effective rank
- `num_spikes` — how many eigenvalues poke above the MP random baseline
- `log_norm`, `log_spectral_norm`, `mp_softrank` — supporting scalars

Across our 10 LoRAs × 40 checkpoints × 28 layers × 7 modules, WW gives us a
**huge scalar table** to feed into trajectory plots, phase classifiers, and
cross-seed aggregates.

---

## Install (Magnolia)

```bash
source $HOME/weightBench/.venv/bin/activate
pip install weightwatcher
python -c "import weightwatcher as ww; print(ww.__version__)"
```

No CUDA needed — WW works on the CPU on weight matrices it loads from a PyTorch
model. Run from cpuq partition or login.

---

## Core API (single model)

```python
import weightwatcher as ww
from transformers import AutoModelForCausalLM
from peft import PeftModel

base = AutoModelForCausalLM.from_pretrained(BASE_PATH, torch_dtype="bfloat16")
model = PeftModel.from_pretrained(base, ADAPTER_PATH)

watcher = ww.WeightWatcher(model=model)

# THE key call for our project — analyze the LoRA delta (BA), not the merged model
details = watcher.analyze(peft=True)
# 'peft=True'         → analyzes ΔW = BA, tags layers with 'lora_BA' in name
# 'peft="with_base"'  → analyzes W₀, ΔW, and W₀+ΔW (3x the rows)
# 'peft="peft_only"'  → only the LoRA delta, no base layers

summary = watcher.get_summary(details)   # one row per layer
print(details.head())
print(summary)
```

The `details` DataFrame returned has one row per layer with all the metrics
listed above. That's the unit we aggregate.

---

## Our use case: trajectory over checkpoints

Loop over all checkpoints of one (task, seed), collect WW output, stack into
a single DataFrame indexed by `(checkpoint_step, layer_name)`:

```python
import pandas as pd, weightwatcher as ww
from pathlib import Path
from transformers import AutoModelForCausalLM
from peft import PeftModel

BASE = Path("$HOME/weightBench/weightBench/experiment1/models/Qwen2.5-7B")
ADAPTERS = Path("$HOME/weightBench/weightBench/experiment1/adapters/hellaswag_seed0")

# load base ONCE; only swap adapter inside the loop
base = AutoModelForCausalLM.from_pretrained(str(BASE), torch_dtype="bfloat16")

rows = []
for ckpt in sorted(ADAPTERS.glob("checkpoint-*"), key=lambda p: int(p.name.split("-")[-1])):
    step = int(ckpt.name.split("-")[-1])
    model = PeftModel.from_pretrained(base, str(ckpt))
    details = ww.WeightWatcher(model=model).analyze(peft=True)
    details["step"] = step
    rows.append(details)
    del model  # free memory before next adapter

traj = pd.concat(rows, ignore_index=True)
traj.to_parquet("ww_trajectory_hellaswag_seed0.parquet")
```

Now `traj` has ~28×7×40 ≈ 7,840 rows for one (task, seed). Stack 10 seeds → 78,400 rows.
That's the full WW dataset for our pool.

**WARNING:** the loop loads the base model in memory and just swaps the adapter.
WW doesn't need GPU. Each WW call on Qwen-7B's LoRA-deltas takes ~10–30 seconds.
Full pool: ~10 LoRAs × 40 ckpts × 20s = ~2 hours single-threaded. Parallelize across
seeds using sbatch array if you want it faster.

---

## What each metric *means* (intuition for our plots)

| Metric | What it measures | What to look for |
|---|---|---|
| `alpha` | Power-law tail of layer spectrum (HT-SR) | **α → 2** over training = layer has reached "universal" well-trained regime. α > 4 = undertrained. α < 1.5 = overtrained. |
| `alpha_weighted` (`alpha-hat`) | α × log₁₀(λ_max) | Quality-and-scale combined. Higher = more meaningful structure. |
| `stable_rank` | ‖W‖_F² / ‖W‖_2² | Effective rank. Low stable_rank = concentrated into few directions. |
| `mp_softrank` | Fraction of eigenvalues above MP random baseline | How many "real" directions vs how many are noise. |
| `num_spikes` | Count of eigenvalues above MP edge | Direct count of signal directions. |
| `log_norm` | log ‖W‖_F | Total magnitude. |
| `log_spectral_norm` | log λ_max | Largest direction's magnitude. |
| `rand_distance` | KS-distance between ESD and randomized-W ESD | How far from "random matrix" — high = lots of learned structure. |

For our project the **headline scalars** are `alpha` and `num_spikes`,
both per-layer per-checkpoint. Everything else is supporting.

---

## Key plots WW can save for us

```python
details = watcher.analyze(peft=True, savefig=True, plot=True, randomize=True)
# Produces, per layer:
#   ww.layer<i>.esd1.png         # log-log ESD with PL fit
#   ww.layer<i>.esd2.png         # lin-lin
#   ww.layer<i>.esd3.png         # MP fit overlay
#   ww.layer<i>.esd4.png         # randomized comparison
```

Useful for the methods section. NOT useful at trajectory-scale (you'd generate
~7800 PNGs). For trajectory we just save the `details` table and plot
aggregates ourselves.

---

## Specific calls we'll use

### Compute α-trajectory for one (task, seed)

```python
ww_traj = compute_trajectory(adapter_dir)   # the loop above
# columns: step, layer_id, alpha, alpha_weighted, stable_rank, mp_softrank, num_spikes, log_norm, ...
```

### Phase classification per checkpoint

From "From Spikes to Heavy Tails" (2406.04657), phases are:
- Phase 1: random (α undefined or huge)
- Phase 2: bulk + spikes (α ≫ 2, few spikes)
- Phase 3: bulk decay (α decreasing)
- Phase 4: bulk-plus-spikes (α ~ 3–4)
- Phase 5: heavy tail (α ≈ 2)
- Phase 6: rank collapse (α < 2)

Quick classifier on WW output:

```python
def phase_of(alpha, num_spikes):
    if alpha > 6 or num_spikes < 2: return 1
    if alpha > 4:                   return 2
    if alpha > 3:                   return 3
    if alpha > 2.3:                 return 4
    if alpha > 1.8:                 return 5
    return 6
```

(Thresholds approximate — calibrate against the AlphaLoRA paper for exact cutoffs.)

### α-shrink across training (project headline candidate)

```python
import pandas as pd
all_traj = pd.concat([compute_trajectory(f"adapters/hellaswag_seed{s}") for s in range(10)],
                     keys=range(10), names=["seed"])
# group: how does per-layer alpha evolve and vary across seeds?
g = all_traj.groupby(["step", "layer_id"])["alpha"].agg(["mean", "std"])
# plot mean ± std vs step — does within-task std shrink over training?
```

This is the **σ-shrink test on a scalar axis**, complementing the geometric
σ-shrink (Grassmannian distance σ).

---

## What WeightWatcher does NOT do (our wedge)

Explicitly missing from WW — these are *our project's* contribution:

- ❌ No Grassmannian distance between models (subspace overlap)
- ❌ No principal angles between layers across models
- ❌ No QR+SVD canonical / GL(r) gauge fixing
- ❌ No Region 1/2/3 split (W₀-aligned vs intruder)
- ❌ No population analysis (10 same-task LoRAs at once)
- ❌ No trajectory-level statistics across checkpoints (one-model API)
- ❌ No same-task-vs-different-task clustering
- ❌ No mergeability or forgetting prediction
- ❌ No path-shape / DTW / lock-in detection

WW gives us the per-layer α scalar; we build everything else around it.

---

## How WW slots into the analysis pipeline

```
checkpoints/
   ├── WeightWatcher (per-layer α, num_spikes, mp_softrank, ...)  ← spectral scalars
   ├── canonical.py    (QR+SVD per layer)                         ← gauge-fixed coord
   ├── region_split.py (against W₀, MP threshold)                 ← R1/R2/R3 mass
   ├── pairwise_grassmannian.py                                   ← subspace distances
   └── trajectory.py   (over all checkpoints, all seeds)          ← assembles everything
```

WW is the *first column* of the master `analysis_table.parquet`. The other columns
are computed by our own scripts on the same checkpoints.

---

## Citations to include in the paper

Mandatory citations whenever you use α or HT-SR language:

- Martin, C. H., & Mahoney, M. W. (2018). *Implicit Self-Regularization in
  Deep Neural Networks: Evidence from Random Matrix Theory.* JMLR.
- Martin, C. H., Peng, T., & Mahoney, M. W. (2021). *Predicting Trends in
  the Quality of State-of-the-Art Neural Networks Without Access to
  Training or Testing Data.* Nature Communications.
- WeightWatcher tool: <https://github.com/CalculatedContent/WeightWatcher>

For LoRA-specific use:

- See `finding_literature/alphalore_htsr_rank_allocation.pdf` (AlphaLoRA) for
  how others have applied α to LoRA rank decisions — directly relevant prior.

---

## Cross-references to project memory

- [[project-anatomy-of-lora-region]] — WW is one instrument in the anatomy toolkit
- [[project-path-vs-anatomy-distinction]] — α-trajectory is the scalar version
  of the path-structure claim
- [[feedback-geometry-first-eval-deferred]] — WW outputs are weight-space
  measurements, not behavioral eval; consistent with the geometry-first stance
- See `LEARNING.md` Tier 1 #4 for the HT-SR reading prerequisites before
  interpreting WW output
