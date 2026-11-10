# Color Grading and Image Quality

> Category: Editing craft | Topic: primary and secondary grades, scopes, Log and LUTs, colour spaces and colour management, white balance and the skin-tone line, noise reduction and sharpening, HDR/SDR conversion and delivery | Compiled: 2026-11-10 | Applies to: grading and QC in DaVinci Resolve / Baselight / Premiere Pro Lumetri, plus batch colour processing with ffmpeg

## 1. Core principles

Grading is the last link in the colour pipeline, but most problems originate in the pipeline rather than in the grade itself: every stage has to answer two questions — what colour space and transfer curve is the material in now, and what does the next stage assume it is. Rec.709 and sRGB share identical primaries and D65 white point, and differ only in transfer function (BT.1886 reference display at about 2.4 gamma, sRGB at about 2.2); that is the root of the same file looking bright and washed out in QuickTime or a browser but normal in grading software. Log is scene-referred (it describes scene light) while Rec.709 is display-referred (it describes display output), and the conversion between them must be explicit, never guessed.

The primary grade acts on the whole frame: white balance, exposure/black level, contrast, saturation, with the goal of neutral consistency across shots. The secondary grade acts on a bounded region: windows, HSL qualifiers and tracking isolate skin, sky or a single object. The order is not negotiable: neutral first, style second; shot matching before any look LUT; noise reduction and sharpening last. Technical LUTs (converting Log to a display space) and creative LUTs are two different things and are not interchangeable — a Sony LUT on Canon footage means nothing.

Colour management runs on ACES or a vendor RCM: IDTs bring each camera's material into a common space -> working space ACEScct (quasi-log with a toe, suited to grading) / ACEScg (linear, suited to VFX) -> ODT renders to Rec.709 / P3 / HDR; ACES2065-1 is the interchange and archival encoding (SMPTE ST 2065-1:2021). PQ is an absolute luminance encoding (SMPTE ST 2084:2014, 0 to 10000 cd/m²), HLG is relative and backward-compatible with SDR broadcast; both sit inside the HDR television system defined by ITU-R BT.2100, with a Rec.2020 container gamut. Scopes turn feeling into data: the waveform shows the luminance distribution, the vectorscope shows hue and saturation, the RGB Parade shows three-channel balance, and the histogram shows overall exposure and clipping.

## 2. Executable standards and parameter tables

Standards and editions (numbers as given in the retrieved official documents):

| Specification | Number / edition | Content |
| --- | --- | --- |
| HDTV parameters | ITU-R BT.709 (often cited as BT.709-6, edition TO VERIFY) | Rec.709 primaries, D65, HD production and interchange |
| UHDTV parameters | ITU-R BT.2020-2 (10/2015) | Rec.2020 primaries, 4K/8K, 10/12 bit, up to 120p |
| HDR television | ITU-R BT.2100-2 (07/2018) (edition current in 2026 TO VERIFY) | The two transfer functions, PQ and HLG |
| SDR display EOTF | ITU-R BT.1886 (edition TO VERIFY) | Reference display, effective gamma about 2.4 |
| PQ | SMPTE ST 2084:2014 | 0 to 10000 cd/m², basis of HDR10 / Dolby Vision |
| PQ/HLG conversion and mapping | Report ITU-R BT.2390 (cites up to -4, 04/2018) | Format conversion, tone mapping |
| HDR operational practice | Report ITU-R BT.2408-1 (2018), subsequently revised to BT.2408-9 (2026) | Nominal levels, reference white |
| ACES | SMPTE ST 2065-1:2021 | ACES2065-1 (AP0) scene-referred encoding |
| Mastering display metadata | SMPTE ST 2086 (number TO VERIFY) | mastering display color volume |
| ACES version | TO VERIFY (1.3 and 2.0 coexist; ACES 2 changed the output rendering design) |

Scope reading thresholds (SDR Rec.709):

