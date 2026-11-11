# references index

> Category: Navigation | Topic: the shortest path and minimum required reading for each stage or task | Compiled: 2026-11-10 | Applies to: read this file first, before entering references

## How to use the three layers

1. **SKILL.md** decides the process and the red lines; read it first.
2. **This file** decides which documents to read right now, so that 50 documents are not dumped in at once.
3. **A specific document** is opened only when you need a parameter, a command or a template.

Every document follows the same structure, so it can be read selectively:

```
# title → metadata block → core principles / concept comparison → executable spec and parameter tables
→ procedure / workflow (with runnable commands) → common mistakes and troubleshooting → quick-reference checklist → references
```

To find a specific value, searching beats reading end to end:

```bash
grep -n "LUFS"      "02-audio-and-voice/02-audio-post-and-mixing.md"
grep -n "CPS\|reading speed" "03-subtitles/01-subtitle-style-and-layout.md"
grep -n "safe area"    "04-genre-playbooks/01-short-form-and-vlog.md"
grep -n "Article 24" "05-copyright/01-china-copyright-law-and-audiovisual-works.md"
```

## The ten volumes at a glance

| Volume | Files | What it solves | When to open it |
| --- | --- | --- | --- |
| `00-overview` | 3 | capability-domain mapping, evidence grading, file inventory | when you need to confirm how reliable a conclusion is |
| `01-editing-craft` | 4 | shot language, transition rhythm, project standards, colour grading | M3 while planning the edit, M4 while editing and grading |
| `02-audio-and-voice` | 4 | recording and voice production, mixing and loudness, music and SFX, AI voice | when there is voiceover / dubbing / mixing work |
| `03-subtitles` | 4 | layout, format standards, tooling workflow, multilingual accessibility | when making subtitles or delivering subtitle files |
| `04-genre-playbooks` | 6 | structure templates and platform specs for six video types | once the type is settled, to take the timeline template |
| `05-copyright` | 5 | copyright, derivative-work boundaries, music licensing, personality rights, platform rules | commercial use, derivative works, material of uncertain provenance |
| `06-delivery-qc` | 3 | technical checklist, content compliance, review-form templates | M5, before delivery |
| `07-tools-and-resources` | 2 | software ecosystem, stock-asset and font licensing | choosing tools, finding commercially usable assets |
| `08-rsi` | 7 | three-dimension reference evaluation, keyframe baseline, fingerprints, mapping, self-improvement, governance | M2, M5, M6 |
| `09-material-memory` | 4 | material description cards, cache protocol, multi-topic governance, coordination | M1, and any occasion where material is reused |

## Minimum required reading by stage

**M1 Material intake** (do this first, so tokens are not spent twice)

- `09-material-memory/02-cache-reuse-protocol-and-token-savings.md` — the action table for the five states
- `09-material-memory/01-material-description-card-spec.md` — field definitions and V1–V8 validation
- `09-material-memory/templates/model-analysis-prompt.md` — the one-off analysis prompt used on a cache miss

**M2 Reference-style evaluation**

- `08-rsi/02-reference-video-evaluation-framework.md` — dimensions A–G and the five-part explanation
- `08-rsi/03-style-fingerprint-spec.md` — fingerprint fields and evidence grades
- `08-rsi/templates/reference-video-evaluation.md` — fill it in directly
- run `scripts/reference_probe.sh` when objective numbers are needed

**M3 Edit plan**

- `08-rsi/04-fingerprint-to-edit-plan-mapping.md` — parameter transfer and conflict resolution
- `04-genre-playbooks/0X-*.md` — the structural timeline template for that type
- read `01-editing-craft/02` only to fill in rhythm and transition detail

**M4 Production**

Take a single volume from the "doing / reading" table in SKILL.md. Read one volume at a time, so the context is not filled up with irrelevant parameters.

**M5 Finished-cut review**

- `06-delivery-qc/01-technical-spec-checklist.md` — technical items and automated checks
- `06-delivery-qc/02-content-and-compliance-review.md` — items that require human judgement
- `06-delivery-qc/03-qc-report-templates.md` — archiving forms A–G
- run `scripts/qc_scan.sh` first, then work through the form item by item
- `08-rsi/07-keyframe-baseline.md` — diff the cut against the reference baseline; run `scripts/keyframe_diff.py compare`, exit 2 means fix

**M6 Feedback loop**

- `08-rsi/05-feedback-loop-and-self-improvement.md` — error attribution and the nine-step gate
- `08-rsi/06-case-library-and-version-governance.md` — archiving, versions, rollback
- `08-rsi/templates/self-improvement-record.md` — leaving a record

## Frequently cross-cutting questions

| Question | Read |
| --- | --- |
| How far can a derivative edit go before it counts as infringement | the decision tree in `05-copyright/02-derivative-edits-and-fair-use.md` |
| Can I use this piece of music | the three layers of rights in `05-copyright/03-music-sfx-and-recording-licensing.md` |
| Will a font create a copyright problem | `05-copyright/04-likeness-fonts-stock-and-personality-rights.md` |
| Specs for Douyin (抖音) / Bilibili (B站) / WeChat Channels (视频号) | `04-genre-playbooks/01-short-form-and-vlog.md` + `07-tools-and-resources` |
| What loudness should I actually target | the target table in `02-audio-and-voice/02-audio-post-and-mixing.md` |
| How long should a subtitle be, and how long should it stay | `03-subtitles/01-subtitle-style-and-layout.md` |
| Which editing application should I use | `07-tools-and-resources/01-nle-software-and-plugins.md` |
| Free assets that are commercially usable | `07-tools-and-resources/02-stock-assets-and-learning-resources.md` (verify the licence yourself) |

## Naming conventions

- Volume directories: `NN-<name>`; the number is the recommended reading order
- Documents: `NN-<topic>.md`, ordered by process sequence within a volume
- Templates: the `templates/` subdirectory of each volume, ready to copy and fill in
- Scripts: all under `scripts/` at the skill root; documents refer to them as `scripts/xxx` (relative to the skill root)

## Evidence grades at a glance

The labels used throughout the documents follow `00-overview/sources-and-reliability.md`:

| Grade | Meaning | Example |
| --- | --- | --- |
| A | the text of a standard or regulation, an official specification | ITU-R BS.1770, the provisions of the Copyright Law |
| B | official vendor documentation, official platform rules | the ffmpeg documentation, platform creator guidelines |
| C | academic papers, industry white papers | empirical research on editing rhythm |
| D | media reporting, community experience | tool reviews, tutorials |
| E0–E4 | material / evaluation evidence strength (see `08/02`) | E1 reproducible measurement, E4 subjective judgement |

**Check the grade before citing any number**: anything below grade B, or marked TO VERIFY, must not be presented to the user as established fact.

Retrieved: 2026-11-10 | Related: `../SKILL.md`, `00-overview/knowledge-map.md`
