#!/usr/bin/env bash
# 参考视频客观探测 —— RSI 评估的 S2 阶段
# 输出：规格、切点表、镜头时长统计、分段切换密度、响度、静音、黑场/冻帧、
#       亮度/饱和度统计、全片与开场抽帧拼图、汇总 metrics.csv
# 用法: bash reference_probe.sh <参考视频> [输出目录，默认 ./probe_out]
# 实测环境: ffmpeg / ffprobe 8.1.2 (Windows, Git Bash)
#
# 注意：本机 Windows 下 metadata=print:file=绝对路径 会因盘符冒号被滤镜解析器误判，
#       因此一律把元数据打到 stderr 再解析，不落盘中间元数据文件。
#
# 本脚本只提供 E1 客观证据。A/B/C 三维度的「推断」与「动作项」必须由人工填写评估表。

set -u
IN="${1:-}"
OUT="${2:-./probe_out}"

if [ -z "$IN" ] || [ ! -f "$IN" ]; then
  echo "Usage: bash reference_probe.sh <reference_video> [output_dir]"
  echo "Example: bash reference_probe.sh ref.mp4 ./case001"
  exit 1
fi

mkdir -p "$OUT" || { echo "Cannot create output dir: $OUT"; exit 1; }
L="$OUT/probe.log"
M="$OUT/metrics.csv"
: > "$L"
printf 'metric,value,unit,source\n' > "$M"

log() { printf '%s\n' "$*" | tee -a "$L"; }
metric() { printf '%s,%s,%s,%s\n' "$1" "$2" "$3" "$4" | tee -a "$L" >> "$M"; }
avg() { awk '{s+=$1;n++} END{if(n>0) printf "%.3f", s/n; else printf "NA"}' "$1"; }

log "=== Reference Probe | $(date '+%Y-%m-%d %H:%M:%S') | $IN ==="
log "tool: $(ffmpeg -version 2>/dev/null | head -1)"
log "NOTE: E1 evidence only. Fill 评估表.md for inference and action items."
log ""

# ---------- 1. 规格 ----------
log "--- 1. container / stream spec ---"
ffprobe -v error -show_entries \
  "stream=index,codec_type,codec_name,width,height,pix_fmt,r_frame_rate,avg_frame_rate,sample_rate,channels:format=format_name,duration,size,bit_rate" \
  -of json "$IN" > "$OUT/probe.json" 2>>"$L"
cat "$OUT/probe.json" | tee -a "$L"
DUR="$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$IN" 2>/dev/null | head -1)"
DUR="${DUR:-0}"
metric "duration" "$DUR" "s" "ffprobe"
metric "width" "$(ffprobe -v error -select_streams v:0 -show_entries stream=width -of csv=p=0 "$IN" 2>/dev/null | head -1)" "px" "ffprobe"
metric "height" "$(ffprobe -v error -select_streams v:0 -show_entries stream=height -of csv=p=0 "$IN" 2>/dev/null | head -1)" "px" "ffprobe"
metric "fps" "$(ffprobe -v error -select_streams v:0 -show_entries stream=avg_frame_rate -of csv=p=0 "$IN" 2>/dev/null | head -1)" "ratio" "ffprobe"
log "[spec] $OUT/probe.json"
log ""

# ---------- 2. 切点表 ----------
log "--- 2. cut points (select scene > 0.25 + showinfo) ---"
ffmpeg -hide_banner -nostdin -i "$IN" \
  -vf "select='gt(scene,0.25)',showinfo" -an -f null - 2>&1 \
  | grep -o 'pts_time:[0-9.]*' | cut -d: -f2 > "$OUT/cuts.txt" || true
CUTN="$(wc -l < "$OUT/cuts.txt" | tr -d ' ')"
log "[cuts] $CUTN candidate cut points -> $OUT/cuts.txt"
head -30 "$OUT/cuts.txt" | tee -a "$L"
if [ "$CUTN" -gt 30 ]; then log "  ... (full list in cuts.txt)"; fi
metric "cut_count" "$CUTN" "count" "select scene>0.25"
log "  !! 快速摇镜/闪光可能误报；请与抽帧拼图交叉验证后再用于 A3/A9"
log ""

# ---------- 3. 镜头时长统计 ----------
log "--- 3. shot length distribution ---"
awk -v dur="$DUR" 'BEGIN{prev=0} {d=$1-prev; if(d>0) print d; prev=$1} END{d=dur-prev; if(d>0) print d}' \
  "$OUT/cuts.txt" > "$OUT/shot_lengths.txt"
SHOTN="$(wc -l < "$OUT/shot_lengths.txt" | tr -d ' ')"
SORTED="$OUT/.sorted"
sort -n "$OUT/shot_lengths.txt" > "$SORTED"
STATS="$(awk '{a[NR]=$1; s+=$1} END{
  if(NR==0){print "NA NA NA NA NA"; exit}
  med = (NR%2) ? a[(NR+1)/2] : (a[NR/2]+a[NR/2+1])/2;
  p = int(NR*0.9); if(p<1)p=1; if(p>NR)p=NR;
  printf "%.3f %.3f %.3f %.3f %.3f", s/NR, med, a[p], a[1], a[NR]
}' "$SORTED")"
set -- $STATS
log "[shots] n=$SHOTN  mean=$1 s  median=$2 s  p90=$3 s  min=$4 s  max=$5 s"
log "[shots] 长尾分布下以 median 为节奏代表，不要用 mean（见 02 卷 A1）"
metric "shot_count" "$SHOTN" "count" "computed"
metric "shot_mean_s" "$1" "s" "computed"
metric "shot_median_s" "$2" "s" "computed"
metric "shot_p90_s" "$3" "s" "computed"
log ""

