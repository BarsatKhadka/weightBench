# Synthesis 24: Dimensional Phase Transition = SOC = LLC Drop = Rank Collapse

**Date:** 2026-05-07
**Session:** 5
**Previous synthesis:** synthesis_night_run_23_task_second_moment_operator_three_regions.md

---

## Three Papers, Three Languages, One Phenomenon

Three papers describe grokking from completely different frameworks. No paths exist between their key measurements. Yet they are measuring the same transition:

| Paper | Object | Pre-Grokking | Transition | Post-Grokking |
|-------|--------|-------------|------------|---------------|
| grokking_dimensional_phase_transition.pdf | Effective Dimensionality D | D < 1 (sub-diffusive) | D = 1 (SOC critical) | D > 1 (super-diffusive) |
| grokking_slt_competing_basins.pdf | Local Learning Coefficient (LLC) | LLC high (mem. basin) | LLC drop | LLC low (gen. basin) |
| grokking_generalization_collapse_htsr.pdf + from_spikes_to_heavy_tails | HTSR alpha | alpha > 2 (over-param.) | alpha ≈ 2 (Phase 5-6) | alpha < 2 (rank collapse) |

All three: the SAME transition (memorization → generalization = rank collapse = grokking).

---

## The Effective Dimensionality D = Gradient Diffusion Speed

The dimensional phase transition paper defines D from Finite Size Scaling (FSS):
    s_max(N) ~ N^D

where s_max is the maximum gradient "avalanche" size as network size N grows.

- D < 1 (sub-diffusive): gradient avalanches are small relative to network size = gradient is "sticky"
  = the gradient field is mostly gauge orbit directions (GL(r) symmetry, synthesis 14)
  = real learning is slow because gradients mostly move in the GAUGE direction (no real update)
  = this IS being trapped in the memorization basin

- D = 1 (critical): gradient avalanches scale linearly with N = Self-Organized Criticality
  = the system reaches the transition state between basins
  = corresponds to HTSR Phase 5 (heavy-tailed, alpha ≈ 2)
  = Gini coefficient peaks here (weights maximally concentrated in top d_task SVs)

- D > 1 (super-diffusive): gradient avalanches are large = gradient moves freely
  = system is in the generalization basin = rank has collapsed
  = LLC is low = HTSR Phase 6 (rank collapse)

**D < 1 (gradient trapped) = HTSR alpha > 4 (Phase 1-4) = LLC at maximum (memorization basin)**
**D = 1 (critical transition) = HTSR alpha ≈ 2 (Phase 5) = LLC dropping (barrier)**
**D > 1 (gradient free) = HTSR alpha < 2 (Phase 6) = LLC at minimum (generalization basin)**

---

## Self-Organized Criticality = The Natural Endpoint of Weight Decay

The dimensional phase transition paper finds: at the grokking transition, D = 1 corresponds to
Self-Organized Criticality (SOC). The system NATURALLY evolves to D = 1 given sufficient
training + weight decay.

Why does SOC occur at D = 1?

In the fiber bundle picture (synthesis 14): the Arrhenius escape (synthesis 20) is driven by
thermal fluctuations (temperature T = η × λ, the weight decay × learning rate).

As T increases (more weight decay), the system explores the energy landscape more broadly.
The SOC point D = 1 is where:
- The temperature T is exactly the Arrhenius activation barrier / log(time)
    T* = ΔF / log(t) = (r - d_task)(m + n)log(n) / 2log(t)

Beyond this temperature, the system spontaneously escapes to the generalization basin.
At exactly T*, the system self-organizes to the critical point.

**SOC at D=1 = the optimal temperature for grokking = the Arrhenius critical temperature T*.**

Weight decay automatically drives T toward T* because high weight decay = lower LLC = lower ΔF.
The system self-organizes by SHRINKING ITS OWN BARRIER (via weight decay reducing r - d_task).

---

## Weight Concentration (Gini) Peak = The Rank Collapse Precursor

The Gini coefficient measures inequality in singular value distribution:
    Gini = 1 when one SV carries all weight (maximally concentrated)
    Gini = 0 when all SVs are equal (uniform distribution)

**Gini peaks AT the grokking transition (D = 1, HTSR Phase 5).**

This makes sense:
- Pre-grokking (Phase 3-4): many moderate SVs (intruder dims still large) = moderate Gini
- At grokking (Phase 5): the top d_task SVs grow large, intruder dims begin collapsing → Gini peaks
  (the RATIO of large to small SVs is maximized just before the intruder dims fully collapse)
- Post-grokking (Phase 6): intruder dims have collapsed, top d_task SVs also settle → Gini decreases slightly

**Gini peak = the HTSR Phase 5 transition marker = D = 1 = LLC drop = grokking.**

All four measures peak/drop at the same event: the rank collapse from r to d_task.

---

## The Gradient Avalanche = Rank-Collapse Cascade

The TDU-OFC (Threshold-Based Diffusion Update) probe measures gradient "avalanches" — how
a small gradient perturbation propagates through the weight space. The FSS exponent D of
the avalanche distribution gives the effective dimensionality.

In LoRA terms: a gradient update ΔA, ΔB triggers a cascade of SV rearrangements.
- Pre-grokking: updates are LOCAL — only affecting a few intruder dim SVs, not d_task directions
- At grokking: a critical cascade occurs — a single gradient update triggers global SV rearrangement
  = the rank collapse from r to d_task is a SYSTEM-WIDE avalanche
- Post-grokking: gradients move freely through the d_task subspace (no intruder dims to "absorb" updates)

**The rank collapse is literally a gradient avalanche** — it's the single moment when
all intruder dims simultaneously collapse (SOC criticality at D=1, weight Gini peaks),
driven by weight decay bringing the system to T*.

---

## Simplest Picture

Five independent papers measuring grokking all measure the same thing:
- Rank collapse from r to d_task (synthesis 13, 15, TRS)
- LLC drop from RLCT_mem to RLCT_gen (synthesis 14, 20, SLT)
- HTSR alpha crossing from > 2 to ≈ 2 to < 2 (synthesis 15, 20, HTSR)
- Arrhenius escape time exp(ΔF/T) reaching O(1) (synthesis 20)
- D crossing from < 1 to = 1 to > 1 (this synthesis, dimensional phase transition)

**They are all: one rank collapse event, measured by five different instruments.**

The rank collapse is triggered by weight decay (temperature T) reaching T* (Arrhenius critical point),
which is when D = 1 (SOC), which is when LLC drops, which is when HTSR alpha ≈ 2.

All of these are the same transition seen from different projection angles.