| Tool | Reading | Target value |
| --- | --- | --- |
| Waveform | Black level / white level | 0 IRE / <= 100 IRE (broadcast safe around 95 to 100 IRE) |
| Waveform | 8-bit / 10-bit legal code values | 16 to 235 (8-bit) / 64 to 940 (10-bit; relationship to the full/limited range flag TO VERIFY) |
| Waveform | 18% mid grey | about 45 to 50 IRE |
| Waveform | Average luminance difference between adjacent shots | <= 10 IRE |
| Vectorscope | Skin-tone line | about the 11 o'clock direction / 123 degrees (NTSC I-axis rule of thumb, no standalone standard number, TO VERIFY) |
| Vectorscope | Dominant hue angle difference between adjacent shots | <= 10 to 15 degrees |
| Vectorscope | Saturation difference between adjacent shots | <= 10 to 15% |
| Vectorscope | 75% colour bar target box | A reference point, not a hard ceiling |
| RGB Parade | Neutral grey | R/G/B channels level with each other |
| Histogram | Clipping | Neither end may pile against the edge into a flat white band |

Log formats and conversion paths (dynamic range figures as claimed by vendors or summarised by third parties, TO VERIFY):

| Format | Vendor | Claimed dynamic range | Curve characteristics | Path to Rec.709 |
| --- | --- | --- | --- | --- |
| S-Log3 | Sony | about 14 stops | Based on a revised Cineon, no shoulder, weak toe | S-Gamut3.Cine / S-Log3 official LUT or colour management |
| C-Log3 | Canon | about 14 stops | Smoother shadow roll-off than C-Log | Canon official LUT |
| V-Log | Panasonic | 14+ stops | V-Log L is the reduced-range variant | Panasonic V-Log LUT |
| N-Log | Nikon | 12+ stops | Relatively recent | Nikon N-Log LUT or colour management |

HDR nominal levels (Report ITU-R BT.2408, 1000 cd/m² nominal peak display):

| Subject | Nominal luminance cd/m² | %PQ | %HLG |
| --- | --- | --- | --- |
| 18% grey card | 26 | 38 | 38 |
| 83% grey upper limit | 162 | 56 | 71 |
| 90% grey upper limit | 179 | 57 | 73 |
| HDR Reference White / diffuse white / Graphics White (100%) | 203 | 58 | 75 |
| Peak white | about 5 times diffuse white | - | - |

On the waveform, 58% PQ or 75% HLG is the reference white marker, leaving headroom above for highlights; an 18% grey card sits closest to skin tone and is unaffected by SDR camera knees, which makes it the anchor for multicamera alignment. HDR work needs at least 10 bit; upconverting 8-bit SDR to HDR stretches the highlights and produces banding. PQ and HLG require conversion rather than transcoding (BT.2390 section 7 / BT.2408-1 section 6): choose a 1000 cd/m² HLG reference peak and limit PQ to the same peak so brightness stays consistent.

Delivery specifications:

| Item | SDR | HDR |
| --- | --- | --- |
| Gamut / transfer function | Rec.709 / BT.1886 (~2.4) | Rec.2020 container / PQ (ST 2084) or HLG |
| Luminance range | 0 to 100 IRE (about 100 nit) | 1000 to 4000 nit mastering monitor |
| Bit depth / sampling | 8 or 10 bit, 4:2:0/4:2:2 | >= 10 bit |
| Mapping approach | - | display-referred (preserve appearance) / scene-referred (match the camera) |
| Audio | 48 kHz / 24-bit; -14 LUFS for social, EBU R128 / ATSC A/85 for broadcast | As left |

## 3. Procedure / Workflow

