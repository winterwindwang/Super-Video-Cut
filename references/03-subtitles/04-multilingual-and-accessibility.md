# Multilingual and Accessible Subtitles

> Category: Subtitles | Topic: Translated subtitles / CC / SDH, WCAG 2.2, multilingual tracks and localisation | Compiled: 2026-11-10 | Applies to: Accessibility delivery, multilingual release, educational media and content localised for international markets

## 1. Core principles / concept comparison

Three terms cause most of the confusion in this field because their **underlying assumptions** differ, and those assumptions determine completely different content inventories:

| Type | Common abbreviation | Assumed audience | Must include | Usually omits |
| --- | --- | --- | --- | --- |
| Translated subtitles | SUB | Can hear, but does not understand the source language | Translation of dialogue and narration | Sound effects, speaker labels |
| Closed captions | CC | Cannot hear | Dialogue + speaker labels + meaningful non-speech sound | — |
| SDH | SDH | Cannot hear, and may also need a translation | Everything in CC + dialogue in the same language or translated | — |

One-line mnemonic: **subtitles assume the audience can hear; captions assume they cannot**; SDH (Subtitles for the Deaf and Hard of Hearing) merges the two and may be either intralingual or interlingual. W3C defines captions as "a text alternative for the audio, synchronised with the media, covering speech and the non-speech audio information needed to understand it", so **a verbatim transcript is not the same thing as captions**, and a pure dialogue translation does not satisfy captions either.

| Presentation | Definition | Viewer control | Recommended for |
| --- | --- | --- | --- |
| Open captions | Burned into the picture pixels | Cannot be switched off or resized | Muted-autoplay social video; content that must keep captions after re-posting |
| Closed captions | A separate subtitle track | Can be toggled, resized and switched between languages | Corporate sites, learning platforms, OTT, compliance delivery |

W3C lists open captions as one sufficient technique for meeting the captions requirement; even so, websites and education platforms usually prefer closed captions because the viewer stays in control. Neither is absolutely more accessible — it depends on where the content is published.

### WCAG 2.2 success criteria in scope (Guideline 1.2 Time-based Media)

| Number | Name | Level | Core requirement |
| --- | --- | --- | --- |
| 1.2.1 | Audio-only and Video-only (Prerecorded) | A | Provide an equivalent alternative for audio-only or video-only content |
| 1.2.2 | Captions (Prerecorded) | A | Provide captions for the audio of prerecorded synchronised media |
| 1.2.3 | Audio Description or Media Alternative (Prerecorded) | A | Provide a media alternative or audio description |
| 1.2.4 | Captions (Live) | AA | Provide captions for live audio |
| 1.2.5 | Audio Description (Prerecorded) | AA | Provide audio description for prerecorded video |
| 1.2.6 | Sign Language (Prerecorded) | AAA | Sign language interpretation |
| 1.2.7 | Extended Audio Description (Prerecorded) | AAA | Extended audio description that pauses the picture to fit the description |
| 1.2.8 | Media Alternative (Prerecorded) | AAA | A full text alternative |
| 1.2.9 | Audio-only (Live) | AAA | An alternative for live audio-only content |
| 1.4.3 | Contrast (Minimum) | AA | Text ≥ 4.5:1; large text ≥ 3:1 |
| 1.3.1 | Info and Relationships | A | Information must not be conveyed by colour, shape or position alone |

Practical conclusion: **accurate, synchronised captions on prerecorded video with speech are the Level A baseline**; audio description sits at AA; live captions are AA. WCAG states *what must exist* but not *how to break lines or time cues* — that is filled in by style guides such as Netflix, BBC and DCMP. Whether any of it is a legal obligation depends on jurisdiction, sector and contract: **marked TO VERIFY, to be confirmed with the client's compliance owner**.

## 2. Executable standards and parameter table

### 2.1 CC / SDH content inventory

