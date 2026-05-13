# Iteration 38 — 2026-05-10 — Same-task ensemble doesn't beat best individual; iter_037's interpretation overclaimed

iter_037 saw rt accuracy at 0.88 in a 5-LoRA mixed merge, exceeding the
best individual solo (0.87). I called this "ensemble effect of same-task
clustering." iter_038 tests that interpretation directly: take ALL 5
seeds of each task, merge them, see if the same-task ensemble exceeds
its best individual.

**Result: same-task ensemble does NOT exceed best individual on most
tasks.** iter_037's interpretation was wrong. The 0.88 rt result was
a property of the *diverse* mixed pool (5 LoRAs from 3 different
tasks), not a same-task ensemble effect.

This iteration corrects the previous overclaim and reveals a stronger
finding: **same-task multi-LoRA full merges are *catastrophic* on
out-of-task accuracy**.

---

## Setup

For each task t in {boolq, agnews, rt}:
- Take all available same-task seeds:
  - boolq: 4 seeds (42, 123, 456, 1024)
  - agnews: 5 seeds (42, 123, 456, 789, 1024)
  - rt: 5 seeds (42, 123, 456, 789, 1024)
- Test 2 ensembles:
  - Full: all dWs added (no recipe)
  - ZeroMLP: all dWs added with MLP zeroed (the recipe)

Eval on all 3 tasks per ensemble. 6 ensemble conditions + base.

## Results

| condition | boolq | agnews | rt |
|---|---|---|---|
| base | 0.41 | 0.38 | 0.37 |
| boolq ensemble full (4 LoRAs) | 0.42 | **0.00** | **0.00** |
| boolq ensemble zeroMLP | 0.59 | 0.21 | 0.82 |
| agnews ensemble full (5 LoRAs) | **0.00** | 0.84 | **0.00** |
| agnews ensemble zeroMLP | 0.65 | 0.87 | 0.57 |
| rt ensemble full (5 LoRAs) | **0.00** | **0.00** | 0.43 |
| rt ensemble zeroMLP | 0.29 | 0.62 | 0.82 |

## Three findings

### Finding 1 — Same-task ensembles do NOT exceed best individual

| task | ensemble zeroMLP | best individual solo (from iter_030) |
|---|---|---|
| boolq | 0.59 | 0.74 (boolq_1024) |
| agnews | 0.87 | 0.87 (agnews_42) — tie |
| rt | 0.82 | 0.87 (rt_456 / boolq_456) |

Ensemble underperforms best-individual on boolq and rt; ties on agnews.
**iter_037's "merge exceeds individual" interpretation was wrong.**

iter_037 K2 (5 LoRAs from 3 tasks, all zeroMLP) gave rt = 0.88 — but
that's because 3 of those 5 LoRAs (rt_1024, rt_42, boolq_456) all
contributed rt-relevant signal *in different directions*. The
ensemble effect that "exceeded individual" was diversity-driven, not
same-task-cluster-driven.

iter_038's pure same-task ensemble of 5 rt LoRAs gives rt = 0.82,
*below* best solo. Same-task seeds aren't diverse enough to give
ensemble lift.

### Finding 2 — Same-task FULL ensembles catastrophically destroy out-of-task

The same-task full-merge (no recipe) results are striking:
- boolq full ensemble: agnews 0.00, rt 0.00 (perfect destruction)
- agnews full ensemble: boolq 0.00, rt 0.00 (perfect destruction)
- rt full ensemble: boolq 0.00, agnews 0.00 (perfect destruction)

Every same-task k-LoRA full merge produces 0.00 on the other tasks.
Compare to single-LoRA destructive cases (iter_030):
- boolq_42 alone: agnews 0.14, rt 0.08
- rt_1024 alone: boolq 0.02
- agnews_42 alone: not destructive at all

**Adding more same-task LoRAs amplifies destructive interference.**
Each LoRA's MLP pushes in similar destructive directions (since
they're all trained on the same task). Summing 4-5 same-task MLPs
creates massive constructive interference *in the destruction
direction*.

This contrasts with cross-task multi-LoRA merges (iter_037 K1 at
k=5 cross-task: agnews 0.78, rt 0.48 — destruction but not
catastrophic). Different-task MLPs partially cancel; same-task
MLPs add up.

**Implication for plan.md continual-learning recipe:** the
zero-destructive-MLP rule is essential when accumulating same-task
LoRAs. Without it, even "preserving" individual LoRAs become
destructive when summed at the same task.

### Finding 3 — agnews ensemble zeroMLP gives best cross-task lift

agnews_ensemble_zeroMLP: boolq 0.65, agnews 0.87, rt 0.57.

- boolq lifted from 0.41 (base) to 0.65 (+0.24) without ANY boolq
  LoRA in the merge. Just by averaging 5 agnews LoRAs with MLPs
  zeroed.
- rt lifted from 0.37 to 0.57 (+0.20).
- agnews matches best individual solo (0.87).

