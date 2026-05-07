# Synthesis 27: NTK vs. Feature Learning Regime in LoRA — Where Grokking Lives

**Date:** 2026-05-07
**Session:** 5
**Previous synthesis:** synthesis_night_run_26_platonic_aristotelian_region1_region2_S.md

---

## The Tension

NTK paper (lora_ntk_regime_no_spurious_minima.pdf) says:
    r >= sqrt(N) → no spurious local minima → global convergence guaranteed

SLT/Arrhenius (synthesis 20) says:
    t_grokking ~ exp(c(r - d_task)log(n)) → exponential delay, competing basins

These seem contradictory: if NTK guarantees global convergence, why does grokking happen?

No path in graph between "Rank Threshold r >= sqrt(N)" and competing basins / Arrhenius.

The resolution: they apply to DIFFERENT REGIMES of LoRA training.

---

## Two Regimes of LoRA Fine-Tuning

**NTK Regime** (large rank, lazy training):
- r >= sqrt(N): sufficient rank for NTK condition
- LoRA weights barely move from initialization (stay in the "lazy" regime)
- Loss landscape is convex-like (no competing basins, no grokking)
- Optimization converges directly to the unique global minimum
- Price: massive parameter count (r = sqrt(N) for N samples = e.g. r ≈ 180 for N = 32K examples)
- All stationary points are global or saddle points (no spurious local minima)

**Feature Learning Regime** (smaller rank, active adaptation):
- r << sqrt(N): below NTK threshold, but r can still be >= d_task
- LoRA weights make large moves from initialization
- Loss landscape has competing basins (memorization vs. generalization)
- Grokking is the escape mechanism from memorization to generalization basin
- Price: exponential grokking delay t ~ exp(c(r - d_task)log(n))
- The SLT competing-basins picture applies here

---

## The Phase Boundary

The NTK threshold r = sqrt(N) is the PHASE BOUNDARY between regimes.

    r >= sqrt(N): NTK regime (lazy, global convergence, no grokking)
    d_task <= r < sqrt(N): Feature learning regime (active, competing basins, grokking)
    r < d_task: Underdetermined (can't solve the task even if it converges)

For practical LoRA (N = 32K–100K examples, d_task ≈ 4–32):
    sqrt(N) ≈ 180–320      [NTK threshold = expensive]
    d_task ≈ 4–32          [Feature learning = economical]

This means: almost ALL practical LoRA training (r = 4, 8, 16, 32, 64) is in the FEATURE LEARNING
REGIME, not the NTK regime. The grokking picture (synthesis 20) applies to all of them.

The NTK result (no spurious minima for r >= sqrt(N)) is theoretically important but practically
irrelevant for low-rank LoRA — no practitioner uses r = 180.

---

## Weight Decay = Nuclear Norm = Bridge Between Regimes

The NTK paper proves: Weight Decay on LoRA = Nuclear Norm Regularization on ΔW = BA.

    λ||A||_F² + λ||B||_F² = 2λ||ΔW||_* (nuclear norm penalty, up to constants)

This is the exact connection between:
- Arrhenius temperature T = η × λ (weight decay = temperature, synthesis 20)
- Nuclear norm regularization = drives toward low-rank solutions
- TRS variational principle: nuclear norm minimum = maximum signal-to-noise in TRS

The nuclear norm = sum of singular values = ||σ||₁. Minimizing it drives singular values to zero.
The ONLY singular values that survive are those that explain enough task variance to overcome the
nuclear norm penalty. These are exactly the above-MP singular values = the TRS.

**Weight decay → nuclear norm → TRS variational principle: the TRS is the minimum-nuclear-norm
solution consistent with the data. This is the stationary-point of the LoRA optimization under
weight decay.**

This directly connects NTK (which proves the weight decay → nuclear norm relationship) to the
TRS decomposition (which is the minimum-nuclear-norm solution to the LoRA optimization problem).

---

## Optimal Rank Unification

Three different rank bounds from three different frameworks:

| Framework | Rank Condition | Meaning |
|-----------|---------------|---------|
| NTK (lora_ntk) | r >= sqrt(N) | No spurious minima (lazy regime) |
| GELoRA (gelora) | r >= d_task | Task accuracy (necessary condition) |
| Arrhenius/SLT | r = d_task | Minimal grokking barrier (feature learning regime) |

In the feature learning regime (r < sqrt(N)):
    Optimal r = d_task    [Arrhenius: no excess rank = zero grokking barrier]

In the NTK regime (r >= sqrt(N)):
    Optimal r = sqrt(N)   [NTK: exactly at phase boundary = most efficient global convergence]

For practical low-rank LoRA (r ≤ 128): always in feature learning regime.
    → Arrhenius picture applies: use r ≈ d_task (layer-wise, from GELoRA or AlphaLoRA)

For very large LoRA (r ≈ 200+): entering NTK regime.
    → NTK picture applies: optimization is clean but expensive

**The two frameworks are complementary: NTK explains the high-rank behavior, Arrhenius/SLT
explains the low-rank behavior. The TRS theory (based on S eigenspectrum) applies to both.**

---

## SeLoRA: Spectral Encoding Bridges Both Regimes

SeLoRA (lora_parameter_redundancy_spectral_encoding.pdf) observes "parameter redundancy" in LoRA
and uses spectral encoding (wavelet reparameterization of the TRS) to remove it.

The "parameter redundancy" in SeLoRA = the excess rank (r - d_task) in the Arrhenius picture.
SeLoRA's spectral encoding = a continuous version of the TRS three-region decomposition
(synthesis 19: SeLoRA wavelet = soft three-region decomposition).

By removing redundant parameters (excess rank), SeLoRA implicitly drives the system toward
the Arrhenius optimum r ≈ d_task — it's doing the same thing as AlphaLoRA and GELoRA
but from a compression/redundancy-removal perspective.

**SeLoRA = AlphaLoRA = GELoRA = all trying to identify and remove the excess rank (r - d_task).**
The Arrhenius formula explains WHY removing this excess rank is so important: each excess
dimension contributes exponentially to the grokking delay.