| Element | How to write it | Key rules |
| --- | --- | --- |
| Speaker label | `MAYA:` / `[narrator]` / the name on its own line | Required when the speaker is off-screen or not visually obvious; a name on its own line stays separate from the dialogue; never rely on colour or position alone (WCAG 1.3.1); when several people speak at once, place each label under its own line or show them in separate cues |
| Sound description | `[door slams]` / `[phone ringing]` | Square brackets; DCMP requires the source of the sound (omissible when it is visible on screen), lower case, present tense, specific rather than vague; off-screen sounds in italics; placed as close to the source as possible |
| Music | `[tense music]`, lyrics wrapped in `♪` | Describe background music objectively and avoid subjective words such as "beautiful"; transcribe lyrics word for word; omit non-essential background music shorter than 5 seconds (DCMP 6.2.1.7) |
| Tone / delivery | `[whispering]`, `[sarcastic]`, `[laughing]` | Annotate only where it changes comprehension; use the present participle for continuous sounds and third-person verb forms for sudden ones |
| Foreign language / dialect | `[speaking French]` | DCMP requires naming the language where possible rather than quietly translating into English; preserve dialect features; render profanity and slang as spoken |
| Silence / no audio | `[no audio]` / `[silence]` | Annotate when people are visibly conversing but nothing is audible |

There is only one editorial test: **would this sound change the viewer's understanding** — not logging every ambient noise as an inventory. W3C likewise describes the choice of which sounds to caption as more art than science.

### 2.2 Presentation rate and structure (official DCMP Captioning Key wording)

| Item | Parameter |
| --- | --- |
| Presentation rate | ≤ 130 wpm lower grades, ≤ 140 wpm middle, ≤ 160 wpm upper |
| Counting method | Counted in **words** (not characters); speaker labels, sound effects and music descriptions all count |
| Minimum / maximum dwell | 40 frames (1 second 10 frames) / 6 seconds (background-music symbols excepted) |
| Timing technique | "Borrow" 15 frames (about 0.5 second) before and after the audio; alternatively delete redundancy and shorten the wording |
| Must be verbatim, rate disregarded | Direct quotes from people, statements by public figures, poetry and published quotations, lyrics |
| Case | Mixed case; all capitals only for screams and shouts, never to emphasise a word |
| Line count / breaking | 2 lines preferred, 3-4 when necessary; break at natural pauses, never splitting modifiers, prepositional phrases, name plus title, after a conjunction, or auxiliaries |
| Alignment and position | DCMP recommends **left-aligning** multi-line captions, placing them in the bottom two lines without covering name straps, mouth shapes or key graphics, and moving them to the top when they conflict |

Note the conflict: DCMP leans towards left alignment while Netflix requires centring — **pick one per delivery target; never mix**; for this project, TO VERIFY against the final platform's guide. DCMP's three essentials for captioning are synchronisation, equivalence and accessibility; its five quality goals are accuracy, consistency, clarity, readability and equal access.

### 2.3 Multilingual track naming and language tags

| Language | BCP 47 | ISO 639-2 (as used by ffmpeg for MP4) | Notes |
| --- | --- | --- | --- |
| English | en | eng | |
| French | fr | fra (bibliographic code fre also exists) | |
| German | de | deu (also ger) | |
| Spanish | es | spa | |
| Vietnamese | vi | vie | The two-letter code is unreliable in MP4 |
| Japanese | ja | jpn | |
| Korean | ko | kor | |
| Chinese Simplified / Traditional | zh-Hans / zh-Hant | zho | zho cannot distinguish the two; subtags under BCP 47 are required |
| Undetermined / multiple / no linguistic content | und / mul / zxx | und / mul / zxx | Special codes |

Rule: ffmpeg's `-metadata:s:s:N language=` takes ISO 639-2 three-letter codes; MKV stores both the legacy Language field (ISO 639-2) and LanguageIETF (BCP 47), so it can carry `zh-Hans`; MP4 is more reliable with three-letter codes. **This conclusion comes from third-party compilations and is marked TO VERIFY**, and local testing found that the `title` tag is not written under MP4/mov_text but displays correctly under MKV. Put the type in the track title, for example `title="Chinese (Simplified, SDH)"` or `title="English (CC)"`, so players and reviewers can tell tracks apart; SDH/CC tracks belong on their own track, never merged with ordinary translation subtitles.

