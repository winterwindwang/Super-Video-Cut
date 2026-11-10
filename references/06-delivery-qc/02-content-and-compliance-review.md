# Content and Compliance Review (Editorial & Compliance QC)

> Category: Delivery QC | Topic: rights ownership, content compliance, subtitle copy and publication risk review | Compiled: 2026-11-10 | Applies to: any film released publicly or used commercially; run in parallel with the technical review in `01-technical-spec-checklist.md`

> ⚠️ This document is a self-check reference for the production process and is not legal advice. Statutes, judicial interpretations and platform rules change; high-risk or commercial projects must be reviewed by legal counsel. Full statutory text and case law are in `../05-copyright/`.

---

## 1. Why this gate has to exist on its own

Technical QC answers "can this file play"; content review answers "**may it go out, and what happens if it does**". Neither covers the other: a film with flawless picture and sound at a compliant loudness can still be taken down, sued or administratively penalised over one unlicensed BGM track, one unmasked passer-by's face, or one absolute claim.

Run the review twice, both times early: **a rights pre-check as soon as the rough cut is locked** (replacing an asset is cheapest at that point), and **a final review before the master is exported**.

---

## 2. Rights and licensing-chain review

### 2.1 Build an asset ledger

Every external asset that appears on the timeline must be able to answer five questions. Missing any one of them is a red blocking item:

| Field | Description |
| --- | --- |
| Asset source | Specific site / shooter / licensor, precise to a URL or contract number |
| Rights type | Picture, music (three layers: composition + recording + performance), sound effects, fonts, likeness, voice |
| Scope of licence | Commercial / non-commercial, territory, term, platform, whether derivative edits are permitted, whether sublicensing is permitted |
| Evidence of licence | Licence agreement, invoice, download record, screenshot of the platform music library (with timestamp) |
| Credit and attribution | Whether credit is required, whether copyright notices / watermarks must be retained |

### 2.2 Item-by-item checklist

- [ ] **Music**: are composition copyright, phonogram producer's rights and performer's rights each covered; does the platform library restrict use to "this platform only / non-commercial"; does the licence term cover the publication window; does cross-border release run into a territorial block.
- [ ] **Sound effects / samples**: confirm the licence at source; royalty-free ≠ copyright-free; satisfy the BY / NC / ND / SA conditions of the CC licence one by one (whether affiliate selling or revenue sharing counts as commercial use under NC is disputed).
- [ ] **Film and other people's footage**: does the use fall within "appropriate quotation"; are the author's name and the title of the work indicated; does it substantially substitute for the original; clip-and-repost compilations that add no new expression carry the highest risk.
- [ ] **Images / fonts**: whether a single glyph constitutes a work of fine art is judicially disputed, so commercial fonts must always be licensed for commercial use; does the stock licence cover video use and the distribution volume you need.
- [ ] **Likeness / voice / privacy**: written consent from everyone on camera (covering use, term, territory and whether it may be used in advertising); passer-by faces and identifiable plates / door numbers / phone numbers must be masked; minors on camera require guardian consent plus attention to advertising-endorsement restrictions.
- [ ] **Rights management information**: **watermarks, copyright notices and metadata must not be removed or covered** — stripping rights management information is itself an independent ground of infringement.
- [ ] **AI-generated content**: licensing of the training / cloning material, the person's own consent for voice cloning, the labelling obligation for generated content, and platform declaration requirements for AI content.
- [ ] **Brands and trademarks**: whether incidental exposure of a competitor's logo or product packaging would be treated as trademark use; do not use another party's trademark as the title or as the key thumbnail visual.

### 2.3 Risk grading

