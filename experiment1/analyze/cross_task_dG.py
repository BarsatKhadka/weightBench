"""Within-task vs between-task Grassmannian distance — the headline 'path/point' test.

Question (C1 from plan.md, scaled to multi-task):
  Same-task LoRAs should land in similar 16-dim subspaces  (small d_G).
  Different-task LoRAs should land in different subspaces  (large d_G,
  approaching the random baseline ~6.28 rad).
  If yes: task identity is *encoded geometrically* — knowledge is a path
  with a task-specific terminus, not a single universal point.

Reads endpoint adapters from experiment1/adapters/<task>_seed<seed>/final
and computes, per layer:
  - all within-task pairs        d_G(same task,  different seeds)
  - all between-task pairs       d_G(different task pairs of seeds)
  - random baseline              d_G between rank-16 uniformly-random subspaces

Outputs:
  - experiment1/analyze/cross_task_dG.csv               (one row per layer-pair)
  - experiment1/analyze/cross_task_dG_summary.txt       (textual headline)
  - experiment1/analyze/phase_plots/cross_task_dG.png   (within/between/random)

Usage:
  python analyze/cross_task_dG.py \
      --tasks hellaswag boolq arc_easy winogrande gsm8k \
      --seeds 0,1,2

The Path-not-Point headline is a single number:
  separation_z = (mean_between - mean_within) / std_within
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
# QR + small-SVD for U(dW) (rank-16 left singular vectors of dW = B@A)
# ---------------------------------------------------------------------------

def parse_layer_key(key: str):
    m = re.match(
        r"base_model\.model\.model\.layers\.(\d+)\.(self_attn|mlp)\.(\w+_proj)\.lora_([AB])\.weight",
        key,
    )
    if not m:
        return None
    return int(m.group(1)), m.group(2), m.group(3), m.group(4)


def left_singular_vectors(ckpt_path: Path) -> dict[tuple[int, str, str], np.ndarray]:
    sd = load_file(str(ckpt_path / "adapter_model.safetensors"))
    pairs: dict[tuple[int, str, str], dict] = {}
    for key, t in sd.items():
        parsed = parse_layer_key(key)
        if parsed is None:
            continue
        layer_idx, sublayer, module, ab = parsed
        pairs.setdefault((layer_idx, sublayer, module), {})[ab] = (
            t.numpy().astype("float32")
        )
    out: dict[tuple[int, str, str], np.ndarray] = {}
    for k, ab in pairs.items():
        if "A" not in ab or "B" not in ab:
            continue
        B, A = ab["B"], ab["A"]
        Q_B, R_B = np.linalg.qr(B)
        M = R_B @ A
        U_small, _, _ = np.linalg.svd(M, full_matrices=False)
        out[k] = (Q_B @ U_small).astype("float32")
    return out


def d_grassmannian(U_a: np.ndarray, U_b: np.ndarray) -> float:
    s = np.linalg.svd(U_a.T @ U_b, compute_uv=False)
    s = np.clip(s, -1.0, 1.0)
    return float(np.sqrt((np.arccos(s) ** 2).sum()))


# ---------------------------------------------------------------------------
# Random baseline
# ---------------------------------------------------------------------------

def random_baseline(n_dim: int, rank: int, n_trials: int = 200, seed: int = 0) -> float:
    rng = np.random.default_rng(seed)
    samples = []
    for _ in range(n_trials):
        X = rng.standard_normal((n_dim, rank))
        Y = rng.standard_normal((n_dim, rank))
        Q_x, _ = np.linalg.qr(X)
        Q_y, _ = np.linalg.qr(Y)
        samples.append(d_grassmannian(Q_x, Q_y))
    return float(np.mean(samples))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--tasks", nargs="+",
                   default=["hellaswag", "boolq", "arc_easy",
                            "winogrande", "gsm8k"])
    p.add_argument("--seeds", default="0,1,2",
                   help="Comma-separated. Will use only seeds present per task.")
    p.add_argument("--checkpoint", default="final")
    p.add_argument("--adapters-root", type=Path, default=EXP / "adapters")
    p.add_argument("--out-csv", type=Path,
                   default=EXP / "analyze" / "cross_task_dG.csv")
    p.add_argument("--summary", type=Path,
                   default=EXP / "analyze" / "cross_task_dG_summary.txt")
    p.add_argument("--plot", type=Path,
                   default=EXP / "analyze" / "phase_plots" / "cross_task_dG.png")
    p.add_argument("--hidden-size", type=int, default=3584,
                   help="For random baseline (Qwen2.5-7B: 3584).")
    args = p.parse_args()

    seeds = [int(s) for s in args.seeds.split(",")]

    # ----- load adapters --------------------------------------------------
    print(f"[load] tasks={args.tasks} seeds={seeds} checkpoint={args.checkpoint}",
          flush=True)
    per_run: dict[tuple[str, int], dict[tuple[int, str, str], np.ndarray]] = {}
    for task in args.tasks:
        for seed in seeds:
            ckpt = args.adapters_root / f"{task}_seed{seed}" / args.checkpoint
            if not ckpt.exists():
                print(f"  [skip] {task}_seed{seed}: {ckpt} not found", flush=True)
                continue
            t0 = time.time()
            per_run[(task, seed)] = left_singular_vectors(ckpt)
            print(f"  [{task} seed {seed}] loaded in {time.time() - t0:.1f}s "
                  f"({len(per_run[(task, seed)])} layers)", flush=True)

    if not per_run:
        raise SystemExit("no adapters loaded")

    # ----- random baseline ------------------------------------------------
    rand = random_baseline(args.hidden_size, 16)
    print(f"[baseline] random d_G in R^{args.hidden_size}, rank 16: {rand:.3f} rad",
          flush=True)

    # ----- shared layer keys ----------------------------------------------
    layer_keys = set.intersection(*[set(d.keys()) for d in per_run.values()])
    layer_keys = sorted(layer_keys)
    print(f"[layers] {len(layer_keys)} shared across all runs", flush=True)

    # ----- pairwise --------------------------------------------------------
    runs = sorted(per_run.keys())
    pairs = list(itertools.combinations(runs, 2))
    print(f"[pairs] {len(pairs)} run-pairs", flush=True)

    rows = []
    t0 = time.time()
    for i, lk in enumerate(layer_keys):
        layer_idx, sublayer, module = lk
        for (ta, sa), (tb, sb) in pairs:
            d = d_grassmannian(per_run[(ta, sa)][lk], per_run[(tb, sb)][lk])
            rows.append({
                "layer_idx": layer_idx,
                "sublayer": sublayer,
                "module": module,
                "task_a": ta, "seed_a": sa,
                "task_b": tb, "seed_b": sb,
                "same_task": ta == tb,
                "d_grassmannian": d,
                "ratio_to_random": d / rand,
            })
        if (i + 1) % 50 == 0 or i == len(layer_keys) - 1:
            print(f"  [{i + 1}/{len(layer_keys)}] layers"
                  f"  ({time.time() - t0:.1f}s)", flush=True)

    df = pd.DataFrame(rows)
    args.out_csv.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.out_csv, index=False)
    print(f"[write] {len(df)} rows -> {args.out_csv}", flush=True)

    # ----- headline summary -----------------------------------------------
    within = df[df["same_task"]]
    between = df[~df["same_task"]]

    lines = []
    lines.append("CROSS-TASK d_G — within vs between task")
    lines.append("=" * 72)
    lines.append(f"tasks       : {sorted({k[0] for k in runs})}")
    lines.append(f"seeds       : {sorted({k[1] for k in runs})}")
    lines.append(f"runs loaded : {len(runs)}")
    lines.append(f"layers      : {len(layer_keys)}")
    lines.append(f"pairs/layer : {len(pairs)}  "
                 f"(within: {sum(1 for (a, b) in pairs if a[0] == b[0])}, "
                 f"between: {sum(1 for (a, b) in pairs if a[0] != b[0])})")
    lines.append(f"random d_G  : {rand:.3f} rad  (baseline = unrelated subspaces)")
    lines.append("")
    lines.append("OVERALL")
    lines.append("-" * 72)
    lines.append(f"  within-task   : mean={within['d_grassmannian'].mean():.4f}  "
                 f"std={within['d_grassmannian'].std():.4f}  "
                 f"n={len(within)}")
    lines.append(f"  between-task  : mean={between['d_grassmannian'].mean():.4f}  "
                 f"std={between['d_grassmannian'].std():.4f}  "
                 f"n={len(between)}")
    sep_z = ((between["d_grassmannian"].mean() - within["d_grassmannian"].mean())
             / within["d_grassmannian"].std()
             if len(within) and within["d_grassmannian"].std() > 0 else float("nan"))
    lines.append(f"  separation_z  : {sep_z:.3f}  "
                 f"(>5 => same-task collapse + clean between-task separation)")
    lines.append(f"  within/random : {within['d_grassmannian'].mean() / rand:.3f}")
    lines.append(f"  between/random: {between['d_grassmannian'].mean() / rand:.3f}")
    lines.append("")
    lines.append("BY SUBLAYER")
    lines.append("-" * 72)
    grp = df.groupby(["sublayer", "same_task"])["d_grassmannian"].agg(["mean", "std", "count"])
    lines.append(grp.to_string())
    lines.append("")
    lines.append("BY MODULE")
    lines.append("-" * 72)
    grp = (df.groupby(["sublayer", "module", "same_task"])["d_grassmannian"]
             .agg(["mean", "std", "count"]))
    lines.append(grp.to_string())
    lines.append("")
    lines.append("BY DEPTH (layer_idx bins)")
    lines.append("-" * 72)
    df["depth_bin"] = pd.cut(df["layer_idx"], bins=4)
    grp = df.groupby(["depth_bin", "same_task"], observed=True)["d_grassmannian"].mean()
    lines.append(grp.to_string())
    text = "\n".join(lines)
    print()
    print(text)
    args.summary.write_text(text, encoding="utf-8")
    print(f"\n[write] summary -> {args.summary}", flush=True)

    # ----- plot ----------------------------------------------------------
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(9, 5))
        bins = np.linspace(0, max(rand + 0.5, df["d_grassmannian"].max() + 0.1), 60)
        ax.hist(within["d_grassmannian"], bins=bins, alpha=0.55,
                label=f"within-task (n={len(within)})", color="tab:blue")
        ax.hist(between["d_grassmannian"], bins=bins, alpha=0.55,
                label=f"between-task (n={len(between)})", color="tab:red")
        ax.axvline(rand, color="black", linestyle="--",
                   label=f"random baseline ({rand:.2f})")
        ax.set_xlabel("Grassmannian distance d_G  (rad)")
        ax.set_ylabel("count")
        ax.set_title("Endpoint subspace distance — within vs between task")
        ax.legend()
        ax.grid(alpha=0.3)
        args.plot.parent.mkdir(parents=True, exist_ok=True)
        fig.tight_layout()
        fig.savefig(args.plot, dpi=120)
        plt.close(fig)
        print(f"[write] plot -> {args.plot}", flush=True)
    except Exception as exc:
        print(f"[plot] skipped: {exc}")


if __name__ == "__main__":
    main()
