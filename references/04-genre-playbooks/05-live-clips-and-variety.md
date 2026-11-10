# Live-Stream Clips and Variety Show Editing Playbook

> Category: Genre playbooks | Topic: Livestream highlight clips / selling clips / variety show moments and behind-the-scenes / secondary-creation packaging | Compiled: 2026-11-10 | Applies to: Clip operators, MCN post-production, variety show editors, account-matrix teams

> **Numeric disclaimer**: Resolution, aspect ratio, frame rate, duration, playback speed, levels, loudness, joke spacing and publishing timeliness are all "subject to the platform's latest official documentation." Platform rules, authorization channels and deduplication criteria change frequently, so re-check before publishing. Industry rules of thumb, specific authorization channels and legal conclusions are marked TO VERIFY; commercial campaigns must pass legal review (full regulations in the 05-copyright category).

---

## 1. Genre goals and evaluation metrics

**Goal**: Distill hours of livestream or a long master cut into 15–90 second highlights that can travel on their own, amplifying the jokes, the contrast and the emotion while staying inside the authorization and compliance lines. **Compliance comes first, not last** — without authorization, no editing technique holds up.

| Metric | Meaning | Related decision |
|---|---|---|
| 3-second retention / completion rate | Does the hook hold | Conflict or benefit in the first 3 seconds |
| Joke / highlight density | Effective emotional beats per unit of time | Reaction shots, slow motion, breathing room |
| Engagement rate (comments / bullet comments (danmaku) / shares) | Does the meme land with this audience | Kinetic text, danmaku elements, trending phrases |
| Originality / dedup pass | Whether it is flagged as "homogeneous reposting" and throttled | Depth of secondary creation |
| Authorization compliance / publishing timeliness | Completeness of the rights chain and paperwork / how fast the trend decays | One-strike disqualifier / tiered at 2h, 24h, 72h |

> Joke frequency rules of thumb (TO VERIFY): ideally a laugh every 3 seconds; in practice, a small laugh every ten-odd seconds and a big one every couple of minutes. Clips need higher density still.

---

## 2. Platform specs and material organization (subject to the platform's latest official documentation)

| Scenario | Aspect ratio | Resolution | Frame rate | Duration | Notes |
|---|---|---|---|---|---|
| Livestream clips (Douyin (抖音) / Kuaishou (快手) / WeChat Channels (视频号)) | 9:16 | 1080×1920 | 30fps | 15–60 s, ≤90 s | MP4 / H.264; must capture system audio |
| Self-recorded capture | 9:16 | 1080P | 30fps | Whole session | OBS or similar; record 1 minute as a test for A/V sync; turn off pop-up notifications |
| Variety master / vertical derivative | 16:9 / 9:16 | 1920×1080 / 1080×1920 | 25/30fps | 1–5 min / 15–90 s | Subject centered; clear the UI safe areas (see category 01) |

**Multi-track / multi-cam material log** (build the ledger before you start cutting):

| Track | Content | Purpose |
|---|---|---|
| V1 | Host / guest main angle (medium shot) | Through-line narration |
| V2 | Product close-ups, hands, details | Enlarge selling points, cover edit points |
| V3 | Wide shots / audience / environment | Establish space, reactions, transitions |
| A1 | Livestream original audio / sync sound | Main audio track, locked for the whole piece |
| A2 / A3 + text track | System audio / audience laughter / highlight markers / transcript | Atmosphere, emotion, reference for locating |

> Highlight markers: for selling, tag "price drop, live test, price comparison, closing push, after-sales"; for content, tag "killer line, counterintuitive, emotional peak, comment flood." Mark the timeline first, then decide what to cut.

**Material naming / highlight marker template** (ASCII straight quotes inside the code block):

```
clip_id: "20261110_LIVE_A1_002345"
source: "licensor's original replay"    # or "self-recorded capture"
timecode_in: "01:23:45:00"
tag: "price_drop"                        # or "killer_line" / "on-air_flub" / "reaction"
authorized_by: "MCN written authorization - No. XXX"
rights_scope: "copyright + likeness + voice"
```

---

## 3. Structure template (timeline tables)

**Template A: 45-second livestream selling clip**

| Timeline | Task |
|---|---|
| 0:00–0:03 | Hook: conflict or benefit ("399 full price, 99 today") |
| 0:03–0:10 | Explain the product feature or the core point |
| 0:10–0:35 | Dense selling points / live test / price comparison, intercut with reactions and close-ups |
| 0:35–0:42 | Climax: closing-push offer / emotional peak + beat-synced sound design |
| 0:42–0:45 | CTA: one clear action ("tap cart item 1"), one line only |

