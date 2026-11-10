# Material Description Card (MDC) Specification · `mdc-v1`

> Category: Material memory | Topic: A structured material description produced by a single video-model call; field dictionary and evidence constraints | Compiled: 2026-11-10 | Applies to: Any owned or licensed video material that must be understood, retrieved, and reused across topics

> ⚠️ This volume is a reference for creative and engineering workflows and **does not constitute legal advice**. Licence, likeness, location, and provenance information in a card must be reviewed by a human; for commercial projects, have legal review it. See `../05-copyright/`.

---

## 1. Design goals: understand once, reuse forever

The same stretch of "seaside sunset B-roll" may be adopted by four topics at once: "autumn nostalgia", "climate science", "tourism promotion", and "brand end card". If the video is resubmitted to the model every time, that is four times the cost, four times the latency, and possibly four mutually contradictory descriptions. The MDC breaks this down into:

| Principle | Meaning | Cost of violating it |
| --- | --- | --- |
| **Write it all at once** | One model request covers content / location / style / usability / timecode events | The model is requested again for every topic, and the savings fall to zero |
| **Topic-neutral** | The card states only *what the material is*, never *how this topic should use it* | When the topic changes, the description turns into noise and can even mislead shot selection |
| **Facts and inferences kept apart** | Every field carries an evidence grade; inferences must state their basis | The model writes "looks like Sanya" as fact, and every downstream step inherits the error |
| **Verifiable identity** | Content hash plus technical specs; any change in bytes invalidates the card automatically | A new version of the material is still cut against the old description, producing the wrong content |
| **Correctable without overwriting** | A correction produces `v+1`; the old version and the reason are kept permanently | After an error you cannot trace which analysis introduced the bias |

A card is a **description**, not an **evaluation**: deep style evaluation (rhythm skeleton, cut-point rationale, sound-design intent) belongs to `../08-rsi/02`. This card answers only "what is in this material, and how can it be used".

---

## 2. Evidence grades (identical to Volume 08)

| Grade | Definition | Typical sources in this volume | Usable as a delivery basis |
| --- | --- | --- | --- |
| **E1 Objectively reproducible** | Re-running the command yields the same values | SHA-256, ffprobe specs, cut points / loudness / YAVG / SATAVG from `reference_probe.sh` | Yes |
| **E2 Pointable fact** | A third party can check it given a timecode | A red street sign at 00:03, a voice saying "this way" at 00:12, OCR of on-screen text; shooting logs, releases, and EXIF also qualify (mark them "documented") | Yes (key items need ≥2 corroborations) |
| **E3 Interpretive inference** | A reasonable inference drawn from E1/E2 | "Possibly dusk backlight", "overall cool cast", "looks like a handheld follow shot", "might work as an opening B-roll" | **No** — reference only, with the basis and confidence stated |
| **E4 Guess / description only** | No visual evidence, or unverifiable | "I heard it was shot in Qingdao", "the client said it was probably last year" | **No** — must be flagged low-confidence and must not enter the delivery ledger |

**Special rules for location and identity**: `where.place_name` may only be E2 (an identifiable landmark or text in frame, or a shooting-record document) or left empty. Inferring a city name from "there is sea + there are coconut palms" is forbidden. You may record it as `E3` in `environment_semantics` (e.g. "subtropical seaside feel"), but that is not a place name. This rule maps directly onto the accuracy requirements for the material ledger in `../06-delivery-qc/02`.

---

## 3. `mdc-v1` field dictionary

### 3.1 Identity layer `identity` (all E1)

| Field | Type | Description |
| --- | --- | --- |
| `material_id` | str | `MID-<first 12 lowercase hex chars of sha256>`, content-addressed, independent of path |
| `content_hash` | str | `sha256:<64hex>`; `hash_mode: sampled \| full` |
| `hash_mode` | enum | `sampled` (6 MB sampling, default) / `full` (whole file, for projects with a high consistency risk) |
| `size_bytes` / `duration_s` | int / float | Participates in hashing and in invalidation decisions |
| `container` `vcodec` `resolution` `fps` `pix_fmt` `acodec` `sample_rate` `channels` | str/num | Taken from ffprobe |
| `aliases` | list[str] | File names and in-project codes; **for retrieval only, never as identity** |
| `source_path_hint` | str | Path hint; the cache **never stores the video itself** |
| `first_registered` / `last_verified` | ISO date | Registration time and time of the most recent `verify` |