### 2.4 Translation compression and cultural adaptation

| Problem | Handling |
| --- | --- |
| Length expansion | English and Chinese lengths are not proportional, so the translation must condense and rewrite rather than follow the source word for word; re-flow the two lines when necessary |
| Fragmented context | Send the whole batch for translation, or concatenate adjacent entries, so pronouns, tense and terminology stay consistent |
| Terminology consistency | Maintain a glossary and enforce uniform personal names, brands and proper nouns |
| Colloquialisms and fillers | Filler words can be cleaned from the text sent for translation, but whether to clean them on screen is a separate decision (SDH in particular must keep hesitations) |
| Culture-bound terms | Flag idioms, slang and internet slang for human review |
| Numbers / units / currencies | Standardise 万 versus 10k, dates and currency formats; Netflix requires currencies to stay in their original denomination, unconverted |
| Bilingual layout | Source language on top, target language below, 2 lines in total; about 14-16 Chinese characters and ≤ 8 English words, so the stack does not become top-heavy |
| In-picture subtitles | Signage, on-screen text and other forced narrative as separate cues or a separate track, never mixed into dialogue |

Subtitle translation is inherently compressive; DCMP's editorial principle is to **preserve the original meaning, content and basic vocabulary** — redundancy may be cut, but a difficult word may not be swapped for a simpler synonym.

## 3. Procedure and workflow (with runnable commands)

Seven-step flow: **① lock the final cut** (a re-edit invalidates hundreds of cues) → ② generate a timed draft → ③ correct the wording by hand (proper nouns, numbers, negations — one dropped not inverts the meaning) → ④ add meaningful non-speech sound → ⑤ add speaker labels → ⑥ make the timing and line breaks readable → ⑦ choose open or closed, export, and attach a transcript and an audio-description script where needed.

Sample SDH SRT excerpt (English, ASCII punctuation):

```srt
1
00:00:01,000 --> 00:00:03,200
[door slams]

2
00:00:03,400 --> 00:00:06,000
MAYA: I did not say that.

3
00:00:06,200 --> 00:00:09,000
[tense music]
[narrator] She was already gone.
```

Multilingual plus SDH on separate tracks (verified on local ffmpeg 8.1.2):

```bash
# 1. Three subtitle tracks: Simplified Chinese translation, Traditional Chinese, English SDH
ffmpeg -y -i input.mp4 -i zh-Hans.srt -i zh-Hant.srt -i en-sdh.srt \
  -map 0:v -map 0:a -map 1 -map 2 -map 3 -c copy -c:s srt \
  -metadata:s:s:0 language=chi -metadata:s:s:0 title="Chinese (Simplified)" \
  -metadata:s:s:1 language=chi -metadata:s:s:1 title="Chinese (Traditional)" \
  -metadata:s:s:2 language=eng -metadata:s:s:2 title="English (SDH)" \
  -disposition:s:0 default output.mkv

# 2. Verify track by track
ffprobe -v error -select_streams s \
  -show_entries stream=index,codec_name:stream_tags=language,title -of json output.mkv

# 3. WebVTT for the web: cue identifiers and positioning, so ::cue can adjust the font size
ffmpeg -y -i en-sdh.srt en-sdh.vtt
```

The resulting WebVTT can use `::cue` to raise contrast and font size (in line with WCAG 1.4.3):

```css
::cue { color: white; background-color: rgba(0,0,0,0.75); font-size: 1.2em; }
```

## 4. Common errors and troubleshooting

