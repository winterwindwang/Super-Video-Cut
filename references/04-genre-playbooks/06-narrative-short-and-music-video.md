# Narrative Short and Music Video Editing Playbook

> Category: Genre playbooks | Topic: Narrative shorts / micro-films / music videos / lyric videos / performance and dance films | Compiled: 2026-11-10 | Applies to: Short film directors and editors, MV post-production, brand micro-films, festival submission teams

> **Numeric disclaimer**: Aspect ratio, resolution, frame rate, duration, BPM math, subtitle sync accuracy, loudness and Spotify Canvas dimensions are all "subject to the platform's latest official documentation / the festival's submission spec sheet" and must be re-verified before delivery. Industry rules of thumb, directing methodologies and third-party tool specs are marked TO VERIFY.

---

## 1. Genre goals and evaluation metrics

**What they share**: Both are governed by "one irreversible timeline." The narrative short is governed by **emotion and character change**; the MV is governed by **the final locked music master**. They differ in first priority: narrative protects the performance first, the MV protects the music first.

| Metric | Narrative short | Music video |
|---|---|---|
| Narrative clarity | A stranger can retell the through-line and the character's change | Does the picture serve the song's structure |
| Emotional curve | Is the flat–rise–turn–fall–warmth variation visible | Does visual energy rise and fall with Intro → Chorus → Outro |
| Performance integrity | Keep the whole emotional arc; don't pick the "most correct" read line by line | Lip sync and performance aligned to the master at frame level |
| Beat and subtitles | Dialogue subtitles, opening and closing titles | Cuts snap to strong beats (lip-sync error measured in frames, TO VERIFY); lyrics aligned word by word to syllables |
| Style consistency | Consistent LUT, continuous scene lighting | The grade supports, never dominates |
| Aftertaste / completeness | Leave an aftertaste rather than "telling it all" | Watchable muted, croppable to vertical, first 3 seconds hold |

> A short film's value isn't in telling the story completely but in "making the audience want more when it ends." Stopping dead at a low point, a dead end or an awakening often leaves more aftertaste than a complete three-act structure.

---

## 2. Platform and delivery specs (subject to the platform's latest official documentation / submission spec sheet)

| Scenario | Aspect ratio | Resolution | Frame rate | Duration | Notes |
|---|---|---|---|---|---|
| Narrative short master | 16:9 (festivals also 1.85:1 / 2.39:1, TO VERIFY) | 1920×1080 / 3840×2160 | 24fps (cinematic) / 25fps | 5–15 min (1 page of script ≈ 1 min) | ProRes/DNxHR master + H.264 distribution copy |
| Micro-film / brand short | 16:9 | 1920×1080 | 25fps | 3–8 min | Brand values implied, never spoken as ad copy |
| MV master | 16:9 | 1920×1080 or 4K | 24/25/30fps | = song length (typically 3–5 min) | High-bitrate AAC; don't thin the low end |
| MV vertical derivative | 9:16 | 1080×1920 | Matches the master | 15–60 s | **Reframe**; place the subject in the central third |
| Spotify Canvas | 9:16 | 720–1080px tall (TO VERIFY) | — | 3–8 s loop | MP4 or JPG; pick one strong visual moment |

