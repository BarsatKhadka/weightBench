# Learning Roadmap — Math for the LoRA Region Anatomy Project

Goal: enough math to read every paper in `finding_literature/`, run every analysis
on the LoRA checkpoints, and *interpret* what the numbers mean — not just produce them.

Tier structure: each tier earns you a layer of capability. Don't read serially —
**interleave reading with running analysis on actual checkpoints**. Every concept
should become a numpy command, become a plot, become intuition.

---

## Tier 0 — Visual intuition (today, ~3 hours)

- [ ] **3Blue1Brown "Essence of Linear Algebra"** — YouTube series
  - Episodes 1–10: vectors, matrices as transformations, change of basis, eigenvectors
  - Episode 14: **SVD** (most important)
  - Episode 15: Abstract vector spaces
  - *Why first:* every analysis treats matrices as geometric operations. Without this,
    you're just running numpy commands; with it, you predict results before running them.

---

## Tier 1 — Non-negotiable math (this week, ~8 hours)

### 1. SVD — *the* tool
- [ ] Trefethen & Bau "Numerical Linear Algebra" Lectures 4–5 (~30 pages)
- Understand:
  - Every matrix `M = U Σ Vᵀ` — one canonical decomposition
  - Singular values = how much M stretches each direction
  - Top-k SVD = best rank-k approximation (Eckart-Young theorem)
  - "Subspace" = span of top-k left or right singular vectors
- **Connects to project:** the canonical coordinate of LoRA's ΔW *is* its SVD after
  QR-gauge-fixing.

### 2. QR decomposition
- [ ] Trefethen & Bau Lectures 7–8
- Understand:
  - `M = QR`, Q orthonormal, R upper-triangular
  - Gram-Schmidt is QR (one column at a time)
  - QR fixes a canonical orthonormal basis of the column space
- **Connects to project:** QR(B) kills the GL(r) ambiguity in `(B, A) → (BG, G⁻¹A)`.

### 3. Marchenko-Pastur (RMT, baby version)
- [ ] Wikipedia "Marchenko-Pastur distribution" (15 min)
- [ ] Martin & Mahoney 2018 "Implicit Self-Regularization in Deep Neural Networks" §3
- Understand:
  - Random Gaussian matrix → singular values follow MP distribution
  - Sharp upper edge at `(√m + √n)·σ_noise` — above = signal, below = noise
  - This defines "what counts as a real direction" in our Region 1/2/3 split

### 4. Heavy-Tailed Self-Regularization (HT-SR)
Read in order:
- [ ] Martin & Mahoney 2018 (the original)
- [ ] `finding_literature/from_spikes_to_heavy_tails_spectral_evolution.pdf` (5+1 phases)
- [ ] `finding_literature/alphalore_htsr_rank_allocation.pdf` (practical α computation)
- [ ] WeightWatcher GitHub README (`CalculatedContent/WeightWatcher`)
- Understand:
  - Trained NN weight spectra follow power laws: `P(σ) ∝ σ^{-α}`
  - α ≈ 2 → universal / well-trained; α ≫ 2 → undertrained; α ≪ 2 → overtrained
  - 5 phases of training: random → bulk+spikes → bulk decay → spikes again → heavy tail
- **Connects to project:** per-checkpoint α is one scalar per layer per timestep.
  Trajectory of α over training = HT-SR phase passage. Direct addition to our analysis.

---

## Tier 2 — Geometry that makes "region anatomy" rigorous (week 2, ~6 hours)

### 5. Grassmannian + principal angles
- [ ] Boumal "An Introduction to Optimization on Smooth Manifolds" Chapter 7
  (free PDF at sites.google.com/site/nicolasboumal)
- Understand:
  - Gr(r,n) = set of all r-dim subspaces of ℝⁿ, a manifold
  - Two subspaces compared via principal angles: `cos(θᵢ) = σᵢ(U₁ᵀU₂)`
  - Grassmannian distance: `d_G = √(Σθᵢ²)` (geodesic) or `√(Σsin²θᵢ)` (chordal)
- **Connects to project:** the right distance for "are two LoRAs in the same subspace?"
  This *is* the pairwise C1 measurement.

### 6. GL(r) quotient + gauge fixing
- [ ] `finding_literature/w2t_lora_weights_know_capabilities.pdf` §3
- [ ] `finding_literature/arxiv_2406_08447.md` (Hayou AsymmetryOfLoRA)
- Understand:
  - LoRA's `(B, A)` has redundancy: `(BG, G⁻¹A)` gives same ΔW for any `G ∈ GL(r)`
  - The quotient space `{LoRA factors} / GL(r)` is what's actually identifiable
  - QR+SVD picks a unique representative per equivalence class — the canonical form
