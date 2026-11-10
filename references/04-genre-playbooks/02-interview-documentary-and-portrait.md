# Interview, Documentary and Portrait Editing Playbook

> Category: Genre playbooks | Topic: Character interviews / documentary / long-form non-fiction / multi-cam talk shows | Compiled: 2026-11-10 | Applies to: Documentary editors, interview post-production, corporate portrait films, video-podcast teams

> **Numeric disclaimer**: Every resolution, frame rate, timecode, loudness target and delivery format in this document is "subject to the platform's latest official documentation / the broadcaster's technical spec sheet" and must be re-verified before delivery. Conflicting figures or rules of thumb are marked TO VERIFY.

---

## 1. Genre goals and evaluation metrics

**Goal**: Without distorting fact or meaning, shape a huge body of sync material into a clear, credible character narrative with an emotional arc. The biggest difference from short-form video: the first KPI is not retention but **accuracy and credibility**.

| Metric | Meaning | How to verify |
|---|---|---|
| Factual accuracy | Every claim traces back to a source timecode | Check the claim-to-evidence map line by line |
| Semantic fidelity | Meaning, tone, certainty, conditions and referents left intact | Compare the transcript against source timecodes; have the subject review |
| Evidence chain clarity | Separate observation, interview, archive, inference, reenactment and generated content | Source classification table plus disclosure where needed |
| Narrative clarity | A complete arc of question → complication → reflection | A stranger can retell the through-line after one viewing |
| Emotional resonance / completion rate | Character dimensionality; the share of full views on a long piece | Test-screening feedback / backend retention curve |
| Technical compliance | Loudness, frame rate, subtitles and color gamut on spec | Loudness report / QC sheet |

> Ethical floor: editing is "selecting and organizing information," not "manufacturing fact." PBS editorial standards require that "editing must never change the meaning of what a subject said."

---

## 2. Mainstream platform and delivery specs (subject to the platform's latest official documentation / broadcaster spec sheet)

| Scenario | Aspect ratio | Resolution | Frame rate | Duration | Audio / loudness |
|---|---|---|---|---|---|
| Broadcast documentary (EBU R128) | 16:9 | 1920×1080 / 3840×2160 | 25fps; 24fps for a cinematic look (TO VERIFY) | 30 / 45 / 60 min per episode | −23 LUFS ±1 LU, ≤ −1 dBTP, LRA ≤15 LU |
| US broadcast (ATSC A/85) | 16:9 | 1920×1080 | 29.97 / 59.94fps | Per station | −24 LKFS, −2 dBTP |
| Online long-form (Bilibili (哔哩哔哩) / Tencent Video, etc.) | 16:9 | ≥1920×1080 | 25/30fps | 8–60 min | About −14 to −16 LUFS (TO VERIFY) |
| Interview shorts / video podcast | 16:9 + 9:16 clips | 1920×1080 / 1080×1920 | 25/30fps | Main version 8–15 min; clips 1–3 min | 48kHz / 24bit, separate recorder |
| Master archive | 16:9 | Native resolution | Native frame rate | — | ProRes 422 HQ / DNxHR HQ |

**On-set prerequisites**: Lock every camera and recorder to the same frame rate, jam-synced timecode and white balance; preserve source timecode; record 30–60 seconds of room tone on every setup. Mixed frame rates (24fps A-cam plus 60fps slow motion) must be conformed to the timeline frame rate first. Otherwise the cut looks aligned while individual angles still drift.

---

## 3. Structure template (timeline tables)

**Template A: 45-minute character documentary** (minute level)

| Timeline | Segment | Task | Material |
|---|---|---|---|
| 0:00–3:00 | Cold open | Build anticipation with a strong question or a killer line | Sync sound + close-ups + title cards on black |
| 3:00–10:00 | Introduction | Establish the person, the environment, the daily life | Observational shots + B-roll + first interview block |
| 10:00–20:00 | Background and conflict | Lay out the backstory; pose the core question | Archive + interviews from multiple sides + graphics |
| 20:00–32:00 | Escalation | Multiple perspectives, counter-evidence | Cross-cutting + verité coverage |
| 32:00–40:00 | Climax / turn | Irreversible change | Long takes to protect performance + music enters |
| 40:00–45:00 | Reflection and close | Aftertaste, title cards | Inserts + end credits |

> Short-film timing rules of thumb (TO VERIFY): the first 30 seconds to 1 minute sets expectation; move into the next act within 5 minutes at most; turn hard around the 8–10 minute mark; demonstrate the change in the final 3–5 minutes. Short films often stop dead at a low point or an awakening. Aftertaste matters more than telling the whole story.

