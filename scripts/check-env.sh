#!/usr/bin/env bash
# Verifies the laptop meets the Phase 1 requirements.
set -u
fail=0
need() { command -v "$1" >/dev/null 2>&1 && echo "ok   $1" || { echo "MISS $1"; fail=1; }; }
need docker; need ffmpeg; need python3; need git
docker compose version >/dev/null 2>&1 && echo "ok   compose" || { echo "MISS compose"; fail=1; }
docker run --rm --gpus all nvidia/cuda:12.4.1-base-ubuntu22.04 nvidia-smi -L >/dev/null 2>&1 \
  && echo "ok   gpu-in-docker" || { echo "MISS gpu-in-docker"; fail=1; }
exit $fail