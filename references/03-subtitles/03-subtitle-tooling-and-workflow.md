# Subtitle Tooling and Workflow

> Category: Subtitles | Topic: Subtitle tooling, speech-to-text, forced alignment, ffmpeg muxing and QC | Compiled: 2026-11-10 | Applies to: Building an end-to-end pipeline from raw audio and video to a deliverable subtitle file

## 1. Core principles / concept comparison

A deliverable subtitle pipeline always runs through seven stages, and tool selection is really about **picking the best executor for each stage** rather than finding one application that does everything:

| Stage | Input → output | Primary tool | Acceptance point |
| --- | --- | --- | --- |
| ① Audio extraction | Video → 16k mono WAV | ffmpeg | Sample rate and channel count correct |
| ② Speech-to-text (ASR) | Audio → timestamped text | Whisper / faster-whisper / CapCut (剪映) | Word accuracy, proper nouns and numbers |
| ③ Forced alignment | Known transcript + audio → word-level timestamps | WhisperX / MFA / stable-ts | Word-boundary precision |
| ④ Line breaking and timing | Long text → standards-compliant cues | Aegisub / Subtitle Edit / Arctime | Semantic integrity, CPS within limits |
| ⑤ Human proofreading | Draft → final text | Three-tier review | Typos, negations, terminology |
| ⑥ Styling and translation | Final text → ASS / bilingual | Aegisub / Subtitle Edit | Consistent styling, balanced two-line stack |
| ⑦ Muxing / encoding / QC | Subtitles → finished file | ffmpeg + QC scripts | Tracks, codecs, language tags |

**ASR and forced alignment are two different things**; treating them as one sets the wrong expectations:

| Dimension | ASR (transcription) | Forced alignment |
| --- | --- | --- |
| Problem being solved | Guessing which words were spoken | The transcript is known; only the position of each word in the audio is needed |
| Output granularity | Segment-level timestamps | Word-level / phoneme-level timestamps |
| Typical error | Segment boundaries may drift by hundreds of milliseconds to several seconds | About ±20-50 ms on clean speech (third-party figure, marked TO VERIFY) |
| Representative tools | Whisper, faster-whisper, CapCut (剪映) | WhisperX (wav2vec2), MFA, Gentle, aeneas, stable-ts |
| Used for | Generating a transcript from scratch | Upgrading the timeline when an accurate transcript already exists; word-by-word highlighting |

## 2. Tool positioning and selection table

| Tool | Positioning | Strengths | Limitations | Best fit |
| --- | --- | --- | --- | --- |
| Aegisub | Open-source cross-platform ASS/SSA effects editor (site aegisub.org; version 3.5.1 found on 2026-10-17) | Keyframes, smooth movement, karaoke, {\...} override tags, frame-by-frame timing | Excellent styling effects but weak format conversion and batch processing; a third-party review once described it as slow-moving, which contradicts the new release on the official site — **status TO VERIFY** | Anime, effect subtitles, karaoke |
| Subtitle Edit | Free open-source Swiss Army knife (nikse.dk/SubtitleEdit, MIT licence) | 200+ format conversions, OCR of burned-in subtitles, Whisper speech-to-text, AI translation, batch timeline shifting, broadcast-grade STL, waveform timing, actively maintained | Engines/models must be installed; ASS effects editing is weaker than Aegisub | Professional delivery, format clean-up, batch QC |
| Arctime / ArcTime Pro | Chinese cross-platform visual timing tool (arctime.org) | Drag-and-drop timeline, AI transcription, 600+ features, ASS/SRT export, offline server option | Steep learning curve; high-accuracy transcription needs your own API | Long-form video, documentaries, course subtitles |
| CapCut (剪映) Pro | All-in-one editing plus automatic subtitles | Fast Chinese recognition, integrated with editing and kinetic text, SRT export, template ecosystem | Frame-by-frame fine-tuning is awkward, no ASS effects, only moderately stable at very large batch sizes, more errors when background music is loud | Short video, talking head, fast turnaround |
| OpenAI Whisper | Open-source multilingual ASR foundation model | Multilingual; translation and language identification in a single model | No native word-level timestamps, segment-level drift, requires coding | General transcription, batch long audio |
| faster-whisper | CTranslate2 reimplementation of Whisper | Same accuracy at about 4x the speed, lower VRAM, INT8 quantisation, word_timestamps, Silero VAD, fully local and offline | GPU needs cuBLAS/cuDNN; Chinese line breaking still needs a human | Local batch transcription, confidential material |
| WhisperX | faster-whisper + wav2vec2 alignment + pyannote diarisation (BSD-2-Clause) | Precise word-level timestamps, speaker labels, SRT/VTT/TSV/JSON output | Loads three models at once and needs a HuggingFace token plus acceptance of the model terms; numbers and amounts misalign, and it handles overlapping speech poorly | Interviews, meetings, subtitles that need word-level alignment |
| ffmpeg | Command-line media processing | Format conversion, soft-subtitle muxing, burn-in, extraction, encoding conversion | No recognition and no text editing | Both ends of the pipeline |

