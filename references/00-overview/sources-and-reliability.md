# Sources, reliability grades and the TO VERIFY register

> Category: Overview | Topic: how the library was built, source grading, the consolidated TO VERIFY register and review priority | Compiled: 2026-11-10 | Applies to: judging the evidence grade of any figure or conclusion before citing it

> ⚠️ This library is **reference material for creative work** — not legal advice, not the text of a standard, not a platform's official rules. Any decision about licensing, compliance or delivery specifications must go back to the primary text and the current official document.

---

## 1. How the library was built

- **Retrieval date**: 2026-11-10 (recorded uniformly at the end of every document).
- **Method**: work was split across six capability domains, each with repeated targeted WebSearch / WebFetch passes; the legal domain received ≥3 searches per document, with a mandatory preference for primary government, court and standards-body sources.
- **Volume**: about 100 searches, 50 documents, about 550,000 characters including tables and code, and more than 180 source domains; plus 3 scripts that were actually run (2 Bash + 1 Python).
- **Command verification**: every ffmpeg / ffprobe example was verified on this machine under **ffmpeg 8.1.2**; `../scripts/qc_scan.sh` was run end to end against real MP4 files (producing probe.json / qc.log / sheet.png).
- **Writing conventions**: factual conclusions carry an accessible URL; standards and statutes are cited with number and edition; anything that cannot be checked against a primary source is marked TO VERIFY; rule-of-thumb values are labelled as starting suggestions.

---

## 2. Source reliability grades

| Grade | Definition | Typical examples in this library | How to use it |
| --- | --- | --- | --- |
| **A — primary authority** | Statutory text, the body of a standard, material published by a government, court or standards body | `npc.gov.cn`, `gov.cn`, `ncac.gov.cn`, courts at every level, `chinacourt.cn`, the official EBU R 128 and Tech 3341-3344 PDFs, ITU-R BS.1770, ATSC A/85, W3C WebVTT and WCAG 2.2, SMPTE, EUR-Lex, the US Copyright Office, the full text of the SIL OFL | May be cited as authority directly, but the edition in force still has to be confirmed |
| **B — vendor or project official** | Official documentation from software, platforms, tools and licensors | `ffmpeg.org`, `adobe.com` / `helpx.adobe.com`, `support.apple.com`, `partnerhelp.netflixstudios.com`, `support.google.com`, `blog.youtube`, `pbs.org`, `oceanengine.com`, `training.tencentads.com`, `opentimeline.io`, `aegisub.org`, `pixabay.com`, `pexels.com`, `dcmp.org` | Parameters and procedures are trustworthy; versions, pricing and platform rules change, so re-check before use |
| **C — authoritative industry, academic or press** | Institutional research, court public-education material, trade press, university scholars | `downloads.bbc.co.uk` (BBC R&D WHP 202), `legaldaily.com.cn`, `ip.people.com.cn`, `thepaper.cn`, articles by scholars at the Communication University of China (中国传媒大学), `americancinemaeditors.org`, `eizo.com.cn` | Good for understanding how a figure is defined and which way case law tends; **no substitute for the statute or the judgment itself** |
| **D — third-party tutorials, roundups, reviews** | Blogs, content farms, second-hand compilations, commercial reviews | ffmpeg tutorial sites of every kind, second-hand subtitle-specification compilations, software pricing roundups, TTS parameter comparisons, WeChat Official Account articles | **Starting reference only**; every figure derived from this grade is marked TO VERIFY in this library |

**The key warning**: the easy-to-remember numbers most often quoted from this library — transition frame counts, J/L-cut offsets, EQ and compression ranges, subtitle CPS, BPM ranges, per-platform bitrate and loudness targets, software pricing — are **mostly grade C/D rule-of-thumb values**, not written standards. They are fine as a starting point for tuning and unsuitable as acceptance criteria. The only things that can serve as acceptance criteria are grade A standards (EBU R 128, for instance) and the written delivery sheet from the client or platform.

---

## 3. Source profile by domain