# ---------- 4. 分段切换密度 ----------
log "--- 4. cut density by quarter ---"
DENSITY="$(awk -v dur="$DUR" 'BEGIN{if(dur<=0)dur=1} {q=int($1/(dur/4))+1; if(q>4)q=4; if(q<1)q=1; c[q]++} END{for(i=1;i<=4;i++) printf "Q%d=%.1f ", i, c[i]/(dur/4)*60}' "$OUT/cuts.txt")"
log "[density] $DENSITY (cuts/min, 4 equal quarters)"
DPM="$(awk -v n="$CUTN" -v d="$DUR" 'BEGIN{if(d>0) printf "%.1f", n/d*60; else print "NA"}')"
metric "cut_density_per_min" "$DPM" "cuts/min" "computed"
log ""

# ---------- 5. 画面异常 ----------
log "--- 5. black / frozen frames ---"
ffmpeg -hide_banner -nostdin -i "$IN" -an \
  -vf "blackdetect=d=0.5:pix_th=0.10:pic_th=0.98,freezedetect=n=-60dB:d=2" \
  -f null - 2>&1 | grep -E "black_start|black_end|freeze_start|freeze_end" | tee -a "$L" || true
log "[video] 刻意黑场/静止画面会误报，需人工确认"
log ""

# ---------- 6. 音频 ----------
HAS_AUDIO="$(ffprobe -v error -select_streams a -show_entries stream=index -of csv=p=0 "$IN" 2>/dev/null | head -1)"
if [ -n "$HAS_AUDIO" ]; then
  log "--- 6a. loudness (EBU R128 ref; read Summary) ---"
  ffmpeg -hide_banner -nostdin -i "$IN" -vn -af "ebur128=peak=true" -f null - 2>&1 \
    | sed -n '/Summary:/,$p' | head -22 > "$OUT/loudness.txt"
  cat "$OUT/loudness.txt" | tee -a "$L"
  ILUF="$(grep -m1 -E '^\s*I:' "$OUT/loudness.txt" | awk '{print $2}')"
  TPK="$(grep -m1 -E '^\s*Peak:' "$OUT/loudness.txt" | awk '{print $2}')"
  metric "integrated_lufs" "${ILUF:-NA}" "LUFS" "ebur128 Summary"
  metric "true_peak" "${TPK:-NA}" "dBFS/dBTP" "ebur128 Summary"
  log ""

  log "--- 6b. silence intervals ---"
  ffmpeg -hide_banner -nostdin -i "$IN" -vn -af "silencedetect=noise=-40dB:d=0.5" -f null - 2>&1 \
    | grep -E "silence_start|silence_end" | tee -a "$L" > "$OUT/silence.txt"
  cat "$OUT/silence.txt" | tee -a "$L"
  log "[silence] 必须人工区分「刻意留白」与「缺音」，见 02 卷 B9"
  log ""

  log "--- 6c. voice band level (300-3400 Hz) ---"
  ffmpeg -hide_banner -nostdin -i "$IN" -vn -af "highpass=f=300,lowpass=f=3400,volumedetect" -f null - 2>&1 \
    | grep -E "mean_volume|max_volume" | tee -a "$L" || true
else
  log "[audio] NO AUDIO TRACK — B 维度需降级，且不得用参考片音轨顶替"
fi
log ""

# ---------- 7. 色彩统计（每秒抽 1 帧） ----------
log "--- 7. color stats (1 sample/sec, signalstats) ---"
for K in YAVG SATAVG; do
  LC="$(printf '%s' "$K" | tr 'A-Z' 'a-z')"
  ffmpeg -hide_banner -nostdin -i "$IN" -an \
    -vf "fps=1,signalstats,metadata=print:key=lavfi.signalstats.$K" -f null - 2>&1 \
    | grep "lavfi.signalstats.$K=" | sed 's/.*=//' > "$OUT/$LC.txt" || true
  V="$(avg "$OUT/$LC.txt")"
  log "[$K] mean=$V  (samples=$(wc -l < "$OUT/$LC.txt" | tr -d ' ')) -> $OUT/$LC.txt"
  metric "$LC" "$V" "level" "signalstats fps=1"
done
log "[color] 数值为相对倾向，跨片比较需同色彩空间与同曝光条件"
log ""

# ---------- 8. 抽帧拼图 ----------
log "--- 8. contact sheets ---"
ffmpeg -hide_banner -nostdin -loglevel error -i "$IN" \
  -vf "fps=1/5,scale=320:-1,tile=5x5" -frames:v 1 -update 1 "$OUT/sheet_overview.png" 2>&1 | tee -a "$L"
[ -f "$OUT/sheet_overview.png" ] && log "[sheet] 全片概览(每 5 s 一格, 25 格): $OUT/sheet_overview.png" || log "[sheet] overview FAILED"
ffmpeg -hide_banner -nostdin -loglevel error -t 15 -i "$IN" \
  -vf "fps=1,scale=320:-1,tile=5x3" -frames:v 1 -update 1 "$OUT/sheet_opening.png" 2>&1 | tee -a "$L"
[ -f "$OUT/sheet_opening.png" ] && log "[sheet] 开场 15 s(每 1 s 一格): $OUT/sheet_opening.png" || log "[sheet] opening FAILED"
log ""

log "=== PROBE DONE ==="
log "E1 客观证据已就绪：$M"
log "人工必做：全片通看 2 遍(画面/声音各一)、关键段逐帧、A/B/C 各 10 项四段式说明、G 过滤器打标。"
log "然后填写 references/08-RSI自进化/模板/参考视频评估表.md，产出风格指纹，并在 S6 取得用户确认后才可开剪。"
log "=== log: $L ==="
rm -f "$SORTED"