## 3. Executable standards and parameter table

### 3.1 Key faster-whisper parameters (from the official README)

| Parameter | Value | Notes |
| --- | --- | --- |
| model_size | `large-v3`, `turbo`, `small`, etc. | Larger models are more accurate and consume more VRAM |
| device / compute_type | `cuda`+`float16` / `cuda`+`int8_float16` / `cpu`+`int8` | FP16 on GPU, INT8 on CPU |
| beam_size | 5 | Decoding beam width |
| word_timestamps | True | Enables word-level timestamps |
| vad_filter | True | Built-in Silero VAD strips non-speech; by default it removes only silences longer than 2 seconds |
| vad_parameters | `dict(min_silence_duration_ms=500)` | Custom silence threshold |
| Batched inference | `BatchedInferencePipeline`, `batch_size=16` | Throughput optimisation for long audio |

**Important**: the `segments` returned by `model.transcribe()` is a **generator** — transcription only actually starts when it is iterated (or passed to `list()`). Skip materialising it and you will conclude there was no output.

### 3.2 Forced-alignment tools compared

| Tool | Alignment model | Notes |
| --- | --- | --- |
| WhisperX | wav2vec2 phoneme model | Needs the alignment model for the language; English, French, German, Spanish, Italian and others have defaults |
| Montreal Forced Aligner (MFA) | Phoneme alignment | The classic choice; needs a language phoneme model, with many community models available |
| Gentle / aeneas | Lightweight alignment | Suitable for coarse alignment when a transcript already exists |
| stable-ts | Improved Whisper word timestamps | `result.to_srt_vtt(..., word_level=True)` |
| ctc-forced-aligner | CTC decoding | Multilingual |

### 3.3 Three-tier human proofreading

| Tier | Who | What is checked |
| --- | --- | --- |
| Tier 1, self-check | Editor / subtitler | Typos, punctuation, line breaks, Chinese particle usage (的/地/得), number units |
| Tier 2, confirmation | At least 2 people on the client side reviewing independently | Technical terms, personal names, product names, brand translations |
| Tier 3, final review | Another team member who "reads only the subtitles, without the picture" | Catches omissions and inverted meaning most reliably (especially a dropped not) |

### 3.4 Batch timeline shifting and the ffmpeg command table

| Need | How |
| --- | --- |
| Shift the whole timeline | Subtitle Edit's Adjust all times; or `shift.py` in this document; must be re-run after any re-edit |
| Local speed change / frame-rate conversion | Subtitle Edit's frame-rate conversion; confirm source and target frame rates first (23.976/24/25/30) |
| Format conversion | `ffmpeg -i in.srt out.ass` / `out.vtt` |
| Mux soft subtitles into MP4 | `-c:s mov_text` |
| Mux soft subtitles into MKV | `-c:s srt` / `-c:s ass` / `-c copy` |
| Burn in SRT | `-vf "subtitles=file.srt"` |
| Burn in ASS | `-vf "ass=file.ass"` |
| Legacy subtitle encoding | `subtitles=x.srt:charenc=GBK` |
| Override the style | `force_style='FontName=Arial,FontSize=24,Outline=2'` |
| Select a subtitle stream inside a container | `subtitles=input.mkv:si=0` |
| Extract subtitles | `ffmpeg -i input.mkv -map 0:s:0 out.srt` |

## 4. Procedure and workflow (including commands verified on local ffmpeg 8.1.2)

```bash
# ① Extract 16k mono audio (the recommended input for Whisper-family models)
ffmpeg -y -i input.mp4 -vn -ac 1 -ar 16000 audio.wav

# ② Install the transcription engine
pip install faster-whisper

# ⑦-a Mux soft subtitles: mov_text is mandatory for MP4
ffmpeg -y -i input.mp4 -i subs.srt \
  -map 0:v -map 0:a -map 1 -c:v copy -c:a copy -c:s mov_text \
  -metadata:s:s:0 language=chi -metadata:s:s:0 title="Chinese" output.mp4

# ⑦-b Mux soft subtitles: MKV with two languages and a default track
ffmpeg -y -i input.mp4 -i zh.srt -i en.srt \
  -map 0:v -map 0:a -map 1 -map 2 -c copy -c:s srt \
  -metadata:s:s:0 language=chi -metadata:s:s:0 title="Chinese" \
  -metadata:s:s:1 language=eng -metadata:s:s:1 title="English" \
  -disposition:s:0 default output.mkv

# ⑦-c Burn-in (the video must be re-encoded)
ffmpeg -y -i input.mp4 -vf "subtitles=subs.srt" -c:v libx264 -c:a copy hard.mp4
ffmpeg -y -i input.mp4 -vf "ass=subs.ass" -c:v libx264 -c:a copy hard_ass.mp4

# ⑦-d Verify the tracks
ffprobe -v error -select_streams s \
  -show_entries stream=index,codec_name:stream_tags=language,title -of json output.mkv
```

