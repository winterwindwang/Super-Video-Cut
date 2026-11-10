# Editing Workflow and Project Standards

> Category: Editing craft | Topic: media ingest and verification, proxy workflows, track organisation, naming and versioning, offline/online conform, interchange formats, 3-2-1 backup and delivery | Compiled: 2026-11-10 | Applies to: post-production on multicamera narrative, documentary and OTT long-form, and project handover between Premiere Pro / Avid Media Composer / DaVinci Resolve

## 1. Core principles

Most post-production disasters come not from bad editing but from lost metadata. The first principle of ingest is never trade verification for speed: unload cards with a tool that computes checksums (OffShoot, Silverstack), run an MD5 check and confirm the copy matches the source bit for bit; never use the operating system's copy and paste. The DIT also logs reel ID, timecode, clip metadata and the camera report (FPS / Shutter / ISO / WB / focal length / T stop / filters / camera height and tilt), which is the only basis for later conform and VFX pickups.

The proxy workflow is the offline / online two-stage process: transcode camera originals such as ARRI RAW, REDCODE and Sony X-OCN into edit-friendly low-bitrate files and cut on the proxies; after picture lock, export AAF or XML, relink the original high-resolution media in Resolve or Baselight, and complete the online conform, shot verification, reframing and final grade before mastering out from the original. A proxy is not a thumbnail: it must match the master exactly in frame rate, start timecode, duration and audio channel mapping — otherwise cuts land on the wrong source timecode after relink (mixed frame rates are the single biggest failure mode in interchange).

Interchange formats each have boundaries. OTIO is JSON that describes editorial decisions (Timeline -> Stack -> Track -> Clip -> MediaReference); it stores only order, cut points, transitions, tracks, durations and external media references, not the media itself and not rendered results, and vendor effects collapse to unknown. EDL (CMX3600) carries one video track, one audio track and basic timecode, with no effects and no subclips. AAF is a container rather than a codec and may wrap MXF essence (Avid uses OP-Atom, one file per essence). FCP7 XML and FCPXML are two different schemas, and OTIO adapts them with the `fcp_xml` and `fcpx_xml` adapters respectively. 3-2-1 backup means three copies of the data, on two different media types, with one off-site (or in the cloud), and project folders should be compressed and backed up daily to two separate locations.

## 2. Executable standards and parameter tables

Project directory layout (the same set on every project, so you can find files by muscle memory):

| Directory | Contents | Notes |
| --- | --- | --- |
| `01_Raw_Footage` | Camera originals, split by `Camera_A` / `Camera_B` / `Drone` / `Audio_External` | Read-only, never overwritten |
| `02_Project_Files` | Project files, Production / project lock files | Backed up daily |
| `03_Assets` | Graphics / Music / SFX / Stock / Brand_Kit / LUT | Fonts and licence files archived alongside |
| `04_Proxies` | Proxy files | Separate directory from raw, different extension |
| `05_Exports` | Review / Final / Social_Cuts | Every export carries a metadata log |
| `06_Deliverables` | Client / Archive, subtitles, stems, handover sheet | The delivery checklist is verified here |

Naming and versioning:

| Object | Format | Example |
| --- | --- | --- |
| Source footage | `PROJ-YYYYMMDD-CAMx-SCENE-TAKE-TC` | `WILDLIFE-20231015-A01-142205-01020304.MOV` |
| Proxy file | Source name + `_proxy` suffix | `A001_C001_proxy.mov` |
| Timeline | `PROJ_CUT_vX.Y_description` | `PROJ_CUT_v1.1_Notes` |
| Version | Increment `v1.0` / `v1.1` / `v2.0`; never `final` | `Project_v2.0_Approved` |
| Timecode | `HH:MM:SS:FF`, 8-digit start `01:00:00:00` | Per SMPTE ST 12-1:2014 |

