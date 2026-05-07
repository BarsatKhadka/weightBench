---
source_url: https://arxiv.org/abs/2512.15634
captured_at: 2026-05-07
author: Anonymous (Dec 2024)
contributor: autonomous-loop
---
# How Much is Too Much? Exploring LoRA Rank Trade-offs (arXiv:2512.15634, Dec 2024)

## Core finding
Rank-forgetting relationship is NOT monotonic across task types. Reasoning tasks more sensitive to rank selection than recall tasks. Intermediate ranks r=32–64 offer a balanced operating point for LLaMA.

## Rank tested
r ∈ {8, 16, 32, 64, 128}. LoRA at r=128 achieves 57.44% MMLU vs 53.03% for full SFT on LLaMA — very high rank LoRA can HELP generalization on some benchmarks.

## Spectral finding
Measures cosine similarity between top-500 singular vectors before and after fine-tuning. LoRA induces "more targeted changes" than full SFT; full SFT causes "more drastic reshaping of the entire representation space." Frobenius norm grows approximately logarithmically with rank.

## Key connection to TRS
Directly measures singular vector alignment with pretrained weights — provides empirical evidence for the W0 singular structure being meaningful for understanding LoRA's update geometry.

## No intruder dimension analysis
Does not perform causal intervention (unlike Shuttleworth). Cannot establish whether forgetting is mediated by intruder dims.
