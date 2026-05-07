# Synthesis 17: Small Singular Values of W₀ Are the Fine-Tuning Target

**Date:** 2026-05-07
**Session:** 5
**Previous synthesis:** synthesis_night_run_16_zero_holonomy_five_implementations.md

---

## The Surprising Finding (small_singular_values_rmt_transformers.pdf)

"Small Singular Values Encode Learned Information in Transformers"

The small singular values of the weight matrix W (not ΔW, but the full pretrained weights W₀)
carry meaningful, learned information — not noise.

Key finding: **Activation Covariance Eigenvector–Singular Vector Overlap**
The small (but above-MP) singular vectors of W₀ have HIGH overlap with specific activation
patterns — they encode SPECIALIZED features learned during pretraining.

This seems to contradict TRS: isn't everything below a threshold = noise?

---

## Resolution: TRS Is About ΔW, Not W₀

The apparent contradiction dissolves once we distinguish:

**TRS (about ΔW = BA):** The small singular values of the FINE-TUNING UPDATE are noise (MP bulk).
The large singular values of ΔW are the task signal (genuine TRS, Region 2).

**Small SVs paper (about W₀):** The small-but-above-MP singular values of the PRETRAINED MODEL
are NOT noise — they encode specialized, task-specific pretraining knowledge.

These are compatible. The pretrained model W₀ has a rich small-SV structure:
- Large SVs of W₀ (~top-20%): universal features shared across all tasks (edge detectors,
  frequency patterns, semantic priors) — these are the FOUNDATION of the pretrained model
- Small-but-above-MP SVs of W₀: specialized features from pretraining (domain-specific patterns,
  language-specific structure, task-specific circuits learned during pretraining)
- Below-MP SVs of W₀: random/noise directions

---

## Why This Validates OPLoRA's Geometric Constraint

OPLoRA (oplora_orthogonal_projection_forgetting.md) constraint: ΔW ∈ U_{W₀}^⊥
(the fine-tuning update must be orthogonal to W₀'s dominant singular subspace)

The small SVs paper explains WHY this is the right constraint:

The large SVs of W₀ encode UNIVERSAL features that ALL tasks depend on.
If ΔW enters the large-SV subspace of W₀ (= intruder dims), it overwrites these universal
features → catastrophic forgetting (all tasks lose their universal foundation).

The small-but-above-MP SVs of W₀ encode SPECIALIZED features that specific subsets of tasks use.
ΔW in this subspace (= genuine TRS) adapts these specialized features to the new task → no forgetting
(other tasks don't depend on these specialized directions as much).

**OPLoRA is correct because:** fine-tuning should update the SMALL SVs of W₀ (adapting
specialized knowledge), not the LARGE SVs (which would destroy universal knowledge).

The horizontal subbundle ker(ω) = the orthogonal complement of W₀'s large SVs = 
EXACTLY the small-SV subspace where fine-tuning should live.

---

## A New Picture of the Full Weight Matrix W₀

The full pretrained model W₀ has a THREE-REGION structure (mirroring the TRS three-region):

**Region A (large SVs of W₀, top ~20%):** Universal features
- Shared by ALL tasks
- High activation overlap with ALL input patterns
- These are the "Platonic" directions (synthesis 14: Aristotelian vs Platonic)
- DO NOT TOUCH: fine-tuning here = catastrophic forgetting

**Region B (moderate SVs of W₀, above-MP, not top-20%):** Specialized features
- Shared by subsets of tasks (domain-specific, language-specific, etc.)
- High activation overlap with SPECIFIC input patterns
- These are the "Aristotelian" directions — task-neighborhood-specific
- UPDATE HERE: genuine TRS lives in this region

**Region C (below-MP SVs of W₀):** Noise
- Random structure, no activation pattern alignment
- Below the MP threshold = not learned, just numerical noise

The fine-tuning update ΔW should live in Region B — adapting the specialized pretrained
features to the new task. This is the horizontal subbundle ker(ω).

---

## The Intruder Dim Mechanism, Reframed

Intruder dims (Shuttleworth 2410.21228): above-MP SVs of ΔW that are LOW cosine similarity
to the dominant SVs of W₀.

Reframing: intruder dims are above-MP SVs of ΔW that enter Region A of W₀ (the universal
directions). They are "novel directions" to W₀ in the sense that W₀'s Region A didn't include
them — they're new axes being added to the weight matrix.

But why does entering Region A cause forgetting? Because:
- W₀'s Region A directions have high activation overlap with ALL inputs
- Modifying these directions changes the network's behavior on ALL inputs
- Other tasks' representations (which depend on Region A for their universal features) are disrupted

Intruder dims = updates that try to "add new universal features" = changes to the foundational
structure that all tasks share → universal disruption = forgetting.

The correct fine-tuning: modify Region B (specialized features) → disrupts only the current
task's specialized features → adapts them to the new task without disrupting other tasks' Region A.

---

## Connection to NTK Rank Threshold

The NTK paper (lora_ntk_regime_no_spurious_minima.pdf) proves: rank r ≥ sqrt(N) eliminates
spurious local minima (N = training examples).

In the pretrained model picture: W₀ has its singular structure from pretraining.
Fine-tuning in the NTK regime means the update ΔW stays in a "lazy" neighborhood of zero.
The NTK rank threshold sqrt(N) is the minimum rank for the LoRA to SPAN the gradient space
of the task (enough degrees of freedom to minimize loss without local traps).

This is NOT the same as GELoRA's d_task bound:
- NTK bound (r ≥ sqrt(N)): safety against optimization traps (may use excess rank)
- GELoRA bound (r ≥ d_task): minimum rank to express the task's intrinsic structure

For most tasks: d_task << sqrt(N), so GELoRA's bound is binding (the optimal rank is d_task,
not sqrt(N)). The NTK bound is relevant for INITIALIZATION: at the start of training, you
need r ≥ sqrt(N) to avoid local traps. But as training progresses into the feature learning
regime, the effective rank collapses to d_task (grokking, rank collapse phase).

**Practical implication:** Start fine-tuning with rank r = max(sqrt(N_small), d_task_estimate)
and use rank regularization (weight decay = nuclear norm penalty) to collapse to d_task.
The NTK bound ensures no local traps at initialization; GELoRA ensures final rank is optimal.

---

## The Complete W₀-to-ΔW Alignment Picture

Pre-training creates W₀ with structure:
    W₀ = [Region A (universal)] + [Region B (specialized)] + [Region C (noise)]

Fine-tuning should create ΔW = BA with structure:
    ΔW = [0 on Region A] + [adaptation of Region B] + [0 on Region C]

The CORRECT ΔW lives ENTIRELY in Region B of W₀.

Violations:
- ΔW in Region A = intruder dim (forgetting)
- ΔW in Region C = noise (no task signal)
- ΔW in Region B = genuine TRS ✓

The small SVs paper provides the EMPIRICAL EVIDENCE that Region B of W₀ is non-trivial
(contains learned information, not just noise). Without this evidence, one might assume
W₀'s Region B is also noise and that fine-tuning should stay in Region A. The small SVs
paper proves that Region B is the "rich middle ground" where task adaptation should happen.
