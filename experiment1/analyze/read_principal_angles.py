"""Per-angle drill-down on subspace_distances.csv.

The Grassmannian distance d_G aggregates all 16 principal angles into one
scalar. That summary can hide structure where the FIRST few angles agree
while the rest are noise.

This script asks: across all (layer, seed_pair) entries, how does each of
the 16 angles behave on average? If theta_0 is small but theta_15 is near
90 degrees, we have "agreement on primary direction(s) only."

Output: a table of mean(theta_i) for i = 0..15, plus per-module breakdown.
"""
from pathlib import Path
import numpy as np
import pandas as pd

EXP = Path(__file__).resolve().parents[1]


def main() -> None:
    df = pd.read_csv(EXP / "analyze" / "subspace_distances.csv")
    angle_cols = [f"theta_{i:02d}_deg" for i in range(16)]

    print("=" * 70)
    print("MEAN PRINCIPAL ANGLE PER INDEX (across all 1960 (layer, pair) entries)")
    print("=" * 70)
    print(f"{'idx':>3s}  {'mean(deg)':>10s}  {'std':>7s}  {'min':>7s}  {'max':>7s}  bar")
    means = df[angle_cols].mean()
    stds = df[angle_cols].std()
    mins = df[angle_cols].min()
    maxs = df[angle_cols].max()
    for i, col in enumerate(angle_cols):
        m = means[col]
        # visual bar: each block = 5 degrees
        bar = "#" * int(m / 2)
        print(f"{i:3d}  {m:10.2f}  {stds[col]:7.2f}  {mins[col]:7.2f}  {maxs[col]:7.2f}  {bar}")

    print()
    print(f"Mean of all 16 angles: {means.mean():.2f} deg")
    print(f"Mean of first 4 angles (top directions): {means.iloc[:4].mean():.2f} deg")
    print(f"Mean of last 4 angles (bottom directions): {means.iloc[-4:].mean():.2f} deg")
    print()
    print("Reading guide:")
    print("  0 deg     = perfectly aligned direction")
    print("  90 deg    = orthogonal (random)")
    print("  ~85-90 deg uniformly = subspaces are essentially random")
    print("  Decreasing pattern (0 small, 15 large) = LoRAs agree on top directions")
    print("    but diverge on minor ones -> partial overlap structure")

    print()
    print("=" * 70)
    print("BY MODULE: mean(theta_0) — agreement on the strongest direction")
    print("=" * 70)
    by_mod_top = (df.groupby(["sublayer", "module"])[angle_cols[0]]
                    .agg(["mean", "std", "count"]))
    print(by_mod_top.to_string())
    print()

    print("=" * 70)
    print("BY MODULE: mean of first 4 principal angles (top-direction agreement)")
    print("=" * 70)
    df["top4_mean"] = df[angle_cols[:4]].mean(axis=1)
    by_mod_top4 = (df.groupby(["sublayer", "module"])["top4_mean"]
                     .agg(["mean", "std", "count"]))
    print(by_mod_top4.to_string())


if __name__ == "__main__":
    main()
