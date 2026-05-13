# Iteration 1 — 2026-05-08

**Question entering this iteration:** What does the freshly-ingested GDL blueprint
(Bronstein/Bruna/Cohen/Veličković, arxiv 2104.13478) tell us about continual learning and
weight-aware AI that the existing corpus does not already say?

**Method:** graphify path/explain/query against `graphify-out/graph.json` after the GDL ingest.
Read every node the queries returned that I had not seen before.

---

## What the graph already contains (verified, not speculated)

Reading `synthesis_night_run_16_zero_holonomy_five_implementations.md`,
`shared_lora_subspaces_continual_learning.md`, and the BFS subgraph around
"fiber bundle holonomy continual learning gauge":

- The fiber-bundle / gauge framework for LoRA weight space is **already worked out**:
  total space = (B,A) pairs, base = ΔW = capability, fiber = GL(r) gauge orbit.
- **Five independent papers (OSRM, EBLoRA, OPLoRA, mtLoRA, Share) converge on the same
  constraint:** Region 2 subspaces of any two tasks must be orthogonal. Differs only in
  WHEN (training/merge/init), WHICH pair (task-task vs task-pretrained), and HOW STRICT.
- Synthesis 16 names the unifying triple-constraint formula:
  `ΔW* = projection onto (U_W₀^⊥ ∩ span{prior tasks}^⊥ ∩ task intrinsic subspace)`
- Universal Weight Subspace Hypothesis (2512.05117) finds ~16 dims shared by 1100+ models;
  Share (2602.06043) finds ~16 dims is enough for any task in continual learning.
- W2T direction is in the corpus (`Idea 10: Canonical TRS via W2T`, `LoRA Population
  Manifold as W/G`, `Synthesis 25`).
- Weight-as-input architectures already studied: SANE, Hyper-Representations, LoRAGen,
  WARP, Weight-Space Linear RNN. None of these is named as gauge-equivariant.

## What GDL adds that the corpus does NOT already say

The corpus uses gauge/fiber-bundle language as a **descriptive frame** (zero holonomy =
zero merge interference). GDL says it must be a **prescriptive constraint on architecture**:

- Erlangen-program move: the symmetry group of weight space (S_n permutations on hidden
  units, GL(r) gauge on each LoRA factor pair, ReLU positive-scale) determines what
  *architectures* are valid for processing those weights.
- The corpus has many constraints **on the weights themselves** (orthogonality between
  task subspaces, alpha → 2 stopping, rank ≤ 16). It has none **on the network that
  reads or writes those weights**.
- This is the missing piece: every existing weight-as-input model (SANE, LoRAGen, W2T-style
  proposals) is built without gauge-equivariance, which means it is forced to learn the
  gauge orbit as data variation rather than collapsing it as symmetry.

## The proposal — the buildable, world-changing target

**Gauge-Equivariant LoRA Hypernetwork (GE-LoRA-Hyper):**
A generative model that, conditioned on a task description, produces a valid LoRA adapter
in one forward pass — no fine-tuning — with three properties that no current weight-space
generator has simultaneously:

1. **Permutation- and GL(r)-equivariant by construction.** Architecture follows the GDL
   blueprint applied to the weight-space symmetry group. Output adapter is canonical
   (π-image) so all generations are gauge-collapsed.
2. **Zero-holonomy projector built into the head.** Conditioned on a registry of prior
   adapters, the final layer projects onto the orthogonal complement of every prior
   Region 2 subspace. Synthesis 16's triple constraint becomes a structural property of
   the *generator*, not a post-hoc fix on the *adapter*.
3. **Self-consistent rank.** The hypernetwork reads its own current spectrum and emits a
   rank-d_task adapter where d_task is predicted from the conditioning + the residual
   intrinsic dim of the model so far (alpha-stopping criterion as a learned head, not
   a hand-tuned threshold).

If this works, the implications are concrete and large:

- **One-shot personalization.** Any user-described task → adapter, no training run.
- **Continual learning by construction.** New task adapters cannot interfere with prior
  ones because the architecture forbids it. Catastrophic forgetting becomes structurally
  impossible in the LoRA-only regime.
- **Capability introspection for free.** Invert the generator: given an adapter, the
  encoder produces a task description. This is exactly the W2T capability-introspector
  the original north star asked for.
- **Compute saving at fleet scale.** A model fleet that generates adapters on demand
  instead of training them collapses fine-tuning compute by orders of magnitude.

## Why this hasn't been built (and isn't already in the corpus)

- Weight-space generative models exist (LoRAGen, SANE) but are not gauge-equivariant.
  They train on raw `(B, A)` pairs and waste capacity on the orbit.
- Zero-holonomy methods exist (the five from Synthesis 16) but operate at training time
  on a per-task basis. They do not pre-train a *generator* that internalizes the
  constraint across many tasks.
- W2T proposals in this corpus stop at "weights as tokens" but do not specify the
  equivariant tokenizer that GDL forces.
- The "~16-dim universal subspace" empirical result is the missing prior: the generator
  can be built with the universal subspace as its bottleneck, drastically reducing
  parameter count.

This is the synthesis: the corpus has the constraint (zero holonomy), the prior
(16-dim universal subspace), the data shape (LoRA model zoos), and the goal (one-shot
adapter generation). What it lacks is the *architecture* that respects the gauge group.
GDL provides that architecture template.

## Concrete next-step work for iter_002

1. Audit the existing weight-space generative models (LoRAGen, SANE, W2T proposals) for
   exactly what symmetry they break. Read the relevant_literature/ PDFs.
2. Find the published architecture closest to gauge-equivariant weight processing
   (DWS-style neural functional networks, Navon 2023; Zhou's NFN; Lim's neural
   functionals) — they exist for MLPs but not for LoRA-factor pairs as far as I know.
3. Specify the symmetry group precisely: `G = (S_{n_in} × S_{n_out}) × GL(r)` per
   LoRA-bearing layer, plus a global ReLU positive-scale per linear layer that shares
   no LoRA. Write out the equivariance condition the architecture must satisfy.
4. Sketch the actual block: weight-as-token tokenizer that already canonicalizes
   (QR+SVD), an equivariant transformer over tokens, and a head that projects onto
   the orthogonal complement of a registry.
5. Identify the smallest empirical experiment that would falsify the central claim
   (gauge-equivariance gives more sample-efficient adapter generation than non-equivariant
   baselines): probably train both on a small LoRA model zoo (CIFAR-LoRA or similar
   public set) at matched parameter count and measure adapter quality at held-out tasks.

## Halt check (against STATE.md halt condition)

| Criterion | Met? | Notes |
|---|---|---|
| Buildable system | Yes (provisional) | Architecture sketched but not specified at block level |
| Serves continual learning / weight-aware AI | Yes | Eliminates forgetting structurally |
| GDL forces (not just inspires) the architecture | Yes | Equivariance is a constraint, not vocabulary |
| No published version yet | Need to verify in iter_002 | Have to read DWS/NFN papers more carefully |
| Next experiment named and runnable | Provisional | Defined the falsification test, not the script |

**Decision:** Do NOT halt yet. iter_002 should attack the four "need-to-verify" items
above — particularly whether NFN/DWS already do this for the LoRA case, and what the
exact architecture of the equivariant tokenizer is. If iter_002 confirms novelty AND
specifies the tokenizer block, halt with this as the breakthrough. If iter_002 finds
prior art that already does this, redirect to whatever the gap actually is.
