# Multi-topic adaptation and reference governance

> Category: Material memory | Topic: Layering, references, conflicts, and revocation when several topics adopt the same material at once | Compiled: 2026-11-10 | Applies to: Material library reuse, serialised content, A/B cut variants, material shared across projects

> ⚠️ This volume is a reference for engineering and creative workflows and **does not constitute legal advice**. The licensed scope of the same material may differ by use, territory, and term; always go back to `../05-copyright/` and the licence documentation.

---

## 1. The problem: why topic adaptation needs a layer of its own

The user's core scenario is "**one piece of material can be adopted by many different topics at once**". Four topics using the same stretch of seaside sunset:

| Topic | Clip used | Narrative role | How it is cut |
| --- | --- | --- | --- |
| Autumn nostalgia | 00:03–00:08 | Emotional opening B-roll | 80% slow motion, a slight warm lift, 1 s of held silence |
| Climate science | 00:12–00:19 | Cloud-layer illustration (information shot) | Native speed, annotation arrows, voice-over |
| Tourism promotion | 00:00–00:05 | Destination establishing shot | Hard cut in, location strap overlaid |
| Brand end card | 00:20–00:24 | The resolution before the logo | 15% darker, music fades out |

All four share **exactly the same objective facts**: dusk, seaside, rocks present, no speech, a slow rightward pan, YAVG falling gradually. Write "good for an autumn opening" into the material card and the other three topics read noise; re-watch the video for each topic and the cache was wasted work. Hence:

- **L1 MDC**: one card per item of material, holding only topic-neutral facts and inferences, shared by every topic.
- **L2 topic adaptation**: one record per `(material_id, theme_id)` holding "how this topic uses it"; appended without limit, revocable, and mutually independent.

This mirrors the idea of "**separating the intellectual work from its instantiations**" found in audiovisual metadata standards such as PBCore and EBUCore: a piece of material is an asset, and its use within a topic is one instantiation of that asset.

---

## 2. L2 adaptation record fields

Stored in: `cache/themes/<MID>.csv` (machine-readable) plus `templates/topic-adaptation-record.md` (a single detailed record, human-readable).

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `theme_id` | str | ✓ | `T-YYYY-<short name>`, e.g. `T-2026-autumn-nostalgia` |
| `theme_title` | str | ✓ | Topic or finished-film title |
| `adapted_at` | ISO datetime | ✓ | Time the record was written |
| `clip_ranges` | list | ✓ | `MM:SS-MM:SS` ranges, possibly several; must fall within `identity.duration_s` |
| `narrative_role` | enum | ✓ | `opening hook / setup / argument shot / emotional peak / transition / resolution / B-roll / evidence material` |
| `rationale` | five-part | ✓ | Observation / basis / inference / action item / confidence; **the basis must cite an MDC field or timecode** |
| `edit_directives` | list | — | Concrete parameters for speed changes, cropping, grade direction, subtitle layout, and audio processing |
| `audio_handling` | str | — | Native sound / muted / score / voice-over; points to `../02-audio-and-voice/` |
| `rights_scope_check` | enum | ✓ | `in_scope / needs_recheck / out_of_scope`; see §4 |
| `conflicts_with` | list[theme_id] | — | Which topics conflict on which field (usually empty) |
| `outcome` | str | — | Filled in after release: adopted or dropped, plus a summary of completion or review feedback |
| `feedback_ref` | str | — | Points to `../08-rsi/case-library/<CASE-ID>/self-improvement-record.md` |

**Worked `rationale` example**:

> ① Observation: MDC `content.timeline` records 00:03–00:08 as "B-roll, no people, no subtitles, no branded objects", and `style.measured` records a long `shot_median_s` and a steady `integrated_lufs` for that stretch｜② Basis: MDC timecode anchors + frame contact sheet row 1 (E1/E2)｜③ Inference: well suited to carrying an emotional opening with no information load｜④ Action item: cut in for 5 s, slow to 80%, hold 1 s of black before it, no subtitles｜⑤ Confidence: high (the visual facts are checkable, and two earlier uses of the same kind in this topic drew good feedback).

A rejected counter-example: "this one has a good vibe, use it for the opening" — no basis, not reusable, not attributable.

