"""Compute per-checkpoint trajectory features per (seed, layer).

Extends compute_spectra (which has scalar spectra per checkpoint) with
subspace-trajectory signals that compute_subspace_distances only computed
at the endpoint:

  - d_G_to_endpoint(t):  Grassmannian distance from U(t) to U(T_final)
  - d_G_to_init(t):      Grassmannian distance from U(t) to U(T_init)
  - d_G_velocity(t):     d_G(U(t), U(t-1))  -- subspace motion per save
  - top1_ratio(t):       σ_0(t) / sum(σ(t)) -- concentration in top direction
  - growth_rate(σ_max):  delta in σ_0 per step

These signals jointly define what "phase" a layer is in at any moment.

Uses the QR + small-SVD trick for speed (~30 min CPU for 5 seeds x 41 ckpts
x 196 layers, vs ~hours without it).

Output: experiment1/analyze/trajectory_features.parquet
"""
from __future__ import annotations

import argparse
import re
import time
from pathlib import Path

import numpy as np
import pandas as pd
from safetensors.torch import load_file

EXP = Path(__file__).resolve().parents[1]


# ---------------------------------------------------------------------------
# Layer key parsing
# ---------------------------------------------------------------------------

def parse_layer_key(key: str) -> tuple[int, str, str, str] | None:
    m = re.match(
        r"base_model\.model\.model\.layers\.(\d+)\.(self_attn|mlp)\.(\w+_proj)\.lora_([AB])\.weight",
        key,
    )
    if not m:
        return None
    return int(m.group(1)), m.group(2), m.group(3), m.group(4)


# ---------------------------------------------------------------------------
# Per-checkpoint extraction
# ---------------------------------------------------------------------------

def extract_per_layer(ckpt_dir: Path) -> dict[tuple[int, str, str], dict]:
    """Return {(layer_idx, sublayer, module): {'U': (d_out,16), 's': (16,)}}."""
    sd = load_file(str(ckpt_dir / "adapter_model.safetensors"))
    pairs: dict[tuple[int, str, str], dict] = {}
    for key, t in sd.items():
        parsed = parse_layer_key(key)
        if parsed is None:
            continue
        layer_idx, sublayer, module, ab = parsed
        pairs.setdefault((layer_idx, sublayer, module), {})[ab] = t.numpy().astype("float32")

    out: dict[tuple[int, str, str], dict] = {}
    for k, ab in pairs.items():
        if "A" not in ab or "B" not in ab:
            continue
        B, A = ab["B"], ab["A"]
        Q_B, R_B = np.linalg.qr(B)
        M = R_B @ A
        U_small, s, _ = np.linalg.svd(M, full_matrices=False)
        U_full = Q_B @ U_small        # (d_out, 16)
        out[k] = {"U": U_full.astype("float32"), "s": s.astype("float32")}
    return out


# ---------------------------------------------------------------------------
# Grassmannian distance between two (d_out, 16) bases
# ---------------------------------------------------------------------------

def grassmannian_distance(U_a: np.ndarray, U_b: np.ndarray) -> float:
    """sqrt(sum(theta_i^2)) where theta_i are the 16 principal angles."""
    M = U_a.T @ U_b
    cosines = np.linalg.svd(M, compute_uv=False)
    cosines = np.clip(cosines, -1.0, 1.0)
    angles = np.arccos(cosines)
    return float(np.sqrt((angles ** 2).sum()))


# ---------------------------------------------------------------------------
# Checkpoint enumeration
# ---------------------------------------------------------------------------

def iter_checkpoints(seed_dir: Path) -> list[tuple[int, Path]]:
    out = []
    for d in seed_dir.iterdir():
        if not d.is_dir():
            continue
        if d.name.startswith("checkpoint-"):
            try:
                step = int(d.name.split("-")[1])
                out.append((step, d))
            except (ValueError, IndexError):
                continue
        elif d.name == "final":
            out.append((-1, d))  # placeholder; we will treat as max+1 after sort
    out.sort()
    if out and out[0][0] == -1:
        rest_max = max((s for s, _ in out if s >= 0), default=0)
        out[0] = (rest_max + 1, out[0][1])
        out.sort()
    return out


