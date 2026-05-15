"""Path-vs-speed test on the existing hellaswag trajectory.

Question (T2 from plan.md): for pairs of same-task LoRAs that hit similar
final accuracy, are their trajectories the same PATH traversed at different
speeds, or DIFFERENT PATHS to the same point?

Method, per (sublayer, module, layer_idx):
  - For each seed s, build the per-step trajectory of U_s(t) (the rank-16
    subspace at step t).
  - For each pair (s_a, s_b), compute two distance series:
      (a) ALIGNED-IN-TIME:  D_aligned[t]  = d_G(U_a(t),  U_b(t))
      (b) DTW-OPTIMAL:      D_dtw         = DTW cost over d_G(U_a(t), U_b(t'))
        with monotone time-warps t -> t'.
  - "Same path, different speeds"  <=>  DTW cost << aligned cost.
  - "Different paths"               <=>  DTW cost ~ aligned cost.

Aggregate ratio  r = mean(D_dtw) / mean(D_aligned)
    r close to 1   => warping doesn't help => same speeds OR genuinely different paths
    r much < 1     => warping helps a lot => same path, different speeds (good for us)

We also report the random baseline: d_G between unrelated rank-16 subspaces
in R^3584 (~6.28 rad).

Inputs:
  - experiment1/adapters/<task>_seed<seed>/{checkpoint-*, final}/
    (loaded directly via the same QR+SVD trick as compute_trajectory_features)
  - For speed we reuse already-saved U bases if a cache exists.

Outputs:
  - experiment1/analyze/path_vs_speed.csv  (per (layer, pair) numbers)
  - experiment1/analyze/path_vs_speed_summary.txt  (textual headline)
  - experiment1/analyze/phase_plots/path_vs_speed_pairs.png

CPU-only. ~10-20 min for 5 seeds x 196 layers x 41 ckpts on a modern laptop.
"""
from __future__ import annotations

import argparse
import itertools
import re
import time
from pathlib import Path

import numpy as np
import pandas as pd
from safetensors.torch import load_file

EXP = Path(__file__).resolve().parents[1]


# ---------------------------------------------------------------------------
# Reuse the same primitives as compute_trajectory_features (kept local so this
# script is runnable standalone).
# ---------------------------------------------------------------------------

def parse_layer_key(key: str):
    m = re.match(
        r"base_model\.model\.model\.layers\.(\d+)\.(self_attn|mlp)\.(\w+_proj)\.lora_([AB])\.weight",
        key,
    )
    if not m:
        return None
    return int(m.group(1)), m.group(2), m.group(3), m.group(4)


def extract_U_per_layer(ckpt_dir: Path) -> dict[tuple[int, str, str], np.ndarray]:
    sd = load_file(str(ckpt_dir / "adapter_model.safetensors"))
    pairs: dict[tuple[int, str, str], dict] = {}
    for key, t in sd.items():
        parsed = parse_layer_key(key)
        if parsed is None:
            continue
        layer_idx, sublayer, module, ab = parsed
        pairs.setdefault((layer_idx, sublayer, module), {})[ab] = (
            t.numpy().astype("float32")
        )
    out = {}
    for k, ab in pairs.items():
        if "A" not in ab or "B" not in ab:
            continue
        B, A = ab["B"], ab["A"]
        Q_B, R_B = np.linalg.qr(B)
        M = R_B @ A
        U_small, _, _ = np.linalg.svd(M, full_matrices=False)
        out[k] = (Q_B @ U_small).astype("float32")
    return out


def iter_checkpoints(seed_dir: Path) -> list[tuple[int, Path]]:
    out = []
    for d in seed_dir.iterdir():
        if not d.is_dir():
            continue
        if d.name.startswith("checkpoint-"):
            try:
                out.append((int(d.name.split("-")[1]), d))
            except (ValueError, IndexError):
                continue
        elif d.name == "final":
            out.append((-1, d))
    out.sort()
    if out and out[0][0] == -1:
        rest_max = max((s for s, _ in out if s >= 0), default=0)
        out[0] = (rest_max + 1, out[0][1])
        out.sort()
    return out


def d_G(U_a: np.ndarray, U_b: np.ndarray) -> float:
    cosines = np.linalg.svd(U_a.T @ U_b, compute_uv=False)
    cosines = np.clip(cosines, -1.0, 1.0)
    return float(np.sqrt((np.arccos(cosines) ** 2).sum()))


# ---------------------------------------------------------------------------
# Pairwise cost matrix and DTW
# ---------------------------------------------------------------------------

def cost_matrix(traj_a: list[np.ndarray], traj_b: list[np.ndarray]) -> np.ndarray:
    """C[i, j] = d_G(traj_a[i], traj_b[j]). (T, T) symmetric-ish."""
    T_a, T_b = len(traj_a), len(traj_b)
    C = np.empty((T_a, T_b), dtype="float64")
    for i in range(T_a):
        Ua = traj_a[i]
        for j in range(T_b):
            C[i, j] = d_G(Ua, traj_b[j])
    return C


