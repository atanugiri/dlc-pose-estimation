# DeepLabCut Installation Guide - Clear & Simplified

## 🎯 Quick Decision Guide

| Your Situation | Recommended Method | Why |
|---------------|-------------------|-----|
| **New to DeepLabCut** | Method 1: Official Environment | Simplest, most reliable |
| **Apple Silicon Mac (M1/M2/M3)** | Method 1: Official Environment | Optimized for your hardware |
| **NVIDIA GPU (CUDA)** | Method 1 or 2 | Both work, Method 1 is easier |
| **CPU-only machine** | Method 1: Official Environment | Handles everything automatically |
| **Need latest features** | Method 2: Manual Installation | More control over versions |
| **Want to contribute code** | Method 3: Development Setup | Full source code access |
| **HPC/Cluster** | Method 2: Manual Installation | Custom CUDA/Python versions |

---

## 📦 Method 1: Official Environment (RECOMMENDED for most users)

### When to Use
- ✅ First-time installation
- ✅ Apple Silicon Macs (M1/M2/M3)
- ✅ Windows/Linux with any GPU
- ✅ CPU-only systems
- ✅ Want guaranteed compatibility

### Steps

1. **Clone the repository** (to get environment files):
   ```bash
   git clone https://github.com/DeepLabCut/DeepLabCut.git
   cd DeepLabCut/conda-environments
   ```

2. **Choose your environment file**:
   - **Most systems**: `DEEPLABCUT.yaml` (Python 3.10, PyTorch, DLC 3.0.0rc9)
   - **Legacy systems**: Check other YAML files in the folder

3. **Create environment**:
   ```bash
   conda env create -f DEEPLABCUT.yaml
   conda activate DEEPLABCUT
   ```

4. **Verify installation**:
   ```bash
   python -c "import deeplabcut; print('DLC version:', deeplabcut.__version__)"
   ```

5. **Test GPU acceleration**:
   ```bash
   # For NVIDIA GPUs
   python -c "import torch; print('CUDA available:', torch.cuda.is_available())"

   # For Apple Silicon
   python -c "import torch; print('MPS available:', torch.backends.mps.is_available())"
   ```

6. **Launch GUI**:
   ```bash
   python -m deeplabcut
   ```

### What's Included
- Python 3.10
- PyTorch (with hardware acceleration)
- DeepLabCut 3.0.0rc9 with GUI
- All necessary dependencies
- Model zoo access
- Wandb integration

### Cleanup
After successful installation, you can delete the cloned repository:
```bash
rm -rf DeepLabCut  # Saves ~500MB
```

---

## 🔧 Method 2: Manual Installation (For advanced users)

### When to Use
- ✅ Need specific Python/CUDA versions
- ✅ HPC clusters with custom requirements
- ✅ Want latest pre-release features
- ✅ Need fine control over dependencies

### Steps

1. **Create environment**:
   ```bash
   conda create -n DEEPLABCUT python=3.10  # or 3.11, 3.12
   conda activate DEEPLABCUT
   ```

2. **Install core dependencies**:
   ```bash
   conda install -c conda-forge pytables==3.8.0
   ```

3. **Install PyTorch** (choose based on your hardware):

   **For NVIDIA GPUs (CUDA)**:
   ```bash
   # Check PyTorch website for latest versions
   conda install pytorch torchvision cudatoolkit=11.8 -c pytorch -c conda-forge
   ```

   **For Apple Silicon Macs**:
   ```bash
   conda install pytorch torchvision -c pytorch
   ```

   **For CPU-only**:
   ```bash
   conda install pytorch torchvision cpuonly -c pytorch
   ```

4. **Install DeepLabCut**:
   ```bash
   # Latest stable
   pip install deeplabcut[gui]

   # Or latest pre-release
   pip install --pre deeplabcut[gui]
   ```

5. **Verify installation** (same as Method 1)

### Advantages
- Full control over versions
- Can use bleeding-edge releases
- Customizable for specific hardware

### Disadvantages
- More complex setup
- Higher chance of compatibility issues
- Requires knowing exact version requirements

