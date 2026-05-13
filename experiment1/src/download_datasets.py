"""Download the 10 HF training datasets into experiment1/data/raw/.

Mirrors dataset/dataset.md. Idempotent — HF datasets caches by hash.
Run on HPC or any node with internet; no GPU required.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from datasets import load_dataset

# (task_id, hf_path, hf_config_or_None)
TASKS = [
    ("boolq",         "google/boolq",        None),
    ("piqa",          "ybisk/piqa",          None),
    ("hellaswag",     "Rowan/hellaswag",     None),
    ("winogrande",    "allenai/winogrande",  "winogrande_xl"),
    ("arc_easy",      "allenai/ai2_arc",     "ARC-Easy"),
    ("arc_challenge", "allenai/ai2_arc",     "ARC-Challenge"),
    ("openbookqa",    "allenai/openbookqa",  "main"),
    ("siqa",          "allenai/social_i_qa", None),
    ("gsm8k",         "openai/gsm8k",        "main"),
    ("mbpp",          "google-research-datasets/mbpp", "full"),
]

DEFAULT_OUT = Path(__file__).resolve().parents[1] / "data" / "raw"


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--out", type=Path, default=DEFAULT_OUT)
    p.add_argument("--only", nargs="*", help="Subset of task ids to fetch.")
    args = p.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    selected = set(args.only) if args.only else None

    for task_id, hf_path, hf_config in TASKS:
        if selected and task_id not in selected:
            continue
        dest = args.out / task_id
        if (dest / "dataset_info.json").exists() or any(dest.glob("**/dataset_info.json")):
            print(f"[skip] {task_id} already at {dest}")
            continue
        print(f"[fetch] {task_id}  ({hf_path}, {hf_config})")
        ds = load_dataset(hf_path, hf_config, trust_remote_code=True)
        ds.save_to_disk(str(dest))
    print("done.")


if __name__ == "__main__":
    main()
