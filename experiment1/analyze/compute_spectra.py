"""Compute SVD spectrum of every LoRA layer at every checkpoint, all seeds.

For each (seed, step, layer) in the hellaswag pool, computes:
  - the 16 singular values of dW = B @ A
  - Frobenius norm of dW
  - effective rank (entropy-based)
  - top-1 ratio (s[0] / sum(s)) — how concentrated is the spectrum
  - rank16 ratio (s[0] / s[15]) — how heavy-tailed

Output: experiment1/analyze/spectra.parquet
        (~1 MB, easily pushed via git)

Run on magnolia:
    cd $HOME/weightBench/weightBench/experiment1
    source $HOME/weightBench/.venv/bin/activate
    python analyze/compute_spectra.py
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

import numpy as np
import pandas as pd
from safetensors.torch import load_file

EXP = Path(__file__).resolve().parents[1]


def parse_layer_key(key: str) -> tuple[int, str, str, str] | None:
    """Return (layer_idx, sublayer, module, ab) or None if key is not a LoRA weight.

    Example key: base_model.model.model.layers.14.self_attn.q_proj.lora_B.weight
                 → (14, 'self_attn', 'q_proj', 'B')
    """
    m = re.match(
        r"base_model\.model\.model\.layers\.(\d+)\.(self_attn|mlp)\.(\w+_proj)\.lora_([AB])\.weight",
        key,
    )
    if not m:
        return None
    return int(m.group(1)), m.group(2), m.group(3), m.group(4)


def collect_layer_pairs(state_dict: dict) -> dict[tuple[int, str, str], dict]:
    """Group safetensors keys into (A, B) pairs per layer position."""
    pairs: dict[tuple[int, str, str], dict] = {}
    for key, tensor in state_dict.items():
        parsed = parse_layer_key(key)
        if parsed is None:
            continue
        layer_idx, sublayer, module, ab = parsed
        slot = pairs.setdefault((layer_idx, sublayer, module), {})
        slot[ab] = tensor.numpy().astype("float32")
    return pairs


def effective_rank(s: np.ndarray) -> float:
    """Entropy-based effective rank: exp(-sum(p * log p)) where p = s^2 / sum(s^2)."""
    sq = s ** 2
    total = sq.sum()
    if total < 1e-12:
        return 0.0
    p = sq / total
    p = p[p > 0]
    return float(np.exp(-(p * np.log(p)).sum()))


def analyze_checkpoint(ckpt_dir: Path, seed: int, step: int) -> list[dict]:
    """Run SVD on every LoRA layer at one checkpoint. Returns list of row dicts."""
    safetensors_path = ckpt_dir / "adapter_model.safetensors"
    if not safetensors_path.exists():
        return []
    sd = load_file(str(safetensors_path))
    pairs = collect_layer_pairs(sd)

    rows = []
    for (layer_idx, sublayer, module), ab in sorted(pairs.items()):
        if "A" not in ab or "B" not in ab:
            continue
        A, B = ab["A"], ab["B"]
        dW = B @ A
        s = np.linalg.svd(dW, full_matrices=False, compute_uv=False)
        # only first 16 should be nonzero; trim
        s16 = s[:16]
        frob = float(np.sqrt((s16 ** 2).sum()))
        row = {
            "seed": seed,
            "step": step,
            "layer_idx": layer_idx,
            "sublayer": sublayer,
            "module": module,
            "frob_norm": frob,
            "effective_rank": effective_rank(s16),
            "top1_ratio": float(s16[0] / s16.sum()) if s16.sum() > 0 else 0.0,
            "rank16_ratio": float(s16[0] / s16[15]) if s16[15] > 0 else float("inf"),
        }
        for i in range(16):
            row[f"sv_{i:02d}"] = float(s16[i])
        rows.append(row)
    return rows


def iter_checkpoints(seed_dir: Path) -> list[tuple[int, Path]]:
    """Return [(step, ckpt_dir), ...] sorted by step. 'final' is treated as step max+1."""
    out = []
    for d in seed_dir.iterdir():
        if not d.is_dir():
            continue
        if d.name.startswith("checkpoint-"):
            step = int(d.name.split("-")[1])
            out.append((step, d))
        elif d.name == "final":
            out.append((-1, d))  # placeholder; we'll fix max+1 after sort
    out.sort()
    if out and out[0][0] == -1:
        rest_max = max((s for s, _ in out if s >= 0), default=0)
        out[0] = (rest_max + 1, out[0][1])
        out.sort()
    return out


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--task", default="hellaswag")
    p.add_argument("--seeds", default="0,1,2,3,4",
                   help="Comma-separated seed list (default: 0,1,2,3,4)")
    p.add_argument("--adapters-root", type=Path,
                   default=EXP / "adapters")
    p.add_argument("--out", type=Path, default=EXP / "analyze" / "spectra.parquet")
    args = p.parse_args()

    seeds = [int(s) for s in args.seeds.split(",")]
    all_rows: list[dict] = []
    for seed in seeds:
        seed_dir = args.adapters_root / f"{args.task}_seed{seed}"
        if not seed_dir.exists():
            print(f"[skip] seed {seed}: {seed_dir} not found")
            continue
        ckpts = iter_checkpoints(seed_dir)
        print(f"[seed {seed}] {len(ckpts)} checkpoints found")
        for step, ckpt_dir in ckpts:
            rows = analyze_checkpoint(ckpt_dir, seed, step)
            print(f"  step {step:>5d}: {len(rows)} layers analyzed")
            all_rows.extend(rows)

    if not all_rows:
        print("no rows produced; check paths")
        return

    df = pd.DataFrame(all_rows)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(args.out, index=False)
    print(f"\n[done] wrote {len(df)} rows to {args.out}")
    print(f"file size: {args.out.stat().st_size / 1024:.1f} KB")
    print(f"\ncolumns: {list(df.columns)}")
    print(f"\nshape: {df.shape}")
    print(f"per-seed counts:\n{df.groupby('seed').size()}")


if __name__ == "__main__":
    main()
