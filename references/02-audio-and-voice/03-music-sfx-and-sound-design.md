# Music, Sound Effects, and Sound Design

> Category: Audio and voice | Topic: BPM beat sync, matching music structure to picture, ambience and Foley layering, transitions and stereo space | Compiled: 2026-11-10 | Applies to: Music editing for short-form video / documentary / promo, SFX bedding, organizing assets before the final mix

## Core principles

Choosing music is not "picking a song you like" — it is three alignment relationships: **picture emotion = musical emotion, cut tempo = musical BPM, picture structure = musical structure**. Harmonic fit, stylistic fit, unified beat sync, and section-to-section correspondence together decide whether the finished piece feels polished.

Sound design usually aims to be *felt but not noticed*. Mixing has a stable layer order: **dialogue → ambience → Foley → music → transition SFX**. Build in that order and you will rarely need to tear the balance down at the end. Dialogue stays centred and essentially dry; it is the anchor of the whole track.

Frequency collision is the most common reason music fails: vocal intelligibility lives in **1-4 kHz**, and if the music is dense in that region (especially with a vocal in the original track or stacked synths), no amount of ducking will rescue it — change the cue. 200-500 Hz is where mud accumulates; both ambience and music should be high-passed out of the way.

A sense of space comes not from level alone but from **three depth cues**: volume, brightness, and reverb. To push a sound "back", lower it, roll off the top end (low-pass), soften transients, and add a touch of room reverb; to bring it "up to the ear", keep it bright, dry, and transient-intact.

## Specifications and parameter tables

### Table 1 BPM mapped to on-screen pacing (empirical classification, TO VERIFY)

| BPM range | Shot duration | Suited to |
| --- | --- | --- |
| 50-80 | 3-6 s | Slow motion, sunsets, nostalgia, quiet landscapes |
| 80-105 | 2-4 s | Documentary, city travel, humanist narration (the most versatile) |
| 105-130 | 1-2 s | Fresh and energetic, street photography, behind-the-scenes |
| Above 130 | 0.5-2 s | Fast cuts, trend-driven beat sync, action footage |

Beat assignment: **downbeats** carry cuts, transitions, punch-ins, and pushes; **offbeats** carry small movements, camera moves, and gentle push-pulls; in **beatless** passages, cut to emotion and do not force a sync.

### Table 2 Beat-sync math (4/4 time)

| Quantity | Formula |
| --- | --- |
| Seconds per beat | `60 / BPM` |
| Seconds per bar (4/4) | `(60 / BPM) * 4` |
| Length of N bars | `seconds per bar * N` |
| Frames | `seconds * project FPS` |

Worked example: 82 BPM → about 0.7317 s per beat, about 2.9268 s per bar, about 11.707 s for 4 bars, about 351 frames at 30 fps. Always loop and trim in **whole bars** (1/2/4 bars) so edits land on the phrase and crossfades land on the beat.

### Table 3 The four sections of a music cue and what picture does over them

| Section | Picture task | Level |
| --- | --- | --- |
| Intro | Establishing wide shots, empty ambience, opening hook | Lower, so speech and effects stand out |
| Verse | Mid-shot storytelling, detail inserts, walking shots | About 60%, narration or ambience may sit on top |
| Chorus (climax) | The best shots, aerials, wide vistas, highlights | 80%-90%, highest cut frequency |
| Outro | Closing freeze, fade to black, titles/CTA | Fade down; never cut off abruptly at the peak |

### Table 4 Level hierarchy rules (reference before mastering, TO VERIFY)

| Scenario | Voice | Background music |
| --- | --- | --- |
| Video with narration | -12 to -15 dB | **-18 to -24 dB** |
| Picture only, no narration | — | -12 to -15 dB |
| Climax passage | — | Nudge up 2-3 dB |
| Ending | — | Auto fade out over 0.5 s (2-3 s for a long cue) |

Sound effects peak around -6 dBFS; game soundtracks and ambience beds sit about 30% lower; Foley sits 6-10 dB below dialogue.

### Table 5 Ambience in three frequency layers

| Layer | Content | Level reference |
| --- | --- | --- |
| Base bed | Continuous, low, unidentifiable: wind, distant traffic, room hum | ≈ -30 dBFS |
| Mid detail | Identifiable but quiet: birdsong, footsteps in a corridor, crowd murmur | ≈ -24 dBFS |
| Accents | Occasional and specific: a door closing, a siren, a chair scraping | ≈ -18 dBFS |

A static loop sounds like a library the moment you hear it: add slow level automation of 0.5-1.5 dB, occasional one-shots, and small EQ shifts between sections so the room feels alive.

### Table 6 Foley and SFX parameters

| Item | Parameter |
| --- | --- |
| Coverage | Everything a character touches must make a sound: cup on table, zipper, keyboard, car door |
| Relative level | 6-10 dB below dialogue |
| High-pass | Cut below 100 Hz (except sub-heavy material such as explosions) |
| Low-pass | Roll off above 10 kHz to stay out of the voice's way |
| Layer ceiling | 3-4 layers per SFX at most; more than that turns to mud |
| Recording | Multiple close and distant passes, varied surfaces; use a deadcat outdoors for wind |
| UI / notification sounds | 50-200 ms, peak -6 dB, high-pass at 200 Hz |

