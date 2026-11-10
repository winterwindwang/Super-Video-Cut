# Mapping a Style Fingerprint to an Edit Plan

> Category: RSI self-improvement | Topic: parameter-transfer rules, conflict resolution, material adaptation and deviation tolerance | Compiled: 2026-11-10 | Applies to: the S7 stage, once S6 user confirmation is obtained; produces a timeline plan that can be executed directly

> ⚠️ This document is a reference for the creative workflow and **does not constitute legal advice**; for decisions involving clearance and compliance, see the 05-copyright volume and have counsel review.

---

## 1. What mapping is, and where it stops

A style fingerprint describes **the reference video's parameters**; an edit plan has to fit **your own material, runtime, platform and compliance requirements**. Mapping is not copying numbers, it is "approximating the relative relationships as closely as the constraints allow".

For example: the reference has a median shot length of 1.8 s, but all your material is 8 s or longer and you have only 12 shots. Copying 1.8 s outright shreds every shot and breaks the meaning. The right move is to keep the **relative relationships** (dense at the opening, sparse at the end, roughly 3:1 density ratio) and scale the absolute durations into the range your material can support (say, 2.6 s / 5.0 s).

**Three iron rules**:
1. Transfer only `transferable: parameter`; `protected: expression` never enters the plan.
2. Relative relationships outrank absolute numbers; absolute numbers yield to the physical constraints of the material.
3. Every mapping must be able to answer "what happens if we don't do this?" — a rule that cannot answer it does not go into the plan.

---

## 2. Conflict-resolution priority (highest to lowest)

When the fingerprint demands something that clashes with another constraint, decide strictly in this order and write the reasoning into the plan:

| Priority | Constraint | Example |
| --- | --- | --- |
| P0 | Law and compliance (the 05 volume, the G filter, platform rules) | the reference's music appears in the fingerprint → strike it, no discussion |
| P1 | The user's explicit requirements (what was confirmed at S6 + this brief) | the user says "no voiceover" → overrides `speech_ratio: 0.71` |
| P2 | Delivery specifications and the 06 volume review standards | loudness must be −14 LUFS / ≤ −1 dBTP, overriding the value measured from the reference |
| P3 | The physical constraints of the material | usable shot count, runtime, image quality, whether there is an audio track |
| P4 | `confidence: high` active rules in the fingerprint | median shot duration, cut-density curve |
| P5 | `confidence: medium` active rules in the fingerprint | J/L-cut frame offset, amount of ducking |
| P6 | `candidate` rules and `hypotheses` | recorded in shadow mode only; they do not drive the edit |
| P7 | Default rules of thumb (volumes 01–04) | the fallback when none of the above applies |

Every conflict must leave a trace: `conflicting item / what was adopted / what was overridden / reason / expected impact`. These traces are important input for L5 error attribution — a rule that is always overridden is a rule that itself needs revising.

---

## 3. Field-by-field mapping rules