**Audio**: An MV must lay the **final approved mix** on the timeline and lock it before cutting. Swap the mix mid-edit and every beat hit drifts, even if the head is only a few frames off. Streaming loudness is about −14 LUFS (Spotify / YouTube / TikTok), Apple Music about −16 LUFS, ≤ −1 dBTP (TO VERIFY, subject to the platform's latest official documentation); broadcast masters follow EBU R128 at −23 LUFS (see category 02).

---

## 3. Structure template (timeline tables)

**Template A: 60-second narrative short (12 shots, ready to apply)**

| Timeline | Segment | Shots (scale / content) | Priority |
|---|---|---|---|
| 0:00–0:15 | Establish the everyday and the loneliness | ① wide of the station platform ② close-up of the clock ③ medium of the cleaner ④ train pulling in ⑤ empty carriage | ② and ④ are functional; one usable take is enough |
| 0:15–0:45 | Create the discovery and the test | ⑥ a figure appears in the glass reflection ⑦ the cleaner turns ⑧ close-up of the figure ⑨ the two look at each other ⑩ the train departs | ⑥ and ⑨ are the emotional core; worth several extra takes |
| 0:45–1:00 | Emotional landing | ⑪ empty station platform ⑫ the cleaner smiles | Close on breathing room |

> Story skeleton (TO VERIFY, director's methodology): three acts at 25% setup / 50% confrontation / 25% resolution; no single shot longer than 30 seconds; no more than 3 characters; no more than 3 locations.

**Short-film three-act timing table** (feature-length framing, TO VERIFY):

| Stage | Position in time | Task |
|---|---|---|
| Opening | First 30 seconds to 1 minute | Set the direction of the audience's expectation |
| Act One, "Departure" | Up to about 5 minutes | Establish character, conflict and world; must enter the next act within 5 minutes at most |
| Act Two, "Descent / Turn" | Around the middle 50%; a hard turn at 8–10 minutes | Escalate the conflict, hit bottom, awaken and rise again |
| Act Three, "Change" | Final 3–5 minutes | Show the change in attitude, behavior or essence, then close |

**Emotional curve**: flat → rise → turn → fall → warmth. For every scene, write down "who wants what / who or what blocks them / what state the scene moves from and to / the latest point to enter and the earliest to leave / which beat is the irreversible change." Enter just before the change and leave once the audience has absorbed the consequence.

**Template B: 3 min 30 s MV (song section → edit density)**

| Section | Timeline | Shot length / cut density | Visual strategy |
|---|---|---|---|
| Intro | 0:00–0:20 | Long takes, slow cutting, 3–8 s per shot | Establish the character and the visual world; set the tone |
| Verse 1 | 0:20–1:10 | Long takes, cuts at phrase ends, 4–8 s per shot | Let the lyrics and the performance breathe |
| Pre-chorus | 1:10–1:35 | Shortening section by section to 1–2 s | Tighten the rhythm, lift toward the drop |
| Chorus / Drop | 1:35–2:10 | Densest; cut on every strong beat or every other, 0.5–1 s per shot | Best angles, widest energy |
| Bridge | 2:10–2:45 | Change the texture: new location / speed ramp / static long take | Reset the eye |
| Chorus 2 + Outro | 2:45–3:30 | After the peak, slow gradually and lengthen shots | Settle into the closing image |

**BPM math and marker template** (ASCII straight quotes inside the code block):

```
bpm: 120
sec_per_beat: 0.5          # 60 / bpm
sec_per_bar_4: 2.0         # 4 beats
markers: "downbeats"       # beat 1 of each bar is the main cut grid
sections: "intro,verse,pre-chorus,chorus,bridge,outro"
pre_cut_chorus_sec: 0.3    # cut into the chorus 0.2-0.4 s early
```

---

## 4. Key techniques and specific parameters

**1. MV: music first**

| Item | Parameter / approach |
|---|---|
| Reference track and grid | Lay in the **final master** from the start and lock it, one version throughout. Find the BPM → mark strong beats (beat 1 of each bar) → mark structural changes → mark the vocal hook, snare hits and drop |
| Beat math | 120 BPM = 0.5 s per beat; 4 beats = 2 s; cutting into the chorus 0.2–0.4 s early locks better |
| Footage volume / multi-cam | Shoot at least 3× the song length; 6–10 s per stock clip, searched by emotional keyword; build a Sync Bin from timecode or shared audio, with separate Performance, Narrative and B-Roll bins |
| Lip sync / performance sync | Align every take to the reference track and check against a crisp consonant or a single hit; **check lip sync on that angle before every beat cut** |
| Mixed frame rates | A 24fps A-cam plus a 60fps slow-motion B-cam must **be conformed to the timeline frame rate first**, then retimed individually; the order is "sync first, retime second" |
| Cut density | Long takes in verses, cuts at phrase ends; densest in the chorus; in dance films, cut on movement accents (turns, landings, hits) rather than drum hits alone |
| Lyric subtitles | **Align word by word to syllables**, not line by line; karaoke / typewriter / big-text; bump stock-footage type size about +30% |
| Stylized grading | One base LUT across the film; teal-and-orange is the most common contrast; warm for intimacy, cool for distance, high contrast for tension, low saturation for texture; in lyric videos let legibility constrain contrast |

**2. Narrative short: performance first**

- **Cut the scene's intention first**: For each scene, write down the goal, the obstacle, the state change and the irreversible beat. Delete lines and coverage that only repeat what is already known; keep what changes the relationship, the pressure or the understanding.
- **Protect the performance / choose the dialogue**: Pick the complete emotional arc, and prioritize the listener, the reaction, the eyes and the body. Dialogue is only one part of a performance; use room tone, breath, clothing and movement sound to keep the body real. When performance and geometric continuity conflict, **protect the performance**, then repair with inserts, reactions and sound bridges. Don't hide behind B-roll to dodge the complicated moments on a face.
- **Sound, silence and counterpoint**: Don't wallpaper the whole film with music; leave a few seconds of ambience alone, or complete silence. Let picture rhythm play against music rhythm (one visual jolt while the music is calm; a second of stillness while the music rages). This is the line between "feels like cinema" and "feels like a fan edit."
- **Subtraction and testing**: Cut shots that duplicate a function, exist to show off, or tell the audience what they already understand. When you're done, **watch it muted, listen with eyes closed, then watch it normally**.
- **Head and tail**: The opening 30 seconds to 1 minute builds expectation; the tail carries title cards, credits, copyright and licensing information, and the logo. A short film should stop dead and leave aftertaste.

---

## 5. Audio, lyric subtitles, head and tail

1. **Audio first**: The MV is one of the few forms where sound is finalized before picture. Export at a high AAC bitrate and never thin the low end. Line-by-line lyric sync feels loose against the music, so align word by word to syllables; **AI lyric transcription must be corrected by hand** (its accuracy is worse than dialogue). Credit the song title and artist at the head, and copyright and licensing at the tail. A short film's opening and ending should rhyme, closing the loop and reinforcing the theme; an MV sets the tone at the head and settles into the closing image at the tail. Subtitle font, position and in/out behavior stay consistent across the film.
2. **Three-question self-check** (before export): Is it still watchable muted? Does the composition survive a 9:16 crop (subject in the central third)? Are the first 3 seconds worth staying for? If any answer is no, go back and fix it. Finish the 16:9 horizontal master first, then derive the 9:16 vertical and the 3–8 second Canvas loop; never re-edit from scratch for each platform.

---

## 6. Common pitfalls and anti-patterns

| Pitfall | Anti-pattern | Consequence | Fix |
|---|---|---|---|
| Swapping the mix mid-edit | Replacing the master halfway through | Every beat hit drifts | Lock the final version before you start |
| Cutting on every beat / chasing the drums | Ignoring vocal phrasing | Fatigue; cuts fight the lyrics | Long takes in verses, dense cutting in choruses, let the lyrics lead |
| Frame rate not conformed / lip sync unchecked | 24fps mixed with 60fps; matching music but not the mouth | Drift, performance breaks | Conform before retiming; check lip sync shot by shot |
| Narrative hiding behind B-roll | Cutting away to inserts whenever it gets complicated | The character is hollowed out | Keep the complicated moments on the face |
| Building the vertical version the night before delivery | Rough-cropping the horizontal cut to 9:16 | Subject cut off, rework | Plan the derivatives at the master stage |

---

## 7. Pre-delivery checklist

- [ ] Narrative: a scene card for every scene, with the flat–rise–turn–fall–warmth curve visible
- [ ] Narrative: performance integrity comes first; room tone, breath and movement sound in place; no B-roll used to dodge complex expressions
- [ ] MV: final master locked and used as a single version throughout; BPM strong beats and section markers complete
- [ ] MV: cuts snap to the beat, the chorus enters 0.2–0.4 s early, and there is no cutting on every beat
- [ ] MV: lip sync and performance aligned to the frame on every take, mixed frame rates conformed, slow motion following "sync first, retime second"
- [ ] Lyrics aligned word by word to syllables and AI transcription corrected by hand; one LUT across the film; music leaves silence and picture plays against it
- [ ] All three questions pass: watchable muted / croppable to 9:16 / first 3 seconds hold
- [ ] The opening sets expectation and the tail carries title cards, credits, copyright and licensing, and the logo; the short film leaves aftertaste
- [ ] Aspect ratio, resolution, frame rate, duration and loudness meet platform and festival specs (re-verified against the platform's latest official documentation / submission spec sheet)
- [ ] The horizontal master, the 9:16 vertical and the 3–8 second Canvas loop all derive from the same master
- [ ] Music, font and footage clearances on file (see category 05); the muted / eyes-closed / normal three-pass check completed

---

## References

- Music video editing (locking the mix, BPM, lip sync): https://www.hanna-eng.com/guides/monter-un-clip-musical
- MV beats and grading: https://www.v8eo.com/blogs/how-to-edit-music-video-beat-sync
- A Resolve MV workflow: https://tryuncle.com/learn/davinci-resolve/davinci-resolve-music-video-editing-and-color-workflow
- Stock-footage MVs: https://suno.bi/tr/blog/free-suno-mv-maker-with-stock-footage-2026-guide-en
- The 7 steps of MV production: https://n23-studio.com/blog/music-video-production-tools
- Taiwan Cinema, "An editing mentor on short film structure": https://taiwancinema.bamid.gov.tw/Articles/ArticlesContent?ContentUrl=94508
- Micro-films and brand storytelling: https://www.greataction.net/news/2449.html
- Three-act narrative structure: http://m.0769px.com/html/show-2-996-1.html
- A young director's guide to short films: http://www.cnmhr.com/?p=7370
- AI short-film directing in practice: https://domer.io/blog/ai-director-narrative-short-video-workflow
- Form playbook: https://github.com/ZimaBlueAI/skills/blob/main/produce-cinematic-video/references/form-playbooks.md
- Platform loudness standards: https://www.signalkey.io/learn/what-is-lufs

Retrieved: 2026-11-10
