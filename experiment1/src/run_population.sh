#!/usr/bin/env bash
# Population trainer for the cross-task path-vs-point comparison.
#
# Trains the same LoRA recipe (configs/train.yaml) on 4 additional tasks
# x 3 seeds = 12 LoRAs. Combined with the existing 5 hellaswag seeds we get
# a 5-task pool that lets us test:
#   within-task d_G   (same-task seed pairs) << between-task d_G   (cross-task pairs)
# which is the "knowledge is a PATH, not a POINT" headline at the endpoint,
# plus the same comparison along the trajectory.
#
# Each run is ~107 min on a single L40S per the config (max_steps=2000).
# 12 runs => ~21 GPU-hours serial.
#
# Prereqs:
#   - experiment1/data/formatted/{boolq,arc_easy,winogrande,gsm8k}.jsonl exist
#     (run: python src/format_datasets.py --only boolq arc_easy winogrande gsm8k)
#   - experiment1/models/Qwen2.5-7B/ exists (or HF cache has it)
#
# Usage:
#   bash experiment1/src/run_population.sh                  # all 4 tasks x 3 seeds
#   bash experiment1/src/run_population.sh boolq            # one task, 3 seeds
#   TASKS="boolq gsm8k" SEEDS="0 1" bash run_population.sh  # custom subset
#
# Logs go to experiment1/logs/<task>_seed<seed>.log.
# Adapters go to experiment1/adapters/<task>_seed<seed>/{checkpoint-*, final}.

set -euo pipefail

EXP_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$EXP_ROOT"

TASKS="${TASKS:-${1:-boolq arc_easy winogrande gsm8k}}"
SEEDS="${SEEDS:-0 1 2}"

LOG_DIR="$EXP_ROOT/logs"
mkdir -p "$LOG_DIR"

echo "==============================================================="
echo "POPULATION TRAINER"
echo "==============================================================="
echo "EXP_ROOT : $EXP_ROOT"
echo "TASKS    : $TASKS"
echo "SEEDS    : $SEEDS"
echo "LOG_DIR  : $LOG_DIR"
echo "==============================================================="
echo

# Sanity: required JSONL files exist
missing=0
for task in $TASKS; do
    if [[ ! -f "$EXP_ROOT/data/formatted/${task}.jsonl" ]]; then
        echo "[!] missing data/formatted/${task}.jsonl"
        missing=1
    fi
done
if [[ "$missing" -eq 1 ]]; then
    echo
    echo "Run first:  python src/format_datasets.py --only $TASKS"
    exit 1
fi

# Optional: skip already-finished runs (resume-friendly)
skip_if_done() {
    local task="$1" seed="$2"
    local final_dir="$EXP_ROOT/adapters/${task}_seed${seed}/final"
    if [[ -f "$final_dir/adapter_model.safetensors" ]]; then
        return 0
    fi
    return 1
}

total=0
done_count=0
for task in $TASKS; do
    for seed in $SEEDS; do
        total=$((total + 1))
    done
done

idx=0
t0=$(date +%s)
for task in $TASKS; do
    for seed in $SEEDS; do
        idx=$((idx + 1))
        tag="${task}_seed${seed}"
        log="$LOG_DIR/${tag}.log"

        if skip_if_done "$task" "$seed"; then
            echo "[$idx/$total] SKIP  $tag  (final/ already present)"
            done_count=$((done_count + 1))
            continue
        fi

        echo "[$idx/$total] START $tag  (log -> $log)"
        ts=$(date +%s)
        python -u src/train_lora.py --task "$task" --seed "$seed" \
            >"$log" 2>&1 \
            && echo "[$idx/$total] DONE  $tag  ($(( $(date +%s) - ts ))s)" \
            || { echo "[$idx/$total] FAIL  $tag  (see $log)"; }
    done
done

echo
echo "==============================================================="
echo "POPULATION TRAINING FINISHED"
echo "wall time: $(( $(date +%s) - t0 ))s"
echo "==============================================================="