# ---------------------------------------------------------------------------
# Per-seed trajectory build
# ---------------------------------------------------------------------------

def build_trajectory_for_seed(seed: int, seed_dir: Path) -> list[dict]:
    """Returns rows: one per (seed, step, layer)."""
    ckpts = iter_checkpoints(seed_dir)
    if not ckpts:
        return []
    print(f"[seed {seed}] {len(ckpts)} checkpoints", flush=True)

    # Pre-load all checkpoints' U and s (memory: ~5 seeds * 41 ckpts * 196 layers
    # * 3584 * 16 * 4 bytes ~= 1.7 GB per seed worst case). Iterate per seed.
    per_step: dict[int, dict] = {}
    t0 = time.time()
    for step, ckpt_dir in ckpts:
        per_step[step] = extract_per_layer(ckpt_dir)
    print(f"[seed {seed}] loaded {len(per_step)} ckpts in {time.time()-t0:.1f}s",
          flush=True)

    steps_sorted = sorted(per_step.keys())
    init_step = steps_sorted[0]
    final_step = steps_sorted[-1]

    # Common layers (should be all 196)
    layer_keys = set(per_step[init_step].keys())
    for s in steps_sorted[1:]:
        layer_keys &= set(per_step[s].keys())

    rows = []
    t1 = time.time()
    for layer_key in sorted(layer_keys):
        layer_idx, sublayer, module = layer_key
        U_init = per_step[init_step][layer_key]["U"]
        U_final = per_step[final_step][layer_key]["U"]

        prev_U = None
        for step in steps_sorted:
            U = per_step[step][layer_key]["U"]
            s = per_step[step][layer_key]["s"]
            row = {
                "seed": seed,
                "step": step,
                "layer_idx": layer_idx,
                "sublayer": sublayer,
                "module": module,
                "frob_norm": float(np.sqrt((s ** 2).sum())),
                "sigma_max": float(s[0]),
                "sigma_min_active": float(s[15]),
                "top1_ratio": float(s[0] / s.sum()) if s.sum() > 0 else 0.0,
                "effective_rank": _effective_rank(s),
                "d_G_to_init": grassmannian_distance(U, U_init),
                "d_G_to_endpoint": grassmannian_distance(U, U_final),
                "d_G_velocity": grassmannian_distance(U, prev_U) if prev_U is not None else float("nan"),
            }
            rows.append(row)
            prev_U = U

    print(f"[seed {seed}] trajectory rows {len(rows)} in {time.time()-t1:.1f}s",
          flush=True)
    return rows


def _effective_rank(s: np.ndarray) -> float:
    sq = s ** 2
    total = sq.sum()
    if total < 1e-12:
        return 0.0
    p = sq / total
    p = p[p > 0]
    return float(np.exp(-(p * np.log(p)).sum()))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--task", default="hellaswag")
    p.add_argument("--seeds", default="0,1,2,3,4")
    p.add_argument("--adapters-root", type=Path, default=EXP / "adapters")
    p.add_argument("--out", type=Path,
                   default=EXP / "analyze" / "trajectory_features.parquet")
    args = p.parse_args()

    seeds = [int(s) for s in args.seeds.split(",")]
    all_rows: list[dict] = []
    t0 = time.time()
    for seed in seeds:
        seed_dir = args.adapters_root / f"{args.task}_seed{seed}"
        if not seed_dir.exists():
            print(f"[skip] seed {seed}: {seed_dir} not found", flush=True)
            continue
        rows = build_trajectory_for_seed(seed, seed_dir)
        all_rows.extend(rows)

    if not all_rows:
        print("no rows produced; check paths")
        return

    df = pd.DataFrame(all_rows)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(args.out, index=False)
    print(f"\n[done] wrote {len(df)} rows to {args.out}")
    print(f"total wall time: {time.time()-t0:.1f}s")
    print(f"per-seed counts:\n{df.groupby('seed').size()}")


if __name__ == "__main__":
    main()
