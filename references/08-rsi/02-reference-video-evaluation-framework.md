# Multi-Dimensional Reference-Video Evaluation Framework (core volume)

> Category: RSI self-improvement | Topic: the three core dimensions of editing craft / sound design / scene and image, plus the mandatory five-part explanation | Compiled: 2026-11-10 | Applies to: the S3–S5 stage after an instruction to cut in the style of a popular reference video

> ⚠️ This document is a reference for the creative workflow and **does not constitute legal advice**; for decisions involving clearance and compliance, see the 05-copyright volume and have counsel review.

> ⚠️ The hard requirement in this volume is one sentence long: **every evaluation item must carry an explanation**. A judgement without one is discarded outright — it may not enter the style fingerprint and may not serve as a basis for editing.

---

## 1. Why evaluation must be dimension-by-dimension, with an explanation each time

"Style" is not a single impression but a set of measurable, reproducible parameters. Saying only "this video has a fast pace, driving music and a warm grade" fails three ways: it cannot be reproduced (how fast is fast?), it cannot be reviewed (no standard for whether the cut matches), and it cannot be attributed (if it underperforms, you do not know what to change).

So an evaluation has to satisfy three conditions at once: **broken down by dimension** (not lumped together), **evidence-backed** (timecodes or reproducible numbers), and **explained** (what was observed, on what basis, why it was cut that way, and how I intend to use it).

---

## 2. The mandatory-explanation constraint (explain or discard)

Every evaluation item must fill all five parts; missing any one voids the whole item:

| Part | Requirement | Counterexample → good example |
| --- | --- | --- |
| ① **Observation** | A fact you can see or hear, with a timecode or a number; no evaluation mixed in | ✗ "the pacing is very fast" → ✓ "four hard cuts across 00:00–00:03, average shot 0.75 s" |
| ② **Evidence** | What produced it: an objective command / contact sheet / frame-by-frame listening / waveform; state the evidence grade | ✓ "`select scene` cut list + row 1 of the contact sheet, E1+E2" |
| ③ **Inference** | Explain the intent and effect of the technique; a hypothesis is acceptable but must be labelled as one | ✓ "stacked short shots raise information density in the opening so the viewer catches three selling points in the first 3 seconds" |
| ④ **Action item** | Land on an executable parameter for this edit; without an action item the entry has no value | ✓ "for this project, three 0.8–1.2 s shots in the opening 3 s, with the third cut 1–2 frames before the peak of the hand-raise" |
| ⑤ **Confidence** | High / medium / low + one sentence of justification; low confidence may not be used as a hard constraint | ✓ "high: the cut points were extracted objectively as E1, and the pattern occurs 3 times in the video" |

**Complete example (dimension A)**

> **A3 Basis of cut points**
> ① Observation: a hard cut at 00:07.12, from a medium shot to a product close-up; the cut lands on the third frame after the hand-raise begins; 22 of the 31 cut points in the video fall on an action or a dialogue break.
> ② Evidence: the cut list from `reference_probe.sh` (E1) + frame-by-frame comparison of 00:07.08/00:07.12 (E2).
> ③ Inference: invisible editing of the "action-to-action" kind, using momentum to carry the seam while shifting the information focus from the person to the product; aligning to breaks keeps the dense cutting from reading as messy.
> ④ Action item: for this project, every product-reveal shot cuts 1–2 frames before the peak of the action; all other cut points align to dialogue or breath breaks rather than landing on random beats.
> ⑤ Confidence: high (E1 is reproducible; the pattern repeats 22/31 times).

**A discarded counterexample**

> ✗ "This video is edited very smoothly, the transitions are natural, it feels very cinematic — worth learning from."
> No observed numbers, no evidence, no action item, no confidence; "smooth / cinematic" are evaluations, not facts → **discard the whole entry; it does not enter the fingerprint**.

---

## 3. Evidence grades and the intensity scale

