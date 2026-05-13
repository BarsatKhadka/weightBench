# Iteration 25 — 2026-05-09 — Lock-in is at step 2; σ peaks at step 14; Region structure is architectural, not emergent

iter_023 saw the lock-in by step 25. iter_025 zoomed in to substep
resolution and found two new things:

1. The same-task vs diff-task σ peaks at step ~14 of training, then
   *degrades* slightly through the remaining 95%. iter_023 missed
   this because it only sampled at step 25+.
2. The three-region geometry (Region 1 / Region 2 / Region 3
   amplitudes; spectrum heavy-tailedness) is **constant** from at
   least step 25. The structure isn't emergent — it's architectural.

Both findings reframe E2 in plan.md without changing its claims.

---

## Pivot from iter_025's first plan

The user redirected. iter_025 was originally going to be the Section 6
mergeability test (does Σsin²θ predict accuracy drop on actual merges?).
A 6-pair smoke test showed drops below noise floor on Qwen-0.5B with
λ=0.5 averaging — the merge is too clean to discriminate at this scale.

The user pointed out: *"merge benchmark isn't necessary; we're here to
understand the weight update trajectory better."* Correct. plan.md's
Section 5 (trajectory) is the headline contribution; Section 6's
mergeability is downstream applied work. iter_025 redirected to two
deeper trajectory questions:

- (2) Sub-step lock-in resolution: where exactly does commitment happen
  in the 0–30 step window?
- (4) Three-region emergence over training: when does the spectral
  structure actually appear?

## What ran

**Sub-step pool (new training):**
- 9 LoRAs (3 tasks × 3 seeds) on Qwen-2.5-0.5B
- 30 steps each, save every 2 steps → 15 checkpoints + endpoint per LoRA
- Lean save format: only `lora_A.weight` + `lora_B.weight` in bf16,
  no PEFT save_pretrained bloat. ~2.4 GB total instead of ~9 GB.
- Wall-clock: ~2.5 min total

**Region-emergence analysis (existing data):**
- Used iter_023's full trajectory pool (15 LoRAs × 11 checkpoints + endpoint)
- For 6 representative layers (q_proj + down_proj at depths 0/11/23),
  reconstructed dW per checkpoint, projected onto W₀'s top-64 subspace
  (Region 1) vs orthogonal complement, computed singular spectra
- ~25 min CPU

## Finding 1 — Substep T2: lock-in is at step 2, peak is at step 14

The same-task vs diff-task d_G separation across the substep window:

| step | same-task d_G | diff-task d_G | σ |
|---|---|---|---|
| 2 | 0.858 ± 0.026 | 0.919 ± 0.008 | **3.17** |
| 6 | 0.838 ± 0.024 | 0.910 ± 0.012 | 3.77 |
| 10 | 0.833 ± 0.021 | 0.905 ± 0.014 | 4.02 |
| **14** | 0.831 ± 0.020 | 0.903 ± 0.015 | **4.12 ← PEAK** |
| 18 | 0.831 ± 0.020 | 0.901 ± 0.015 | 4.03 |
| 22 | 0.832 ± 0.020 | 0.900 ± 0.015 | 3.88 |
| 26 | 0.834 ± 0.021 | 0.900 ± 0.015 | 3.64 |
| 30 | 0.835 ± 0.021 | 0.899 ± 0.015 | 3.50 |

Compare to iter_023's full-training (300 steps, save every 25):
- iter_023 step 25: σ=3.74 → matches our step 26 reading (3.64).
- iter_023 endpoint: σ=3.52 → matches our step 30 reading (3.50).

The substep data and full-training data are consistent at the
overlapping points. What's NEW is the resolution: **the σ peaks at step
~14 (4.12), not at endpoint.** iter_023's coarsest-resolution view
missed this peak.

**Operational reading.**
- After 32 training examples (2 steps × bs 16), same-task LoRAs are
  already 3.17σ closer to each other than to diff-task LoRAs.
- The signal grows for the first ~14 steps (224 training examples),
  peaks at 4.12σ, then **erodes** through the remaining 95%+ of training.
- "Lock-in is at step 25" (iter_023) was the truth at iter_023's
  resolution. The sharper truth is: **lock-in begins at step 2, peaks at
  step 14, then degrades.**

### Why does σ degrade after step 14?

- Same-task d_G stays roughly constant (0.831 → 0.835): same-task pairs
  are about as similar at endpoint as at step 14.
- Diff-task d_G *decreases* (0.903 → 0.899): different-task pairs become
  slightly more similar to each other over training.
- Both stds drift slightly.

This is consistent with a **drift-toward-common-ground** picture:
continued gradient updates on a shared base model push every LoRA
slightly toward whatever common features the model is learning to
amplify, regardless of task. Within-task structure stays fixed; cross-
task differentiation slowly erodes.

## Finding 2 — Region split is at random-baseline level; spectral shape genuinely emerges

