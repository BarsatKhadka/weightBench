#!/bin/bash
#SBATCH --job-name=eval_pop
#SBATCH --partition=gpuq
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --time=01:30:00
#SBATCH --output=logs/%x_%A_%a.out
#SBATCH --error=logs/%x_%A_%a.err

# Evaluate every (task, seed) LoRA on its own task via lm-evaluation-harness.
# We need this so we can GATE the geometric analysis on actual LoRA quality:
# if a LoRA didn't beat the base, its trajectory geometry is suspect.
#
# Array index 0..11 -> (task, seed):
#   0..2    boolq             0,1,2
#   3..5    arc_easy          0,1,2
#   6..8    winogrande        0,1,2
#   9..11   gsm8k             0,1,2
#
# (Hellaswag was already evaluated; rerun with the hellaswag sbatch if needed.)
#
# Usage:
#   sbatch --array=0-11%6 scripts/eval_population_array.sbatch

set -euo pipefail

module purge
module load python/2025.12-2
module load cuda12.8/toolkit/12.8.1

source "${HOME}/weightBench/.venv/bin/activate"

cd "${HOME}/weightBench/weightBench/experiment1"
mkdir -p logs eval_results

TASKS=(boolq arc_easy winogrande gsm8k)
SEEDS=(0 1 2)
N_SEEDS=${#SEEDS[@]}

IDX="${SLURM_ARRAY_TASK_ID:-0}"
TASK_IDX=$((IDX / N_SEEDS))
SEED_IDX=$((IDX % N_SEEDS))
TASK="${TASKS[$TASK_IDX]}"
SEED="${SEEDS[$SEED_IDX]}"

# lm-evaluation-harness task ids (mostly match our internal names)
declare -A LMEVAL_TASK
LMEVAL_TASK[boolq]=boolq
LMEVAL_TASK[arc_easy]=arc_easy
LMEVAL_TASK[winogrande]=winogrande
LMEVAL_TASK[gsm8k]=gsm8k

LM_TASK="${LMEVAL_TASK[$TASK]}"

ADAPTER_DIR="${HOME}/weightBench/weightBench/experiment1/adapters/${TASK}_seed${SEED}/final"
MODEL_DIR="${HOME}/weightBench/weightBench/experiment1/models/Qwen2.5-7B"
OUT_DIR="${HOME}/weightBench/weightBench/experiment1/eval_results/${TASK}_seed${SEED}"

if [[ ! -d "${ADAPTER_DIR}" ]]; then
    echo "[skip] adapter not found at ${ADAPTER_DIR} (train hasn't finished?)"
    exit 0
fi

if [[ -d "${OUT_DIR}" && -n "$(find "${OUT_DIR}" -name 'results*.json' 2>/dev/null | head -n1)" ]]; then
    echo "[skip] eval already present in ${OUT_DIR}"
    exit 0
fi

export PYTHONUNBUFFERED=1

echo "[eval] task=${TASK} seed=${SEED} lm_eval_task=${LM_TASK} host=$(hostname)"
nvidia-smi --query-gpu=name,memory.total --format=csv

lm_eval \
    --model hf \
    --model_args "pretrained=${MODEL_DIR},peft=${ADAPTER_DIR},dtype=bfloat16" \
    --tasks "${LM_TASK}" \
    --batch_size 8 \
    --output_path "${OUT_DIR}" \
    --log_samples

echo "[done] $(date) task=${TASK} seed=${SEED}"