| Directory | Dominant source grade | High-frequency domains | TO VERIFY items (approx.) |
| --- | --- | --- | --- |
| `01-editing-craft` | B (Adobe / Apple / SMPTE / OTIO / ITU) + D rule-of-thumb values | adobe.com, pub.smpte.org, itu.int, support.apple.com, partnerhelp.netflixstudios.com | 23 |
| `02-audio-and-voice` | **A** (EBU / ITU / ATSC / BBC / PBS) + D | tech.ebu.ch, itu.int, atsc.org, downloads.bbc.co.uk, bento.pbs.org, ffmpeg.org | 25 |
| `03-subtitles` | **A/B** (W3C / WCAG / DCMP / BBC / ffmpeg) + C second-hand compilations | w3.org, dcmp.org, bbc.co.uk, ffmpeg.org, aegisub.org, nikse.dk | 20 |
| `04-genre-playbooks` | B (Ocean Engine / Tencent Ads / Google Ads / PBS) + C/D rule-of-thumb values | oceanengine.com, training.tencentads.com, support.google.com, helpx.adobe.com, pbs.org | 30 |
| `05-copyright` | **A** (NPC / State Council / National Copyright Administration / courts / EU / US) + C paraphrase | npc.gov.cn, gov.cn, ncac.gov.cn, bjinternetcourt.gov.cn, chinacourt.cn, eur-lex.europa.eu, copyright.gov | **51** |
| `06-delivery-qc` | A (EBU / ITU) + B (ffmpeg official) + local measurement | ffmpeg.org, tech.ebu.ch, yololab.net, huntapi.com | 8 (threshold rule-of-thumb values) |
| `07-tools-and-resources` | B (full official licence texts) + D (pricing and reviews) | openfontlicense.org, pexels.com, pixabay.com, github.com, umatechnology.org | 11 |
| `08-rsi` | A/B (standards and official sources) + C (academic) + D (governance trade articles and preprints) | ffmpeg.org, aaltodoc.aalto.fi, papers.iafor.org, cdn.aaai.org, arxiv.org, ncac.gov.cn, ccct.net.cn | about 12 (self-evolution parameters and probe thresholds) |
| `09-material-memory` | **B (vendor documentation)** + C/D (cache engineering patterns, metadata standards surveys) | ai.google.dev, firebase.google.com, ffmpeg.org, msi.dublincore.org, nedcc.org, lobehub.com, arxiv.org | about 6 (conflicting token figures, sampling-hash blind spots, estimation thresholds) |

That is about **186 TO VERIFY items** in total, each listed and explained in the body or at the end of the relevant document, with the point of dispute stated. This is deliberate: **making uncertainty explicit is worth more than a wrong number that looks certain**.

**The evidence position of volume `09`**: the `mdc-v1` fields, the V1–V8 validation, the cache state machine and the accounting conventions are **all conventions defined by this library** (they borrow the asset/instantiation layering idea from EBUCore and PBCore, but are not an implementation of either); the video input token rate can only be taken from vendor documentation (grade B), and the vendors themselves give both `100/300 tok/s` and `263 tok/s`; on top of that there are volatile parameters such as 1 FPS sampling, the context-cache TTL and the minimum token threshold. The `sampled` hash in `material_cache.py` covers only 6 MiB, so in theory a change in the unsampled region can be missed — a **known engineering trade-off**, which is why delivery-grade material must go through `--full` plus `verify`. Every `stats` figure is an estimate and must never be treated as an invoice.

**The evidence position of volume `08`**: the judging criteria and compliance boundaries of its three-dimension evaluation follow the grade A/B sources used in volumes 01–07; but the **self-evolution algorithm** (η, δ, N_min, decay, tolerances, sample sizes, gate thresholds) has **no written industry standard** — these are all initial values set by this library, drawn mostly from 2026 trade articles and arXiv preprints (grade D methodological reference). They exist to make the process runnable and **must not be treated as validated optimal parameters**; recalibrate and record after every real case. Likewise, `scene > 0.25` and `silence −40 dB` in `reference_probe.sh` are starting thresholds — fast pans and flashes will trigger them falsely, so always cross-check against a frame-extraction contact sheet.

---

## 4. Review priority

### P0 — affects legal conclusions or delivery compliance; verify before citing