### Table 7 Transition SFX types

| Type | Use | Key requirement |
| --- | --- | --- |
| Whoosh | Fast shot or scene changes | Peak lands **exactly on the cut**; two frames late reads as sloppy |
| Riser | Building energy, pre-climax | A half-second swell often hides a hard cut better than a 6-second build |
| Impact / Reverse | Reveals, flashbacks, jumps | One transition sound per transition; do not reuse the same whoosh four times |
| Room-tone ramp | Masks the rhythmic seam when two interviews are spliced | Pair with a slight lift in the music |

### Table 8 Frequency carving and ducking

| Technique | Parameter |
| --- | --- |
| Music / ambience high-pass | 120-200 Hz (higher than you would expect) |
| Mud cut | -2 to -4 dB at 200-500 Hz |
| Intelligibility band | Leave 1-4 kHz to the voice; use a dynamic EQ that ducks only while the voice is active |
| Music ducking | -2 to -6 dB (3-6 dB typical) |
| Ambience ducking | -1 to -3 dB |
| Attack / Release | <10 ms / 200-400 ms, ratio 2:1-3:1 |
| Band selectivity | Multiband compression on 1-4 kHz only, preserving low end and air |
| Abort criterion | If you need more than 10 dB of ducking to hear the voice → change the cue, do not force it |

### Table 9 Panning and the three depth cues

| Cue | "Far / back" | "Near / front" |
| --- | --- | --- |
| Volume | Low | High |
| Brightness | Low-pass to darken (e.g. 6-10 kHz) | Stay bright |
| Reverb | Add a little room verb, soften transients | Dry, transients intact |

Dialogue stays centred and dry; **one wide element plus one centre element is the limit** (everything wide means nothing is wide); pan Foley slightly to match the character's position in frame; send dialogue and Foley to the same aux with different wet/dry so the space feels unified; roll off the highs on distant Foley to imitate air absorption.

### Table 10 Music editing parameters

| Operation | Parameter |
| --- | --- |
| Fade in / fade out | 1 s at the head / 2 s at the tail |
| Crossfade between two cues | 2-3 s overlap, outgoing fades out while incoming fades in |
| BPM difference between cues | Keep within ±10 |
| Loop-boundary crossfade | 20-50 ms, still landing on the beat |
| Section extraction | Prefer complete "intro + verse" or "verse + chorus" blocks; do not cut mid-section |
| Looping in moderation | Repeated loops fatigue the ear on long videos; prefer a second cue spliced in |
| Export | 48kHz/24bit; H.264 + AAC for online delivery, bitrate >=20 Mbps |

## Procedure / Workflow (commands tested locally on ffmpeg 8.1.2)

### A. Cue selection and beat sync
1. **Lock the picture before choosing the music** (scoring to a cut that is still moving is wasted work). Settle the overall emotion, then fix the style and BPM.
2. Import the music, read the waveform energy peaks or generate beat markers automatically, then hand-tune the keyframes by half a beat.
3. Use the formulas in Table 2 to derive seconds per beat and per bar, and snap cuts to the downbeat or to 8th/16th notes.

### B. Structural alignment and music editing
4. Lay the picture out against intro / verse / chorus / outro; put the chorus under the aerials and wide shots.
5. Trim long cues, fade in and out, and splice two cues with a crossfade (commands below).

Trim + fades + slight tempo change:
```
ffmpeg -ss 12 -t 30 -i music.wav -af "afade=t=in:st=0:d=1,afade=t=out:st=28:d=2,atempo=1.05" -ar 48000 -c:a pcm_s24le music_cut.wav
```

Exact trim (atrim form):
```
ffmpeg -i music.wav -af "atrim=start=12:end=42,asetpts=PTS-STARTPTS" -ar 48000 -c:a pcm_s24le seg.wav
```

Crossfade splice between two cues (tested `acrossfade`):
```
ffmpeg -i a.wav -i b.wav -filter_complex "[0:a][1:a]acrossfade=d=2:c1=tri:c2=tri[out]" -map "[out]" -ar 48000 -c:a pcm_s24le joined.wav
```

Seamless whole-bar loop (tested `aloop`; `size` is in samples; one bar at 48kHz/120BPM = 96000 samples):
```
ffmpeg -i loop.wav -af "aloop=loop=3:size=96000" -ar 48000 -c:a pcm_s24le loop4.wav
```

### C. Layering and carving
6. Set the dialogue anchor first, then build the three ambience layers, Foley, music, and transitions, taking levels from Tables 4/5/6.
7. Carve frequency space for the music and ambience:
```
ffmpeg -i music.wav -af "highpass=f=150,equalizer=f=300:t=q:w=1:g=-3,equalizer=f=2500:t=q:w=1:g=-2" -ar 48000 -c:a pcm_s24le music_carved.wav
```
8. Sidechain ducking (see document 02 for detail): 3-6 dB for music, 1-3 dB for ambience, attack <10 ms, release 200-400 ms.