| Symptom | Root cause | Fix |
| --- | --- | --- |
| Delivery rejected as not accessible | Plain translation subtitles submitted as CC | Add speaker labels, sound effects and music descriptions, or ship a dedicated SDH track |
| Speakers distinguished by colour alone | Violates WCAG 1.3.1 | Use name labels / `[narrator]`; keep colour as a visual aid only |
| Sound written as `[loud noise]` | Missing source, too vague | Change to `[door slams]`: specific, lower case, present tense |
| Auto-generated captions published without proofreading | Wrong names, numbers, negations | Read through by hand, especially `not`, proper nouns and amounts |
| A dropped "not" inverts the meaning | ASR misrecognition | Three-tier proofreading, with a final reviewer who reads the subtitles without the picture |
| Live captions prepared to Level A | Live captions are 1.2.4, AA | Use professional realtime captioners and do a light clean-up pass on the recording |
| Both Simplified and Traditional tagged zho | ISO 639-2 cannot distinguish them | Use BCP 47 `zh-Hans` / `zh-Hant` in MKV |
| Player skips a language track | Two-letter code or `und` used | Switch to ISO 639-2 three-letter codes |
| Burned-in subtitles used as the only accessible option | Viewers cannot resize or switch them off | Prefer a closed track on corporate and education sites, and produce a separate open version for social |
| Every ambient sound logged throughout | Sound effects treated as an event log | Keep only the sounds that change understanding |
| Lyrics mixed in with background music | Music symbol and verbatim rule not applied | Transcribe lyrics word for word with `♪` at both ends; omit short background music |
| All subtitles drift after a re-edit | Final cut never locked | Re-run timeline alignment after any edit |

## 5. Quick reference

- [ ] Established which deliverable is required — SUB, CC or SDH — and encoded it in the filename and the track title
- [ ] Prerecorded video with speech meets 1.2.2 (A); live captions follow 1.2.4 (AA); audio description follows 1.2.5 (AA)
- [ ] Speaker labels do not rely on colour or position; off-screen speech, emotion and foreign languages all annotated
- [ ] Sound descriptions carry a source, use lower case, present tense and square brackets; lyrics use ♪; background music under 5 seconds omitted
- [ ] Rate checked against the DCMP word count: 130/140/160 wpm, 40 frames to 6 seconds, labels and sound effects included
- [ ] Quotations, statements by public figures, poetry and lyrics are verbatim and exempt from the rate limit
- [ ] Multilingual tracks use ISO 639-2 three-letter codes; Simplified and Traditional use BCP 47 subtags; only one track is set `default`
- [ ] SDH kept on its own track, separate from translation subtitles; in-picture subtitles as separate cues
- [ ] Translation compressed, terminology unified, culture-bound terms reviewed by a human
- [ ] Text contrast ≥ 4.5:1 (large text ≥ 3:1), and a closed version retained
- [ ] Every TO VERIFY compliance obligation and platform detail confirmed with the official source or the client

## References

- W3C WCAG 2.2 — https://www.w3.org/TR/WCAG22/
- W3C WCAG 2.2 Guidelines (full text of Guideline 1.2) — https://w3c.github.io/wcag/guidelines/22/
- DCMP Captioning Key (print) — https://dcmp.org/captioningkey/print
- DCMP Keys to Access — http://keystoaccess.org/learn
- Information for Captioning and Description Vendors — http://www.captionedmedia.org/vendor-info
- Localization Accessibility: WCAG, SDH and Audio Description — https://blog.translastars.com/localization-accessibility-wcag-sdh-audio-description
- Video accessibility: captions, subtitles, and what WCAG expects — https://www.autocap.studio/guides/video-accessibility-captions-guide
- Video Accessibility: A Practical Captioning Guide for WCAG 2.2 — https://reelwords.ai/blog/video-accessibility-captioning-guide
- Accessible video: captions, transcripts, audio description — https://www.granary.digital/accessible-video-captions-transcripts-audio-description.html
- What Is Language In Metadata? (ISO 639-2 / BCP 47) — https://www.metadata2go.com/dictionary/language
- Subtitle Language Tags in MP4 and MKV (TO VERIFY) — https://daohuy.com/en/blog/post-subtitle-language-tags-bcp47-mp4-mkv
- W3C WebVTT 1.0 (cues and ::cue) — https://www.w3.org/TR/webvtt1/
- Bilingual subtitle production practice (Baidu Developer Center) — https://developer.baidu.com/article/detail.html?id=9439722

Retrieved: 2026-11-10
