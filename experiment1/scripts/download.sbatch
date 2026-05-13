#!/bin/bash
#SBATCH --job-name=lora_dl
#SBATCH --partition=cpuq
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=02:00:00
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err

# Magnolia (Ole Miss MCSR) — runs the three setup steps on a CPU node so we
# don't hammer the login node with a 14GB HF download.
# Usage:
#   sbatch scripts/download.sbatch

set -euo pipefail

module purge
module load python/2025.12-2

source "${HOME}/weightBench/.venv/bin/activate"

cd "${HOME}/weightBench/weightBench/experiment1"
mkdir -p logs

echo "[$(date)] download model"
python src/download_model.py

echo "[$(date)] download datasets"
python src/download_datasets.py

echo "[$(date)] format datasets"
python src/format_datasets.py

echo "[$(date)] done"
du -sh models/Qwen2.5-7B data/raw data/formatted 2>/dev/null || true
