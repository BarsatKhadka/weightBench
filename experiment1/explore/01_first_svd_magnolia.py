"""First SVD on a LoRA checkpoint, designed to run on magnolia.

Just run this and read the output. No file transfer needed.

Usage:
    cd $HOME/weightBench/weightBench/experiment1
    source $HOME/weightBench/.venv/bin/activate
    python explore/01_first_svd_magnolia.py
"""
from __future__ import annotations

import numpy as np
from safetensors.torch import load_file
from pathlib import Path

EXP = Path(__file__).resolve().parents[1]
ADAPTERS = EXP / "adapters" / "hellaswag_seed0"

# One layer, two checkpoints.
B_KEY = "base_model.model.model.layers.14.self_attn.q_proj.lora_B.weight"
A_KEY = "base_model.model.model.layers.14.self_attn.q_proj.lora_A.weight"


def svd_one(ckpt_path: Path) -> tuple[np.ndarray, np.ndarray]:
    """Return (singular values, dW) for one checkpoint, layer 14 q_proj."""
    sd = load_file(str(ckpt_path / "adapter_model.safetensors"))
    B = sd[B_KEY].numpy().astype("float32")
    A = sd[A_KEY].numpy().astype("float32")
    dW = B @ A
    _, s, _ = np.linalg.svd(dW, full_matrices=False)
    return s, dW


def main() -> None:
    print(f"adapter root: {ADAPTERS}")
    print(f"exists: {ADAPTERS.exists()}")
    print()

    # --- Cell 1: inventory ---
    print("=" * 60)
    print("CELL 1 — inventory")
    print("=" * 60)
    sd2000 = load_file(str(ADAPTERS / "checkpoint-2000" / "adapter_model.safetensors"))
    print(f"total tensors in checkpoint-2000: {len(sd2000)}")
    print("first 6 keys with shapes:")
    for k in list(sd2000.keys())[:6]:
        print(f"  {k}  shape={tuple(sd2000[k].shape)}")
    print()

    # --- Cell 2: SVD on layer 14 q_proj at step 2000 ---
    print("=" * 60)
    print("CELL 2 — SVD on layer 14 q_proj at step 2000")
    print("=" * 60)
    s, dW = svd_one(ADAPTERS / "checkpoint-2000")
    print(f"dW shape: {dW.shape}  (rank ≤ 16 because of LoRA)")
    print(f"\nfirst 20 singular values:")
    for i, v in enumerate(s[:20]):
        flag = "  <-- should be ~0" if i >= 16 else ""
        print(f"  s[{i:2d}] = {v:.6f}{flag}")
    print(f"\nratio s[0] / s[15]: {s[0] / s[15]:.2f}")
    print(f"Frobenius norm of dW: {np.sqrt((s ** 2).sum()):.4f}")
    print()

    # --- Cell 3: same layer at step 50 ---
    print("=" * 60)
    print("CELL 3 — SVD on the same layer at step 50 (early in training)")
    print("=" * 60)
    s_early, _ = svd_one(ADAPTERS / "checkpoint-50")
    print(f"first 16 singular values at step 50:")
    for i, v in enumerate(s_early[:16]):
        print(f"  s[{i:2d}] = {v:.6f}")
    print(f"\nFrobenius norm at step 50: {np.sqrt((s_early ** 2).sum()):.4f}")
    print()

    # --- Cell 4: comparison ---
    print("=" * 60)
    print("CELL 4 — how the spectrum grew from step 50 to step 2000")
    print("=" * 60)
    print(f"{'idx':>3s} | {'step 50':>12s} | {'step 2000':>12s} | {'ratio':>8s}")
    print("-" * 50)
    for i in range(16):
        ratio = s[i] / s_early[i] if s_early[i] > 1e-9 else float("inf")
        print(f"{i:3d} | {s_early[i]:12.6f} | {s[i]:12.6f} | {ratio:8.2f}x")
    print(f"\nFrobenius norm growth: {np.sqrt((s ** 2).sum()) / np.sqrt((s_early ** 2).sum()):.2f}x")
    print()
    print("Questions to answer by eye:")
    print("  1. Did all 16 singular values grow uniformly, or did the top ones grow more?")
    print("  2. Is there a 'gap' in the final spectrum (effective rank < 16)?")
    print("  3. What does that say about how this LoRA learned hellaswag?")


if __name__ == "__main__":
    main()
