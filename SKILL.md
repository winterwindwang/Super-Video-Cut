---
name: super-video-cut
description: End-to-end video editing delivery skill covering multi-dimensional evaluation of a reference/viral video's style (editing craft, sound, scene — each item justified with observation-evidence-inference-action-confidence), material memory and deduplication (analyse footage once, reuse the description across topics, avoid re-requesting a vision model), edit plans and timeline mapping, voice-over mixing and loudness compliance, subtitle production and layout, differentiated cutting for six video genres, delivery QC, and derivative-work copyright self-checks. Use when asked to edit or re-cut a video, do a mashup or derivative edit, match a reference or viral video's style, add subtitles or voice-over, grade colour, export to platform specs, QC a finished cut, or judge whether footage or a derivative edit infringes copyright. Ships runnable ffmpeg/ffprobe commands, EBU R128 and ITU-R BS.1770 loudness targets, W3C WebVTT and other subtitle format standards, and Chinese copyright law alongside US/EU fair use and DMCA rules.
agent_created: true
---

# Super-Video-Cut

## Positioning

Treat every editing job as **an engineering delivery with an evidence chain**, not a pile of clips assembled by feel. This skill supplies reproducible objective measurement, itemised and justified evaluation, reusable timeline templates, pre-delivery QC, and copyright boundaries that run through the whole process.

`references/` holds the deep material, split by capability domain (about 50 documents, most of them 100–250-line parameter tables and specifications). **Do not pre-read all of it** — follow the routing below and read only the 1–3 documents the current stage needs.

Volume shorthand used throughout this file: `09/02` means `references/09-material-memory/02-*.md`.

## Three red lines

Violate any one of them and you must not deliver.

1. **Reference style: evaluate first, cut second.** When the user supplies a reference video, you must complete the three-dimension evaluation (editing craft / sound / scene) with an itemised justification for every entry, and get user confirmation before touching the timeline. Producing a cut without that confirmation counts as rework.
2. **Footage: check the cache before you reach for a model.** Before analysing any video material, run `material_cache.py lookup`. On a hit, read the material description card directly — calling a video model to look again is **forbidden**; only on a miss do you run one full analysis and register it.
3. **Compliance and QC come first.** Do not cut a plan whose copyright risk is undetermined, and do not hand over a finished file that `qc_scan.sh` has not passed. The legal volume is reference material, not legal advice; for commercial or high-risk projects, tell the user to have it reviewed by counsel.

## Main workflow M0–M6

| Stage | Goal | Must read | Output |
| --- | --- | --- | --- |
| M0 Intake | Lock down executable parameters | This file | Brief |
| M1 Footage intake | Never pay for the same tokens twice | `09/02` + `scripts/material_cache.py` | Material card or cache hit |
| M2 Style evaluation | Turn "a feeling" into parameters | `08/02` + `08/03` + `scripts/reference_probe.sh` | Evaluation sheet + fingerprint + one-page conclusion |
| M3 Edit plan | Fingerprint → timeline | `08/04` + the matching genre volume | Second-level plan |
| M4 Production | Cut / voice / subtitles / grade | `01` / `02` / `03` as needed | Rough cut and project |
| M5 Delivery QC | Technical + compliance pass, then diff against the reference | `06/01` + `06/02` + `06/03` + `08/07` | QC report + diff report + paired sheet |
| M6 Feedback | Produce candidates only, never auto-change rules | `08/05` | Self-improvement record |

### M0 Intake: ask for missing parameters, at most 3 questions

You must obtain: **platform and aspect ratio** (determines safe area and duration), **total duration**, **whether voice-over/dubbing is needed**, **whether it is commercial**, **delivery spec** (resolution / bitrate / container).

Infer and state anything that can be inferred from what you already have; do not interrogate the user item by item. Whether the work is commercial directly determines which music and footage you may use — if that is unclear, you must ask.

### M1 Footage intake: the action for each of the five states is hard-coded

```bash
SK="$HOME/.workbuddy/skills/super-video-cut"
export MDC_HOME="$PWD/material-cache"     # keep the cache inside the project, never inside the skill directory
python "$SK/scripts/material_cache.py" lookup "<footage path>"
```

| State | Action |
| --- | --- |
| `HIT` | **Do not call a video model.** Read `$MDC_HOME/cards/<MID>.yaml` and do topic adaptation only |
| `MISS` | Local E1 probe → **one** full analysis request using `references/09-material-memory/templates/model-analysis-prompt.md` → fill the card → `validate` → `register` |
| `STALE` | The footage changed; mark the old card `superseded` and redo as a MISS |
| `HIT_BLOCKED` | Rights status is not cleared; do not use it — resolve the rights first |
| kill switch | When `_config.json` has `cache_enabled=false`, treat everything as MISS; bypassing it is forbidden |

The description card has three layers: L0 identity (hash / specs), L1 material description (what it shows / where it was shot / what the style is / whether it is usable), L2 topic adaptation (which seconds this topic takes, and what narrative role they play). **"Works well as the opening for topic X" belongs in L2 only** — putting it in L1 contaminates every other topic.

