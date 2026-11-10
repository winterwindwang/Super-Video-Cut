# Single Full Material Analysis · Model Prompt Template

> Category: Material memory | Topic: The complete prompt for the single video-understanding request issued on `MISS` | Compiled: 2026-11-10 | Applies to: Any video-understanding model or multimodal service; used together with `material-description-card.yaml`

> ⚠️ This volume is a creative and engineering process reference and **does not constitute legal advice**; all model output is treated as unverified material, and rights, location and identity conclusions must be reviewed by a human.

---

## Usage rules (read these five first)

1. **Use only when `lookup` returns `MISS` or `STALE`.** Never send this prompt on `HIT`.
2. **Send it once, and only once.** Replace `<LOCAL_E1_DATA>` and `<CLIP_ALIAS>` below and send the whole block in a single request, asking for all five dimensions at once; do not split it into separate questions per topic.
3. Attach the local objective data first (ffprobe specs, the cut/loudness/colour statistics from `reference_probe.sh`, the frame contact sheet) as context, so the model does not have to "guess" the specs again and hallucinates less.
4. Model output **is not a finished card**: a human verifies it line by line, assigns evidence grades, adds the five-part explanations and fills in the rights data, and only then does it go through `validate` → `register`.
5. Long material: static mode defaults to 1 FPS, which can miss detail during fast motion; you may lower the FPS or split the material into segments in the way the provider supports, but cross-check with separately sampled frames. All timestamps use `MM:SS` or `MM:SS.mmm`.

---

## Prompt body (ready to copy)

```
You are a video material cataloguer. Analyse the following video completely in a single pass and output YAML that can be pasted directly into a material description card.
This description will be reused many times across many different topics, so it must be theme-neutral, must separate fact from inference, and must be verifiable.

[Known objective data (measured by local tools; treat as E1 and do not estimate again)]
<LOCAL_E1_DATA>
# e.g. duration=180.0s, 1920x1080, 25fps, h264/aac 48kHz
# cuts: 0.00 / 12.40 / 31.08 / 58.20 ; median shot length = 18.4s
# integrated=-16.2 LUFS, TruePeak=-1.4 dBTP, YAVG=104, SATAVG=31
# attached: frame contact sheet (each row labelled with its timecode)

[Clip alias] <CLIP_ALIAS>

[Output requirements]
1. Output exactly one YAML code block. Use the four field groups content / where / style / usability,
   consistent with mdc-v1: content.{summary, subjects, actions, timeline[{tc,event,evidence}],
   spoken{has_speech,language,key_lines,transcript_ref}, onscreen_text, affordances,
   notable_absences}; where.{setting_type, place_name, place_basis, landmarks,
   environment{time_of_day,weather,season,light_direction,light_quality,background,props},
   camera{position,angle,height,movement,stability}, geo_hint, inference_note};
   style.{genre, visual{...}, measured{}, audio{...}, mood, rhythm,
   style_notes[{观察,依据,推断,动作项,置信度}], similarity_caveat};
   usability.{quality_issues, edit_notes{best_ranges,avoid_ranges,continuity_risks}}.
   Do not output identity / meta / constraints (those are filled in locally).
2. Attach evidence to every fact: E1 = carried over from the objective data above; E2 = clearly
   identifiable in picture or sound and accompanied by a timecode; E3 = an inference based on E1/E2
   (must state the basis and a falsification condition); E4 = unverifiable (avoid wherever possible).
3. content.timeline needs at least 3 timecode anchors; for material longer than 60 seconds add one
   anchor every 15-30 seconds, in increasing time order, covering the beginning, the middle and the end.
   Every onscreen_text and quality_issues entry carries a timecode.
4. summary must be ≤80 characters, with a complete subject-verb-object, and must not contain evaluative
   wording such as "beautiful", "premium" or "great texture".
5. [Hard constraint on place and identity] Fill where.place_name only when text or a landmark is
   identifiable on screen, or when a shooting record is known; otherwise it must be null and
   place_basis must read "none". Never infer a city or country from the sea, mountains, vegetation or
   architectural style alone. Such impressions may only go into where.inference_note, marked E3, with a
   stated falsification condition. Do not guess a person's identity, occupation, age or relationships;
   describe only what is identifiably visible and what they do.
6. [Hard constraint on theme neutrality] The output must not contain any specific theme name, project
   name or client name, nor usage conclusions such as "suitable for a XX topic", "good as an opening"
   or "good as an ending". content.affordances may contain only neutral tags: empty plate / facial
   expression / product close-up / action process / ambient atmosphere / data screen / sync sound.
7. style.style_notes needs at least 2 entries, each containing all five parts:
   observation (with a timecode or a value), basis (evidence grade + specific source), inference
   (begin it with "This is an inference:"), action item (what it means for the edit), confidence
   (high/medium/low + reason).
   mood takes at most 3 words, each followed by one line of visual or audio basis.
8. [Expression and privacy] key_lines records key points and timecodes only; never transcribe dialogue
   in full and never transcribe complete lyrics; never write real names, ID numbers, licence plates,
   house numbers or other personal information. If these appear in frame, note it only in
   usability.quality_issues, e.g. "00:00 frame appears to contain a licence plate, manual anonymisation required".
9. When unsure, always write unknown / null. Do not invent. Never emit filler such as "inferred from
   common cases".
10. End with a CHECK section: list the 3 fields you consider most in need of manual review, and why.
```

