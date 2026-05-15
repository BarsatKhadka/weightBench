"""Quality gate: which LoRAs are actually better than the base?

We want to refuse to compute path/trajectory geometry on LoRAs that didn't
learn anything — they pollute the within-task d_G distribution and make
the headline noisier. This script reads eval_summary.csv (produced by
aggregate_eval.py) and prints / writes:

  - per (task, seed): acc_norm minus base acc_norm   (the "lift")
  - PASS / FAIL flag at threshold (default: lift > 2 * combined stderr)
  - a tidy CSV of just the good runs, ready to be passed as --gate-list to
    cross_task_dG.py / path_vs_speed.py.

Usage:
  python analyze/quality_gate.py
  python analyze/quality_gate.py --metric acc_norm --min-lift 0.01
  python analyze/quality_gate.py --strict             # only lift > 2*stderr
"""
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

EXP = Path(__file__).resolve().parents[1]


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--summary", type=Path,
                   default=EXP / "analyze" / "eval_summary.csv")
    p.add_argument("--metric", default="acc_norm",
                   help="acc, acc_norm, exact_match, ... (whichever the task uses)")
    p.add_argument("--fallback-metric", default="acc",
                   help="If --metric isn't present for a task, use this.")
    p.add_argument("--min-lift", type=float, default=0.005,
                   help="Absolute lift threshold (default 0.5 pp).")
    p.add_argument("--strict", action="store_true",
                   help="Also require lift > 2 * combined stderr.")
    p.add_argument("--out", type=Path,
                   default=EXP / "analyze" / "lora_gate.csv")
    args = p.parse_args()

    if not args.summary.exists():
        raise SystemExit(f"missing {args.summary} - run aggregate_eval.py first")

    df = pd.read_csv(args.summary)

    # ---- helpers ---------------------------------------------------------
    def value_and_stderr(sub: pd.DataFrame, metric: str) -> tuple[float, float]:
        """Pick metric=<m>,none and metric=<m>_stderr,none from the rows."""
        v = sub[sub["metric"].str.startswith(f"{metric},")]
        s = sub[sub["metric"].str.startswith(f"{metric}_stderr,")]
        if v.empty:
            return float("nan"), float("nan")
        val = float(v["value"].iloc[0])
        stderr = float(s["value"].iloc[0]) if not s.empty else float("nan")
        return val, stderr

    # ---- base per task ---------------------------------------------------
    base_rows = df[df["is_base"]]
    base_map: dict[str, tuple[float, float, str]] = {}
    for task in base_rows["task"].unique():
        sub = base_rows[base_rows["task"] == task]
        v, e = value_and_stderr(sub, args.metric)
        used = args.metric
        if pd.isna(v):
            v, e = value_and_stderr(sub, args.fallback_metric)
            used = args.fallback_metric
        if not pd.isna(v):
            base_map[task] = (v, e, used)

    if not base_map:
        raise SystemExit("no base-model results found in eval_summary.csv")

    print("Base scores:")
    for t, (v, e, m) in sorted(base_map.items()):
        print(f"  {t:15s} {m:10s} = {v:.4f} (+/- {e:.4f})")
    print()

    # ---- LoRA rows -------------------------------------------------------
    # Skip "_letterfmt" rerun variants — they're a known-bad prompt formatting
    # ablation; we want the canonical eval.
    df_lora = df[(~df["is_base"]) & (~df["model_id"].str.contains("letterfmt"))]
    rows = []
    for model_id, sub in df_lora.groupby("model_id"):
        seed = sub["seed"].iloc[0]
        # Pick which task this LoRA was trained on. We trust the model_id prefix.
        task_guess = None
        for t in base_map:
            if model_id.startswith(t):
                task_guess = t
                break
        if task_guess is None:
            # fall back to the task field
            task_guess = sub["task"].iloc[0]
        sub_t = sub[sub["task"] == task_guess]
        if sub_t.empty:
            continue
        v, e = value_and_stderr(sub_t, args.metric)
        used = args.metric
        if pd.isna(v):
            v, e = value_and_stderr(sub_t, args.fallback_metric)
            used = args.fallback_metric
        base_v, base_e, _ = base_map.get(task_guess, (float("nan"), float("nan"), ""))
        lift = v - base_v if not pd.isna(v) else float("nan")
        comb_stderr = (e ** 2 + base_e ** 2) ** 0.5 if not (
            pd.isna(e) or pd.isna(base_e)) else float("nan")
        pass_abs = (not pd.isna(lift)) and (lift > args.min_lift)
        pass_strict = (not pd.isna(comb_stderr)) and (lift > 2 * comb_stderr)
        gate = pass_abs and (pass_strict if args.strict else True)
        rows.append({
            "model_id": model_id,
            "task": task_guess,
            "seed": int(seed) if not pd.isna(seed) else None,
            "metric": used,
            "lora_value": v,
            "base_value": base_v,
            "lift": lift,
            "combined_stderr": comb_stderr,
            "lift_over_2stderr": (lift / (2 * comb_stderr))
                if comb_stderr and not pd.isna(comb_stderr) and comb_stderr > 0
                else float("nan"),
            "pass": bool(gate),
        })

    out = pd.DataFrame(rows).sort_values(["task", "seed"])
    args.out.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.out, index=False)

    # ---- pretty print ----------------------------------------------------
    print("Per-LoRA gate report")
    print("=" * 88)
    print(f"{'task':14s} {'seed':>4s} {'metric':10s} "
          f"{'lora':>8s} {'base':>8s} {'lift':>8s} "
          f"{'2*stderr':>9s}  pass")
    print("-" * 88)
    for _, r in out.iterrows():
        seed_s = "-" if r["seed"] is None or pd.isna(r["seed"]) else f"{int(r['seed'])}"
        two_se = (2 * r["combined_stderr"]
                  if not pd.isna(r["combined_stderr"]) else float("nan"))
        flag = "OK " if r["pass"] else "BAD"
        print(f"{r['task']:14s} {seed_s:>4s} {r['metric']:10s} "
              f"{r['lora_value']:8.4f} {r['base_value']:8.4f} "
              f"{r['lift']:+8.4f} {two_se:9.4f}  {flag}")
    print()
    n_pass = int(out["pass"].sum())
    n_total = len(out)
    print(f"PASS: {n_pass} / {n_total}  -- only these will be used downstream")
    print()
    bad = out[~out["pass"]]
    if len(bad):
        print("DROPPED:")
        for _, r in bad.iterrows():
            print(f"  - {r['model_id']}  (lift {r['lift']:+.4f})")
    print(f"\n[write] gate -> {args.out}")
    print("Pass to other scripts:")
    print(f"  --keep-csv {args.out}")


if __name__ == "__main__":
    main()
