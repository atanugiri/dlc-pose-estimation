### Initial Sync or General Update
rsync -avzP . lonestar6:/work/10823/atanugiri2025/ls6/DLC-Black-LightOnly-Atanu-2025-12-13/

### Initial Sync or General Update from Outside Project Folder
rsync -avzP /Users/atanugiri/Downloads/dlc-pose-estimation/DLC-Black-LightOnly-Atanu-2025-12-13 lonestar6:/work/10823/atanugiri2025/ls6/

### Exact Mirror (Deletes Extra Files)
rsync -avzP --delete . lonestar6:/work/10823/atanugiri2025/ls6/DLC-Black-LightOnly-Atanu-2025-12-13/

### Safe Testing (Dry Run)
rsync -avzP --dry-run . lonestar6:/work/10823/atanugiri2025/ls6/DLC-Black-LightOnly-Atanu-2025-12-13/