1. **Confirm the delivery spec first**: SDR or HDR, gamut, gamma, peak luminance, bit depth, bitrate, loudness; HDR must be graded on a reference monitor capable of the target range in a controlled room, and a laptop with HDR switched on does not count as a reference.
2. **Configure colour management**: RCM or ACES in Resolve, selecting the matching IDT for each camera; ACEScct as the working space and an ODT chosen per deliverable.
3. **Primary**: white balance first (grey card plus the vectorscope skin-tone line, corrected with temperature/tint — never mask a cast by desaturating) -> exposure (waveform black and white levels) -> contrast -> saturation.
4. **Shot matching**: switch to RGB Parade and compare shot by shot, pressing the luminance difference between adjacent shots to <= 10 IRE and the hue angle difference to <= 10 to 15 degrees.
5. **Secondary**: window or qualifier the face before reading the skin-tone line (a whole frame is dominated by a green wall or a red shirt); rotate hue on the skin rather than desaturating globally.
6. **Style**: apply a consistent look LUT or node tree only after the balance is neutral.
7. **Noise reduction and sharpening**: at the last stage, denoise before sharpening so that sharpening does not amplify noise first.
8. **Format conversion**: HDR -> SDR via tone mapping, and watch for 8-bit highlight banding on SDR -> HDR; PQ <-> HLG goes through BT.2390 conversion.
9. **Tagging and QC on output**: write `-color_primaries` / `-color_trc` / `-colorspace`, re-check YMIN/YMAX with signalstats, and verify the full/limited range flag.

```bash
ffprobe -v error -select_streams v:0 -show_entries stream=color_space,color_transfer,color_primaries,pix_fmt -of default=noprint_wrappers=1 input.mp4
ffmpeg -i input.mp4 -vf "signalstats,metadata=print:key=lavfi.signalstats.YMAX" -f null -
```

HDR10 (PQ) -> SDR Rec.709, requiring a zscale build with `--enable-libzimg`:

```bash
ffmpeg -i input_hdr.mp4 -vf "zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p" -c:v libx264 -crf 18 -preset slow -c:a copy output_sdr.mp4
```

`smpte2084` means PQ/HDR10, `arib-std-b67` means HLG and `bt2020nc` means BT.2020 non-constant luminance. Tonemap options are `hable` (best detail), `reinhard` (overall brighter), `mobius` (a middle ground) and `bt.2390` (the ITU standard, the broadcast default); `npl=100` is the SDR reference peak, and a 1000 nit source can be tried at `npl=1000`.

## 4. Common errors and troubleshooting

| Symptom | Root cause | Troubleshooting step |
| --- | --- | --- |
| Exports look washed out in QuickTime or a browser | Transfer function difference between Rec.709 at 2.4 and sRGB at 2.2, or missing colour tags | Write the correct color_trc / color_primaries and check on a consumer display |
| The same grade looks different on two machines | Monitor drift / no calibration | Calibrate to D65, BT.1886 at 2.4, in a dark reference environment |
| HDR looks grey and washed out after a straight re-encode | No tone mapping; PQ values read as SDR | Use the zscale + tonemap chain and re-tag BT.709 at the end |
| Skin drifts cyan or magenta | White balance, or green spill from fluorescent light | Correct with temperature/tint rather than desaturating; window the face and read the 123-degree line |
| Vectorscope readings are untrustworthy | The whole frame is dominated by background or clothing colour | Window or qualifier the face only |
| The look LUT exaggerates the colour temperature spread | LUT applied before the balance was neutral | Go back to steps 3 and 4 and redo them |
| Banding appears in HDR gradients | 8-bit SDR upconverted with expanded highlights | Stay at >= 10 bit and upconvert with care |
| Brightness is inconsistent after PQ/HLG conversion | Transcoding instead of converting | Convert per BT.2390 and unify the 1000 cd/m² reference peak |
| The picture "pumps" on every cut between shots | Luminance, hue or saturation difference beyond threshold | Match shot by shot at 10 IRE / 10 to 15 degrees / 10 to 15% |
| zscale does not exist | ffmpeg built without libzimg | `ffmpeg -filters \| grep zscale`; or switch to libplacebo (requires Vulkan) |

## 5. Quick reference

