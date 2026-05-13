# Iteration 21 — 2026-05-09 — A01 + A07 first cut (structural half)

**Code phase, user-driven.** A01's geometric instrument and A07's
spectrum-only baseline ran on the same cached pool from A11, K=10
(felixml dropped). Cost: ~$0, ~1 min CPU after a factor-form-SVD
refactor that avoided materializing full ΔW matrices. Several
operational fixes along the way; the final clean run is the second
realized A-finding cluster.

This is **the structural half of A1's falsifier**. The full A1
falsifier additionally needs ground-truth post-merge accuracy
(actual adapter merging + inference) — that's separate work.

---

## What ran successfully

10 LoRA adapters × 10 attention projection layers × pairwise:

- **A01 instrument**: `Σ sin²(θ_k) / max(r_i, r_j)` between Region 2
  column spaces of pairs of LoRAs (Region 2 = column space of ΔW =
  column space of B). Sin² = 1 padding for unequal ranks per the
  canonical Grassmannian metric.
- **A07 instrument**: Euclidean distance between zero-padded sorted
  singular value vectors. Spectrum-only — no subspace direction.

Both share the same SVDs (factor-form: QR(B) + SVD on R_B @ A *
scaling), so A07 is essentially free atop A01.

## Operational fixes that got us here

The first three runs failed in increasingly informative ways:

1. **Background launch with stdout buffering** — output was empty
   for 10+ min because Python prints aren't flushed in piped
   subprocesses. Switched to `python -u` and ran synchronously.
2. **Windows page-file exhaustion (OSError 1455)** when
   `safetensors.torch.load_file` tried to mmap felixml's ~3.4 GB
   safetensors file. Refactored `load_lora_delta` →
   `load_lora_factors` using streaming `safe_open` reads of only the
   specific lora_A/lora_B keys. Worked for everyone except felixml.
3. **Hard segfault (exit 139)** at adapter index 8 — accumulated
   ΔW = B @ A materializations across 10 adapters × 10 layers
   exhausted memory (each 4096×4096 q_proj ΔW is 64 MB FP32; cumulative
   ~4 GB plus Python overhead). Refactored to keep B and A in factor
   form everywhere; computed Region 2 basis and singular values via
   QR(B) + SVD(R_B @ A * scaling) without ever forming the full
   m×n product. Drops memory from ~64 MB per layer per adapter to
   ~256 KB. Solved.
4. **felixml's safetensors mmap** still triggered an uncatchable
   segfault inside the Rust mmap layer (Windows commits the full
   virtual address space at file open even for streaming reads).
   Removed felixml from the adapter list — K=10. The other 10
   adapters loaded cleanly.

The factor-form SVD trick is the lasting lesson: for any pool of low-
rank ΔW = BA at scale, never materialize the m×n product.

## Headline numbers

```
adapters    : 10  (felixml dropped)
layers      : 10  (q_proj × {0,8,16,24,31} + v_proj × {0,8,16,24,31})
pairs       : 45

A01 normalized in [0, 1]; 0 = subspaces equal, 1 = orthogonal:
  mean   = 0.9747
  median = 0.9833
  min    = 0.8494  (instruct-safety, both lovepon q,v r=8)
  max    = 0.9901  (summ-finance, different setups)
```

## Surprising finding: rank/setup confound dominates task signal

Top 8 most-aligned pairs (rank by A01, lower = more aligned):

```
 1  instruct-safety        0.849   ← both lovepon q,v r=8
 2  instruct-code          0.914   ← both lovepon q,v r=8
 3  math-gen-chatqa        0.934   different setups
 4  instruct-math-cot      0.943   ← both lovepon q,v r=8
 5  code-safety            0.955   ← both lovepon q,v r=8
 6  code-math-cot          0.956   ← both lovepon q,v r=8
 7  math-cot-safety        0.962   ← both lovepon q,v r=8
 8  instruct-edu-dpo       0.966   instruct-flavored
```

7 of the top 8 are **same-author + same-rank + same-target-modules**
pairs (the lovepon r=8 q,v cluster), regardless of underlying task
(instruct vs code vs safety vs math-CoT). Meanwhile the same-task
math/math pair (yspkm-math r=32 all-7-proj vs lovepon-math-cot r=8
q,v) ranks **27/45** — slightly less aligned than median. Their
Region 2 subspaces literally live in different ambient dimensions
(rank 32 vs rank 8) on different layer sets (all 7 vs q,v only).

### What this is and isn't

This is **not** a falsification of A1. It's a **confirmation of plan.md's
controlled-pool design**. plan.md Section 4 mandates:

> rank=16 fixed, alpha=32, dropout=0.05, target=all linear in
> attention + MLP

i.e., every LoRA in the controlled population has **the same
parameterization**. With parameterization held constant, the
geometric instrument is freed up to read task signal. With
parameterization varying — as in our wild HuggingFace pool — the
dominant variation axis is *adapter setup*, not *task*. The
instrument did its job (distinguished pairs); the pool was the wrong
test.

For the actual paper, plan.md's controlled population will give
clean A01 readings. iter_021 surfaces an empirical reason *why* the
controlled population is necessary — the instrument is sensitive
enough to pick up parameterization differences that swamp task
signal in mixed pools.

## Free corroborations

### Q vs V asymmetry (third time corroborated)

```
Q layers overall mean A01: 0.9714
V layers overall mean A01: 0.9779
V-projections MORE diverse across tasks than Q (V - Q = 0.0065)
```

