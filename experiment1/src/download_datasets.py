"""Download the 10 HF training datasets into experiment1/data/raw/.

Mirrors dataset/dataset.md. Idempotent — HF datasets caches by hash.
Run on a CPU compute node (login can't handle the I/O).

Robustness:
- Each task in its own try/except so one failure doesn't kill the rest.
- Idempotent skip check uses presence of the task's save_to_disk root.
- Final summary lists which tasks succeeded, which failed, why.
"""
from __future__ import annotations

import argparse
import traceback
from pathlib import Path

from datasets import load_dataset

# (task_id, hf_path, hf_config_or_None, trust_remote_code)
# Some HF datasets ship with a loading script and require trust_remote_code=True.
TASKS = [
    ("boolq",         "google/boolq",                   None,             False),
    ("piqa",          "ybisk/piqa",                     None,             True),
    ("hellaswag",     "Rowan/hellaswag",                None,             True),
    ("winogrande",    "allenai/winogrande",             "winogrande_xl",  True),
    ("arc_easy",      "allenai/ai2_arc",                "ARC-Easy",       False),
    ("arc_challenge", "allenai/ai2_arc",                "ARC-Challenge",  False),
    ("openbookqa",    "allenai/openbookqa",             "main",           False),
    ("siqa",          "allenai/social_i_qa",            None,             True),
    ("gsm8k",         "openai/gsm8k",                   "main",           False),
    ("mbpp",          "google-research-datasets/mbpp",  "full",           False),
]

DEFAULT_OUT = Path(__file__).resolve().parents[1] / "data" / "raw"


def already_present(dest: Path) -> bool:
    """Return True if dest looks like a successful save_to_disk output.

    save_to_disk creates either a dataset_info.json at the root (single Dataset)
    or a dataset_dict.json (DatasetDict). Either is fine.
    """
    if not dest.is_dir():
        return False
    if (dest / "dataset_dict.json").exists():
        return True
    if (dest / "dataset_info.json").exists():
        return True
    # Some HF versions nest one level deep per split.
    if any((dest / split).is_dir() and (dest / split / "dataset_info.json").exists()
           for split in ("train", "validation", "test")):
        return True
    return False


def fetch_one(task_id: str, hf_path: str, hf_config: str | None,
              trust_remote_code: bool, out_root: Path) -> tuple[bool, str]:
    dest = out_root / task_id
    if already_present(dest):
        return True, f"already present at {dest}"
    print(f"[fetch] {task_id}  ({hf_path}, config={hf_config}, trust={trust_remote_code})")
    ds = load_dataset(
        hf_path,
        hf_config,
        trust_remote_code=trust_remote_code,
    )
    dest.parent.mkdir(parents=True, exist_ok=True)
    # Wipe partial leftovers so save_to_disk doesn't refuse.
    if dest.exists() and not already_present(dest):
        import shutil
        shutil.rmtree(dest)
    ds.save_to_disk(str(dest))
    return True, f"saved to {dest}"


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--out", type=Path, default=DEFAULT_OUT)
    p.add_argument("--only", nargs="*", help="Subset of task ids to fetch.")
    p.add_argument("--retry", action="store_true",
                   help="Retry tasks even if already_present says they're done.")
    args = p.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    selected = set(args.only) if args.only else None

    results: list[tuple[str, bool, str]] = []
    for task_id, hf_path, hf_config, trust in TASKS:
        if selected and task_id not in selected:
            continue
        if args.retry:
            dest = args.out / task_id
            if dest.exists():
                import shutil
                shutil.rmtree(dest)
        try:
            ok, msg = fetch_one(task_id, hf_path, hf_config, trust, args.out)
            results.append((task_id, ok, msg))
            print(f"  -> {msg}")
        except Exception as e:
            tb = traceback.format_exc(limit=2)
            results.append((task_id, False, f"{type(e).__name__}: {e}"))
            print(f"  !! {task_id} FAILED: {type(e).__name__}: {e}")
            print(tb)

    print("\n=== summary ===")
    for task_id, ok, msg in results:
        flag = "OK " if ok else "ERR"
        print(f"  [{flag}] {task_id:15s} {msg}")
    n_ok = sum(1 for _, ok, _ in results if ok)
    print(f"\n{n_ok}/{len(results)} tasks succeeded")


if __name__ == "__main__":
    main()
