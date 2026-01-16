# dlc-pose-estimation

Local workspace containing independent DeepLabCut projects for pose estimation analysis on black animals under various experimental conditions.

## Purpose
- Organize multiple self-contained DeepLabCut projects, each with its own configuration, training data, and analysis outputs.
- Provide shared utilities and scripts for video preprocessing, HPC workflows (GPU/CPU), and data management.
- Maintain documentation and guides for DeepLabCut setup and common workflows.

## Layout
```
dlc-pose-estimation/
├── DLC-Black-LightOnly-Atanu-2025-12-13/ # Example DLC project
│   ├── config.yaml                       # DeepLabCut configuration
│   ├── labeled-data/
│   ├── training-datasets/
│   ├── dlc-models/
│   ├── filtered_pose_data/
│   └── videos/
├── Black-FoodOnly-Atanu-2026-01-06/     # Other DLC projects...
├── Black-ToyOnly/
├── Black-FoodLight-Atanu-2026-01-15/
├── scripts/                              # Shared utilities
│   ├── convert_to_grayscale.py          # Video preprocessing
│   ├── dlc_pipeline_cpu.slurm           # HPC CPU workflow
│   └── dlc_pipeline_gpu.slurm           # HPC GPU workflow
├── deeplabcut_cookbook.md               # Common DLC workflows
├── DeepLabCut_Installation_Guide.md     # Setup instructions
└── README.md
```

## Documentation
- **deeplabcut_cookbook.md**: Step-by-step guides for common tasks
- **DeepLabCut_Installation_Guide.md**: Environment setup and dependencies
