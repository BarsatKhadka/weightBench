#!/bin/bash
#SBATCH --job-name=lora_analyze
#SBATCH --partition=cpuq
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --time=01:00:00
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err

# Cheap CPU-only analyses: subspace distances + spectra.
# Run on cpuq so we don't hog the login node.
#
# Usage:
#   sbatch scripts/analyze_cpu.sbatch

set -euo pipefail

module purge
module load python/2025.12-2

source "${HOME}/weightBench/.venv/bin/activate"

cd "${HOME}/weightBench/weightBench/experiment1"
mkdir -p logs analyze

export PYTHONUNBUFFERED=1

echo "[$(date)] === compute_subspace_distances ==="
python analyze/compute_subspace_distances.py

echo
echo "[$(date)] === compute_spectra ==="
python analyze/compute_spectra.py

echo
echo "[$(date)] === done ==="
ls -lh analyze/