---

## 3. Retrieval: finding material by tag once the cache hits

With an MDC in place, finding material no longer needs a model:

```bash
PY="scripts/material_cache.py"
# List the topics that have used a given item
python "$PY" themes "D:/footage/sunset-beach.mp4"
# Library-wide statistics (items / topics / hit rate / estimated savings)
python "$PY" stats
# Text search: find candidates by affordances and on-screen text (costs no tokens)
grep -rl "affordances" "$MDC_HOME/cards/" | xargs grep -l "ambient atmosphere"
grep -rl "onscreen_text" "$MDC_HOME/cards/" | xargs grep -l "NO PARKING"
```

Order of decisions when choosing a shot: **read the MDC's `affordances` / `timeline` / `edit_notes` first → then look at the topic's existing adaptation records → only then consider a new model request**. If none of the three settles it, prefer local frame extraction (`ffmpeg -ss … -frames:v 1`); only if that still falls short, take the "only legitimate path to a supplementary request" described in `02`.

`edit_notes.continuity_risks` is the field most often overlooked when reusing across topics: the same dusk-backlight material can sit next to a cool interior shot in topic A without a problem (a deliberate contrast), whereas in topic B it may need its axis and colour temperature checked against another dusk shot. Such a clash is a problem **inside a single finished film**; it affects neither the MDC nor other topics' adaptation records.

---

## 4. Reference governance

| Rule | Content |
| --- | --- |
| Reference count | The number of rows in `themes/<MID>.csv` is the number of topics that adopted the item; `stats` aggregates the top material |
| Idempotency | Repeating `use` for the same `(theme_id, clip_ranges)` does not double-count; only the timestamp updates |
| Append-only | Adaptation records are never deleted; a dropped use writes `outcome: dropped + reason`, preserving the trail of judgement |
| Revocation | When a licence is withdrawn, mark the MDC `blocked`; **every topic record that references it becomes invalid automatically but is not deleted**, and the finished film goes through the replacement procedure in `../06-delivery-qc/02` |
| Rights scope | `rights_scope_check` must be decided per topic: licences are usually limited by "use / territory / term / medium", and an item being `in_scope` for topic A does not mean it is `in_scope` for topic B |
| Version linkage | When material is replaced (new MID), adaptation records for the old MID do not migrate automatically; confirm each one by hand and re-register under the new MID |
| Concurrency | When several topics write the same `themes/<MID>.csv` at once, the tool serialises the writes with a lock, and no rows are lost |

**Three kinds of conflict; do not confuse them**:

