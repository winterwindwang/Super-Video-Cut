# Delivery QC Report Template (ready to copy and use)

> Category: Delivery QC | Topic: fillable templates for technical QC and compliance QC, plus batch field definitions | Compiled: 2026-11-10 | Applies to: item-by-item completion for a single project, or CSV-field ingestion across batch projects

> ⚠️ The licensing and compliance judgements in Tables C–G are production-process self-checks only and are not legal advice; high-risk projects must be reviewed by legal counsel, with a written conclusion attached separately.

> How to use: copy Tables A–G into your project notes or a spreadsheet and fill them in line by line. **Every "not applicable" needs a stated reason** — blanks are not allowed. Verdict symbols: `✅ pass` / `❌ fail` / `⚠️ to be confirmed` / `— not applicable`. Every `❌` must be closed out as "fixed + re-reviewer + re-review date" before release.

---

## Table A · Project and delivery information

| Field | Entry |
| --- | --- |
| Project name | |
| Final filename / version | `project_v03_20261110_1080p.mp4` |
| Delivered to / platform | |
| Source of the delivery specification | Delivery sheet / official platform documentation (attach link or screenshot) |
| Duration / aspect ratio / frame rate | |
| Export date / version of the encoding software | |
| Reviewer / review date | |
| Re-reviewer / re-review date | |
| Final verdict | ☐ Cleared for release ☐ Conditionally cleared ☐ Rejected, redo |

---

## Table B · Technical specifications (per `01-technical-spec-checklist.md`)

| # | Check | Required value | Measured value | Verdict | Notes / timecode |
| --- | --- | --- | --- | --- | --- |
| B01 | Container / video codec | | | | |
| B02 | Resolution / aspect ratio | | | | |
| B03 | Constant frame rate (r = avg) | | | | |
| B04 | Pixel format / bit depth | | | | |
| B05 | The three colour tags | | | | |
| B06 | Bitrate / GOP | | | | |
| B07 | Audio codec / sample rate / channels | | | | |
| B08 | Duration within ≤1 frame of the delivery sheet | | | | |
| B09 | Decode integrity: `-xerror` produces no output | | | | |
| B10 | Black-frame intervals confirmed manually | | | | |
| B11 | Freeze-frame intervals confirmed manually | | | | |
| B12 | Silence intervals confirmed manually | | | | |
| B13 | Integrated loudness | ___ LUFS | ___ LUFS | | Target: ___ ± ___ |
| B14 | True Peak | ≤ ___ dBTP | ___ dBTP | | |
| B15 | Speech band audible (300–3400 Hz) | | | | |
| B16 | A/V sync (6 spot checks, ≤2 frames) | | | | |
| B17 | Contact sheet free of goofs / out-of-frame content | | | | |
| B18 | First frame / thumbnail / ending | | | | |
| B19 | Target-platform upload preview passed | | | | |
| B20 | Whole film viewed at 1.0× | | | | |

---

## Table C · Asset and licensing ledger (per `02-content-and-compliance-review.md`)

| # | Asset description | Timecode in film | Source / URL / contract no. | Rights type | Licence scope (commercial · territory · term · platform) | Evidence location | Credit required | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C01 | | | | Picture | | | | |
| C02 | | | | Music · composition | | | | |
| C03 | | | | Music · recording | | | | |
| C04 | | | | Sound effect / sample | | | | |
| C05 | | | | Font | | | | |
| C06 | | | | Likeness / voice | | | | |
| C07 | | | | Film clip / quotation in a derivative work | | | | |
| C08 | | | | AI-generated material | | | | |

> Quotation in a derivative work must also record: total quoted duration ___ sec / total film duration ___ sec = ___%; share of original commentary and criticism ___%; author and title of the work identified ☐ Yes ☐ No; does it substantially substitute for the original ☐ Yes ☐ No.

---

## Table D · Content compliance

