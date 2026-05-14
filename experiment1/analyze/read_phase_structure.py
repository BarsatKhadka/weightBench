"""Phase structure visualization + change-point detection.

Reads trajectory_features.parquet and asks: do the per-layer signals
(frob_norm, effective_rank, top1_ratio, d_G_to_endpoint, d_G_velocity)
shift coordinately at the same training steps?

If they do -> phases exist and are detectable.
If they don't -> trajectories are smooth, no phase structure.

Output: textual summary + saved PNGs of trajectory plots.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

EXP = Path(__file__).resolve().parents[1]
OUT_DIR = EXP / "analyze" / "phase_plots"


def main() -> None:
    df = pd.read_parquet(EXP / "analyze" / "trajectory_features.parquet")
    print(f"loaded {len(df)} rows from trajectory_features.parquet")
    print(f"seeds: {sorted(df['seed'].unique())}")
    print(f"steps: {len(df['step'].unique())} unique "
          f"(min={df['step'].min()}, max={df['step'].max()})")
    print()

    # Try to import matplotlib for plotting; fall back to text-only if missing.
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        plotting = True
        OUT_DIR.mkdir(parents=True, exist_ok=True)
    except Exception:
        plotting = False
        print("(matplotlib unavailable; skipping plot output)")

    # ----- Step 1: per-signal aggregated trajectory ---------------------
    print("=" * 70)
    print("AVERAGED TRAJECTORY (mean over layers and seeds, per step)")
    print("=" * 70)
    agg = (df.groupby("step")
             [["frob_norm", "effective_rank", "top1_ratio",
               "d_G_to_endpoint", "d_G_velocity"]]
             .mean()
             .sort_index())
    print(agg.to_string())
    print()

    # ----- Step 2: detect change-points per signal -----------------------
    print("=" * 70)
    print("CHANGE-POINT HEURISTIC PER SIGNAL")
    print("=" * 70)
    for col in ["frob_norm", "effective_rank", "top1_ratio",
                "d_G_to_endpoint", "d_G_velocity"]:
        series = agg[col].dropna()
        cp = _detect_change_points(series)
        print(f"  {col:20s} change points at steps: {cp}")
    print()

    # ----- Step 3: per-module breakdown of trajectory shape -----------
    print("=" * 70)
    print("PER-MODULE FROB_NORM TRAJECTORY (mean over seeds, top steps shown)")
    print("=" * 70)
    by_mod = (df.groupby(["sublayer", "module", "step"])["frob_norm"]
                .mean().unstack("step"))
    print(by_mod.iloc[:, [0, len(by_mod.columns)//2, -1]].to_string())
    print()

    # ----- Step 4: lock-in heuristic per layer + seed -------------------
    print("=" * 70)
    print("LOCK-IN STEP: first step where d_G_to_endpoint < 50% of init value")
    print("=" * 70)
    lockins = []
    for (seed, layer_idx, sublayer, module), g in df.groupby(
            ["seed", "layer_idx", "sublayer", "module"]):
        g = g.sort_values("step")
        init_dG = g["d_G_to_endpoint"].iloc[0]
        threshold = 0.5 * init_dG
        below = g[g["d_G_to_endpoint"] < threshold]
        first_step = int(below["step"].iloc[0]) if len(below) else int(g["step"].iloc[-1])
        lockins.append({
            "seed": seed, "layer_idx": layer_idx, "sublayer": sublayer,
            "module": module, "lockin_step": first_step,
        })
    lock_df = pd.DataFrame(lockins)
    print(f"Overall mean lock-in step: {lock_df['lockin_step'].mean():.0f}")
    print(f"Overall std: {lock_df['lockin_step'].std():.1f}")
    print()
    print("By sublayer:")
    print(lock_df.groupby("sublayer")["lockin_step"].agg(["mean", "std"]).to_string())
    print()
    print("By module:")
    print(lock_df.groupby(["sublayer", "module"])["lockin_step"].agg(["mean", "std"]).to_string())
    print()

    # ----- Step 5: plots -----------------------------------------------
    if plotting:
        _plot_aggregate(agg, OUT_DIR / "agg_trajectory.png")
        _plot_per_module(df, OUT_DIR / "per_module_frob.png")
        _plot_lockin_histogram(lock_df, OUT_DIR / "lockin_histogram.png")
        print(f"plots saved to {OUT_DIR}/")


def _detect_change_points(series: pd.Series, k: int = 2) -> list[int]:
    """Return up to k step indices where the absolute first difference is largest."""
    if len(series) < 3:
        return []
    deltas = series.diff().abs().dropna()
    if deltas.sum() < 1e-12:
        return []
    top = deltas.nlargest(k).index.tolist()
    return sorted(int(s) for s in top)


def _plot_aggregate(agg: pd.DataFrame, out_path: Path) -> None:
    import matplotlib.pyplot as plt
    cols = ["frob_norm", "effective_rank", "top1_ratio",
            "d_G_to_endpoint", "d_G_velocity"]
    fig, axes = plt.subplots(len(cols), 1, figsize=(10, 14), sharex=True)
    for ax, c in zip(axes, cols):
        ax.plot(agg.index, agg[c], "o-")
        ax.set_ylabel(c)
        ax.grid(alpha=0.3)
    axes[-1].set_xlabel("training step")
    fig.suptitle("Mean trajectory across layers + seeds (hellaswag pool)")
    fig.tight_layout()
    fig.savefig(out_path, dpi=120)
    plt.close(fig)


def _plot_per_module(df: pd.DataFrame, out_path: Path) -> None:
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(10, 6))
    for (sub, mod), g in df.groupby(["sublayer", "module"]):
        ts = g.groupby("step")["frob_norm"].mean().sort_index()
        ax.plot(ts.index, ts.values, label=f"{sub}/{mod}", alpha=0.8)
    ax.set_xlabel("training step")
    ax.set_ylabel("frob_norm (mean across layers + seeds)")
    ax.set_title("Per-module trajectory of |dW|")
    ax.legend(loc="upper left", fontsize=8)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(out_path, dpi=120)
    plt.close(fig)


def _plot_lockin_histogram(lock_df: pd.DataFrame, out_path: Path) -> None:
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(lock_df["lockin_step"], bins=30, edgecolor="black")
    ax.set_xlabel("lock-in step (first step where d_G_to_endpoint < 50% of init)")
    ax.set_ylabel("count")
    ax.set_title(f"Lock-in step distribution across all (seed, layer)")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(out_path, dpi=120)
    plt.close(fig)


if __name__ == "__main__":
    main()
