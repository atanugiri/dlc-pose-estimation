#!/usr/bin/env python3
import os
import subprocess
import argparse


def split_video_to_quadrants(input_path, output_dir=None, dry_run=False, overwrite=False):
    """Split a video into 4 quadrants using ffmpeg.
    
    Args:
        input_path: Path to input video file
        output_dir: Directory for output files (defaults to input file's directory)
        dry_run: If True, only print commands without executing
        overwrite: If True, overwrite existing output files
    
    Creates 4 files named: top_left.mp4, top_right.mp4, bottom_left.mp4, bottom_right.mp4
    """
    if not os.path.exists(input_path):
        print(f"Error: Input file not found: {input_path}")
        return
    
    if output_dir is None:
        output_dir = os.path.dirname(os.path.abspath(input_path))
    os.makedirs(output_dir, exist_ok=True)
    
    ext = os.path.splitext(input_path)[1] or '.mp4'
    
    # Define quadrants with their crop filters
    quadrants = {
        'top_left':    'crop=in_w/2:in_h/2:0:0',           # top-left
        'top_right':   'crop=in_w/2:in_h/2:in_w/2:0',      # top-right
        'bottom_left': 'crop=in_w/2:in_h/2:0:in_h/2',      # bottom-left
        'bottom_right':'crop=in_w/2:in_h/2:in_w/2:in_h/2'  # bottom-right
    }
    
    for name, crop_filter in quadrants.items():
        output_filename = f"{name}{ext}"
        output_path = os.path.join(output_dir, output_filename)
        
        if os.path.exists(output_path) and not overwrite:
            print(f"Skipping (file exists): {output_path}")
            continue
        
        cmd = [
            'ffmpeg',
            '-y',  # overwrite output files
            '-i', input_path,
            '-filter:v', crop_filter,
            '-c:a', 'copy',  # copy audio stream
            output_path
        ]
        
        print(f"Creating {name}: {output_path}")
        if dry_run:
            print(f"  Command: {' '.join(cmd)}")
            continue
        
        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            print(f"  ✓ Created {output_filename}")
        except subprocess.CalledProcessError as e:
            print(f"  ✗ Error creating {output_filename}: {e.stderr}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Split a video into 4 quadrants')
    parser.add_argument('input', help='Input video file path')
    parser.add_argument('-o', '--output', help='Output directory (default: input file directory)')
    parser.add_argument('-n', '--dry-run', action='store_true', help='Show commands without executing')
    parser.add_argument('--overwrite', action='store_true', help='Overwrite existing output files')
    
    args = parser.parse_args()
    
    split_video_to_quadrants(args.input, output_dir=args.output, dry_run=args.dry_run, overwrite=args.overwrite)
