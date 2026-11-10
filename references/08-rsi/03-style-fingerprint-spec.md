# Style Fingerprint Specification (`sfp-v1`)

> Category: RSI self-improvement | Topic: the parameterised representation of evaluation conclusions, the YAML schema, validation, and version evolution | Compiled: 2026-11-10 | Applies to: the S5 deliverable, which serves as the shared baseline for S7 mapping and L4 deviation review

---

## 1. Definition and purpose

A style fingerprint is a **machine-readable snapshot of the reference-video evaluation**: it compresses the explained judgements in `02` into a set of parameters so that they can be reused, diffed, reviewed and regression-tested.

It is neither a "how good does it look" score nor a shot list. Four design principles:

1. **Parameters and structure only**: it takes only the entries that the G filter in `02` tagged `transferable: parameter`; anything marked `protected: expression` is excluded without exception.
2. **Every value is traceable**: `source` (originating case ID), `evidence` (E1/E2/E3), `confidence` (high/medium/low) and `note` (one sentence) are mandatory.
3. **Confidence tiers are binding**: low-confidence entries may live only in the `hypotheses` section and may not act as hard constraints on the edit.
4. **Diffable**: plain YAML, stable key names, no free-text paragraphs — so versions can be compared and regressions run.

---

## 2. Schema overview

```yaml
sfp_version: sfp-v1
id: SFP-20261110-001
created: 2026-11-10
source_case: CASE-20261110-001
reference:
  title: "Example: 45-second product recommendation short"
  duration_s: 45.2
  platform: "vertical short-form video"
  genre: "04-genre-playbooks/01-short-form-and-vlog"
  probe_log: "case-library/CASE-20261110-001/probe.log"
  assessment: "case-library/CASE-20261110-001/evaluation.md"
evidence_summary:
  e1_ratio: 0.55          # share of all evaluation items backed by objective evidence
  e3_count: 4             # number of interpretive inferences
  low_confidence_count: 2
  overall_confidence: medium
edit: { }        # dimension A, see §3
audio: { }       # dimension B
scene: { }       # dimension C
caption: { }     # dimension D
narrative: { }   # dimension E
context: { }     # dimension F
constraints: { } # summary of dimension G, mandatory
derived_rules: [ ]   # rules derived from the fingerprint that can drive the edit directly
hypotheses: [ ]      # low-confidence / unverified items, excluded from hard constraints
```

**Mandatory top-level keys**: `sfp_version`, `id`, `created`, `source_case`, `reference`, `evidence_summary`, `edit`, `audio`, `scene`, `constraints`. The rest may be empty objects, but the keys must be present.

---

## 3. Field dictionary

Every parameter uses a uniform "value + provenance" structure. The scalar shorthand is allowed, but when it is used, `evidence`/`confidence` fall back to `evidence_summary` and the item is flagged at review.

