# Experiment 1 Insights from LoRA-Specific Papers

## From AsymmetryOfLoRA: Your weight-space representation should be B-only

The key empirical finding is that **B matrices cluster by task, A matrices don't**. B encodes what the model has learned to predict; A encodes what input features to extract, and when initialization is fixed (as it would be in your controlled population), A is nearly identical across tasks.

**Direct implications:**

- Use B matrices as your primary weight-space coordinate. ΔW = BA conflates two structurally different things. B alone is the task-specific signal.
- A matrices are noise for your geometry — including them dilutes within-task clustering and inflates cross-task distances artifactually.
- Your population of LoRAs trained at fixed parameterization (same rank, same target_modules, same init) will have near-constant A. The variance in weight space is almost entirely in B.

**For Experiment 1 setup:** Target `q_proj` and `v_proj` and extract only B matrices for your weight-space coordinate. You get cleaner geometry for free.

---

## From AdaLoRA: The geometry is not uniform — layer position and module type predict information density

AdaLoRA's importance scores across layers and modules reveal a consistent gradient: **FFN layers carry more task-specific adaptation than attention layers, and top layers carry more than bottom layers.** This isn't an artifact of AdaLoRA's method — it's the underlying distribution of task-relevant singular values.

**Direct implications:**

- If you flatten all LoRA weights into a single vector for geometry analysis, you're averaging a high-signal region (top-layer FFN) with a low-signal region (early-layer attention). The result is a noisy coordinate.
- Layer-wise representation is more informative than a single flattened vector. Consider: compute weight-space coordinates separately per layer (or per layer group: bottom third, middle third, top third) and see whether task clustering is sharper at top layers.
- The singular value distribution within each ΔW = PAQ tells you rank utilization. Two LoRAs with the same nominal rank r but different effective rank (number of non-negligible singular values) may behave differently despite having similar benchmark scores — exactly the kind of disagreement your project is looking for.

**Hidden implication for your behavioral/weight joint analysis:** If behavioral scores are driven by top-layer adaptation and weight-space distances are dominated by lower-layer variance, the two coordinates will appear weakly correlated. But that weak correlation is itself a finding: benchmark scores are not measuring the same thing as weight-space position. This directly supports your cross-signal framing.

---

## From SymmetriesInWSL: Your distance metric must match what you're predicting

The symmetry hierarchy is:
- **Zeroth-order features** (performance prediction, task identity) → fully GL_r(ℝ)-invariant
- **Sensitivity/Hessian features** (gradient behavior, fine-tuning stability) → only O(r)-invariant
- **Coordinate-specific features** (which direction in weight space the adaptation moved) → no symmetry

**What this means for your distance metric:**

If you compute raw Euclidean distance between B matrices across tasks, you're using a coordinate-specific metric — it has no symmetry and will give you arbitrary distances depending on initialization. Two LoRAs that are functionally identical could appear far apart.

For **task clustering** (predicting which task a LoRA was trained on from weight space alone), you want a GL_r-invariant metric. The natural choice: compare singular value spectra of B, not raw B values. The singular values of B are GL_r-invariant (the SVD is unique up to sign flips).

For **predicting fine-tuning behavior / sensitivity** (e.g., whether a LoRA will merge well, or whether its performance will degrade under small weight perturbations), you want an O(r)-invariant metric.

**This gives you a concrete experimental design:** Run your downstream prediction task (e.g., merge compatibility) with three distance metrics:
1. Raw Euclidean on ΔW = BA (no symmetry)
2. Singular-value distance on B (GL_r invariant)
3. Frobenius on BᵀB (O(r) invariant, equivalent to comparing Gram matrices)

If the GL_r-invariant metric outperforms raw Euclidean on task prediction, and the O(r)-invariant metric outperforms on sensitivity prediction, you have a clean demonstration that symmetry-awareness is necessary — which is a methodological contribution, not just an empirical finding.

---

## Hidden Cross-Paper Insights

**1. B-only + singular value spectrum = the canonical Experiment 1 representation**

AsymmetryOfLoRA says use B. SymmetriesInWSL says use a GL_r-invariant feature of B. AdaLoRA says the singular values of ΔW carry the task-relevant signal. These three converge on one answer: **your weight-space coordinate should be the singular value spectrum of B, computed per layer, aggregated across layers with importance weighting.** This is more principled than any single paper recommends.

**2. The "same benchmark, different weight space" story has a mechanistic explanation**

AdaLoRA shows that two models can achieve the same benchmark score with different rank distributions (one concentrates adaptation in attention, another in FFN). AsymmetryOfLoRA shows that B varies significantly within-task across seeds. SymmetriesInWSL shows that coordinate-specific features have no symmetry — so two LoRAs with the same B singular value spectrum can still be at different coordinates in weight space. Together: **benchmark score is invariant to a large family of weight-space transformations**. Your paper's contribution is mapping out which transformations those are.

**3. Rank is a confound you can control for**

AdaLoRA reveals that nominal rank r ≠ effective rank. If you train all LoRAs at rank 8, some will effectively use rank 3-4 (concentrated singular values) and others will spread across all 8. This means your population isn't actually at fixed parameterization in terms of information content, even with fixed r. You can control for this: compute effective rank per LoRA (number of singular values above some threshold, e.g., 1% of the max), and include it as a covariate in your analysis. LoRAs with similar effective rank but different task assignments are the cleanest test of your geometry.

**4. A-matrix variation can test cross-seed robustness**

The asymmetry paper shows A is task-agnostic when initialization is fixed. But if you use different seeds, A initialization differs. This means the same task trained from different seeds will have the same B structure but different A. If your B-based distance correctly clusters these as the same task despite A variation, you've validated that B-only representation is robust — a concrete ablation for the methods section.

---

## Concrete Experiment 1 Changes

| Decision | Before | After |
|---|---|---|
| Weight-space coordinate | Full ΔW = BA flattened | Singular value spectrum of B, per layer |
| Target modules | `q_proj, v_proj` | Add `up_proj, down_proj` — FFN matters more |
| Distance metric | TBD | Three variants: raw / GL_r-invariant / O(r)-invariant |
| Layer analysis | Single representation | Layer-grouped (bottom/mid/top) |
| Confound control | None | Effective rank as covariate |

The FFN addition is worth flagging: AdaLoRA consistently shows `up_proj`/`down_proj` carry more task-relevant singular values than attention projections. If you only target `q_proj`/`v_proj`, you're leaving the high-information-density layers out of your weight-space representation.