| Grade | Meaning | Usable as a hard constraint |
| --- | --- | --- |
| **E1 objectively reproducible** | ffprobe/ffmpeg numbers, cut lists, loudness, colour statistics — anyone re-running it gets the same result | Yes |
| **E2 identifiable fact** | Timecoded human observation (what is on screen, the dialogue, how a sound effect is heard) that a third party can check | Yes (needs corroboration in ≥2 places) |
| **E3 interpretive inference** | Inference about intent, audience or emotion | No; reference only, and it must be labelled as inference |
| **E4 guess / description only** | No video, only a text description or an impression | No; confidence is forced to "low" and the user must be told at S6 |

**The 0–4 intensity scale expresses how strong or dense a feature is, not how good it is** (so that subjective taste never becomes a score):

| Value | Meaning |
| --- | --- |
| 0 | Absent |
| 1 | Occasional (<10% of runtime or <2 occurrences) |
| 2 | Present but not dominant (10–30%) |
| 3 | Evident and sustained (30–60%) |
| 4 | Dominant (>60%) or a whole-video structural device |

Every evaluation records `intensity` + `confidence` + `evidence grade`, and the three are independent. An item with intensity 4 but low confidence cannot be a hard constraint.

---

## 4. The seven dimensions at a glance

| Code | Dimension | Status | Main method | Output field prefix |
| --- | --- | --- | --- | --- |
| **A** | **Editing craft** | ★ core | Objective cut list + frame-by-frame observation | `edit.*` |
| **B** | **Sound effects and sound design** | ★ core | Loudness measurement + timecoded listening | `audio.*` |
| **C** | **Scene and image** | ★ core | Contact sheets + colour statistics + scene inventory | `scene.*` |
| D | Subtitles and on-screen text | Extended | OCR / manual proofreading | `caption.*` |
| E | Narrative structure and emotion curve | Extended | Segment timeline + inference | `narrative.*` |
| F | Platform and audience context | Extended | Specifications + publishing environment | `context.*` |
| G | Compliance and replicability boundary | **Mandatory** | The 05 volume + the idea/expression dichotomy | `constraint.*` |

A/B/C must be evaluated sub-item by sub-item; D/E/F must each yield at least 2 explained judgements; G is not a descriptive dimension but a **filter applied to every action item in A–F** (see §8).

---

## 5. Dimension A · Editing craft (★)

| Sub-item | What to observe | Measurement | Focus of the explanation (③ must answer this) | Fingerprint field |
| --- | --- | --- | --- | --- |
| A1 Shot-duration distribution | Median, mean, p90, shortest/longest; differences between segments | E1 cut list → adjacent differences in `awk`; shot duration tends to follow a long-tail distribution in the literature, so **use the median, not the mean, as the rhythm representative** | Why this duration? Its relation to information density and emotion | `edit.shot_median_s`, `edit.shot_p90_s` |
| A2 Cut-density curve | cuts/min per 10 s; opening vs. middle vs. ending | E1 cut list, bucketed | What the density change serves (hook / build-up / climax) | `edit.cut_density_per_min`, `edit.density_curve` |
| A3 Basis of cut points | Share of action peaks / eyelines / dialogue breaks / beats / information turns | E1 cut list + E2 frame-by-frame; tally the proportions | Why this kind of cut point, invisible or emphatic | `edit.cut_anchor_distribution` |
| A4 Transition types and durations | Mix and frame counts of hard cut / dissolve / mask / whip pan / match transition | E2 frame comparison across each transition; a dissolve can be counted by its double-exposure frames | Whether a transition connects, separates or argues | `edit.transition_mix`, `edit.dissolve_frames` |
| A5 Shot-size sequence and assembly | The WS→MS→CU progression pattern; whether the 180°/30° rules hold; how axis crossings are handled | E2, label shot sizes on the contact sheet | How shot-size change steers attention | `edit.scale_progression` |
| A6 In-shot motion | Push/pull, pan/tilt, handheld, gimbal, amount of subject movement | E2 segment-by-segment observation; `signalstats`/motion estimation can assist | Whether motion adds to or complements the cutting rhythm | `edit.camera_motion` |
| A7 J-cut / L-cut | Count and frame offset of audio leading or trailing the picture | E2 waveform compared against the cut list (8–24 frames is a common starting range) | How a sound bridge softens the seam | `edit.jl_cut_frames` |
| A8 B-roll share | Proportion of runtime covered, placement, whether it hides jump cuts | E2 timeline annotation | Whether B-roll adds information or hides defects | `edit.broll_ratio` |
| A9 Beat alignment | Distribution of frame error between cut points and musical beats | E1 cut list + E2 waveform/beat annotation | Whether the whole video is on the beat or only the chorus | `edit.beat_align_frame_error` |
| A10 Frame rate, overcranking, speed ramps | 25/30/50/60 fps; slow-motion passages and their purpose | E1 ffprobe `r_frame_rate`; E2 to locate speed-ramped passages | Whether the speed change serves emphasis or transition | `edit.fps`, `edit.slowmo_segments` |

