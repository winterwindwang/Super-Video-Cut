# Subtitle Style and Layout

> Category: Subtitles | Topic: Subtitle style and layout | Compiled: 2026-11-10 | Applies to: A single baseline for subtitle timing, translation, layout and pre-delivery QC

## 1. Core principles / concept comparison

Subtitles are timed reading performed under distraction, so the rules are built around three bandwidth constraints:

| Constraint | Physical quantity controlled | Symptom when unmanaged |
| --- | --- | --- |
| Line discipline | Characters per line, line count, break position | Three lines smother the lower frame; breaks land inside phrases; meaning is cut in two |
| Time discipline | Dwell time, gap between cues, reading speed | Cues flash past before they can be read, cues linger, cues collide with edits |
| Space discipline | Safe area, contrast, font size, stroke | Covered by platform buttons, unreadable on bright backgrounds, glyph edges cropped |

The rules for the three kinds of on-screen text are not interchangeable:

| Type | Definition | Bound by CPS | What matters |
| --- | --- | --- | --- |
| Dialogue subtitles | Dialogue and narration rendered as text | Yes | Every rule in this document applies |
| In-picture subtitles / forced narrative | Signage, on-screen text, title cards, translation of off-screen speech | Yes, but as separate cues | Must not share a cue with dialogue; must avoid existing on-screen text |
| Titles / kinetic typography | Opening titles, chapter cards, programme packaging | No | Font size may be enlarged, but safe area and contrast still apply |

How three public guidelines differ (which is why their numbers cannot be swapped between them):

| Guideline | Scope | Unit of measure | Core concern |
| --- | --- | --- | --- |
| Netflix Timed Text Style Guide, TTSG | Multilingual streaming delivery | characters per second, CPS | Per-language settings; automated machine QC rejection |
| BBC Subtitle Guidelines | Broadcast and iPlayer | words per minute, wpm | Verbatim accuracy, speech-rate ceiling, adaptation to screen shape |
| DCMP Captioning Key | Educational media accessibility | words per minute, wpm | An equivalent experience for deaf viewers, speaker labels and sound descriptions |

## 2. Executable standards and parameter table

### 2.1 Reading speed and dwell time (three-way comparison)

| Metric | Netflix English adult | BBC | DCMP |
| --- | --- | --- | --- |
| Reading-speed ceiling | 20 CPS (adult) / 17 CPS (children) TO VERIFY | 160-180 wpm | 130 wpm (lower grades) / 140 (middle) / 160 (upper) |
| Per-line limit | 42 characters | about 37 characters (teletext is monospaced) | Character count not specified |
| Line limit | 2 lines, 1 preferred | 2 lines (landscape / square) | 2 lines preferred, 3-4 when necessary |
| Minimum dwell | 5/6 second (about 20 frames at 24fps, about 833 ms) | about 0.3 second per word | 40 frames (1 second 10 frames, about 1.33 seconds) |
| Maximum dwell | 7 seconds | Context-dependent; avoid abrupt long/short swings | 6 seconds (background-music symbols excepted) |
| Minimum gap between events | 2 frames (at any frame rate) | about 1.5 seconds at speech pauses, TO VERIFY | Borrow 15 frames (about 0.5 second) as a timing technique |

Secondary sources disagree sharply on Netflix CPS (adult 17 / 20 / 20-25 CPS; children 13 / 17 CPS, varying by language and between SDH and translation), **all marked TO VERIFY — before delivery, defer to the wording of the TTSG for the relevant language on the Netflix Partner Help Center**; this table uses the most widely cited English figures, 20 for adults and 17 for children, as its working baseline. CPS counts spaces and punctuation but not line breaks.

### 2.2 English versus Chinese, and characters per line

| Language | Counting method | Suggested per-line limit | Suggested for 9:16 vertical | Reading-speed reference |
| --- | --- | --- | --- | --- |
| English and other Latin scripts | Characters | 42 characters | about 25 characters | 17-20 CPS |
| Chinese | Han characters | 12-18 characters (in practice); Netflix Traditional Chinese 16 / SDH 18, TO VERIFY | 10-14 characters | about 7-9 characters/second, TO VERIFY |

