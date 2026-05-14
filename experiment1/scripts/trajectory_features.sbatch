#!/bin/bash
#SBATCH --job-name=traj_features
#SBATCH --partition=cpuq
#SBATCH --cpus-per-task=16
#SBATCH --mem=96G
#SBATCH --time=02:00:00
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err

# Per-checkpoint trajectory feature extraction for the phase-structure project.
# CPU-only: SVD + Grassmannian on rank-16 LoRA factors.
# 5 seeds x 41 checkpoints x 196 layers ~= 40K SVDs (~milliseconds each with
# the QR+small-SVD trick) + ~40K Grassmannian distances. ~30 min wall.

set -euo pipefail

module purge
module load python/2025.12-2

source "${HOME}/weightBench/.venv/bin/activate"

cd "${HOME}/weightBench/weightBench/experiment1"
mkdir -p logs analyze

export PYTHONUNBUFFERED=1

echo "[$(date)] starting trajectory feature extraction"
python analyze/compute_trajectory_features.py
echo "[$(date)] done"
ls -lh analyze/trajectory_features.parquet
