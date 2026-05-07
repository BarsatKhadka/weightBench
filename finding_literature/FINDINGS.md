# Literature Findings — Autonomous Night Run
_Last updated: Iteration 1 (complete)_

---

## The Platonic Representation Hypothesis (arxiv:2405.07987)
**Key finding**: Neural network representations converge toward a shared statistical model of reality as models scale. Vision and language models develop increasingly aligned distance metrics between datapoints.
**Implication for Experiment 1**: If LoRA adaptations converge toward shared representations for the same task, the weight-space geometry of a LoRA population should reflect task structure — supporting dual-signal framing.
**Implication for Experiment 2 / cross-model**: Theoretical grounding for cross-model comparison. Two LoRAs from different base models trained on the same task may converge to similar adaptation geometry.
**Extraordinary idea triggered**: If the Platonic hypothesis holds at the LoRA level, B-matrix singular value spectra for same-task LoRAs from different base models should cluster together — no alignment step needed.

---

## Revisiting the Platonic Representation Hypothesis: Aristotelian View (arxiv:2602.14486)
**Key finding**: CKA contains biases that inflate alignment. After permutation-based calibration, convergence evidence weakens. Networks retain task-specific and architecture-specific structure.
**Implication for Experiment 1**: Do NOT use raw CKA. Use calibrated metrics with permutation-based null distributions.
**Implication for Experiment 2 / cross-model**: Any cross-model similarity must be validated above permutation null. SVD spectra bypass CKA bias entirely.
**Extraordinary idea triggered**: SVD spectrum of B is the calibration-robust, CKA-free similarity metric the Aristotelian critique demands.

---

## Towards Universality: Mechanistic Similarity Across Language Model Architectures (arxiv:2410.06672)
**Key finding**: Transformers and Mambas share most SAE-extracted features. Induction circuits are structurally analogous. Feature similarity correlates with universality predictions. One difference: Off-by-One motif.
**Implication for Experiment 1**: Confirms mechanistic similarity exists across radically different architectures. Within-architecture LoRA populations should show even stronger structure.
**Implication for Experiment 2 / cross-model**: Direct motivation — if base architectures share mechanistic structure, LoRA adaptations for the same task should share adaptation geometry. Off-by-One is exactly the hidden difference benchmarks miss.
**Extraordinary idea triggered**: SAE features as cross-model substrate — architecture-agnostic monosemantic units that LoRAs activate similarly for same tasks regardless of base model.

---

## The Triangle of Similarity (arxiv:2601.17093)
**Key finding**: Three views — (1) Static: CKA/Procrustes, (2) Functional: linear mode connectivity, (3) Sparsity: robustness under pruning. Architecture family is primary determinant of similarity. Pruning exposes shared computational core.
**Implication for Experiment 1**: Run all three views on LoRA population — divergence between static and functional views IS the finding.
**Implication for Experiment 2 / cross-model**: Functional view (linear mode connectivity) is architecture-agnostic — viable cross-architecture comparison without weight alignment.
**Extraordinary idea triggered**: Use all three views. If all three agree on cross-architecture similarity, it's real. If they disagree, the disagreement is the finding.

---

## Model Stitching by Functional Latent Alignment — FuLA (arxiv:2505.20142)
**Key finding**: Optimal affine transformation aligns two models for task performance. Stitched model is proxy for functional similarity. More robust to task-cue artifacts than conventional stitching.
**Implication for Experiment 1**: FuLA as downstream prediction validation — if two LoRAs are close in B-SVD space, they should stitch well (low FuLA loss).
**Implication for Experiment 2 / cross-model**: Apply FuLA between LoRA-adapted models from different base models trained on same task. Alignment loss = continuous measure of cross-model adaptation similarity.
**Extraordinary idea triggered**: Cross-model LoRA stitching as a benchmark — stitch Llama's task-adapted layers into Mistral. If stitching quality correlates with B-SVD distance, you've validated spectral fingerprints.

---

## Revisiting Model Stitching in the Foundation Model Era (arxiv:2603.12433)
**Key finding**: Feature-matching loss at penultimate layer makes heterogeneous VFMs stitchable. Conventional approaches fail at shallow stitch points. VFM Stitch Tree shares early layers.
**Implication for Experiment 2**: Shallow stitch fails, deep stitch succeeds — target stitching at deep layers where task signal concentrates (confirmed by AdaLoRA).
**Extraordinary idea triggered**: Stitch only at LoRA-targeted layers (FFN layers). If those layers are cross-base-model stitchable after LoRA adaptation, LoRA has created a shared representational interface.

---

