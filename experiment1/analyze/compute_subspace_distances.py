"""Compute pairwise subspace distances (principal angles, Grassmannian distance)
between all pairs of (seed_a, seed_b) at the endpoint, per layer.

Why this is the C1 measurement:
  Two LoRAs' subspaces "agree" if the left singular vectors of ΔW span similar
  directions. Principal angles measure this precisely:
      θ_i = arccos(σ_i(U_aᵀ · U_b))   for i = 1..16
  If θ_i is small (cosine near 1), direction i overlaps. If θ_i ≈ 90°, totally
  orthogonal.

  Grassmannian distance: d_G = sqrt(sum(θ_i²))    (geodesic)
                          d_C = sqrt(sum(sin² θ_i))   (chordal)

For 5 seeds, there are 10 pairs (5 choose 2). For 196 layers, that's 1,960
distance numbers — tiny CSV, easy to push.

Output: experiment1/analyze/subspace_distances.csv
        columns: layer_idx, sublayer, module, seed_a, seed_b,
                 d_grassmannian, d_chordal, mean_principal_angle_deg,
                 theta_0_deg, ..., theta_15_deg

Run on magnolia:
    cd $HOME/weightBench/weightBench/experiment1
    source $HOME/weightBench/.venv/bin/activate
    python analyze/compute_subspace_distances.py
"""
from __future__ import annotations

import argparse
import re
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd
from safetensors.torch import load_file

EXP = Path(__file__).resolve().parents[1]


def parse_layer_key(key: str) -> tuple[int, str, str, str] | None:
    m = re.match(
        r"base_model\.model\.model\.layers\.(\d+)\.(self_attn|mlp)\.(\w+_proj)\.lora_([AB])\.weight",
        key,
    )
    if not m:
        return None
    return int(m.group(1)), m.group(2), m.group(3), m.group(4)


def left_singular_vectors(ckpt_path: Path) -> dict[tuple[int, str, str], np.ndarray]:
    """Return {(layer_idx, sublayer, module): U_dW (d_out, 16)} for one checkpoint.

    Uses the QR+small-SVD trick to avoid forming the full (d_out, d_in) dW:
        B = Q_B @ R_B            (QR on (d_out, 16) — cheap)
        M = R_B @ A              ((16, d_in) — small)
        M = U_small @ σ @ Vᵀ     (SVD on (16, d_in) — fast)
        U_full = Q_B @ U_small   (rank-16 left singular vectors of dW)

    ~50-100× faster than np.linalg.svd(B @ A) for these shapes.
    """
    sd = load_file(str(ckpt_path / "adapter_model.safetensors"))
    pairs: dict[tuple[int, str, str], dict] = {}
    for key, t in sd.items():
        parsed = parse_layer_key(key)
        if parsed is None:
            continue
        layer_idx, sublayer, module, ab = parsed
        pairs.setdefault((layer_idx, sublayer, module), {})[ab] = t.numpy().astype("float32")

    Us: dict[tuple[int, str, str], np.ndarray] = {}
    for k, ab in pairs.items():
        if "A" not in ab or "B" not in ab:
            continue
        B, A = ab["B"], ab["A"]
        Q_B, R_B = np.linalg.qr(B)            # (d_out, 16), (16, 16)
        M = R_B @ A                            # (16, d_in)
        U_small, _, _ = np.linalg.svd(M, full_matrices=False)  # U_small: (16, 16)
        U_full = Q_B @ U_small                 # (d_out, 16) — same as SVD(B@A) up to sign
        Us[k] = U_full.astype("float32")
    return Us


def principal_angles(U_a: np.ndarray, U_b: np.ndarray) -> np.ndarray:
    """Return the 16 principal angles in radians between two (d_out, 16) bases."""
    # ensure orthonormal columns (they are, from SVD, but cheap to confirm)
    # σ_i of U_aᵀ U_b are the cosines of principal angles
    M = U_a.T @ U_b
    s = np.linalg.svd(M, compute_uv=False)
    s = np.clip(s, -1.0, 1.0)  # numerical safety
    return np.arccos(s)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--task", default="hellaswag")
    p.add_argument("--seeds", default="0,1,2,3,4")
    p.add_argument("--checkpoint", default="final",
                   help="Which checkpoint to compare across seeds (default: final)")
    p.add_argument("--adapters-root", type=Path, default=EXP / "adapters")
    p.add_argument("--out", type=Path, default=EXP / "analyze" / "subspace_distances.csv")
    args = p.parse_args()

    seeds = [int(s) for s in args.seeds.split(",")]

    # Load left singular vectors for each seed's chosen checkpoint
    print(f"loading {args.checkpoint} for {len(seeds)} seeds", flush=True)
    import time
    per_seed: dict[int, dict[tuple[int, str, str], np.ndarray]] = {}
    for seed in seeds:
        ckpt_dir = args.adapters_root / f"{args.task}_seed{seed}" / args.checkpoint
        if not ckpt_dir.exists():
            print(f"  [skip] seed {seed}: {ckpt_dir} not found", flush=True)
            continue
        t0 = time.time()
        print(f"  [seed {seed}] loading + SVD on {ckpt_dir}", flush=True)
        per_seed[seed] = left_singular_vectors(ckpt_dir)
        print(f"  [seed {seed}] done in {time.time() - t0:.1f}s "
              f"({len(per_seed[seed])} layers)", flush=True)

    if len(per_seed) < 2:
        print("need at least 2 seeds to compute pairwise distances")
        return

    # Pairwise principal angles per layer
    layer_keys = set.intersection(*[set(d.keys()) for d in per_seed.values()])
    print(f"\n{len(layer_keys)} layers shared across all seeds")
    print(f"{len(list(combinations(per_seed.keys(), 2)))} pairs to compute")

    rows: list[dict] = []
    for layer_key in sorted(layer_keys):
        layer_idx, sublayer, module = layer_key
        for seed_a, seed_b in combinations(sorted(per_seed.keys()), 2):
            angles = principal_angles(per_seed[seed_a][layer_key],
                                      per_seed[seed_b][layer_key])
            angles_deg = np.degrees(angles)
            row = {
                "layer_idx": layer_idx,
                "sublayer": sublayer,
                "module": module,
                "seed_a": seed_a,
                "seed_b": seed_b,
                "d_grassmannian": float(np.sqrt((angles ** 2).sum())),
                "d_chordal": float(np.sqrt((np.sin(angles) ** 2).sum())),
                "mean_angle_deg": float(angles_deg.mean()),
                "max_angle_deg": float(angles_deg.max()),
                "min_angle_deg": float(angles_deg.min()),
            }
            for i, a in enumerate(angles_deg):
                row[f"theta_{i:02d}_deg"] = float(a)
            rows.append(row)

    df = pd.DataFrame(rows)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.out, index=False)
    print(f"\n[done] wrote {len(df)} rows to {args.out}")
    print(f"file size: {args.out.stat().st_size / 1024:.1f} KB")

    # Headline summary: mean Grassmannian distance per layer + module across all pairs
    print("\nmean Grassmannian distance by sublayer/module (across all seed pairs):")
    summary = df.groupby(["sublayer", "module"])["d_grassmannian"].agg(["mean", "std", "count"])
    print(summary.to_string())


if __name__ == "__main__":
    main()