1. **Factual conflict** (two topics describe the material's content inconsistently) → almost certainly someone edited the MDC or used a STALE card; go back to `verify` and trust the `E1` objective values and the original footage.
2. **Usage conflict** (the same clip is cut differently in two finished films) → **not a conflict**; the films are independent and each keeps its own treatment.
3. **Rights conflict** (the use exceeds the licensed scope) → block that topic and send it to legal/licensing review; this has nothing to do with the description.

---

## 5. Writing corrections back: change only the layer that needs changing

| Problem found | Layer to change | Re-run the model? |
| --- | --- | --- |
| "The opening selection for autumn nostalgia is wrong" | L2 record: `clip_ranges` / `outcome` | No |
| "There is actually faint speech here, but the card says no speech" | L1 MDC `content.spoken`, `card_version+1` + `corrections` | No — listen locally or run ASR |
| "The place name is wrong" | L1 MDC `where.place_name`, with E2 documentation mandatory | No |
| "The material was re-exported and the duration has changed" | New MID + new card; old card `superseded` | Yes (new material) |
| "The model's overall style judgement is consistently off" | **Do not edit the card** — edit the prompt or the evaluation rules, and enter the candidate process in `../08-rsi/05` | Not involved at the candidate stage |

**Hard guardrail**: the self-evolution engine **must not** rewrite L1 objective descriptions (`E1`/`E2` fields) automatically. It may only propose changes to prompt templates, field weights, or adaptation-layer rules, and those must pass through the nine-step gate in Volume 08 with a human sign-off. The reason is straightforward: let "the system believes it knows better" write itself back into the fact layer, and a single contamination spreads through the cache into every topic that follows.

---

## 6. Worked example: one complete multi-topic reuse

```
15:02  lookup seaside-sunset.mp4 (autumn nostalgia topic) → MISS
15:03  ffprobe + reference_probe.sh        → E1 specs and cut points (0 tokens)
15:05  one full model request (low resolution) → 18,000 est_tokens
15:08  fill the MDC → validate V1–V8 pass → register
15:10  use T-2026-autumn-nostalgia / 00:03-00:08 / opening B-roll  → read the card, 0 tokens
15:14  lookup (climate science topic)      → HIT, 0 tokens
       use / 00:12-00:19 / argument shot
15:20  lookup (tourism promotion topic)    → HIT, 0 tokens
       use / 00:00-00:05 / establishing shot
15:26  lookup (brand end card topic)       → HIT, 0 tokens
       use / 00:20-00:24 / resolution
16:00  stats → 1 MISS + 3 HIT / hit rate 75% / estimated saving 54,000 video input tokens
16:01  release feedback → write outcome per topic → aggregate into the Volume 08 self-evolution record (a candidate; no rule changes)
```

Four topics, one model request. The arithmetic: `no cache 4×18,000=72,000` versus `with cache 1×18,000=18,000`, a net saving of `54,000 = 3 HIT × 18,000`, consistent with the tool's `stats`; the general form is `1 − 1/N`. All of these figures are **estimates**; the real bill is whatever `usage_metadata` reports. If card creation is treated as a standalone step that is not tied to any topic, there is one extra `HIT` and the statistics skew slightly optimistic.

---

## 7. Common errors and troubleshooting

| Error | Correct approach |
| --- | --- |
| Writing "suits topic X" into the MDC | Write it into L2; the MDC stays topic-neutral (V8 will warn) |
| Creating a new card for every topic | One card per `content_hash`, shared by all topics |
| Checking the licence term once and never again | Run `rights_scope_check` for every topic and every release |
| Carrying old adaptation records over after the material is replaced | A new MID needs each record confirmed by hand and re-registered |
| Deleting dropped records outright | Write `outcome: dropped + reason`; counter-examples are assets for the regression set |
| Assuming a data conflict because two topics cut the clip differently | Different usage is not a conflict; each film keeps its own treatment |
| Letting the self-evolution engine fix the MDC automatically | Forbidden; it may only propose prompt/rule changes and go through the nine-step gate |

---

## 8. Quick reference

- [ ] Every adaptation record has a `theme_id`, a clip, a `narrative_role`, and a five-part `rationale`
- [ ] The `rationale` basis cites an MDC field or timecode, not an impression
- [ ] `rights_scope_check` is filled in per topic; anything other than `in_scope` blocks the use
- [ ] Reference counts and `outcome` have been filled in
- [ ] Dropped uses and revocations are appended, never deleted
- [ ] Factual conflicts go back to `verify`, and `corrections` are retained
- [ ] Old adaptations do not migrate automatically when material is replaced
- [ ] Errors in key conclusions have not been written back into L1 automatically

---

## References

- PBCore 2.1 (layering of intellectual work and instantiation; rights and provenance fields): https://msi.dublincore.org/standards/pbcore
- EBUCore / EBU Tech 3293 (layering of descriptive, technical, and rights metadata): https://msi.dublincore.org/standards/ebucore
- Dublin Core Metadata Standards Index (comparison of metadata standards): https://msi.dublincore.org/standards/ebucore
- This volume's `01` (fields and evidence grades), `02` (hits, invalidation, and accounting), `04` (working with RSI)
- `../08-rsi/05-feedback-loop-and-self-improvement.md` (the nine-step gate), `../08-rsi/06-case-library-and-version-governance.md` (append-only practice and counter-examples)
- `../06-delivery-qc/02-content-and-compliance-review.md` (material ledger), `../05-copyright/03-music-sfx-and-recording-licensing.md` (use / territory / term)

Retrieved: 2026-11-10. The `theme_id` naming scheme, the `narrative_role` enumeration, `rights_scope_check`, and all L2 fields are **conventions defined by this knowledge base**, not industry standards. Legal judgements about licensed scope rest on the contract and the current law; this document does not constitute legal advice.
