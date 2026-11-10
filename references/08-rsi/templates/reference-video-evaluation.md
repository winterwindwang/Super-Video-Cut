# Reference-Video Evaluation Form (ready to fill in)

> Category: RSI self-improvement | Topic: the dimension-by-dimension evaluation record for stage S4 | Compiled: 2026-11-10 | Applies to: every time a reference video is received

> ⚠️ **The mandatory-explanation constraint**: every row must fill all four of ①observation, ②basis, ③inference and ④action item, and must state intensity, confidence and a G tag. If any one is missing, the row is void and does not enter the fingerprint. Low confidence may never become a hard constraint.

---

## 0. Basic information

| Field | Entry |
| --- | --- |
| Case ID | `CASE-YYYYMMDD-NNN` |
| Reference video title / source | |
| Local file / how it was obtained | |
| Duration / aspect ratio / frame rate / platform | |
| Video type (which book of the 04 volume it maps to) | |
| Probe-script output paths | `probe.log` / `probe.json` / `sheet.png` |
| Evaluator / date | |
| Compliance pre-check: analysis only, no reuse of expression | ☐ Confirmed |
| S6 user confirmation | ☐ Pending　☐ Confirmed (date / corrections:) |

---

## 1. Dimension A · Editing craft (★ core, all 10 items mandatory)

| # | Item | ①Observation (fact + timecode/value) | ②Basis (tool · evidence grade) | ③Inference (intent and effect) | ④Action item (executable parameter for this edit) | Intensity 0-4 | Confidence | G tag |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A1 | Shot-duration distribution | | | | | | | |
| A2 | Cut-density curve | | | | | | | |
| A3 | Basis of cut points | | | | | | | |
| A4 | Transition types and frame counts | | | | | | | |
| A5 | Shot-scale sequence and assembly | | | | | | | |
| A6 | In-shot kinetic energy | | | | | | | |
| A7 | J-cut / L-cut | | | | | | | |
| A8 | B-roll ratio | | | | | | | |
| A9 | Beat-alignment frame error | | | | | | | |
| A10 | Frame rate / slow motion / speed ramps | | | | | | | |

**Dimension A, must answer**: if you were allowed to change only one parameter, which one is the skeleton of this video's rhythm? Why?
> Answer:

---

## 2. Dimension B · Sound effects and sound design (★ core, all 10 items mandatory)

| # | Item | ①Observation | ②Basis | ③Inference | ④Action item | Intensity 0-4 | Confidence | G tag |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B1 | BPM / music structure / mood | | | | | | | |
| B2 | Music in and out points, chorus alignment | | | | | | | |
| B3 | Voice type and share of runtime | | | | | | | |
| B4 | SFX density and types | | | | | | | |
| B5 | SFX–cut-point coupling | | | | | | | |
| B6 | Level relationships and ducking | | | | | | | |
| B7 | Integrated LUFS / True Peak | | | | | | | |
| B8 | Sound bridges and cross-scene carry | | | | | | | |
| B9 | Silence and negative space (requires human confirmation) | | | | | | | |
| B10 | Frequency range / space / playback environment | | | | | | | |

**Dimension B, must answer**: is the music driving the edit, or the edit driving the music? What is the evidence (the A9 frame-error distribution)?
> Answer:

---

## 3. Dimension C · Scene and image (★ core, all 10 items mandatory)

| # | Item | ①Observation | ②Basis | ③Inference | ④Action item | Intensity 0-4 | Confidence | G tag |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | Scene inventory (number / timecode / location / function) | | | | | | | |
| C2 | Scene-change frequency and segments | | | | | | | |
| C3 | Composition preferences and negative space | | | | | | | |
| C4 | Camera height and shot-scale habits | | | | | | | |
| C5 | Lighting and colour temperature | | | | | | | |
| C6 | Colour statistics (YAVG / SATAVG / dominant colours) | | | | | | | |
| C7 | Motion and stability | | | | | | | |
| C8 | Aspect ratio, safe area, UI occlusion | | | | | | | |
| C9 | In-frame elements (kinetic type / props / brand) | | | | | | | |
| C10 | Share of narrative function by scene | | | | | | | |

**Dimension C, must answer**: which scene features depend on the specific content and cannot transfer? Which are only structure and can transfer?
> Non-transferable (content):
> Transferable (structure):

---

## 4. Extended dimensions (at least 2 entries each for D/E/F)

