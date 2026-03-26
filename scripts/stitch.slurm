#!/bin/bash
#SBATCH --job-name=final_stitch
#SBATCH --output=final_stitch_%j.out
#SBATCH --error=final_stitch_%j.err
#SBATCH --partition=dgx
#SBATCH --time=04:00:00
#SBATCH --cpus-per-task=4
#SBATCH --mem=8G

set -euo pipefail

source "$HOME/miniconda3/etc/profile.d/conda.sh"
conda activate DEEPLABCUT

python scripts/stitch_videos.py \
    Elevated-maze/videos/ \
    -o Elevated-maze/

# python scripts/convert_to_grayscale.py --input-dir Elevated-maze/ \
#     --ext avi \
#     --output-dir Elevated-maze/videos/