## Bridging Critical Gaps in Convergent Learning (arxiv:2502.18710)
**Key finding**: Orthogonal Procrustes aligns representations nearly as well as full linear maps. Alignment crystallizes within first epoch (architecture-driven). Early layers align well; deep layers diverge under distribution shift.
**Implication for Experiment 1**: Orthogonal Procrustes is right alignment method — confirms O(r)-invariant metric is best choice.
**Implication for Experiment 2 / cross-model**: Focus on deep-layer B-matrix SVD spectra — they're the task-specific signal (not architecture-driven convergence).
**Extraordinary idea triggered**: Top-layer-only LoRA training + B-matrix SVD comparison. If same-task LoRAs from different architectures cluster in deep-layer SVD spectrum space better than cross-task LoRAs from same architecture → task > architecture in spectral geometry.

---

## Intrinsic Dimensionality of Language Model Fine-Tuning (arxiv:2012.13255)
**Key finding**: Pre-trained LMs have very low intrinsic dimension for fine-tuning. 90% of full performance with only 200 parameters in random subspace. Pre-training minimizes intrinsic dimension.
**Implication for Experiment 1**: Effective rank of B IS the intrinsic dimension of the adaptation. Varies by task. Tasks requiring higher effective rank are structurally more complex.
**Implication for Experiment 2 / cross-model**: If two base models learn the same task with different effective ranks (intrinsic dimensions), they have different internal mechanisms at equal benchmark score.
**Extraordinary idea triggered**: Intrinsic dimension as task complexity fingerprint. Plot (benchmark score) vs (effective rank) colored by base model — clustering by architecture at fixed benchmark score = cross-model mechanistic difference.

---

## LoRA vs Full Fine-tuning: An Illusion of Equivalence (arxiv:2410.21228) *** CRITICAL ***
**Key finding**: LoRA introduces "intruder dimensions" — novel high-ranking singular vectors absent in base model and absent in full fine-tuning. Intruder dimensions drive catastrophic forgetting. Reducing intruder dimension singular values improves pre-training distribution modeling with minimal task performance drop.
**Implication for Experiment 1**: **Intruder dimensions ARE the task-specific spectral fingerprint of B matrices.** The B matrix is rank-r by construction, and its singular values represent the intruder dimensions relative to the base model. This is the signal to compare.
**Implication for Experiment 2 / cross-model**: If same-task LoRAs from different base models produce similar intruder dimension patterns (similar B-matrix singular value distributions), task identity is encoded architecture-agnostically. If patterns differ, architectures have different task encoding mechanisms.
**Extraordinary idea triggered**: The intruder dimension count, magnitude distribution, and concentration index are the cross-architecture task fingerprint. Compare these three statistics across architectures for same-task LoRAs. This is already theoretically grounded — it's a direct measurement of what LoRA's B matrix does that full fine-tuning doesn't.

---

## Small Singular Values Matter: Random Matrix Analysis of Transformers (arxiv:2410.17770) *** CRITICAL ***
**Key finding**: Both large AND small singular values carry task information. After fine-tuning, smallest 10% of singular values = 3rd most influential portion. Fine-tuning refines the model primarily in small singular value regions (departures from Random Matrix Theory). Small singular vectors align with activation covariance eigenvectors.
**Implication for Experiment 1**: Don't only look at top singular values of B. The full spectrum matters. Use the ENTIRE singular value distribution (not just top-k) when comparing LoRAs.
**Implication for Experiment 2 / cross-model**: The departure from RMT baseline at both spectrum extremes is the task-specific signal. Measure: for each LoRA, compute KL divergence from RMT null distribution at large AND small singular value tails. This RMT-deviation fingerprint is potentially architecture-agnostic.
**Extraordinary idea triggered**: RMT as the universal baseline for spectral fingerprinting. The deviation pattern (what departs from random) encodes task; the random component encodes architecture noise. Separate them: task fingerprint = RMT deviation, architecture noise = RMT-conforming component.

---

## Weight Spectra Induced Efficient Model Adaptation (arxiv:2505.23099)
**Key finding**: Fine-tuning amplifies top singular values while leaving remainder largely intact. Dominant singular vectors rotate toward task-specific directions. Non-dominant subspaces remain stable. Fine-tuning = selective amplification in low-dimensional subspace.
**Implication for Experiment 1**: Singular vector rotation angle (not just magnitude) encodes task identity. Two LoRAs with similar singular values but different vector directions may be in different task regions.
**Implication for Experiment 2 / cross-model**: The rotation direction of top singular vectors during adaptation might converge across architectures for the same task. But rotation direction IS coordinate-dependent — need GL_r-invariant version (i.e., compare the subspace, not the vectors).
**Extraordinary idea triggered**: Subspace angle between pre-trained weight singular subspace and LoRA-adapted singular subspace = task adaptation direction. This is coordinate-independent if measured as principal angles between subspaces (which are GL_r-invariant).

---

