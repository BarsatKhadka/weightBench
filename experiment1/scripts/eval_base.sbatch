#!/bin/bash
#SBATCH --job-name=lora_eval_base
#SBATCH --partition=gpuq
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --time=01:00:00
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err

# Evaluate the BASE Qwen2.5-7B (no adapter) on hellaswag — establishes the
# "before fine-tuning" baseline that every per-seed accuracy is compared against.

set -euo pipefail

module purge
module load python/2025.12-2
module load cuda12.8/toolkit/12.8.1

source "${HOME}/weightBench/.venv/bin/activate"

cd "${HOME}/weightBench/weightBench/experiment1"
mkdir -p logs eval_results

MODEL_DIR="${HOME}/weightBench/weightBench/experiment1/models/Qwen2.5-7B"
OUT_DIR="${HOME}/weightBench/weightBench/experiment1/eval_results/hellaswag_base"

export PYTHONUNBUFFERED=1

echo "[eval base] $(date) host=$(hostname)"
nvidia-smi --query-gpu=name,memory.total --format=csv

lm_eval \
    --model hf \
    --model_args pretrained=${MODEL_DIR},dtype=bfloat16 \
    --tasks hellaswag \
    --batch_size 8 \
    --output_path "${OUT_DIR}"

echo "[done] $(date)"