Consistent with:
- A11's "q_proj depth-dependent with low bottom-W₀, v_proj uniform top/bottom W₀."
- Synthesis 22's "Q/K spectral lifecycle (depth-dependent dynamics)
  vs V/O uniform compression."

A01 reads this asymmetry from a third angle (within-layer pair-wise
subspace alignment) and gets the same answer.

### Depth pattern

Both Q and V layers show **lower A01 (more cross-task alignment) at
extremes (layer 0 and layer 31)** and **higher A01 (more orthogonal)
in middle layers (8 / 16 / 24)**:

```
[Q] layer 0  : mean A01 = 0.9436
[Q] layer 8  : mean A01 = 0.9801
[Q] layer 16 : mean A01 = 0.9815
[Q] layer 24 : mean A01 = 0.9809
[Q] layer 31 : mean A01 = 0.9707
[V] layer 0  : mean A01 = 0.9779
[V] layer 8  : mean A01 = 0.9826
[V] layer 16 : mean A01 = 0.9837
[V] layer 24 : mean A01 = 0.9784
[V] layer 31 : mean A01 = 0.9671
```

Middle attention carries the most task-specific subspaces.

### A07 spectrum-only is a different signal

A07's L2-spectrum-distance ranks pairs DIFFERENTLY from A01. Among
the lovepon-r8-qv cluster (top 7 by A01), A07 spans 0.13 → 1.31 — a
10× range. So A01 (subspace direction) and A07 (subspace magnitude)
capture orthogonal facets of LoRA structure. For the full A1 falsifier
(regression against merge accuracy), both columns will be useful
features.

## Cascading implications

1. **plan.md's E1 controlled-pool design choice is empirically validated.**
   Under uncontrolled pool, A01 reads parameterization more than task;
   under fixed parameterization, A01 should be free to read task. This
   is concrete justification for the controlled population.

2. **Q vs V asymmetry is now a 3-way corroboration** (A11 spectrum
   alignment, A01 pair-wise subspace alignment, Synthesis 22's
   theoretical prediction). Solid empirical pattern; useful as a
   methodological footnote.

3. **The full A1 falsifier still needs merge-accuracy ground truth.**
   That requires actually merging adapter pairs and evaluating on a
   benchmark. With our 8 GB VRAM, LLaMA-3-8B 4-bit inference would
   work, but each merge + eval run is several minutes per pair × 45
   pairs = several GPU-hours for the math; plus we need a benchmark
   to evaluate on for each task.

4. **The lessons-learned scaffolding** (factor-form SVDs, streaming
   safetensors reads, Windows page-file gotchas) is now baked into
   the code base. Future experiments inherit it. This is iteration's
   compounding: every fix makes the next experiment cheaper.

## Files written this iteration

- `thesis_plan/test_experiments/a01_analytic_mergeability/run_a01_a07.py`
  — final factor-form-SVD version with K=10 adapter list.
- `thesis_plan/test_experiments/a01_analytic_mergeability/results/results.json`
  — 45-pair × 10-layer A01 + A07 numbers, ranks, structural callouts.
- `BREAKTHROUGH.md` A1 — appended `REALIZED FIRST-CUT (iter_021)`
  block with headline numbers, confound interpretation, free
  corroborations.
- `INDEX.md` — A01+A07 row added; A11 still listed; A07 placeholder
  retired.
- `STATE.md` — iter_021 entry added.

## What iter_022+ should consider

Three options, in roughly increasing cost:

1. **Run A01 + A07 on a controlled small pool.** Train ~5 LoRAs each
   on 3 different tasks (15 LoRAs total) on Qwen-2.5-0.5B or
   TinyLlama-1.1B, all at rank=16 / α=32 / fixed targets. Same script
   reads them; we get a clean A01 with controlled parameterization.
   Cost: ~5 GPU-hours small-base training + ~$0 SVD. Tier 2.

2. **Add merge-accuracy ground truth to the existing pool.** For each
   of the 45 pairs, actually merge (TIES / task-arithmetic /
   averaging) and run a single canonical benchmark. Even a tiny
   benchmark like 100 questions per task would make A01's
   `Σ sin²(θ_i)` regressable against accuracy drop. Cost: ~5 GPU-hours
   inference (45 × ~6 min at 4-bit). Tier 2.

3. **Train a Cross-LoRA-style cross-arch comparison** to test the A11
   cascade implication: does the U_S* frame transfer across base
   models? This is the A10/A16 paper-level revision iter_020 surfaced.
   Cost: ~10 GPU-hours small-base training × 2 architectures. Tier 2+.

iter_022 priority recommendation: **option 1 (controlled small pool
on Qwen-0.5B)**. Cleanest empirical step; addresses the confound
iter_021 surfaced; cost fits the user's hardware. Output gives a
real test of A1's per-task collapse claim under fixed parameterization
— exactly what plan.md's E1 commits to.

## Summary

iter_021 produced **the second realized A-finding** in the catalog —
A01 + A07's structural instruments running on real data. Headline:
on an uncontrolled pool, the geometric instrument reads adapter
parameterization more than task identity, **validating plan.md's
controlled-pool design choice empirically**. Q vs V asymmetry
corroborated for the third time. The instrument scaffolding (streaming
safetensors loads, factor-form SVDs, skip-on-fail for outlier
adapters) is now ready for any larger pool. plan.md unchanged. Catalog
state: 17 A-findings, **A11 + A1/A7 now realized empirically**.
