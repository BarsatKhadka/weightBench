"""
Principal angles between U_W0 (pretrained singular subspace) and U_S* (cross-LoRA covariance).

Measures whether two reference frames in the fine-tuning literature are the same object:
  U_W0  = top-k left singular vectors of the pretrained weight matrix W0
  U_S*  = top-k eigenvectors of (1/K) sum_i ΔŴ_i ΔŴ_i^T  (cross-LoRA covariance)
  ΔŴ_i  = ΔW_i / ||ΔW_i||_F  (Frobenius-normalized so each adapter contributes equally)

No inference needed. Load weights only. ~30-45 min on CPU (one-time base model load + SVDs).
pip install torch transformers safetensors huggingface_hub scipy numpy
"""

import math
import json
import torch
import numpy as np
from scipy.linalg import subspace_angles
from pathlib import Path
from transformers import AutoModelForCausalLM

BASE_MODEL = "meta-llama/Meta-Llama-3-8B"

# 11 diverse tasks, all raw meta-llama/Meta-Llama-3-8B base (not Instruct, not quantized backbone).
# Ordered by expected task diversity, not size.
LORA_ADAPTERS = [
    # Task                      Model ID
    # ---                       --------
    "yspkm/Meta-Llama-3-8B-lora-math",                          # Math (general), r=32, all 7 proj
    "lovepon/Meta-Llama-3-8B-alpaca_cleaned-lora",              # Instruction (Alpaca), r=8, q+v
    "lovepon/Meta-Llama-3-8B-code_alpaca-lora",                 # Code (CodeAlpaca), r=8, q+v
    "felixml/Meta-Llama-3-8B-text-to-sql",                      # SQL, r=256, all 7 proj
    "pkbiswas/Llama-3-8B-Summarization-QLoRa",                  # Summarization (SciTLDR), r=16, all 7
    "FinGPT/fingpt-mt_llama3-8b_lora",                          # Finance/sentiment, r=8, q+v
    "NouRed/BioMed-Tuned-Llama-3-8b",                          # Biomedical, r=8, all 7
    "jiazhengli/Meta-Llama-3-8B-QLoRA-Assessment-Rationale-dpo",# Educational reasoning, r=8, all 7
    "beratcmn/Llama3-ChatQA-1.5-8B-lora",                      # Conversational QA, r=64, all 7
    "lovepon/Meta-Llama-3-8B-numinamath_cot-lora",              # Math CoT (NuminaMath), r=8, q+v
    "lovepon/Meta-Llama-3-8B-saferpaca-lora",                   # Safety-aligned instruct, r=8, q+v
]

# q_proj and v_proj are covered by ALL 11 adapters.
# k_proj, o_proj, gate/up/down_proj: covered by ~6 adapters (all-7-proj adapters only).
# Script handles partial coverage: skips a layer if <2 adapters define ΔW for it.
LAYER_NAMES = (
    [f"model.layers.{n}.self_attn.q_proj" for n in range(32)] +
    [f"model.layers.{n}.self_attn.k_proj" for n in range(32)] +
    [f"model.layers.{n}.self_attn.v_proj" for n in range(32)] +
    [f"model.layers.{n}.self_attn.o_proj" for n in range(32)]
)

# Primary analysis uses these 5 representative depths for q_proj and v_proj
PRIMARY_LAYERS = (
    [f"model.layers.{n}.self_attn.q_proj" for n in [0, 8, 16, 24, 31]] +
    [f"model.layers.{n}.self_attn.v_proj" for n in [0, 8, 16, 24, 31]]
)

K = 16  # rank of universal subspace to estimate


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------

def load_base_weights(base_model_id, layer_names, device="cpu"):
    print(f"Loading base model {base_model_id} (~14 GB, once only) ...")
    model = AutoModelForCausalLM.from_pretrained(
        base_model_id,
        torch_dtype=torch.float32,
        device_map=device,
        low_cpu_mem_usage=True,
    )
    state = model.state_dict()
    W0 = {}
    for ln in layer_names:
        key = ln + ".weight"
        if key in state:
            W0[ln] = state[key].cpu().float()
    del model
    print(f"  -> {len(W0)} weight matrices loaded")
    return W0


