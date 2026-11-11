# Keyframe Baseline and Structural Diff

> Category: RSI self-improvement | Topic: recording per-shot keyframe anchors for a reference video, then diffing the finished cut against them | Compiled: 2026-11-11 | Applies to: S2 (baseline extraction) and M5 (post-cut comparison)

> ⚠️ This document is a reference for the creative workflow and **does not constitute legal advice**; mark every threshold here as TO VERIFY until it has been calibrated on real cases.

---

## 1. Why a fingerprint is not enough

A style fingerprint stores parameters derived from the reference: median shot length, cut density, loudness, transition mix. Those numbers survive the cut, but they cannot answer a question that arrives immediately afterwards: **did the finished cut actually land in the same places?**

Two cuts can share a 1.8 s median and still feel different, because the median says nothing about *which* shot got long and which got short. The keyframe baseline closes that gap: it records one anchor per shot plus the objective image statistics at three positions inside that shot, so the finished cut can be diffed shot by shot instead of argued about.

The idea is simple — record the reference's frame-level structure once, then compare mechanically after cutting, rather than re-watching both films and trusting memory.

---

## 2. The decisive constraint: never compare pixels

The reference and the finished cut are made from **different footage**. A pixel diff, a perceptual hash distance or an SSIM score between them is meaningless: it will flag every legitimate difference and stay silent about real drift. Anyone who has tried knows the failure mode — 20% similarity, and no idea what to do with that number.

So the baseline stores two different kinds of thing, and only one of them is compared automatically:

| Stored | Compared | Why |
| --- | --- | --- |
| Shot boundaries, durations, cut positions | **Yes, automatically** | Structure is what was borrowed; it must match |
| Per-shot luma / saturation / colour cast | **Yes, but as a distribution** | A systematic shift indicates a grade problem; a per-shot shift is usually just different content |
| The keyframe images themselves | **No — shown side by side for a human** | Composition, shot size and subject placement cannot be judged by a number |
| Anything in the frame (subject, props, faces) | **No** | Different footage by definition; comparing it is a category error |

The paired sheet exists precisely because the last two rows cannot be automated. The tool's job is to point at the rows worth looking at, not to pretend it can see.

---

## 3. What gets recorded

`scripts/keyframe_diff.py extract <video> --out <dir>` writes:

| File | Content |
| --- | --- |
| `shots.csv` | One row per shot: index, in/out, duration, luma at 15/50/85% of the shot, mid-shot luma / saturation / U / V, keyframe path, plus **three empty columns for a human** |
| `kfs.json` | Source path, duration, fps, cut times, scene threshold, sampling offsets, ffprobe output, tool version |
| `frames/mid/shotNNN.png` | The mid-shot keyframe of every shot, scaled to 240 px wide |
| `kfs_sheet.png` | All mid-shot keyframes stacked top to bottom, one row per shot — the reference's visual index |

The three human columns are `shot_size`, `composition`, `note`. The tool measures; it does not interpret. A shot is `CU` because a person looked at it and said so, and the diff can only compare shot-size sequences once those columns are filled on both sides.

**Sampling rule:** samples sit at 15%, 50% and 85% of each shot, never at fixed absolute times. This keeps the comparison meaningful when shot lengths differ slightly — a 1.2 s shot and a 1.4 s shot are still sampled at their own head, middle and tail.

Scene detection uses `select='gt(scene,0.25)'`, the same threshold as `reference_probe.sh`, so the cut list is identical whether you get it from the probe or from this tool. Pass `--cuts` to reuse an existing `cuts.txt` and skip detection entirely.

---

## 4. How the diff is judged

`compare` aligns the two baselines by shot index after normalising both timelines to the same length, then reports three tiers. Exit code is **2 when anything blocking is found**, `0` otherwise, so it can gate a pipeline.

| Tier | Code | Condition | Meaning |
| --- | --- | --- | --- |
| **BLOCK** | `T1-duration` | Runtime differs by >2% | The cut is a different length; every downstream comparison is unreliable |
| **BLOCK** | `T1-shotcount` | Shot count differs by >15% | The structure is different, not merely the timing |
| **BLOCK** | `T1-cutdrift` | A cut lands >0.32 s (≈8 frames at 25 fps) from the reference position after normalisation | The rhythm broke at that point |
| WARN | `T1-cutdrift` | >0.16 s (≈4 frames) | Watch it; may be acceptable for a different edit |
| WARN | `T2-median` | Median shot length drifts >25% | Overall pacing moved |
| WARN | `T2-density` | Cut-density curve correlation < 0.70 | The *shape* of the pacing differs — dense where the reference was slow |
| WARN | `T2-luma` | Median luma shifts >15% | Systematic, so suspect grade / LUT / transfer function before blaming content |
| WARN | `T2-saturation` | Median saturation shifts >20% | Same reasoning |
| WARN | `T2-cast` | Mean U or V shifts >6 units | White balance pushed towards blue or red |
| WARN | `T2-lumatrend` | Luma trend direction flips across the clip | The reference darkens while the cut brightens (or the reverse) |
| WARN | `T3-shotsize` | Shot-size sequence diverges (only if both sides are annotated) | Assembly logic differs |
| INFO | `T3-spread` | Always: the three largest per-shot luma gaps | Prompts you to look at those rows; content normally differs |
| INFO | `T3-annotation` | `shot_size` empty on either side | That check was skipped |

