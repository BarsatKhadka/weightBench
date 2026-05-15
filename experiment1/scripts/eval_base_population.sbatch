#!/bin/bash
#SBATCH --job-name=eval_base_pop
#SBATCH --partition=gpuq
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --time=02:00:00
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err

# Evaluate the BASE Qwen2.5-7B on every task we're going to gate on.
# Required so quality_gate.py can compute (LoRA - base) per task.
#
# Hellaswag base is already done (see eval_summary.csv); we add the rest.
#
# Usage:
#   sbatch scripts/eval_base_population.sbatch

set -euo pipefail

module purge
module load python/2025.12-2
module load cuda12.8/toolkit/12.8.1

source "${HOME}/weightBench/.venv/bin/activate"

cd "${HOME}/weightBench/weightBench/experiment1"
mkdir -p logs eval_results

MODEL_DIR="${HOME}/weightBench/weightBench/experiment1/models/Qwen2.5-7B"

export PYTHONUNBUFFERED=1

for TASK in boolq arc_easy winogrande gsm8k; do
    OUT_DIR="${HOME}/weightBench/weightBench/experiment1/eval_results/${TASK}_base"
    if [[ -d "${OUT_DIR}" && -n "$(find "${OUT_DIR}" -name 'results*.json' 2>/dev/null | head -n1)" ]]; then
        echo "[skip] ${TASK}_base already evaluated"
        continue
    fi
    echo "[eval-base] task=${TASK}"
    lm_eval \
        --model hf \
        --model_args "pretrained=${MODEL_DIR},dtype=bfloat16" \
        --tasks "${TASK}" \
        --batch_size 8 \
        --output_path "${OUT_DIR}"
done

echo "[done] $(date)"