The location field is a hard rule: without on-screen text, a landmark, or a shooting record, set `place_name: null`. Never infer a city from "there is sea and a palm tree".

### M2 Style evaluation: six steps whenever the user supplies a reference video

```
S1 compliance pre-check → S2 objective probe → S3 two full viewings → S4 dimension-by-dimension evaluation
→ S5 one-page conclusion → S6 ★user confirmation gate★
```

- **S1** Analyse only, never reuse its expression. Opening and closing titles, dialogue, music, kinetic text, and shot staging are all tagged `protected: expression`.
- **S2** Run the probe script for reproducible numbers (cut points, shot lengths, loudness, silence, colour statistics, contact sheets).
- **S2b** Record the keyframe baseline while the reference is in front of you — `keyframe_diff.py extract`. It stamps one keyframe per shot plus its luma/saturation, so the finished cut can be diffed against it later instead of argued about from memory. Fill `shot_size` and `composition` in `shots.csv` by hand; the tool measures, it does not interpret.
- **S3** Watch the whole thing twice: once for picture only, once **for sound only**. Skipping through at speed loses rhythm and held beats — this is the most common methodological error.
- **S4** Evaluate item by item across the three core groups — A editing craft / B sound / C scene (10 sub-items each) — plus D subtitles, E narrative, F platform context, and **G compliance boundary (mandatory)**.
- **S5** Deliver a one-page conclusion: 3 key characteristics, 3 non-transferable items, overall confidence.
- **S6** Hand it to the user for confirmation. **Without that confirmation you may not enter M3.**

**Every evaluation entry must fill all five parts; a missing part voids the whole entry:**

> ① Observation (timecode + concrete phenomenon) ② Basis (evidence ID) ③ Inference (why it was designed this way) ④ Action item (how this cut uses it) ⑤ Confidence (high/medium/low + reason)

Counter-example (must never be output): "The editing is smooth and very cinematic." — no timecode, no basis, no action item, nothing executable.

Every action item must carry a transfer tag: `transferable: parameter` (rhythm, duration, loudness, shot-size sequence — learnable) or `protected: expression` (specific shots, dialogue, music, kinetic text — not reproducible). **Style and formula sit in the realm of ideas and may be borrowed; expression may not be copied.** That is this skill's copyright floor, not a suggestion.

### M3 Edit plan: translate the fingerprint into a second-level timeline

Read the mapping rules in `08/04` and produce a directly executable timeline: in/out point for every clip, shot size, transition type and duration in frames, sound-effect cue points, subtitle in/out points, and loudness target.

Conflict resolution order: **explicit user request > hard platform limits > reference-video characteristics > default aesthetics**. When the footage cannot support something, say so plainly — "the reference uses technique X; this project has no matching footage, so Y replaces it" — rather than forcing it.

### M4 Production: read exactly one volume per current action

| Doing | Read |
| --- | --- |
| Rhythm, transitions, axis | `01/01`, `01/02` |
| Project organisation, proxies, conform, delivery | `01/03` |
| Colour grading, Log/LUT, HDR | `01/04` |
| Voice recording, delivery, ADR | `02/01` |
| Mixing, loudness, EQ/compression | `02/02` |
| Score, sound effects, sound design | `02/03` |
| AI voice, TTS, SSML | `02/04` |
| Subtitle layout and duration | `03/01` |
| SRT/VTT/ASS/TTML formats | `03/02` |
| Transcription, alignment, burn-in | `03/03` |
| Multilingual, CC/SDH, accessibility | `03/04` |
| How to cut a specific genre | `04/01`–`04/06` |

Loudness anchors (full target table in `02/02`): streaming around −14 LUFS, podcast/Apple around −16 LUFS, broadcast EBU R128 at −23 LUFS, with True Peak generally required at ≤ −1 dBTP. **Defer to the target platform's official documentation**; if unsure, measure first, then decide.

### M5 Delivery QC: run the script first, then judge as a human

```bash
bash "$SK/scripts/qc_scan.sh" "<finished file>" "<output directory>"
```

One run yields a spec JSON, decode integrity, black-frame/freeze detection, silence, loudness, and a contact sheet. The script can only find **technical anomalies** — content and compliance must go through the tables by hand:

- `06/01` technical specification checklist (resolution / frame rate / colour / bitrate / audio tracks / duration / naming)
- `06/02` content and compliance review (facts, sensitive content, prohibited advertising claims, rights documentation)
- `06/03` Tables A–G fill-in templates (for the archive)

**Then diff the finished cut against the reference baseline** (skip only if there was no reference):

```bash
python "$SK/scripts/keyframe_diff.py" extract "<finished file>" --out case/mine_kfs
python "$SK/scripts/keyframe_diff.py" compare case/ref_kfs case/mine_kfs --out case/diff
```

Exit code 2 means blocking: the shot count, the runtime or a cut position is off by more than tolerance. Read `case/diff/diff_report.md` for the verdict, then open `diff_sheet.png` — one row per shot, left is the reference, right is your cut. **Pixels are never compared**; the diff judges structure and the systematic image profile, and leaves composition to your eyes. Warnings are prompts to look, not defects; record what you decided.