**A deliberate asymmetry:** image statistics are judged on the *median across shots*, not shot by shot. Per-shot luma differences are dominated by content — shot 3 of the reference is a night exterior, shot 3 of your cut is a bright interior, and neither is wrong. Only a systematic shift across the whole clip is evidence of a real problem. This is the difference between a tool people trust and one they learn to ignore.

Thresholds above are starting values with no empirical validation, exactly like the self-improvement parameters in volume 08. Calibrate them on real cases and keep them marked TO VERIFY.

---

## 5. Workflow

```
S2 (with the reference probe)
   python scripts/keyframe_diff.py extract ref.mp4 --out case/ref_kfs
   → fill shot_size / composition in case/ref_kfs/shots.csv by hand

M3–M4 (cut as planned)

M5 (before delivery, after qc_scan.sh)
   python scripts/keyframe_diff.py extract final.mp4 --out case/mine_kfs
   python scripts/keyframe_diff.py compare case/ref_kfs case/mine_kfs --out case/diff
   → read case/diff/diff_report.md, open case/diff/diff_sheet.png
   → exit 2 means fix, then re-extract and re-compare
```

The paired sheet has **one row per shot: left = reference, right = finished cut**, matched by index. That is the part a human must look at — the numbers can prove the timing matches, but only the eye can say whether shot 4 is doing the same job as the reference's shot 4.

---

## 6. Worked example

A 6.8 s reference of five shots (2.0 / 0.8 / 0.8 / 0.8 / 2.4 s) against two cuts of the same length:

| Cut | Shots | Blocking | Warnings | Verdict |
| --- | --- | --- | --- | --- |
| Structure matched | 5 | 0 | 0 | PASS |
| Restructured to 4 shots, darker and desaturated | 4 | 2 (`T1-shotcount` 20% off, `T1-cutdrift` 0.96 s) | 4 (median 90% off, density corr 0.26, luma −50%, saturation −60%) | BLOCKING, exit 2 |

The second case is instructive: the 4-shot version was still 6.8 s long, so a runtime check alone would have passed it. It was the shot count and the cut-drift check that caught the restructure, and the median-plus-density pair that explained *why* it felt different.

---

## 7. Limits, stated plainly

- **It cannot judge quality.** Whether a shot is well composed, whether the performance works, whether the subject is on brand — none of that is in here.
- **It cannot hear.** Loudness, J/L-cut offsets and sound bridges are checked by `qc_scan.sh` and the audio volume. A cut can pass this diff with a completely wrong soundtrack.
- **A WARN is a prompt to look, not a defect.** A flat grade shift may be an intentional choice for the platform or the brand. The diff reports; the editor decides; the decision gets written down.
- **Frame-index sampling assumes constant frame rate.** On VFR material the mid-shot keyframes fall back to per-shot seeking, which is slower but correct; the statistics pass is unaffected.
- **Shot-size comparison only works if a human filled both sides.** An empty column is reported as INFO rather than silently passing.

---

## References

- FFmpeg Filters Documentation — `signalstats` (YAVG / SATAVG / UAVG / VAVG), `select`, `scdet`, `metadata`, `tile`, `hstack`: https://ffmpeg.org/ffmpeg-filters.html
- FFmpeg Formats — `rawvideo` and image sequence output: https://ffmpeg.org/ffmpeg-formats.html
- This knowledge base, `../01-editing-craft/01-shot-language-and-theory.md` (shot-duration distribution and why the median is used), `02-reference-video-evaluation-framework.md` (dimensions A–G), `03-style-fingerprint-spec.md` (fingerprint fields)
- `scripts/keyframe_diff.py` — the implementation, tested end to end on ffmpeg 8.1.2

Retrieved: 2026-11-11. Thresholds and sampling offsets are this library's own starting values, not standards: TO VERIFY.
