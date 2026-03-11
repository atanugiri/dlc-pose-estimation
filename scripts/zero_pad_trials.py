import re
import argparse
from pathlib import Path


def zero_pad_trials(folder, dry_run=False):
    pattern = re.compile(r"Trial_(\d+)")
    root = Path(folder)

    for old_path in sorted(root.rglob("*")):
        match = pattern.search(old_path.name)

        if match:
            trial_num = int(match.group(1))
            new_name = pattern.sub(f"Trial_{trial_num:02d}", old_path.name)

            if new_name != old_path.name:
                new_path = old_path.parent / new_name

                if dry_run:
                    print(f"[dry-run] {old_path.relative_to(root)} → {new_path.relative_to(root)}")
                else:
                    old_path.rename(new_path)
                    print(f"{old_path.relative_to(root)} → {new_path.relative_to(root)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Zero-pad Trial numbers in filenames (e.g. Trial_1 → Trial_01)."
    )
    parser.add_argument("folder", help="Path to the folder containing the files to rename.")
    parser.add_argument("--dry-run", action="store_true", help="Preview renames without making any changes.")
    args = parser.parse_args()

    zero_pad_trials(args.folder, dry_run=args.dry_run)