- **Connects to project:** without gauge-fixing, distances between LoRAs are meaningless.
  Two reparameterizations of the same model would have arbitrary "distance."

### 7. Linear mode connectivity (LMC)
- [ ] Frankle et al. 2020 "Linear Mode Connectivity and the Lottery Ticket Hypothesis"
- [ ] `finding_literature/arxiv_1912_05671.md` (the corpus summary)
- [ ] `finding_literature/arxiv_2205_12411.md` (Juneja 2022 — BERT disconnection)
- Understand:
  - Two fine-tunes are LMC if the line segment between them stays low-loss
  - This is what makes "knowledge is a region" precise — a region is LMC-connected
  - BERT-style often *isn't* LMC; well-pretrained LLMs usually are
- **Connects to project:** the falsifier. If your hellaswag LoRAs aren't LMC, "region"
  reduces to "cluster of disconnected points" and the whole framing weakens.

---

## Tier 3 — Project-mapped papers (week 2–3, ~10 hours)

Read in this order:

- [ ] `relevant_literature/KnowledgeIsARegionInWeightSpace.pdf` — Gueta 2022, the existence proof
- [ ] `finding_literature/w2t_lora_weights_know_capabilities.pdf` — Salama, your QR+SVD machinery
- [ ] `finding_literature/arxiv_2406_08447.md` — Hayou AsymmetryOfLoRA, B-only anchor
- [ ] `finding_literature/lora_vs_fullft_intruder_dimensions.pdf` — Shuttleworth, intruder dims
- [ ] `finding_literature/subspace_geometry_catastrophic_forgetting_lora.pdf` — Steele 2026,
      principal angles → forgetting
- [ ] `finding_literature/universal_weight_subspace_hypothesis.pdf` — many LoRAs share a subspace
- [ ] `finding_literature/from_spikes_to_heavy_tails_spectral_evolution.pdf` — trajectory phases
- [ ] `finding_literature/alphalore_htsr_rank_allocation.pdf` — practical α
- [ ] `finding_literature/weight_space_learning_survey.pdf` — Schürholt survey (read LAST,
      it's the map of the field)

---

## Tier 4 — Extras for insight depth (week 3+, optional)

- [ ] **Absil, Mahony, Sepulchre "Optimization Algorithms on Matrix Manifolds"** —
      deeper Riemannian geometry, Stiefel retractions. For *proposing* new metrics.
- [ ] **Tao "Topics in Random Matrix Theory"** — mathematician's view of MP. Free notes.
- [ ] **Amari "Information Geometry and Its Applications"** Ch. 1–3 — Fisher information,
      natural gradient. Useful if you go after "what does the loss landscape look like
      near the region."
- [ ] `finding_literature/implicit_regularization_matrix_factorization_gunasekar.md` —
      why GD on factorized matrices produces sparse-spectrum solutions; predicts which
      directions show up first in trajectories.
- [ ] **Singular Learning Theory** (Watanabe) — math behind LLC (local learning coefficient).
      See `finding_literature/grokking_slt_competing_basins.pdf` for the ML connection.

---

## How to study (not just what)

1. **Interleave reading with running.** Tier 1 #1 (SVD) → run our `canonical.py`
   on `checkpoint-50/` and look at the singular value spectrum → Tier 1 #3 (MP) →
   look at where the MP cutoff falls on that spectrum → Tier 1 #4 (α) → run
   WeightWatcher → ...

2. **Single physical notebook.** When you learn principal angles, write
   `θᵢ = arccos(σᵢ(U₁ᵀU₂))` with a small drawing. When you see Grassmannian
   distance numbers from your own LoRAs, write what they mean.

3. **The "real" test:** after 2 weeks, you can look at a Grassmannian-distance
   matrix figure and explain in 30 seconds: what each cell means, what the
   diagonal-vs-off-diagonal pattern tells you about same-task clustering, why
   we don't use Euclidean distance on flattened weights.

---

## Right-now-tonight plan (training runs ~2 hours)

If you have one evening:

1. **3Blue1Brown episodes 14 + 15** — 25 min
2. **Martin & Mahoney 2018 §1–4** — 45 min
3. **`KnowledgeIsARegionInWeightSpace.pdf` intro + Figure 1** — 15 min
4. **`thesis_plan/test_experiments_archive.md` re-read with fresh frame** — you'll
   see the math behind each archive finding

By end of tonight: vocabulary to read every other paper in the corpus.
By end of next week: depth to interpret your own analysis figures.

---

## Cross-references to memory

- [[project-anatomy-of-lora-region]] — what we're building
- [[feedback-geometry-first-eval-deferred]] — why this math is the deliverable
- [[feedback-explorer-no-code]] — read before writing
- [[feedback-graphify-pdf-discipline]] — real PDFs (not MD abstracts) for each paper