Target bitrates for proxy codecs (Apple's official glossary, 1920x1080 / 29.97 fps):

| Codec | Target bitrate | Use |
| --- | --- | --- |
| ProRes 422 Proxy | about 45 Mbps | Offline editing, full resolution at low bitrate |
| ProRes 422 LT | about 102 Mbps | Compromise between storage and bandwidth |
| ProRes 422 | about 147 Mbps | General mastering |
| ProRes 422 HQ | about 220 Mbps | High-quality intermediate / mezzanine |
| ProRes 4444 | about 330 Mbps | Graphics interchange with alpha |
| ProRes 422 Proxy @1080p24 | about 36 Mbps | The 24p figure given in Apple Motion documentation |
| DNxHR LB | TO VERIFY (no official vendor bitrate figure found) | Common proxy codec on Windows / Avid |

Interchange format matrix:

| NLE | Export format | Cautions |
| --- | --- | --- |
| Premiere Pro | FCP7 XML / AAF | Different from FCPXML schema; specify `--version` |
| Final Cut Pro X | FCPXML | Media paths need the `file:///` prefix |
| DaVinci Resolve | FCPXML / AAF / EDL / OTIO (from 18.5) | DRP is opaque binary; use FCPXML for round trips |
| Avid Media Composer | AAF + DNxHR MXF OP-Atom | Use `-f mxf_opatom`, not OP1a |
| Lightworks | AAF / EDL (CMX3600) | Cut points and basic transitions only |

Related specifications: SMPTE ST 12-1:2014 (timecode), SMPTE 258M-2004 "For Television - Transfer of Edit Decision Lists" (CMX3600 EDL; numbering scheme and current edition TO VERIFY), AAF Object Specification v1.1 (AMWA; current version TO VERIFY), SMPTE ST 377-1 (MXF container, TO VERIFY), the SMPTE ST 2067 series (IMF; individual part numbers TO VERIFY), and SMPTE ST 2110 (IP production, cited by the Ultra HD Forum). The track layout is a recommended project configuration (TO VERIFY whether any vendor publishes a written standard): V1-V3 primary camera, V4 B-roll, V5 graphics, V6 grade/adjustment layers; A1-A2 production dialogue (dual mono), A3-A4 wild lines, A5 SFX, A6 ambience, A7 music, A8 mix stems.

## 3. Procedure / Workflow

1. **Set up directories and the naming table**: Create the six directories and version rules above before the shoot and document them in `02_Project_Files/README`.
2. **Offload and verify**: Unload with OffShoot / Silverstack and MD5 checksums, and do not format a card until verification completes. Generate the checksum manifest:

```bash
md5sum A001_C001.mov > A001_C001.mov.md5
md5sum -c A001_C001.mov.md5
ffprobe -v error -select_streams v:0 -show_entries stream=codec_name,width,height,r_frame_rate,pix_fmt:stream_tags=timecode -of default=noprint_wrappers=1 A001_C001.mov
```

3. **Generate proxies**: Frame rate, timecode, reel ID and channel mapping must match the source exactly; for 4K sources test at 1/2 or 1/4 size and run a screen test before batching. ffmpeg example (`-profile:v 0` maps to ProRes 422 Proxy only as far as this machine's `ffmpeg -h encoder=prores_ks` output indicates, TO VERIFY):

```bash
ffmpeg -i A001_C001.mov -vf "scale=1920:1080" -c:v prores_ks -profile:v 0 -c:a pcm_s16le -ar 48000 -timecode 01:00:00:00 A001_C001_proxy.mov
```

The equivalent menus in each NLE: Premiere Pro `File > Generate Proxies` / Media Browser `Transcode to Proxy`; Resolve `Generate Proxy Media`; FCP `Transcode to Proxy`; Avid `Create Proxy Clips`.

4. **Sync and build bins**: Sync external audio by timecode or waveform and build the multicamera sequence; suggested bins are `00_INGEST_RAW` / `01_PROXY` / `02_OFFLINE_EDIT` / `03_ONLINE_MASTER`, and inside `02` use descriptive names such as `INT_KITCHEN_DAY_01_TAKE3` rather than original filenames.
5. **Offline edit**: Enable proxy mode; star-rate selects, paper-edit markers, radio cut (audio first), B-roll layering, subtitles; normalise loudness first to -14 LUFS (social) / -16 LUFS (LinkedIn, Twitter), and follow EBU R128 or ATSC A/85 for broadcast.
6. **Picture lock and handover**: Export AAF (audio conform to Pro Tools) and XML/OTIO (picture conform to Resolve); OTIO hub conversion example:

```bash
otio-convert --input premiere.xml --output-format fcpx_xml > resolve.fcpxml
otio-convert --input resolve.fcpxml --input-format fcpx_xml --output-format cmx_3600 > cut.edl
```

After conversion, verify clip count, total duration, transition count, audio track count and levels, and spot-check 3 to 5 cuts at known timecodes. If media paths change after conform, remap them with OTIO's `remap-media`.

7. **Online conform**: Disable proxies -> Relink Media / Replace with Originals pointing at `01_Raw` -> check offset, timecode, speed changes, scaling and renames shot by shot; in Resolve, conform first and grade second, leaving noise reduction for last.
8. **Master output**: Disable Use Proxies / Proxy Export; choose ProRes 422 HQ / DNxHR HQ / H.265 per the delivery spec, write the correct colour space tags, and use 48 kHz / 24-bit audio.
9. **Verify the delivery checklist**: master + platform variants (batch queue) + SRT subtitles + audio stems + project files + fonts/licences + LUTs + EDL/XML/AAF + checksum manifest + metadata log.
10. **3-2-1 archive**: three copies (shared storage + local drive + off-site/cloud), two media types, one off-site; compress and back up the project folder to two locations daily.

## 4. Common errors and troubleshooting

| Symptom | Root cause | Troubleshooting step |
| --- | --- | --- |
| Cuts land on the wrong source timecode after relink | Proxy frame rate or timecode differs from the source | Compare start TC and `r_frame_rate` with ffprobe, then regenerate the proxies |
| Many clips go offline (media offline) | Directories moved after proxies were generated; OTIO does not store media | Fix the directory structure, use relative paths, run `remap-media` |
| Structure is lost on import | Wrong adapter for FCP7 XML versus FCPXML | State `--input-format fcp_xml` / `fcpx_xml` explicitly |
| No picture in the AAF | AAF is a container and the essence may be MXF OP-Atom | Inspect the contents with MediaInfo; use `-f mxf_opatom` for Avid |
| Frame-by-frame drift after mixing 23.976 with 29.97 DF | Drop-frame and non-drop timecode mixed | Unify on a single mezzanine frame rate and pass `-timecode` through |
| Effects vanish in the target NLE | Vendor effects do not round-trip | Budget for manual rebuilds; treat pre-rendered effects as source |
| Abnormal file size or degraded picture | Exported from proxies (Use Proxies left on) | Turn proxy export off and output from the master again |
| Camera originals overwritten | Proxies share the master's name and directory | Separate directories and extensions, and make the raw directory read-only |
| DRP round trip loses information | DRP is opaque binary | Use FCPXML for round trips instead |
| Channel count or layout scrambled | Stereo, dual mono and 5.1 mixed together | Check the channel layout with ffprobe and verify track by track after import |

## 5. Quick reference

- [ ] Six directories plus naming/version rules in place before the shoot
- [ ] Offload verified with MD5; no card formatted before the check passes
- [ ] Proxies match the source on all four: frame rate, start TC, duration, channel mapping
- [ ] Proxies in ProRes 422 Proxy (about 45 Mbps @1080p29.97) or DNxHR LB
- [ ] Bin structure fixed; edits use descriptive names rather than original filenames
- [ ] Target NLE and interchange format (AAF / FCPXML / FCP7 XML / EDL / OTIO) agreed before handover or conform
- [ ] After conversion, verify clip count, total duration, transitions and audio track count; spot-check 3 to 5 cuts
- [ ] Proxy export disabled for the online conform; output from the master
- [ ] Audio 48 kHz / 24-bit; -14 LUFS for social
- [ ] Delivery includes master, variants, subtitles, stems, project, LUTs, fonts/licences, EDL/XML/AAF, checksum manifest
- [ ] 3-2-1: 3 copies / 2 media / 1 off-site, with the project backed up to two locations daily

## References

- The Streamic, "Studio-Grade Video Workflow Post-Production (2026)" http://thestreamic.in/articles/studio-grade-video-workflow-post-production-2026.html
- media-os / Claude Plugin Hub, "workflow-editorial-interchange" https://www.claudepluginhub.com/skills/damionrashford-media-os/workflow-editorial-interchange
- OpenTimelineIO README (including notes on SMPTE 258M-2004 and the CMX3600 / AAF adapters) http://guthub.com/wquintero/OpenTimelineIO
- OpenTimelineIO official site https://opentimeline.io/ ; GitHub https://github.com/PixarAnimationStudios/OpenTimelineIO
- Violetflare, "What Is OpenTimelineIO (OTIO) and Why Should Creators Care?" https://violetflare.ai/blog/what-is-opentimelineio-otio-creators
- Frame One, "Best Practices for New Projects in Avid" (definition of 3-2-1) http://help.frameone.com/support/solutions/articles/69000790810-best-practices-for-new-projects-in-avid
- Apple, Final Cut Pro Glossary (Final Cut Pro 词汇表), ProRes target bitrates https://support.apple.com/zh-cn/guide/final-cut-pro/glossary-ver90ba496f/10.6.6/mac/12.6
- Apple, "Popular video codecs in Motion" (Motion 中的流行视频编解码器) https://support.apple.com/en-us/guide/motion/motn18cbcefb/5.5/mac/10.15.6
- SharedTutor, "Video Editing Workflow Tips for Creators" https://sharedtutor.com/2026/07/27/video-editing-workflow-tips-creators-2026-8/
- SHIFTS!, "Proxy workflow" https://www.blogshifts.net/videomaker-tutorial-20260827-proxy-workflow
- LearnLab, CINEWORKFLOW (DIT / Checksums / 3-2-1 / XML-EDL conform) http://www.learnlab.com.cn/Link3
- Netflix Partner Help, "Picture Archival Assets: Folder Structure and File Naming Convention" https://partnerhelp.netflixstudios.com/hc/en-us/articles/360000384727
- SMPTE ST 12-1:2014, Time and Control Code https://pub.smpte.org/latest/st12-1/st0012-1-2014.pdf
- Sony Pictures, "Master and Archive Specifications" http://partnerzone.sonypictures.com/master-and-archive.html
- Ultra HD Forum, "Ultra HD Production and Post Production 3.0" https://ultrahdforum.org/wp-content/uploads/BlueBook-Ultra_HD_Production_and_Post_Production_3.0.0.pdf

Retrieved: 2026-11-10
