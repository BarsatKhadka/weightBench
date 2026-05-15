#!/bin/bash
#SBATCH --job-name=lora_pop
#SBATCH --partition=gpuq
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --time=04:00:00
#SBATCH --output=logs/%x_%A_%a.out
#SBATCH --error=logs/%x_%A_%a.err

# Cross-task population trainer for the "knowledge is a PATH, not a POINT"
# headline. Trains the same LoRA recipe (configs/train.yaml) on 4 additional
# tasks x 3 seeds = 12 LoRAs. Combined with the 5 hellaswag seeds we already
# have, that gives a 5-task pool for within-task vs between-task d_G analysis.
#
# Job-array index 0..11 decodes to (task, seed):
#       index   task              seed
#       0..2    boolq             0,1,2
#       3..5    arc_easy          0,1,2
#       6..8    winogrande        0,1,2
#       9..11   gsm8k             0,1,2
#
# Usage:
#   sbatch --array=0-11%6 scripts/train_population_array.sbatch
# (%6 caps concurrent jobs to be polite to the gpuq.)
#
# Resume-friendly: jobs that already produced .../final/adapter_model.safetensors
# exit immediately without retraining.

set -euo pipefail

module purge
module load python/2025.12-2
module load cuda12.8/toolkit/12.8.1

source "${HOME}/weightBench/.venv/bin/activate"

cd "${HOME}/weightBench/weightBench/experiment1"
mkdir -p logs

export PYTHONUNBUFFERED=1
export TRANSFORMERS_VERBOSITY=info

TASKS=(boolq arc_easy winogrande gsm8k)
SEEDS=(0 1 2)
N_SEEDS=${#SEEDS[@]}

IDX="${SLURM_ARRAY_TASK_ID:-0}"
TASK_IDX=$((IDX / N_SEEDS))
SEED_IDX=$((IDX % N_SEEDS))
TASK="${TASKS[$TASK_IDX]}"
SEED="${SEEDS[$SEED_IDX]}"

echo "[start] $(date) idx=${IDX} task=${TASK} seed=${SEED} host=$(hostname)"
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv

FINAL_ADAPTER="adapters/${TASK}_seed${SEED}/final/adapter_model.safetensors"
if [[ -f "${FINAL_ADAPTER}" ]]; then
    echo "[skip] ${FINAL_ADAPTER} already exists -- nothing to do"
    exit 0
fi

# Verify the formatted data exists before launching the (~2h) training.
if [[ ! -f "data/formatted/${TASK}.jsonl" ]]; then
    echo "[fatal] data/formatted/${TASK}.jsonl missing"
    echo "  run on the login node:"
    echo "    python src/format_datasets.py --only ${TASK}"
    exit 1
fi

python -u src/train_lora.py --task "${TASK}" --seed "${SEED}"

echo "[done]  $(date) task=${TASK} seed=${SEED}"