**Additional requirement for dimension A**: you must answer "if only one parameter could be changed, which one is the skeleton of this video's rhythm?" — that answer sets the priority for the mapping stage.

---

## 6. Dimension B · Sound effects and sound design (★)

| Sub-item | What to observe | Measurement | Focus of the explanation | Fingerprint field |
| --- | --- | --- | --- | --- |
| B1 Music structure and parameters | BPM, key/mood, sections (intro / verse / chorus), whether it loops | E2 listening + tapping the beat; E1 with a BPM tool as an aid | Why this energy curve was chosen | `audio.bpm`, `audio.mood` |
| B2 Music in/out points | Start and end times, fades, alignment of the chorus with the visual climax | E2 waveform + timecodes | How music carries structure rather than just bedding the picture | `audio.music_in_s`, `audio.drop_align_s` |
| B3 Voice type and share | Spoken to camera / dialogue / no voice; pace, timbre, emotion | E2 listening + transcript word count and duration | Whether the voice is the main information or a support | `audio.voice_type`, `audio.speech_ratio` |
| B4 SFX density and types | SFX count per 10 s; whoosh / impact / UI / ambience / Foley | E2 timecoded listening and counting | Whether SFX reinforce cut points or tell their own story | `audio.sfx_per_10s`, `audio.sfx_types` |
| B5 SFX-to-cut coupling | Whether a cut point carries an SFX, and in what proportion | E1 cut list × E2 SFX list, cross-referenced | Coupling determines where the "punch" comes from | `audio.sfx_cut_coupling` |
| B6 Level relationships and ducking | Relative levels of dialogue / music / SFX; how far music ducks under voice | E1 `ebur128` in segments + `volumedetect`; E2 listening | How intelligibility is protected | `audio.music_duck_db` |
| B7 Loudness and true peak | Integrated LUFS, LRA, True Peak | **E1** `ffmpeg -af ebur128=peak=true` (read the Summary block at the end) | The delivery platform sets the target; louder is not better | `audio.integrated_lufs`, `audio.true_peak_dbtp` |
| B8 Sound bridges and cross-scene audio | Dialogue or SFX continuing across a cut; the audio side of J/L-cuts | E2 waveform comparison | Whether it pairs with A7 | `audio.sound_bridge` |
| B9 Silence and negative space | Deliberate silent passages, their length and surrounding context | **E1** `silencedetect=noise=-40dB:d=0.5` + E2 confirmation | Whether the silence creates contrast or is a mistake | `audio.intentional_silence` |
| B10 Frequency range and space | Low-end weight, sibilance, stereo width, mono compatibility | E2 listening; E1 `highpass/lowpass + volumedetect` | How the target playback environment (phone / headphones) shapes the mix | `audio.playback_target` |

**Additional requirement for dimension B**: you must decide whether **the music drives the edit** or **the edit drives the music**. The test: do the cut points fall systematically on the beat (A9 frame error small and tightly clustered)? This determines whether the project locks the music first or the picture first.

---

## 7. Dimension C · Scene and image (★)