| Fingerprint field | Mapping action | How to scale / adapt | Fallback when in conflict |
| --- | --- | --- | --- |
| `edit.shot_median_s` | Set the base shot duration | Scale in both directions by `target runtime / reference runtime` and by the number of usable shots; preserve the **proportions** of opening / middle / ending first | Not enough material → relax by up to +50% and reduce cut density rather than shredding meaning |
| `edit.density_curve` | Allocate a cut budget per segment | Normalise to proportions, then redistribute the cut count over the target runtime | Different number of segments → interpolate linearly across segments |
| `edit.cut_anchor_distribution` | Decide the mix of cut-point types | Transfer the proportions directly; action and dialogue breaks take priority | No action footage → switch to dialogue breaks or information turns |
| `edit.transition_mix` | Transition-type mix | Transfer directly; convert dissolve frame counts to the project frame rate | Platform style does not fit → raise the hard-cut share |
| `edit.scale_progression` | Shot-size progression template | Transfer the sequence pattern, not the specific camera positions | Material has a single shot size → simulate with reframing / push-ins; never fake an angle |
| `edit.jl_cut_frames` | Audio offset in frames | Convert by frame rate (25↔30 fps needs ×1.2) | No separate audio track → skip |
| `edit.broll_ratio` | B-roll coverage | Transfer directly | Not enough B-roll → protect the jump cuts in the talking-head sections first, cover the rest with graphics or stills |
| `edit.beat_align_frame_error` | Beat-sync precision | Enable only in the passages where the reference is on the beat as well | Different music → re-align to the new track's beats; do not force the same timecodes |
| `audio.bpm` / `mood` | Direction for track selection | **Transfer energy and BPM range only**; do not pick the same track | Limited library → keep the energy curve, drop the exact BPM |
| `audio.music_in_s` / `drop_align_s` | Position within the music structure | Convert to proportions of the target runtime (e.g. 12.4/45.2 → 0.27) | Different track structure → align to the "first product reveal" event rather than to seconds |
| `audio.sfx_cut_coupling` | Proportion of cut points carrying an SFX | Transfer the proportion directly | Limited SFX library → keep coupling in the climax, simplify the rest |
| `audio.music_duck_db` | Sidechain ducking amount | Transfer directly | No voice → disable |
| `audio.integrated_lufs` / `true_peak_dbtp` | Mix targets | **P2 takes priority**: use the delivery platform's target, not the value measured from the reference | — |
| `audio.intentional_silence` | Placement of negative space | Transfer the structure "silence sits before the climax", not the seconds | Rhythm does not fit → shorten or drop it, and record that |
| `scene.yavg` / `satavg` / `lighting_key` | Grading direction | Transfer the relative tendency (brighter / warmer), not frame-accurate values | Material varies widely in colour temperature → prioritise consistency over exact numbers |
| `scene.composition` / `safe_area` | Composition and safe area | Transfer directly (critical for vertical video) | Different platform → use the target platform's safe area (P2) |
| `scene.duration_dist` / `narrative_role_ratio` | Segment-duration proportions | Normalise to proportions, then apply to the target runtime | Different number of segments → merge by structural role |
| `caption.*` | Subtitle layout parameters | Transfer directly; the wording itself must be original | Different language → reset the character count per `03-subtitles` |
| `context.*` | Aspect ratio, hook, first frame | P1/P2 take priority | — |
| `constraints.*` | Hard filter | Re-run the G check after each plan is generated | A forbidden action is hit → scrap the whole plan and redo it |

---

## 4. Material adaptation: four kinds of shortfall

| Situation | Symptom | Handling | Must be recorded |
| --- | --- | --- | --- |
| Not enough shots | The target needs 30 cut points; the material supports 12 | Keep the shape of the density curve and lower density overall; create visual variation with shot-size changes and reframing, not with meaningless repeated cuts | Coverage rate, segments abandoned |
| No B-roll | Jump cuts in the talking-head sections cannot be hidden | Patch at the jump cuts first; cover the rest with graphics, subtitle animation or eased stills | Which segments are left with exposed jump cuts |
| No separate audio track | J/L-cuts and ducking are impossible | Disable the related rules; **never substitute the reference's audio track** (P0) | Reason for the downgrade |
| No scenes of the same type | The reference has 5 scenes; you have 1 interior | Transfer the structure "scene-change frequency" and replace location changes with camera position, shot size and lighting changes | The substitution and the expected deviation |

**Downgrade order**: lower absolute numbers first → then secondary dimensions → only then core dimensions. Core dimensions (A1 shot duration, B7 loudness, C8 aspect ratio and safe area) must never be abandoned entirely. Every downgrade states its `expected deviation` in the plan, for L4 review and L5 attribution.

---

## 5. Edit-plan output template

```markdown
# Edit plan · <project name> · based on <SFP-ID>

## 0. Basis and confirmation
- Reference video: <title/ID>; evaluation table: <path>; fingerprint: <path>
- S6 confirmation date / confirmed by / user corrections:
- Compliance precondition: G filter passed, __ protected items removed

## 1. Target specifications (P1/P2)
Aspect ratio / resolution / frame rate / runtime / delivery platform / loudness target / subtitle method

## 2. Structural timeline
| Segment | Time | Structural role | Shot count | Target shot duration | Cut density | Music/SFX events | Subtitle points |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Hook | 0-3s | | 3 | 1.0s | high | enters on the first frame | |
| ... | | | | | | | |

## 3. Mapping rules adopted
| # | Fingerprint field | Reference value | Value for this edit | Scaling/adaptation rationale | Priority | Expected deviation |
| --- | --- | --- | --- | --- | --- | --- |

## 4. Conflict rulings and downgrade log
| Conflicting item | Adopted | Overridden | Reason | Expected impact |
| --- | --- | --- | --- | --- |

## 5. Prohibited items
(list of protected items + item-by-item confirmation of forbidden_actions)

## 6. Execution checklist
- [ ] Rough cut follows the structural timeline
- [ ] Fine cut follows the cut-point type mix
- [ ] Sound mixed to the B targets
- [ ] Subtitles follow the caption parameters
- [ ] Grade follows the scene tendencies
- [ ] scripts/qc_scan.sh run after export
- [ ] L4 deviation comparison done (see §6)
```

