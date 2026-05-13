"""Download Qwen2.5-7B base weights into experiment1/models/Qwen2.5-7B/.

Run once per machine. Idempotent — HF hub cache + local_dir resume on partial downloads.
Run on HPC; ~14GB. No GPU required for download.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from huggingface_hub import snapshot_download

DEFAULT_REPO = "Qwen/Qwen2.5-7B"
DEFAULT_DIR = Path(__file__).resolve().parents[1] / "models" / "Qwen2.5-7B"


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--repo", default=DEFAULT_REPO)
    p.add_argument("--out", type=Path, default=DEFAULT_DIR)
    p.add_argument("--revision", default=None, help="Pin a specific commit hash for reproducibility.")
    args = p.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    print(f"Downloading {args.repo} → {args.out}")
    snapshot_download(
        repo_id=args.repo,
        local_dir=str(args.out),
        revision=args.revision,
        allow_patterns=["*.json", "*.safetensors", "*.txt", "tokenizer*", "*.model"],
    )
    print("done.")


if __name__ == "__main__":
    main()
