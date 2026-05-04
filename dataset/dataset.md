# Training Tasks and Evaluation Benchmarks

## Design: One LoRA Per Task (Specialist)

Each LoRA is trained on a single task's training split. Population size: **10 tasks × 5 seeds = 50 LoRAs**.

Evaluation: every LoRA is scored on all 10 tasks using `lm-evaluation-harness`. That 10-dimensional score vector is the behavioral coordinate.

---

## Training Tasks

### 8-Task Commonsense Suite
Standard in recent LoRA papers (DoRA, ReFT, HydraLoRA — NeurIPS/ICLR 2024-2025).

| Task | HuggingFace Dataset | Type |
|---|---|---|
| BoolQ | `google/boolq` | yes/no reading comprehension |
| PIQA | `piqa` | physical commonsense |
| HellaSwag | `hellaswag` | sentence completion |
| WinoGrande | `winogrande` | coreference reasoning |
| ARC-Easy | `allenai/ai2_arc` (ARC-Easy) | science MCQ |
| ARC-Challenge | `allenai/ai2_arc` (ARC-Challenge) | harder science MCQ |
| OpenBookQA | `allenai/openbookqa` | knowledge + reasoning |
| SIQA | `social_i_qa` | social commonsense |

### Math + Code
| Task | HuggingFace Dataset | Type |
|---|---|---|
| GSM8K | `gsm8k` | grade-school math reasoning |
| MBPP | `mbpp` | Python code generation |

---

## Evaluation Suite (Behavioral Coordinate)

Run `lm-evaluation-harness` on every LoRA across all 10 tasks:

```bash
lm_eval --model hf \
  --model_args pretrained=<base_model>,peft=<lora_path> \
  --tasks boolq,piqa,hellaswag,winogrande,arc_easy,arc_challenge,openbookqa,social_iqa,gsm8k,mbpp \
  --output_path results/<lora_id>.json
```

Each LoRA produces a 10-dim behavioral coordinate vector:
```
[boolq_acc, piqa_acc, hellaswag_acc, winogrande_acc, arc_easy_acc, arc_challenge_acc, openbookqa_acc, siqa_acc, gsm8k_acc, mbpp_pass@1]
```

---

## LoRA Training Configuration (Fixed Across All Tasks)

Must be identical across all 50 LoRAs so weight-space coordinates are comparable.

| Parameter | Value |
|---|---|
| Base model | Qwen2.5-7B |
| Rank (r) | 8 |
| Alpha | 16 |
| Target modules | `q_proj, v_proj, up_proj, down_proj` |
| Seeds | 0, 1, 2, 3, 4 |
| Dropout | 0.05 |

> **Why these target modules:** AdaLoRA shows FFN layers (`up_proj`, `down_proj`) carry more task-relevant singular values than attention alone. Including them gives richer weight-space geometry.

---

## Directory Structure

```
dataset/
  dataset.md          # this file
  raw/                # downloaded HF datasets cached locally
results/
  lora_<task>_seed<n>/
    adapter_model.bin  # saved LoRA weights
    eval.json          # 10-dim behavioral coordinate
```
