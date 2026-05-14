"""Aggregate lm-eval JSON outputs into one tidy CSV.

After eval.sbatch finishes for each seed (and eval_base.sbatch for baseline),
this walks eval_results/ and produces a single small table with one row per
(model, task, metric).

Output: experiment1/analyze/eval_summary.csv

Run on magnolia (or anywhere with the eval_results dir):
    cd $HOME/weightBench/weightBench/experiment1
    source $HOME/weightBench/.venv/bin/activate
    python analyze/aggregate_eval.py
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import pandas as pd

EXP = Path(__file__).resolve().parents[1]


def find_results_json(d: Path) -> list[Path]:
    """lm_eval writes results to either results.json or results_<timestamp>.json
    inside subdirectories of the --output_path."""
    return sorted(d.rglob("results*.json"))


def parse_run(run_dir: Path) -> list[dict]:
    """Return list of rows from one model's eval. Each row = one metric of one task.

    Recognized directory name patterns:
        hellaswag_base                 → base model, no LoRA
        hellaswag_seed<N>              → final-adapter eval for one seed
        hellaswag_seed<N>_step<S>      → mid-trajectory eval at step S, seed N
    """
    name = run_dir.name
    seed = None
    step = None
    is_base = name.endswith("_base")
    if not is_base:
        m_step = re.search(r"seed(\d+)_step(\d+)$", name)
        if m_step:
            seed = int(m_step.group(1))
            step = int(m_step.group(2))
        else:
            m_seed = re.search(r"seed(\d+)$", name)
            seed = int(m_seed.group(1)) if m_seed else None

    rows: list[dict] = []
    for jpath in find_results_json(run_dir):
        with jpath.open("r", encoding="utf-8") as f:
            data = json.load(f)
        # lm_eval structure: data["results"][task_name][metric_name] = value
        results = data.get("results", {})
        for task, metrics in results.items():
            for metric_name, value in metrics.items():
                if not isinstance(value, (int, float)):
                    continue
                rows.append({
                    "model_id": name,
                    "is_base": is_base,
                    "seed": seed,
                    "step": step,
                    "task": task,
                    "metric": metric_name,
                    "value": float(value),
                    "json_path": str(jpath.relative_to(EXP)),
                })
    return rows


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--root", type=Path, default=EXP / "eval_results")
    p.add_argument("--out", type=Path, default=EXP / "analyze" / "eval_summary.csv")
    args = p.parse_args()

    if not args.root.exists():
        print(f"no eval_results at {args.root}")
        return

    all_rows: list[dict] = []
    for run_dir in sorted(args.root.iterdir()):
        if not run_dir.is_dir():
            continue
        rows = parse_run(run_dir)
        print(f"[{run_dir.name}] {len(rows)} metrics parsed")
        all_rows.extend(rows)

    if not all_rows:
        print("no rows parsed; check eval_results contents")
        return

    df = pd.DataFrame(all_rows)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.out, index=False)
    print(f"\n[done] wrote {len(df)} rows to {args.out}")
    print()
    # Pretty headline: accuracy per model on hellaswag
    headline = df[
        (df["task"] == "hellaswag")
        & (df["metric"].str.startswith("acc_norm"))
        & (~df["metric"].str.contains("stderr"))
    ]
    if not headline.empty:
        print("Hellaswag acc_norm per model:")
        for _, row in headline.sort_values("model_id").iterrows():
            tag = "[BASE]" if row["is_base"] else f"[seed{int(row['seed']):2d}]"
            print(f"  {tag} {row['model_id']:30s} acc_norm = {row['value']:.4f}")


if __name__ == "__main__":
    main()
