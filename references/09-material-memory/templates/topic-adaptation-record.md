# Topic Adaptation Record Template (L2 layer)

> Category: Material memory | Topic: Selection, narrative role, rationale and outcome feedback for one material by one topic | Compiled: 2026-11-10 | Applies to: Fill in whenever a registered clip is used in a topic; the machine-readable part is written by `material_cache.py use` into `cache/themes/<MID>.csv`

> ⚠️ This volume is a creative and engineering process reference and **does not constitute legal advice**; `rights_scope_check` must be verified per topic against the rights documentation, and commercial projects should be reviewed by legal.

---

## Template (copy one block per use)

```markdown
## Adaptation record: <THEME-ID> / <MID>

| Field | Content |
| --- | --- |
| theme_id | T-YYYY-<short-name> |
| theme_title | |
| adapted_at | 2026-11-10T15:20:00 |
| material_id / summary | MID-xxxxxxxxxxxx / (copy the 80-character summary from the MDC, do not rewrite it) |
| clip_ranges | 00:00:03-00:00:08 |
| narrative_role | opening hook / setup / argument footage / emotional peak / transition / close / B-roll / evidence material |
| rationale ① observation | |
| rationale ② basis | (must cite an MDC field name or a timecode, e.g. `content.timeline[1]`, `style.measured`) |
| rationale ③ inference | (begin with "This is an inference:") |
| rationale ④ action item | (concrete parameters: duration, speed, grade, subtitles, audio) |
| rationale ⑤ confidence | high / medium / low + one line of reasoning |
| edit_directives | |
| audio_handling | original audio / muted / score / replaced by voice-over |
| rights_scope_check | in_scope / needs_recheck / out_of_scope |
| conflicts_with | (usually "none"; a different usage does not count as a conflict) |
| outcome | (fill in after publishing: adopted / rejected + reason + data summary) |
| feedback_ref | ../../08-rsi/case-library/<CASE-ID>/self-improvement-record.md |
```

---

## Worked example (fictional, format demonstration)

| Field | Content |
| --- | --- |
| theme_id | `T-2026-秋日怀旧` |
| theme_title | "The Summer After That" — 30 s short film |
| adapted_at | 2026-11-10T15:10:00 |
| material_id / summary | `MID-9f3c1a7b02de` / Fixed-camera empty plate, seaside dusk, slow pan right, surf on rocks, no people |
| clip_ranges | `00:00:03-00:00:08` |
| narrative_role | opening hook (emotional setup) |
| ① observation | The MDC records 00:03–00:08 as an empty plate with no people, no subtitles and no branded objects; `style.measured` records `cuts_per_min=0.0` and continuous original surf audio |
| ② basis | `content.notable_absences`, `content.timeline[1]`, `style.measured.shot_median_s` (E1/E2, source MDC) |
| ③ inference | This is an inference: the segment carries no information load and works as an undisturbed emotional entry point |
| ④ action item | Cut in 5 s at 80% speed, 1 s of black before it, no subtitle overlay, original surf audio starting at −6 dB with a 2 s fade-in |
| ⑤ confidence | High: the picture facts are verifiable; two earlier uses of the same kind in this theme passed review |
| edit_directives | No warm LUT (MDC `style_notes[0]` already flags the colour-temperature break risk); no scaling on the first frame |
| audio_handling | Original audio (surf), 2 s fade-in, score enters at 00:05 |
| rights_scope_check | `in_scope` (own shoot; the rights documentation covers commercial and non-commercial use) |
| conflicts_with | None (another theme uses 00:12–00:19; the segments and the edits are independent) |
| outcome | To be filled in |
| feedback_ref | To be filled in |

---

## Hard rules

1. **Never write back to the MDC**: no judgement in this record may modify `cards/<MID>.yaml`. If an MDC fact turns out to be wrong, go through `verify` + manual correction to produce `card_version+1`.
2. **The basis must be pointable**: `rationale ②` cites an MDC field or a timecode; "feels good" or "fits nicely" is void.
3. **Check rights per topic**: when `rights_scope_check != in_scope` the theme may not enter the timeline; go through `../../05-copyright/` for review.
4. **Append only**: record a rejection as `outcome: rejected + reason` and never delete the record; counter-examples are regression-set assets (see `../../08-rsi/06`).
5. **Segments must be legal**: `clip_ranges` must fall inside `identity.duration_s` and must not overlap `edit_notes.avoid_ranges`; any overlap needs a justification in `rationale ④`.
6. **No migration across versions**: when a change of bytes produces a new MID, the old adaptation records are kept but not applied automatically; each one needs manual confirmation.

---

## Correspondence with the commands

```bash
PY="scripts/material_cache.py"
V="D:/footage/2026-09/sunset-beach-raw.mp4"

# Machine-readable record (writes themes/<MID>.csv + usage.csv + audit.log)
python "$PY" use "$V" --theme "T-2026-秋日怀旧" --clip "00:00:03-00:00:08" --note "opening empty plate"
python "$PY" use "$V" --theme "T-2026-气候科普" --clip "00:00:12-00:00:19" --note "cloud layer illustration"

# See which themes have used this material
python "$PY" themes "$V"
```

This Markdown template is for cases that need a detailed `rationale` and `edit_directives`; for simple reuse the command alone is enough, and the two are linked by `theme_id + clip_ranges`.

---

## Quick checklist

- [ ] `theme_id`, `clip_ranges` and `narrative_role` all present
- [ ] The five-part `rationale` is complete, and ② cites an MDC field or timecode
- [ ] `rights_scope_check` verified per topic
- [ ] The segment does not conflict with `avoid_ranges`
- [ ] Nothing written back to the MDC; factual errors go through the correction process
- [ ] `outcome` and `feedback_ref` filled in after publishing

---

## References

- This volume: `../03-multi-topic-adaptation-and-references.md` (L1/L2 layering, field dictionary, citation governance, conflict classification)
- This volume: `../01-material-description-card-spec.md` (MDC fields and evidence grades), `../02-cache-reuse-protocol-and-token-savings.md` (accounting)
- `../../08-rsi/06-case-library-and-version-governance.md` (append-only, counter-examples and the regression set)
- `../../05-copyright/03-music-sfx-and-recording-licensing.md` (purpose/territory/term), `../../06-delivery-qc/02-content-and-compliance-review.md` (Table C)
- PBCore 2.1 (asset and instantiation layering): https://msi.dublincore.org/standards/pbcore

Retrieved: 2026-11-10. The fields and enumerations in this template are conventions defined by this knowledge base rather than industry standards; the example data is fictional.