| Level | Test | Handling |
| --- | --- | --- |
| 🔴 Red | Core asset with no licence evidence, clip-and-repost, watermark removal, minors without consent, plainly absolute claims | **Block release**; replace the asset or obtain a licence and review again |
| 🟡 Amber | Ambiguous licence scope, territorial limits on a platform music library, a high proportion of quoted third-party material, unlabelled AI content | Legal confirmation / add labelling / reduce the quoted proportion; keep a written conclusion |
| 🟢 Green | Own footage + licensed assets + a complete ledger | File the ledger and the evidence; pass |

---

## 3. Content compliance review

| Dimension | Checks | Related documents |
| --- | --- | --- |
| Advertising and marketing | Absolute claims ("best", "first", "national-level" and the like), false claims, efficacy assertions, sourcing of data and quotations, comparative advertising, sector qualifications for healthcare / finance / education | `../04-genre-playbooks/03-ads-and-brand-films.md`, `../05-copyright/` |
| Fact-checking | Names and job titles, times and places, figures and units, whether quotations are taken out of context, sources and statistical basis for chart data | — |
| Editing ethics | Whether cutting changes what the interviewee meant; whether lines from different times or occasions are spliced into one sentence; whether staged scenes are labelled; whether sync sound and picture are mismatched | `../04-genre-playbooks/02-interview-documentary-and-portrait.md` |
| Privacy and personal information | Identifiable information such as faces, names, staff badges, courier labels, chat logs, location data, medical records | `../05-copyright/04-likeness-fonts-stock-and-personality-rights.md` |
| Platform rules | Platform-specific rules on derivative works, reposting, engagement bait, off-platform traffic and medical / financial content; rules change, so check the latest official text before publishing | `../05-copyright/05-platform-rules-and-cross-border-compliance.md` |
| Maps and markings | When maps appear, use compliant base maps and correct national-boundary labelling | Per current surveying and map administration requirements |
| Minors | Consent for appearing on camera, use of their image, prohibition on acting as advertising endorsers, no school badges or home addresses on screen | `../05-copyright/04` |
| Cross-border release | Territorial music licensing, DMCA / Content ID, Article 17 of the EU DSM Directive, data export and GDPR | `../05-copyright/05` |
| AI labelling | Prominent marking and explicit disclosure for generative / deep-synthesis content, platform declaration | Re-check against current rules such as the Interim Measures for the Administration of Generative AI Services (《生成式人工智能服务管理暂行办法》) and the Provisions on the Administration of Deep Synthesis of Internet Information Services (《互联网信息服务深度合成管理规定》) |

---

## 4. Subtitle, copy and accessibility review

- [ ] Full subtitle proofread: typos, characters with multiple readings, consistent names and terminology, numbers and units, spacing between Chinese and Latin text, punctuation.
- [ ] Timeline: no overlaps, no out-of-order cues, minimum dwell time met, last cue within the film length, no cue split across a hard cut.
- [ ] Bilingual / multilingual: translation accurate, no cultural misreading, language tags correct (ISO 639), track naming unambiguous.
- [ ] Accessibility: do SDH captions identify speakers and key sound effects; is contrast sufficient; is important information conveyed by colour alone or by sound alone.
- [ ] On-screen text: validity period and scannability of titles, kinetic typography, corner bugs and QR codes; nothing in the vertical-video UI safe area is covered.
- [ ] End credits: copyright notice, production company, licences and thanks, and disclaimer are all present and on screen long enough to read.

---

## 5. Review workflow and record-keeping

```
Rough cut locked
  → ① Export the asset ledger and check licence evidence line by line (rights pre-check)
  → ② Content compliance self-check (advertising wording / facts / privacy / platform rules)
  → ③ Subtitle and copy proofread + accessibility check
  → ④ Technical QC (see 01)
  → ⑤ Risk grading: red items block / amber items need a written conclusion / green items pass
  → ⑥ Fill in 03-qc-report-templates.md, recording reviewer, date, version number and conclusion
  → ⑦ Archive: final film + project + asset ledger + licence evidence + QC report, kept together
  → ⑧ After publication, re-check against platform feedback (takedown / throttling / copyright claim)
```

