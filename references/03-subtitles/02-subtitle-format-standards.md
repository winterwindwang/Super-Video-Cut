# Subtitle Format Standards

> Category: Subtitles | Topic: Subtitle formats, timecodes and container muxing | Compiled: 2026-11-10 | Applies to: Format selection, format conversion, soft-subtitle muxing and burned-in delivery

## 1. Core principles / concept comparison

A subtitle format really answers only two questions: **when** (timeline encoding) and **what to show** (text or image, plus styling). First split by storage form, then by delivery form; picking the wrong category produces entirely different classes of failure — "the file won't open", "the styles turned into literal text", "it can't be translated".

| Category | Representative formats | Searchable / editable / translatable | Typical failure |
| --- | --- | --- | --- |
| Text-based | SRT, WebVTT, ASS/SSA, TTML/DFXP, SCC, SBV, MicroDVD | Yes | Timecode punctuation, encoding, style tags not recognised |
| Image-based | SUB/IDX (VobSub), PGS/.sup, EBU-STL (binary) | No, OCR required | Cannot change text or language; resolution fixed |

| Delivery form | Definition | Can it be switched off / language changed | Does it require re-encoding the video | Typical use |
| --- | --- | --- | --- | --- |
| Sidecar soft subtitles | A separate .srt/.vtt file alongside the video | Yes | No | YouTube upload, translation hand-off, review |
| Muxed soft subtitles | Subtitle stream muxed into an MP4/MKV container | Yes | No (`-c copy`) | Multilingual release, in-app players |
| Burned-in subtitles | Subtitles rendered into the picture pixels | No | Yes (`-vf` always re-encodes) | Muted-autoplay social video |

**Timecodes are the biggest compatibility trap**: SRT uses a comma, WebVTT a point, ASS a point with only two centisecond digits, SCC frame numbers. The same "1 minute 2.5 seconds" is written completely differently in each format, and mixing them up breaks parsing outright.

## 2. Format structures, minimal examples and differences

### 2.1 SRT (SubRip)

A de facto standard with no official specification, and the most widely compatible. The structure is fixed: index → timecode line → text lines → blank line separator. Timecode `HH:MM:SS,mmm --> HH:MM:SS,mmm`, **with a comma before the milliseconds**.

```srt
1
00:00:01,500 --> 00:00:04,000
The first line of dialogue.

2
00:00:04,200 --> 00:00:07,100
And the second one.
```

Only a very small set of HTML-style tags is supported (`<b>`, `<i>`, `<u>`, `<font color=...>`), and players render them inconsistently; no positioning, no fonts. YouTube accepts plain UTF-8 SRT and ignores style markup.

### 2.2 WebVTT (W3C standard)

The native format for HTML5 `<track>` and HLS, UTF-8 encoded, MIME type `text/vtt`. The file body must be: optional BOM → mandatory first line `WEBVTT` → two or more line terminators → optional REGION/STYLE/NOTE blocks → cue blocks. Timecodes are `MM:SS.mmm` or `HH:MM:SS.mmm`; **the separator before milliseconds is a point and exactly three digits are required**.

```vtt
WEBVTT

intro
00:01.000 --> 00:04.000 align:center position:50% size:100%
Hello.
```

Key points: the cue identifier is optional but must be unique within the whole file and can be targeted by CSS with `::cue(#intro)`; cue settings include `vertical:rl|lr`, `line:<pct|line number>[,start|center|end]`, `position:<pct>[,line-left|center|line-right]`, `size:<pct>`, `align:start|center|end|left|right` and `region:<id>`, and settings must not repeat within a single list; the cue payload must not contain the substring `-->`; implementations must not perform Unicode normalisation. A STYLE block may contain `::cue { color: lime; }`.

### 2.3 ASS / SSA (SubStation Alpha)

A complete styling language: named styles, font/colour/stroke/shadow, pixel-level positioning, rotation, karaoke and animation. INI-style sections; within a `Dialogue:` line, `{\an8}` pins the cue to the top and `{\b1}...{\b0}` toggles bold — these are override tags. Timecodes are `H:MM:SS.cc`, **with a single digit for hours and two digits of centiseconds**; colours are `&HAABBGGRR`.

```ass
[Script Info]
Title: Example
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,48,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,2,1,2,10,10,40,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:01.00,0:00:04.00,Default,,0,0,0,,Hello, this is a subtitle.
Dialogue: 0,0:00:05.00,0:00:08.00,Default,,0,0,0,,This line has {\b1}bold{\b0} text.
```

