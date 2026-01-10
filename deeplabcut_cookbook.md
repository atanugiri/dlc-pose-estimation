# DeepLabCut Cookbook

This cookbook summarizes the DeepLabCut workflow for pose estimation, based on our project setup. It covers local development, HPC training, and troubleshooting. Use it as a quick reference to avoid forgetting steps.

## Table of Contents
- [Setup](#setup)
- [Project Creation](#project-creation)
- [Adding Videos](#adding-videos)
- [Frame Extraction](#frame-extraction)
- [Labeling Frames](#labeling-frames)
- [Creating Training Dataset](#creating-training-dataset)
- [Training the Network](#training-the-network)
- [Evaluating the Model](#evaluating-the-model)
- [Analyzing Videos](#analyzing-videos)
- [Filtering Predictions](#filtering-predictions)
- [Creating Labeled Videos](#creating-labeled-videos)
- [Active Learning (Outliers)](#active-learning-outliers)
- [HPC Usage](#hpc-usage)
- [Troubleshooting](#troubleshooting)

## Setup
1. Install DeepLabCut: `pip install deeplabcut[gui]`
2. Activate environment: `conda activate DEEPLABCUT`
3. Check PyTorch: Ensure GPU support if available.

## Project Creation, Adding Videos, Frame Extraction, and Labeling Frames (Recommended: Use the GUI)

For these steps, it is easiest to use the DeepLabCut GUI:

1. Activate your conda environment:
  ```bash
  conda activate DEEPLABCUT
  ```
2. Launch the GUI:
  ```bash
  python -m deeplabcut
  ```
3. Use the GUI to:
  - Create a new project
  - Add videos to a project
  - Extract frames for labeling
  - Label frames (and refine labels)

You can also do these steps programmatically if needed:

  ```python
  import deeplabcut
  # Create a new project
  config_path = deeplabcut.create_new_project(
    "ProjectName", "Scorer", [video_paths],
    working_directory="/path/to/projects",
    copy_videos=True, multianimal=False
  )
  # Add more videos
  deeplabcut.add_new_videos(config_path, [new_video_paths], copy_videos=False, extract_frames=False)
  # Extract frames
  deeplabcut.extract_frames(config_path, mode='automatic', algo='kmeans', crop='GUI', userfeedback=True)
  # Label frames
  deeplabcut.label_frames(config_path)
  # Refine labels
  deeplabcut.refine_labels(config_path)
  ```

- Edit `config.yaml` for bodyparts, skeleton, etc. as needed.

## Creating Training Dataset
- Merge labels and create splits:
  ```python
  deeplabcut.merge_datasets(config_path)
  ```
  Recommended: Use IPython for creating the training dataset (better for debugging and interactive work):

  1. Activate your environment:
    ```bash
    conda activate DEEPLABCUT
    ipython
    ```
  2. In IPython:
    ```python
    import deeplabcut
    from pathlib import Path
    config_path = str(Path("config.yaml").resolve())
    deeplabcut.create_training_dataset(config_path, num_shuffles=3)
    ```

## Training the Network
- Train the model:
  ```python
  deeplabcut.train_network(
      config_path, shuffle=1, trainingsetindex=0,
      device="cuda:0", epochs=500, batch_size=8,
      snapshot_path="path/to/init/model.pt"  # Optional transfer learning
  )
  ```
- **Model Selection**: Use ResNet-101 or ResNet-152 for complex data (occlusions, low contrast) instead of ResNet-50. Larger models improve accuracy but require more GPU memory/time.
- **Transfer Learning**: For multiple shuffles, train shuffle 1 from scratch, then use shuffle 1's best snapshot as `snapshot_path` for shuffle 2, and so on. This speeds up convergence and boosts performance.

## Evaluating the Model
- Evaluate on test set:
  ```python
  deeplabcut.evaluate_network(config_path, Shuffles=[1], plotting=True)
  ```
- Check metrics: RMSE <2 pixels and mAP >80% indicate excellent performance. mAP >85% is outstanding.
- **Multiple Shuffles**: For robustness, create and evaluate multiple shuffles.
  ```python
  deeplabcut.create_training_dataset(config_path, num_shuffles=3)  # Shuffles 1,2,3
  # Train each shuffle separately (update SHUFFLE in script)
  deeplabcut.evaluate_network(config_path, Shuffles=[1,2,3], plotting=True)
  ```
  - Compare metrics across shuffles for uniformity. If one shuffle has much lower mAP (e.g., <50%), it may be overfitting—consider retraining with more data or active learning.

## Analyzing Videos
- Predict poses on new videos:
  ```python
  deeplabcut.analyze_videos(config_path, [video_paths], shuffle=1, gputouse="cuda:0", save_as_csv=True)
  ```

## Filtering Predictions
- Smooth predictions:
  ```python
  deeplabcut.filterpredictions(config_path, [video_paths], shuffle=1, filtertype='median', p_bound=0.05)
  ```

## Adding or Modifying Bodyparts
If you need to add more bodyparts (e.g., tail segments, limbs) after initial setup:

1. **Edit `config.yaml`**: Add new bodyparts under `bodyparts:` and update `skeleton:` for connections.
2. **Relabel Specific Frames**: Label only the relevant videos/folders for the new bodyparts.
   ```python
   deeplabcut.label_frames(config_path, videos=["path/to/labeled-data/folder/"])
   ```
3. **Merge and Retrain**:
   ```python
   deeplabcut.merge_datasets(config_path)
   deeplabcut.create_training_dataset(config_path, num_shuffles=3)
   # Retrain shuffles as needed
   ```

## Active Learning (Outliers)
Active learning is used to improve model performance by identifying and labeling frames where the model is uncertain. Use this after initial training and evaluation if metrics are poor (e.g., RMSE >5 pixels, mAP <80%). This typically happens after the first round of training, evaluation, and analysis on videos. If the model's predictions are inaccurate or inconsistent, extract outliers, label them, and retrain. If mAP is already >80%, active learning is optional but can push accuracy higher.

**Tip:** For labeling outlier frames, using `deeplabcut.label_frames` with the GUI is often easier and more user-friendly than `refine_labels`.

  ```python
  deeplabcut.extract_outlier_frames(config_path, [video_paths], outlieralgorithm='uncertain', p_bound=0.1) # use judgement for p_bound
  deeplabcut.refine_labels(config_path)  # Label outliers
  deeplabcut.merge_datasets(config_path)
  deeplabcut.create_training_dataset(config_path)
  # Retrain
  ```
## Lesson: Using extract_outlier_frames Across Projects

### Key Points

1. **Cross-Project Model Usage:** You can use a pose-estimation model trained in one DeepLabCut project for another project, provided the videos are visually similar (lighting, subjects, etc.).

2. **Expect Outliers:** When you use `deeplabcut.label_videos` to validate predictions in the new project, expect some outlier frames, especially if the new videos differ in subtle ways from the training set.

3. **Extract Outlier Frames:** Use `deeplabcut.extract_outlier_frames` for the videos in the new project folder to identify and extract frames where the model predictions are likely incorrect.

4. **Important Directory Structure:** Ensure that the output files from `deeplabcut.analyze_videos` (e.g., `.h5` or `.csv` pose data) are present in the same directory as the corresponding video files. This is required for `extract_outlier_frames` to work correctly.

---

This workflow allows you to efficiently adapt and improve pose estimation for new datasets by leveraging existing models and refining them with outlier correction.

## HPC Usage
- Sync files to HPC:
  - Initial sync or general update: `rsync -avzP . lonestar6:/work/10823/atanugiri2025/ls6/DLC-Black-LightOnly-Atanu-2025-12-13/`
  - From outside project folder: `rsync -avzP /Users/atanugiri/Downloads/dlc-pose-estimation/DLC-Black-LightOnly-Atanu-2025-12-13 lonestar6:/work/10823/atanugiri2025/ls6/`
  - Exact mirror (deletes extra files): `rsync -avzP --delete . lonestar6:/work/10823/atanugiri2025/ls6/DLC-Black-LightOnly-Atanu-2025-12-13/`
  - Safe testing (dry run): `rsync -avzP --dry-run . lonestar6:/work/10823/atanugiri2025/ls6/DLC-Black-LightOnly-Atanu-2025-12-13/`
- Submit job: `sbatch scripts/train_dlc.slurm`
- Monitor: `squeue -u user`, `sacct -j job_id`
- Paths: Use `$WORK` for project root.

## Troubleshooting
- **Poor Metrics**: Check labels, retrain longer, add data, use outliers.
- **Path Issues**: Ensure `$WORK` resolves correctly on HPC.
- **GPU Errors**: Check `torch.cuda.is_available()`.
- **SLURM Fails**: Verify script syntax, permissions, resources.
- **Import Errors**: Activate correct environment.

## Tips
- Always evaluate after training.
- Use multiple shuffles for robustness and compare metrics.
- For challenging data (occlusions, low contrast), use ResNet-101 and transfer learning between shuffles.
- If mAP >80%, the model is ready for analysis; active learning can refine further.
- Preprocess videos (e.g., contrast enhancement with FFmpeg) if color differentiation is poor.
- Backup models and data regularly.
- For questions, refer to [DeepLabCut Docs](https://deeplabcut.github.io/DeepLabCut/).

This cookbook is based on our workflow—update as needed!