Sub-segments use a separate `segment_id = sha256(content_hash + "|" + start + "|" + end)[:12]`, carry `parent_mid`, inherit the parent card's description, and rewrite only the differences for that segment. A trimmed or transcoded file is **new material** and must be `register`ed again.

### 3.2 Content and narrative `content` (what it shows)

| Field | Content requirement | Evidence |
| --- | --- | --- |
| `summary` | ≤80 characters, a complete sentence, no evaluative adjectives | E2 |
| `subjects` | List of people / objects / scene subjects; for people, record only identifiable features, never an identity guess | E2 |
| `actions` | Key actions and state changes | E2 |
| `timeline` | `[{tc:"00:00:03.5", event:"…", evidence:"E2"}]`, sorted by timecode; **at least 3 anchors**, plus one every 15–30 s for long material | E2 |
| `spoken` | `has_speech` / `language` / `key_lines` / `transcript_ref` (path to the ASR text) | E2 |
| `onscreen_text` | Verbatim on-screen text (signage, subtitles, UI, watermarks) plus timecode | E2 |
| `affordances` | **Topic-neutral** usage tags: `B-roll / facial expression / product close-up / action sequence / ambient atmosphere / data screen / sync sound` | E3, basis required |
| `notable_absences` | Things explicitly *not* present (no speech, no subtitles, no brand exposure); extremely valuable when searching | E2 |

### 3.3 Shooting location and scene `where` (where it was shot)

| Field | Content requirement | Evidence |
| --- | --- | --- |
| `setting_type` | `indoor / outdoor / studio / nature / screen_capture / virtual / unknown` | E2 |
| `place_name` | Administrative region or landmark name; **must be `null` without E2 support** | E2 documented |
| `place_basis` | Basis type: `in-frame text / identifiable landmark / EXIF GPS / shooting log / written client statement` | E2 |
| `landmarks` | Identifiable objects (bridges, signage, mountain silhouettes) with timecode | E2 |
| `environment` | `time_of_day / weather / season / light_direction / light_quality / background / props` | E2 or E3 (state which) |
| `camera` | `position / angle / height / movement / stability` | E2 |
| `geo_hint` | Coordinates or administrative region only when documented; otherwise `null` | E2 |
| `inference_note` | All E3 inferences are collected here, each with "basis + confidence + falsification condition" | E3 |

### 3.4 Style `style` (what it looks like)

| Field | Content requirement | Evidence |
| --- | --- | --- |
| `genre` | Material genre: `documentary / narrative / commercial / screen recording / surveillance / animation / user-generated` | E3 |
| `visual` | `shot_sizes / composition / movement / stability / color_palette / contrast / saturation / white_balance / grain / era_feel` | E2 observation + E3 generalisation |
| `measured` | **E1 objective values**: `shot_median_s / cuts_per_min / integrated_lufs / true_peak_dbtp / yavg / satavg` — from `scripts/reference_probe.sh` and `scripts/qc_scan.sh` | E1 |
| `audio` | `music / ambience / sfx / voice / noise_floor / has_music_bed` | E2 |
| `mood` | At most 3 mood words, each paired with one visual or audio basis | E3 |
| `rhythm` | Description of the internal rhythm (shot length, speed of movement, whether there is breathing room) | E3 |
| `style_notes` | **Style inferences must use the five-part form**; see §4 | E3 |
| `similarity_caveat` | "Looks like style X" may only be an analogy; never stated as fact or as provenance | E3 |

### 3.5 Usability and compliance `usability` (whether it can be used)