SSA is the predecessor: it uses a `[V4 Styles]` section and has fewer styling features, and ASS is backward compatible with it. `PlayResX/PlayResY` define the style coordinate space, not the video size — in testing, `ffmpeg -i subs.srt subs.ass` emits `PlayResX: 384 / PlayResY: 288` by default, and this must be changed to the actual resolution, otherwise font sizes and margins scale against the wrong ratio.

### 2.4 TTML / DFXP (W3C standard)

An XML document with the root `<tt>`, namespace `http://www.w3.org/ns/ttml`, styling under the `tts:` prefix and parameters under `ttp:`; `head` (metadata / styling / layout) is kept separate from `body` (div / p); `p` carries `begin` / `end` / `dur`, and time values may be clock time `00:00:01.000` or offset time `0.76s`, `3s`, `1500ms`.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<tt xml:lang="en" xmlns="http://www.w3.org/ns/ttml"
    xmlns:ttp="http://www.w3.org/ns/ttml#parameter"
    xmlns:tts="http://www.w3.org/ns/ttml#styling"
    ttp:profile="http://www.w3.org/ns/ttml/profile/dfxp-presentation">
  <head>
    <metadata/>
    <styling>
      <style xml:id="s1" tts:fontSize="22px" tts:color="white" tts:textAlign="center"/>
    </styling>
    <layout><region xml:id="r1" style="s1"/></layout>
  </head>
  <body region="r1">
    <div>
      <p begin="00:00:01.000" end="00:00:03.000">Hello TTML</p>
      <p begin="3s" dur="2s">Offset-time cue</p>
    </div>
  </body>
</tt>
```

For strict document exchange the MIME type is `application/ttml+xml`. Netflix delivery is built on TTML1 / IMSC1.1 (including Japanese vertical text) and requires **font size as a percentage (100%) rather than pixels**, positioning through `tts:textAlign` and `tts:displayAlign` combined with `tts:extent` / `tts:origin`, Arial as the placeholder font, and characters restricted to those in its Glyph List — these delivery details come from third-party compilations and are **marked TO VERIFY; defer to the original wording on the Netflix Partner Help Center**.

### 2.5 SCC (Scenarist Closed Captions)

US broadcast CEA-608 closed captions: header `Scenarist_SCC V1.0`, timecodes `HH:MM:SS:FF` (**frame numbers, not milliseconds**, at 29.97fps), and a payload of hexadecimal control codes rather than human-readable text.

```scc
Scenarist_SCC V1.0

