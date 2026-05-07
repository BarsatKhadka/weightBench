# Synthesis 28: The Single Unifying Principle

**Date:** 2026-05-07
**Session:** 5
**Previous synthesis:** synthesis_night_run_27_ntk_vs_feature_learning_regime_lora.md

---

## The One Fact That Explains Everything

Neural networks trained on language converge to the same function class. The space of these
functions has a spectral structure given by the task second-moment operator:

    S = E_tasks[ΔW^T ΔW]

S is defined over the task distribution (not any specific architecture or model).
Its eigenspectrum, thresholded at the Marchenko-Pastur noise floor, gives THREE REGIONS:

    Region 1 (top eigenvectors):  universal, architecture-independent, Platonic
    Region 2 (middle eigenvectors): task-specific, Aristotelian
    Region 3 (below MP threshold): noise, not learned by any task

THIS IS THE SINGLE UNIFYING PRINCIPLE. Everything in the knowledge graph follows.

---

## What Follows

**WHY LoRA works:**
Region 2 is low-rank. d_task = rank(Region 2 for one task) << ambient dimension.
A rank-r factorization with r ≥ d_task can represent the task update exactly.
LoRA is not an approximation — it's an exact representation of the task-relevant directions.

**WHY region 1 should not be updated:**
Region 1 = top eigenvectors of S = the pretrained model's generic capacity.
Updating Region 1 during fine-tuning = corrupting the Platonic universal circuits (induction heads,
  universal features, etc.) that all tasks share = catastrophic forgetting.
OPLoRA, EBLoRA, OSRM all implement this constraint from different directions.

**WHY intruder dims cause forgetting:**
Intruder dims = LoRA gradient rotated into Region 1 directions (W₀'s large SVs = Region A).
Updating Region 1 while trying to fine-tune Region 2 = corrupting universal circuits.
Forgetting ∝ intruder dim count (ρ = 0.971, synthesis 17).

**WHY grokking happens:**
r > d_task = excess rank = the LoRA update has r dimensions but only d_task are task-relevant.
The excess (r - d_task) directions are intruder dims or noise — they need to be "collapsed" out.
The collapse = the grokking transition = Arrhenius escape with barrier ΔF ~ (r - d_task) × log(n).
Weight decay = temperature T driving the escape. AlphaLoRA/GELoRA = choosing r ≈ d_task to
eliminate the barrier entirely.

**WHY model merging works (and when it fails):**
Task arithmetic = sum of ΔW vectors = vector addition in Region 2 subspaces.
If Region 2 subspaces are orthogonal (different tasks → different Region 2 directions) → no interference.
If they overlap (similar tasks, or intruder dims contaminate Region 1) → interference.
The 1/√N CLT decay of task-specific Region 2 (synthesis 13) = why averaging many LoRAs washes out task-specific features.

**WHY MAML/iMAML/Fisher connections matter:**
Region 2 has nonzero curvature (curved fiber connection, Aristotelian region).
The gradient in Region 2 doesn't flow in a straight line — the Fisher metric captures the curvature.
MAML ignores this (trivial/Euclidean connection → fails in high-curvature task distributions).
iMAML/EWC-LoRA use the Fisher metric → correct curvature → better few-shot adaptation and continual learning.

**WHY cross-architecture transfer works:**
S is architecture-independent. Region 1 (74% of features) is shared across transformers, SSMs, MLPs.
Any two models trained on the same task distribution share Region 1.
Cross-LoRA transfer quality = Region 2 overlap = how similar the architectures' Region 2 directions are.

**WHY weight decay is essential:**
Weight decay = nuclear norm regularization on ΔW.
Nuclear norm minimum = minimum-energy solution consistent with data = concentrate on d_task directions.
Weight decay drives the LoRA update toward Region 2 (the task-relevant S eigenvectors) and
away from Region 3 (noise) and Region 1 (pretrained universal circuits).

**WHY bigger rank is not always better:**
Excess rank (r - d_task) = extra dimensions that aren't in Region 2.
These become intruder dims (absorbed into Region 1 = forgetting) or noise.
The Arrhenius grokking delay is EXPONENTIAL in (r - d_task).
Using r >> d_task: wastes parameters, causes forgetting, and delays generalization exponentially.

---

## The Single Equation

If we had to write one equation:

    S eigenspectrum after MP thresholding = {Region 1, Region 2, Region 3}

Every other result in this knowledge graph is a corollary.

---

## How to Read a LoRA Adapter

Given any LoRA adapter (A, B):
1. Compute ΔW = BA
2. Compute SVD: ΔW = UΣV^T
3. Separate by threshold: above-MP → signal; below-MP → noise (Region 3)
4. Separate signal by W₀-alignment: W₀-orthogonal → Region 2 (genuine TRS); W₀-aligned → intruder dims
5. Count Region 2 directions: this is d_task (the intrinsic rank of the task)
6. Check HTSR alpha of each Region 2 SV: alpha ≈ 2 → optimal; alpha > 4 → undertrained; alpha < 2 → overtrained
7. Stop training when: rank(Region 2) = d_task AND all Region 2 alphas ≈ 2

This 7-step procedure is the complete "TRS audit" of a LoRA adapter.
It reads off the spectrum of S sampled from a single fine-tuning.
It is equivalent to all of: GELoRA rank estimation, AlphaLoRA quality check, DSiRe dataset size, W2T capability prediction, D2C clustering.

---

## The Hierarchy of Instruments

All methods in this knowledge graph are reading S from different angles:

| Instrument | What it measures | Where in S spectrum |
|-----------|-----------------|---------------------|
| GELoRA rank | rank(Region 2) = d_task | Count above-MP eigenvectors |
| AlphaLoRA alpha | training quality of Region 2 | Shape of above-MP tail |
| DSiRe dataset size | rank stability of Region 2 | How well Region 2 is resolved |
| TRS fingerprint | task identity | Which Region 2 eigenvectors |
| SLT RLCT | geometric complexity of basin | Volume of top-k eigenspace |
| HTSR phase | training stage | alpha trend in Region 2 |
| SNR (Spectrum paper) | signal energy / noise energy | Region 2 energy / Region 3 energy |
| D2C clustering | task similarity | Subspace overlap in Region 2 |
| Spectral Skewness | Region1/Region2 energy ratio | S eigenvalue mass distribution |
| Effective Dim D | grokking state | Is D below/at/above 1 |

They are all one-dimensional projections of the same multi-dimensional object: the spectrum of S.

---

## The Simplest Statement (Newton's View)

**S is the operator. Its spectrum gives the structure. Everything else is computation.**

Fine-tuning = sampling from the eigenspectrum of S.
A perfect LoRA = the projection of S onto d_task task-specific eigenvectors.
A bad LoRA = any mixture that includes Region 1 contamination (intruder dims).
The history of LoRA fine-tuning research = the gradual discovery of this spectral structure.