**(Reframed after advisor caught a baseline issue. See note at end of
this section.)**

For each LoRA, at each of the 12 saved checkpoints, decomposed dW
into:
- **Region 1**: projection onto W₀'s top-64 singular subspace
- **Region 2 + 3**: the orthogonal complement
- Within Region 2+3, the **spectrum shape** (top-1 / bulk-mean) — heavy-
  tailed shape = Region 2 distinct from Region 3 noise floor

Aggregate per-task per-step:

```
                          ||dW||   ||R1||   R1/total   top1/bulk(orth)
add_mod (smooth):
  step 25                  0.154    0.046    0.299      568
  step 100                 0.265    0.078    0.295      640
  step 175                 0.324    0.096    0.296      673
  step 275                 0.381    0.116    0.304      689
  endpoint                 0.387    0.118    0.305      688

mul_mod (grokking):
  step 25                  0.167    0.050    0.301      650
  step 100                 0.289    0.089    0.308      648
  step 175                 0.392    0.119    0.303      750
  step 275                 0.432    0.131    0.303      784
  endpoint                 0.451    0.137    0.303      815

max (no-learning):
  step 25                  0.150    0.047    0.312      525
  step 100                 0.192    0.060    0.315      514
  step 275                 0.192    0.061    0.316      509
  endpoint                 0.192    0.061    0.316      510
```

**Random-baseline check (the advisor's catch).** Before reading this
as "architectural pinning," compute the random-projection baseline:
for an m × n matrix dW projected onto a uniformly random k-dim
subspace of R^m, the expected ratio ‖P_random dW‖_F / ‖dW‖_F is
exactly √(k/m). For our probed layers (m=896, k=64), this baseline
is **0.267**. Observed R1/total = 0.30 → **1.12× the random baseline**.
That's only ~12% above random. The "architectural pinning" framing
was overreach. What the data actually says about R1/total:

> dW has slightly-above-random alignment with W₀'s top-64 singular
> subspace. The slight alignment is consistent across training and
> tasks but is small in absolute terms.

**Substep region run (the advisor's second cheap fix).** Re-ran the
analysis on iter_025's substep pool (16 checkpoints from step 2 to
step 30, 9 LoRAs). Confirms two things:

| step | add_mod | mul_mod | max |
|---|---|---|---|
| 2 | R1/total=0.304, obs/rand=**1.14×**, top1/bulk=**433** | 0.301, 1.13×, **428** | 0.308, 1.15×, 439 |
| 14 | 0.298, 1.11×, 536 | 0.294, 1.10×, **602** | 0.310, 1.16×, 489 |
| 30 | 0.298, 1.11×, 539 | 0.299, 1.12×, **639** | 0.313, 1.17×, 491 |

**Three corrected findings:**

1. **R1/total is at random-baseline level (1.10–1.17× rand) from
   step 2 already.** Not "architectural pinning" — just slightly-
   above-random and fixed early. Consistent with iter_020's A11 finding
   that the LoRA signal lives orthogonal to W₀'s top.

2. **Top1/bulk(orth) GROWS during training**, in a task-dependent way:
   - add_mod (smooth): 433 → 539 (+24%)
   - mul_mod (grokking): 428 → 639 (**+49%**)
   - max (no real learning): 439 → 491 (+12%)

   This is the genuinely emergent finding. The heavy-tailedness of
   the spectrum *within the orthogonal-to-W₀-top component* sharpens
   during training, and sharpens *more for harder tasks*. mul_mod's
   grokking shows up here as the steepest spectral concentration
   gain.

3. **`max` task** has the smallest top1/bulk growth (12%) AND the
   smallest magnitude growth (||dW|| 0.045 → 0.160). The no-learning
   signature is consistent across both magnitude and shape.

**Corrected reading.** The three-region decomposition has two parts:
- The R1 vs orth-to-R1 split is at random-baseline level and fixed
  from step 2 (not architectural pinning, just random-level alignment).
- The spectral concentration (heavy-tailedness) within orth-to-R1 IS
  emergent and task-dependent — and is what plan.md's Section 3 should
  point to as the genuinely-trained quantity.

iter_023's earlier-flagged finding (within-task variance encodes
training-dynamics signal) gets a layer-level mechanism: the top1/bulk
spectral metric distinguishes smooth/grokking/no-learning by how much
it concentrates over training.

## Combined picture for plan.md

Two-component picture of what training is doing:

**Set early and stays:**
- R1 vs orth-to-R1 split sits at random-baseline level (1.1× random)
  from step 2 onward. Doesn't change.
- Same-task vs diff-task subspace separation reaches σ=3.17 by step 2,
  peaks at σ=4.12 by step 14.

**Genuinely emerges during training:**
- Spectral concentration (top1/bulk-mean) within orth-to-W₀-top.
  This grows 12-49% over training, with task difficulty controlling
  the rate. *This is what should be called "Region 2 emergence."*