00:00:01:15  942c 942f 94ae 94ae 9420 94f2 4865 6c6c 6f2e 942c 942f
```

The precise semantics of individual control words (such as 942c / 942f / 9420) were not checked word for word against the CEA-608 / CTA-608 specification for this document and are **marked TO VERIFY**; they are listed only to recognise the format and choose a conversion tool — never hand-write control codes.

### 2.6 MOV text (tx3g)

Not a standalone file but the text-subtitle **codec** inside an MP4/MOV container. In ffmpeg it is `-c:s mov_text`, which converts SRT into 3GPP timed text and muxes it. No native support for ASS styling or positioning.

### 2.7 SUB / IDX (VobSub) and the extension collision

`.idx` is a text index (time points + language + offsets), `.sub` is bitmap data. Common from DVD extraction; the Blu-ray equivalent is PGS `.sup`. Because it is an image, it **cannot be searched, edited, restyled or translated — OCR is mandatory** to recover text. Note that `.sub` may also be MicroDVD (plain text, frame numbers `{100}{250}This is a line.`), a completely different format sharing the extension; EBU-STL `.stl` is a binary broadcast format (EBU Tech 3264).

### 2.8 Timecodes and capabilities at a glance

| Format | Extension | How 1 min 2.5 s is written | Styling capability | Positioning | Primary use |
| --- | --- | --- | --- | --- | --- |
| SRT | .srt | `00:01:02,500` | Very limited | None | General exchange, upload |
| WebVTT | .vtt | `01:02.500` or `00:01:02.500` | CSS `::cue` | Yes | Web, HLS |
| ASS/SSA | .ass/.ssa | `0:01:02.50` | Full | Pixel-level | Effects, karaoke, local playback |
| TTML/DFXP | .ttml/.dfxp/.xml | `00:01:02.500` or `62.5s` | Full | Yes | Streaming / broadcast delivery |
| SCC | .scc | `00:01:02:15` | Limited | Limited | US broadcast CC |
| SBV | .sbv | `0:01:02.500` | None | None | YouTube upload |
| MicroDVD | .sub | `{1499}` frame number | None | None | Legacy players |
| VobSub | .idx+.sub | Frame/time stored in .idx | Fixed image | Fixed | DVD backup |

## 3. Encoding, BOM, tracks and language tags (executable standards)

| Item | Requirement |
| --- | --- |
| Text encoding | UTF-8 throughout; convert legacy files with `-vf "subtitles=x.srt:charenc=GBK"` |
| BOM in SRT / VTT | SRT should be **BOM-free** — a leading BOM makes some parsers reject the first cue; WebVTT permits an optional `U+FEFF` BOM but the file is still UTF-8 |
| Line terminators | WebVTT allows CRLF / LF / CR; SRT conventionally uses CRLF or LF |
| MP4 subtitle codec | Must be `-c:s mov_text`; `-c:s srt` fails or produces an unreadable stream |
| MKV subtitle codec | `-c:s srt` / `-c:s ass` / `-c copy` all work, with `-c copy` giving the highest styling fidelity |
| Multi-track language tags | `-metadata:s:s:N language=<ISO 639-2 three-letter code>`, e.g. `eng/chi/fra/spa/jpn/zho/vie`; `title=` is the name shown in player menus |
| Default track | `-disposition:s:0 default`; clear the others with `-disposition:s:1 0` |

**TO VERIFY**: MP4 accepts only ISO 639-2 three-letter codes (the two-letter `vi` is unreliable), whereas MKV also supports full BCP 47 (`zh-Hans` / `zh-Hant` distinguish Simplified from Traditional); this conclusion comes from third-party compilations and must be re-checked against the target platform. **Local test note**: `-metadata:s:s:0 title=` is not written under MP4/mov_text (ffprobe reports only `language`), while `title` displays correctly under MKV — so player menu names are more reliable with MKV.

## 4. Procedure and workflow (all verified on local ffmpeg 8.1.2)

```bash
# 1. Format conversion: SRT -> ASS / WebVTT
ffmpeg -y -i subs.srt subs.ass
ffmpeg -y -i subs.srt subs.vtt

# 2. Mux soft subtitles into MP4 (mov_text is mandatory); video and audio are not re-encoded
ffmpeg -y -i input.mp4 -i subs.srt \
  -map 0:v -map 0:a -map 1 -c:v copy -c:a copy -c:s mov_text \
  -metadata:s:s:0 language=chi -metadata:s:s:0 title="Chinese" output.mp4

# 3. Two-language soft subtitles in MKV, with a default track
ffmpeg -y -i input.mp4 -i zh.srt -i en.srt \
  -map 0:v -map 0:a -map 1 -map 2 -c copy -c:s srt \
  -metadata:s:s:0 language=chi -metadata:s:s:0 title="Chinese" \
  -metadata:s:s:1 language=eng -metadata:s:s:1 title="English" \
  -disposition:s:0 default output.mkv

# 4. Inspect the subtitle tracks in a container
ffprobe -v error -select_streams s \
  -show_entries stream=index,codec_name:stream_tags=language,title -of json input.mkv

# 5. Extract embedded subtitles (first track / keeping ASS styles)
ffmpeg -y -i input.mkv -map 0:s:0 out.srt
ffmpeg -y -i input.mkv -map 0:s:0 out.ass

# 6. Burn-in with the general subtitles filter
ffmpeg -y -i input.mp4 -vf "subtitles=subs.srt" -c:v libx264 -c:a copy hard.mp4

# 7. Burn-in with the ASS-specific filter, keeping every style in the file
ffmpeg -y -i input.mp4 -vf "ass=subs.ass" -c:v libx264 -c:a copy hard_ass.mp4

# 8. Burn-in with an overridden style and a legacy subtitle encoding (escape the Windows drive colon)
ffmpeg -y -i input.mp4 \
  -vf "subtitles='F\:/work/subs.srt':charenc=GBK:force_style='FontName=Microsoft YaHei,FontSize=48,Outline=2,Alignment=2'" \
  -c:v libx264 -c:a copy hard_styled.mp4
