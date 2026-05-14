#!/bin/bash
#SBATCH --job-name=lora_hellaswag
#SBATCH --partition=gpuq
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --time=04:00:00
#SBATCH --output=logs/%x_%A_%a.out
#SBATCH --error=logs/%x_%A_%a.err

# 10-seed array on hellaswag. Same hyperparams across seeds (only the
# RNG seed differs) so the resulting LoRA pool's weight-space coordinates
# are directly comparable.
#
# Usage:
#   sbatch --array=0-9%6 scripts/train_hellaswag_array.sbatch
# (%6 caps concurrent jobs at 6 = one per GPU node, be polite.)

set -euo pipefail

module purge
module load python/2025.12-2
module load cuda12.8/toolkit/12.8.1

source "${HOME}/weightBench/.venv/bin/activate"

cd "${HOME}/weightBench/weightBench/experiment1"
mkdir -p logs

SEED="${SLURM_ARRAY_TASK_ID:-0}"

# Force unbuffered stdout so progress lines show up live in slurm logs
# (without this, Python buffers and you see nothing until job end).
export PYTHONUNBUFFERED=1
export TRANSFORMERS_VERBOSITY=info

echo "[start] $(date) task=hellaswag seed=${SEED} host=$(hostname)"
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv

python -u src/train_lora.py --task hellaswag --seed "${SEED}"

echo "[done]  $(date)"
