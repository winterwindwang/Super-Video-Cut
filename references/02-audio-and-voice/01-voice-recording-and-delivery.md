# Voice-over Recording and Delivery Technique

> Category: Audio and voice | Topic: Vocal control, recording specifications, microphones, and ADR lip sync | Compiled: 2026-11-10 | Applies to: Narration / on-camera delivery / character recording, ADR pickups, home studio setup and sign-off

## Core principles

The vocal chain splits into four layers: power, source, resonance, articulation. Breath is the power stage, and a steady airstream comes from **combined chest-and-abdominal breathing** — the diaphragm drops while the waist and abdomen expand in sync. The vocal folds are the source. Chest, oral, and head resonance determine whether the timbre is thick or thin, bright or dark. Lips and tongue determine articulation clarity. The goal of training is not a "born-with-it voice" but a steady airstream, long sentences that do not run out of air, and phonation that does not squeeze the throat. Basic drills: alternate slow-inhale/fast-exhale with fast-inhale/slow-exhale; "dog panting" (6 sets a day, 15 s per set, recommended) to train diaphragm elasticity; counting to 30 on one breath for airstream stability; and vocal fry to wake up the folds.

Delivery has four controllable variables: **rate, pause, stress, emotion**. Break a sentence into thought groups by meaning, land stress on content words (nouns, verbs, numbers, conclusions), and slow down and lean in at each stress. Pauses come in two kinds: grammatical (comma, full stop) and emotional (a beat of anticipation before an emphasis). Rise at the end of a question, fall at the end of a statement, widen the contour on an exclamation — that alone prevents the metronomic monotone of a read-aloud. Reading the same passage in several different intonations is the most direct way to cure a mechanical delivery.