```

Acceptance: after each command, run `ffprobe -v error -show_entries stream=index,codec_name,codec_type -of csv output.mp4` to confirm the subtitle stream exists with the correct codec. Mind the order of `-c copy -c:s mov_text` — the later `-c:s` overrides the earlier `-c copy` while video and audio still pass through untouched.

## 5. Common errors and troubleshooting

| Symptom | Root cause | Fix |
| --- | --- | --- |
| Subtitles missing entirely / first cue lost | SRT carries a UTF-8 BOM, or sequence numbers are missing | Save as "UTF-8 without BOM" and check the index and timecode lines |
| SRT with timecodes like `00:00:01.500` flagged as invalid | WebVTT-style point reused | Change back to a comma: `00:00:01,500` |
| `0:00:01,50` in ASS fails to parse | SRT comma reused by mistake | ASS needs `0:00:01.50` (point + two-digit centiseconds) |
| Chinese text renders as `Ã©` or question marks | File is GBK / Windows-1252 | Convert to UTF-8, or use `charenc=` temporarily |
| Adding subtitles to MP4 errors out | `-c:s srt` used | Change to `-c:s mov_text` |
| `{\an8}` shows up as literal text after upload | ASS delivered as if it were SRT | Convert to SRT first, or use a player that supports ASS |
| All font sizes and margins too large or too small | ASS PlayResX/Y does not match the video resolution | Set it to the actual `1920x1080` or similar |
| Effect-subtitle fonts render wrong | Target machine lacks the font | `ass=subs.ass:fontsdir=/path/to/fonts` |
| Cannot change text in SUB/IDX | Image-based subtitles | OCR it to SRT with Subtitle Edit |
| Burn-in with `-c copy` produces no subtitles | Filters and stream copy are mutually exclusive | The video must be re-encoded (`-c:v libx264`); audio can stay `-c:a copy` |
| Multi-language track menu shows the wrong language | Two-letter language code used | Switch to ISO 639-2 three-letter codes |
| `title` does not appear in MP4 | mov_text has limited support for title metadata (local testing) | Deliver as MKV, or accept that only the language shows |
| VTT file does not load at all | Missing the opening `WEBVTT` line, or only one line break after it | Add the opening line plus one blank line |

## 6. Quick reference

- [ ] Text formats are UTF-8 and SRT is BOM-free; legacy files transcoded first
- [ ] SRT comma / VTT point / ASS point + two-digit centiseconds / SCC frame numbers — none mixed up
- [ ] Each format's minimal example parses on its own
- [ ] MP4 → `mov_text`; MKV → `srt`/`ass`/`copy`, chosen to match the container
- [ ] ASS PlayResX/Y equals the video resolution, and fonts are either shipped with the file or in fontsdir
- [ ] Image-based subtitles (SUB/IDX, PGS) checked for whether OCR is needed
- [ ] Multi-track `language` uses ISO 639-2 three-letter codes, and only one track is set `default`
- [ ] Burn-in always re-encodes the video; subtitle-stream copy is only for muxing
- [ ] After muxing, re-check codec_name and language tags with ffprobe
- [ ] Every TO VERIFY platform detail re-checked against the official delivery guide

## References

- W3C WebVTT 1.0 — https://www.w3.org/TR/webvtt1/
- W3C TTML 1.0 (DFXP) — https://www.w3.org/TR/ttml1/
- FFmpeg Filters Documentation (subtitles / ass / drawtext) — https://ffmpeg.org/ffmpeg-filters.html
- Subtitle File Formats: SRT, VTT, ASS & TTML With Examples — https://translatebot.dev/en/blog/subtitle-file-format/
- Uploading SRT and Other Subtitle Files (format identification table) — https://docs.nomad.media/docs/uploading-srt-subtitle-files
- Subtitle Formats Explained: SRT vs VTT vs ASS — https://tembrica.com/en/blog/subtitle-formats-explained
- Subtitle Formats — SRT, VTT, ASS, SSA, and More — https://syncsubtitle.com/formats/subtitle-formats
- How to Add Subtitles to Video with FFmpeg (muxing commands) — https://ffhub.io/blog/how-to-add-subtitles-to-video-with-ffmpeg
- Subtitles and Captions (ffmpeg tutorial) — https://www.ffmpeg-micro.com/training/learn-ffmpeg/subtitles
- Subtitle Language Tags in MP4 and MKV (BCP 47, TO VERIFY) — https://daohuy.com/en/blog/post-subtitle-language-tags-bcp47-mp4-mkv
- SRT Validator (reading-speed and format validation criteria) — https://sozai.app/tools/srt-validator/
- Subtitle format classification (Wikipedia mirror) — https://www.xdizhu.net/wikipedia/wiki/%E5%AD%97%E5%B9%95

Retrieved: 2026-11-10