- [ ] Delivery spec (SDR/HDR, gamut, gamma, nit, bit depth) confirmed in writing
- [ ] Colour management configured, with the correct IDT for each camera
- [ ] Order: white balance -> exposure -> contrast -> shot matching -> secondary -> look LUT -> noise reduction -> sharpening
- [ ] Waveform: 0 IRE black, <= 100 IRE white, mid grey 45 to 50 IRE
- [ ] Skin sits on the 123-degree skin-tone line, read from a window on the face only
- [ ] Adjacent shots within <= 10 IRE luminance, <= 10 to 15 degrees hue angle, <= 10 to 15% saturation
- [ ] HDR: 203 cd/m² = 58% PQ = 75% HLG reference white, >= 10 bit
- [ ] HDR -> SDR uses tone mapping; PQ <-> HLG uses BT.2390 conversion
- [ ] Output carries color_primaries / color_trc / colorspace and a correct range flag
- [ ] YMIN / YMAX verified with signalstats, audio at 48 kHz / 24-bit, loudness within spec

## References

- Recommendation ITU-R BT.2020-2 (10/2015) https://www.itu.int/dms_pubrec/itu-r/rec/bt/R-REC-BT.2020-2-201510-I!!PDF-C.pdf
- Report ITU-R BT.2408-1 (2018), Operational practices in HDR television production https://www.itu.int/dms_pub/itu-r/opb/rep/R-REP-BT.2408-1-2018-PDF-E.pdf
- Report ITU-R BT.2408-9 (2026) https://www.itu.int/dms_pub/itu-r/opb/rep/R-REP-BT.2408-9-2026-PDF-E.pdf
- Report ITU-R BT.2408-2 (2019) https://www.itu.int/dms_pub/itu-r/opb/rep/R-REP-BT.2408-2-2019-PDF-E.pdf
- ICC / Color.org, "High Dynamic Range Imaging - Is there a role for ICC?" (citing BT.2408-1 Table 1 and BT.2100-2) https://archive.color.org/groups/displays/20190215_High_Dynamic_Range_imaging_and_Hybrid_Log-Gamma.pdf
- SMPTE ST 2065-1:2021, ACES RGB encoding https://pub.smpte.org/latest/st2065-1/st2065-1-2021.pdf
- ACES Central, "Overview of the ACES Encodings" https://docs.acescentral.com/encodings/overview
- SMPTE ST 2084:2014 / Perceptual quantizer https://handwiki.org/wiki/Perceptual_quantizer
- EIZO, "HDR explained - gamma curves" (HDR 详解 - 伽玛曲线) https://www.eizo.com.cn/global/library/management/ins-and-outs-of-hdr/index2.html
- Clouds Agency, "Color Pipeline Basics: Rec.709, HDR and ACES" https://www.cloudsagency.co/blog/color-pipeline-basics-rec709-hdr-aces
- The Post Flow, "Color Spaces for Editors: Rec.709, Log, HDR, and the Gamma Shift" https://thepostflow.com/filmmaker-resources/color-spaces-reference/
- TokDL, "Video Scopes Explained" https://tokdl.com/video-scopes/
- Luttie, "Vectorscope" (the 123-degree skin-tone line) https://luttie.app/tools/vectorscope
- DataBrush, "Consistent tone is the baseline for beat sync" (示波器判读阈值) https://www.databrush.com/article.php?id=1286
- Ultra HD Forum, "Ultra HD Production and Post Production 3.0" https://ultrahdforum.org/wp-content/uploads/BlueBook-Ultra_HD_Production_and_Post_Production_3.0.0.pdf
- FFmpegLab, "Color Spaces, HDR, and Tone Mapping in FFmpeg" https://www.ffmpeglab.com/articles/ffmpeg-color-spacing.html
- FFmpeg Cookbook, "Convert HDR to SDR with FFmpeg" https://ffmpeg-cookbook.com/en/articles/hdr-to-sdr/
- DEV Community, "FFmpeg HDR to SDR tone mapping (2026)" https://dev.to/masonwritescode/ffmpeg-hdr-to-sdr-tone-mapping-that-doesnt-look-washed-out-2026-24ie
- Netflix Partner Help, "Picture Archival Assets" (colour space / transfer function abbreviations) https://partnerhelp.netflixstudios.com/hc/en-us/articles/360000384727
- Sony Pictures, "Master and Archive Specifications" http://partnerzone.sonypictures.com/master-and-archive.html

Retrieved: 2026-11-10
