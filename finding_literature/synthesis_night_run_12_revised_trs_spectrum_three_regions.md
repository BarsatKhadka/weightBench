# Synthesis 12: Revised TRS Spectrum — Three Regions, Not Two

**Date:** 2026-05-07
**Session:** 4 (continued)
**Previous synthesis:** synthesis_night_run_11_srfm_pave_spectral_web.md

---

## A Critical Correction

**Previous claim in BIG_IDEAS.md (Idea 17, labeled incorrectly):**
"Top-20% singular values = 89% inter-task interference" [WRONG]

**What mtLoRA (arXiv:2603.01526) actually says:**
"High-SV top-20% components have 89% inter-task ALIGNMENT (shared knowledge)"

This is the OPPOSITE interpretation. The large singular values of LoRA B matrices are NOT
the most task-specific — they are the MOST SHARED across tasks. Task-specific signal lives
in the INTERMEDIATE above-MP singular values, not the top.

---

## The Revised Three-Region Spectral Decomposition

The LoRA singular value spectrum has THREE regions, not two (above-MP / below-MP):

### Region 1: Universal Fiber Directions (Very Large SV, High Inter-Task Alignment)
- mtLoRA: top-20% SVs, 89% inter-task alignment
- Universal subspace (2512.05117): ~16-dim subspace shared by 1100+ LoRAs
- Share (2602.06043): foundational subspace extracted by SVD stacking
- EigenLoRAx: principal subspace recycled across adapters

**Geometric identity:** These are the **flat fiber directions** — shared by all tasks,
zero holonomy (universal subspace = zero curvature conjecture from synthesis 1-4), the
"background" task adjustment that every task makes regardless of its specific content.

NOT task-specific. NOT intruder dims. NOT noise. They are the **structural prior** of the
model family — directions all fine-tunings naturally use.

### Region 2: Task-Specific Signal (Moderate SV, Above MP, Low Inter-Task Alignment)
- GELoRA: these are the first d_task = intrinsic_dim(task) directions above the fiber
- Shuttleworth/TRS: genuine TRS (W₀-orthogonal) vs. intruder dims (W₀-aligned) within this region
- mtLoRA: bottom 50% of LoRA SVs have only 3% inter-task alignment = task-specific

**Geometric identity:** These are the **task-specific directions** above the fiber —
either genuinely horizontal (genuine TRS, W₀-orthogonal, add new task knowledge) or
intruder dims (W₀-aligned, overwrite pretrained structure). The W₀-alignment criterion
(Shuttleworth) distinguishes the two within Region 2.

**This is where the actual task fingerprint lives.** Not the largest SVs.

### Region 3: Noise (Below MP Threshold)
- Marchenko-Pastur bulk
- No task signal, no fiber signal, just parameter space noise

---

## Implication for TRS Measurement

The original TRS computation:
1. SVD ΔW → get singular values σ₁ ≥ σ₂ ≥ ... ≥ σ_r
2. All σᵢ > σ_MP = candidates for "genuine TRS"
3. Divide by W₀-alignment into genuine TRS vs intruder dims

The revised TRS computation should be:
1. SVD ΔW → get singular values σ₁ ≥ σ₂ ≥ ... ≥ σ_r
2. Very large σᵢ (top-20%, or σᵢ > σ_universal_subspace_threshold) = Region 1 (fiber)
3. Moderate σᵢ (above MP, not top-20%) = Region 2 candidates
4. Low σᵢ (below MP) = Region 3 (noise)
5. Within Region 2: divide by W₀-alignment into genuine TRS vs intruder dims

The FOUR-WAY decomposition (genuine TRS / intruder / MP bulk / suppression) was correct
but missed the distinction between VERY LARGE shared components (Region 1) and task-specific
components (Region 2). The revised five-way decomposition:
1. Universal fiber (very large, shared) — stable across tasks
2. Genuine TRS (moderate above-MP, W₀-orthogonal) — task signal
3. Intruder dims (moderate above-MP, W₀-aligned) — forgetting
4. MP bulk (below threshold) — noise
5. Suppression (below zero) — attenuated by pretraining

---

## Implication for the Universal Subspace Conjecture

The universal subspace (~16 dims) = Region 1 = flat fiber directions.
These are NOT at risk from intruder dims. They persist across fine-tunings because they
are the structural prior of the foundation model.

The conjecture "universal subspace = flat fiber = zero holonomy" is NOW SUPPORTED by
mtLoRA's empirical finding that these directions have near-perfect inter-task alignment:
if they are shared by all tasks (near-unity alignment), they accumulate zero holonomy
when traversing the task graph (all tasks agree on these directions = no curvature).

**New prediction:** The holonomy of any fine-tuning loop should be zero in Region 1
directions and nonzero in Region 2 directions. The holonomy lives entirely in the
task-specific subspace (Region 2), not the universal subspace (Region 1).

---

## Implication for GELoRA's Rank Bound

GELoRA: r_i ≥ intrinsic_dim(task at layer i)

With the revised decomposition:
- Optimal rank = dim(Region 1) + dim(Region 2, task-specific)
                ≈ 16 (universal fiber) + d_task (intrinsic task dimension)

For most fine-tuning tasks, d_task is small (typically 5-50). So:
- LoRA rank r = 16 + d_task is theoretically optimal
- Rank r > 16 + d_task → extra components become intruder dims
- Rank r < 16 → insufficient coverage of the universal fiber
- Rank r = 16 only → adapts universal fiber, no task-specific signal

GELoRA's formula r_i = max(d_{i+1} - d_i, 0) + 1 measures the CHANGE in intrinsic
dimension across layers — the part that needs new task signal. Region 1 (fiber) is implicit
and always needed; Region 2 adds the GELoRA amount.

---

## Amari Dual Connections: A Genuine Open Thread

No paper connects Amari's e/m-connections to LoRA fine-tuning or natural gradient LoRA.
The gap:

The m-connection of information geometry is the one used by natural gradient descent (NGD):
it defines parallel transport using the Fisher metric in the sense that preserves model
distributions under reparameterization. NGD for LoRA would use the m-connection on the
quotient manifold W/G.

The e-connection (exponential connection) is the dual: it preserves the exponential family
structure. For LoRA: the e-connection on W/G would preserve the exponential family of
output distributions as you move along the fiber.

**The fiber bundle connection ω is related to the m-connection:** ω measures the component
of any tangent vector that lies in the "exponential family" direction (the fiber = gauge
directions). The horizontal subbundle ker(ω) = directions that are m-geodesic in the quotient.

This is a formal mathematical claim that would require proof, but the structure is there:
Amari's dual pair (e/m) on the full parameter space restricts to our (fiber/horizontal)
split on the LoRA quotient manifold. This connection is entirely unexplored and would
provide the first principled connection between information geometry and the fiber bundle
approach to LoRA.

---

## Summary of Revisions from This Session

1. **mtLoRA correction:** Top-20% SVs = shared fiber (NOT interference). Task signal in intermediate SVs.
2. **Three-region decomposition:** Universal fiber / Task-specific (genuine TRS + intruder) / Noise
3. **Holonomy lives in Region 2:** Universal subspace has zero holonomy; task-specific subspace has all the holonomy
4. **Optimal rank:** ~16 (universal fiber) + d_task (intrinsic task dimension)
5. **Amari dual connections:** Genuine gap — m-connection / e-connection not yet connected to LoRA NGD or fiber bundle