1. **The number of circumstances in Article 24 of the Copyright Law (《著作权法》)**: the 2020 text actually lists **13 items** (12 specific items plus item (13) as a catch-all), while some official commentary still uses the older wording of "12 categories". This library follows the statutory text and lists 13. → Check the current text at `npc.gov.cn`.
2. **How the implementing regulations line up**: the Regulations for the Implementation of the Copyright Law (《著作权法实施条例》, 2013 revision) and the Regulations on the Protection of the Right to Network Dissemination of Information (《信息网络传播权保护条例》, 2006/2013) were not updated in step with the 2020 amendment; how their article numbers and their wording of the "three-step test" now apply remains to be settled, and the progress of the draft revision of the implementing regulations is still TO VERIFY.
3. **Platform agreements and music-library terms**: the copyright, derivative-work and "this platform only / non-commercial only" restrictions attached to the music libraries of Douyin (抖音), Kuaishou (快手), Bilibili (B站) and Channels (视频号) come, in this library, mostly from court and rights-body public-education material; **the current agreement text of each platform has not been checked clause by clause**. These rules change often.
4. **The original judgments in the leading cases**: the "movie in stills" case (图解电影案), the "Calabash Brothers" case (葫芦娃案), the typeface cases (including 九层妖塔), the AI text-to-image and voice-infringement cases, and the Ultraman case (奥特曼案) — case numbers, parties and damages come largely from media reports, and **the judgments themselves were not obtained**, so they must not be cited directly as authority.
5. **First-hand check of the Civil Code (《民法典》) article numbers**: portrait rights, voice rights, the fair-use boundary in Article 1020, how an already released film is handled once authorisation is withdrawn under Article 1022, and Articles 1018–1023; plus Article 13 of the Personal Information Protection Law and the cross-border data rules that start at Article 38.
6. **AI regulation and cases**: the specific provisions on labelling, portrait and voice consent and platform duties in the Interim Measures for the Administration of Generative AI Services (《生成式人工智能服务管理暂行办法》) and the Provisions on the Administration of Deep Synthesis of Internet Information Services (《互联网信息服务深度合成管理规定》); Article 50 of the EU AI Act; the current status of the NO FAKES Act; and the case numbers of AI cases.
7. **Loudness standards: editions and distribution conventions**: ATSC A/85 has a new edition approved in 2026-07 (this library relies on A/85:2013); the −3 dBTP distribution-stage figure in EBU Tech 3344 comes from secondary material; the streaming targets are a summary table rather than any platform's own specification.
8. **Advertising compliance conventions**: the prohibited terms of the Advertising Law, the qualification requirements for special industries, and the penalty ranges (phrasing such as CNY 200,000–1,000,000) all need re-checking against the current text and the market regulator's guidance.
9. **Asset and font licensing**: Pexels / Pixabay / Unsplash are frequently mislabelled as CC0 when their official licences are their own Content Licence; whether a single glyph counts as a work of fine art; the commercial-use scope of Source Han Sans (思源), Microsoft YaHei (微软雅黑) and Founder (方正); and whether content already published stays covered after a music-library subscription lapses.
10. **Platform technical specifications**: resolution, bitrate, maximum duration, portrait safe area and loudness targets conflict sharply between sources (Douyin's duration and bitrate and Channels' duration, for example), so **the platform's own creator documentation plus an actual upload test** must decide.
11. **The compliance boundary of style transfer** (volume `08`): where the idea/expression dichotomy actually falls when "imitating a hit video's style", and how AI stylisation and the reproduction of shot choreography should be characterised, rest today on expert opinion and public legal education material only, with **no dedicated judicial interpretation**; this library takes the strict line (migrate parameters only). Commercial projects must go through legal review.
12. **RSI governance and algorithm parameters** (volume `08`): η=0.05, δ=0.1, N_min=5, decay=0.9, a 7-day cooldown, the size of the regression and holdout sets, the L4 deviation tolerance and the 0.25 scene-cut threshold are **all initial values set by this library, with no written standard and no empirical validation**. The governance method comes mostly from 2026 trade articles and arXiv preprints. Recalibrate and record after every real case; no rule change may be approved until a frozen regression baseline exists.
13. **Video-model tokens and caching conventions** (volume `09`): about 100 tok/s for static low-resolution and about 300 tok/s for high-resolution input (Google, "Video understanding"), with Firebase giving a further 263 tok/s; a minimum context-cache input of 2048/4096 tokens, a default TTL of 1 hour, explicit caching unsupported on some newer models, and the retention period for Files API uploads — **all of these vary widely between vendors and model versions and change often**. The `1 − 1/N` saving formula, the 6 MiB sampled hash, "one timecode anchor every 15–30 s" and the V1–V8 thresholds are all set by this library and rest on no industry standard. Always take usage from the `usage_metadata` in the response.