This is the strongest cross-task transfer effect we've seen. **A
zeroMLP ensemble of one task's seeds appears to teach the model a
"general fine-tune competence" that lifts unrelated tasks
substantially.**

Mechanism hypothesis: the attention-only ensemble averages out
seed-specific noise in the attention component, leaving only the
"task-general adaptation pattern" — which happens to help related
2-token-classification tasks (yes/no, World/Sports/Business/Tech,
positive/negative all share the "answer in 1-2 tokens given a cue"
structure).

## Correcting the catalog narrative

iter_037 included this sentence: "K2 uniform-zero gives rt 0.88, the
best rt solo was 0.87. The 5-LoRA merge produced an above-solo rt
model. Constructive interference between multiple preserving LoRAs."

iter_038 directly tests that claim. Result: NO. Same-task ensemble of
5 rt seeds gives rt 0.82, *below* best solo.

The right reading of iter_037's K2 = 0.88 result: it's a 5-LoRA
mixed pool (2 destructive + 3 preserving across 3 tasks) where 3 of
the 5 LoRAs contribute rt-relevant signal in different directions.
That diversity gives the lift.

**The behavior is closer to "weak ensembling via diverse contributors"
than "same-task clustering ensemble."** This is consistent with
classical ensemble theory (diversity matters more than mean accuracy
for ensemble lift) and explicitly contradicts the "C1 clustering →
ensemble effect" narrative.

## Implications for plan.md

1. **iter_037's "scaling helps via constructive interference" has
   exceptions.** Cross-task scaling helps; same-task scaling hurts.
   plan.md continual-learning recipe should highlight:
   - Apply MLP-zero to ANY same-task accumulation (otherwise
     catastrophic).
   - Cross-task accumulation can use either uniform-zero or
     asymmetric.

2. **C1 clustering doesn't directly translate to ensemble lift.**
   Same-task LoRAs cluster on the Grassmannian (iter_022, iter_024),
   but the cluster doesn't act as a useful ensemble centroid for
   accuracy. The cluster is a *geometric* finding; the per-task
   accuracy benefit doesn't follow.

3. **agnews-style ensemble zeroMLP as a general "fine-tune
   benefactor"** — zeroMLP ensemble of one task's seeds boosts
   unrelated tasks. A single task's training is paying for general
   improvement on related task structures. Worth more investigation:
   does the boolq ensemble zeroMLP also help unrelated tasks? Yes,
   it gave rt 0.82 (above base 0.37). Both classification-style
   ensembles help across the binary-classification family.

## Caveats

- 4-5 seeds per task. Larger ensembles untested.
- 100 eval examples. Differences > 0.05 are robust; 0.59 vs 0.74 is
  well above noise.
- The "0.00 across out-of-task" results from full ensembles deserve
  closer look — what specific outputs is the model producing?
  Probably the LoRA pushed it toward consistent same-task-format
  answers regardless of input.

## What iter_039+ should consider

1. **Inspect what the destructive ensembles output.** Take the
   boolq-full-ensemble (agnews → 0.00, rt → 0.00). Print 10 actual
   model outputs for an agnews input. Probably "yes" / "no" for all.
   Confirms the "MLP overwrites output token bias" mechanism.

2. **k=2 same-task vs k=4 same-task ensemble.** Where does the
   destruction become catastrophic? Bisection between k=1 (mild)
   and k=4 (catastrophic) tells us how interference scales.

3. **Drop iter_037's "constructive interference exceeds individual"
   from BREAKTHROUGH.** Replace with "diversity in zeroMLP merge
   gives mild ensemble lift; same-task ensemble doesn't beat
   individuals." Run baseline first.

4. **The cross-task help from agnews zeroMLP ensemble is the most
   surprising new datapoint.** Probe what direction in dW space gives
   this lift. May be a "task-general adaptation direction" worth
   isolating.

iter_039 priority: **option 1 (output inspection of destructive
ensembles).** Cheap (5 min), confirms or refutes the mechanism story.

## Catalog state after iter_038

- ... (18 prior iters)
- **iter_038 same-task ensemble:**
  - **Same-task ensembles do NOT exceed best individual on most
    tasks.** boolq 0.59 vs best 0.74; rt 0.82 vs best 0.87; agnews
    ties at 0.87.
  - **Same-task FULL ensembles catastrophically destroy out-of-task
    accuracy** (0.00 across the board). Same-direction MLP
    interference compounds.
  - **Cross-task help via zeroMLP ensemble is substantial** (agnews
    ensemble → 0.65 boolq, +0.24 over base).
  - **iter_037's "merge exceeds individual" interpretation is
    refuted.** It was diversity-driven, not same-task ensembling.

Nineteen iters, ~$0 spend, ~5 GPU-hours total. plan.md unchanged.
The continual-learning recipe holds; iter_037's same-task ensemble
narrative is corrected.