## A Survey of Weight Space Learning (arxiv:2603.10090)
**Key finding**: Three dimensions — WSU (geometry and symmetries), WSR (weight embeddings), WSG (hypernetworks, generative models). Weights can be embedded, compared, and generated. Rich structure in weight space enables model retrieval, continual learning, neural architecture search.
**Implication for Experiment 1**: The entire project IS a WSU+WSR study. We're doing WSU (geometry of LoRA population) and using it for downstream prediction (WSR territory).
**Implication for Experiment 2 / cross-model**: WSR methods (learned weight embeddings) could be used to embed LoRAs from different architectures into a shared space. If a learned encoder can embed cross-architecture LoRAs in a shared space where task identity clusters — that's a WSR contribution.
**Extraordinary idea triggered**: Train a small hypernetwork that takes any LoRA's B matrices as input and outputs a task embedding. Train it to cluster same-task LoRAs regardless of base model. This is a WSG/WSR hybrid that directly solves the cross-model comparison problem.

---

## Foundation Models Secretly Understand Neural Network Weights (arxiv:2503.00838)
**Key finding**: Foundation models (LLMs/VLMs) can process and understand neural network weights. Transformer-based architectures improve hypernetworks through foundation model understanding.
**Implication for Experiment 1**: Could use a foundation model to "read" LoRA B matrices and predict task identity — a neural weight reader.
**Implication for Experiment 2 / cross-model**: Train a foundation model to read B matrices from any architecture and predict task clusters. Cross-architecture invariance emerges from the foundation model's generalization.
**Extraordinary idea triggered**: Fine-tune an LLM on LoRA B matrices as sequences. The LLM learns to "understand" weight space. Ask it: "are these two LoRAs doing the same task?" This is using language to bridge the cross-architecture comparison problem.

---

## Grokking as Dimensional Phase Transition (arxiv:2604.04655) *** CRITICAL ***
**Key finding**: Grokking = transition in effective dimensionality D (reflecting gradient field geometry, NOT architecture). Sub-diffusive (D<1) = memorization. Super-diffusive (D>1) = generalization. D is architecture-independent — it reflects how gradient information propagates through weight space.
**Implication for Experiment 1**: B-matrix effective rank undergoes a phase transition at generalization. Pre-grokking: high effective rank (memorization). Post-grokking: low effective rank (generalization). The POST-GROKKING B matrix is the right one to compare. Standard LoRA training may stop before grokking.
**Implication for Experiment 2 / cross-model**: Since D is architecture-agnostic, the grokking transition in B-matrix effective rank occurs at the same N for the same task across architectures. Post-grokking effective rank is architecture-independent — directly supporting the TRS universality claim.
**Extraordinary idea triggered**: Train LoRAs PAST the grokking transition (train longer with weight decay). Compare their post-grokking TRS across architectures. The signal is cleaner because memorization noise is purged. This is a concrete protocol for getting clean TRS measurements.

---

## Grokking as Phase Transition between Competing Basins — SLT (arxiv:2603.01192)
**Key finding**: Grokking = competition between memorization basin and generalization basin. Local learning coefficient (LLC) measures loss landscape degeneracy. Low LLC = concentrated singular values = simple task. High LLC = complex task. LLC scales with problem difficulty.
**Implication for Experiment 1**: LLC of each LoRA adapter IS the SLT-theoretic effective rank. Use LLC as an additional task complexity measure alongside effective rank from TRS.
**Implication for Experiment 2 / cross-model**: If same task on two architectures converges to solutions with the same LLC, task SLT complexity is architecture-agnostic. Testable: compute LLC for Llama and Mistral LoRAs on same tasks.
**Extraordinary idea triggered**: LLC-based taxonomy of tasks — cluster by LLC regardless of semantic task type. If clusters match semantic categories, task complexity is geometrically encoded in weight space in an architecture-agnostic way.

---

## Unraveling LoRA Interference: Orthogonal Subspaces — OSRM (arxiv:2505.22934)
**Key finding**: LoRA subspace overlap causes task interference in merging. OSRM: constrain LoRA subspaces to be orthogonal before fine-tuning. Orthogonal subspaces = zero interference. Subspace overlap = merge quality predictor.
**Implication for Experiment 1**: Principal angles between B-matrix column spaces predicts merge quality. This IS the concrete downstream prediction for Experiment 1. Weight-space distance (subspace overlap) → behavioral outcome (merge quality). Clean, measurable, falsifiable.
**Implication for Experiment 2 / cross-model**: Cross-architecture LoRAs for the same task should occupy "the same" subspace (after Procrustes). Measure cross-architecture subspace overlap for same-task vs cross-task pairs.
**Extraordinary idea triggered**: Same-task LoRAs from different architectures → Procrustes-align B-column-spaces → if principal angles are small (high overlap), task encodes in universal subspace. Cross-task from same architecture → large angles. This is a direct test of TRS universality using subspace geometry rather than spectral distances.

