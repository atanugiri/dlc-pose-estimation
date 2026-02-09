#!/usr/bin/env python3
import os
import argparse

DEFAULT_EXTS = ['.mp4', '.avi', '.mov', '.mkv']
PREFIX = 'ChocolateMilk_'


def prepend_prefix_to_file(path, prefix=PREFIX, dry_run=False):
    dirn = os.path.dirname(path)
    name = os.path.basename(path)
    if name.startswith(prefix):
        print(f"Skipping (already prefixed): {path}")
        return
    new_name = prefix + name
    new_path = os.path.join(dirn, new_name)
    if os.path.exists(new_path):
        print(f"Target exists, skipping: {new_path}")
        return
    print(f"Rename: '{path}' -> '{new_path}'")
    if not dry_run:
        os.rename(path, new_path)


def walk_and_prepend(folder, exts=None, prefix=PREFIX, dry_run=False):
    if exts is None:
        exts = DEFAULT_EXTS
    exts = [e.lower() for e in exts]
    for root, dirs, files in os.walk(folder):
        for f in files:
            if os.path.splitext(f)[1].lower() in exts:
                full = os.path.join(root, f)
                try:
                    prepend_prefix_to_file(full, prefix=prefix, dry_run=dry_run)
                except Exception as e:
                    print(f"Failed: {full} -> {e}")


if __name__ == '__main__':
    p = argparse.ArgumentParser(description='Prepend a prefix to video files recursively')
    p.add_argument('folder', help='Folder to process')
    p.add_argument('-n', '--dry-run', action='store_true', help='Show changes but do not rename')
    p.add_argument('--prefix', default=PREFIX, help='Prefix to add')
    p.add_argument('--exts', nargs='*', help='File extensions to include (e.g. .mp4 .avi)')
    args = p.parse_args()

    walk_and_prepend(args.folder, exts=args.exts, prefix=args.prefix, dry_run=args.dry_run)