**Template B: 60-second variety moment / behind the scenes**

| Timeline | Segment | Approach |
|---|---|---|
| 0:00–0:03 | Result up front / contrast teaser | The most explosive frame up front, 3 fast cuts |
| 0:03–0:15 | Establish the situation | Multi-cam sets up the relationships; fast cuts build tension in a standoff |
| 0:15–0:40 | The comic beat | A cut every 3–5 s, intercutting faces, hands, inserts and reaction shots |
| 0:40–1:00 | Climax flub + aftertaste | 0.5–0.7× slow motion holding a micro-expression + sound effects and kinetic text; 0.3–0.8 s of breathing room to close |

**Publishing timeliness tiers** (industry rule of thumb, TO VERIFY): post trend clips within 2 hours of the stream ending, best-of clips within 24 hours, and long-tail Q&A clips within 72 hours.

---

## 4. Key techniques and specific parameters

| Item | Parameter | Key point |
|---|---|---|
| Overall speed | 1.2–1.3×, back to 1.0× on key moments | Cut flubs, dead air, repetition and irrelevant content |
| Shot changes | A cut every 3–5 s | Intercut faces, hands, inserts and reaction shots |
| Fast/slow contrast | Slow motion 0.5–0.7×; beat-synced fast cuts at emotional peaks | Freeze on the blank micro-expression at the moment of the reveal |
| Breathing room | Pause 0.3–0.8 s after a joke or a reversal | Give the audience time to react |
| Reaction shots | Intercut other people's reactions | **Support the emotion; never steal the subject's thunder** |
| Kinetic text | Yellow with black stroke / white with black stroke / bright pink-purple; bold, stroked, shaking | Inner monologue, !!! / ???, memes |
| Sound effects | 1–2 light effects per shot: spring, snort, shock sting, gasp, whoosh / swish / ding transitions | Don't stack them |
| BGM | Upbeat / earworm / hard beat; switch the moment the emotion turns | Voice −6 dB / music −12 dB; original audio can drop to 20%–80% and be layered underneath |
| Overall loudness / watermark removal | About −14 to −12 LUFS, −1 dBTP (TO VERIFY); masks, occlusion, cropping | Avoid normalization flattening the dynamics; operate only within the authorized scope |

**Secondary-creation dedup** (to avoid being throttled as "homogeneous reposting / duplicate content"):

| Layer | Methods |
|---|---|
| Picture + structure | Mirroring, frame sampling ±2–5 frames, scale and position shifts, filter grading, custom stickers; break 1 minute into a dozen to twenty shots; replace the first 3 seconds, reorder, add 3-second head and tail cards |
| Sound + copy | Keep the original audio under BGM or add an original voice-over; **rewrite the subtitles** instead of copying the stream's kinetic text; rewrite the title and description |

> Trimming a clip and posting it as-is gets flagged as homogeneous reposting; deep secondary creation is often also a condition of the authorization.

---

## 5. Audio, subtitles and interactive packaging

1. **Subtitles**: Proofread by hand after machine recognition; enlarge key numbers and selling points and highlight them with kinetic text. Never copy the stream's on-screen text — rewrite it into your own distilled selling point (e.g. "this dress hides the belly" → "this cut is built for a lower-belly bulge").
2. **Three audio layers**: host's voice + ambience (fabric rustle, footsteps) + emotional sound design; don't swap the voice track when cutting shots, or the level will jump (same as category 02).
3. **Danmaku and interactive elements**: floating danmaku, inner-monologue speech bubbles, reaction stickers, corner tags (`@account name`), dual-language subtitles, self-deprecation and meme translation; harvest trending phrases for the joke. Kinetic-text sound effects are garnish only and must never upstage the content; interactive elements must contain no discrimination, flame-baiting or false advertising.

---

## 6. Clip authorization and compliance boundaries (critical)