QC severity: **blocking** (black frames, missing audio track, loudness out of tolerance, infringement risk) must be fixed; **improvement** items may ship once logged; **suggestion** items wait for the next version.

### M6 Feedback loop: one hit video never changes a rule

Once real feedback arrives (completion rate, conversion, client notes), do error attribution per `08/05` and write it to `08/case-library/<CASE-ID>/self-improvement-record.md`.

Hard rule: a single case produces **candidates** only; a change takes effect only after ≥5 same-direction samples, a frozen regression set, human sign-off, versioning, and a canary release. The self-improvement engine **must not automatically rewrite** the E1/E2 objective fields of a material description card — the cache would spread one error across every later topic, while the hit records still look perfectly normal.

## Shortest path once triggered

| The user says | Do this |
| --- | --- |
| "Cut something in the style of this viral video" | Full M2 flow → S6 confirmation gate; **do not start cutting** |
| "Edit this video for me" | M0 ask platform/duration/commercial → M1 footage → M3 plan |
| "Is this footage usable, what does it show?" | M1 `lookup`; answer straight away on HIT, analyse only on MISS |
| "Add subtitles" | `03/01` layout + `03/03` transcription and alignment; check reading speed and minimum duration |
| "The voice-over sounds bad" | `02/01` recording → `02/02` processing chain → measure loudness |
| "Export for Douyin / WeChat Channels / Bilibili" | `04/01` platform specs + `06/01` delivery check |
| "Would this edit infringe anything?" | `05/02` decision tree + dimension G in `08/02`; give a risk tier, not a conclusive legal opinion |
| "Is the finished cut OK?" | `qc_scan.sh` + `06/01` / `06/02` item by item |
| "Does my cut actually match the reference?" | `keyframe_diff.py compare`, read `diff_report.md`, then judge `diff_sheet.png` row by row |

## Scripts

| Script | Purpose | Dependencies |
| --- | --- | --- |
| `scripts/material_cache.py` | Footage fingerprint, cache lookup, registration, reuse, validation, statistics (8 subcommands) | Python 3, no third-party packages |
| `scripts/reference_probe.sh` | Objective probe of a reference or footage file: cut points, shot lengths, loudness, silence, colour, contact sheets | bash + ffmpeg/ffprobe |
| `scripts/qc_scan.sh` | Technical QC of a finished file: specs, decode, black frames, freezes, silence, loudness, contact sheet | bash + ffmpeg/ffprobe |
| `scripts/keyframe_diff.py` | Per-shot keyframe baseline (`extract`) and structural diff against it (`compare`); exit 2 on a blocking difference | Python 3, no third-party packages |

Check the environment first: `ffmpeg -version && ffprobe -version && python --version`. Without ffmpeg every objective measurement is unavailable — in that case tell the user plainly that only manual evaluation is possible and no reproducible metrics can be given. Never fabricate numbers.

## Pre-delivery self-check

- [ ] The reference went through S1–S6 and the user has confirmed (if a reference was used)
- [ ] Every piece of footage can be traced in the cache to its source and rights status
- [ ] No unsupported phrases like "smooth", "premium", or "textured" appear in the evaluation or the plan
- [ ] Loudness has been measured and sits inside the target tolerance; True Peak is under the limit
- [ ] Subtitles do not overflow the safe area, contain no typos, and meet the reading-speed limit
- [ ] `qc_scan.sh` reports no blocking items, and Tables A–G are filled in
- [ ] Rights documentation for music / fonts / likeness / stock is complete, or the risk tier is stated
- [ ] Delivery file naming, container, and bitrate match the platform requirements

## Scope of the material (must be stated to the user)

- **The legal volume is not legal advice.** Articles and judicial positions change; for commercial or high-risk projects have counsel review it and rely on the latest official text.
- **Platform parameters change.** Duration, bitrate, safe area, and loudness targets conflict across sources, so they are always marked "subject to the platform's latest official documentation" — upload and preview to verify before delivery.
- **The self-improvement parameters have no industry standard.** η, δ, N_min and the rest in volume `08` are this library's own starting values; they exist to make the process runnable, not because they are validated optima.
- **About 190 "TO VERIFY" items** are itemised in the body or at the end of each document, concentrated in `references/00-overview/sources-and-reliability.md` (with A/B/C/D evidence grades and P0/P1/P2 priorities). Check that file's evidence grade before citing anything.

## Routing and indexes

- `references/INDEX.md` — shortest path and minimum required reading per stage or task
- `references/00-overview/knowledge-map.md` — full capability-domain mapping and troubleshooting quick look-up
- `references/00-overview/sources-and-reliability.md` — evidence grades, source list, TO VERIFY items
- `references/00-overview/manifest.csv` — machine-readable file index

When searching a large file, locate by keyword instead of reading it end to end, e.g. `grep -n "LUFS" references/02-audio-and-voice/02-audio-post-and-mixing.md`.
