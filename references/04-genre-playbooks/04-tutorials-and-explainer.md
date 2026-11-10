# Tutorial, Course and Knowledge Video Editing Playbook

> Category: Genre playbooks | Topic: Screen-recorded tutorials / online courses / software demos / coding and math instruction | Compiled: 2026-11-10 | Applies to: Instructional designers, technical instructors, educational video post-production, corporate training and LMS delivery teams

> **Numeric disclaimer**: Recording resolution, frame rate, bitrate, font pixel size, type size, duration, subtitle line count and dwell time, and loudness are all "subject to the platform's latest official documentation / the current WCAG standard," and must be tested on the target device before delivery. Rules of thumb and research statistics are marked TO VERIFY.

---

## 1. Genre goals and evaluation metrics

**Goal**: Get learners to "understand it, keep up, produce the result, and be able to look it up again." Unlike short-form video, which fights for attention, knowledge content must **reduce cognitive load and hand pacing control back to the learner**. Play, pause, rewind, speed and jump matter more than any hook.

| Metric | Meaning | How to verify |
|---|---|---|
| Learning objective achieved | Can learners perform the target task afterwards | In-class quiz / hands-on task accuracy |
| Segment completion rate | Completion of each 5–7 minute segment | Backend segment curve |
| Replay / pause hot zones | Which moments get rewound repeatedly | Locate the under-explained passages and add cues |
| Information retention | Performance on a delayed quiz | End-of-segment questions + summary |
| Accessibility compliance | WCAG 2.1/2.2 AA | Audit subtitles, transcript, audio description and keyboard operation item by item |

> Instructional design principles: **short segments + signaling on demand + clear audio**. Remove every image, music cue and animation with no instructional value. Exact commands, code, paths and setting values must be given as accessible text so learners can scan, copy and compare without replaying.

---

## 2. Platform specs and recording parameters (subject to the platform's latest official documentation)

| Item | Recommended value | Rationale |
|---|---|---|
| Recording resolution | 3840×2160 (4K) | Leaves image-quality headroom for a 2× zoom; recording straight to 1920×1080 leaves none |
| Delivery resolution | 1920×1080 (16:9); vertical clips 1080×1920 (9:16) | One master feeds multiple platforms |
| Frame rate (static code / terminal) | 30fps | Text updates don't need 60fps, and the files are smaller |
| Frame rate (UI interaction / scrolling / animation) | 60fps | Smoother scrolling and cursor movement |
| IDE font size | ≥18–22px (readable at 1080p), zoom 150%–175% | Too small is the number-one flaw in instructional video |
| Editor settings | Dark theme, line numbers ON, minimap OFF, sidebars collapsed | Reduces visual noise |
| Audio | 44.1–48kHz, external mic + system audio **on separate tracks** | Lets you denoise and mix them independently |
| Export codec | H.264 + MP4 (H.265 optional), 1080p 4–8 Mbps | Compatibility first |
| Segment length | 30–90 seconds per focused step | Easier to segment and search |
| Chapter / segment | 5–7 minutes; ≤6 minutes recommended | Guo et al. 2014, across 6.9 million viewing sessions: median engagement peaks at about 6 minutes (measures watch time, not learning outcomes; TO VERIFY) |
| Background music | −18 to −24 dB, ducked under narration | Music must not compete for attention |