| Field | Description |
| --- | --- |
| `provenance` | `origin: self_shot / stock / client / archive / ugc / unknown`; `acquired_from`; `license_ref` (path to the supporting document, with no sensitive data embedded) |
| `rights_status` | `cleared / pending / restricted / blocked / unknown`; **`unknown` and `blocked` must never enter a timeline** |
| `rights_expiry` | Licence expiry date; on expiry mark `blocked` and append a log entry, **never delete the card** |
| `releases` | Likeness consent / guardian consent for minors / location permit / trademark and brand exposure / music licence, each `yes/no/na/unknown` |
| `quality_issues` | Black frames, silence, shake, soft focus, overexposure, fluffed lines, watermarks, A/V sync drift, each with timecode |
| `edit_notes` | `best_ranges` / `avoid_ranges` / `handles_frames` / `continuity_risks` (axis, colour temperature, or time-of-day clashes with adjacent material) |
| `qc_ref` | Points to the `qc_scan.sh` output directory and the row number in the review sheet |
| `privacy_flags` | Faces, licence plates, house numbers, ID documents, personal information on screens → flag for de-identification (see `../05-copyright/04`) |

### 3.6 Metadata and constraints `meta` / `constraints`

`meta`: `model` (model name and version), `prompt_ref` (which prompt version was used), `analyzed_at`, `analyst`, `card_version` (starting at 1), `status: active / superseded / blocked / unverified`, `supersedes`, `corrections[]` (each correction records `time / field / old value / new value / basis / sign-off`).

`constraints`: `no_expression_copy: true` (the description must not reproduce protected expression; long dialogue is reduced to key points and positions), `theme_neutrality: true` (no topic or project names may appear), `no_geo_guess: true`, `no_identity_guess: true`.

---

## 4. Mandatory form for style notes (carried over from Volume 08)

Every entry in `style.style_notes` must use the five-part form; if any part is missing, the whole entry is void:

| Part | Requirement |
| --- | --- |
| ① Observation | Specific, with a timecode or a reproducible value |
| ② Basis | Evidence grade + source (which row of the frame contact sheet / which field of the probe log) |
| ③ Inference | The style judgement derived from the observation, explicitly marked "this is an inference" |
| ④ Action item | What it means for the edit (shot selection, grade direction, pacing) |
| ⑤ Confidence | High / medium / low + one sentence of justification |

> **Worked example**: `S1 Light and colour`｜① From 00:04 to 00:11 the sky fills about two-thirds of the frame, the subject's edge carries a rim light, and YAVG falls from 118 to 76 (backlit, darkening)｜② E1 `signalstats` output + E2 frame contact sheet, row 2｜③ Inferred as warm–cool contrast from dusk backlight, natural light rather than a designed setup｜④ When used as an opening B-roll, do not stack a warm LUT on top, or the colour temperature will break against the interior shots that follow｜⑤ Medium: a single piece of material, with no view of the whole film's colour strategy.

**Rejected counter-examples**: "the image has real texture, the grade is premium", "good for an emotional piece" — no basis, no confidence, and "good for an emotional piece" is a topic judgement that belongs in the L2 topic adaptation layer, not in the MDC.

---

## 5. The eight validation rules (`material_cache.py validate`)

| # | Rule | On failure |
| --- | --- | --- |
| V1 | `mdc_version == "mdc-v1"` and `material_id` is well-formed | Registration rejected |
| V2 | All four required sections `content / where / style / usability` present, and `meta` exists | Registration rejected |
| V3 | `identity.content_hash` matches the actual file hash | Registration rejected; re-run `fingerprint` |
| V4 | `content.summary` ≤80 characters and non-empty; `timeline` has ≥3 anchors with increasing timecodes | Registration rejected |
| V5 | A non-null `where.place_name` requires a non-empty `place_basis` | Registration rejected (blocks unsupported place names) |
| V6 | Every `style.style_notes` entry contains the five keys `observation / basis / inference / action / confidence` | That entry is void and the whole card is marked `unverified` |
| V7 | When `rights_status` is `unknown / blocked`, `constraints` must contain `no_use_until_cleared: true` | Marked `blocked`; the editing pipeline is halted |
| V8 | `constraints.theme_neutrality == true` and none of the four field groups contains a topic word such as `theme`, `topic`, or a project code | Warning; human confirmation required |