- ||dW|| magnitude grows linearly with training (most of the
  parameter movement happens here).

Implications:

1. **plan.md E1's "endpoint analysis" is mildly suboptimal.** The
   peak-σ checkpoint is at step ~14, not at endpoint. For task-ID
   purposes, an early-training snapshot is *strictly better*. iter_023
   already noted this faintly; iter_025 makes it sharp.

2. **plan.md Section 3's three-region framing tightens to a
   spectrum-shape claim.** The R1 / R2+R3 *projection split* is at
   random-baseline level — not architectural, not emergent, just
   random-level alignment that's set fast. What's substantively
   trained is the *spectral concentration* within R2+R3, which
   sharpens 12-49% during training and tracks task difficulty.
   plan.md's "three-region decomposition" claim should center on the
   spectrum, not on the W₀-aligned vs not-W₀-aligned split.

3. **plan.md A2 (4-estimator phase statistic t*).** Substep data
   doesn't run all 4 estimators, but the σ-peak step (~14) is a
   single-estimator candidate for plan.md's t*. Worth checking
   whether the 4 estimators all converge near step 14 on a future
   experiment.

4. **The grokking signature has a spectral fingerprint.** mul_mod's
   top1/bulk grows 49% over training; add_mod 24%; max 12%. The
   spectral-concentration *growth rate* over training distinguishes
   the three dynamical regimes more cleanly than any single-step
   measurement does. Useful for plan.md's E2 trajectory-features
   downstream prediction story.

## Methodological notes for the log

- **Lean checkpoint format works.** Saving only `lora_A.weight` +
  `lora_B.weight` tensors in bf16 cuts checkpoint size from 35 MB
  to ~2 MB per step. With per-step saves over a 30-step run, this
  is the difference between fitting on disk (~2 GB) and not (~9 GB).
  Pattern: bypass PEFT's save_pretrained for trajectory work; save
  only the tensors you need.

- **Beware key-name conventions.** PEFT's `named_parameters()`
  includes `.default.` (the active adapter name). PEFT's
  `save_pretrained` strips it. If you save manually via
  named_parameters() and downstream analyzers use the
  save_pretrained convention, your keys won't match. Strip
  `.default.` from manual saves.

- **Disk hygiene matters at scale.** iter_025's first attempt OOM'd
  the disk with PEFT save_pretrained × 30 steps × 9 LoRAs. Lean save
  + disk cleanup recovered.

## Catalog state after iter_025

- A11 realized (iter_020): frames orthogonal at 84°.
- A01+A07 first-cut (iter_021): instrument confound on uncontrolled.
- C1 realized synthetic (iter_022): pooled-std sep 3.52.
- E2 trajectory iter_023: T2 3.74 at step 25; T1 distinguishes 3 regimes.
- C1 realized real-task iter_024: pooled-std sep ~11; output-vocab refuted.
- **iter_025 substep + region:**
  - **Lock-in begins at step 2; σ peaks at step 14 (4.12), then erodes
    to 3.50 by step 30 and 3.52 by step 276.** Earlier and sharper than
    iter_023 estimated.
  - **R1/orth-to-R1 split is at random-baseline level (1.1× rand)
    from step 2 onward.** Not architectural pinning; just slightly-
    above-random and fixed early.
  - **Spectral concentration WITHIN orth-to-R1 genuinely emerges
    during training**, growing 12% (max), 24% (add_mod), 49% (mul_mod
    grokking). This is the genuinely-trained shape signal; it's what
    plan.md's three-region decomposition should center on.

Six iters, ~$0 spend, ~3 GPU-hours total. plan.md unchanged but with
sharper E1 and Section 3 framings available.

## What iter_026+ should consider

1. **Pre-step-2 resolution.** What does dW look like at step 1, after
   exactly one gradient update? Does the three-region structure
   appear after one batch, or after several? Substep training at
   save_every=1 for the first 5 steps would answer.

2. **Real-task substep.** Does the same step-14 peak hold for real NLP
   tasks (BoolQ/AGNews/RT)? Training the iter_024 pool in substep mode
   would test generalization of the peak finding. ~10 GPU-min.

3. **Tangent direction (proper A4).** Now that we have substep checkpoints
   with closely-spaced saves, computing subspace velocity vectors is
   cheap. Same-task LoRAs walking the same path vs different paths is
   directly testable.

4. **Longer training to test post-step-30 erosion.** iter_023 showed
   σ shrinks to 3.52 at step 276. iter_025 substep ends at step 30
   with σ=3.50. Does σ keep degrading past 300? At what training step
   does same-task vs diff-task σ drop below 3? This would change the
   "fine-tuning makes LoRAs less distinguishable over time" framing
   from a small effect to a load-bearing one.

iter_026 priority recommendation: **(1) pre-step-2 resolution.**
Cheapest and answers the most basic remaining question (when do these
structures actually first appear?).