### D. Unified loudness before export
```
ffmpeg -i mix.wav -af "loudnorm=I=-14:TP=-1:LRA=11" -ar 48000 -c:a pcm_s24le master.wav
```
9. Check on two systems: a phone speaker (is the voice being masked?) and good headphones (imaging and noise). If you can, calibrate monitoring at 85 dB SPL (TO VERIFY).

## Common errors and troubleshooting

| Error | Consequence | Fix |
| --- | --- | --- |
| Using a cue with an original vocal under narration | Vocals fight each other, quality drops | Always switch to an instrumental or backing track |
| Hard-cutting a loop at the half-bar | Rhythm breaks | Whole bars + 20-50 ms crossfade |
| Transition peak two frames late | Reads as sloppy | Align the peak exactly to the cut |
| Everything panned wide | Smeared imaging, mono collapse | One wide + one centre, and stop there |
| Rescuing frequency collisions with heavy ducking | Pumping, music surges up and down | Band-selective EQ; change the cue if needed |
| Static ambience loop | Sounds like a library | 0.5-1.5 dB automation + occasional one-shots |
| Foley too loud | Steals focus, fatigues | 6-10 dB below dialogue, check at low volume |
| Cutting off abruptly at the climax | The audience is yanked out | Fade through the outro, land on the musical resolution |
| Choosing music before locking picture | Endless rework | Lock the picture first |

## Quick reference

- [ ] Picture locked first; emotion / BPM / structure all three aligned
- [ ] Beat math done in whole bars, cuts snapped to the downbeat
- [ ] Instrumental only under narration, music at -18 to -24 dB
- [ ] Ambience three layers at -30/-24/-18 dBFS, with automation to avoid static
- [ ] Foley 6-10 dB below dialogue, high-pass at 100 Hz, 3-4 layers max
- [ ] Transition peaks on the cut, one per transition, never repeated
- [ ] Frequency carving: high-pass 120-200 Hz, cut 200-500 Hz, keep 1-4 kHz for the voice
- [ ] Fade in 1 s / fade out 2 s; cue crossfade 2-3 s, BPM difference <=10
- [ ] Reviewed on both a small speaker and headphones; the voice stays intelligible throughout

## References

- WeChat Official Account article, The complete guide to music for short video (BPM ranges / four-section structure / level hierarchy) — http://mp.weixin.qq.com/s?__biz=Mzg3OTA3MTYyOA==&mid=2247483910&idx=1&sn=8eea8e6922be1d37b29d17fab56ee278
- DV Editing Home (DV 非编之家), Music editing and structural workflow guide — https://www.dv123.cn/forum.php?action=printable&mod=viewthread&tid=73558
- Efusc (豚牛手游网), Scoring game edits from scratch (levels / ducking / fades) — https://www.efusc.com/news/807253.html
- Xunmiwang (寻觅网), TikTok script-to-BGM matching and section alignment — https://www.xunmiwang.cn/678873.html
- Artclip, Syncing Motion Clips to Singles (BPM math) — https://artclip.biz/syncing-motion-clips-to-singles-quick-guide-for-indie-musici
- SonusGearFlow, The Art of Layering in Podcasts (layering / ducking / three depth cues) — https://sonusgearflow.com/musicproduction/the-art-of-layering-in-podcasts
- Domer AI, How to Improve Audio Quality in AI Video (three-band levels) — https://domer.io/blog/improve-audio-quality-ai-video-voice-music
- AudioScene, Balancing Dialogue and Foley (Foley 6-10 dB down, 85 dB SPL) — https://audioscene.org/article/balancing-dialogue-and-foley-for-a-natural-and-engaging-soundscape
- Plugg Supply, Foley & Sound Effects Design Guide 2026 — https://sv.plugg-supply.net/articles/foley-sound-effects-design-guide-elevate-your-productions-in-2026
- Domer AI, Studio-Grade Video Sound (layer order, attack/release) — https://domer.io/blog/ai-background-music-video-sound-workflow
- FFmpeg official documentation (filter syntax) — https://www.ffmpeg.org/ffmpeg-filters.html

Retrieved: 2026-11-10

**TO VERIFY**: ① The BPM ranges and their mapping to mood and shot duration in Table 1, the level hierarchy in Table 4, the -30/-24/-18 dBFS figures in Table 5, and the ±10 BPM difference and crossfade durations in Table 10 are all rule-of-thumb values from tutorials and engineering blogs, not mandatory standards, and must be tested per genre and platform; ② The 85 dB SPL monitoring calibration has not been checked against an official specification; ③ WeChat Official Account article links may expire over time; ④ The `size` argument of `aloop` must be converted from the actual sample rate and bar length (the 96000-sample example applies only to 48kHz/120BPM/1 bar); ⑤ The ffmpeg commands in this file were tested locally on 8.1.2, but input and output filenames must be substituted for your own.