---

## Singular Learning Theory for Grokking (arxiv:2512.00686)
**Key finding**: SLT free energy and local learning coefficient measure model complexity from loss landscape geometry. Applies to low-rank networks. LLC scales with problem difficulty. Phase transitions are SLT-predicted.
**Implication for Experiment 1**: LoRA adapters ARE low-rank networks — SLT applies directly. LLC of a LoRA adapter = effective model complexity. Theoretically grounded measure of task intrinsic dimensionality.
**Implication for Experiment 2**: SLT predicts that same task on different-capacity models should converge to same LLC. Architecture is a nuisance variable; task complexity is the signal.
**Extraordinary idea triggered**: Purely geometric task taxonomy — cluster LoRAs by LLC. If this matches semantic task categories, task complexity is a weight-space invariant.

---

## The Universal Weight Subspace Hypothesis (arxiv:2512.05117) *** CRITICAL — DIRECT VALIDATION ***
**Key finding**: Deep neural networks systematically converge to shared spectral subspaces regardless of initialization, task, or domain. Empirically validated across 1,100+ models: 500 Mistral-7B LoRAs, 500 Vision Transformers, 50 LLaMA-8B models. Universal subspaces capture majority variance in just a few principal directions. These sparse joint subspaces are consistently exploited within shared architectures across diverse tasks and datasets.
**Implication for Experiment 1**: This is within-architecture validation of TRS universality. The shared spectral subspace IS the "prior" that TRS measures departure from. If 500 same-architecture LoRAs converge to a shared subspace, the TRS is measuring deviation from that shared baseline — exactly what we claim.
**Implication for Experiment 2 / cross-model**: The LLaMA-8B sample (50 models) vs Mistral-7B sample (500 models) are separate populations. The KEY open question they DON'T address: do the universal subspaces from Mistral-7B and LLaMA-8B ALIGN with each other? This is our novel contribution — cross-architecture universal subspace comparison.
**Extraordinary idea triggered**: If the universal subspace is architecture-specific (Mistral has one, LLaMA has a different one), then TRS must be architecture-normalized. If the subspaces align across architectures (Platonic hypothesis would predict this), TRS is directly comparable. The Universal Subspace Hypothesis gives us the TEST: measure principal angles between the universal subspaces of Mistral-7B and LLaMA-8B LoRA populations. Small angles → cross-architecture TRS comparison is valid without normalization. Large angles → need Procrustes alignment first.

---

## W2T: LoRA Weights Already Know What They Can Do (arxiv:2603.15990)
**Key finding**: LoRA checkpoints inherently encode task-specific information, recoverable without running the base model or accessing training data. The key technical contribution: a canonical form via QR decomposition followed by SVD, resolving the infinite-factorization ambiguity of LoRA (ΔW = BA has infinitely many valid factorizations). Once factorization ambiguity is removed, weights reliably predict adapter behavior. Validated on language and vision LoRA collections for attribute classification, performance prediction, and adapter retrieval.
**Implication for Experiment 1**: W2T's canonical form (QR then SVD) is the correct preprocessing step before computing TRS. We should apply QR+SVD rather than naive SVD to avoid fitting factorization artifacts. The canonical singular values are the true task fingerprint.
**Implication for Experiment 2 / cross-model**: W2T proves that task capability prediction from weights is architecture-agnostic enough to work on vision AND language LoRAs. If weight → task identity works cross-modality, it almost certainly works cross-architecture within the same modality. This is strong circumstantial evidence for cross-model TRS universality.
**Extraordinary idea triggered**: W2T's adapter retrieval task is the direct downstream validation for TRS. If TRS distances predict retrieval performance (same-task LoRAs retrieved as similar), TRS is validated as a task fingerprint. We can use W2T's benchmark dataset as our validation set for Experiment 1 without training new LoRAs.

---

## Cross-LoRA: Data-Free LoRA Transfer Across Heterogeneous LLMs (arxiv:2508.05232)
**Key finding**: LoRA modules can be transferred between different LLM architectures without any training data, using rank-truncated SVD + Frobenius-optimal linear transformation for subspace alignment. The transfer runs in ~20 minutes on standard GPU hardware. Results show up to 5.26% relative improvement on ARCs, OBOA, and HellaSwag compared to baseline, maintaining performance parity on commonsense reasoning.
**Implication for Experiment 1**: The Frobenius-optimal linear transformation between subspaces IS the alignment step that TRS aims to make unnecessary. If TRS works (architecture-agnostic fingerprint), you don't need Cross-LoRA's alignment — you can compare directly. If TRS fails, Cross-LoRA's alignment is the fallback.
**Implication for Experiment 2 / cross-model**: Cross-LoRA validates that cross-architecture LoRA transfer is feasible. More importantly: the quality of Cross-LoRA transfer for same-task pairs vs cross-task pairs is a measure of task-subspace similarity — exactly what TRS claims to capture. Low Cross-LoRA transfer loss for same-task, different-architecture pairs → high TRS similarity prediction. This gives us an independent behavioral validation of TRS.
**Extraordinary idea triggered**: Use Cross-LoRA transfer quality as TRS validation oracle. Train TRS predictor on pairs, then use actual Cross-LoRA transfer results to validate. If TRS predicts transfer quality (correlation > 0.7), TRS has been validated as an architecture-agnostic task fingerprint. This is a clean, single-number falsifiable test.

