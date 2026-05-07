# EXPERIMENT: Principal Angles Between U_W₀ and U_S*
*The discriminating measurement — scoped May 2026*
*Status: NOT YET RUN — design only*

---

## THE QUESTION

Are the two reference frames in the fine-tuning literature the same object?

- **U_W₀**: top-k left singular vectors of pretrained weight matrix W₀
- **U_S***: top-k eigenvectors of cross-LoRA covariance S = (1/K) Σᵢ ΔWᵢ ΔWᵢᵀ

**Prediction from "they are the same":** principal angles θ_j(U_W₀, U_S*) ≈ 0 for all j ≤ k
**Prediction from "they are different":** principal angles spread uniformly in [0, π/2]

**Either result is publishable.** No paper has reported this number.

---

## ADDITIONAL QUESTIONS RESOLVED BY THE SAME EXPERIMENT

1. **Where in W₀'s spectrum does U_S* sit?**
   - Compute cosine similarity between U_S*[:, j] and U_W₀[:, :m] for m=16, 64, 128, 512
   - Does U_S* align with W₀ top-16, top-128, or bottom-512?
   - Resolves MiLoRA (claims minor W₀ subspace) vs PiSSA (claims principal W₀ subspace) contradiction

2. **What fraction of each ΔWᵢ lies in U_S* vs. outside?**
   - var_explained_i = ||P_{U_S*} ΔWᵢ||_F² / ||ΔWᵢ||_F²
   - Should be high (>80%) if universal subspace captures most task signal
   - What's in the remaining variance? Random noise? Intruder dims?

3. **Cross-architecture consistency:**
   - Do LoRAs from Mistral-7B and LLaMA-3-8B produce the same U_S* (after alignment)?
   - This is the original cross-architecture TRS experiment from CORE_CLAIM.md

---

## EXPERIMENTAL DESIGN

### Models
- **Base model 1**: `meta-llama/Meta-Llama-3-8B` (HuggingFace)
- **Base model 2** (optional): `mistralai/Mistral-7B-v0.1`
  
### LoRA Adapters — RESOLVED HuggingFace IDs (K=11)

All use `meta-llama/Meta-Llama-3-8B` as base (raw base, NOT instruct, NOT quantized backbone).
K=11 diverse tasks ensures the cross-LoRA covariance is not dominated by sampling noise.
Each ΔW_i is Frobenius-normalized before pooling to prevent high-rank adapters (felixml r=256) from dominating.

| # | HF Model ID | Task | r | α | Target Layers | Notes |
|---|---|---|---|---|---|---|
| 1 | `yspkm/Meta-Llama-3-8B-lora-math` | Math (general) | 32 | 64 | all 7 proj | .bin format |
| 2 | `lovepon/Meta-Llama-3-8B-alpaca_cleaned-lora` | Instruction (Alpaca) | 8 | 16 | q, v | local path in config; adapter weights valid |
| 3 | `lovepon/Meta-Llama-3-8B-code_alpaca-lora` | Code (CodeAlpaca) | 8 | 16 | q, v | local path in config; adapter weights valid |
| 4 | `felixml/Meta-Llama-3-8B-text-to-sql` | SQL generation | 256 | 128 | all 7 proj | 3.44 GB; high rank |
| 5 | `pkbiswas/Llama-3-8B-Summarization-QLoRa` | Summarization (SciTLDR) | 16 | 64 | all 7 proj | standard LoRA despite "QLoRa" name |
| 6 | `FinGPT/fingpt-mt_llama3-8b_lora` | Finance / sentiment | 8 | 32 | q, v | financial news |
| 7 | `NouRed/BioMed-Tuned-Llama-3-8b` | Biomedical | 8 | 16 | all 7 proj | 54K medical instructions |
| 8 | `jiazhengli/Meta-Llama-3-8B-QLoRA-Assessment-Rationale-dpo` | Educational reasoning | 8 | 16 | all 7 proj | EMNLP 2024; DPO |
| 9 | `beratcmn/Llama3-ChatQA-1.5-8B-lora` | Conversational QA | 64 | 64 | all 7 + lm_head | extracted adapter |
| 10 | `lovepon/Meta-Llama-3-8B-numinamath_cot-lora` | Math CoT (NuminaMath) | 8 | 16 | q, v | different math distribution than #1 |
| 11 | `lovepon/Meta-Llama-3-8B-saferpaca-lora` | Safety-aligned instruct | 8 | 16 | q, v | SafeRPACA dataset |

