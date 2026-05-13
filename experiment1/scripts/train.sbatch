#!/bin/bash
#SBATCH --job-name=lora_train
#SBATCH --partition=gpuq
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --time=04:00:00
#SBATCH --output=logs/%x_%A_%a.out
#SBATCH --error=logs/%x_%A_%a.err

# Magnolia (Ole Miss MCSR) — L40S nodes (45-50), 46GB VRAM, bf16 native.
# Usage (single run):
#   sbatch --export=ALL,TASK=boolq,SEED=0 scripts/train.sbatch
# Usage (array — 10 tasks × 5 seeds = 50 jobs, max 6 concurrent = 1 per GPU node):
#   sbatch --array=0-49%6 scripts/train.sbatch
#
# In array mode, TASK and SEED are derived from $SLURM_ARRAY_TASK_ID below.

set -euo pipefail

module purge
module load python/2025.12-2
module load cuda12.8/toolkit/12.8.1

source "${HOME}/weightBench/.venv/bin/activate"

cd "${HOME}/weightBench/weightBench/experiment1"
mkdir -p logs

TASKS=(boolq piqa hellaswag winogrande arc_easy arc_challenge openbookqa siqa gsm8k mbpp)
SEEDS=(0 1 2 3 4)

if [[ -n "${SLURM_ARRAY_TASK_ID:-}" ]]; then
    # Array mode: 0..49 → (task_idx, seed_idx)
    IDX=${SLURM_ARRAY_TASK_ID}
    TASK_IDX=$(( IDX / ${#SEEDS[@]} ))
    SEED_IDX=$(( IDX % ${#SEEDS[@]} ))
    TASK="${TASKS[$TASK_IDX]}"
    SEED="${SEEDS[$SEED_IDX]}"
fi

: "${TASK:?TASK must be set via --export=ALL,TASK=... or array index}"
: "${SEED:?SEED must be set via --export=ALL,SEED=... or array index}"

echo "[start] $(date) task=${TASK} seed=${SEED} host=$(hostname)"
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv

python src/train_lora.py --task "${TASK}" --seed "${SEED}"

echo "[done]  $(date)"