Chinese carries more information per character and has no inter-word spaces, so 42 characters and 20 CPS cannot be transplanted directly. Chinese CPS is quoted under two conventions, 4-6 and 7-9 characters/second, **TO VERIFY**; adopt "at least 1 second per cue and no more than 16 characters per line" as the hard constraint. Bilingual stacks are 2 lines in total, 14-16 Chinese characters and no more than 8 English words; check both lines when splitting so neither outweighs the other.

### 2.3 Line breaking and semantic integrity

Line-breaking priority: **semantic integrity > syntactic boundary > punctuation > length constraint**. A workable splitting order: split on punctuation first → then re-split overlong sentences at clause and thought-group boundaries → finally align to speech with word-level timestamps. Prohibited breaks: separating a modifier from its head word, splitting a prepositional phrase, putting a person's name and their title on separate lines, breaking after a conjunction, splitting an auxiliary from the word it modifies, and packing the tail of one sentence together with the head of the next on a single line. Break at clause level; never cut a sentence arbitrarily in half. For two-speaker dialogue Netflix starts the second speaker's line with a hyphen, whereas DCMP prefers placing each speaker's caption beneath that speaker and forbids using a hyphen as a speaker identifier (**the two rules conflict — choose one per delivery target and mark it TO VERIFY**). For a sentence continued across two cues, add no ellipsis if the pause is shorter than 2 seconds; use one only for longer pauses or trailing speech. Netflix specifies a single U+2026 ellipsis character rather than three periods.

### 2.4 Cue gaps and frame-accurate alignment

| Item | Parameter | Source |
| --- | --- | --- |
| Minimum gap between adjacent subtitles | ≥ 2 frames; gaps of 3-11 frames are collapsed to exactly 2 frames | Netflix TTSG |
| Sync error against audio | Within 3 frames; out-points may run at most 12 frames past the end of the audio | Netflix delivery notes, TO VERIFY |
| Camera cuts | A subtitle must not cross a shot change | Netflix delivery notes, TO VERIFY |
| In-point / out-point practice | Place the in-point on the onset of the waveform; delay the out-point by 0.2-0.3 second; overall audio-video offset ≤ 0.1 second | Chinese production practice, TO VERIFY |

### 2.5 Safe area and vertical adaptation

| Scenario | Text-block width | Cap height (share of frame height) | Lines | Bottom margin |
| --- | --- | --- | --- | --- |
| 16:9 landscape | about 68% of frame width | 7%-8% (about 76-86 px at 1080p) | 2 lines | 8%-12% from the bottom |
| 9:16 vertical | about 90% of frame width | 3.9%-4.5% (about 75-86 px at 1920 height) | 3 lines maximum | 15%-25% from the bottom |
| Television broadcast | 18% clear on each side | — | 2 lines | 12% clear top and bottom |

The BBC figures in the table above (68% / 90% / 7-8% / 3.9-4.5%) and the television and cinema safe areas come from second-hand compilations, **TO VERIFY**. Vertical video must avoid the top status bar, the bottom third (comment and button zone) and the right-hand icon column. For contrast, follow WCAG 2.2 SC 1.4.3: ≥ 4.5:1 for normal text, ≥ 3:1 for large text; burned-in text counts as images of text and is subject to the same requirement, so check the worst frame in moving backgrounds.

### 2.6 Font, size, stroke, shadow and background-box parameters

The following are starting values that drop straight into ASS and ffmpeg `force_style` at 1080p / PlayResY=1080:

| Parameter | Suggested value | Notes |
| --- | --- | --- |
| FontName | Source Han Sans (思源黑体) / Microsoft YaHei / Arial / Verdana | Medium weight, sans-serif, proportional spacing, generous width; avoid light and decorative faces |
| FontSize | 48-60 (PlayResY 1080) | Roughly 5%-6% of frame height; calibrate against the cap heights in section 2.5 |
| PrimaryColour | &H00FFFFFF | Pure white (ASS uses &HAABBGGRR) |
| OutlineColour | &H00000000 | Pure black stroke |
| Outline / Shadow | 2-3 / 1-2 | Mandatory on bright backgrounds; DCMP recommends adding a semi-transparent background box |
| BorderStyle | 1 (outline + shadow) or 3 (opaque box) | The exact rendering of 3 differs between implementations, TO VERIFY; confirm on the target player |
| Alignment | 2 | Bottom centre; use 8 for top |
| MarginV / MarginL / MarginR | 40-60 / 10% of frame width / 10% of frame width | Keeps glyph edges from being cropped |
| Bold / Italic | 0 / italic only for off-screen narration, emphasis and inner monologue | Mixed case; never use all caps for emphasis (shouting excepted) |

