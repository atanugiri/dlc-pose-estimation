#!/bin/bash
#SBATCH --job-name=dlc_outliers
#SBATCH --output=%x-%j.out
#SBATCH --error=%x-%j.err
#SBATCH --partition=dgx         # CPU partition (no GPU cost)
#SBATCH --time=02:00:00
#SBATCH --cpus-per-task=24
#SBATCH --mem=16G

set -euo pipefail

# Edit these if needed
CONDA_ENV=DEEPLABCUT
CONFIG_PATH="${WORK}/Black-ToyRat-Atanu-2026-03-04/config.yaml"
VIDEO="${WORK}/Black-ToyRat-Atanu-2026-03-04/stitched_video.mp4"

echo "Job started on $(hostname) at $(date)"
echo "Config: $CONFIG_PATH"
echo "Video: $VIDEO"

# Activate conda
source "$HOME/miniconda3/etc/profile.d/conda.sh"
conda activate "$CONDA_ENV"

echo "Starting DeepLabCut extract_outlier_frames..."
python - <<PY
import builtins
builtins.input = lambda prompt=None: "yes"
import deeplabcut
config = "${CONFIG_PATH}"
videos = ["${VIDEO}"]
print('Config:', config)
print('Videos:', videos)
deeplabcut.extract_outlier_frames(config, videos, shuffle=3)
PY

echo "Job finished at $(date)"

