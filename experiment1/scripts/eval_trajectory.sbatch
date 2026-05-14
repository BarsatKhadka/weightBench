#!/bin/bash
#SBATCH --job-name=lora_eval_traj
#SBATCH --partition=gpuq
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --time=01:00:00
#SBATCH --output=logs/%x_%A_%a.out
#SBATCH --error=logs/%x_%A_%a.err

# Evaluate one (seed, checkpoint) combination on hellaswag.
# The array index encodes both: index = seed_idx * len(steps) + step_idx
#
# Usage (default: 5 seeds × 8 strategic steps = 40 jobs):
#   sbatch --array=0-39%5 scripts/eval_trajectory.sbatch
#
# Strategic steps cover early lock-in, mid-training, endpoint.

set -euo pipefail

module purge
module load python/2025.12-2
module load cuda12.8/toolkit/12.8.1

source "${HOME}/weightBench/.venv/bin/activate"

cd "${HOME}/weightBench/weightBench/experiment1"
mkdir -p logs eval_results

# 5 seeds × 8 strategic steps
SEEDS=(0 1 2 3 4)
STEPS=(50 100 200 400 800 1200 1600 2000)
N_STEPS=${#STEPS[@]}

IDX="${SLURM_ARRAY_TASK_ID}"
SEED_IDX=$(( IDX / N_STEPS ))
STEP_IDX=$(( IDX % N_STEPS ))
SEED="${SEEDS[$SEED_IDX]}"
STEP="${STEPS[$STEP_IDX]}"

ADAPTER_DIR="${HOME}/weightBench/weightBench/experiment1/adapters/hellaswag_seed${SEED}/checkpoint-${STEP}"
MODEL_DIR="${HOME}/weightBench/weightBench/experiment1/models/Qwen2.5-7B"
OUT_DIR="${HOME}/weightBench/weightBench/experiment1/eval_results/hellaswag_seed${SEED}_step${STEP}"

if [[ ! -d "${ADAPTER_DIR}" ]]; then
    echo "ERROR: adapter not found at ${ADAPTER_DIR}"
    exit 1
fi

export PYTHONUNBUFFERED=1

echo "[eval-traj] seed=${SEED} step=${STEP} host=$(hostname)"
nvidia-smi --query-gpu=name,memory.total --format=csv

lm_eval \
    --model hf \
    --model_args pretrained=${MODEL_DIR},peft=${ADAPTER_DIR},dtype=bfloat16 \
    --tasks hellaswag \
    --batch_size 8 \
    --output_path "${OUT_DIR}"

echo "[done] $(date)"
