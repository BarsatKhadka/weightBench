#!/bin/bash
#SBATCH --job-name=lora_eval
#SBATCH --partition=gpuq
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --time=01:00:00
#SBATCH --output=logs/%x_%A_%a.out
#SBATCH --error=logs/%x_%A_%a.err

# Evaluate one LoRA adapter (final/) on hellaswag via lm-evaluation-harness.
# Usage (single):
#   sbatch --export=ALL,SEED=0 scripts/eval.sbatch
# Usage (array — all 10 seeds):
#   sbatch --array=0-9%6 scripts/eval.sbatch

set -euo pipefail

module purge
module load python/2025.12-2
module load cuda12.8/toolkit/12.8.1

source "${HOME}/weightBench/.venv/bin/activate"

cd "${HOME}/weightBench/weightBench/experiment1"
mkdir -p logs eval_results

SEED="${SEED:-${SLURM_ARRAY_TASK_ID:-0}}"
ADAPTER_DIR="${HOME}/weightBench/weightBench/experiment1/adapters/hellaswag_seed${SEED}/final"
MODEL_DIR="${HOME}/weightBench/weightBench/experiment1/models/Qwen2.5-7B"
OUT_DIR="${HOME}/weightBench/weightBench/experiment1/eval_results/hellaswag_seed${SEED}"

if [[ ! -d "${ADAPTER_DIR}" ]]; then
    echo "ERROR: adapter not found at ${ADAPTER_DIR}"
    exit 1
fi

echo "[eval] seed=${SEED} host=$(hostname)"
nvidia-smi --query-gpu=name,memory.total --format=csv

lm_eval \
    --model hf \
    --model_args pretrained=${MODEL_DIR},peft=${ADAPTER_DIR},dtype=bfloat16 \
    --tasks hellaswag \
    --batch_size 8 \
    --output_path "${OUT_DIR}" \
    --log_samples

echo "[done] $(date)"