| Sub-item | What to observe | Measurement | Focus of the explanation | Fingerprint field |
| --- | --- | --- | --- | --- |
| C1 Scene inventory | Number / timecode / location / people / function of the scene | E2 contact sheets + one full viewing | What narrative task each scene carries | `scene.list` |
| C2 Scene-change frequency | Number of scenes and duration distribution; segment boundaries | E1 `scdet` / `select scene` as aids + E2 merging | The relationship between scene density and information capacity | `scene.count`, `scene.duration_dist` |
| C3 Composition preferences | Rule of thirds / centred / symmetrical, subject size, direction of negative space | E2, annotate frame by frame | Whether composition serves subtitles and the vertical-video UI | `scene.composition` |
| C4 Camera height and shot-size habits | Eye level / high / low, habitual shot sizes, over-the-shoulder | E2 observation | What viewing relationship the angle establishes | `scene.camera_height` |
| C5 Tone and light | High key / low key, warm vs. cool colour temperature, contrast, hard vs. soft light | E2 observation + E1 colour statistics | How the grade matches mood and category | `scene.lighting_key`, `scene.color_temp` |
| C6 Colour statistics | Mean luma, saturation, dominant hues, jumps between scenes | **E1** `signalstats` output such as `YAVG/SATAVG` | Whether the grade is globally uniform or contrasted by segment | `scene.yavg`, `scene.satavg` |
| C7 Motion and stability | Camera movement style, stabilisation, amount of in-frame movement | E2 observation | Whether it is consistent with A6 | `scene.motion_level` |
| C8 Aspect ratio and safe area | Ratio, letterboxing, subtitle/UI safe area, top and bottom occlusion on vertical video | E1 ffprobe + E2 visual check | Which part of the frame the platform UI will eat | `scene.aspect`, `scene.safe_area` |
| C9 Elements inside the frame | Kinetic type, props, brand exposure, relationships and blocking | E2 annotation | Which parts are borrowable structure and which are protected expression | `scene.on_screen_elements` |
| C10 Scene and narrative function | Share of runtime for setup / development / turn / payoff | E2 structural timeline (**E3 inference**, must be labelled) | How the structural proportions transfer to different material | `scene.narrative_role_ratio` |

**Additional requirement for dimension C**: you must list "which scene features depend on the specific content and cannot be transferred". For example, "a seaside sunset" is content and cannot be transferred; "change location every 8–12 s to keep it fresh" is structure and can be. This distinction is the first filter against copying expression.

---

## 8. The extended dimensions and the mandatory dimension G