---

## Task Singular Vectors: Reducing Task Interference in Model Merging (arxiv:2412.00081)
**Key finding**: Task vectors (ΔW = BA) are low-rank structures when examined at the layer level via SVD. The resulting singular vectors (Task Singular Vectors, TSV) quantify task interference through interaction of singular vectors from different tasks. TSV-Compress reduces task matrices to 10% of size while retaining 99% accuracy. TSV-Merge combines compression with interference reduction, significantly outperforming existing merging methods. Accepted to CVPR 2025.
**Implication for Experiment 1**: TSV are the layer-level spectral fingerprint of task vectors — equivalent to our B-matrix singular vectors but applied to ΔW = BA instead of B alone. The interference measure (singular vector interaction) is the inverse of TRS similarity. High TSV-distance between two LoRAs = high interference = low TRS similarity. This is an alternative operationalization of the same underlying geometry.
**Implication for Experiment 2 / cross-model**: If TSV interference measurement works for same-architecture merging, the cross-architecture version (using Procrustes-aligned TSVs) should work for cross-model comparison. Tasks that interfere heavily within architecture should also show large TRS distance across architectures.
**Extraordinary idea triggered**: The spectral skewness of task matrices affects merge quality (per the isotropic merging literature). Skewed spectra (concentrated singular values) = fewer dominant components = easier to separate tasks. Flat spectra = many comparable singular values = tasks bleed together. TRS can predict merge success from skewness alone, without running the merge — a 0-shot merge quality predictor.

---

## AlphaLoRA: Assigning LoRA Experts Based on Layer Training Quality (arxiv:2410.10054)
**Key finding**: Heavy-Tailed Self-Regularization (HT-SR) theory provides a training-free measure of layer training quality via the power-law exponent α of the empirical spectral density (ESD). Number of LoRA experts per layer should correlate with layer training quality, which varies significantly across layers. AlphaLoRA uses α to allocate LoRA capacity non-uniformly across layers, achieving comparable or superior performance to uniform allocation baselines across 10 language benchmarks.
**Implication for Experiment 1**: The HT-SR power-law exponent α is a layer-level quality metric that is independent of our TRS. Together, they give two orthogonal views of the same layer: α measures how well-trained the pre-trained layer is (base model quality), TRS measures how much the LoRA added to it (task signal). Layers where α is large but TRS is small = layer doesn't need adaptation. Layers where α is small but TRS is large = most important layers for the task.
**Implication for Experiment 2 / cross-model**: HT-SR theory (Martin & Mahoney) is architecture-agnostic — the power-law exponent α is well-defined for any weight matrix regardless of architecture. Cross-architecture comparison: layers with similar α values in Llama vs Mistral are in the "same training state" and should be the best candidates for cross-model LoRA transfer. α as a layer matching criterion for cross-model stitching.
**Extraordinary idea triggered**: A 2D layer selection criterion: (α of base layer) × (TRS of LoRA B matrix). High α × high TRS = this layer is well-trained AND the task strongly adapted it = the most information-dense layer for cross-model comparison. Low α × low TRS = this layer is poorly trained AND task-irrelevant = skip it. This α×TRS selection criterion for cross-model LoRA stitching has not been proposed by any paper.

---