---

## 6. L4 deviation tolerance (finished cut vs. fingerprint)

After export, measure the finished cut and compare it with the fingerprint. **Tolerance is tiered by confidence**, not guessed:

| Metric | Source of the reference value | High-confidence tolerance | Medium-confidence tolerance | Measurement command |
| --- | --- | --- | --- | --- |
| Median shot duration | `edit.shot_median_s` | ±15% | ±30% | `select scene` + adjacent-difference statistics |
| Cut density | `edit.cut_density_per_min` | ±20% | ±35% | as above, bucketed |
| Integrated loudness | `audio.integrated_lufs` | ±1 LU | ±2 LU | `ebur128=peak=true` Summary |
| True Peak | `audio.true_peak_dbtp` | must not exceed the ceiling | must not exceed the ceiling | as above |
| Aspect ratio / frame rate | `context.aspect`, `edit.fps` | exact match | exact match | `ffprobe` |
| Mean-luma tendency | `scene.yavg` | ±12% | ±25% | `signalstats` YAVG |
| Subtitle characters per line | `caption.chars_per_line` | ±2 characters | ±4 characters | manual proofreading |

Items outside tolerance are handled in three ways: ① a downgrade is on record → treat it as an expected deviation and pass it; ② no record but fixable → send it back for a recut; ③ repeatedly out of tolerance with no clear cause → log it as an **attribution TODO** and hand it to L5; never adjust the rules on your own initiative.

---

## 7. Common errors and troubleshooting

| Error | Consequence | Correction |
| --- | --- | --- |
| Applying the reference's timecodes directly to the new edit | Music and structure land in the wrong places | Align by event, convert by proportion |
| "Recreating the style" with the same track | Copyright risk (P0) | Transfer BPM and the energy curve only |
| Forcing the cut count when material is short | Meaning falls apart; it looks bad | Lower the density, keep the shape of the proportions |
| Treating the reference's measured loudness as the delivery target | Volume abnormalities after platform transcoding | P2 takes priority; follow the platform target |
| Downgrading without recording it | L5 cannot attribute anything; the deviation stays unexplained forever | Write every downgrade into §4 |
| Editing the fingerprint when the deviation exceeds tolerance | Hides execution problems; it is self-deception | Check execution first, then the mapping, and only then the fingerprint |
| Using low-confidence rules as hard constraints | The cut is boxed in by unreliable judgements | Tier rules as `active`/`candidate` |

---

## 8. Quick reference

- [ ] The plan header states the fingerprint ID and the S6 confirmation details
- [ ] Every mapping rule has "reference value / value for this edit / adaptation rationale"
- [ ] Conflicts resolved P0–P7 and traced
- [ ] Material shortfalls downgraded per the four cases, with expected deviations recorded
- [ ] G filter re-run; zero protected items remain
- [ ] Structural timeline, sound events and subtitle points all complete
- [ ] L4 deviation comparison done after export; out-of-tolerance items categorised and handled
- [ ] Deviation and downgrade records archived and available to L5

---

## References

- This volume, `01-overview-and-design-principles.md`, `02-reference-video-evaluation-framework.md` and `03-style-fingerprint-spec.md`
- `../04-genre-playbooks/` (structural templates and platform specifications)
- `../06-delivery-qc/01-technical-spec-checklist.md` (L4 measurement commands and tolerance conventions)
- `../01-editing-craft/02-transitions-rhythm-and-timing.md` (shot duration and cut-point selection)

Retrieved: 2026-11-10. The tolerance figures are starting suggestions; calibrate them for the project type and platform and mark them TO VERIFY.