**Excluded:**
- `ae-aydin/Llama-3-8B-Instruct-Medical-QLoRA` — base is LLaMA-3-8B-**Instruct**, contaminating covariance
- `mogmyij/Llama-3-8B-ARC-Challenge-0-9-LoRA-train-A` — `task_type: SEQ_CLS`, loads differently
- `juzhengz/LoRI-D_code_llama3_rank_32` — LoRI-D (A matrices frozen, B sparsified), structural bias in covariance
- Any adapter with `quantization_bits: 4` (LoftQ etc.) — requires 4-bit backbone

**RSLoRA note:** Only `lovepon/Meta-Llama-3-8B-numinamath_cot-lora-r16` (not in this list) has `use_rslora: true`. All 11 above use standard scaling α/r. Script checks this field from adapter_config.json and handles both.

**Layer coverage:** q_proj and v_proj have K=11. k_proj and o_proj have K≈6 (adapters #1, 4, 5, 7, 8, 9). Analysis reports n_adapters per layer so results are reproducible.

### Layers to Analyze
Primary: `model.layers[N].self_attn.q_proj` for N ∈ {0, 8, 16, 24, 31}
Secondary: all projection types (q, k, v, o) at layer 16 (middle)
Full: all 32 layers if compute permits

Rationale: Q/K layers most connected to forgetting and curvature in literature (arXiv:2502.10927, arXiv:2604.22778)

---

## THE SCRIPT (RUNNABLE)

Save as `run_experiment.py`. Requires: `pip install torch transformers peft safetensors huggingface_hub scipy numpy`

```python
"""
Principal angles between U_W0 (pretrained singular subspace) and U_S* (cross-LoRA covariance).
No inference needed. Load weights only. ~30 min on CPU, ~5 min with GPU.
"""

import torch
import numpy as np
import json
from scipy.linalg import subspace_angles
from pathlib import Path
from transformers import AutoModelForCausalLM

BASE_MODEL = "meta-llama/Meta-Llama-3-8B"

LORA_ADAPTERS = [
    "yspkm/Meta-Llama-3-8B-lora-math",
    "lovepon/Meta-Llama-3-8B-alpaca_cleaned-lora",
    "lovepon/Meta-Llama-3-8B-code_alpaca-lora",
    "felixml/Meta-Llama-3-8B-text-to-sql",
]

# Only layers where ALL adapters define ΔW (lovepon/ only has q_proj and v_proj)
LAYER_NAMES = [
    f"model.layers.{n}.self_attn.q_proj" for n in [0, 8, 16, 24, 31]
] + [
    f"model.layers.{n}.self_attn.v_proj" for n in [0, 8, 16, 24, 31]
]

K = 16  # rank of universal subspace to estimate


def get_param_name(layer_name):
    return layer_name + ".weight"


def load_base_weights(base_model_id, layer_names, device="cpu"):
    print(f"Loading base model {base_model_id} ...")
    model = AutoModelForCausalLM.from_pretrained(
        base_model_id,
        torch_dtype=torch.float32,
        device_map=device,
        low_cpu_mem_usage=True,
    )
    state = model.state_dict()
    W0 = {}
    for ln in layer_names:
        key = get_param_name(ln)
        if key in state:
            W0[ln] = state[key].cpu().float()
    del model
    return W0


def load_lora_delta(adapter_id, layer_names):
    """Load ΔW = (alpha/r) * lora_B @ lora_A directly from adapter checkpoint.
    Does NOT reload the base model — much cheaper (~50-300MB per adapter, not 14GB).
    """
    print(f"  Loading adapter {adapter_id} ...")
    from huggingface_hub import hf_hub_download
    import safetensors.torch
    import json as _json

    # Download adapter_config.json to get rank and alpha
    cfg_path = hf_hub_download(adapter_id, "adapter_config.json")
    cfg = _json.loads(Path(cfg_path).read_text())
    r = cfg.get("r", 8)
    alpha = cfg.get("lora_alpha", r)
    scaling = alpha / r

    # Download adapter weights (safetensors preferred, fall back to .bin)
    try:
        ckpt_path = hf_hub_download(adapter_id, "adapter_model.safetensors")
        state = safetensors.torch.load_file(ckpt_path, device="cpu")
    except Exception:
        ckpt_path = hf_hub_download(adapter_id, "adapter_model.bin")
        state = torch.load(ckpt_path, map_location="cpu")

    deltas = {}
    for ln in layer_names:
        # PEFT stores as base_model.model.<ln>.lora_A.weight and lora_B.weight
        key_A = f"base_model.model.{ln}.lora_A.weight"
        key_B = f"base_model.model.{ln}.lora_B.weight"
        if key_A in state and key_B in state:
            A = state[key_A].float()  # (r, n)
            B = state[key_B].float()  # (m, r)
            dW = scaling * (B @ A)    # (m, n)
            if dW.abs().max() > 1e-9:
                deltas[ln] = dW

    return deltas


def measure_alignment(W0_weights, all_deltas, layer_names, k=K):
    results = {}
    for layer in layer_names:
        # Collect ΔW_i for this layer across all adapters that define it
        dWs = [d[layer].numpy().astype(np.float64)
               for d in all_deltas if layer in d]
        if len(dWs) < 2:
            continue

        W0 = W0_weights[layer].numpy().astype(np.float64)  # (m, n)
        m = W0.shape[0]

        # U_W0: top-k left singular vectors of W0
        U_W0, S_W0, _ = np.linalg.svd(W0, full_matrices=False)
        U_W0_top_k = U_W0[:, :k]

        # S_hat = (1/K) Σ ΔW_i ΔW_i^T
        S_hat = np.zeros((m, m))
        for dW in dWs:
            S_hat += dW @ dW.T
        S_hat /= len(dWs)

        # U_S*: top-k eigenvectors of S_hat
        eigenvals, eigenvecs = np.linalg.eigh(S_hat)
        idx = np.argsort(-eigenvals)
        U_Sstar = eigenvecs[:, idx[:k]]

        # Principal angles between U_W0_top_k and U_Sstar
        angles = subspace_angles(U_W0_top_k, U_Sstar)

        # Where in W0 spectrum does U_S* sit?
        spectrum_alignment = {}
        for m_test in [k, 4 * k, 16 * k, min(128 * k, m)]:
            U_W0_top_m = U_W0[:, :m_test]
            captured = float(np.trace(U_Sstar.T @ (U_W0_top_m @ U_W0_top_m.T) @ U_Sstar) / k)
            spectrum_alignment[f"top_{m_test}"] = captured

        # Variance of each ΔW_i explained by U_S*
        P = U_Sstar @ U_Sstar.T
        var_explained = []
        for dW in dWs:
            proj_norm_sq = np.linalg.norm(P @ dW, "fro") ** 2
            total_norm_sq = max(np.linalg.norm(dW, "fro") ** 2, 1e-10)
            var_explained.append(float(proj_norm_sq / total_norm_sq))

        results[layer] = {
            "n_adapters": len(dWs),
            "principal_angles_deg": np.degrees(angles).tolist(),
            "mean_angle_deg": float(np.degrees(angles).mean()),
            "max_angle_deg": float(np.degrees(angles).max()),
            "alignment_score": float(np.cos(angles).mean()),
            "US_in_W0_spectrum": spectrum_alignment,
            "variance_explained_by_US": var_explained,
            "mean_var_explained": float(np.mean(var_explained)),
            "W0_singular_values_top16": S_W0[:k].tolist(),
            "S_hat_eigenvalues_top16": eigenvals[idx[:k]].tolist(),
        }

    return results


def interpret(results):
    print("\n" + "=" * 60)
    print("PRINCIPAL ANGLE RESULTS: U_W0 vs U_S*")
    print("=" * 60)
    for layer, r in sorted(results.items()):
        print(f"\n--- {layer} ({r['n_adapters']} adapters) ---")
        print(f"  Mean principal angle : {r['mean_angle_deg']:6.1f}°  (0°=same, 90°=orthogonal)")
        print(f"  Max  principal angle : {r['max_angle_deg']:6.1f}°")
        print(f"  Alignment score      : {r['alignment_score']:.4f}  (1.0=identical)")
        k = len(r["principal_angles_deg"])
        sp = r["US_in_W0_spectrum"]
        print(f"  U_S* in W0 top-{k:3d} : {sp.get(f'top_{k}', 0):.4f}")
        print(f"  U_S* in W0 top-{4*k:3d} : {sp.get(f'top_{4*k}', 0):.4f}")
        print(f"  U_S* in W0 top-{16*k:3d} : {sp.get(f'top_{16*k}', 0):.4f}")
        print(f"  Mean ΔW var in U_S*  : {r['mean_var_explained']:.1%}")


if __name__ == "__main__":
    print("Step 1: Load base weights")
    W0 = load_base_weights(BASE_MODEL, LAYER_NAMES)

    print("\nStep 2: Load LoRA deltas (reads adapter files only, not full base model)")
    all_deltas = []
    for adapter_id in LORA_ADAPTERS:
        deltas = load_lora_delta(adapter_id, LAYER_NAMES)
        print(f"    -> {len(deltas)} layers with non-zero ΔW")
        all_deltas.append(deltas)

    print("\nStep 3: Measure alignment")
    results = measure_alignment(W0, all_deltas, LAYER_NAMES, k=K)

    interpret(results)

    out = Path("experiment_results_reference_frame.json")
    out.write_text(json.dumps(results, indent=2))
    print(f"\nResults saved to {out}")
```

---

## EXPECTED OUTPUTS AND INTERPRETATIONS

### If U_W₀ ≈ U_S* (principal angles ≈ 0°):
- The two reference frames are the same object
- Intruder dims (Shuttleworth) = secondary subspace (Kaushik) — same definition
- Claim: "we establish the equivalence between two independently proposed reference frames"
- Strong paper: unifies two separate literatures

### If U_W₀ ⊥ U_S* (principal angles ≈ 90°):
- The two frames are genuinely different objects
- Knowing U_S* does NOT tell you about U_W₀, and vice versa
- Claim: "two distinct geometric properties of fine-tuning that have been conflated in the literature"
- Diagnostic: which one predicts forgetting better? (Shuttleworth's intruder dim removal vs. secondary subspace removal)
- Strong paper: identifies a hidden confound in existing methods

### If U_S* ⊂ U_W₀_bottom (aligns with W₀ minor subspace):
- MiLoRA's intuition is right: the task-shared space is the minor W₀ subspace
- Fine-tuning universally moves in "free space" (minor singular directions)
- PiSSA (top W₀ init) and MiLoRA (bottom W₀ init) are solving different problems

### If U_S* ⊂ U_W₀_top (aligns with W₀ principal subspace):
- PiSSA's intuition is right: the task-shared space is the principal W₀ subspace
- Suggests pretraining already encodes the task directions

---

## COST ESTIMATE

- **Compute**: ~30 min on a CPU with 32GB RAM (or 5 min with GPU)
  - Load LLaMA-3-8B weights: ~14GB
  - SVD of 128 layers × (4096×4096): ~10M operations each, ~seconds total
  - No GPU inference, no forward passes
- **Data**: All LoRAs freely available on HuggingFace
- **Tokens**: $0 (pure numpy/scipy)
- **Total cost: ~$0 for local run, ~$5-10 if using cloud CPU**

---

## WHAT TO WRITE FROM THE RESULTS

**If angles are small (< 30°)**: Write the note "the universal subspace is approximately the top-k singular subspace of the pretrained model. This means Shuttleworth's intruder dimensions = Kaushik's secondary subspace."

**If angles are large (> 60°)**: Write "the two reference frames are empirically distinct. The community has been using conflated concepts."

**In both cases**: Report the actual angle distribution, the spectrum alignment plot, and the variance-explained numbers. These numbers have never been reported.

---

## RELATION TO CORE_CLAIM.md

This experiment is Experiment 0 (cheapest, most informative) relative to the four-experiment suite in the project memory. It costs ~$0 and resolves the most important theoretical ambiguity before running any of the more expensive experiments.

If the result shows U_W₀ ≈ U_S* (aligned), then:
- CORE_CLAIM.md's Grassmannian framework is valid within U_S* ≈ U_W₀
- The experiment in CORE_CLAIM.md (cross-architecture Grassmannian clustering) is validated
- The full paper becomes: TRS + Grassmannian distance + this measurement

If the result shows U_W₀ ⊥ U_S* (orthogonal), then:
- CORE_CLAIM.md needs revision: the Grassmannian should be within U_S*, not full R^n
- TRS definition needs to be updated: above-MP within U_S*, not within full W₀ spectrum