**Template B: 8-minute character interview short**

| Timeline | Segment | Beat |
|---|---|---|
| 0:00–0:20 | Cold-open line | Open on the most powerful sentence; no setup |
| 0:20–1:30 | Establish the person | Alternate interview A-roll with life B-roll |
| 1:30–5:30 | Three thematic blocks | About 80 seconds each; open each with a claim |
| 5:30–7:00 | Emotional high point | Keep the full performance and its pauses; cut less |
| 7:00–8:00 | Close | One reflection + a name/date/place card |

**Single A-roll / B-roll alternation beat** (ready to apply):

| Duration | Picture | Sound |
|---|---|---|
| 0–6s | Interview medium shot | Sync sound; the conclusion sentence |
| 6–12s | B-roll: hands / environment / objects | Sync sound continues (L-cut) |
| 12–18s | Back to the interview, different close-up angle | Sync sound |
| 18–24s | B-roll: wide shot + process action | Sync sound + room tone bed |

**Sync and scene-card template** (ASCII straight quotes inside the code block):

```
sync_method: "timecode"   # or "waveform" / "clapper" / "clip marker"
audio_offset_frames: 0    # correction range -100 to +100 frames
scene_card: "scene|goal|obstacle|reveal|emotional_temperature|duration|dependencies"
```

---

## 4. Key techniques and specific parameters

