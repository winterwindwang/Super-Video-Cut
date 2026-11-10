# Super-Video-Cut

[English](README.md) | [简体中文](README.zh-CN.md)

> An agent skill for end-to-end video editing delivery: evaluate a reference edit, plan the timeline, cut, mix, subtitle, clear rights, and QC the final file — with measured numbers instead of adjectives.

## Why this exists

Most AI-assisted editing fails in three predictable ways. This skill is built around fixing them.

**1. Style imitation by vibe.** Asked to match a viral edit, a model tends to answer "fast cuts, cinematic feel" — which cannot be executed. Here a reference clip is first measured (cut points, shot-length distribution, loudness, color statistics, contact sheets), and every judgment must carry five parts: observation → evidence → inference → action → confidence. Missing one part voids the item.

**2. Re-analyzing the same footage.** One clip usually serves several topics. Descriptions are cached per file, addressed by content hash, so the video model is called **once** and reused across themes instead of once per topic.

**3. Rights and QC as afterthoughts.** Copyright boundaries and a technical checklist are gates before delivery, not a closing paragraph.

## Install

```bash
git clone git@github.com:winterwindwang/Super-Video-Cut.git ~/.workbuddy/skills/super-video-cut
```

Then trigger it by describing the task — no command needed:

- "Cut a 60s vertical version matching this viral video's style"
- "What is in these clips, and which ones fit the launch video?"
- "Add Chinese subtitles and check the loudness before I upload"

## Requirements

| Dependency | Needed for | Notes |
| --- | --- | --- |
| `ffmpeg` + `ffprobe` | All measurement, QC, subtitle burn-in | Tested on ffmpeg 8.1.2 |
| Python 3 | `material_cache.py` | Standard library only, no pip install |
| `PyYAML` | Optional YAML validation | Falls back to a basic check |

Without ffmpeg the objective measurement is unavailable. The skill will say so rather than invent numbers.

## Three red lines

| # | Rule | Why |
| --- | --- | --- |
| 1 | **Reference first, cut later.** No edit before the user confirms the evaluation. | An unconfirmed style read is rework, not progress. |
| 2 | **Cache before model.** Run `lookup` before spending tokens on any clip. A hit forbids re-analysis. | The same footage is reused across topics; paying twice is waste. |
| 3 | **Compliance and QC gate delivery.** Rights unresolved means no cut; `qc_scan.sh` failing means no delivery. | Fixing a published file is far more expensive than checking it. |

## Workflow

| Stage | Goal | Output |
| --- | --- | --- |
| **M0 Intake** | Lock platform, aspect, duration, narration, commercial use, delivery spec | Requirement sheet |
| **M1 Material memory** | Avoid paying twice for the same clip | Description card, or a cache hit |
| **M2 Style evaluation** | Turn "the feel" into parameters | Evaluation sheet + style fingerprint + one-page verdict |
| **M3 Plan** | Translate the fingerprint into a timeline | Second-level shot plan |
| **M4 Production** | Cut, voice, subtitle, grade | Rough cut + project |
| **M5 QC** | Technical and rights gates | QC sheet + detection logs |
| **M6 Feedback** | Learn from real outcomes | Improvement record (candidates only) |

M2 runs in six steps, and step S6 is a hard stop:

```
S1 rights check → S2 objective probe → S3 watch twice (picture / sound only)
→ S4 rate A–G dimensions → S5 one-page verdict → S6 ★ user confirmation ★
```

Dimensions: **A editing craft**, **B sound design**, **C scene**, plus D subtitles, E narrative, F platform context, and **G rights boundary (mandatory)**. Each action item is tagged `transferable: parameter` or `protected: expression` — style and structure may be learned, the specific shots, lines, music and motion graphics may not be copied.

## Contents

```
super-video-cut/
├── SKILL.md              # workflow, red lines, routing (loaded on trigger)
├── references/           # 10 volumes, loaded only as needed
│   ├── INDEX.md          # shortest path per stage
│   ├── 00-总览/           # capability map, evidence grading, manifest
│   ├── 01-剪辑技巧/       # cutting craft, pacing, engineering, grading
│   ├── 02-配音与音频/     # recording, mixing, loudness, music, TTS
│   ├── 03-字幕系统/       # typography, formats, tooling, accessibility
│   ├── 04-分类型剪辑/     # six genres with timeline templates
│   ├── 05-版权法规/       # copyright, fair use, licensing, platforms
│   ├── 06-成片审查/       # technical QC, content compliance, checklists
│   ├── 07-工具与资源/     # software, assets, licensing caveats
│   ├── 08-RSI自进化/      # reference evaluation, fingerprints, feedback loop
│   └── 09-素材记忆/       # clip description cards and cache protocol
└── scripts/
    ├── material_cache.py     # fingerprint / lookup / register / use / verify / stats
    ├── reference_probe.sh    # cut points, shot lengths, loudness, color, contact sheets
    └── qc_scan.sh            # delivery QC: spec, decode, black, freeze, silence, loudness
```

Reference documents are written in Chinese; the workflow and structure are language-neutral. Detailed tables (loudness targets, subtitle timings, platform specs, copyright clauses) are the substance — read them on demand via `references/INDEX.md` rather than up front.

## Scripts

All three are deliberately dependency-light and have been verified end to end on real files.

```bash
SK="$HOME/.workbuddy/skills/super-video-cut"

# Cache the description of a clip once, reuse it across topics
export MDC_HOME="$PWD/素材缓存"
python "$SK/scripts/material_cache.py" lookup "clip.mp4"

# Measure a reference edit's objective signature
bash "$SK/scripts/reference_probe.sh" "reference.mp4" "probe_out"

# QC the final file before delivery
bash "$SK/scripts/qc_scan.sh" "final.mp4" "qc_out"
```

`material_cache.py` writes to `$MDC_HOME` (default `./素材缓存`), never into the skill directory.

## Evidence, not authority

Numbers in this repository carry an evidence grade: **A** official standard or statute, **B** vendor documentation, **C** academic, **D** secondary reporting. Anything uncertain is marked as to-be-verified rather than stated as fact. See `references/00-总览/资料来源与可信度.md`.

## Scope and limits

- **Not legal advice.** Copyright rules and judicial practice change. Commercial or high-risk projects need counsel and the current official text.
- **Platform specs drift.** Duration, bitrate, safe areas and loudness targets conflict across sources; treat them as "check the official docs and test on upload".
- **Self-improvement parameters are uncalibrated.** The thresholds in volume 08 are self-defined starting values, not validated optima.
- **Roughly 190 items are explicitly flagged as unverified**, each with the disputed point stated.

## License

No license has been chosen yet. Add one before redistributing or reusing this content commercially.