For bilingual subtitles, set the secondary English line to about 80% of the font size and keep the typeface family consistent (a sans-serif Chinese face plus Arial/Roboto for English).

### 2.7 Punctuation and number conventions

Chinese dialogue subtitles use full-width punctuation throughout. No full stop at the end of a cue; no comma or enumeration comma at the end of a line or cue; keep ?, ! and … . Foreign-language and numeric content takes the corresponding half-width punctuation. Insert one space between a Han character and a Latin letter or digit. The Netflix Traditional Chinese guide explicitly forbids the ideographic full stop (U+3002) anywhere in the file; this is stated platform policy but the official wording was not checked directly for this document, so it is **marked TO VERIFY**. Format numbers, dates, time ranges, percentages and amounts consistently across the whole programme (write 10 million, not 10M); Netflix requires currencies mentioned in dialogue to remain in their original currency, unconverted. US English uses a double hyphen for interruptions and UK English uses an ellipsis — **a hard rule difference; never mix the two**. Emoji, garbled net-speak and invented symbols are prohibited.

### 2.8 In-picture subtitles versus titles

In-picture subtitles (forced narrative) belong in their own cues or their own track, carry position data so they do not cover existing on-screen text, and must never share a cue with dialogue. Titles are exempt from CPS and the 2-line limit but must still satisfy safe area and contrast; give titles and subtitles separate style layers so they can be toggled and reviewed independently.

## 3. Procedure and workflow

Lock the baseline (aspect ratio / frame rate / delivery target) → produce an unstyled SRT draft following section 2.3 → time it with word-level timestamps and apply the minimum and maximum dwell plus the 2-frame gap → convert to ASS and edit `[V4+ Styles]` (parameters from section 2.6) → preview the burn-in on the worst frames and run automated QC.

Runnable commands (verified on local ffmpeg 8.1.2):

```bash
# Convert SRT to ASS, then edit the styles; the PlayRes ffmpeg generates is not necessarily the video resolution, so set it to the real values by hand
ffmpeg -y -i subs.srt subs.ass

# Override the style with force_style and burn in a preview; the colon in a Windows drive letter must be escaped as \:
ffmpeg -y -i input.mp4 -vf "subtitles='F\:/work/subs.srt':force_style='FontName=Microsoft YaHei,FontSize=54,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,Outline=2,Shadow=1,Alignment=2,MarginV=50'" -c:v libx264 -c:a copy preview.mp4

# Use the dedicated filter for ASS effect subtitles; keeps every style in the file
ffmpeg -y -i input.mp4 -vf "ass='F\:/work/subs.ass'" -c:v libx264 -c:a copy preview_ass.mp4
```

Approach for a CPS self-check script (standard library only; prints the IDs of offending cues):

```python
import re, sys
# Read the SRT and split into blocks on blank lines; CPS = character count after stripping markup / duration in seconds
pat = re.compile(r"(\d\d):(\d\d):(\d\d),(\d\d\d) --> (\d\d):(\d\d):(\d\d),(\d\d\d)")
def ms(h, m, s, x): return ((int(h)*3600 + int(m)*60 + int(s))*1000 + int(x))
blocks = open(sys.argv[1], encoding="utf-8-sig").read().strip().split("\n\n")
limit = float(sys.argv[2]) if len(sys.argv) > 2 else 20.0
for i, b in enumerate(blocks, 1):
    lines = b.splitlines()
    m = pat.search(b)
    if not m: continue
    dur = (ms(*m.group(5,6,7,8)) - ms(*m.group(1,2,3,4))) / 1000.0
    text = re.sub(r"<[^>]+>|\{\\[^}]*\}", "", " ".join(lines[2:])).replace("\n", "")
    cps = len(text) / dur if dur > 0 else 999
    if cps > limit or dur < 0.833 or dur > 7.0:
        print(f"#{i} dur={dur:.2f}s cps={cps:.1f} :: {text[:40]}")
```

