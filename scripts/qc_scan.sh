#!/usr/bin/env bash
# Delivery technical QC helper - automated L1 checks only, it does not replace human review.
# Usage: bash qc_scan.sh <video_file> [log_dir, default ./qc_logs]
# Tested on: ffmpeg / ffprobe 8.1.2 (Windows, Git Bash)
set -u

IN="${1:-}"
OUT="${2:-./qc_logs}"

if [ -z "$IN" ] || [ ! -f "$IN" ]; then
  echo "Usage: bash qc_scan.sh <video_file> [log_dir]"
  echo "Example: bash qc_scan.sh final_v03.mp4 ./qc_logs"
  exit 1
fi

mkdir -p "$OUT" || { echo "Cannot create log dir: $OUT"; exit 1; }
B="$(basename "$IN")"
L="$OUT/${B}.qc.log"
: > "$L"

log() { printf '%s\n' "$*" | tee -a "$L"; }

log "=== QC Report | $(date '+%Y-%m-%d %H:%M:%S') | $IN ==="
log "tool: $(ffmpeg -version 2>/dev/null | head -1)"
log ""

log "--- 1. container / stream spec ---"
ffprobe -v error -show_entries \
  "stream=index,codec_type,codec_name,profile,width,height,pix_fmt,field_order,color_space,color_transfer,color_primaries,r_frame_rate,avg_frame_rate,sample_rate,channels,channel_layout,bit_rate:format=format_name,duration,size,bit_rate" \
  -of json "$IN" > "$OUT/${B}.probe.json" 2>>"$L"
cat "$OUT/${B}.probe.json" | tee -a "$L"
log "[spec] saved: $OUT/${B}.probe.json"
log ""

log "--- 2. decode integrity (-xerror; empty output = clean) ---"
ffmpeg -hide_banner -nostdin -v error -xerror -i "$IN" -f null - 2>&1 | tee -a "$L"
log "[decode] if nothing above, full-file decode is clean"
log ""

log "--- 3. black frames / frozen frames ---"
ffmpeg -hide_banner -nostdin -i "$IN" -an \
  -vf "blackdetect=d=0.5:pix_th=0.10:pic_th=0.98,freezedetect=n=-60dB:d=2" \
  -f null - 2>&1 | grep -E "black_start|black_end|freeze_start|freeze_end|Error|error" | tee -a "$L" || true
log "[video] no intervals listed = none found; intentional black/still frames must be confirmed by a human"
log ""

HAS_AUDIO="$(ffprobe -v error -select_streams a -show_entries stream=index -of csv=p=0 "$IN" 2>/dev/null | head -1)"

if [ -n "$HAS_AUDIO" ]; then
  log "--- 4. silence intervals ---"
  ffmpeg -hide_banner -nostdin -i "$IN" -vn \
    -af "silencedetect=noise=-40dB:d=0.5" -f null - 2>&1 \
    | grep -E "silence_start|silence_end|Error|error" | tee -a "$L" || true
  log "[silence] no intervals listed = none found"
  log ""

  log "--- 5. loudness (EBU R128 reference; read the final Summary) ---"
  ffmpeg -hide_banner -nostdin -i "$IN" -vn \
    -af "ebur128=peak=true" -f null - 2>&1 \
    | sed -n '/Summary:/,$p' | head -25 | tee -a "$L"
  log ""

  log "--- 6. voice-band level (300-3400 Hz) ---"
  ffmpeg -hide_banner -nostdin -i "$IN" -vn \
    -af "highpass=f=300,lowpass=f=3400,volumedetect" -f null - 2>&1 \
    | grep -E "mean_volume|max_volume" | tee -a "$L" || true
  log "[voice] low level here means possible missing narration - listen to confirm"
else
  log "[audio] NO AUDIO TRACK FOUND - if delivery requires audio, this item FAILS"
fi
log ""

log "--- 7. contact sheet (one frame per 10 s, 4x6 grid) ---"
SHEET="$OUT/${B}.sheet.png"
ffmpeg -hide_banner -nostdin -loglevel error -i "$IN" \
  -vf "fps=1/10,scale=320:-1,tile=4x6" -frames:v 1 -update 1 "$SHEET" 2>&1 | tee -a "$L"
if [ -f "$SHEET" ]; then log "[sheet] $SHEET"; else log "[sheet] FAILED to generate"; fi
log ""

log "=== AUTO CHECK DONE ==="
log "Still REQUIRED by a human: A/V sync, subtitle proofreading & timing,"
log "content compliance & rights clearance, first/last frame, full-length viewing."
log "See references/06-delivery-qc/02-content-and-compliance-review.md and 03-qc-report-templates.md."
log "=== full log: $L ==="
