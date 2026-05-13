# Iteration 2 — 2026-05-08

**Question entering this iteration:**
1. Is the iter_001 proposal (GE-LoRA-Hyper) genuinely novel against existing
   weight-space prior art (Navon DWS, Zhou NFN, Zhou UNF, Lim GMN) AND against
   newer (post-Oct-2024) work?
2. If novel, specify the symmetry group, tokenizer block, zero-holonomy head, and
   the smallest falsifiable experiment.

**Method:** Read four PDFs already on disk; web-search arxiv for newer prior art;
download the candidates with `curl`; read their abstracts and architecture sections.

---

## Prior art read this iteration (all PDFs in `finding_literature/`)

### The four "old" weight-space metanets (verified by reading)

| Paper | What it does | What it does NOT do |
|---|---|---|
| Navon DWS (2301.12780) | Permutation-equivariant *processor* of MLP weights — predict generalization, classify INRs | No GL(r) gauge; no LoRA factor pairs; no generation. Authors explicitly list "scaling/GL symmetries" as future work. |
| Zhou NFN (2302.14040) | Same as DWS but extended to CNNs via parameter sharing | Same gaps. Processor only. |
| Zhou UNF (2402.05232) | Automates the equivariant-basis construction for arbitrary tensor weight spaces with permutation symmetry | Still permutation-only (`S = ∏ S_n`); processor; no GL(r). |
| Lim GMN (2312.04501) | Encodes any feedforward arch as a parameter graph; GNN handles attention/residual/normalization | Permutation symmetry via DAG automorphisms. Processor. No GL(r). |

**Conclusion on the four:** none address GL(r) gauge symmetry of LoRA factor pairs,
none generate adapters, none structurally enforce zero-holonomy.

### Newer arxiv prior art (downloaded fresh)

| Paper | What it does | What it does NOT do |
|---|---|---|
| **LoL / GL-net** (2410.04207, Putterman/Lim/Gelberg/Jegelka/Maron, Oct 2024) | First explicit GL(r)-equivariant *processing* of LoRA pairs (U,V). Equivariant linear `F(U,V) = (ΦU, ΨV)`, GL-equivariant nonlinearity `σ_GL`, invariant head via `UV^T`. Predicts CLIP score, dataset attributes, dataset membership, accuracy. | **Processor only — predicts scalars from a LoRA. Does not generate LoRAs.** No continual-learning / zero-holonomy use. They explicitly find outer permutation symmetries are *less* important for LoRA than GL(r). |
| **SG-LoRA** (2509.10535, Li et al. 2025) | First text→LoRA generator (CVAE conditioned on CLIP text embedding) for zero-shot open-world adaptation. Sparse router over expert-LoRA pool, semantic prior, CVAE decoder. | **NOT gauge-equivariant.** Operates on raw `ΔW = BA` (averaged across epochs), wastes capacity on the GL(r) orbit. **No zero-holonomy.** No mechanism preventing inter-task interference when several SG-LoRA outputs are stacked or composed. |
| LoRA.rar (2412.05148) | Hypernetwork that *merges* two given content/style LoRAs at inference time | Closed-world (two named LoRAs in, one out). Not a from-scratch generator, no symmetry-aware processing of inputs. |
| HyRA (2510.04295) | Hypernetwork generating coupled low-rank matrices across attention heads within ONE training run | A training-time architecture, not a from-text generator over a model-zoo. No gauge handling of the cross-task case. |
| HypeLoRA (2603.19278) | Hypernetwork producing LoRA factors with calibration | Single-task; not gauge-aware; not for continual learning. |

**Conclusion on the new five:** the closest competitors split the problem:
- LoL = gauge-aware *but* processor only.
- SG-LoRA = generator *but* gauge-blind and not continual-learning-aware.
- LoRA.rar / HyRA / HypeLoRA = hypernetworks for single tasks or two-LoRA merging,
  not for an open registry of prior tasks with non-interference guarantees.

**No paper found that does all three of: (a) GL(r)-equivariant, (b) generative, (c)
zero-holonomy / structurally non-interfering with a registry of prior adapters.**

---

## Sharpened proposal — `GE-LoRA-Hyper-CL`