```yaml
edit:
  shot_median_s:
    value: 1.8
    evidence: E1
    confidence: high
    source: "A1 / probe.cut_table"
    note: "median of the cut list; the 2.6 s mean is skewed by the long tail and is not used"
  shot_p90_s: { value: 4.2, evidence: E1, confidence: high, source: "A1", note: "long shots cluster at the end" }
  cut_density_per_min: { value: 33, evidence: E1, confidence: high, source: "A2", note: "whole-video average" }
  density_curve: { value: [58, 34, 29, 18], evidence: E1, confidence: high, source: "A2", note: "cuts/min per quarter, densest at the opening" }
  cut_anchor_distribution:
    value: { action: 0.45, dialogue_break: 0.26, beat: 0.19, other: 0.10 }
    evidence: E1+E2
    confidence: medium
    source: "A3"
    note: "31 cut points classified by hand; action-to-action dominates"
  transition_mix:
    value: { hard_cut: 0.90, dissolve: 0.06, wipe: 0.04 }
    evidence: E2
    confidence: high
    source: "A4"
    note: "dissolves only across time jumps, 12 frames each"
  scale_progression: { value: "WS→MS→CU cycle; product reveals always cut to CU", evidence: E2, confidence: medium, source: "A5", note: "occurs 4 times" }
  camera_motion: { value: "mostly a slight push-in; handheld only in the opening", evidence: E2, confidence: medium, source: "A6", note: "" }
  jl_cut_frames: { value: [8, 24], evidence: E2, confidence: medium, source: "A7", note: "rule-of-thumb range, calibrate for this project" }
  broll_ratio: { value: 0.32, evidence: E2, confidence: medium, source: "A8", note: "mainly covers jump cuts in the talking-head sections" }
  beat_align_frame_error: { value: 2, evidence: E1+E2, confidence: medium, source: "A9", note: "on the beat in the chorus only, not throughout" }
  fps: { value: 30, evidence: E1, confidence: high, source: "A10 / ffprobe", note: "constant frame rate" }
  slowmo_segments: { value: ["00:31-00:34"], evidence: E2, confidence: high, source: "A10", note: "emphasises the product landing" }

audio:
  bpm: { value: 120, evidence: E2, confidence: medium, source: "B1", note: "hand-tapped, ±2" }
  mood: { value: "bright, ascending, electronic", evidence: E3, confidence: low, source: "B1", note: "inference, reference only" }
  music_in_s: { value: 0.0, evidence: E2, confidence: high, source: "B2", note: "enters on the first frame" }
  drop_align_s: { value: 12.4, evidence: E2, confidence: high, source: "B2", note: "chorus aligns with the first product close-up" }
  voice_type: { value: "female presenter, talking to camera", evidence: E2, confidence: high, source: "B3", note: "" }
  speech_ratio: { value: 0.71, evidence: E2, confidence: medium, source: "B3", note: "derived from the transcript" }
  sfx_per_10s: { value: 6.5, evidence: E2, confidence: medium, source: "B4", note: "11 in the first 10 s" }
  sfx_types: { value: ["whoosh", "impact", "UI click"], evidence: E2, confidence: high, source: "B4", note: "" }
  sfx_cut_coupling: { value: 0.78, evidence: E1+E2, confidence: medium, source: "B5", note: "cut list cross-referenced with the SFX list" }
  music_duck_db: { value: -6, evidence: E2, confidence: medium, source: "B6", note: "music ducks under the voice" }
  integrated_lufs: { value: -14.2, evidence: E1, confidence: high, source: "B7 / ebur128 Summary", note: "streaming target" }
  true_peak_dbtp: { value: -1.3, evidence: E1, confidence: high, source: "B7", note: "" }
  sound_bridge: { value: true, evidence: E2, confidence: medium, source: "B8", note: "pairs with A7" }
  intentional_silence: { value: ["00:29.6-00:30.2"], evidence: E1+E2, confidence: high, source: "B9", note: "0.6 s of negative space before the chorus, not a defect" }
  playback_target: { value: "phone speaker + headphones", evidence: E3, confidence: medium, source: "B10", note: "" }

scene:
  count: { value: 5, evidence: E2, confidence: high, source: "C1/C2", note: "3 indoor / 2 outdoor" }
  duration_dist: { value: [6, 9, 12, 10, 8], evidence: E2, confidence: medium, source: "C2", note: "seconds" }
  composition: { value: "centred subject + top quarter left clear for subtitles", evidence: E2, confidence: high, source: "C3", note: "adapted to the vertical-video UI" }
  camera_height: { value: "eye level, slightly low", evidence: E2, confidence: medium, source: "C4", note: "" }
  lighting_key: { value: "high key, soft", evidence: E2, confidence: high, source: "C5", note: "" }
  color_temp: { value: "warm", evidence: E2, confidence: medium, source: "C5", note: "" }
  yavg: { value: 138, evidence: E1, confidence: high, source: "C6 / signalstats", note: "whole-video average" }
  satavg: { value: 0.42, evidence: E1, confidence: medium, source: "C6", note: "after normalisation" }
  motion_level: { value: medium, evidence: E2, confidence: medium, source: "C7", note: "" }
  aspect: { value: "9:16 / 1080x1920", evidence: E1, confidence: high, source: "C8 / ffprobe", note: "" }
  safe_area: { value: "no key information in the top 12% or bottom 18%", evidence: E2, confidence: medium, source: "C8", note: "rule-of-thumb for the platform UI, TO VERIFY" }
  on_screen_elements: { value: "brand bug permanently in the lower right", evidence: E2, confidence: high, source: "C9", note: "the structure transfers, the specific graphic does not" }
  narrative_role_ratio: { value: { setup: 0.15, build: 0.35, turn: 0.3, payoff: 0.2 }, evidence: E3, confidence: low, source: "C10", note: "inference" }
  non_transferable: { value: ["live-action seaside sunset", "specific product packaging", "the reference's kinetic-type graphics"], evidence: E2, confidence: high, source: "C additional requirement", note: "content layer, must not be transferred" }

caption:
  lines: { value: 2, evidence: E2, confidence: high, source: "D", note: "two lines maximum" }
  chars_per_line: { value: 14, evidence: E2, confidence: medium, source: "D", note: "Chinese text" }
  lead_in_frames: { value: 2, evidence: E2, confidence: medium, source: "D", note: "subtitles run slightly ahead of the voice" }
  on_screen_text_role: { value: "keywords enlarged + kinetic type emphasising selling points", evidence: E2, confidence: medium, source: "D", note: "the structure transfers, the exact wording does not" }

narrative:
  structure: { value: ["hook 0-3s", "pain point 3-12s", "demo 12-31s", "climax 31-38s", "CTA 38-45s"], evidence: E3, confidence: medium, source: "E", note: "inference" }
  emotional_curve: { value: [3, 2, 3, 4, 3], evidence: E3, confidence: low, source: "E", note: "subjective annotation, reference only" }

context:
  aspect: { value: "9:16", evidence: E1, confidence: high, source: "F", note: "" }
  hook: { value: "product on the first frame + high density in the first 3 s", evidence: E2, confidence: high, source: "F", note: "" }
  loudness_policy: { value: "platform target -14 LUFS / -1 dBTP", evidence: E1, confidence: high, source: "F/B7", note: "check the platform spec again" }
  playback_environment: { value: "mobile portrait, autoplay muted", evidence: E3, confidence: medium, source: "F", note: "this is why subtitles are always on" }

constraints:
  principle: "idea/expression dichotomy: transfer parameters and structure, never expression"
  protected_items:
    - "the reference's dialogue and narration"
    - "its original music and specific sound-effect assets"
    - "its kinetic-type wording and unique graphics"
    - "its signature shot staging and character styling"
  transferable_scope: ["rhythm parameters", "structural proportions", "loudness targets", "colour-statistics tendencies", "subtitle layout parameters"]
  forbidden_actions: ["reusing frames", "dubbing off the audio track", "recreating shots frame by frame", "removing or obscuring watermarks and rights-management information"]
  legal_review_required: false
  note: "this section constrains the creative workflow and is not legal advice; commercial projects require review by counsel"
```