## 4. Common errors and troubleshooting

| Symptom | Root cause | Fix |
| --- | --- | --- |
| Cues flash past | Dwell under 5/6 second, or under 0.83 second | Lengthen the dwell or merge cues; do not fix it by compressing the timeline |
| CPS over limit | Too much text for too little time | Split lines or cut redundant words; shortening the duration only makes it worse |
| Cues linger | A single cue runs longer than 7 seconds | Split the cue and align the out-point to the end of the speech |
| Subtitle crosses a shot change | Timing done without watching the cut points | Close 2 frames before the cut and start a new cue after it |
| Unreadable on a bright background | No stroke or no background box | Add Outline 2-3 or a semi-transparent plate and verify 4.5:1 |
| Bottom of a vertical video hidden by buttons | Landscape MarginV reused | Move the block to the middle of the frame and leave 15%-25% at the bottom |
| Bilingual stack is top-heavy | Each line written to the monolingual limit | Split Chinese and English together: 14-16 Chinese characters / ≤ 8 English words |
| Full stop at the cue end or a comma at the line end | Copied from a written script | Remove the final full stop and trailing commas or enumeration commas |
| Stray space before punctuation, or mixed full-width and half-width | Copy-paste | Normalise to full-width punctuation and delete spaces before punctuation |
| In-picture subtitle overlaid on dialogue | Both in the same cue | Split into separate cues and tag the position |

## 5. Quick reference

- [ ] Aspect ratio, frame rate and delivery spec locked, and the CPS ceiling written into the project settings
- [ ] ≤ 42 characters per line (English) / ≤ 16 characters (Chinese), 2 lines maximum, single line preferred
- [ ] Dwell 5/6 second to 7 seconds per cue, gaps ≥ 2 frames, no crossing a shot change
- [ ] Breaks at clause boundaries; no phrases, names or prepositional phrases split apart
- [ ] Bilingual stack balanced across both lines, Chinese on top
- [ ] White text + black stroke + shadow / semi-transparent plate, contrast ≥ 4.5:1
- [ ] Vertical video clears the top bar, the bottom third and the right-hand button column
- [ ] No full stop at the cue end, no trailing commas, number and currency formats consistent throughout
- [ ] In-picture subtitles are separate cues; title and dialogue styles kept apart
- [ ] Every TO VERIFY figure re-checked against the official guideline of the final delivery platform

## References

- BBC Subtitle Guidelines — https://www.bbc.co.uk/accessibility/forproducts/guides/subtitles
- DCMP Captioning Key (print) — https://dcmp.org/captioningkey/print
- DCMP Keys to Access — http://keystoaccess.org/learn
- W3C WCAG 2.2 — https://www.w3.org/TR/WCAG22/
- W3C WebVTT 1.0 — https://www.w3.org/TR/webvtt1/
- Netflix Subtitle Guidelines Explained (third-party compilation, figures TO VERIFY) — https://vsubtitle.com/netflix-subtitle-guidelines-explained/
- Subtitling Services for OTT Platforms (third-party compilation, figures TO VERIFY) — https://ekitaisolutions.com/subtitling-services-for-ott-platforms-what-netflix-standard-quality-actually-requires/
- Traditional Chinese Subtitle Style Guide (third-party compilation, figures TO VERIFY) — https://www.taption.com/blog/zh/traditional-chinese-subtitle-style-guide-zh
- On screen text: size, duration and safe zones (secondary compilation of BBC/WCAG material) — https://onecraft.app/blog/on-screen-text-best-practices-video
- Bilingual subtitle production practice (Baidu Developer Center) — https://developer.baidu.com/article/detail.html?id=9439722
- Video subtitle production standards (safe-area practice, TO VERIFY) — https://acg.sohu.com/a/1086698081_120949282
- FFmpeg Filters Documentation — https://ffmpeg.org/ffmpeg-filters.html

Retrieved: 2026-11-10