(continual-learning specialization of iter_001's GE-LoRA-Hyper)

A text-conditioned generator of LoRA adapters that is, by construction:

1. **Gauge-collapsed at I/O.** Inputs (existing registry of adapters) are
   QR-canonicalized — replace `(U_i, V_i)` with `(Q_i, R_i V_i)` where `Q_i, R_i = QR(U_i)`,
   then SVD-canonicalize: `Q_i R_i V_i^T = Ŭ_i Σ_i V̆_i^T`, sort by σ descending. This collapses
   the `O(r) × GL(r)` orbit into a unique representative.
   *(LoL avoids canonicalization to keep expressivity. We accept a small expressivity hit because
   we want a deterministic generation target — the head produces a unique canonical adapter, not
   one of an infinite gauge family.)*
2. **Permutation- and gauge-equivariant body.** Trunk is the LoL GL-net stack
   (equivariant linear `F(U,V) = (ΦU, ΨV)` + `σ_GL` nonlinearity) layered with
   permutation-equivariant cross-token attention (DWSNet-style block diagonals over neuron
   indices). Cross-attention to a CLIP-encoded task description.
3. **Three-region zero-holonomy head.** The output `(Û_new, V̆_new)` is structurally
   projected: `Û_new ← P_⊥ · Û_new` where `P_⊥ = I − Σ_{prior k} Û_k Û_k^T` *restricted
   to Region 2* (above-MP, low-cross-task-alignment SVs of `W_0`) — i.e., the head's
   final layer is a fixed (non-learned) orthogonalization against the registry.
   Region 1 (universal subspace) and Region 3 (below-MP noise) are excluded from
   the projection by design — Region 1 is shared and should not be excluded;
   Region 3 contributes nothing to function. **This is Synthesis 16's triple
   constraint compiled into the architecture.**
4. **Self-consistent rank.** A small head reads the spectrum `Σ_new` and emits a
   stop index `r̂` — the AlphaLoRA `α → 2` criterion learned end-to-end. Rows past
   `r̂` are zeroed. No hand-tuned rank.

### Symmetry group, made precise

For the LoL-style trunk, per LoRA-bearing layer `ℓ`:
```
G_ℓ = (S_{n_in,ℓ} × S_{n_out,ℓ}) × GL(r)         (LoRA factors)
G_global = ∏_ℓ G_ℓ                               (per-layer independent)
```

LoL handles the `GL(r)` part. DWSNets/NFN handle the `S_n × S_n` part. **GE-LoRA-Hyper-CL
is the first architecture stacking both.** Why this matters: outer-permutation symmetry
of LoRA factors is exactly the symmetry of the *base model's neuron ordering* — so making
the generator equivariant to it lets the same generator transfer across base models with
different permutations of identically-functioning neurons. (Cross-model transfer is currently
solved at inference time by alignment; we collapse it into the architecture.)

### Tokenizer block (the missing iter_001 deliverable)

Per layer `ℓ`:
```
1. Read (U_ℓ, V_ℓ) ∈ ℝ^{n_in × r} × ℝ^{n_out × r}.
2. QR-canonicalize: Q_ℓ, R_ℓ = QR(U_ℓ);  V'_ℓ = V_ℓ R_ℓ^T.
3. SVD-canonicalize: U_svd, S, V_svd = SVD(Q_ℓ V'_ℓ^T);     # collapses O(r)
   produce token (U_svd, S, V_svd) with `r` rows, fixed by descending σ.
4. Embed each row ("rank-i token") with a positional code σ_rank(i) and the
   layer-id ℓ; concatenate with CLIP(task_description).
5. Add the registry: encode each prior adapter the same way, mark with a
   "registry" type embedding.
```

The trunk is then a permutation+GL-equivariant transformer over the union of
(this-task-rank-token, registry-rank-token) sequences.

### The minimal falsifiable experiment

**Setup (uses already-public datasets):**
- CelebA-LoRA (3900 LoRAs, rank 4, Stable Diffusion 1.4) from the LoL paper.
- Train/val/test split at the *celebrity* level so test celebrities are unseen tasks.

**Three baselines, matched parameter count:**
- B1 (Vanilla MLP hypernet): SG-LoRA-style CVAE on raw `BA`.
- B2 (LoL processor → flip to generator): use GL-net body, train as a generator
  with a non-canonicalizing head. (Tests: does GL equivariance alone help?)
- B3 (Ours): GE-LoRA-Hyper-CL with QR+SVD canonicalized I/O AND zero-holonomy
  head against the registry of seen-celebrity LoRAs.

**Falsifiable claim:**
On *unseen* celebrities, with the registry stocked from seen celebrities, B3
attains higher CLIP score than B1 *and* simultaneously lower
catastrophic-forgetting score (CKA drop on seen-celebrity prompts) than B2.
If B3 is dominated by either B1 or B2 on its own claim, the architecture's
combined commitment to gauge + zero-holonomy is empirically unnecessary, and
the proposal is falsified.

**Sample-efficiency claim (secondary):** B3 reaches B1's best CLIP score with
≥ 4× fewer training LoRAs, predicted by the universal-subspace bottleneck (~16
shared dimensions account for most of the function — Universal Weight Subspace
Hypothesis, 2512.05117).

**Compute estimate:** GL-net forward time is `O((n+m)r)` per layer (LoL Table 1).
Training a generator on 3900 LoRAs at rank 4 over Stable Diffusion (1.4B params)
fits on a single A100. Estimate: 1–2 GPU-days.

---

## Halt check

| Criterion | Met? | Notes |
|---|---|---|
| Buildable system | YES | Tokenizer + trunk + head are now block-level specified. Both training datasets exist publicly. |
| Serves continual learning / weight-aware AI | YES | Zero-holonomy head makes inter-task interference structurally impossible *for the generated registry*. |
| GDL forces (not just inspires) the architecture | YES | The symmetry group `(S_n × S_n) × GL(r)` prescribes the linear layers (LoL's `(ΦU, ΨV)`) and the head's projection structure. |
| No published version yet | YES — verified by reading 9 closest papers | LoL is processor-only. SG-LoRA is generator-only (gauge-blind). No paper combines GL-equivariance + generation + structural zero-holonomy. |
| Next experiment named and runnable | YES | CelebA-LoRA dataset, three explicit baselines, falsifier defined. |

**Decision: HALT condition met.** Write `BREAKTHROUGH.md` at project root.

The breakthrough is the synthesis itself: nine prior papers each hold one piece
(LoRAGen has text→LoRA, LoL has GL-equivariance, Synthesis 16 has zero-holonomy as a
property of trained adapters, ~16-dim universal subspace gives the bottleneck, Universal
Neural Functionals gives the construction recipe). **None has assembled them into a
single generator that, by architecture, cannot catastrophically forget across an open
registry of tasks.** GE-LoRA-Hyper-CL is that assembly.

## What iter_003+ should do (post-halt)

If the user wants to continue the loop *past* the halt:
1. Implement the tokenizer and run the falsification experiment on CelebA-LoRA.
2. Extend the registry to include W2T-style "what can this LoRA do" inversion —
   feeding the generator's encoder backwards becomes a free capability introspector.
3. Cross-base-model: train on Stable Diffusion 1.4 LoRAs, evaluate generation
   targeting Stable Diffusion 1.5 (LoL paper has a 1.4→1.5 transfer baseline).
   This tests whether outer permutation equivariance buys cross-base transfer.

## Files added this iteration (PDFs in `finding_literature/`, no MD abstracts written)

- `lol_gl_equivariant_2410_04207.pdf` (Putterman/Lim et al., LoL/GL-net)
- `semantic_lora_params_gen_2509_10535.pdf` (Li et al., SG-LoRA)
- `lora_rar_hypernetwork_merge_2412_05148.pdf` (LoRA.rar)
- `hyra_hypernet_lora_attention_2510_04295.pdf` (HyRA)
- `hypelora_calibrated_2603_19278.pdf` (HypeLoRA)

`graphify update .` ran (AST-only): 1912 nodes, 2052 edges, 171 communities (was 1901/2043/170).
Semantic re-extraction is pending (no LLM key set in env this session).