The transcription script for stage ②, `asr_to_srt.py` (depends on faster-whisper; everything else is standard library):

```python
from faster_whisper import WhisperModel

def ts(t):
    total = int(round(t * 1000))
    h, total = divmod(total, 3600000)
    m, total = divmod(total, 60000)
    s, ms = divmod(total, 1000)
    return "%02d:%02d:%02d,%03d" % (h, m, s, ms)

model = WhisperModel("large-v3", device="cuda", compute_type="float16")
segments, info = model.transcribe(
    "audio.wav", beam_size=5, word_timestamps=True, vad_filter=True,
    vad_parameters=dict(min_silence_duration_ms=500))
segments = list(segments)  # a generator must be materialised before transcription actually runs
with open("out.srt", "w", encoding="utf-8") as f:
    for i, seg in enumerate(segments, 1):
        f.write("%d\n%s --> %s\n%s\n\n" %
                (i, ts(seg.start), ts(seg.end), seg.text.strip()))
print("lang=%s p=%.2f cues=%d" %
      (info.language, info.language_probability, len(segments)))
```

Batch timeline shifting, `shift.py` (`python shift.py subs.srt +1.5 shifted.srt`):

```python
import re, sys
pat = re.compile(r"(\d{2}):(\d{2}):(\d{2}),(\d{3})")
def to_ms(m):
    h, mi, s, x = map(int, m.groups())
    return (h * 3600 + mi * 60 + s) * 1000 + x
def to_tc(v):
    v = max(0, v)
    h, v = divmod(v, 3600000)
    mi, v = divmod(v, 60000)
    s, x = divmod(v, 1000)
    return "%02d:%02d:%02d,%03d" % (h, mi, s, x)
shift = int(round(float(sys.argv[2]) * 1000))
src = open(sys.argv[1], encoding="utf-8-sig").read()
out = pat.sub(lambda m: to_tc(to_ms(m) + shift), src)
open(sys.argv[3], "w", encoding="utf-8").write(out)
```

The QC script `qc.py` (structure, overlaps, duration, CPS, line count, empty text, monotonicity):

```python
import re, sys
pat = re.compile(r"(\d{2}):(\d{2}):(\d{2}),(\d{3}) --> (\d{2}):(\d{2}):(\d{2}),(\d{3})")
def ms(a):
    h, mi, s, x = map(int, a)
    return (h * 3600 + mi * 60 + s) * 1000 + x
blocks = open(sys.argv[1], encoding="utf-8-sig").read().strip().split("\n\n")
prev_start, prev_end = -1, -1
for i, b in enumerate(blocks, 1):
    lines = [x for x in b.splitlines() if x != ""]
    m = pat.search(b)
    if not m or len(lines) < 3 or not lines[0].strip().isdigit():
        print("#%d STRUCT ERROR" % i)
        continue
    st, en = ms(m.group(1, 2, 3, 4)), ms(m.group(5, 6, 7, 8))
    text = re.sub(r"<[^>]+>|\{[^}]*\}", "", " ".join(lines[2:]))
    dur = (en - st) / 1000.0
    cps = len(text) / dur if dur > 0 else 999
    issues = []
    if en <= st: issues.append("non-positive duration")
    if st < prev_start: issues.append("out of order")
    if st < prev_end: issues.append("overlap %dms" % (prev_end - st))
    if dur < 0.833: issues.append("too short")
    if dur > 7.0: issues.append("too long")
    if cps > 20.0: issues.append("CPS %.1f" % cps)
    if len(lines) - 2 > 2: issues.append("over 2 lines")
    if not text.strip(): issues.append("empty text")
    if issues:
        print("#%d [%s] %s" % (i, "; ".join(issues), text[:36]))
    prev_start, prev_end = st, en
```

The QC approach can be extended further: BOM and encoding detection, monotonic sequence numbers, per-language CPS thresholds (characters/second for Chinese), line count and characters per line, adjacent gaps under 2 frames, shot-change detection, glossary cross-checking, consistency between language tags and track count, and frame extraction plus OCR review after burn-in.

## 5. Common errors and troubleshooting