### P1 — affects tool selection and budget; review periodically

Software pricing and versions (Premiere / Resolve Studio / FCP / Avid / Vegas), hardware thresholds (VRAM / RAM / NAS / monitor gamut), TTS engine metrics and free tiers, the specific figures in the Netflix subtitle specification (CPS, characters per line, sync frames — secondary sources contradict each other), the release status of Aegisub / Subtitle Edit, how courts read the NC condition of Creative Commons licences, and collective management organisation rosters and tariff schedules.

### P2 — rule-of-thumb starting values; calibrate per project

Transition frame counts, 8–24 frame J/L-cut offsets, B-roll handles of ≥12 frames, EQ / compression / ducking ranges, BPM and level hierarchy, the emotion-curve-to-shot-duration mapping, characters per subtitle line and reading speed, joke frequency and how fast a clip should go out, and the three-act timing of a short film. None of these has **a written standard**; tune them by ear and eye, and never use them as acceptance criteria.

---

## 5. How to verify

| What to check | Where to check it |
| --- | --- |
| Statutory text | The NPC website (中国人大网) `npc.gov.cn`, the State Council website (中国政府网) `gov.cn`, the National Copyright Administration (国家版权局) `ncac.gov.cn`, and the websites of the Supreme People's Court and the lower courts |
| The body of a standard | ITU `itu.int`, EBU `tech.ebu.ch`, SMPTE `pub.smpte.org`, ATSC `atsc.org`, W3C `w3.org` |
| Subtitle and encoding tools | The `ffmpeg.org` documentation plus a local test with `ffmpeg -h filter=<name>` |
| Platform specifications | The platform's own creator academy or help centre plus an actual upload-preview test (**do not rely on third-party roundups**) |
| Asset licensing | The stock site's own full licence text (**not** a third-party "free for commercial use" collection), and keep a timestamped screenshot plus the agreement |
| Case law | China Judgements Online (中国裁判文书网) / court websites / court gazettes; capture the case number and whether the judgment is in force |
| Music rights | Official announcements from MCSC (音著协) and CAVCA (音集协), and the original licence contract |
| Video-model tokens and caching | The vendor's current official documentation (for example `ai.google.dev/gemini-api/docs/video-understanding`, `docs/caching`) plus a measured `usage_metadata` response; **do not rely on third-party roundups** |
| Material description and cache conventions | `09-material-memory/01` and `02` in this library (library-defined conventions); EBUCore/PBCore are a reference for the layering idea only, not the basis of this implementation |

Once you have verified something, append a line to this file: `date | item | conclusion | source URL`, and update the matching TO VERIFY marker in the relevant document. **Never delete the original TO VERIFY item** — keep the trail of judgement.

---

## 6. Disclaimer and maintenance

- This library does not constitute legal advice; consult a qualified lawyer for high-risk or commercial projects.
- Platform rules, software pricing, AI service terms, statutes and judicial interpretations change; re-check the current official text before citing.
- TO VERIFY items are never deleted; conclusions and dates are appended.
- When you add a document, update the routing table in `../SKILL.md` and `manifest.csv` at the same time; when you edit a document, update its `Compiled` field.
- Suggested review cadence: P0 items before every use; P1 items quarterly; P2 items calibrated per project.

---

## References

The full source URLs for each domain are listed in the References section at the end of the corresponding document; entry points to primary sources are in the table above.
Retrieved: 2026-11-10.
