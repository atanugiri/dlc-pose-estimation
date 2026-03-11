#!/bin/bash
#SBATCH --job-name=stitch_videos
#SBATCH --output=logs/stitch_%A_%a.out
#SBATCH --error=logs/stitch_%A_%a.err
#SBATCH --partition=dgx
#SBATCH --time=02:00:00
#SBATCH --cpus-per-task=8
#SBATCH --mem=8G
#SBATCH --array=1-86%10        # adjust 100 to number of lines in folders.txt; %10 = 10 at a time

# ── User settings ─────────────────────────────────────────────────────────────
CONDA_ENV=DEEPLABCUT
SCRIPT=/work/agiri/scripts/stitch_videos.py
FOLDERS_FILE=/work/agiri/scripts/folders.txt   # one folder path per line
OUTPUT_DIR=/work/agiri/Competition-task/stitched_videos
# ──────────────────────────────────────────────────────────────────────────────

set -euo pipefail

mkdir -p logs "$OUTPUT_DIR"

# Pick the folder for this array task (1-indexed)
INPUT_FOLDER=$(sed -n "${SLURM_ARRAY_TASK_ID}p" "$FOLDERS_FILE")

if [[ -z "$INPUT_FOLDER" ]]; then
    echo "No folder found for task ${SLURM_ARRAY_TASK_ID}, exiting."
    exit 0
fi

echo "Task ${SLURM_ARRAY_TASK_ID}: processing folder: $INPUT_FOLDER"

# Derive output name from the first video file's stem, stripping _Trial_N suffix
first_file=$(ls "$INPUT_FOLDER"/*.mp4 2>/dev/null | sort | head -1)
if [[ -z "$first_file" ]]; then
    echo "No .mp4 files found in $INPUT_FOLDER, skipping."
    exit 0
fi

base=$(basename "$first_file" .mp4)
output_name=$(echo "$base" | sed 's/_Trial_[0-9]*$//')

echo "Output name: $output_name"

# Activate conda
source "$HOME/miniconda3/etc/profile.d/conda.sh"
conda activate "$CONDA_ENV"

python "$SCRIPT" "$INPUT_FOLDER" \
    -o "$OUTPUT_DIR" \
    -n "$output_name"

echo "Done at $(date)"

