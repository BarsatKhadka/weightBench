# Iteration 42 — 2026-05-10 — Path decomposition (PATH-A through PATH-E unified)

After deep corpus re-reading (the 5+1 HTSR phases, Yunis direction-vs-magnitude
separation, Synthesis 24's unified grokking event, Synthesis 17's per-region
split, and our own iter_023 step-25 lock-in), iter_042 builds the single
densest training-trajectory measurement the project has run so far.

**Premise.** iter_023 established that the Grassmannian subspace locks in by
step 25 (8% of training) on synthetic tasks. The deeper question is **what
the path does AFTER lock-in**. Three hypotheses:
1. Pure magnitude scaling (1D ray)
2. Spectrum redistribution within fixed subspace
3. Slow direction drift

iter_042 measures direction, spectrum, alpha, region 1/2 split, velocity,
and cross-task d_G all on the same training data, in order to distinguish
these.

## Setup

- Qwen-2.5-0.5B-Instruct, LoRA r=16 α=32, all 7 target modules
- 3 tasks × 2 seeds = 6 LoRAs
- 300 steps each
- Dense checkpoint schedule: every 2 steps for 0-50, every 10 for 50-150,
  every 25 for 150-300 (~42 ckpts per LoRA)
- 6 probe layers (attn + mlp at depths 0, 11, 23)

## Measurements (per checkpoint per probe layer)

| ID | Object |
|---|---|
| D1 | Canonical column subspace |
| D2 | Full singular spectrum |
| D3 | Marchenko-Pastur threshold + above-MP count |
| D4 | HTSR α (power-law MLE on σ² tail) |
| D5 | Region 1 (W₀-aligned) vs Region 2 (W₀-orthogonal) subspaces |
| D6 | d_G(t, T) direction-to-endpoint |
| D7 | d_G(t-1, t) step velocity |
| D8 | ‖σ(t) - σ(T)‖ / ‖σ(T)‖ spectrum-to-endpoint |
| D9 | Cross-LoRA d_G at every step (same-task vs diff-task) |

## Results

TBD (training in progress; this section will be filled after analysis).

## Catalog state after iter_042

TBD
