# Transferring Data from HPC (punakha) to WSL via Mac SSH Tunnel

This document records the steps required to transfer large datasets from the HPC cluster (`punakha`) to a Windows machine running **WSL**, using a Mac as the intermediary SSH tunnel.

---

# Overview of Connection Chain

The transfer path is:

```
punakha (HPC)
   │
   │ reverse SSH tunnel
   ▼
Mac localhost:2222
   │
   │ local SSH forward
   ▼
WSL localhost:22
```

Data flow:

```
HPC → Mac tunnel → Windows/WSL → local drive
```

---

# Step 0: Ensure SSH is Running in WSL

Inside WSL:

```bash
sudo service ssh status
```

If it is not running:

```bash
sudo service ssh start
```

Test locally:

```bash
ssh localhost
```

---

# Step 1: Create Mac → WSL Tunnel

On the **Mac**, open Terminal 1:

```bash
ssh -N -L 2222:localhost:22 automatics_wsl
```

This forwards:

```
Mac:2222 → WSL:22
```

---

# Step 2: Create Reverse Tunnel from HPC

On the **Mac**, open Terminal 2:

```bash
ssh -N -R 2222:localhost:2222 punakha
```

This creates:

```
punakha:2222 → Mac:2222 → WSL:22
```

---

# Step 3: SSH from HPC to WSL (Test)

SSH into the HPC normally and test the tunnel:

```bash
ssh -4 -p 2222 atanugiri@127.0.0.1
```

If this logs into WSL successfully, the tunnel chain is working.

---

# Step 4: Transfer Files Using rsync

Run on **punakha**:

```bash
rsync -avP -e "ssh -4 -p 2222" \
/scratch/agiri/Backup/Black-ChickenBroth-Backup/ \
atanugiri@127.0.0.1:/mnt/e/Atanu/Black-ChickenBroth-Backup/
```

Explanation:

* `-a` : archive mode
* `-v` : verbose
* `-P` : progress + resumable transfers