**1. Multi-cam sync (Adobe Premiere's official method)**

| Method | When it applies | Accuracy |
|---|---|---|
| Timecode | All cameras and recorders jam-synced | Fastest and most accurate; the professional default |
| Linear / Sound / Aux Timecode | LTC embedded in the audio track, separate recorder | Choose per source |
| Audio (waveform) | All cameras share a common sound (clapper, ambience, lav bleed) | Most common on small and mid-size shoots; less accurate than timecode on long takes |
| Clapper | A clean slate at the head of every take | Visual + audio spike |
| Clip marker / in and out points | Already marked / small projects | Requires prior markers or manual alignment |

- `Offset Audio by` applies frame-level correction of −100 to +100 frames to an individual audio track (an Adobe official parameter).
- Order of operations: **sync first → select the story (transcript-first) → cut between angles last**. Skipping story selection and going straight to angle-cutting is the number-one cause of a timeline spiraling out of control.
- Angle-cutting principles: cut to the speaker, to a wide shot for emphasis, to a close-up for reaction; never cross the 180-degree line; for a long answer, stay on a single angle and let the performance breathe.

**2. Audio parameters**

| Item | Parameter |
|---|---|
| Reference track | Pick one clean external, boom or lav track and keep it running for the whole film; **cut picture, not sound**, to avoid level and timbre jumps |
| Edit-point fades | 2–10 frame crossfades across segments and deletions; as short as 1 frame when removing a single filler word |
| Room tone | Record room tone for every setup; bed the gaps so the edits become inaudible |
| Removing flubs | Cut "um," "uh," false starts and repeated phrases; cover the visual jump cut with B-roll |
| Loudness | Broadcast −23 LUFS ±1 LU / −1 dBTP; online about −14 to −16 LUFS (TO VERIFY) |
| Music | Licensed or royalty-free libraries only; step back under dialogue |

**3. B-roll and shot scale**: The three-shot set is wide to establish the place → medium to explain the process → close-up to emphasize an object or gesture. Leave 2–3 seconds of handles on either side of each action; 3–8 seconds per clip; lock exposure, lock white balance, keep the composition stable. B-roll must serve the meaning of the line, not simply look good. **It must never imply that a subject did something they never did or went somewhere they never went**, and an unverified text close-up must not be presented as fact. For interviews, use soft light and off-center framing; keep color temperature and lighting ratio consistent within a scene, and avoid jumping across too many shot sizes between angles.

---

## 5. Audio and subtitle specifics

1. **Sync sound is the spine**: external mic (lav or boom) + separate recorder + headphone monitoring; shut off fans and air conditioning; layer sync sound, ambience and Foley, and stitch the edits together with room tone.
2. **The transcript is the edit bay**: keep the transcript and source timecodes so revisions never lose the original context. Textualize first to circle the sentences worth keeping, then return to picture.
3. **Subtitles**: speaker IDs, sync-sound captions, time/place title cards; for online distribution, provide closed captions and a full transcript (see category 04).
4. **Three passes**: watch once muted to check the visual storytelling, listen once with eyes closed to check whether the edits are audible, then watch normally.

---

## 6. Common pitfalls and ethical red lines

| Pitfall | Anti-pattern | Consequence | Fix |
|---|---|---|---|
| Answer-question mismatch | Attaching an answer about question A to question B | Serious distortion; potentially defamatory | Summarize the question in narration or keep the original question |
| Composite sentence (Frankenbite) | Splicing together "a sentence never spoken" | Violates PBS standards; subject, verb and object must never be swapped | Trim for concision only; never build a new sentence |
| Seamless cross-time splice | Covering two separate statements with B-roll so they read as one quote | Misleads the audience | Signal the jump with a flash frame, a wipe or an angle change |
| Time confusion | Compressing several interviews into one, or inserting a fake pause after a question | Unfair and distorted | Keep time references; do not add dramatic pauses |
| Quote mining | Removing qualifiers, conditions or counter-evidence | Changes certainty and tone | Preserve qualifiers and verifiable sources on contested points |
| B-roll fabrication | Using footage from elsewhere to imply the subject was present | Implies a causal link the material does not support | Label as "illustrative / archival / reenactment" |
| Cutting angles before selecting the story | Syncing, then immediately multi-cam cutting | Timeline out of control | Use transcript-first to lock the lines that stay |

**Ethics checklist**: Build an evidence chain that separates "direct observation / interview statement / archive and its source / creator inference / expert explanation / graphic simulation / reenactment / generated content." Use a claim-to-evidence map to record each claim's source, timecode, limitations and counter-evidence. Reenactments, simulations and generated content must be disclosed in a comprehensible way on screen, in subtitles, in narration, in end credits or in metadata. Never fabricate key evidence, lines a real person never spoke, events that did not happen, or fake sync sound.

---

## 7. Pre-delivery checklist

- [ ] Source timecodes, frame rates and white balance unified; mixed frame rates conformed
- [ ] Multi-cams synced and verified segment by segment (re-check any segment synced by waveform)
- [ ] One clean reference track locked for the whole film; picture cut without cutting sound
- [ ] All flubs removed; 2–10 frame fades at edit points (1 frame for single words), room tone bedded underneath
- [ ] Transcript and source timecodes complete; trims left tone, certainty, conditions and referents intact
- [ ] No answer-question mismatch, composite sentences, seamless cross-time disguise or time confusion
- [ ] B-roll matches the meaning of the line, implies no action that did not happen, and has adequate handles
- [ ] Shot scale, lighting, color temperature and the 180-degree line stay continuous within a scene
- [ ] Evidence chain and claim-to-evidence map complete; reenactments and generated content disclosed
- [ ] Music, archive and images have clearance on file; speaker IDs, time and place cards, closed captions and transcript all present
- [ ] Loudness on spec: broadcast −23 LUFS ±1 LU / −1 dBTP; online per the platform target (re-verified against the platform's latest official documentation)
- [ ] Subject, director and compliance review passed and archived

---

## References

- Adobe, "Create a multi-camera source sequence" (sync methods, timecode options, Offset Audio): https://helpx.adobe.com/cn/premiere/desktop/edit-projects/set-up-multi-camera-sequences-for-editing/create-a-multi-camera-source-sequence.html
- Adobe, English edition (Linear/Sound/Aux Timecode, All Cameras): https://helpx.adobe.com/content/help/ca/en/premiere/desktop/edit-projects/set-up-multi-camera-sequences-for-editing/create-a-multi-camera-source-sequence.chromeless.html
- PBS, "Handle Interview Edits with Care" (no change of meaning, no Frankenstein sentences): https://www.pbs.org/standards/blogs/standards-memos/handling-quotations/
- Documentary dialogue editing (2–10 frame fades, B-roll cover, ethics): https://audioscene.org/article/best-practices-for-editing-dialogue-in-documentary-films
- B-roll terminology and checklist (shot scale, handles, no fabrication): https://www.thebarcoe.studio/glossary/b-roll
- Multi-cam interview workflow (waveform sync, story first, 180-degree line): https://scriptcut.io/blog/how-to-edit-multicam-interviews
- The three sync methods and the need to verify sync: https://scriptcut.io/blog/what-is-a-multicam-edit
- Form playbook (evidence chain, claim-to-evidence map, disclosure): https://github.com/ZimaBlueAI/skills/blob/main/produce-cinematic-video/references/form-playbooks.md
- Documentary sound and B-roll (soft light, room tone): https://skymedia.com.sg/zh/how-to-shoot-a-documentary-singapore
- Broadcast and streaming loudness standards: https://wefixsound.com/blog/broadcast-audio-quality-standards
- Short-film structure and timing: https://taiwancinema.bamid.gov.tw/Articles/ArticlesContent?ContentUrl=94508

Retrieved: 2026-11-10
