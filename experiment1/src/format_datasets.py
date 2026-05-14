"""Convert each raw HF task into a single JSONL of {prompt, completion} pairs.

Output: experiment1/data/formatted/{task}.jsonl
Uses the train split only — eval is via lm-evaluation-harness later.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Callable, Iterable

from datasets import load_from_disk

RAW = Path(__file__).resolve().parents[1] / "data" / "raw"
OUT = Path(__file__).resolve().parents[1] / "data" / "formatted"
LETTERS = ["A", "B", "C", "D", "E"]


def _fmt_boolq(ex: dict) -> dict:
    prompt = (
        f"Passage: {ex['passage']}\n"
        f"Question: {ex['question']}\n"
        f"Answer (yes or no):"
    )
    completion = " yes" if ex["answer"] else " no"
    return {"prompt": prompt, "completion": completion}


def _fmt_piqa(ex: dict) -> dict:
    prompt = (
        f"Goal: {ex['goal']}\n"
        f"A. {ex['sol1']}\n"
        f"B. {ex['sol2']}\n"
        f"Which is more appropriate? Answer A or B:"
    )
    completion = " A" if ex["label"] == 0 else " B"
    return {"prompt": prompt, "completion": completion}


def _fmt_hellaswag(ex: dict) -> dict:
    """Continuation format — matches how lm-evaluation-harness scores hellaswag.

    lm_eval computes P(ending_i | context) for each candidate ending and picks
    the highest. So we train on (context -> correct_ending) directly. NO multiple
    choice menu in the prompt, NO letter prediction. This gives rich semantic
    gradient AND aligns training with eval.
    """
    correct_ending = ex["endings"][int(ex["label"])]
    prompt = f"{ex['activity_label']}: {ex['ctx']}"
    completion = f" {correct_ending}"
    return {"prompt": prompt, "completion": completion}


def _fmt_winogrande(ex: dict) -> dict:
    prompt = (
        f"Sentence: {ex['sentence']}\n"
        f"A. {ex['option1']}\n"
        f"B. {ex['option2']}\n"
        f"Which option correctly fills the blank? Answer A or B:"
    )
    completion = " A" if ex["answer"] == "1" else " B"
    return {"prompt": prompt, "completion": completion}


def _fmt_arc(ex: dict) -> dict:
    choices = ex["choices"]
    labels = choices["label"]
    texts = choices["text"]
    body = "\n".join(f"{lbl}. {txt}" for lbl, txt in zip(labels, texts))
    prompt = (
        f"Question: {ex['question']}\n{body}\n"
        f"Answer with a letter:"
    )
    completion = f" {ex['answerKey']}"
    return {"prompt": prompt, "completion": completion}


def _fmt_openbookqa(ex: dict) -> dict:
    choices = ex["choices"]
    labels = choices["label"]
    texts = choices["text"]
    body = "\n".join(f"{lbl}. {txt}" for lbl, txt in zip(labels, texts))
    prompt = (
        f"Question: {ex['question_stem']}\n{body}\n"
        f"Answer with a letter:"
    )
    completion = f" {ex['answerKey']}"
    return {"prompt": prompt, "completion": completion}


def _fmt_siqa(ex: dict) -> dict:
    body = (
        f"A. {ex['answerA']}\n"
        f"B. {ex['answerB']}\n"
        f"C. {ex['answerC']}"
    )
    prompt = (
        f"Context: {ex['context']}\n"
        f"Question: {ex['question']}\n{body}\n"
        f"Answer with a letter:"
    )
    completion = f" {LETTERS[int(ex['label']) - 1]}"
    return {"prompt": prompt, "completion": completion}


def _fmt_gsm8k(ex: dict) -> dict:
    prompt = f"Question: {ex['question']}\nAnswer:"
    completion = " " + ex["answer"]
    return {"prompt": prompt, "completion": completion}


def _fmt_mbpp(ex: dict) -> dict:
    tests = "\n".join(ex.get("test_list", []))
    prompt = (
        f"You are an expert Python programmer.\n"
        f"Problem: {ex['text']}\n"
        f"Your code must pass the following tests:\n{tests}\n"
        f"```python\n"
    )
    completion = ex["code"] + "\n```"
    return {"prompt": prompt, "completion": completion}


FORMATTERS: dict[str, tuple[Callable[[dict], dict], str]] = {
    "boolq":         (_fmt_boolq,      "train"),
    "piqa":          (_fmt_piqa,       "train"),
    "hellaswag":     (_fmt_hellaswag,  "train"),
    "winogrande":    (_fmt_winogrande, "train"),
    "arc_easy":      (_fmt_arc,        "train"),
    "arc_challenge": (_fmt_arc,        "train"),
    "openbookqa":    (_fmt_openbookqa, "train"),
    "siqa":          (_fmt_siqa,       "train"),
    "gsm8k":         (_fmt_gsm8k,      "train"),
    "mbpp":          (_fmt_mbpp,       "train"),
}


def _write_jsonl(path: Path, rows: Iterable[dict]) -> int:
    n = 0
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
            n += 1
    return n


def format_task(task_id: str, raw_dir: Path, out_dir: Path) -> int:
    fmt, split = FORMATTERS[task_id]
    ds = load_from_disk(str(raw_dir / task_id))
    if split not in ds:
        # MBPP "full" config has only one split ("train" missing? use the only key)
        split = list(ds.keys())[0]
    rows = (fmt(ex) for ex in ds[split])
    out_path = out_dir / f"{task_id}.jsonl"
    return _write_jsonl(out_path, rows)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--raw", type=Path, default=RAW)
    p.add_argument("--out", type=Path, default=OUT)
    p.add_argument("--only", nargs="*", help="Subset of task ids.")
    args = p.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    tasks = args.only or list(FORMATTERS.keys())
    for task_id in tasks:
        if task_id not in FORMATTERS:
            print(f"[skip] unknown task: {task_id}")
            continue
        n = format_task(task_id, args.raw, args.out)
        print(f"[ok] {task_id}: {n} examples → {args.out / (task_id + '.jsonl')}")


if __name__ == "__main__":
    main()
