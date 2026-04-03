#!/bin/bash
#SBATCH --job-name=outliers
#SBATCH --output=/work/agiri/logs/%x-%j.out
#SBATCH --error=/work/agiri/logs/%x-%j.err
#SBATCH --partition=dgx         # dgx partition; no GPU requested
#SBATCH --time=03:00:00
#SBATCH --cpus-per-task=12
#SBATCH --mem=16G

set -euo pipefail

mkdir -p "$WORK/logs" "$WORK/.cache" "$WORK/pip-cache" "$WORK/mplconfig" "$WORK/tmp" "$WORK/home_fake"

# Edit these if needed
CONDA_ENV=DEEPLABCUT
CONFIG_PATH="${WORK}/ElevatedMaze-Atanu-2026-03-25/config.yaml"
VIDEO="${WORK}/ElevatedMaze-Atanu-2026-03-25/stitched_video.mp4"

# Activate conda
source /home/agiri/miniconda3/etc/profile.d/conda.sh
conda activate "$CONDA_ENV"

export PIP_CACHE_DIR="$WORK/pip-cache" XDG_CACHE_HOME="$WORK/.cache" MPLCONFIGDIR="$WORK/mplconfig" 
export TMPDIR="$WORK/tmp" TMP="$WORK/tmp" TEMP="$WORK/tmp" HOME="$WORK/home_fake"

echo "HOME=$HOME" "XDG_CACHE_HOME=$XDG_CACHE_HOME" "PIP_CACHE_DIR=$PIP_CACHE_DIR"
echo "TMPDIR=$TMPDIR" "TMP=$TMP" "TEMP=$TEMP" "MPLCONFIGDIR=$MPLCONFIGDIR"
echo "Allocated CPUs: $SLURM_CPUS_PER_TASK"

echo "Starting DeepLabCut extract_outlier_frames..."
python - <<PY
import os
print("CPU count visible:", os.cpu_count())
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