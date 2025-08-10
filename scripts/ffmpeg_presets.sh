#!/usr/bin/env bash
set -euo pipefail
EPI="$1"
OUTDIR="build/${EPI}"
VID="${OUTDIR}/${EPI}_raw.mp4"
FIN="${OUTDIR}/${EPI}.mp4"
SRT="${OUTDIR}/${EPI}.srt"
# Loudness normalize to YouTube-ish -14 LUFS and transcode to H.264/AAC
ffmpeg -y -i "$VID" \
  -filter_complex loudnorm=I=-14:TP=-1.5:LRA=11 \
  -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p \
  -c:a aac -b:a 192k \
  "$FIN"
# Mux captions if present
if [ -f "$SRT" ]; then
  mkvmerge -o "${FIN%.mp4}.mkv" "$FIN" --language 0:eng --track-name 0:"English" "$SRT" || true
fi
# Thumbnail
ffmpeg -y -ss 00:00:02 -i "$FIN" -frames:v 1 "${OUTDIR}/thumb_${EPI}.png"
