# Technical Specifications Checklist (Technical QC)

> Category: Delivery QC | Topic: pre-delivery verification of technical specifications and automated anomaly detection | Compiled: 2026-11-10 | Applies to: the first gate after any final export; verified on local ffmpeg / ffprobe 8.1.2

> ⚠️ This document covers **technical specifications** only and is not legal advice. Passing automated checks does not mean the content is compliant or that the rights position is clean; run `02-content-and-compliance-review.md` in parallel.

> ⚠️ Automated checks can only find anomalies that can be described algorithmically (black frames, silence, freeze frames, loudness, decode errors). **A/V sync, subtitle typos, content compliance, rights clearance and how the film actually feels must be checked by a human** — see `02-content-and-compliance-review.md`. No errors reported ≠ a deliverable that is fit to ship.

---

## 1. Review layers

| Layer | Method | Finds | Cannot find |
| --- | --- | --- | --- |
| L1 Automated | ffprobe / ffmpeg filters | Specification mismatches, encoding errors, black frames, silence, freeze frames, loudness overshoot | Semantic errors, aesthetic problems |
| L2 Semi-automated | Frame-extraction contact sheets, waveform displays, scopes | On-screen goofs, framing that drifts out of bounds, subtitles covering the picture, clipping | Narrative pacing, logic |
| L3 Manual | Full-length viewing plus item-by-item check against the QC report | A/V sync drift, typos, factual errors, compliance risk | — |
| L4 Delivery validation | Real-device playback / upload preview on the target platform | Picture quality after transcoding, level re-normalised by the platform, subtitle compatibility | — |

Principle: **scan the whole film at L1 first, then watch the whole film at L3**. If any L1 check fails, there is no point moving on to L2/L3 — send it back for re-export first.

---

## 2. Specification checklist (tick each line against the delivery sheet)

| Item | Typical requirement | Measurement command / basis |
| --- | --- | --- |
| Container | MP4 / MOV / MXF (per the delivery sheet) | `format_name` |
| Video codec | H.264 / H.265 / ProRes / DNxHR | `codec_name`, `profile` |
| Resolution | 1920×1080, 3840×2160, 1080×1920 (vertical) | `width`, `height` |
| Aspect ratio | 16:9 / 9:16 / 1:1 / 2.39:1 (must match the matte) | `display_aspect_ratio` + visual check |
| Frame rate | 25 / 30 / 50 / 60 / 23.976 / 24 / 29.97 fps, constant across the whole film | `r_frame_rate` and `avg_frame_rate` must agree |
| Scanning | Progressive | `field_order` should be `progressive` / unknown |
| Pixel format and bit depth | yuv420p 8-bit (general); yuv422p10le (master) | `pix_fmt` |
| Colour tags | Colour space / transfer / primaries all tagged (e.g. bt709/bt709/bt709) | `color_space`, `color_transfer`, `color_primaries` |
| Bitrate | Per platform or master spec (VBR ceiling / CBR) | `bit_rate`, `format.bit_rate` |
| Keyframe interval | Usually 1–2 seconds (GOP ≈ fps × 1~2) | Frame sampling / `ffprobe -show_frames` |
| Audio codec | AAC-LC / PCM / Opus | `codec_name` |
| Audio format | 48 kHz / 24-bit (production), 48 kHz AAC ≥192 kbps (delivery) | `sample_rate`, `bit_rate` |
| Channels | Stereo 2.0 / 5.1, channel order correct | `channels`, `channel_layout` |
| Loudness | Broadcast −23 LUFS ±1 / −1 dBTP; streaming −14 to −16 LUFS / −1 to −2 dBTP | `ebur128=peak=true` |
| Duration | Within ≤ 1 frame of the delivery sheet; state whether bars and black are included | `format.duration` |
| Subtitles | Sidecar SRT/ASS in the same language as the picture; timeline must not run past the end of the film | see `03-subtitles/03` |
| Head and tail | First frame not black (unless designed that way), no abrupt cut-off at the end, no stray tail frames | Visual check + `blackdetect` |
| File naming | Follows the `project_version_date_spec` convention, with no compatibility problems from non-ASCII characters or spaces | see `01-editing-craft/03` |

### Getting every specification in one command

```bash
ffprobe -v error -show_entries \
  stream=index,codec_type,codec_name,profile,width,height,pix_fmt,field_order,color_space,color_transfer,color_primaries,r_frame_rate,avg_frame_rate,sample_rate,channels,channel_layout,bit_rate:format=format_name,duration,size,bit_rate \
  -of json "out.mp4"
```