---

## 4. Derived rules and the hypothesis section

`derived_rules` is the bridge from fingerprint to edit plan, in a format that `04` can consume directly:

```yaml
derived_rules:
  - id: R-001
    when: "segment == opening && duration <= 3s"
    apply: "shot_len ∈ [0.8, 1.2] s, cut_count == 3"
    priority: high
    weight: 0.8
    basis: "A1/A2 + cut_anchor_distribution"
    status: active          # active | candidate | retired
  - id: R-002
    when: "voiceover_present"
    apply: "music_duck = -6 dB; integrated_lufs target -14"
    priority: high
    weight: 0.9
    basis: "B6/B7"
    status: active
  - id: R-003
    when: "chorus_onset"
    apply: "align cut to beat, |frame_error| <= 2"
    priority: medium
    weight: 0.5
    basis: "A9/B2"
    status: candidate       # medium confidence, shadow-run first
```

`hypotheses` holds low-confidence, unverified items. They are excluded from hard constraints, but they are a legitimate source of candidates during self-improvement:

```yaml
hypotheses:
  - id: H-001
    statement: "the dense opening is a feature of this account rather than of this category"
    evidence: E3
    confidence: low
    test: "compare density_curve against 3 more videos in the same category"
```

The `weight` field is the main object that L5 self-improvement operates on; only rules with `status: active` drive the edit. `candidate` rules run in shadow mode only.

