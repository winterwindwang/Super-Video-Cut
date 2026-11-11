# 08 · The RSI Self-Improvement Volume

> Category: RSI self-improvement | Topic: the evaluate–map–review–self-improve loop used when cutting in the style of a popular reference video | Compiled: 2026-11-10 | Applies to: the trigger phrases "reference / imitate / benchmark against / in the style of"

**In one sentence**: when you say "cut my footage in the style of this hit video", I **evaluate it dimension by dimension with an explanation for each item, and only start cutting once you confirm**; the predictions and the real outcome of every task flow back, so the evaluation and mapping rules get gradually more accurate within the guardrails.

---

## The P0 trigger protocol (pin it to the wall)

```
reference video received
  S1 Compliance precondition: analyse only, reuse none of its expression
  S2 Run scripts/reference_probe.sh → objective metrics
  S3 Two full viewings (one for picture, one for sound only) + frame-by-frame on key passages
  S4 Fill in templates/reference-video-evaluation.md
       A editing craft / B sound / C scene, sub-item by sub-item
       Each item needs: observation → evidence → inference → action item → confidence
  S5 Produce the style-fingerprint YAML + a one-page conclusion
       the 3 most critical features + the 3 non-transferable items + an overall confidence judgement
  S6 ★ handed to you for confirmation ★  ← no finished cut before it is confirmed
  S7 Map to an edit plan → edit → 06 volume review
  S8 Collect real feedback → candidate revision (no immediate effect) → nine-step gate
```

**Four things that do not bend**: the mandatory-explanation constraint (a judgement without an explanation is discarded), the S6 user confirmation gate, the idea/expression boundary (transfer parameters, never expression), and single cases producing candidates only.

---

## Contents

| File | What it covers |
| --- | --- |
| `01-overview-and-design-principles.md` | What RSI means here, the six-layer architecture, the nine-step cycle, the seven hard guardrails, the compliance precondition |
| **`02-reference-video-evaluation-framework.md`** | **★ core: editing craft / sound / scene, sub-item by sub-item + the mandatory five-part explanation + evidence grades + the intensity scale** |
| `03-style-fingerprint-spec.md` | The `sfp-v1` YAML schema, field dictionary, derived rules, 8 validation rules |
| `04-fingerprint-to-edit-plan-mapping.md` | Conflict resolution P0–P7, field-by-field mapping, material downgrades, L4 deviation tolerance |
| `05-feedback-loop-and-self-improvement.md` | Error attribution, candidate generation, the weight-update formula, the nine-step gate, drift prevention, the kill switch |
| `06-case-library-and-version-governance.md` | Directory structure, naming, rule versions, audit log, rollback procedure |
| `07-keyframe-baseline.md` | Per-shot keyframe anchors, what may and may not be compared, the blocking/warning tiers of the structural diff |
| `templates/reference-video-evaluation.md` | **A 30+ item evaluation sheet you can fill in directly** |
| `templates/style-fingerprint.yaml` | A copyable empty fingerprint |
| `templates/self-improvement-record.md` | The feedback record for a single task |
| `scripts/reference_probe.sh` | Objective metric probing (cut points / shot durations / loudness / silence / colour / contact sheets), tested |
| `scripts/keyframe_diff.py` | Keyframe baseline (`extract`) and structural diff against it (`compare`), exit 2 on a blocking difference, tested |
| `case-library/README.md` | Case index and configuration notes |

---

## The three dimensions at a glance

| Dimension | 10 sub-items | Core question |
| --- | --- | --- |
| **A Editing craft** | Shot-duration distribution, cut-density curve, basis of cut points, transition types and frame counts, shot-size sequence, in-shot motion, J/L-cut, B-roll share, beat frame error, frame rate and overcranking | What is the skeleton of the rhythm? Why does the cut sit here? |
| **B Sound effects and sound design** | BPM and music structure, music in/out points, voice type and share, SFX density and types, SFX-to-cut coupling, levels and ducking, loudness and true peak, sound bridges, silence and negative space, frequency range and playback environment | Does the music drive the edit, or the edit drive the music? |
| **C Scene and image** | Scene inventory, scene-change frequency, composition, camera height and shot-size habits, light and colour temperature, colour statistics, motion and stability, aspect ratio and safe area, on-screen elements, narrative function of scenes | Which parts are structure (transferable) and which are content (not transferable)? |

There are also D subtitles and on-screen text, E narrative and emotion, F platform context, and **G the compliance and replicability boundary (mandatory; tag every action item)**.

---

## What one evaluation looks like (example)

> **A3 Basis of cut points**
> ① Observation: hard cut at 00:07.12, medium shot → product close-up; the cut lands on the third frame after the hand-raise begins; 22 of the 31 cut points fall on action/dialogue breaks.
> ② Evidence: the probe script's cut list (E1) + frame-by-frame comparison of 00:07.08/07.12 (E2).
> ③ Inference: invisible action-to-action editing, carrying the seam with momentum and shifting attention from the person to the product.
> ④ Action item: for this project, product-reveal shots cut 1–2 frames before the peak of the action; the rest align to dialogue/breath breaks.
> ⑤ Confidence: high (E1 is reproducible; the pattern repeats 22/31 times).
> G tag: `transferable: parameter`

A rejected counterexample: "this video is edited very smoothly, it feels cinematic" — no observation, no evidence, no action item, no confidence.

---

## Also: check the cache before using your own footage

If the task also involves "use my footage", **before evaluating the reference video, run `lookup` per the P0 protocol in `../09-material-memory/README.md`**: on a hit, read the material description card directly (what it shows / where it was shot / what style it is) and skip the video model; only on a miss do a full analysis and register the result. That way, reusing the same footage across several topics costs one model call in total.

## First use

1. Put the reference video on your machine (or tell me how to obtain it).
2. I run the objective probe and complete the evaluation sheet first, then hand you the **one-page conclusion** to confirm.
3. Only after you confirm or correct it do I start on the edit plan.
4. If publishing data is available after delivery, I log a self-improvement record (candidates only; rules are never changed unilaterally).

> ⚠️ This volume does not constitute legal advice. Style and formulas belong to the level of ideas and may be borrowed; specific shots, dialogue, music, kinetic type and other expression may not be copied. Have counsel review commercial projects; see `../05-copyright/`.

---

## References

- This volume, all documents `01`–`06`; `../05-copyright/`, `../06-delivery-qc/`, `../02-audio-and-voice/`
- National Copyright Administration of China (国家版权局), "How Media Should Protect Copyright in the 5G Era" (《5G时代媒体该如何保护版权》) (the idea/expression dichotomy): https://www.ncac.gov.cn/xxfb/yjdt/201909/t20190923_49648.html
- The original source URLs and methodological basis for each document are listed in its own "References" section at the end

Retrieved: 2026-11-10.
