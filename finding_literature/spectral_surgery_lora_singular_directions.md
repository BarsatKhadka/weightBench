---
source_url: https://arxiv.org/abs/2603.03995
captured_at: 2026-05-07
author: Tian, Chen, Han, Liao (Mar 2026)
contributor: autonomous-loop
---
# Spectral Surgery: Training-Free Refinement of LoRA via Gradient-Guided Singular Value Reweighting (arXiv:2603.03995)

## Core finding
LoRA updates have an **inefficient spectrum**: task effects concentrate in a small subset of
singular directions while many remaining components are neutral or detrimental. Reweighting
~1,000 scalar coefficients (singular values) while preserving directions improves performance.

## Key claim
Not all singular components of a trained LoRA are task-relevant. Many are noise/interference.
The gradient can identify which singular values to upweight (signal) vs downweight (interference).

## Connection to TRS / intruder dim theory
The "detrimental" singular components are intruder dimensions in our language — they are
above-MP but misaligned with task structure. The paper confirms empirically that removing or
downweighting these components improves task performance, supporting the causal claim from
Shuttleworth (2410.21228).

The paper does not distinguish components by their alignment to W₀ singular vectors (which
is the TRS criterion), but the phenomenon they observe is consistent: LoRA has signal dims +
intruder dims + bulk, and only the signal dims should be upweighted.

## What they do NOT do
- No fiber bundle language
- No intruder dimension analysis using W₀ alignment criterion
- No forgetting measurement — focused on in-task performance only