---

## 5. Validation rules (must pass before writing)

| # | Rule | What to do if it fails |
| --- | --- | --- |
| V1 | All mandatory top-level keys present | Fill them in; otherwise the fingerprint may not proceed to S6 |
| V2 | Every parameter has `value`; `evidence`/`confidence`/`source`/`note` are recommended | Missing provenance → send back to S4 to be filled in again |
| V3 | No `protected: expression` entry and no specific asset name appears anywhere | Delete it and return to the G filter |
| V4 | Entries with `confidence: low` may not appear in `active` rules of `derived_rules` | Downgrade to `candidate` or move into `hypotheses` |
| V5 | Numeric parameters carry units and match the probe log (e.g. `integrated_lufs` ↔ `ebur128 Summary`) | Re-check `probe.log` |
| V6 | `constraints.protected_items` and `forbidden_actions` are non-empty | Fill them in |
| V7 | `evidence_summary.e3_count` matches the number of inference entries | Reconcile |
| V8 | The file is valid YAML, UTF-8 and parseable | Fix the syntax |

**Suggested validation command** (if Python + PyYAML are available locally):

```bash
python -c "import yaml,sys; d=yaml.safe_load(open(sys.argv[1],encoding='utf-8')); assert d['sfp_version']=='sfp-v1'; print('OK', len(d.get('derived_rules',[])), 'rules')" "SFP-20261110-001.yaml"
```

> On the local machine (2026-11-10) **PyYAML is confirmed not installed**: the command above needs `pip install pyyaml` first, or use any other YAML parser. Without a parser installed, at minimum do the basic checks — UTF-8 encoding, no tab indentation, all V1 mandatory top-level keys present, and V6's `constraints.protected_items` and `forbidden_actions` non-empty.

---

## 6. Version evolution

- `sfp-v1` is a **one-instance-per-case** version and is not the rules-library version. The rules library is versioned separately as `rules-vN`, recorded in `06-case-library-and-version-governance.md`.
- Allowed evolution: adding fields (backwards-compatible), revising `weight` and `status`, promoting `hypotheses` into `derived_rules`.
- Forbidden evolution: deleting mandatory keys, changing the meaning of an existing key, silently overwriting an old fingerprint.
- Every revision produces a new `id` and keeps the old file; the diff must be attached to the self-improvement record.
- Fingerprints are linked to the evaluation table and the probe log through `source_case`, and the three must not be archived separately.

---

## 7. Quick reference

- [ ] Contains `transferable` parameters only, with no specific expression
- [ ] Every value traces back to an evaluation-table entry and the probe log
- [ ] Low-confidence entries are in `hypotheses`, not used as hard constraints
- [ ] `derived_rules` active/candidate status is correct
- [ ] `constraints` is non-empty and lists the forbidden actions
- [ ] Passes validation V1–V8
- [ ] Archived as a three-piece set with `source_case` (evaluation table / log / fingerprint)

---

## References

- YAML 1.2 specification: https://yaml.org/spec/1.2.2/
- This volume, `01-overview-and-design-principles.md` and `02-reference-video-evaluation-framework.md`
- `../06-delivery-qc/01-technical-spec-checklist.md` (measurement conventions and ffmpeg commands)
- `../00-overview/sources-and-reliability.md` (evidence grading and the TO VERIFY convention)

Retrieved: 2026-11-10. The sample data is a **fictional demonstration** and does not represent measured values from any real video; the field value conventions are starting suggestions and need calibrating per project.