**Record-keeping requirement**: every conclusion must exist as a written record. "Someone said it was fine" is worth nothing in a dispute. Licence evidence and QC reports should be retained for no less than the publication cycle of the work plus the period in which a dispute can still be brought.

---

## 6. Common errors and troubleshooting

| Symptom | Root cause | Fix |
| --- | --- | --- |
| Used a platform's "free for commercial use" music and still received a claim | The library licence is limited to that platform / to non-commercial use / the account holder does not match | Re-read the library agreement in full, switch to a licence that covers commercial use across platforms, and keep the evidence |
| Derivative work judged infringing | Quoted proportion too high, no attribution, substantial substitution for the original | Raise the share of original commentary, shorten the quotes, make the attribution and the critical purpose explicit; if it is still high-risk, do not use it |
| Interviewee complains "that is not what I meant" | Splicing across sentences changed the meaning | Restore the context or re-record, and get the interviewee's written approval of the finished film |
| Received a demand letter over a font | Used a font library without buying a commercial licence | Switch to an open-licensed font (e.g. SIL OFL) or buy the licence |
| Privacy complaint over a passer-by's face | Identifiable and not masked | Blur it or obtain consent; street photography is not automatically exempt |
| Ad rejected by the platform | Absolute claims / missing qualifications | Compare the copy sentence by sentence against prohibited wording and supply the sector qualification documents |
| Level squashed or subtitles lost after publishing | Only the file was checked, not the platform | Verify with an upload preview; see L4 in `01-technical-spec-checklist.md` |
| Review was done but cannot be evidenced | No ledger, no signed record | Mandate `03-qc-report-templates.md` and archive it |

---

## 7. Final-gate quick check (print and pin to the wall)

- [ ] Asset ledger complete; every external asset has licence evidence
- [ ] All three layers of music rights checked, along with platform / territory / term limits
- [ ] No watermark removal, no unauthorised likeness / voice / private information
- [ ] Quotation in derivative works meets appropriate-quotation and attribution requirements, and does not substitute for the original
- [ ] No absolute claims, no unsourced data, no out-of-context quotation
- [ ] Subtitles proofread in full, timeline valid, accessibility acceptable
- [ ] AI-generated content labelled and declared under the rules currently in force
- [ ] Copyright and licensing statements complete in the end credits
- [ ] Risk grading finished: red items at zero, amber items carry a written conclusion
- [ ] QC report filled in and signed, archived with the project
- [ ] High-risk projects reviewed by legal counsel

---

## References

- National Copyright Administration (国家版权局) — discussion of short-video derivative works and fair use: https://www.ncac.gov.cn/xxfb/ztzl/2021zgwlbqbhdh/pthd/dspbqbhdtzyxtzl/jbgd_961/202106/t20210610_53612.html
- National Copyright Administration (国家版权局) — strict separation of infringement from fair use: https://www.ncac.gov.cn/xxfb/ztzl/2021zgwlbqbhdh/pthd/dspbqbhdtzyxtzl/jbgd_961/202106/t20210610_53615.html
- Legal Daily (《法治日报》) — "Film and TV re-edits and clip videos: infringement or fair use": https://www.legaldaily.com.cn/sylm/content/2021-11/19/content_8631293.html
- National People's Congress (中国人大网) — Copyright Law of the People's Republic of China (《中华人民共和国著作权法》): http://www.npc.gov.cn/
- All five documents in this knowledge base under `../05-copyright/` (article-by-article statute text, cases, and the 51-item TO VERIFY list)
- W3C WCAG 2.2 (accessibility): https://www.w3.org/TR/WCAG22/
- DCMP Captioning Key (accessible captions): https://dcmp.org/learn/captioning-key

Retrieved: 2026-11-10 | Currency: to be re-verified. Statutes and platform rules are subject to the latest official texts; this document is not legal advice.