def load_lora_delta(adapter_id, layer_names, verbose=False):
    """
    Load ΔW = scaling * lora_B @ lora_A directly from the adapter checkpoint.
    Does NOT load the base model — reads only the small adapter file.
    Handles both standard LoRA (scaling = alpha/r) and RSLoRA (scaling = alpha/sqrt(r)).
    """
    from huggingface_hub import hf_hub_download
    import safetensors.torch as st

    cfg_path = hf_hub_download(adapter_id, "adapter_config.json")
    cfg = json.loads(Path(cfg_path).read_text())
    r = cfg.get("r", 8)
    alpha = float(cfg.get("lora_alpha", r))
    use_rslora = cfg.get("use_rslora", False)
    scaling = alpha / math.sqrt(r) if use_rslora else alpha / r

    try:
        ckpt_path = hf_hub_download(adapter_id, "adapter_model.safetensors")
        state = st.load_file(ckpt_path, device="cpu")
    except Exception:
        ckpt_path = hf_hub_download(adapter_id, "adapter_model.bin")
        state = torch.load(ckpt_path, map_location="cpu", weights_only=True)

    if verbose:
        sample_keys = [k for k in list(state.keys())[:6]]
        print(f"  [diagnostic] First 6 keys: {sample_keys}")

    deltas = {}
    for ln in layer_names:
        # PEFT key pattern: base_model.model.<ln>.lora_A.weight
        # For LlamaForCausalLM, ln starts with "model.layers..." so full key has "model.model.layers..."
        key_A = f"base_model.model.{ln}.lora_A.weight"
        key_B = f"base_model.model.{ln}.lora_B.weight"
        if key_A in state and key_B in state:
            A = state[key_A].float()  # (r, n)
            B = state[key_B].float()  # (m, r)
            dW = scaling * (B @ A)    # (m, n)
            if dW.abs().max() > 1e-9:
                deltas[ln] = dW

    return deltas, {"r": r, "alpha": alpha, "use_rslora": use_rslora, "scaling": scaling}


def key_format_diagnostic(adapter_id):
    """Print first 6 adapter state dict keys so you can verify the key pattern."""
    from huggingface_hub import hf_hub_download
    import safetensors.torch as st
    try:
        ckpt_path = hf_hub_download(adapter_id, "adapter_model.safetensors")
        state = st.load_file(ckpt_path, device="cpu")
    except Exception:
        ckpt_path = hf_hub_download(adapter_id, "adapter_model.bin")
        state = torch.load(ckpt_path, map_location="cpu", weights_only=True)
    print(f"  {adapter_id}: {list(state.keys())[:4]}")


# ---------------------------------------------------------------------------
# Measurement
# ---------------------------------------------------------------------------

