#!/bin/bash

input="$1"

if [[ ! -f "$input" ]]; then
    echo "Usage: $0 <video_file>"
    exit 1
fi

dir=$(dirname "$input")
filename=$(basename "$input")
base="${filename%.*}"

outdir="$dir/$base"
mkdir -p "$outdir"

ffmpeg -i "$input" \
-filter_complex \
"[0:v]crop=iw/2:ih/2:0:0[tl]; \
 [0:v]crop=iw/2:ih/2:iw/2:0[tr]; \
 [0:v]crop=iw/2:ih/2:0:ih/2[bl]; \
 [0:v]crop=iw/2:ih/2:iw/2:ih/2[br]" \
-map "[tl]" -c:v libx264 -crf 18 "$outdir/${base}_top_left.mp4" \
-map "[tr]" -c:v libx264 -crf 18 "$outdir/${base}_top_right.mp4" \
-map "[bl]" -c:v libx264 -crf 18 "$outdir/${base}_bottom_left.mp4" \
-map "[br]" -c:v libx264 -crf 18 "$outdir/${base}_bottom_right.mp4"