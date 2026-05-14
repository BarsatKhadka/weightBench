"""Train one LoRA on one (task, seed) and save checkpoints + final adapter.

Population layer: run this N times for N (task, seed) combinations — serially
or as an HPC job array. Hyperparams come from configs/train.yaml; CLI flags
override task/seed only (so weight-space coords stay comparable across pool).

Example:
    python src/train_lora.py --task boolq --seed 0
    python src/train_lora.py --task gsm8k --seed 2 --config configs/train.yaml
"""
from __future__ import annotations

import argparse
import json
import os
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import torch
import yaml
from datasets import Dataset
from peft import LoraConfig, get_peft_model
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    DataCollatorForSeq2Seq,
    Trainer,
    TrainingArguments,
    set_seed,
)

EXP_ROOT = Path(__file__).resolve().parents[1]


# ---------------------------------------------------------------------------
# config loading
# ---------------------------------------------------------------------------

@dataclass
class Cfg:
    raw: dict

    def __getitem__(self, k: str) -> Any:
        return self.raw[k]


def load_cfg(path: Path) -> Cfg:
    with path.open("r", encoding="utf-8") as f:
        return Cfg(yaml.safe_load(f))


# ---------------------------------------------------------------------------
# data
# ---------------------------------------------------------------------------

def _read_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def build_dataset(task: str, formatted_dir: Path, tokenizer, max_seq_len: int) -> Dataset:
    """Tokenize with COMPLETION-ONLY LOSS.

    Standard SFT practice: the loss should be computed only on the completion
    tokens, not the prompt. We achieve this by setting labels to -100 (ignored
    by cross-entropy) on prompt tokens, and to input_ids on completion tokens.

    Without this, the loss is dominated by prompt-token prediction (which the
    base model already does fine), and the LoRA's gradient signal on the actual
    answer is tiny. Symptom: training loss barely drops over many steps.
    """
    path = formatted_dir / f"{task}.jsonl"
    rows = _read_jsonl(path)

    def tokenize(ex: dict) -> dict:
        prompt_ids = tokenizer(ex["prompt"], add_special_tokens=False)["input_ids"]
        completion_ids = tokenizer(
            ex["completion"] + tokenizer.eos_token, add_special_tokens=False
        )["input_ids"]

        input_ids = prompt_ids + completion_ids
        # Truncate from the right if too long; keep at least the completion.
        if len(input_ids) > max_seq_len:
            overflow = len(input_ids) - max_seq_len
            # Prefer truncating prompt over completion.
            if overflow < len(prompt_ids):
                prompt_ids = prompt_ids[overflow:]
                input_ids = prompt_ids + completion_ids
            else:
                input_ids = input_ids[-max_seq_len:]
                prompt_ids = []  # everything left is completion or close to it

        labels = [-100] * len(prompt_ids) + list(completion_ids)
        assert len(labels) == len(input_ids), (len(labels), len(input_ids))

        return {
            "input_ids": input_ids,
            "attention_mask": [1] * len(input_ids),
            "labels": labels,
        }

    ds = Dataset.from_list(rows).map(
        tokenize,
        remove_columns=["prompt", "completion"],
        desc=f"tokenize:{task}",
    )
    return ds


# ---------------------------------------------------------------------------
# model
# ---------------------------------------------------------------------------

def _resolve_model_path(model_cfg: dict) -> str:
    local = EXP_ROOT / model_cfg["local_dir"]
    if (local / "config.json").exists():
        return str(local)
    return model_cfg["name_or_path"]


def build_model_and_tokenizer(model_cfg: dict, lora_cfg: dict):
    model_path = _resolve_model_path(model_cfg)
    print(f"[model] loading from {model_path}")

    tokenizer = AutoTokenizer.from_pretrained(
        model_path,
        trust_remote_code=model_cfg.get("trust_remote_code", False),
    )
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    dtype = getattr(torch, model_cfg.get("dtype", "bfloat16"))
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        torch_dtype=dtype,
        trust_remote_code=model_cfg.get("trust_remote_code", False),
    )
    model.config.use_cache = False

    peft_cfg = LoraConfig(
        r=lora_cfg["r"],
        lora_alpha=lora_cfg["alpha"],
        lora_dropout=lora_cfg["dropout"],
        bias=lora_cfg.get("bias", "none"),
        target_modules=lora_cfg["target_modules"],
        task_type="CAUSAL_LM",
    )
    model = get_peft_model(model, peft_cfg)
    model.print_trainable_parameters()
    return model, tokenizer


# ---------------------------------------------------------------------------
# seed
# ---------------------------------------------------------------------------

def seed_all(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    set_seed(seed)


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--task", required=True)
    p.add_argument("--seed", type=int, required=True)
    p.add_argument("--config", type=Path, default=EXP_ROOT / "configs" / "train.yaml")
    p.add_argument("--max-steps", type=int, default=None, help="Override config.train.max_steps.")
    args = p.parse_args()

    cfg = load_cfg(args.config)
    seed_all(args.seed)

    train_cfg = cfg["train"]
    if args.max_steps is not None:
        train_cfg["max_steps"] = args.max_steps

    model, tokenizer = build_model_and_tokenizer(cfg["model"], cfg["lora"])

    formatted_dir = EXP_ROOT / cfg["data"]["formatted_dir"]
    ds = build_dataset(args.task, formatted_dir, tokenizer, train_cfg["max_seq_len"])
    print(f"[data] {args.task}: {len(ds)} examples")

    out_dir = EXP_ROOT / cfg["data"]["output_root"] / f"{args.task}_seed{args.seed}"
    out_dir.mkdir(parents=True, exist_ok=True)

    ckpt_cfg = cfg["checkpoint"]
    log_cfg = cfg["logging"]

    targs = TrainingArguments(
        output_dir=str(out_dir),
        per_device_train_batch_size=train_cfg["per_device_batch_size"],
        gradient_accumulation_steps=train_cfg["grad_accum_steps"],
        learning_rate=train_cfg["learning_rate"],
        lr_scheduler_type=train_cfg["lr_scheduler"],
        warmup_ratio=train_cfg["warmup_ratio"],
        weight_decay=train_cfg["weight_decay"],
        max_steps=train_cfg["max_steps"],
        bf16=train_cfg.get("bf16", True),
        gradient_checkpointing=train_cfg.get("gradient_checkpointing", True),
        logging_steps=log_cfg["log_every"],
        save_strategy="steps",
        save_steps=ckpt_cfg["save_every"],
        save_total_limit=ckpt_cfg.get("save_total_limit"),
        report_to=log_cfg.get("report_to", "none"),
        seed=args.seed,
        data_seed=args.seed,
        dataloader_num_workers=2,
        remove_unused_columns=False,
    )

    collator = DataCollatorForSeq2Seq(
        tokenizer=tokenizer,
        padding=True,
        label_pad_token_id=-100,
        pad_to_multiple_of=8,
    )
    trainer = Trainer(
        model=model,
        args=targs,
        train_dataset=ds,
        data_collator=collator,
    )

    trainer.train()

    if ckpt_cfg.get("save_final", True):
        final_dir = out_dir / "final"
        trainer.save_model(str(final_dir))
        tokenizer.save_pretrained(str(final_dir))
        print(f"[done] adapter saved → {final_dir}")

    # Stamp run config for reproducibility
    with (out_dir / "run_config.json").open("w", encoding="utf-8") as f:
        json.dump(
            {"task": args.task, "seed": args.seed, "config": cfg.raw},
            f,
            indent=2,
        )


if __name__ == "__main__":
    main()