V8 is a coarse keyword filter: it misses cases and it raises false positives. **It is a hint only, not a substitute for a human read-through.**

---

## 6. Filling workflow

1. Run `fingerprint` to obtain identity and ffprobe specs → fill `identity` automatically (E1, no model involved).
2. Probe locally and objectively: `reference_probe.sh` yields cut points, shot durations, loudness, YAVG/SATAVG, and frame contact sheets → fill `style.measured` (E1).
3. Send **one** video-understanding request using `templates/model-analysis-prompt.md`, asking for structured output → check it item by item, then split the model output across `content / where / style / usability`.
4. Grade every entry; add five-part notes to all E3 inferences; use `null` wherever location or identity lacks support.
5. Fill rights information from the supporting documents, **never from model guesses**; review `privacy_flags` by hand.
6. `validate` → `register` → from then on, every topic simply reads the card.

---

## 7. Common errors and troubleshooting

| Error | Correct approach |
| --- | --- |
| The card says "suits an autumn nostalgia topic" | Put that in the L2 topic adaptation layer; the MDC records only `affordances: [B-roll, ambient atmosphere]` |
| The model says "looks like Sanya" and it is copied into `place_name` | `place_name: null`; record "subtropical seaside feel" in `inference_note` as E3 |
| The material was re-exported but the old card is still in use | The content hash changes → `lookup` returns `STALE`; register again and keep the old card as `superseded` |
| Long stretches of dialogue are copied into the description | `key_lines` holds key points plus timecodes only; `transcript_ref` points to the transcript file |
| The card is deleted when the licence expires | Mark `blocked` and append a log entry; keep the history traceable |
| Rhythm is described with a mean | Use `shot_median_s` (the mean is distorted under a long-tail distribution), matching Volume 08 |
| Each topic has the model watch the material again | A hit means read-only; if something is genuinely missing, try frame extraction / ASR / ffprobe first |

---

## 8. Quick reference

- [ ] `identity` is entirely E1; hashes match the file
- [ ] `content` has a summary, subjects, ≥3 timecode anchors, speech, and on-screen text
- [ ] `where` has a setting type and environment; the place name is `null` without documentation
- [ ] `style` has E1 measurements plus five-part style notes, and mood words have bases
- [ ] `usability` has an explicit rights status, privacy items reviewed, and `quality_issues` with timecodes
- [ ] `meta` records the model version, prompt version, analysis date, and sign-off
- [ ] `constraints` has all four switches
- [ ] Passes V1–V8, and the whole card is topic-neutral and reusable across topics

---

## References

- EBUCore (EBU Tech 3293; layered descriptive, technical, and rights metadata): https://msi.dublincore.org/standards/ebucore
- PBCore 2.1 (separation of assets from instantiations; rights and provenance fields): https://msi.dublincore.org/standards/pbcore
- MPEG-7 and audiovisual archive metadata (temporal structure, scenes, colour and motion descriptors): https://www.nedcc.org/fundamentals-of-av-preservation-textbook/chapter-4-introduction/chapter-4-section-5
- Google, "Video understanding" (1 FPS sampling may miss fast action; timestamp formats; recommendations for timecode anchors): https://ai.google.dev/gemini-api/docs/video-understanding
- This volume's `README.md`, `02`, `03`; `../08-rsi/02-reference-video-evaluation-framework.md` (E1–E4 evidence grades and the five-part note)
- `../06-delivery-qc/02-content-and-compliance-review.md` (material ledger), `../05-copyright/04-likeness-fonts-stock-and-personality-rights.md`

Retrieved: 2026-11-10. The `mdc-v1` fields, the V1–V8 validation rules, and the "one anchor every 15–30 s" guideline are all **conventions defined by this knowledge base**, not industry standards; calibrate the thresholds against the complexity of your material.
