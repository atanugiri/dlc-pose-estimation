#!/usr/bin/env python3

import os
import glob
import subprocess
import argparse

def convert_to_grayscale_ffmpeg(input_path, output_path, contrast=1.0, brightness=-0.1):
    """
    Convert a video to grayscale with adjustable contrast and brightness.
    
    Args:
        input_path: Path to input video
        output_path: Path to output video
        contrast: Contrast adjustment (1.0 = no change, <1 = decrease, >1 = increase)
        brightness: Brightness adjustment (0 = no change, negative = darker, positive = brighter)
    """
    cmd = [
        "ffmpeg",
        "-y",  # overwrite output
        "-i", input_path,
        "-vf", f"format=gray,eq=contrast={contrast}:brightness={brightness}",
        "-c:v", "libx264",  # Re-encode with H.264 for better quality
        "-preset", "medium",  # Balance speed/quality
        "-crf", "20",  # High quality (lower = better, 18-23 range)
        output_path
    ]
    subprocess.run(cmd, check=True)

def batch_convert_ffmpeg(input_dir, output_dir, ext="mp4", contrast=1.0, brightness=-0.1):
    """
    Convert all videos in a directory to grayscale.
    
    Args:
        input_dir: Input directory with videos
        output_dir: Output directory for converted videos
        ext: Video file extension to process
        contrast: Contrast adjustment (1.0 = no change)
        brightness: Brightness adjustment (0 = no change)
    """
    os.makedirs(output_dir, exist_ok=True)
    for file in glob.glob(os.path.join(input_dir, f"*.{ext}")):
        filename = os.path.basename(file)
        output_file = os.path.join(output_dir, f"{filename}")
        print(f"Converting {file} -> {output_file}")
        convert_to_grayscale_ffmpeg(file, output_file, contrast=contrast, brightness=brightness)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert video(s) to grayscale with adjustable contrast and brightness",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # Mode selection
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--input", "-i",
        help="Input video file (single file mode)"
    )
    group.add_argument(
        "--input-dir",
        help="Input directory (batch mode)"
    )
    
    # Output paths
    parser.add_argument(
        "--output", "-o",
        help="Output video file (single file mode, required with --input)"
    )
    parser.add_argument(
        "--output-dir",
        help="Output directory (batch mode, default: input_dir + '_gray')"
    )
    
    # Processing options
    parser.add_argument(
        "--ext", "-e",
        default="mp4",
        help="Video file extension for batch mode"
    )
    parser.add_argument(
        "--contrast", "-c",
        type=float,
        default=1.0,
        help="Contrast adjustment (1.0=no change, <1=decrease, >1=increase)"
    )
    parser.add_argument(
        "--brightness", "-b",
        type=float,
        default=-0.1,
        help="Brightness adjustment (0=no change, negative=darker, positive=brighter)"
    )
    
    args = parser.parse_args()
    
    try:
        if args.input:
            # Single file mode
            if not args.output:
                parser.error("--output is required when using --input")
            print(f"Converting single file: {args.input} -> {args.output}")
            print(f"  Contrast: {args.contrast}, Brightness: {args.brightness}")
            convert_to_grayscale_ffmpeg(
                args.input, 
                args.output, 
                contrast=args.contrast, 
                brightness=args.brightness
            )
            print("✓ Conversion complete")
        else:
            # Batch mode
            output_dir = args.output_dir or f"{args.input_dir.rstrip('/')}_gray"
            print(f"Converting batch: {args.input_dir} -> {output_dir}")
            print(f"  Extension: .{args.ext}")
            print(f"  Contrast: {args.contrast}, Brightness: {args.brightness}")
            batch_convert_ffmpeg(
                args.input_dir, 
                output_dir, 
                ext=args.ext, 
                contrast=args.contrast, 
                brightness=args.brightness
            )
            print("✓ Batch conversion complete")
    except Exception as e:
        print(f"Error: {e}")
        exit(1)