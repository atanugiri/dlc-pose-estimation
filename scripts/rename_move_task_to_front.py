#!/usr/bin/env python3
"""
Rename files by moving the task (first animal-like segment) to the front.

Pattern handled:
  <prefix>_<task>_<animal1>_<animal2>_<animal3>_<animal4>_TrialN.mp4

Renamed to:
  <task>_<prefix>_<animal1>_<animal2>_<animal3>_<animal4>_TrialN.mp4

Example:
  10_02_23_S1_P2L1P_ToyRAT_None1_Joey_Bob_Teddy_Trial0.mp4
  -> ToyRAT_10_02_23_S1_P2L1P_None1_Joey_Bob_Teddy_Trial0.mp4

This script operates on a single file or all .mp4 files in a directory (recursively).
Default behaviour is a dry-run; use `--commit` to perform renames.

Options:
  --dry-run, -n    Show what would be done (default if --commit not given)
  --commit         Actually perform the renames
  --force          When committing, overwrite target if it exists

Usage:
  python rename_move_task_to_front.py [path]
  python rename_move_task_to_front.py some_dir/ --dry-run
  python rename_move_task_to_front.py file.mp4 --commit
"""

from pathlib import Path
import argparse
import re
import sys

# Regex captures:
# Try to capture a structured prefix: date_session_treatment (e.g. 10_02_23_S1_P2L1P)
# session and treatment are any non-underscore tokens; if the structured prefix
# doesn't match, fall back to a generic `prefix` capture.
PAT = re.compile(
    r"^(?:(?P<date>\d{2}_\d{2}_\d{2})_(?P<session>[^_]+)_(?P<treatment>[^_]+)|(?P<prefix>.+))_"
    r"(?P<task>[^_]+)_(?P<a1>[^_]+)_(?P<a2>[^_]+)_(?P<a3>[^_]+)_(?P<a4>[^_]+)_(?P<trial>Trial_?\d+)\.(?P<ext>mp4|MP4)$"
)


def rename_file(path: Path, dry_run: bool) -> bool:
    """Attempt to compute and optionally perform a rename for one file.

    Returns True if the file matched and the action (dry or real) succeeded/skipped
    in a benign way; False for errors.
    """
    m = PAT.match(path.name)
    if not m:
        print(f"SKIP (pattern mismatch): {path.name}")
        return False

    # Build a normalized prefix: prefer structured date/session/treatment when available
    gd = m.groupdict()
    if gd.get('date'):
        # collapse underscore between session and treatment: S1_P2 -> S1P2
        norm_prefix = f"{gd['date']}_{gd['session']}{gd['treatment']}"
    else:
        norm_prefix = gd.get('prefix') or ''

    new_name = (
        f"{m.group('task')}_{norm_prefix}_{m.group('a1')}_"
        f"{m.group('a2')}_{m.group('a3')}_{m.group('a4')}_{m.group('trial')}.{m.group('ext')}"
    )
    target = path.with_name(new_name)

    if dry_run:
        print(f"DRY: {path.name} -> {new_name}")
        return True

    # commit by default when not dry-run. Do not overwrite existing targets.
    if target.exists():
        print(f"SKIP (target exists): {path.name} -> {new_name}")
        return False

    try:
        path.rename(target)
        print(f"RENAMED: {path.name} -> {new_name}")
        return True
    except Exception as exc:
        print(f"ERROR renaming {path.name}: {exc}")
        return False


def gather_files(path: Path):
    """Return a list of Path objects to process from the given path.

    If `path` is a directory, all `*.mp4` files inside it and its subdirectories
    are returned (recursive).
    If `path` is a file, a single-item list with that file is returned.
    """
    if path.is_dir():
        return sorted(path.rglob("*.mp4"))
    return [path]


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Move the task segment to the front of matching mp4 filenames"
    )
    parser.add_argument(
        "path",
        nargs='?',
        default='.',
        help="File or directory to process (default: current directory)",
    )
    parser.add_argument("--dry-run", "-n", action="store_true", help="Show actions (dry-run). If omitted, script will perform renames.")

    args = parser.parse_args(argv)

    dry_run = args.dry_run

    path = Path(args.path)
    if not path.exists():
        print(f"ERROR: Path not found: {path}")
        return 2

    files = gather_files(path)
    if not files:
        print(f"No .mp4 files found in: {path}")
        return 0

    total = 0
    successes = 0
    for f in files:
        total += 1
        ok = rename_file(f, dry_run=dry_run)
        if ok:
            successes += 1

    mode = "simulated" if dry_run else "performed"
    print(f"\nSummary: {successes}/{total} {mode}")
    return 0 if successes == total else 1


if __name__ == "__main__":
    sys.exit(main())