- **D Subtitles and on-screen text**: characters per line and line count, dwell time, timing (does text arrive before the voice?), typeface and stroke, kinetic-type frequency, whether the text carries the joke or the information. Criteria in `../03-subtitles/`.
- **E Narrative structure and emotion curve**: segment timeline (hook / build-up / turn / climax / payoff), emotional intensity curve, order in which information is revealed. This dimension is mostly E3 inference and must be labelled as such.
- **F Platform and audience context**: aspect ratio, duration, first frame, the 3-second hook, cover image, target playback environment, platform loudness normalisation. Criteria in `../04-genre-playbooks/`.
- **G Compliance and replicability boundary (mandatory)**: tag every action item in A–F with one of two labels:
  - `transferable: parameter` — a parameter or a structure, which may enter the fingerprint and be transferred (e.g. "median shot length 1.8 s").
  - `protected: expression` — specific expression, which may not be transferred (e.g. the reference's dialogue, its unique kinetic-type graphics, its signature shot staging, its original music).
  - Basis: the idea/expression dichotomy; substantial similarity compares the selections, choices, arrangements and designs inside the expression. For a popular reference video the "access" element is almost certainly satisfied, so apply the strict reading throughout.
  - No item tagged `protected` may appear in an edit plan; if one is found there, go back to L1 and re-evaluate.

---

## 9. Evaluation order and deliverables

```
S2 objective probe (reference_probe.sh)
   → specs / cut list / shot-duration statistics / loudness / silence / colour statistics / contact sheets
S3 observation
   → two full viewings at 1.0× (one for picture, one for sound only) + frame-by-frame on key passages
S4 evaluation
   → fill the A/B/C table sub-item by sub-item (five-part explanation each), ≥2 entries each for D/E/F, tag G item by item
S5 synthesis
   → ① reference-video-evaluation.md (complete)
      ② style-fingerprint YAML (transferable items only)
      ③ one-page conclusion: the 3 most critical features + the 3 non-transferable items + an overall confidence judgement
S6 user confirmation gate
   → no editing until confirmed
```

**How to write deliverable ③**: lead with "what I observed / how I intend to apply it to your footage / which points I am not sure about", and then ask the user to confirm. Do not lead with a finished cut.

---

## 10. Common errors and troubleshooting

| Error | Consequence | Correction |
| --- | --- | --- |
| Describing shot duration with the mean | Under a long-tail distribution the mean misleads | Use median + p90 |
| Treating every high `scdet` score as a cut | Fast whip pans and flashes produce false positives | Cross-check against `select scene` and frame-by-frame human review |
| "The music goes hard" as a dimension-B conclusion | No action item | Break it into BPM, entry point, chorus alignment, loudness |
| Writing "seaside sunset" into the fingerprint | Copies content instead of style | Run the G filter; keep only structural parameters |
| Treating every silent passage as a defect | It may be deliberate negative space | `silencedetect` must always be followed by human confirmation |
| Using low-confidence items as hard constraints | Every later deviation is attributed wrongly | Low confidence → mark as a hypothesis and keep it out of the fingerprint's mandatory fields |
| Evaluation items that state conclusions without evidence | Cannot be checked, cannot feed self-improvement | Five-part explanation; missing one part voids the item |
| Judging the whole video from contact sheets alone | Misses sound and rhythm detail | Contact sheets serve dimension C only; A and B require watching and listening to the whole video |

---

## 11. Quick reference

- [ ] A1–A10 each carry a five-part explanation and the `edit.*` fields can be filled
- [ ] B1–B10 each carry a five-part explanation, with loudness figures taken from the `ebur128` Summary
- [ ] C1–C10 each carry a five-part explanation, and the specific non-transferable content is listed
- [ ] D/E/F each ≥2 entries; inferences under E are labelled E3
- [ ] **G has tagged every action item `transferable` / `protected`**
- [ ] Intensity, confidence and evidence grade all present and mutually independent
- [ ] The 3 most critical features + the 3 non-transferable items are written up as the one-page conclusion
- [ ] S6 user confirmation obtained

---

## References

- Aalto University, "Film Mood: Assessment, Analysis, and Computational Modeling" (feature tables for luminance / saturation / shot duration / motion; the Weibull long tail and the recommendation to use medians): https://aaltodoc.aalto.fi/bitstreams/687de83f-bfce-47d5-a882-0ab3c2b4bd86/download
- IAFOR, "Toward Automating the Classification of Films' Narrative Structures" (shot boundary detection, duration patterns and pacing): https://papers.iafor.org/wp-content/uploads/papers/mediasia2024/MediAsia2024_85782.pdf
- AAAI, "Multi-Modal Analysis of Movies for Rhythm Extraction" (visual and auditory rhythm as two modalities): https://cdn.aaai.org/ocs/ws/ws1277/8862-38046-1-PB.pdf
- IEEE, "AI-Based Multimodal Framework for Shot-Level Analysis" (PySceneDetect + representative frames + human cross-checking, multimodal rhythm maps): https://xplorestaging.ieee.org/document/11335504/figures
- FFmpeg Filters Documentation (scdet / select / showinfo / signalstats / silencedetect / ebur128 / metadata): https://ffmpeg.org/ffmpeg-filters.html
- National Copyright Administration of China (国家版权局), "How Media Should Protect Copyright in the 5G Era" (《5G时代媒体该如何保护版权》) (the idea/expression dichotomy): https://www.ncac.gov.cn/xxfb/yjdt/201909/t20190923_49648.html
- Procuratorate Daily (检察日报), "Copycat Short Videos Grab Traffic: How Are Original Creators' Rights Protected" (《仿拍短视频抢流量 原创者权益如何保障》) (access + substantial similarity; compare expression, not theme or idea): http://newspaper.jcrb.com/2023/20230911//20230911_004/news-zgjcb-10331-20230911-m-004-300.pdf
- This knowledge base, `../01-editing-craft/`, `../02-audio-and-voice/`, `../03-subtitles/`, `../04-genre-playbooks/`, `../05-copyright/`

Retrieved: 2026-11-10. The objective probing commands were tested on the local ffmpeg 8.1.2. The thresholds (scene 0.25, silence −40 dB and so on) are starting suggestions: calibrate them against the material and mark them TO VERIFY.
