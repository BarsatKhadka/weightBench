# CONJECTURE: Universal Subspace ↔ TRS / Intruder Dims Bridge
*Status: OPEN CONJECTURE — do not promote to theorem*
*Written: May 2026 — after advisor warning against premature synthesis*

---

## THE TWO REFERENCE FRAMES (operationally distinct in all existing papers)

**Frame 1 — Shuttleworth (arXiv:2410.21228): W₀-relative**
- Intruder dims = singular vectors of ΔW with cos-similarity < ε to ALL of W₀'s top singular vectors
- Reference: W₀'s top singular subspace U_W₀
- OPLoRA (arXiv:2510.13003) also uses this frame: projects LoRA updates ⊥ to top-k singular vectors of W₀

**Frame 2 — Kaushik (arXiv:2512.05117): Cross-LoRA covariance**
- Universal subspace = top-k eigenvectors of S = E_{t~τ}[f*_t ⊗ f*_t]
- Reference: U_S* = population covariance across task distribution
- Secondary subspace (outside U_S*) = much worse performance (empirically confirmed)

**The discriminating measurement (not done by anyone):**
Take a pretrained base model + ≥5 LoRAs on different tasks. Compute:
- U_W₀ = top-k left singular vectors of W₀
- U_S* = top-k eigenvectors of (1/K) Σ_i ΔW_i ΔW_iᵀ
- Measure principal angles θ_j between subspaces U_W₀ and U_S*

If θ_j ≈ 0 for all j: frames are empirically the same → intruder dims ≈ secondary subspace
If θ_j large: frames are genuinely different objects

CONJECTURE (INFERRED, confidence 0.65): U_W₀ ≈ U_S* for large pretrained models
Reason: both are shaped by the same pretraining objective on the same data distribution
What could break it: fine-tuning tasks drawn from a very different distribution than pretraining

---

## WHAT IS ESTABLISHED (EXTRACTED facts)

| Claim | Source | Status |
|---|---|---|
| Universal subspace is rank ≤ 16 per layer | arXiv:2512.05117 | EXTRACTED (empirical) |
| 1100+ LoRAs across 4 architectures have the same subspace | arXiv:2512.05117 | EXTRACTED |
| Secondary subspace performance is drastically worse | arXiv:2512.05117 | EXTRACTED |
| Denoising effect: universal subspace LoRA outperforms individual LoRAs | arXiv:2512.05117 | EXTRACTED |
| Intruder dims predict catastrophic forgetting | arXiv:2410.21228 | EXTRACTED |
| Suppressing intruder dims restores base model knowledge | arXiv:2410.21228 | EXTRACTED |
| OPLoRA: projecting ⊥ W₀ prevents forgetting (ρ_k = 0.003) | arXiv:2510.13003 | EXTRACTED |
| Universal subspace paper does NOT compare to W₀ singular subspace | arXiv:2512.05117 | EXTRACTED (absence) |
| Intruder dim paper does NOT compare to cross-LoRA covariance | arXiv:2410.21228 | EXTRACTED (absence) |

---

## CONJECTURE EDGES (INFERRED, marked for graph)

1. **Universal_Subspace_Secondary ↔ Intruder_Dims** (INFERRED, confidence 0.65)
   - Secondary subspace outside U_S* MAY be the same population as intruder dims outside U_W₀
   - Open empirical question: do they coincide?

2. **Universal_Subspace_S_star ↔ TRS_Ambient_Space** (INFERRED, confidence 0.70)
   - TRS subspaces may all lie within S* — TRS computes where in S* each task lives
   - Testable: are all above-MP singular vectors within S*?

3. **Task_Second_Moment_Operator ↔ Spiked_Covariance_Signal** (INFERRED, confidence 0.75)
   - S = E[f*_t ⊗ f*_t] is the population version of the signal matrix in the spiked covariance model
   - Under spiked covariance: individual ΔW = S^{1/2} signal + noise
   - Above-MP threshold selects entries where S eigenvalue > σ_noise * (MP threshold)

---

## WHAT MUST NOT BE CLAIMED (labeled CONJECTURE until measured)

- "NTK eigenspace = W₀ singular subspace" — category error (function space vs weight space)
- "NTK explains universal subspace" — cited as hand-wave in Discussion of 2512.05117, not theorem
- "Intruder dims = secondary subspace" — operationally distinct reference frames, not measured to coincide

---

## PAPERS TO READ FOR DISCRIMINATING EVIDENCE

Priority 1: **Eigenlorax (arXiv:2502.04700)** — same Kaushik group, earlier paper on recycling adapters
  May compare U_W₀ to U_S* or connect to forgetting literature

Priority 2: **Kaushik et al. 2021 (arXiv:2102.11343)** — earliest Kaushik paper on catastrophic forgetting
  "optimal relevance mapping" — may bridge universal subspace and intruder dims

Priority 3: **Mao et al. PNAS 2024** — "training process explores same low-dimensional manifold"
  Independent confirmation; check if W₀ alignment is mentioned