| Item | Rule | Notes |
|---|---|---|
| Cutting someone else's livestream | **Must** obtain written authorization from the host / MCN / official alliance and keep the paperwork on file | On Douyin, apply through Zhongxiaohe (众小河), Chanxuan (蝉选), Ocean Engine Xingtu (巨量星图) or the host's clip alliance; on WeChat Channels / Kuaishou, confirm authorization before attaching products (**specific channels TO VERIFY, subject to the platform's latest official documentation**) |
| Scope of authorization | Must cover **copyright (including the right of information network dissemination and the right of adaptation) + likeness rights + voice rights**, with the chain verified as complete | Lawyer's recommendation (legal applicability TO VERIFY) |
| Fair use / platform liability | Personal study and appreciation may fall under Article 24 of the Copyright Law, but **clip-based selling for profit is not fair use**; Articles 1195/1197 of the Civil Code establish joint liability where a platform fails to remove content promptly after notice | As above |
| Attribution / the four checks | **Attribution ≠ authorization**; being playable on a platform ≠ permission to edit, run ads or post cross-platform; the four checks are source, scope of authorization, proportion used, and commercial use | Secondary-creation copyright risk warning |
| Material ledger | Distinguish self-produced / client-supplied / platform template / licensed library / licensed music / downloaded from the internet, and keep order numbers and IDs | As above |
| Product links / music | An attached product must **match exactly** the brand and store the host recommended in the stream; platform built-in music is usually licensed for in-platform use only | Otherwise it becomes false advertising; see category 05 |
| Outsourcing and takedowns | Require the production vendor to hand over a material list, sources, scope of authorization and a replacement plan; a takedown ≠ the risk is over — keep the original video, publish time, play count, media-buying records and correspondence | As above |

---

## 7. Common pitfalls and anti-patterns

| Pitfall | Anti-pattern | Consequence | Fix |
|---|---|---|---|
| Cutting first, licensing later | Reposting a host's selling stream without authorization | Takedown, penalty points, account ban, damages | Authorization first; paperwork on file |
| Assuming attribution makes it legal | "Footage from XX's livestream" in the end credits | Still infringement | Written authorization covering all three rights |
| Trimming as-is / copying the on-screen text | Grabbing a section of the replay and posting it, reusing the host's subtitles | Flagged as homogeneous reposting, throttled | Deep secondary creation + new opening + rewritten subtitles |
| Unlicensed music / overstepping on watermark removal | Using platform trending songs in paid media, erasing rights-holder marks | Copyright complaints, aggravated infringement finding | Use a commercially licensed library; operate only within the authorized scope |

---

## 8. Pre-delivery checklist

- [ ] Authorization first: written paperwork covers copyright (including the rights of information network dissemination and adaptation), likeness and voice, with a traceable chain and reference numbers
- [ ] Specific authorization channels verified against the platform's latest rules (TO VERIFY items re-checked); material source ledger complete
- [ ] Product links match exactly the brand and store named in the host's delivery; "advertisement" labeled as required (where promotional)
- [ ] Music, fonts, images and meme stickers have commercial clearance on file
- [ ] Aspect ratio, frame rate and duration match the target platform; hook in the first 3 seconds; 15–60 s runtime (re-verified against the platform's latest official documentation)
- [ ] Highlight markers complete; flubs and dead air removed; 1.2–1.3× overall with key moments at original speed
- [ ] A cut every 3–5 s including reaction shots; slow motion 0.5–0.7×; 0.3–0.8 s of breathing room after each joke
- [ ] Kinetic text is **rewritten copy**; 1–2 light sound effects per shot; BGM below the original audio
- [ ] Voice −6 dB / music −12 dB, overall −14 to −12 LUFS at −1 dBTP (re-verified against the platform's latest official documentation)
- [ ] Deep secondary creation in place (new first 3 seconds, reordering, restructured shots, rewritten subtitles, 3-second head and tail cards)
- [ ] Watermark removal only within the authorized scope; danmaku and kinetic text free of discrimination, flame-baiting or false advertising
- [ ] Staggered by the 2h / 24h / 72h tiers; original video, publish time, play count, media-buying records and correspondence archived
- [ ] Legal / compliance review passed and archived (full regulations in the 05-copyright category)

---

## References

- Steps for producing livestream clips: https://www.wlcbw.com/jingdian/142107.html
- Copyright risk in secondary creation: http://xinlvlianlaw.com/insights/short-video-remix-copyright-risk.html
- Lawyer's analysis (Civil Code / Copyright Law / three-rights authorization): https://new.qq.com/rain/a/20261013A05L8000
- Clip compliance: https://weitoutiao.zjurl.cn/rogue/topic_share/?concern_id=1753066943312912
- Authorization and distribution management: http://znbo.com/post/6401.html
- Anime-style VFX in online variety shows: https://www.toutiao.com/article/6317763556193042690/
- Variety pacing with kinetic text and sound effects: https://post.smzdm.com/p/anvd2xw7/
- Post-production that amplifies the fun: https://so.html5.qq.com/page/real/search_news?docid=70000021_5346aeb09be57452
- Danmaku interaction: https://m.yule.360.com/content/4710821
- Platform loudness targets: https://www.databrush.com/article.php?id=516

Retrieved: 2026-11-10