| Symptom | Root cause | Fix |
| --- | --- | --- |
| Transcription "prints nothing / comes back empty" | `segments` is a generator that was never iterated | `segments = list(segments)` |
| The whole subtitle track drifts seconds early or late | Whisper segment-level timestamp drift | Apply WhisperX / wav2vec2 forced alignment, or shift with `shift.py` and fine-tune by hand |
| Word-level timestamps still inaccurate (especially Chinese or numbers) | ASR interpolation rather than true alignment | Switch to a forced-alignment tool; check amounts and figures by hand |
| Names, brands and numbers wrong | Domain vocabulary missing from the ASR | Build a glossary and run the three-tier review; prompt with initial_prompt (Whisper family) |
| Error rate spikes when background music is loud | Speech masked by the BGM | Separate vocals or denoise before transcribing, or switch to manual transcription |
| All subtitles drift after a re-edit | The final cut was never locked | Re-run alignment and timeline shifting after any edit |
| GPU run fails | Missing cuBLAS/cuDNN (Linux needs LD_LIBRARY_PATH) | Install per the official faster-whisper Requirements, or fall back to `device="cpu", compute_type="int8"` |
| WhisperX diarisation fails | HuggingFace token missing, or the pyannote model terms not accepted | Request a token and accept the terms; do not rely on diarisation output for overlapping speech |
| No subtitles after burn-in | `-vf` and `-c copy` both applied to the video | Re-encode the video with `-c:v libx264`; audio may stay `-c:a copy` |
| Windows path error | The drive colon is read as a filtergraph separator | Write `subtitles='F\:/work/subs.srt'`, or switch to a relative path |
| ASS fonts render wrong | The target machine lacks the font | `ass=subs.ass:fontsdir=/path/to/fonts`, and ship properly licensed fonts with the file |
| First SRT cue lost | BOM present | Read with `utf-8-sig` and write back BOM-free UTF-8 |
| title not shown in MP4 | mov_text has limited title support (local testing) | Deliver MKV, or rely on the language tag alone |
| Subtitles half a second out of sync with the picture | Frame rate / time base mismatch | Confirm 23.976/25/30 and convert by frame rate |

## 6. Quick reference

- [ ] Audio extracted to 16k mono WAV, and the edit version locked
- [ ] Transcription parameters explicit: model, device/compute_type, beam_size, word_timestamps, vad_filter
- [ ] Forced alignment enabled wherever precise timing is needed, rather than relying on ASR segment timestamps
- [ ] Breaks at semantic boundaries; CPS / dwell / 2-frame gaps pass `qc.py`
- [ ] Three-tier proofreading complete; proper nouns, numbers, negations and glossary checked
- [ ] Timeline shifting reproducible by script, and re-run after any re-edit
- [ ] Muxing matched to the container: MP4→mov_text, MKV→srt/ass/copy
- [ ] Burn-in always re-encodes the video; fonts shipped with the file or pointed to via fontsdir
- [ ] Track codec, language, title and default verified with ffprobe
- [ ] Commercial licensing for all fonts and assets verified independently (see 07-tools-and-resources)

## References

- SYSTRAN/faster-whisper (official README) — https://github.com/SYSTRAN/faster-whisper
- Aegisub site / Downloads — https://aegisub.org/downloads
- Arctime site — https://arctime.org/
- Subtitle Edit site — https://www.nikse.dk/SubtitleEdit/
- Subtitle Edit repository and docs — https://github.com/SubtitleEdit/subtitleedit · http://subtitleedit.github.io/subtitleedit/
- FFmpeg Filters Documentation (subtitles / ass) — https://ffmpeg.org/ffmpeg-filters.html
- How to Add Subtitles to Video with FFmpeg — https://ffhub.io/blog/how-to-add-subtitles-to-video-with-ffmpeg
- Subtitle Edit review (version and licence, TO VERIFY) — https://www.promptquorum.com/zh/power-local-llm/subtitle-edit-review
- Subtitle Edit features and tool comparison — https://s.sskoo.com/?p=2236/
- Force-aligned (how forced alignment works; accuracy TO VERIFY) — https://socaptions.com/glossary/force-aligned
- WhisperX Guide 2026 — https://localaimaster.com/blog/whisperx-guide
- WhisperX vs Whisper — https://transcribeall.io/knowledge/how_does_whisperx_compare_to_openais_whisper_in_terms_of_transcription_accuracy_and_performance.php
- alignment (stable-ts / MFA / ctc-forced-aligner) — https://atmoscompute.com/glossary/speech/alignment
- Roundup of free audio and video-to-text software — https://www.shuiyinyun.com/article/5227.html
- AI subtitle software comparison — https://www.runmie.com/zh-tw/49178.html

Retrieved: 2026-11-10