---

## 3. L1 automated checks (every command verified on local ffmpeg 8.1.2)

### 3.1 Decode integrity

```bash
ffmpeg -hide_banner -nostdin -v error -xerror -i "out.mp4" -f null -
```

No output at all means the whole file decodes cleanly. Any output means corrupted frames / timestamp anomalies / encoding that runs out of range — locate the timecode and re-export.

### 3.2 Black frames and freeze frames

```bash
ffmpeg -hide_banner -nostdin -i "out.mp4" -an \
  -vf "blackdetect=d=0.5:pix_th=0.10:pic_th=0.98,freezedetect=n=-60dB:d=2" \
  -f null - 2>&1 | grep -E "black_start|black_end|freeze_start|freeze_end|Error"
```

- `d=0.5`: only reports once black lasts ≥0.5 seconds; deliberately designed black transitions should be shortened or whitelisted.
- `pix_th=0.10`: pixel brightness threshold; `pic_th=0.98`: a frame is judged black only when 98% of its pixels qualify.
- `freezedetect n=-60dB:d=2`: −60 dB noise tolerance, 2 seconds or longer counts as frozen. **Static shots (slides, stills, title cards) will produce false positives and must be confirmed by a human**.

### 3.3 Silence

```bash
ffmpeg -hide_banner -nostdin -i "out.mp4" -vn \
  -af "silencedetect=noise=-40dB:d=0.5" -f null - 2>&1 | grep -E "silence_start|silence_end"
```

Threshold −40 dB / 0.5 seconds. Note: if there is a continuous noise floor, silence will never be detected; **no detected silence does not mean anyone is speaking** — also check the 300–3400 Hz speech band:

```bash
ffmpeg -hide_banner -nostdin -i "out.mp4" -vn \
  -af "highpass=f=300,lowpass=f=3400,volumedetect" -f null - 2>&1 | grep -E "mean_volume|max_volume"
```

### 3.4 Loudness and true peak

```bash
ffmpeg -hide_banner -nostdin -i "out.mp4" -vn -af "ebur128=peak=true" -f null - 2>&1 | sed -n '/Summary:/,$p'
```

Read `I:` (Integrated, LUFS), `LRA:` (loudness range) and `Peak:` (true peak) from `Summary`. For pass/fail criteria see `02-audio-and-voice/02-audio-post-and-mixing.md`:

| Delivery target | Target Integrated | True peak ceiling | Basis |
| --- | --- | --- | --- |
| European broadcast | −23 LUFS ±1 (±0.5 recommended for file delivery) | −1 dBTP | EBU R128 / ITU-R BS.1770 |
| US broadcast | −24 LKFS ±2 | −2 dBTP | ATSC A/85 / CALM Act |
| Streaming, general | −14 to −16 LUFS (differs per platform) | −1 to −2 dBTP | Platform specs, must be re-checked |

### 3.5 Everything in one pass (audio and video split, so it does not fail when there is no audio track)

```bash
ffmpeg -hide_banner -nostdin -i "out.mp4" -filter_complex \
  "[0:v]blackdetect=d=0.5:pix_th=0.10,freezedetect=n=-60dB:d=2[v];[0:a]silencedetect=noise=-40dB:d=0.5,ebur128=peak=true[a]" \
  -map "[v]" -map "[a]" -f null - 2> qc.log
```

> This combination requires the source to carry **both a video stream and an audio stream**; if either is missing it fails. For day-to-day batch QC, use the bundled `qc_scan.sh`, which checks whether an audio track exists before branching. Filter logs go to **stderr**, and **stderr output does not mean the run failed**.

### 3.6 Frame-extraction contact sheet (L2)

```bash
ffmpeg -hide_banner -nostdin -loglevel error -i "out.mp4" \
  -vf "fps=1/10,scale=320:-1,tile=4x6" -frames:v 1 -update 1 "sheet.png"
```

One frame every 10 seconds, tiled into 4×6 = 24 cells, covering roughly 4 minutes; for longer films lower the `fps` value (e.g. `1/30`). Use it to spot goofs, wrong mattes, subtitles running out of frame and abrupt picture changes quickly.

---

## 4. L3 checks a human must do

