"""Headline analysis of subspace_distances.csv — the Level 0 C1 test.

Question: do same-task LoRAs land in the same 16-dim subspace per layer?

Reads experiment1/analyze/subspace_distances.csv and prints:
  1. The random baseline (what d_G between truly unrelated subspaces looks like)
  2. The overall mean d_G across all 1960 (layer, seed_pair) entries
  3. By sublayer (attention vs MLP)
  4. By module type (q,k,v,o,gate,up,down)
  5. By depth (early/mid/late layers)
  6. Per-layer histogram bins

If most entries are <<random_baseline, C1 holds at 7B on hellaswag.
If they're near baseline, the LoRAs found independent subspaces (different result).
"""
from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

EXP = Path(__file__).resolve().parents[1]


def random_baseline(n_dim: int, rank: int, n_trials: int = 200) -> float:
    """Expected d_G between two random orthonormal rank-r frames in R^n_dim."""
    samples = []
    rng = np.random.default_rng(0)
    for _ in range(n_trials):
        A = rng.standard_normal((n_dim, rank))
        B = rng.standard_normal((n_dim, rank))
        Q_A, _ = np.linalg.qr(A)
        Q_B, _ = np.linalg.qr(B)
        cosines = np.linalg.svd(Q_A.T @ Q_B, compute_uv=False)
        cosines = np.clip(cosines, -1, 1)
        angles = np.arccos(cosines)
        samples.append(np.sqrt((angles ** 2).sum()))
    return float(np.mean(samples))


def main() -> None:
    df = pd.read_csv(EXP / "analyze" / "subspace_distances.csv")
    print(f"loaded {len(df)} rows from subspace_distances.csv")
    print()

    # 1. Random baseline — d_G if subspaces were unrelated
    # Qwen2.5-7B has hidden_size 3584; MLP intermediate is 18944.
    # Use the smaller (attention) for a conservative baseline.
    print("=" * 60)
    print("RANDOM BASELINE (rank-16 subspaces in R^3584, unrelated)")
    print("=" * 60)
    rand_baseline = random_baseline(3584, 16)
    print(f"  d_G between unrelated rank-16 subspaces: {rand_baseline:.3f} rad")
    print(f"  (~ all 16 angles near pi/2 = 1.571 rad, giving sqrt(16 * 1.571^2) ~ 6.28)")
    print()

    # 2. Overall same-task d_G
    print("=" * 60)
    print("OVERALL SAME-TASK D_G (5 seeds, all 1960 pair-layer entries)")
    print("=" * 60)
    print(f"  mean   = {df['d_grassmannian'].mean():.3f} rad")
    print(f"  median = {df['d_grassmannian'].median():.3f} rad")
    print(f"  std    = {df['d_grassmannian'].std():.3f}")
    print(f"  min    = {df['d_grassmannian'].min():.3f}")
    print(f"  max    = {df['d_grassmannian'].max():.3f}")
    print()
    print(f"  baseline ratio: {df['d_grassmannian'].mean() / rand_baseline:.3f}")
    print(f"  (1.0 = unrelated; 0.0 = identical subspace)")
    print()

    # 3. By sublayer: attention vs MLP — the M7 territory
    print("=" * 60)
    print("BY SUBLAYER (attention vs MLP)")
    print("=" * 60)
    by_sub = df.groupby("sublayer")["d_grassmannian"].agg(["mean", "std", "count"])
    print(by_sub.to_string())
    print()

    # 4. By module — q/k/v/o vs gate/up/down
    print("=" * 60)
    print("BY MODULE (which projections agree most across seeds?)")
    print("=" * 60)
    by_mod = df.groupby(["sublayer", "module"])["d_grassmannian"].agg(["mean", "std", "count"])
    print(by_mod.to_string())
    print()

    # 5. By depth — early/mid/late layers
    print("=" * 60)
    print("BY DEPTH (early/mid/late layers)")
    print("=" * 60)
    depth_bins = pd.cut(df["layer_idx"], bins=[-1, 9, 18, 28],
                        labels=["early (0-9)", "mid (10-18)", "late (19-27)"])
    df["depth"] = depth_bins
    by_depth = df.groupby("depth", observed=True)["d_grassmannian"].agg(["mean", "std", "count"])
    print(by_depth.to_string())
    print()

    # 6. Distribution buckets
    print("=" * 60)
    print("DISTRIBUTION OF D_G ACROSS ALL ENTRIES")
    print("=" * 60)
    buckets = pd.cut(
        df["d_grassmannian"],
        bins=[0, 1, 2, 3, 4, 5, 6, rand_baseline + 1],
        labels=["<1 (very close)", "1-2", "2-3", "3-4", "4-5", "5-6",
                f">6 (near baseline {rand_baseline:.1f})"],
    )
    print(buckets.value_counts(sort=False).to_string())
    print()

    # 7. Per-layer detail — which exact layer agreements are best/worst?
    print("=" * 60)
    print("TOP 10 LAYERS WITH SMALLEST D_G (best same-task agreement)")
    print("=" * 60)
    per_layer = df.groupby(["sublayer", "module", "layer_idx"])["d_grassmannian"].mean()
    print(per_layer.sort_values().head(10).to_string())
    print()
    print("=" * 60)
    print("BOTTOM 10 LAYERS WITH LARGEST D_G (worst same-task agreement)")
    print("=" * 60)
    print(per_layer.sort_values().tail(10).to_string())


if __name__ == "__main__":
    main()