def dtw_total_cost(C: np.ndarray) -> float:
    """Standard DTW with the three classical moves (i+1,j) / (i,j+1) / (i+1,j+1).
    Returns the total accumulated cost along the optimal monotone alignment.
    Endpoints are forced to (0,0) and (T_a-1, T_b-1). No warping window.
    """
    T_a, T_b = C.shape
    D = np.full_like(C, np.inf, dtype="float64")
    D[0, 0] = C[0, 0]
    for i in range(T_a):
        for j in range(T_b):
            if i == 0 and j == 0:
                continue
            best = np.inf
            if i > 0:
                best = min(best, D[i - 1, j])
            if j > 0:
                best = min(best, D[i, j - 1])
            if i > 0 and j > 0:
                best = min(best, D[i - 1, j - 1])
            D[i, j] = C[i, j] + best
    return float(D[T_a - 1, T_b - 1])


def aligned_total_cost(C: np.ndarray) -> float:
    """No warping: sum of the diagonal d_G(U_a(t), U_b(t))."""
    T = min(C.shape)
    return float(np.sum(np.diag(C)[:T]))


# ---------------------------------------------------------------------------
# Main per-(layer, pair) loop
# ---------------------------------------------------------------------------

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--task", default="hellaswag")
    p.add_argument("--seeds", default="0,1,2,3,4")
    p.add_argument("--adapters-root", type=Path, default=EXP / "adapters")
    p.add_argument("--out-csv", type=Path,
                   default=EXP / "analyze" / "path_vs_speed.csv")
    p.add_argument("--summary", type=Path,
                   default=EXP / "analyze" / "path_vs_speed_summary.txt")
    p.add_argument("--plot",   type=Path,
                   default=EXP / "analyze" / "phase_plots" / "path_vs_speed_pairs.png")
    p.add_argument("--max-layers", type=int, default=None,
                   help="Subsample layers for a quick smoke run.")
    args = p.parse_args()

    seeds = [int(s) for s in args.seeds.split(",")]
    print(f"[load] {args.task} seeds={seeds}", flush=True)

    # Load all U(t) per seed, organized by (layer_idx, sublayer, module).
    per_seed: dict[int, dict[int, dict[tuple[int, str, str], np.ndarray]]] = {}
    common_steps: set[int] | None = None
    for s in seeds:
        seed_dir = args.adapters_root / f"{args.task}_seed{s}"
        if not seed_dir.exists():
            raise SystemExit(f"missing adapter dir: {seed_dir}")
        ckpts = iter_checkpoints(seed_dir)
        if not ckpts:
            raise SystemExit(f"no checkpoints under {seed_dir}")
        print(f"  seed {s}: {len(ckpts)} checkpoints", flush=True)
        t0 = time.time()
        steps_map: dict[int, dict[tuple[int, str, str], np.ndarray]] = {}
        for step, d in ckpts:
            steps_map[step] = extract_U_per_layer(d)
        per_seed[s] = steps_map
        print(f"    loaded in {time.time() - t0:.1f}s", flush=True)
        cs = set(steps_map.keys())
        common_steps = cs if common_steps is None else (common_steps & cs)

    steps_sorted = sorted(common_steps or [])
    print(f"[load] {len(steps_sorted)} common steps", flush=True)

    # Common layer set across seeds at step 0
    layer_keys = set(per_seed[seeds[0]][steps_sorted[0]].keys())
    for s in seeds:
        layer_keys &= set(per_seed[s][steps_sorted[0]].keys())
    layer_keys = sorted(layer_keys)
    if args.max_layers is not None:
        layer_keys = layer_keys[:: max(1, len(layer_keys) // args.max_layers)]
    print(f"[load] {len(layer_keys)} layers in scope", flush=True)

    # Random baseline: rank-16 in R^3584
    rng = np.random.default_rng(0)
    randoms = []
    for _ in range(50):
        X = rng.standard_normal((3584, 16))
        Y = rng.standard_normal((3584, 16))
        Q_x, _ = np.linalg.qr(X)
        Q_y, _ = np.linalg.qr(Y)
        randoms.append(d_G(Q_x, Q_y))
    rand_baseline = float(np.mean(randoms))
    print(f"[baseline] random rank-16 in R^3584: d_G ~ {rand_baseline:.3f} rad",
          flush=True)

    rows = []
    pairs = list(itertools.combinations(seeds, 2))
    print(f"[run] {len(pairs)} pairs x {len(layer_keys)} layers", flush=True)

    t0 = time.time()
    for li, lk in enumerate(layer_keys):
        layer_idx, sublayer, module = lk
        # Build per-seed trajectories for this layer
        trajs: dict[int, list[np.ndarray]] = {}
        for s in seeds:
            trajs[s] = [per_seed[s][step][lk] for step in steps_sorted]

        for a, b in pairs:
            C = cost_matrix(trajs[a], trajs[b])
            T = C.shape[0]
            aligned_total = aligned_total_cost(C)
            dtw_total = dtw_total_cost(C)
            aligned_mean = aligned_total / T
            dtw_mean = dtw_total / T  # rough per-step cost
            warp_ratio = dtw_mean / aligned_mean if aligned_mean > 0 else float("nan")
            rows.append({
                "task": args.task,
                "layer_idx": layer_idx,
                "sublayer": sublayer,
                "module": module,
                "seed_a": a,
                "seed_b": b,
                "T": T,
                "aligned_mean_dG": aligned_mean,
                "dtw_mean_dG": dtw_mean,
                "warp_ratio": warp_ratio,
                "endpoint_dG": float(C[-1, -1]),
                "init_dG": float(C[0, 0]),
            })
        if (li + 1) % 20 == 0 or li == len(layer_keys) - 1:
            print(f"  [{li + 1}/{len(layer_keys)}] layers done"
                  f"  ({time.time() - t0:.1f}s)", flush=True)

    df = pd.DataFrame(rows)
    args.out_csv.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.out_csv, index=False)
    print(f"[write] {len(df)} rows -> {args.out_csv}", flush=True)

    # ---------- Headline summary ------------------------------------------
    lines = []
    lines.append("PATH vs SPEED — DTW on same-task LoRA trajectories")
    lines.append("=" * 70)
    lines.append(f"task          : {args.task}")
    lines.append(f"seeds         : {seeds}")
    lines.append(f"layers used   : {len(layer_keys)}  (of 196 if full Qwen2.5-7B)")
    lines.append(f"pairs / layer : {len(pairs)}")
    lines.append(f"steps         : {len(steps_sorted)}")
    lines.append("")
    lines.append(f"random baseline d_G (rank-16 in R^3584) : {rand_baseline:.3f} rad")
    lines.append("")
    lines.append("OVERALL")
    lines.append("-" * 70)
    lines.append(f"  mean aligned-in-time d_G : {df['aligned_mean_dG'].mean():.4f}")
    lines.append(f"  mean DTW-warped d_G      : {df['dtw_mean_dG'].mean():.4f}")
    lines.append(f"  mean warp-ratio          : {df['warp_ratio'].mean():.4f}")
    lines.append(f"  mean endpoint d_G        : {df['endpoint_dG'].mean():.4f}")
    lines.append(f"  mean init d_G            : {df['init_dG'].mean():.4f}")
    lines.append("")
    lines.append("INTERPRETATION")
    lines.append("-" * 70)
    lines.append("  warp_ratio close to 1.0   => trajectories already aligned in time")
    lines.append("                                (same path AND same speed, OR")
    lines.append("                                 different paths that DTW can't fix)")
    lines.append("  warp_ratio << 1.0         => same path, different speeds")
    lines.append("                                (this is the 'same path' headline)")
    lines.append("")
    lines.append("BY SUBLAYER")
    lines.append("-" * 70)
    by_sub = df.groupby("sublayer")[
        ["aligned_mean_dG", "dtw_mean_dG", "warp_ratio", "endpoint_dG"]
    ].mean()
    lines.append(by_sub.to_string())
    lines.append("")
    lines.append("BY MODULE")
    lines.append("-" * 70)
    by_mod = df.groupby(["sublayer", "module"])[
        ["aligned_mean_dG", "dtw_mean_dG", "warp_ratio", "endpoint_dG"]
    ].mean()
    lines.append(by_mod.to_string())
    lines.append("")
    lines.append("ENDPOINT d_G  vs  RANDOM BASELINE")
    lines.append("-" * 70)
    lines.append(
        f"  endpoint d_G / random  =  {df['endpoint_dG'].mean() / rand_baseline:.4f}"
    )
    lines.append("  (1.0 = unrelated subspaces ;  ~0 = identical subspace)")
    text = "\n".join(lines)
    print()
    print(text)
    args.summary.write_text(text, encoding="utf-8")
    print(f"\n[write] summary -> {args.summary}", flush=True)

    # ---------- Plot -------------------------------------------------------
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        axes[0].scatter(df["aligned_mean_dG"], df["dtw_mean_dG"], s=6, alpha=0.4)
        m = max(df["aligned_mean_dG"].max(), df["dtw_mean_dG"].max())
        axes[0].plot([0, m], [0, m], "k--", alpha=0.5, label="y = x")
        axes[0].set_xlabel("aligned-in-time mean d_G")
        axes[0].set_ylabel("DTW-warped mean d_G")
        axes[0].set_title("Per (layer, pair) — DTW vs aligned")
        axes[0].legend()
        axes[0].grid(alpha=0.3)

        axes[1].hist(df["warp_ratio"].dropna(), bins=40, edgecolor="black")
        axes[1].axvline(1.0, color="red", linestyle="--", label="ratio = 1")
        axes[1].set_xlabel("warp_ratio = DTW / aligned")
        axes[1].set_ylabel("count")
        axes[1].set_title("Distribution of warp-ratio")
        axes[1].legend()
        axes[1].grid(alpha=0.3)

        args.plot.parent.mkdir(parents=True, exist_ok=True)
        fig.tight_layout()
        fig.savefig(args.plot, dpi=120)
        plt.close(fig)
        print(f"[write] plot -> {args.plot}", flush=True)
    except Exception as exc:
        print(f"[plot] skipped: {exc}")


if __name__ == "__main__":
    main()
