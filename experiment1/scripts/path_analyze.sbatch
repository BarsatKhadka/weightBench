#!/bin/bash
#SBATCH --job-name=path_analyze
#SBATCH --partition=cpuq
#SBATCH --cpus-per-task=16
#SBATCH --mem=64G
#SBATCH --time=04:00:00
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err

# CPU-only path analyses for the "knowledge is a PATH, not a POINT" headline.
#
#   1. path_vs_speed.py   -- DTW on the 5 hellaswag trajectories.
#                            Runs immediately on what we already have.
#   2. cross_task_dG.py   -- endpoint within vs between task d_G.
#                            Requires the population trainer to have produced
#                            at least some {boolq, arc_easy, winogrande, gsm8k}
#                            seeds. Will skip missing runs (warnings only).
#
# Usage:
#   sbatch scripts/path_analyze.sbatch                 # both steps
#   STEP=path  sbatch scripts/path_analyze.sbatch      # only path_vs_speed
#   STEP=cross sbatch scripts/path_analyze.sbatch      # only cross_task_dG

set -euo pipefail

module purge
module load python/2025.12-2

source "${HOME}/weightBench/.venv/bin/activate"

cd "${HOME}/weightBench/weightBench/experiment1"
mkdir -p logs analyze analyze/phase_plots

export PYTHONUNBUFFERED=1

STEP="${STEP:-both}"

if [[ "${STEP}" == "path" || "${STEP}" == "both" ]]; then
    echo "[$(date)] === path_vs_speed.py (DTW on hellaswag) ==="
    python analyze/path_vs_speed.py \
        --task hellaswag \
        --seeds 0,1,2,3,4
fi

if [[ "${STEP}" == "cross" || "${STEP}" == "both" ]]; then
    echo
    echo "[$(date)] === cross_task_dG.py (within vs between task) ==="
    python analyze/cross_task_dG.py \
        --tasks hellaswag boolq arc_easy winogrande gsm8k \
        --seeds 0,1,2
fi

echo
echo "[$(date)] === done ==="
ls -lh analyze/ analyze/phase_plots/ 2>/dev/null || true