## No Task Left Behind: Isotropic Model Merging (arxiv:2502.04959) *** CRITICAL — TRS PREDICTS MERGE QUALITY ***
**Key finding**: Spectral skewness of task vectors directly predicts merge quality. Skewed singular value distributions (one large, others small — concentrated spectrum) create misalignment between task and merged weight matrices, degrading performance. Isotropic merging (flattening the singular value spectrum while preserving singular vectors) achieves state-of-the-art merge performance. The core mathematical insight: alignment between singular components of task-specific and merged matrices correlates with performance improvement. Validated on vision and language tasks at multiple model scales.
**Implication for Experiment 1**: TRS is the SPECTRAL SKEWNESS of the B-matrix singular values relative to the Marchenko-Pastur null. High TRS (large departures from null) = concentrated spectrum = skewed. Low TRS = flat spectrum = isotropic. Isotropic merging shows flat spectra → better merge. Prediction: same-task LoRAs will have similar skewness (similar TRS), making them compatible for merging. Cross-task LoRAs will have different skewness profiles, predicting interference. This directly validates our "TRS distance predicts merge quality" hypothesis.
**Implication for Experiment 2 / cross-model**: If same-task LoRAs from Llama and Mistral have similar spectral skewness profiles (similar TRS), they should merge well across architectures. Different-task LoRAs from the same architecture should have different skewness. Test: compute TRS skewness correlation within-task (across architectures) vs across-task (same architecture). If within-task correlation > across-task correlation, spectral skewness is architecture-agnostic.
**Extraordinary idea triggered**: The isotropic merging paper provides an EXACT METRIC for validating TRS: Δ(spectral skewness) between two LoRAs should predict their merge quality (via the TRS distance). Run isotropic merging on all pairs of same-task/cross-task LoRAs, measure merge loss. Correlate with TRS distance. If r > 0.6, TRS = the spectral predictor for merge quality. This is the strongest possible downstream validation.

---

## Generalizing Model Merging via Fréchet Averages on Quotient Manifolds (arxiv:2604.27155) *** GL_r PROOF ***
**Key finding**: Model merging should be understood as Fréchet averaging on a Riemannian manifold. For LoRA adapters specifically, architectural symmetries (GL_r group action) induce a QUOTIENT MANIFOLD structure: mathematically equivalent LoRA representations map to the same point in the quotient space. The averaging procedure itself must be symmetry-invariant. Current LoRA merging methods fail because they don't respect this quotient geometry. The paper outlines quotient-compatible primitives for low-rank updates that yield symmetry-corrected merging algorithms.
**Implication for Experiment 1**: This is the PROOF that GL_r-invariant metrics (like TRS singular values) are not just convenient — they are geometrically NECESSARY for correct LoRA comparison. Two LoRAs that are equivalent under GL_r must have the same TRS. The quotient manifold structure means TRS is the NATURAL COORDINATE on the LoRA moduli space. This elevates TRS from "a good choice" to "the only principled choice" for LoRA comparison.
**Implication for Experiment 2 / cross-model**: The quotient manifold structure explains WHY cross-architecture comparison without alignment is possible: both architectures' LoRAs live on quotient manifolds where GL_r acts, and TRS provides canonical coordinates on both quotient manifolds. If the canonical coordinates are comparable (same task), it's because the underlying tasks share a universal point on the quotient. This connects TRS universality to the geometry of fiber bundles over the space of tasks.
**Extraordinary idea triggered**: The Fréchet average on the LoRA quotient manifold IS the "canonical cross-architecture LoRA" — the orbit that all architecture-specific representations orbit around. The TRS of the Fréchet average should equal the average TRS across architectures (for same-task LoRAs). Testing this: compute Fréchet average of Llama + Mistral LoRAs for the same task → compute its TRS → compare to average TRS of individual LoRAs. If they match, TRS is a geodesic invariant of the task, not of the architecture.

---

## Learning in the Fisher Subspace: Guided Initialization for LoRA (arxiv:2605.01046)
**Key finding**: Fisher information (data-aware curvature induced by downstream tasks) should guide LoRA initialization, not just pre-trained weight magnitude. "Data-aware sensitivity, rather than weight-only magnitude, should govern the choice of adaptation subspaces." The Fisher subspace = directions with largest impact on model predictions given the task's data distribution. Validated across diverse tasks and modalities.
**Implication for Experiment 1**: The Fisher subspace IS the optimal TRS: it's the set of directions where task-specific information is encoded. LoRA initialized in the Fisher subspace should have all its B-matrix singular values above the Marchenko-Pastur edge (everything is task-specific, no wasted capacity). The TRS of a Fisher-initialized LoRA should be maximally concentrated. This provides a theoretical upper bound on TRS: TRS_max = Fisher-initialized LoRA's TRS.
**Implication for Experiment 2 / cross-model**: Fisher information is approximately architecture-agnostic (supported by Platonic hypothesis): same task on different architectures induces approximately the same Fisher curvature in the output space. Therefore the Fisher subspaces of Llama and Mistral for the same task should be approximately aligned. PREDICTION: Fisher-initialized LoRAs on Llama and Mistral for the same task should have MORE similar TRS than random-initialized LoRAs, because initialization already places them in the approximately-shared Fisher subspace.
**Extraordinary idea triggered**: A definitive test of TRS universality using Fisher initialization: (1) train Fisher-initialized LoRAs on Llama and Mistral for same tasks, (2) train random-initialized LoRAs on same tasks. PREDICTION: Fisher-initialized LoRAs have higher TRS similarity across architectures than random-initialized LoRAs, because Fisher initialization forces both to start near the universal Fisher subspace. If true, this PROVES that architecture-specific random initialization is the main source of TRS variability, and the universal Fisher subspace is the architecture-agnostic ground truth.

