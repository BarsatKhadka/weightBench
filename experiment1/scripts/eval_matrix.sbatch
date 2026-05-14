#!/bin/bash
#SBATCH --job-name=eval_matrix
#SBATCH --partition=gpuq
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --time=02:00:00
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err

# Mini-run pilot for Accretive LM:
#   Eval each of {hellaswag-only, boolq-only, combined} on each of {hellaswag, boolq}
#   plus base on boolq (base on hellaswag we already have).
#
# Total: 7 lm_eval calls. ~12 min each = ~85 min wall on one GPU.
# To parallelize, split into multiple sbatch jobs; this single-job version
# is fine for one-shot validation.

set -euo pipefail

module purge
module load python/2025.12-2
module load cuda12.8/toolkit/12.8.1

source "${HOME}/weightBench/.venv/bin/activate"

cd "${HOME}/weightBench/weightBench/experiment1"
mkdir -p logs eval_results

export PYTHONUNBUFFERED=1

BASE="${HOME}/weightBench/weightBench/experiment1/models/Qwen2.5-7B"
HELLASWAG="${HOME}/weightBench/weightBench/experiment1/adapters/hellaswag_seed0/final"
BOOLQ="${HOME}/weightBench/weightBench/experiment1/adapters/boolq_seed0/final"
COMBINED="${HOME}/weightBench/weightBench/experiment1/adapters/combined_hellaswag_boolq/combined"

echo "===================================================================="
echo "[$(date)] BASE on boolq"
echo "===================================================================="
lm_eval --model hf --model_args "pretrained=${BASE},dtype=bfloat16" \
    --tasks boolq --batch_size 8 \
    --output_path "eval_results/base_on_boolq"

echo "===================================================================="
echo "[$(date)] hellaswag-LoRA on boolq (cross-interference test)"
echo "===================================================================="
lm_eval --model hf --model_args "pretrained=${BASE},peft=${HELLASWAG},dtype=bfloat16" \
    --tasks boolq --batch_size 8 \
    --output_path "eval_results/hellaswagLoRA_on_boolq"

echo "===================================================================="
echo "[$(date)] boolq-LoRA on boolq (specialist alone)"
echo "===================================================================="
lm_eval --model hf --model_args "pretrained=${BASE},peft=${BOOLQ},dtype=bfloat16" \
    --tasks boolq --batch_size 8 \
    --output_path "eval_results/boolqLoRA_on_boolq"

echo "===================================================================="
echo "[$(date)] boolq-LoRA on hellaswag (cross-interference test)"
echo "===================================================================="
lm_eval --model hf --model_args "pretrained=${BASE},peft=${BOOLQ},dtype=bfloat16" \
    --tasks hellaswag --batch_size 8 \
    --output_path "eval_results/boolqLoRA_on_hellaswag"

echo "===================================================================="
echo "[$(date)] combined (50/50) on hellaswag (composition test)"
echo "===================================================================="
lm_eval --model hf --model_args "pretrained=${BASE},peft=${COMBINED},dtype=bfloat16" \
    --tasks hellaswag --batch_size 8 \
    --output_path "eval_results/combined_on_hellaswag"

echo "===================================================================="
echo "[$(date)] combined (50/50) on boolq (composition test)"
echo "===================================================================="
lm_eval --model hf --model_args "pretrained=${BASE},peft=${COMBINED},dtype=bfloat16" \
    --tasks boolq --batch_size 8 \
    --output_path "eval_results/combined_on_boolq"

echo "[$(date)] done."