**Where it lands**: Bilibili (哔哩哔哩) / YouTube / corporate LMS are mostly 16:9 1920×1080; Udemy, Coursera and internal platforms follow their own upload specs (subject to the platform's latest official documentation); derived knowledge-point clips can be reframed to 9:16 1080×1920 (safe area in category 01).

---

## 3. Structure template (timeline tables)

**Template A: 6-minute single lesson**

| Timeline | Segment | Task | Presentation |
|---|---|---|---|
| 0:00–0:15 | Goal first | Write the goal with a verb: "By the end you'll have configured X" | Title card + voice-over; no opening animation |
| 0:15–0:45 | Name the parts + signaling | Name each part first, then give visual cues | Wide shot at 1.0×, arrows or labels pointing at the target |
| 0:45–4:30 | 3–5 steps | 30–90 seconds per step, one sub-goal per step | Explain → zoom demo → back to wide to recap |
| 4:30–5:30 | Full run-through / common errors | Run it end to end and call out the easy mistakes | 1.0×, enlarge and highlight the errors |
| 5:30–6:00 | Summary + one question | Set a stopping point; preview the next lesson | Key-point title card + copyable command list |

**Template B: 60–90 second knowledge-point clip**

| Timeline | Segment | Key point |
|---|---|---|
| 0:00–0:05 | Problem / result preview | Start with "what you'll be able to do" |
| 0:05–0:15 | Name the parts | Give the terminology and where it lives |
| 0:15–1:10 | Operation demo | Includes 1–2 zooms; hold key frames 3–7 seconds |
| 1:10–1:30 | Recap + copyable text | Hand over the command or formula text card |

**Chapter and clip planning table** (ready to apply):

| Chapter | Knowledge point | Duration | Clip timecodes | Supporting text |
|---|---|---|---|---|
| 1 | Environment setup | 5:30 | 00:00 / 02:10 | Dependency list, version numbers |
| 2 | Core concepts | 6:00 | 00:00 / 03:20 | Glossary, diagrams |
| 3 | Step-by-step practice | 6:00 | 00:00 / 01:45 / 04:10 | Full code / commands |
| 4 | Troubleshooting and verification | 5:00 | 00:00 / 02:30 | Error reference table |

> Segmentation principle: split at **meaningful sub-goal boundaries**, using chapter markers or standalone clips; never cut mechanically at fixed intervals. Put a question or a stopping point at every chapter boundary.

**Screen-recording parameter template** (ASCII straight quotes inside the code block):

```
resolution_record: "3840x2160"
resolution_deliver: "1920x1080"
fps_static_code: 30
fps_ui_scroll: 60
ide_font_px: 20
cursor_size: "1.5-2x"
zoom_code_focus: "1.5-2.0x"
zoom_transition_sec: 0.8
dead_air_remove_over_sec: 1.5
bgm_db: "-18 to -24"
```

---

## 4. Key techniques and specific parameters

| Technique | Parameter | How to do it |
|---|---|---|
| Cursor highlight | 1.5–2×; yellow or white ring about 50px radius; click ripple; smoothing 0.9 | Rest on the target 0.5 s before clicking; **never circle the cursor**; hide it while talking through code |
| Local zoom | Code 1.5–2.0×; UI elements 2.0–2.5×; terminal 1.5×; back to wide 1.0× | 0.8 s ease-in-out (0.6 s for terminal and for the return to wide); **announce it in the voice-over first** ("let's look at this function"), then zoom |
| Pan | Follow the active area, ease in and out | Hold for at least 3 s before the next pan; never jump instantly |
| Speed changes | Navigation 1.5×, repeated operations 2×, key moments 1.0× | Remove pauses >1.5 s |
| Split screen / picture-in-picture | Instructor head as a PiP (circle or rounded rectangle with a stroke); screen capture and camera on two tracks | On camera when explaining concepts; shrink or move out of the subject area during demos |
| Code presentation | Monospace font, syntax highlighting, line numbers, line-by-line highlight, enlarge key lines | One focus at a time; **exact commands, paths and setting values must be given as copyable text** |
| Formulas / charts | Large-type standalone cards, item-by-item highlight, synced to the voice-over | Hold ≥3–7 s; never let them flash past |
| Information density | One focus per screen; cue with "look at the panel in the top right" or "watch the cursor here" | Attach labels to the thing being explained; delete decorative animation and transitions |
| Subtitle dwell | 3–7 s per screen, ≤3 lines, ≤32 characters per line | Bottom center, never covering critical UI |

> Signaling substantially reduces the attention split between subtitles and picture: saying out loud "look here" works better than adding a highlight alone. Keep the shot order fixed — wide for context → zoom to focus → wide to confirm — or learners lose their sense of space.

---

## 5. Audio and subtitles / accessibility

1. **Audio layering**: Record narration on an external mic and system audio on its own track; overall loudness about −14 to −16 LUFS at −1 dBTP (TO VERIFY, subject to the platform's latest official documentation); BGM at −18 to −24 dB with ducking under the voice; consistent level throughout, with no overlapping voices and no music swamping speech.
2. **Subtitles (WCAG 2.1 AA)**: Provide **closed captions (switchable)** rather than burned-in hard subtitles; cover all speech and important non-speech sound (annotated in square brackets as `[music]`, `[laughter]`); identify speakers; keep them in sync with the audio; ≤32 characters per line, ≤3 lines, 3–7 s dwell; contrast ≥4.5:1, white text on a solid or semi-transparent black background, sans-serif ≥16pt (Arial/Helvetica/Verdana); 99% accuracy, no rewriting and no free translation. **Never rely on auto-generated captions alone**; proper nouns must be proofread by hand.
3. **Key WCAG 2.2 criteria** (subject to the latest WCAG standard):

| Criterion | Level | Requirement |
|---|---|---|
| 1.2.1 Audio-only / video-only | A | Provide an equivalent alternative or an audio track |
| 1.2.2 Captions (prerecorded) | A | All prerecorded video with audio needs synchronized captions |
| 1.2.3 Audio description or media alternative | A | Important visual information has an equivalent description |
| 1.2.5 Audio description | AA | A transcript does not satisfy the AA requirement |
| 2.2.2 Pause, stop, hide | A | Auto-moving content lasting more than 5 seconds must be pausable |

4. **Full transcript**: Include dialogue, speaker names, important sounds and picture description, placed near the player. A transcript is good for scanning and search, but **it does not replace synchronized captions**, nor the audio description required by 1.2.5.
5. **Learner control**: Play, pause, seek, rewind and volume all available, plus playback speed where supported; autoplaying content must be pausable; player controls must be keyboard-operable with readable names and states and a sensible focus order.
6. **Never rely on a single channel**: Don't convey necessary distinctions by color, sound or motion alone; respect `prefers-reduced-motion`; avoid harmful flashing.

---

## 6. Common pitfalls and anti-patterns

| Pitfall | Anti-pattern | Consequence | Fix |
|---|---|---|---|
| Recording at delivery resolution | Recording at 1080p and then doing a 2× zoom | Turns to mush when enlarged | Record 4K, deliver 1080p |
| Type too small | 14px IDE with all sidebars open | Unreadable on a phone | ≥18–22px, collapse irrelevant panels |
| Hard subtitles only / trusting auto captions | Burned-in captions plus unproofread ASR | Inaccessible, proper nouns wrong | Closed captions + 99% human proofreading |
| Cursor flying around | Mouse circling all over the screen | Divides attention | Move with purpose; rest 0.5 s before clicking |
| Zoom with no warning / instant jump | Sudden enlargement with no transition | Loss of spatial sense | Announce in the voice-over + 0.8 s transition |
| Commands only on screen | A string of commands flashing past | Impossible to copy; constant rewinding | A matching copyable text card |
| One 20-minute monologue, no segmentation | A single long file with no chapters | High load, unsearchable | 5–7 minute segments + chapter markers |
| Decorative motion and BGM over the narration | Transitions everywhere; music louder than the voice | Distraction, information lost | Remove decoration; anchor on the voice at −18 to −24 dB + ducking |
| Key frames held too briefly | A formula or error message on screen <2 s | Unreadable | Hold 3–7 s |

---

## 7. Pre-delivery checklist

- [ ] Recorded in 4K, delivered at 1080p; code still crisp after zoom; frame rate chosen as 30 or 60fps per content
- [ ] IDE at ≥18–22px, dark theme, line numbers on, minimap and sidebars off
- [ ] External mic and system audio on separate tracks; noise handled, levels consistent, BGM clear of the voice
- [ ] Cursor highlighted at 1.5–2× with no circling; zooms announced with a 0.8 s transition; holds ≥3 s before pans
- [ ] All pauses >1.5 s removed; navigation and repeated operations sped up; key moments at 1.0×
- [ ] Exact commands, code, paths and formulas all available as **copyable text** (matching what is on screen)
- [ ] Split into 5–7 minute segments at sub-goal boundaries with chapter markers, each ending on a question
- [ ] Closed captions switchable and in sync, ≤32 characters, ≤3 lines, 3–7 s, contrast ≥4.5:1, ≥16pt, 99% human proofread
- [ ] Full transcript provided; audio description or visual description where needed
- [ ] Player supports play/pause/seek/rewind/volume/speed, is keyboard-operable, and auto-moving content can be paused
- [ ] No necessary information conveyed by color, sound or motion alone; reduced-motion respected; no harmful flashing
- [ ] Exported H.264 + MP4 at 1080p 4–8 Mbps, loudness per the platform target (re-verified against the platform's latest official documentation)

---

## References

- Screen Recording Pipeline (4K record / 1080p deliver, 30/60fps, cursor and zoom parameters, IDE 18–22px): https://www.skillsdirectory.com/skills/aicodedecode-screen-recording
- Columbia, "Creating Accessible Video" (WCAG 2.1 AA, closed captions, ≤32 characters / 3–7 s, 4.5:1, 16pt, 99%): https://accessibility.columbia.edu/content/creating-accessible-video
- "Video authoring reference" (WCAG 2.2 SC 1.2.1/1.2.2/1.2.3/1.2.5/2.2.2, signaling and segmentation): https://github.com/metyatech/skill-tutorial-authoring/blob/main/references/video.md
- "How to make instructional videos people actually learn from" (≤6 minute segments, the Guo 2014 study): https://alugha.com/cms/how-to-make-instructional-videos
- "Screen Capturing for Tutorials" (30–90 s per segment, BGM −18 to −24 dB, 4–8 Mbps, dual tracks): https://boardthen.com?p=196/
- Accessibility Canada toolkit (the four elements: transcript, caption, audio description, keyboard): https://a11y.canada.ca/en/introduction-to-accessibility-requirements-for-audio-video/
- "Managing Captions and Cognitive Load" (WCAG 1.2.2, 5–7 minute segments, signaling): https://instruction.austincc.edu/nexus?p=19136
- A screen-recording teaching setup in Cap (picture-in-picture, dual-track audio, chapter markers): https://m.blog.csdn.net/gitblog_00921/article/details/156548019
- "Screen Recording" (recording parameters, 1080p/30fps): https://blog.csdn.net/gitblog_00188/article/details/159610772
- InScreen Editor (4K@60fps, zoom 1.25–5×, webcam PiP): https://garrik.design/studio

Retrieved: 2026-11-10