**Narration and character work are fundamentally different.** Narration *tells the listener something*: objective, neutral, clean articulation, even breath, restrained emotion, consistent pace, no put-on "broadcaster voice". Character work *lives the part*: design the timbre around age, occupation, and emotional state (raise the pitch and add breathiness for a child, drop the larynx for a villain's sense of menace), allow breathiness, gasps, and vocal breaks, and sync to on-screen action (panting while running, a pause while thinking). The "action language" training method borrows physical memory to make the performance feel real.

**ADR** (Automated Dialogue Replacement, also called looping) re-records individual lines in a studio against locked picture, in the same language and usually with the same actor — unlike **dubbing**, which swaps language and cast for a whole film. ADR is typically triggered by on-set wind, traffic, or generator noise; wireless dropouts; clothing rustle; rewritten lines after the cut; and mumbled or swallowed words. Real-world ADR rates run 5%-15%; the ideal is 0%. Recording clean production sound on set and grabbing a wild line immediately (same mic, repeat the line right after the take) can eliminate roughly 80% of ADR.

The physics of the recording chain: a microphone captures **direct sound plus room reflections**. The closer you are, the higher the direct-to-reflected ratio, and the fuller the low end thanks to the **proximity effect**; the farther you are, the more reflections dominate and the thinner it gets. Placement therefore matters more than post gain, because gain lifts the noise floor along with the voice and cannot restore lost low end. 48kHz/24bit is the de facto standard for video and broadcast: 48kHz avoids resampling against 44.1kHz material and gives the anti-aliasing filter a wider transition band; 24bit offers about 144dB of theoretical dynamic range (about 96dB at 16bit), leaving headroom above the quantization noise floor for post.

## Specifications and parameter tables

### Table 1 Speaking rate and pacing reference (Chinese, teaching rule-of-thumb values, TO VERIFY)

| Content type | Suggested rate | Character |
| --- | --- | --- |
| Concept explanation | 140-160 characters/min | Unhurried and clear |
| Walkthrough / demo | 160-180 characters/min | Moderate and fluid |
| Case study / story | 180-200 characters/min | Brisk and lively |
| Summary / recap | 150-170 characters/min | Steady and emphatic |
| Emotional radio / audiobook | About 160 characters/min (0.85-0.95× speed) | Comfortable over long listens |

Pauses: 0.3-0.8 s breath breaks between sentences; keep each sentence to 20 characters or fewer; slow down on key points, speed up through transitions; faster when excited, slower when serious.

### Table 2 Microphone types and polar patterns

| Type / pattern | Pickup character | Use | Watch out for |
| --- | --- | --- | --- |
| Condenser | High sensitivity, lots of detail, needs 48V phantom power | Quiet, acoustically treated studio | Prone to plosives and ambient noise |
| Dynamic | Low sensitivity, insensitive to distant noise | Untreated rooms, street-facing spaces, live streaming | Needs closer placement and more gain |
| Cardioid | Acceptance angle about 131 degrees, most sensitive on axis, weakest at the rear | First choice for solo narration / on-camera delivery | Proximity effect and plosive tendency |
| Supercardioid | Narrower, stronger side rejection | Noisy environments | Slight rear pickup lobe |
| Omni | 360-degree pickup, immune to proximity effect | Room ambience, group vocals | Captures every reflection |
| Figure-8 | Front and back, rejected at the sides | Two people facing each other | Demanding on the room |

### Table 3 Placement, levels, and recording specifications

| Item | Recommended value | Notes |
| --- | --- | --- |
| Sample rate / bit depth / channels | 48kHz / 24bit / mono (voice) | Baseline for video delivery |
| Recording peaks | -18 to -12 dBFS, never above -3 dBFS | Leave adequate headroom |
| Input gain knob | In the -12 to -6 dB range | Units differ between interfaces |
| Condenser distance | 10-20 cm | 15-20 cm from the pop filter rim to the lips |
| Dynamic distance | 5-15 cm | Closer |
| Off-axis angle | 30-45 degrees | Stay out of the airstream, reduce p/b plosives |
| Microphone height | Diaphragm level with the tip of the nose | Prevents excess nasal resonance |
| Pop filter spacing | >=5 cm from the mic | Buffers the airstream, reduces high-frequency overload |
| Low cut | 80 Hz | Removes HVAC and desk rumble |
| Room noise floor | <= -60 dBFS | Reachable with bookshelves, rugs, heavy curtains |
| Two-mic 3:1 rule | Second mic at least 3× the source distance from the primary | Reduces phase comb filtering |
| Monitoring | Closed-back headphones + zero-latency direct monitoring | Open-back headphones leak into the mic |

### Table 4 Markup symbols for delivery scripts (studio-specific, no unified national standard, TO VERIFY)

| Symbol | Meaning |
| --- | --- |
| `/` | Short pause (thought group) |
| `//` | Long pause / paragraph |
| `·` or bold | Stress |
| `↑` / `↓` | Rising / falling intonation |
| `<slow>` `<fast>` | Tempo change |
| `[breath]` | Breath point |
| `()` | Emotion cue |

### Table 5 ADR cue sheet fields

| Field | Example |
| --- | --- |
| Cue number | MAY-014 |
| Character / TC in / TC out | Maya / 01:12:10:04 / 01:12:12:20 |
| Original line | "You knew the whole time." |
| Reason for re-record | Coffee grinder masking the line |

## Procedure / Workflow

### A. Script preparation and markup
1. Fix the purpose (commercial / documentary / training / character) and the audience, then mark the emotional arc line by line.
2. Split thought groups by meaning with `/`, mark key information with `·`, write emotional anchors in the margin; for long sentences, find the breath points first.
3. Rehearse once or twice, using method acting to trigger genuine emotion rather than a projected voice.

### B. Studio setup and test recording
1. Pick the quietest room and separate **soundproofing** (blocking external noise; needs professional construction and is expensive) from **acoustic treatment** (absorbing internal reflections): place 2-inch wedge foam at the first reflection points, add heavy curtains, rugs, and a reflection filter. Never add reverb to a voice.
2. Turn off air conditioning, fans, and phone notifications; keep the computer away from the mic; monitor on closed-back headphones.
3. Cardioid mic on a shock mount with a pop filter, 30 degrees off axis, 15-20 cm away, diaphragm level with the nose; confirm the interface has 48V phantom power and zero-latency direct monitoring.
4. Set the DAW to 48kHz/24bit/mono, record a 30-second test, and check that peaks land between -18 and -12 dBFS.
5. Capture 3-5 seconds of pure room tone as a spare, for bedding in post and for matching ADR.

### C. Recording
- Record in segments: after a flub or a stall, pause 2 seconds and restart from the previous thought group so the edit can be stitched; keep 2-3 usable takes per line.

### D. ADR workflow
1. **Spotting**: director, editor, and supervising sound editor review the locked cut and produce the ADR list (timecode, original line, reason). Exhaust the alternate takes first — if production sound can be substituted, do not re-record.
2. **Prep**: cut each cue into a 5-10 second loop (Loop Method) or a beep strip (Strip Method); import production sound as a guide track; lock the DAW frame rate to 23.976/24 fps; add streamers and wipes as visual cues; check the on-set mic model.
3. **Recording**: the actor watches picture, hears 3 beeps, and comes in on the fourth beat (the silent point); 2-5 passes per line (10+ for hard lines); record a wild line as well.
4. **Editing**: align lip sync syllable by syllable, splicing the best head and tail from different takes if needed; use a VocAlign-class tool for waveform alignment; correct offsets within 50-100 ms.
5. **Matching**: prefer the same mic model, then add EQ, location reverb, and room tone to remove the "studio sound"; match levels to the production dialogue; replace only the problem segment and keep the clean parts of the production track.

### E. Runnable commands (tested locally on ffmpeg 8.1.2)

Check recording peaks/RMS and confirm nothing clipped:
```
ffmpeg -hide_banner -i raw.wav -af astats=metadata=1 -f null -
```

Convert to 48kHz/24bit mono with an 80Hz low cut:
```
ffmpeg -i raw.wav -af "highpass=f=80" -ar 48000 -ac 1 -c:a pcm_s24le clean.wav
```

Locate silences and pauses to help segment the edit:
```
ffmpeg -hide_banner -i raw.wav -af "silencedetect=n=-45dB:d=0.4" -f null - 2>&1
```

Measure test-recording loudness (I / LRA / True Peak in one pass):
```
ffmpeg -hide_banner -i raw.wav -af "ebur128=peak=true" -f null - 2>&1
```

Extract the first 5 seconds of room tone:
```
ffmpeg -i raw.wav -t 5 -af "highpass=f=80" -ar 48000 -ac 1 -c:a pcm_s24le roomtone.wav
```

> Note: the `ebur128` summary prints Integrated loudness (LUFS), Threshold, LRA, and True peak. Threshold sits about 10 LU below I, which is exactly the -10 LU relative gate of BS.1770 (measured locally on a 1 kHz sine: I=-21.1 LUFS, Threshold=-31.1 LUFS).

## Common errors and troubleshooting

| Symptom | Root cause | Fix |
| --- | --- | --- |
| Thin, floaty voice | Too far from the mic, making up for it with gain | Move in to 15-20 cm first; do not add gain (it lifts the noise floor too) |
| p/b plosives, popping | Straight into the airstream | 30 degrees off axis + pop filter, spaced >=5 cm |
| Boomy low end | Proximity effect | Back off slightly, engage the mic's low cut, or high-pass at 80Hz |
| Sibilance / mouth clicks | Too close | Back off, go off axis, de-ess in post |
| Heavy room echo | High proportion of reflected sound | Acoustic foam, heavy curtains, reflection filter |
| Hum / noise floor | Insufficient USB power, fans | Move to a rear port or a powered hub; relocate the computer |
| Dropouts | Buffer too small | Set the ASIO buffer to 512 samples |
| Clipping | Peaks above 0 dBFS | Pull gain back 6 dB and re-record |
| ADR "studio sound" | Dry signal with no sense of room | Add EQ, reverb, and room tone; match the production mic |
| Lip sync drift | Line starts too early or late | Nudge the waveform 50-100 ms, or rewrite the phrasing / lengthen a vowel |

## Quick reference

- [ ] Script marked with pauses `/`, stress `·`, breaths `[breath]`, and emotional anchors
- [ ] 48kHz / 24bit / mono, peaks -18 to -12 dBFS, never above -3 dBFS
- [ ] Cardioid mic + pop filter + shock mount, 15-20 cm, 30 degrees off axis, level with the nose
- [ ] Air conditioning / fans / notifications off, 3-5 s of room tone captured, noise floor <= -60 dBFS
- [ ] Segmented recording, 2-second pause before a re-take, 2-3 takes kept per line
- [ ] ADR: cue sheet carries timecode; 3 beeps + entry on the fourth beat; frame rate locked
- [ ] ADR mic model and distance match production; room tone and reverb added in the mix
- [ ] Monitoring check on two systems: headphones plus a small speaker

## References

- Hertz Studio, ADR Recording: When Dialogue Replacement Is Needed and How It Works — https://www.hertzstudio.com/?p=12782
- Storiara, ADR (Automated Dialogue Replacement) — https://storiara.com/glossary/adr
- Filmfarm, Automatic Dialogue Replacement (ADR) — https://filmfarm.de/en/adr
- Mattermind, ADR for Film: Mastering the Technical Workflow — https://mattermind.blog/adr-film-mastering-technical-workflow
- Xiangla Dubbing Network (响啦配音网), Film dubbing workflow: a sound director's field notes — http://www.xiangla.cn/article/17952905.html
- Audio App (音频应用), How to build a clean recording space (polar patterns / proximity effect) — https://audioapp.cn/audio/11898.html
- CSDN, VoiceStudio personal audio workstation (48kHz/24bit parameter math) — https://blog.csdn.net/weixin_26911099/article/details/165801692
- Kaifayun (嵌云网), USB condenser microphone buying guide and recording setups (placement / gain / low cut) — https://kaifayun.com/article/weixin_29055699/1172605
- Zhou Shuchang (周舒畅), Chapter 6: Audio processing and dubbing technique (speaking-rate table) — https://zsc.github.io/video_author/chapter6.html
- Study Methods Network (学习方法网), Learning methods and technique for broadcast voice work (breath training) — https://www.ettschool.cn/xuexifangfa/1256514.html
- Taiwan Access (台湾高空), Podcast microphone capture and acoustic treatment (acoustics vs. soundproofing) — https://www.taiwanaccess.com.tw/en/blog/posts/podcast-microphone-acoustic-treatment
- DAV Digital Audio-Visual Engineering (DAV 数字音视工程网), Pickup distance and the proximity effect — https://m.dav01.com/corp/teanma/article/2026/09/a75038.html
- FFmpeg official documentation (filter syntax) — https://www.ffmpeg.org/ffmpeg-filters.html

Retrieved: 2026-11-10

**TO VERIFY**: ① The speaking rates in Table 1 (140-200 characters/min) are teaching rule-of-thumb values, not a mandatory standard, and must be tuned by genre and platform through testing; ② The script markup symbols in Table 4 are defined per studio, with no unified national standard; ③ "The last beep lands 1 1/3 seconds before the line starts" comes from a single source, and streamer/beep configurations differ between studios; ④ Placement distances and gain ranges must be calibrated against the specific microphone model and interface; ⑤ The ffmpeg commands in this file were tested locally on 8.1.2, but output filenames and paths must be substituted for your own.
