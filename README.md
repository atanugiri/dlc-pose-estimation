# dlc-pose-estimation

Local project containing DeepLabCut notebooks and environment for pose-estimation work.

## Purpose
- Hold DeepLabCut training/evaluation notebooks and a DeepLabCut-specific conda environment file.
- Keep heavy DLC-specific dependencies and notebooks separate from the lighter `GhrelinBehaviorQuantification` analysis repo.

## Layout (example)
```
dlc-pose-estimation/
├── notebooks/                     # DeepLabCut training & tracking notebooks
│   ├── 10_DLCjupyter.ipynb
├── environment_dlc.yml            # Conda environment for DeepLabCut (local)
└── data/                          # (optional) Raw videos, extracted DLC outputs
```

## Quick notes
- The `GhrelinBehaviorQuantification` repo points to this local path for DeepLabCut-specific materials. If you publish this project later, replace the local path with a URL.
- The large filtered DLC CSVs are distributed separately (Harvard Dataverse). After downloading and extracting `DlcDataPytorchFiltered.zip`, place the `DlcDataPytorchFiltered/` folder in the `data/` directory here or in the analysis repo's `data/` directory as needed.

## Using the environment
1. Create the environment from the local `environment_dlc.yml`:

```bash
conda env create -f ~/Downloads/dlc-pose-estimation/environment_dlc.yml
conda activate dlc-pose
```

2. Open notebooks in `notebooks/` (JupyterLab or VS Code). Select the `dlc-pose` kernel if available.

## Re-generating metadata
- Metadata mapping between raw/filtered CSVs and trial IDs is produced by the `DLCDatabaseSetup` tools. If you need to re-generate `dlc_table.csv`, use:

https://github.com/atanugiri/DLCDatabaseSetup

(That repository remains the canonical place for `dlc_table.csv` generation and parsing helpers.)

## Notes
- This project is intentionally local. If you later want me to prepare a small publish-ready package (README, license, minimal usage examples), tell me whether you want it on GitHub or another host and I will scaffold it.

## Local ⇄ HPC workflow (annotation locally, training on HPC)

Overview:
- Annotate and verify training/validation frames locally (fast interactive work).
- Transfer the labeled data and environment spec to the university HPC for model training (GPU nodes).

Recommended workflow:
1. Keep your authoritative dataset and labels locally in `~/Downloads/dlc-pose-estimation/data/` while editing/annotating.
2. Export a small, validated training set for quick iteration; sync it to the HPC when ready for full training.
3. Export the DeepLabCut environment spec and any required conda packages to ensure reproducibility on the cluster.

Sync commands (rsync examples):

```bash
# Push local folder to HPC (preserve permissions, resume-capable)
rsync -avP ~/Downloads/dlc-pose-estimation/data/ yourusername@hpc.university.edu:/scratch/yourusername/dlc-data/

# Pull results back from HPC (models, logs)
rsync -avP yourusername@hpc.university.edu:/scratch/yourusername/dlc-results/ ~/Downloads/dlc-pose-estimation/results/
```

Secure copy (scp) alternative for smaller transfers:
```bash
scp ~/Downloads/dlc-pose-estimation/data/small-training-set.zip yourusername@hpc.university.edu:/scratch/yourusername/
```

Environment management:
- Export a reproducible conda environment YAML locally and transfer it to the HPC.

```bash
conda activate dlc-pose
conda env export --from-history > environment_dlc.yml
rsync -avP environment_dlc.yml yourusername@hpc.university.edu:/scratch/yourusername/
```

On the HPC, prefer creating an environment with `mamba` if available (faster):

```bash
# on the cluster
mamba env create -f /scratch/yourusername/environment_dlc.yml -n dlc-pose
conda activate dlc-pose
```

Slurm job example (GPU training):

```bash
#!/bin/bash
#SBATCH --job-name=dlc_train
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=24:00:00
#SBATCH --output=dlc_train.%j.out

module load anaconda/2021.11
source activate dlc-pose
cd /scratch/yourusername/dlc-data
python ~/Downloads/dlc-pose-estimation/notebooks/train_dlc.py --config config.yaml
```

Notes and best practices:
- Use SSH key authentication and keep large transfers on fast storage (scratch or project disk) on the cluster.
- Avoid training directly on network-mounted home directories; prefer local scratch for speed and stability.
- Keep a small validation subset locally for quick checks before full HPC runs.
- Clean up large intermediate files on the cluster after successful transfers to avoid quota issues.

If you want, I can add a ready-to-use `sync.sh` script and a `slurm/` folder with job templates tuned for your HPC.