| # | Dimension | ①Observation | ②Basis | ③Inference | ④Action item | Intensity | Confidence | G tag |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| D1 | Subtitle layout and timing | | | | | | | |
| D2 | Role of kinetic type / on-screen graphics | | | | | | | |
| E1 | Narrative structure and segment proportions | | | | | | | |
| E2 | Emotional curve (E3 inference, must be labelled) | | | | | | | |
| F1 | Platform specs and first-frame hook | | | | | | | |
| F2 | Audience and playback environment | | | | | | | |

---

## 5. Dimension G · Compliance and replicability boundary (mandatory summary)

| # | From entry | Verdict | Note |
| --- | --- | --- | --- |
| G1 | | `transferable: parameter` / `protected: expression` | |
| G2 | | | |
| G3 | | | |
| G4 | | | |
| G5 | | | |

| Item | Content |
| --- | --- |
| Prohibited-transfer list (the reference's dialogue / music / kinetic type / shot staging / character styling, etc.) | |
| Forbidden-action confirmation (frame reuse / dubbing off the audio track / frame-by-frame recreation / watermark removal) | ☐ Each item confirmed |
| Is legal review required | ☐ No　☐ Yes (reason:) |

> Basis: the idea/expression dichotomy; substantial-similarity analysis compares the selections, choices, arrangement and design contained in the expression. This is a constraint on the creative workflow and does not constitute legal advice.

---

## 6. Paste area for objective probe results

| Metric | Measured value | Source command |
| --- | --- | --- |
| Duration / resolution / frame rate | | `ffprobe` |
| Cut count / median shot length / p90 | | `select scene` + adjacent difference |
| Cut density per segment | | bucketed cut list |
| Integrated LUFS / LRA / True Peak | | `ebur128=peak=true` Summary |
| Silent intervals (human-confirmed as intentional / defect) | | `silencedetect` |
| Mean brightness / saturation | | `signalstats` |
| Black-frame / freeze-frame anomalies | | `blackdetect` / `freezedetect` |
| Contact-sheet location | | `sheet.png` |

---

## 7. One-page conclusion (S5 output, handed to the user for confirmation)

| Item | Content |
| --- | --- |
| **The three most decisive features** (ordered by confidence, one sentence each) | 1.<br>2.<br>3. |
| **The three non-transferable items** | 1.<br>2.<br>3. |
| **How I intend to apply this to your footage** (3–5 executable parameters) | |
| **Where my judgement is uncertain** (low confidence / E3 inference / information I need from you) | |
| Evidence structure | E1 ___ entries / E2 ___ entries / E3 ___ entries / E4 ___ entries; low-confidence ___ entries |
| Overall confidence | ☐ High　☐ Medium　☐ Low |
| Related artefacts | Fingerprint `SFP-___` / probe log / contact sheet |

---

## 8. S6 user confirmation gate

| Item | Entry |
| --- | --- |
| User's verdict | ☐ Pass　☐ Needs correction (see below)　☐ On hold |
| User's corrections | |
| IDs of items re-evaluated after correction | |
| Confirmation date / confirmed by | |

> **No edited output or final timeline may be produced before confirmation is obtained.**

---

## 9. Worked example (for comparison)

| # | Item | ①Observation | ②Basis | ③Inference | ④Action item | Intensity | Confidence | G tag |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A3 | Basis of cut points | A hard cut at 00:07.12, medium shot → product close-up; the cut lands on the third frame after the hand-raise begins; 22 of the 31 cut points fall on an action or a dialogue break | Probe-script cut list (E1) + frame-by-frame comparison of 00:07.08/00:07.12 (E2) | Invisible editing of the action-to-action kind, using momentum to carry the seam while shifting attention from the person to the product | For this edit, place the product-reveal cut 1–2 frames before the peak of the action; align all other cut points to dialogue or breath breaks | 4 | High | `transferable: parameter` |

Discarded counterexample: "the edit is very smooth and very cinematic" — no observation, no basis, no action item, no confidence; the whole entry is void.

---

## References

- `../02-reference-video-evaluation-framework.md` (the seven dimensions and the mandatory four-part explanation)
- `../03-style-fingerprint-spec.md` (mapping from evaluation items to fingerprint fields)
- `scripts/reference_probe.sh` (E1 objective probe commands)
- `../../06-delivery-qc/01-technical-spec-checklist.md` (measurement definitions)

Retrieved: 2026-11-10.
