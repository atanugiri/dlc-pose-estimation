#!/bin/bash
#SBATCH --job-name=grayscale_convert
#SBATCH --output=%x-%j.out
#SBATCH --error=%x-%j.err
#SBATCH --partition=dgx         # CPU partition
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8       # ffmpeg can use multiple threads
#SBATCH --time=01:00:00         # Adjust based on number/size of videos
#SBATCH --mem=8G

# --- Variables ---
export CONDA_ENV="$HOME/miniconda3/envs/DEEPLABCUT"
export SCRIPT_PATH="$WORK/scripts/convert_to_grayscale.py"
export INPUT_DIR="$WORK/Black-ChocolateMilk-Atanu-2026-02-08/videos_colored"
export OUTPUT_DIR="$WORK/Black-ChocolateMilk-Atanu-2026-02-08/videos"
export CONTRAST=1.0
export BRIGHTNESS=-0.1

echo "=========================================="
echo "Job: $SLURM_JOB_NAME"
echo "Job ID: $SLURM_JOB_ID"
echo "Node: $(hostname)"
echo "Started: $(date)"
echo "=========================================="

# Initialize environment
source $HOME/miniconda3/etc/profile.d/conda.sh
conda activate "$CONDA_ENV"

# Verify ffmpeg is available
which ffmpeg
ffmpeg -version | head -1

# Run conversion
echo ""
echo "Converting videos to grayscale..."
echo "Input:  $INPUT_DIR"
echo "Output: $OUTPUT_DIR"
echo "Contrast: $CONTRAST, Brightness: $BRIGHTNESS"
echo ""

python "$SCRIPT_PATH" \
    --input-dir "$INPUT_DIR" \
    --output-dir "$OUTPUT_DIR" \
    --contrast "$CONTRAST" \
    --brightness "$BRIGHTNESS"

EXIT_CODE=$?

echo ""
echo "=========================================="
echo "Job finished: $(date)"
echo "Exit code: $EXIT_CODE"
echo "=========================================="

exit $EXIT_CODE