---

## Pre-send self-check

- [ ] `lookup` confirms `MISS` / `STALE`
- [ ] `<LOCAL_E1_DATA>` is populated with the ffprobe + `reference_probe.sh` results, and the frame contact sheet is attached
- [ ] The target service has an appropriate `media_resolution` / FPS / processing mode set (follow the official guidance for long video)
- [ ] The three hard constraints in the prompt — theme neutrality / no place-name guessing / five-part explanations — are unmodified
- [ ] The output is declared as YAML and its fields are aligned with `mdc-v1`

---

## Handling the output you receive

| Step | Action |
| --- | --- |
| 1 | Spot-check ≥3 timecode anchors against the original footage (models commonly summarise well but misplace exact moments) |
| 2 | Add basis, confidence and falsification condition to every `E3` inference; delete any that has no basis |
| 3 | Check whether `place_name` has E2 documentation; if not, set it to `null` |
| 4 | Overwrite `style.measured` with the local E1 data (the model should not be estimating these) |
| 5 | Fill the rights, likeness and privacy items under `usability` **entirely by hand from the documentation**; do not trust the model |
| 6 | Copy into `material-description-card.yaml` and fill in `identity` / `meta` / `constraints` |
| 7 | `python scripts/material_cache.py validate <card>` → only `register` once it passes |
| 8 | Record the actual token count from this run's `usage_metadata` via `register --tokens`, so `stats` can reconcile it |

---

## Common mistakes

| Mistake | Correct approach |
| --- | --- |
| Sending one request for the "autumn theme" and another for the "science-explainer theme" | Send once only; topic judgement belongs in the L2 adaptation layer |
| Asking the model in the prompt to "also judge what topic this suits" | Remove it; it pollutes the card and triggers repeated requests later |
| Registering the model output directly as a finished card | Manual verification + `validate` are mandatory |
| Asking the model to supply specs that ffprobe can measure | Provide the local E1 data up front: fewer tokens and more accurate |
| Output containing "looks like it is in Sanya (三亚)" | `place_name: null`, put the impression in `inference_note` marked E3 |

---

## References

- This volume: `../01-material-description-card-spec.md` (mdc-v1 fields, E1–E4, five-part explanations, V1–V8)
- This volume: `../02-cache-reuse-protocol-and-token-savings.md` (write it all at once, legitimate paths for supplementary requests, token accounting)
- Google, "Video understanding" (1 FPS sampling, `MM:SS` timestamp format, custom FPS and clipping in static mode only, model timestamps need verification): https://ai.google.dev/gemini-api/docs/video-understanding
- Google, "Context caching" (vendor-side optimisation for repeated questions about the same video): https://ai.google.dev/gemini-api/docs/caching
- `../../08-rsi/02-reference-video-evaluation-framework.md` (authoritative reading of E1–E4 and the five-part explanation)

Retrieved: 2026-11-10. This prompt is a template customised for this knowledge base and must be tuned to the capabilities and output format of the model in use; sampling rates, resolution parameters and billing models vary over time, so re-check the vendor's current documentation before use.