def measure_alignment(W0_weights, all_deltas, layer_names, k=K):
    """
    For each layer, compute:
      - Principal angles between U_W0_top_k and U_S* (top-k eigenvecs of cross-LoRA covariance)
      - ΔW is Frobenius-normalized before pooling to prevent large adapters dominating
      - Spectrum alignment: what fraction of U_S* lies in W0's top-m subspace for m in {k, 4k, 16k, 128k}
      - Per-adapter variance explained by U_S*
    """
    results = {}
    for layer in layer_names:
        dWs_raw = [d[layer].numpy().astype(np.float64)
                   for d in all_deltas if layer in d]
        if len(dWs_raw) < 2:
            continue

        W0 = W0_weights[layer].numpy().astype(np.float64)  # (m, n)
        m = W0.shape[0]

        # U_W0: top-k left singular vectors of W0
        U_W0, S_W0, _ = np.linalg.svd(W0, full_matrices=False)
        U_W0_top_k = U_W0[:, :k]

        # Frobenius-normalize each ΔW_i before pooling
        # Without this, high-rank adapters (felixml r=256) dominate the covariance
        dWs_normed = []
        frob_norms = []
        for dW in dWs_raw:
            fn = np.linalg.norm(dW, "fro")
            frob_norms.append(float(fn))
            dWs_normed.append(dW / max(fn, 1e-10))

        # S_hat = (1/K) sum ΔŴ_i ΔŴ_i^T  (normalized)
        S_hat = np.zeros((m, m))
        for dW_n in dWs_normed:
            S_hat += dW_n @ dW_n.T
        S_hat /= len(dWs_normed)

        # U_S*: top-k eigenvectors of S_hat
        eigenvals, eigenvecs = np.linalg.eigh(S_hat)
        idx = np.argsort(-eigenvals)
        U_Sstar = eigenvecs[:, idx[:k]]

        # Principal angles between U_W0_top_k and U_Sstar
        angles = subspace_angles(U_W0_top_k, U_Sstar)

        # Where in W0 spectrum does U_S* sit?
        spectrum_alignment = {}
        for m_test in [k, 4 * k, 16 * k, min(128 * k, m)]:
            U_top = U_W0[:, :m_test]
            captured = float(
                np.trace(U_Sstar.T @ (U_top @ U_top.T) @ U_Sstar) / k
            )
            spectrum_alignment[f"top_{m_test}"] = captured

        # Variance of each ΔW_i (un-normalized) explained by U_S*
        # This answers: "what fraction of each task's update lives in the shared subspace?"
        P = U_Sstar @ U_Sstar.T
        var_explained = []
        for dW in dWs_raw:
            proj = np.linalg.norm(P @ dW, "fro") ** 2
            total = max(np.linalg.norm(dW, "fro") ** 2, 1e-10)
            var_explained.append(float(proj / total))

        # Per-adapter intruder dimension analysis (Shuttleworth 2410.21228).
        # Intruder dims = singular vectors of ΔW with max cosine similarity < 0.3 to
        # top-4k W0 singular vectors. Measures Frobenius energy in intruder vs TRS dims,
        # adjudicating the rank-forgetting tension: is the mediator intruder count or magnitude?
        U_W0_ref = U_W0[:, :min(4 * k, m)]  # generous reference (4k W0 directions)
        intruder_analysis = []
        for dW in dWs_raw:
            if np.linalg.norm(dW, "fro") < 1e-10:
                intruder_analysis.append({"intruder_count": 0, "intruder_frob_energy": 0.0,
                                          "trs_frob_energy": 0.0})
                continue
            U_dW, S_dW, _ = np.linalg.svd(dW, full_matrices=False)
            max_cos = np.abs(U_W0_ref.T @ U_dW).max(axis=0)  # (r,): max W0-alignment per ΔW dim
            intruder = max_cos < 0.3
            intruder_analysis.append({
                "intruder_count": int(intruder.sum()),
                "intruder_frob_energy": float(np.sum(S_dW[intruder] ** 2)),
                "trs_frob_energy": float(np.sum(S_dW[~intruder] ** 2)),
            })

        results[layer] = {
            "n_adapters": len(dWs_raw),
            "principal_angles_deg": np.degrees(angles).tolist(),
            "mean_angle_deg": float(np.degrees(angles).mean()),
            "max_angle_deg": float(np.degrees(angles).max()),
            "alignment_score": float(np.cos(angles).mean()),  # 1=same, 0=orthogonal
            "US_in_W0_spectrum": spectrum_alignment,
            "variance_explained_by_US": var_explained,
            "mean_var_explained": float(np.mean(var_explained)),
            "adapter_frob_norms": frob_norms,
            "W0_singular_values_top_k": S_W0[:k].tolist(),
            "S_hat_eigenvalues_top_k": eigenvals[idx[:k]].tolist(),
            "intruder_analysis": intruder_analysis,
        }

    return results


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def interpret(results, adapter_ids=None):
    print("\n" + "=" * 64)
    print("PRINCIPAL ANGLE RESULTS: U_W0 vs U_S*")
    print("  0° = same subspace  |  90° = orthogonal subspaces")
    print("=" * 64)

    all_mean_angles = []
    for layer in sorted(results.keys()):
        r = results[layer]
        all_mean_angles.append(r["mean_angle_deg"])
        print(f"\n{layer}  ({r['n_adapters']} adapters)")
        print(f"  Mean principal angle  : {r['mean_angle_deg']:6.1f}°")
        print(f"  Max  principal angle  : {r['max_angle_deg']:6.1f}°")
        print(f"  Alignment score       : {r['alignment_score']:.4f}")
        sp = r["US_in_W0_spectrum"]
        sorted_sp = sorted(sp.items(), key=lambda x: int(x[0].split("_")[1]))
        for key, val in sorted_sp:
            print(f"  U_S* in W0 {key:>10}: {val:.4f}")
        print(f"  Mean ΔW var in U_S*   : {r['mean_var_explained']:.1%}")

    if all_mean_angles:
        overall = np.mean(all_mean_angles)
        print(f"\n{'='*64}")
        print(f"OVERALL mean principal angle across {len(all_mean_angles)} layers: {overall:.1f}°")
        if overall < 30:
            print("RESULT: ALIGNED — U_W0 ≈ U_S*")
            print("  Interpretation: The two reference frames are empirically the same object.")
            print("  Intruder dims (Shuttleworth) ≈ secondary subspace (Kaushik).")
        elif overall > 60:
            print("RESULT: ORTHOGONAL — U_W0 ⊥ U_S*")
            print("  Interpretation: Two genuinely distinct reference frames.")
            print("  The community has been conflating different geometric objects.")
        else:
            print(f"RESULT: PARTIAL ALIGNMENT ({overall:.1f}°)")
            print("  Interpretation: Intermediate. Report full angle distribution.")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    run_diagnostic = "--diagnostic" in sys.argv
    full_scan = "--full" in sys.argv  # use all 32 layers instead of PRIMARY_LAYERS
    layer_set = LAYER_NAMES if full_scan else PRIMARY_LAYERS

    if run_diagnostic:
        print("=== KEY FORMAT DIAGNOSTIC ===")
        print("Checking adapter state dict key patterns (first 4 keys each):")
        for aid in LORA_ADAPTERS[:3]:  # check first 3 only
            key_format_diagnostic(aid)
        print("\nExpected pattern: base_model.model.model.layers.N.self_attn.q_proj.lora_A.weight")
        print("If you see a different pattern, update key_A/key_B in load_lora_delta().")
        sys.exit(0)

    print("Step 1: Load base weights (loads ~14 GB once)")
    W0 = load_base_weights(BASE_MODEL, layer_set)

    print("\nStep 2: Load LoRA deltas (reads adapter files only, ~50-300 MB each)")
    all_deltas = []
    adapter_meta = []
    for adapter_id in LORA_ADAPTERS:
        print(f"  {adapter_id}")
        try:
            deltas, meta = load_lora_delta(adapter_id, layer_set)
            n = len(deltas)
            print(f"    r={meta['r']}, alpha={meta['alpha']}, rslora={meta['use_rslora']}, "
                  f"scaling={meta['scaling']:.4f}, layers_with_dW={n}")
            if n == 0:
                print("    WARNING: no layers found — check key format with --diagnostic")
            all_deltas.append(deltas)
            adapter_meta.append({**meta, "adapter_id": adapter_id, "layers_found": n})
        except Exception as e:
            print(f"    ERROR loading {adapter_id}: {e}. Skipping.")

    K_actual = len(all_deltas)
    print(f"\n  K = {K_actual} adapters loaded successfully")

    print("\nStep 3: Measure alignment")
    results = measure_alignment(W0, all_deltas, layer_set, k=K)

    interpret(results)

    out_results = Path("experiment_results_reference_frame.json")
    out_meta = Path("experiment_adapter_meta.json")
    out_results.write_text(json.dumps(results, indent=2))
    out_meta.write_text(json.dumps(adapter_meta, indent=2))
    print(f"\nResults saved to {out_results}")
    print(f"Adapter metadata saved to {out_meta}")