---

## 💻 Method 3: Development Installation (For contributors)

### When to Use
- ✅ Want to modify DeepLabCut code
- ✅ Need to fix bugs or add features
- ✅ Want to test changes locally
- ✅ Contributing to the project

### Steps

1. **Clone repository**:
   ```bash
   git clone https://github.com/DeepLabCut/DeepLabCut.git
   cd DeepLabCut
   ```

2. **Set up environment** (choose one):

   **Option A: Use provided environment**:
   ```bash
   conda env create -f conda-environments/DEEPLABCUT.yaml
   conda activate DEEPLABCUT
   ```

   **Option B: Manual setup**:
   ```bash
   conda create -n DEEPLABCUT python=3.10
   conda activate DEEPLABCUT
   pip install -e .[gui]  # Install in development mode
   ```

3. **Install in development mode**:
   ```bash
   pip install -e .[gui]
   ```

4. **Make changes and test**:
   ```bash
   # Edit code in DeepLabCut/ folder
   # Run reinstall script after changes
   ./reinstall.sh
   ```

5. **Run tests**:
   ```bash
   python -m pytest tests/
   ```

### Development Workflow
- Code changes are immediately active (no reinstall needed for Python changes)
- Use `./reinstall.sh` for Cython extensions or major changes
- Test with provided test scripts in `examples/`
- Check version: `deeplabcut.__version__`

---

## 🖥️ Platform-Specific Notes

### Apple Silicon Macs (M1/M2/M3/M4)
- Use **Method 1** with `DEEPLABCUT.yaml`
- MPS acceleration is automatically enabled
- No CUDA installation needed

### Windows with NVIDIA GPU
- Use **Method 1** or **Method 2**
- Ensure NVIDIA drivers are installed
- CUDA toolkit installed via conda

### Linux with NVIDIA GPU
- Use **Method 1** or **Method 2**
- Install NVIDIA drivers and CUDA toolkit
- May need additional system packages

### CPU-Only Systems
- Use **Method 1** (handles CPU-only automatically)
- Or **Method 2** with `cpuonly` PyTorch

### HPC Clusters
- Use **Method 2** for custom CUDA/Python versions
- Check cluster-specific requirements
- May need to load modules (e.g., `module load cuda`)

---

## 🔍 Troubleshooting

### Common Issues

**"Module not found" errors**:
- Ensure correct conda environment is activated
- Try `conda env update -f DEEPLABCUT.yaml`

**CUDA not detected**:
- Check NVIDIA drivers: `nvidia-smi`
- Verify PyTorch CUDA: `python -c "import torch; print(torch.cuda.is_available())"`

**MPS not working on Mac**:
- Ensure PyTorch 1.12+
- Check: `python -c "import torch; print(torch.backends.mps.is_available())"`

**GUI won't start**:
- Install missing Qt dependencies
- Try `conda install qt` or `pip install PyQt5`

**OpenMP errors on macOS**:
- Set environment variable: `export KMP_DUPLICATE_LIB_OK=TRUE`

### Getting Help
- Check [DeepLabCut GitHub Issues](https://github.com/DeepLabCut/DeepLabCut/issues)
- Read the [official documentation](https://deeplabcut.github.io/DeepLabCut/)
- Post questions on the [DeepLabCut forum](https://forum.deeplabcut.org/)

---

## 📚 Additional Resources

- [Official Installation Docs](https://deeplabcut.github.io/DeepLabCut/docs/installation.html)
- [PyTorch Installation Guide](https://pytorch.org/get-started/locally/)
- [Conda Environment Management](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)
- [DeepLabCut User Guide](https://deeplabcut.github.io/DeepLabCut/docs/standardDeepLabCut_UserGuide.html)

---

*This guide is based on the official DeepLabCut installation tips, organized for clarity. For the most up-to-date information, always check the [official documentation](https://deeplabcut.github.io/DeepLabCut/docs/recipes/installTips.html).*</content>
<parameter name="filePath">/Users/atanugiri/Downloads/dlc-pose-estimation/DeepLabCut_Installation_Guide.md