---

## Spectrum: Targeted Training on Signal to Noise Ratio (arxiv:2406.06623) *** INDEPENDENT MP-NULL VALIDATION ***
**Key finding**: Uses the Marchenko-Pastur distribution as an operational null hypothesis to identify which weight matrix dimensions carry real learned signal vs. random noise BEFORE fine-tuning begins. Computes per-layer signal-to-noise ratio by comparing the empirical spectral density to the MP bulk; trains ONLY the high-SNR layers while freezing low-SNR layers. Matches full fine-tuning quality while dramatically reducing GPU memory requirements.
**Implication for Experiment 1**: This paper independently validates the core mathematical operation of TRS — using the MP distribution as a null baseline for signal extraction in neural network weight matrices. Spectrum does it PRE-fine-tuning on base model weights; TRS does it POST-fine-tuning on LoRA B-matrix singular values. These are COMPLEMENTARY, not competing: Spectrum identifies which layers to adapt, TRS identifies what was learned in each layer.
**Implication for Experiment 2 / cross-model**: The α×TRS 2D layer selection map we proposed (AlphaLoRA × TRS) is directly supported by Spectrum: α measures base model spectral health (HT-SR), and Spectrum's SNR measures the same thing via MP null. The α×TRS map has PRIOR ART in Spectrum's layer selection logic, making our 2D extension a natural generalization. We independently proposed this combination before finding Spectrum — strong convergent discovery.
**Extraordinary idea triggered**: Spectrum's framework can be applied to LoRA B-matrix singular values directly: the "signal" dimensions are those above the MP edge (TRS > 0), the "noise" dimensions are those within the MP bulk (TRS = 0). The number of signal dimensions = effective rank of TRS = task complexity. This gives a clean operational definition of "task complexity" from spectral first principles, matching what NTK theory predicts (effective rank ∝ √N).

---

## Learning on LoRAs: GL-Equivariant Processing of Low-Rank Weight Spaces (arxiv:2410.04207) *** CONFIRMS TRS IS LEARNABLE ***
**Key finding**: Introduces the "Learning on LoRAs" (LoL) paradigm — training a meta-network on LoRA weight matrices as data points to predict task properties (downstream accuracy, harmful fine-tune detection, training data membership, training data characteristics). Critical technical challenge: LoRA weights have GL_r parameter symmetry (B→BM, A→M⁻¹A for any invertible M). They handle this via canonicalization (equivalent to QR+SVD canonical form) and equivariant layers. Works across thousands of text-to-image and language models.
**Implication for Experiment 1**: LoL EMPIRICALLY CONFIRMS that task properties are learnable from LoRA weight structure. The meta-network extracts GL_r-invariant features — which are exactly the singular value spectra of B matrices (our TRS). TRS is therefore the natural feature space for the LoL paradigm. TRS + LoL = a foundation model for LoRA property prediction, more principled than raw LoL because we use the canonical spectral representation.
**Implication for Experiment 2 / cross-model**: LoL doesn't test cross-architecture transfer. But if LoL can predict task properties from LoRA weights for a single architecture, and TRS is the canonical feature, then cross-architecture LoL using TRS features should predict task identity across architectures. This is a natural extension: train LoL on TRS features from Llama LoRAs, test prediction on Mistral LoRAs. If task property prediction transfers, TRS is architecture-agnostic.
**Extraordinary idea triggered**: LoL + TRS = a "LoRA API for task identity". Given any LoRA checkpoint, compute its TRS, run LoL inference, get: (1) task label, (2) training data characteristics, (3) estimated performance on holdout tasks. This is a zero-shot LoRA audit tool — without running the model, you can identify what task it was trained on. Patent-worthy application of TRS.

---