1. **A/V sync**: find 3 obvious closing actions (a door, a clap, a strike) and 3 onsets of dialogue; lip-sync error is measured in frames, and more than 2 frames is perceptible.
2. **Full viewing**: 1.0× speed from start to finish, no skipping; log timecode plus a description of each problem.
3. **Subtitles**: typos, line breaks, overlapping timings, cues that dwell too briefly, whether the last cue runs past the end of the film, whether burned-in subtitles are covered by the UI.
4. **Audio**: listen to the whole film on headphones; check for clipping, sibilance, sudden noise-floor jumps, out-of-phase left and right channels, and music burying the voice.
5. **Shadows and highlights**: watch once on an ordinary monitor and once on a phone; confirm shadows have not crushed into one flat mass and that subtitles stay legible over bright backgrounds.
6. **First frame and thumbnail**: is the frame the platform grabs by default usable; does the thumbnail text sit inside the safe area.
7. **Live test on the target platform**: upload and preview; check picture quality after platform transcoding, level normalisation, and whether subtitles get compressed a second time.

---

## 5. Common errors and troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| `blackdetect` reports a lot of black | Deliberate black at head and tail, dark scenes | Confirm against timecode manually, whitelist them, or adjust `d`/`pix_th` |
| `freezedetect` false positives | Still photos, static slides, title cards | Confirm manually; exclude that section from detection if needed |
| No silence detected | Continuous noise floor / compression noise | Raise the `noise` threshold (e.g. −35 dB) and run a speech-band check |
| `ebur128` values keep jumping | You are reading intermediate output instead of the final `Summary` | Always go by `I` in `Summary` |
| `r_frame_rate` ≠ `avg_frame_rate` | Variable frame rate (VFR) source | Force a constant frame rate on export: `-vsync cfr` / `-fps_mode cfr` |
| Colour looks washed out or oversaturated | Colour tags missing or tagged wrongly | Write them explicitly with `-colorspace bt709 -color_primaries bt709 -color_trc bt709` |
| Level drops after platform upload | Platform re-normalisation | Master to the platform's target loudness instead of brute-forcing it louder |
| Combined filter graph reports `Invalid stream specifier` | Source has no audio track | Run two separate commands, or use `qc_scan.sh` |
| Automated checks all green but the client rejects it | Only L1 was done | Add the L3 full viewing and the compliance review |

---

## 6. Pre-delivery quick checklist

- [ ] All 16 items in the specification table checked against the delivery sheet; unknown items marked "to be confirmed" instead of being filled in with guesses
- [ ] Decode integrity with `-xerror` produces no output
- [ ] Every black-frame / freeze-frame / silence interval has been played back and confirmed
- [ ] Integrated loudness and true peak are within spec; the `Summary` values are recorded
- [ ] Frame-extraction contact sheet reviewed: no goofs, nothing running out of frame, no matte errors
- [ ] Whole film watched at 1.0×; A/V sync spot-checked at 6 points
- [ ] Full subtitle text proofread; last cue does not run past the end
- [ ] Whole film listened to on headphones: no clipping / noise-floor jumps / channel errors
- [ ] First frame, thumbnail and ending are usable
- [ ] The rights and content gate in `02-content-and-compliance-review.md` has been passed
- [ ] Upload preview on the target platform verified
- [ ] Results entered in `03-qc-report-templates.md`, with signatory, date and version number complete

---

## References

- FFmpeg Filters Documentation (blackdetect / freezedetect / silencedetect / ebur128 / tile): https://ffmpeg.org/ffmpeg-filters.html
- FFmpeg `ffprobe` Documentation: https://ffmpeg.org/ffprobe.html
- EBU R 128 (2020) official PDF: https://tech.ebu.ch/files/live/sites/tech/files/shared/r/r128v4_0.pdf
- EBU Tech 3343 implementation guide: https://tech.ebu.ch/files/live/sites/tech/files/shared/tech/tech3343v2_0.pdf
- BBC R&D White Paper WHP 202 (loudness terminology): http://downloads.bbc.co.uk/rd/pubs/whp/whp-pdf-files/WHP202.pdf
- FFmpeg tutorial on black-frame / silence / freeze detection (combined filter graphs and stderr behaviour): https://yololab.net/archives/ffmpeg-video-qc-blackdetect-silencedetect-freezedetect-guide
- Hands-on notes on combining FFmpeg analysis filters (scdet / signalstats / blurdetect): https://blog.gitcode.com/60f14ae685220cef79ff1a1dcfa34c46.html
- Video Quality Inspector (blackdetect / freezedetect threshold examples): https://www.huntapi.com/toolbox/ffmpeg-quality-inspector

Retrieved: 2026-11-10. Environment in which the commands were verified: ffmpeg 8.1.2 (Gyan.FFmpeg full build, Windows).