| # | Check | Verdict | Basis / notes |
| --- | --- | --- | --- |
| D01 | No absolute claims, false claims or unsourced data | | |
| D02 | Sector qualifications and permitted wording (healthcare / finance / education etc.) | | |
| D03 | Names and job titles, times and places, quotations, fact-checking | | |
| D04 | Editing has not changed what the interviewee meant / staged scenes are labelled | | |
| D05 | Private information handled: faces, plates, door numbers, chat logs | | |
| D06 | Consent for minors on camera and advertising-endorsement restrictions | | |
| D07 | No watermarks / copyright notices / rights management information removed | | |
| D08 | Trademark and brand exposure carries no infringement risk | | |
| D09 | Maps and national-boundary labelling compliant | | |
| D10 | AI-generated / deep-synthesis content labelled and declared | | |
| D11 | Platform rules on derivative works, off-platform traffic and engagement bait complied with | | |
| D12 | Cross-border release: territorial music licensing / DMCA / GDPR | | |
| D13 | End credits carry copyright, production, thanks and disclaimer | | |

---

## Table E · Subtitles and accessibility

| # | Check | Verdict | Notes |
| --- | --- | --- | --- |
| E01 | Full proofread: typos / terminology / numbers and units / punctuation | | |
| E02 | Timeline has no overlaps, no out-of-order cues, last cue within film length | | |
| E03 | Characters per cue and dwell time within limits; no cue broken across a hard cut | | |
| E04 | Burned-in subtitles inside the safe area, not covered by UI, contrast sufficient | | |
| E05 | Bilingual translation accurate; language tags and track naming correct | | |
| E06 | SDH: speaker identification and key sound-effect description | | |
| E07 | Important information not conveyed by colour alone / by sound alone | | |

---

## Table F · Full-viewing problem log

| # | Timecode | Category (picture / sound / subtitles / pacing / compliance) | Problem description | Severity (blocking / minor / suggested) | Action taken | Fix version | Reviewer / date |
| --- | --- | --- | --- | --- | --- | --- | --- |
| F01 | | | | | | | |
| F02 | | | | | | | |
| F03 | | | | | | | |

> Severity definitions: **blocking** = must be fixed before release (a typo in the title, A/V sync drift, infringing material, a black screen); **minor** = affects the experience but the film can be released with conditions; **suggested** = an optimisation.

---

## Table G · Risk grading and sign-off

| Risk level | Count | Item IDs | Disposition |
| --- | --- | --- | --- |
| 🔴 Red (blocking) | | | Must be 0 before release |
| 🟡 Amber (to be confirmed) | | | Requires a written conclusion from legal counsel / the owner |
| 🟢 Green (passed) | | | File the ledger and evidence |

| Sign-off | Name | Date | Notes |
| --- | --- | --- | --- |
| Technical QC | | | |
| Content compliance review | | | |
| Legal review (required for high-risk projects) | | | |
| Final release approval | | | |

**Archive checklist**: ☐ Final film ☐ Project file and font / plug-in versions ☐ Asset ledger ☐ Licence evidence ☐ This QC report ☐ Automated check logs (`qc_scan.sh` output) ☐ Frame-extraction contact sheets

---

## CSV field definitions for batch projects

When several projects run in parallel, load the review results into a database. Suggested fields (one row per film):

```csv
project_id,filename,version,platform,review_date,reviewer,duration_sec,width,height,fps,codec,pix_fmt,integrated_lufs,true_peak_dbtp,decode_ok,black_flag,freeze_flag,silence_flag,a_v_sync_ok,subtitle_ok,rights_cleared,compliance_ok,risk_red,risk_yellow,final_verdict,fix_version,signoff,notes
```

Field conventions: `*_ok` / `*_flag` take `1/0/NA`; `final_verdict` takes `pass / conditional / reject`; every `NA` must be paired with a `notes` entry explaining why.

---

## Appendix: automated detection script

`qc_scan.sh` in the same directory runs specification export, decode integrity, black-frame / freeze-frame detection, silence, loudness and frame-extraction contact sheet in one pass, and works out for itself whether an audio track exists:

```bash
bash "scripts/qc_scan.sh" "D:/output/final_v03.mp4" "D:/output/qc_logs"
```

Output: `*.probe.json`, `*.qc.log`, `*.sheet.png`. **The script covers only the automated part of Table B**; Tables C–G must be completed by hand.

---

## References

- `01-technical-spec-checklist.md` and `02-content-and-compliance-review.md` in this knowledge base
- `../01-editing-craft/03-editing-workflow-and-project-standards.md` (project archiving and version naming)
- `../05-copyright/` (rights types and review basis for the licensing ledger)
- FFmpeg official documentation: https://ffmpeg.org/documentation.html

Retrieved: 2026-11-10.