## When Shared Knowledge Hurts: Spectral Over-Accumulation in Model Merging (arxiv:2602.05536) *** TASK IDENTITY IN DISTINCT SINGULAR DIRECTIONS ***
**Key finding**: When multiple fine-tuned models are merged via linear combination, singular directions shared across models accumulate disproportionately, biasing the merged model toward shared (non-task-specific) subspaces. This spectral over-accumulation degrades performance on individual tasks. Proposes Singular Value Calibration (SVC) to rescale over-accumulated singular values. Achieves ~13% improvement in Task Arithmetic performance by correcting for this bias.
**Implication for Experiment 1**: This paper PROVES that task-specific information resides in DISTINCT singular value directions that are NOT shared across tasks. The shared directions are the "background" (equivalent to the MP null or universal subspace). The task-specific signal is the DEPARTURE from this shared spectrum — which is exactly what TRS measures. Spectral Over-Accumulation provides empirical proof that TRS's decomposition (task signal = departure from null) is the correct and causally meaningful decomposition.
**Implication for Experiment 2 / cross-model**: SVC calibration is architecture-specific (it recalibrates based on the merged model's spectrum). But TRS is calibrated against the universal MP null, which is architecture-agnostic. TRS-based calibration should therefore generalize across architectures in a way that SVC cannot. Prediction: TRS-based merge calibration outperforms SVC for cross-architecture merging because TRS uses the correct (universal) null distribution.
**Extraordinary idea triggered**: SVC recalibrates by pushing accumulated singular values DOWN. TRS recalibrates by normalizing against the MP edge. These are different operations but encode the same insight. A unified "spectral calibration theory": both SVC and TRS are special cases of the principle "normalize singular values against a meaningful null distribution." TRS uses the RMT (MP) null; SVC uses the empirical shared distribution. The MP null is theoretically principled; the empirical null is data-dependent. A hybrid: use the MP null as prior, update with empirical shared distribution — a Bayesian spectral calibration for LoRA.

---

## Subspace Geometry Governs Catastrophic Forgetting in Low-Rank Adaptation (arxiv:2603.02224) *** TASK SUBSPACE GEOMETRY IS CAUSAL ***
**Key finding**: Catastrophic forgetting in LoRA continual learning is governed by the MINIMUM PRINCIPAL ANGLE between task gradient subspaces, not by adapter rank alone. When tasks operate in orthogonal subspaces (large principal angle), forgetting is minimal regardless of rank. When task subspaces overlap, forgetting scales with overlap. This establishes task gradient subspace geometry as the CAUSAL driver of cross-task interference, validated on Split-CIFAR100 and sequential GLUE benchmarks.
**Implication for Experiment 1**: The minimum principal angle between task gradient subspaces is DIRECTLY RELATED to TRS distance: tasks with similar TRS will have overlapping gradient subspaces (small principal angle = high forgetting = high interference). Tasks with very different TRS will have orthogonal gradient subspaces (large principal angle = low forgetting = low interference). TRS predicts continual learning difficulty: high TRS-distance pairs should forget less when sequential-trained than low TRS-distance pairs.
**Implication for Experiment 2 / cross-model**: If TRS is architecture-agnostic, then TRS-predicted principal angles between tasks should be the same across Llama and Mistral. Same-task pairs should have small TRS distance AND small principal angles in both architectures. Different-task pairs should have large TRS distance AND large principal angles in both architectures. Cross-architecture validation of TRS via principal angle predictions is a clean falsifiable test.
**Extraordinary idea triggered**: The minimum principal angle between task subspaces is the forgetting coefficient. TRS distance is the spectral distance between tasks. If these two quantities are correlated (they should be by theory), then TRS predicts not just task identity but task sequentiality — which pairs of tasks can be sequential-trained with minimal forgetting. A "task sequencing algorithm" based on TRS distances: train tasks in an order that maximizes pairwise TRS distances, minimizing forgetting. This is a practical application of TRS to continual learning curriculum design.

---

## A Random Matrix Theory Perspective on the Spectrum of Learned Features (arxiv:2410.18938) *** SPIKED RMT THEORY FOR TRS ***
**Key finding**: Analyzes two-layer neural network feature adaptation after one gradient step using RMT. Establishes an equivalence between updated features and a SPIKED RANDOM FEATURE MODEL in the large-batch limit. Derives exact asymptotic generalization error from the updated feature spectrum. The "spike" above the Marchenko-Pastur bulk represents the task-learned signal; the bulk itself is the random noise component.
**Implication for Experiment 1**: This is the theoretical foundation for TRS. The paper proves that task-specific learning creates SPIKES ABOVE THE MP BULK in the feature spectrum — exactly what TRS proposes to measure. The departure of singular values from the MP edge IS the learned spike. The magnitude of the spike correlates with generalization performance (proved asymptotically). TRS therefore measures not just task identity but TASK LEARNING QUALITY — a quantitative measure of how well the LoRA learned the task.
**Implication for Experiment 2 / cross-model**: If same-task LoRAs on different architectures have learned the task equally well, they should have the same spike structure above the MP bulk (same TRS). Differences in TRS across architectures for same-task LoRAs may reflect differences in TASK LEARNING QUALITY rather than differences in task identity. This is a confound we should measure: compute test performance for each LoRA, and check whether performance differences predict TRS differences across architectures.
**Extraordinary idea triggered**: The spiked RMT model gives an EXACT FORMULA for the optimal signal estimator given a spike above MP. The optimal "denoised" B matrix is the Marchenko-Pastur shrinkage of the singular values: σ_i → max(σ_i - σ_MP_edge, 0). This is the optimal estimator of the task-specific component. The denoised singular values ARE the TRS. Computing TRS is therefore computing the optimal Bayes estimator of the task signal in the LoRA B matrix — a rigorous statistical interpretation of TRS.

---
