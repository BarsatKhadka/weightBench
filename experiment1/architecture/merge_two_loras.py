"""Merge two LoRAs (hellaswag + boolq) into a single combined adapter.

Uses PEFT's add_weighted_adapter — supports linear combination of LoRA factors.
Output: adapters/combined_hellaswag_boolq/ ready for lm_eval.

Mini-run 1 of the Accretive LM pilot:
  Are two same-base task LoRAs compositional under naive 50/50 stacking,
  or do they catastrophically interfere?

Run on magnolia (CPU is fine, but easier on a GPU node since the base is bf16):
    cd $HOME/weightBench/weightBench/experiment1
    source $HOME/weightBench/.venv/bin/activate
    python architecture/merge_two_loras.py
"""
from __future__ import annotations

from pathlib import Path

import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM

EXP = Path(__file__).resolve().parents[1]


def main() -> None:
    base_path = EXP / "models" / "Qwen2.5-7B"
    hellaswag_path = EXP / "adapters" / "hellaswag_seed0" / "final"
    boolq_path = EXP / "adapters" / "boolq_seed0" / "final"
    out_path = EXP / "adapters" / "combined_hellaswag_boolq" / "final"

    print(f"loading base from {base_path}")
    base = AutoModelForCausalLM.from_pretrained(
        str(base_path), torch_dtype=torch.bfloat16
    )

    print(f"loading hellaswag adapter from {hellaswag_path}")
    model = PeftModel.from_pretrained(base, str(hellaswag_path), adapter_name="hellaswag")

    print(f"loading boolq adapter from {boolq_path}")
    model.load_adapter(str(boolq_path), adapter_name="boolq")

    print("merging with 50/50 weighting -> 'combined'")
    model.add_weighted_adapter(
        adapters=["hellaswag", "boolq"],
        weights=[0.5, 0.5],
        adapter_name="combined",
        combination_type="linear",
    )

    print(f"saving combined adapter to {out_path}")
    model.set_adapter("combined")
    out_path.mkdir(parents=True, exist_ok=True)
    model.save_pretrained(str(out_path.parent), selected_adapters=["combined"])

    print("done.")
    print(f"to eval: lm_eval --model hf "
          f"--model_args pretrained={base_path},peft={out_path},dtype=bfloat16 "
          f"--tasks hellaswag,boolq --batch_size 8")


if __name__ == "__main__":
    main()
