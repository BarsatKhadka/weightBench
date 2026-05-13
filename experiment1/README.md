# experiment1 — Qwen2.5-7B LoRA Trajectory Pipeline

First real-scale run for the LoRA trajectory thesis program. Bridges from the
Qwen-0.5B archive results (`thesis_plan/test_experiments_archive.md`) to a
7B base. Targets are E1 (endpoint C1: same-task subspace collapse) and E2
(trajectory geometry: step-K lock-in, σ-shrink across training).

## Pipeline order

1. `python src/download_model.py`         — pulls Qwen2.5-7B into `models/Qwen2.5-7B/`
2. `python src/download_datasets.py`      — pulls 10 HF tasks into `data/raw/`
3. `python src/format_datasets.py`        — formats each task into instruction
                                            JSONL at `data/formatted/{task}.jsonl`
4. `python src/train_lora.py --task boolq --seed 0`
                                          — trains one LoRA, saves adapter +
                                            checkpoints under `adapters/{task}_seed{n}/`

Run (3) before (4). (1) and (2) are independent and can run in parallel.

## Conventions

- LoRA config is canonical per `plan.md`: r=16, α=32, dropout=0.05,
  target_modules = all 7 linear (q,k,v,o,gate,up,down). Override via
  `configs/train.yaml` only if you have a reason — same-task collapse
  needs identical parameterization across the pool to be comparable.
- Checkpoints saved every `save_every` steps (default 50) for E2 trajectory.
- bf16 mixed precision (Qwen-0.5B archive used bf16; fp16 NaNs on long seq).
- Single GPU per run. Population = 10 tasks × 5 seeds = 50 LoRAs, trained
  serially or via job-array on HPC.

## Directory layout

```
experiment1/
├── README.md
├── configs/
│   └── train.yaml            # hyperparams, paths
├── src/
│   ├── download_model.py
│   ├── download_datasets.py
│   ├── format_datasets.py
│   └── train_lora.py
├── models/Qwen2.5-7B/        # populated by step 1
├── data/
│   ├── raw/                  # HF dataset cache (step 2)
│   └── formatted/            # per-task JSONL (step 3)
└── adapters/                 # per-LoRA outputs (step 4)
    └── {task}_seed{n}/
        ├── final/
        ├── checkpoint-50/
        ├── checkpoint-100/
        └── ...
```
