# Audio Post and Mixing Specifications

> Category: Audio and voice | Topic: Vocal chain, EQ and compression settings, and EBU R128 / ATSC A/85 loudness compliance | Compiled: 2026-11-10 | Applies to: Mixing finished video, broadcast and streaming delivery, pre-delivery loudness measurement and compliance sign-off

## Core principles

**The processing chain follows one rule: subtract first, add second, lock loudness last.** Start with corrective subtraction (dereverb, noise reduction, de-essing) so later compression does not amplify the noise along with the voice; then shape tone (corrective EQ, mostly cuts); then compress to control dynamics; finally normalize loudness to bring the whole program to the target LUFS. Reverse any stage and you amplify the flaws of the one before it.

**How loudness measurement works**: ITU-R BS.1770 uses K-weighting to approximate subjective loudness — a pre-filter (a high-frequency shelf of about +4 dB, modelling the acoustics of the head), then an RLB high-pass that removes sub-low frequencies below about 38 Hz. Measurement uses three time windows: Momentary (400 ms), Short-term (3 s), and Integrated (over the whole program), abbreviated M/S/I; blocks are 400 ms with 75% overlap. Integrated loudness uses two-stage gating: an absolute gate at -70 LKFS removes silence first, then a relative gate removes passages 10 LU below the ungated loudness (the **-10 LU relative gate**), so long pauses cannot drag the average down. Channel weights are unity for L/R/C, +1.5 dB for the surround channels Ls/Rs, and LFE is excluded. True Peak (dBTP) estimates inter-sample peaks via 4× oversampling to prevent clipping after lossy encoding.

**Three units must be kept apart (BBC WHP202 is explicit about this)**:
- **LUFS and LKFS are exactly equivalent**: the same BS.1770 meter, with EBU documents writing LUFS and ATSC/ITU plus most US specs writing LKFS; -24 LKFS = -24 LUFS.
- **LUFS is an absolute loudness level** (relative to full scale); **LU is a relative difference**: -23 to -21 is "a 2 LU difference", not "2 LUFS".
- **1 LU = 1 dB**: apply +1 dB of gain and the loudness level rises 1 LU. A 1 kHz stereo sine at -18 dBFS reads -18 LUFS.

Loudness standards exist to end the "loudness war": peak normalization made loudness jump between programmes, so EBU R128 and ATSC A/85 switched to perceptual loudness normalization, and the US CALM Act went further, making it law that commercials match programme loudness.

## Specifications and parameter tables

### Table 1 Vocal chain order and parameter ranges (engineering rule-of-thumb values, TO VERIFY)

| # | Stage | ffmpeg filter | Key parameter range | Purpose |
| --- | --- | --- | --- | --- |
| 0 | Dereverb | No native filter (external plugin, TO VERIFY) | Voice booth RT60 <=0.3 s | Fix room reflections first |
| 1 | Noise reduction | `afftdn` | `nf=-25` (noise floor in dB), strength 30%-50% | Subtraction; too aggressive gives metallic or underwater artifacts |
| 2 | High-pass | `highpass` | 80-100 Hz | Remove rumble and low-end mud |
| 3 | De-esser | `deesser` | `i=0.3-0.6` `m=0.5` `f=0.5` | Tame s/sh around 5-9 kHz |
| 4 | Corrective EQ | `equalizer` | Cut 2-4 dB at 200-500 Hz; boost 1-2 dB at 3-5 kHz | Cut mud first, then lift presence |
| 5 | Compression | `acompressor` | ratio 2:1-4:1, attack 10-30 ms, release 100-300 ms | Target 3-6 dB of GR, never above 10 dB |
| 6 | Loudness | `loudnorm` | Per-platform target I / TP / LRA | Only two-pass linear is compliant |

> Measured `deesser` options: `i` (intensity 0-1, default 0), `m` (maximum de-essing 0-1, default 0.5), `f` (frequency 0-1, default 0.5), `s` (o/i/e output mode). `acompressor` options: `threshold` (0.00098-1), `ratio` (1-20), `attack` (0.01-2000 ms), `release` (0.01-9000 ms), `knee` (1-8, default 2.83), `makeup` (1-64).

### Table 2 Quick EQ band reference

| Band | Role | Typical treatment |
| --- | --- | --- |
| 20-60 Hz | Sub-low / rumble | High-pass at 80 Hz |
| 60-120 Hz | Body, warmth | ±1-2 dB; too much turns muddy |
| 200-500 Hz | Boxiness, mud | -2 to -4 dB |
| 500 Hz-1 kHz | Nasality, telephone character | Handle with care, minimal moves |
| 1-4 kHz | Consonants, the intelligibility zone | Preserve; +1-2 dB if needed |
| 3-5 kHz | Presence, sense of distance | +1-2 dB to brighten |
| 5-9 kHz | Sibilance, metallic artifacts | De-esser / narrow notch at -2 to -4 dB |
| Above 10 kHz | Air | Gentle shelf |

### Table 3 Broadcast loudness standards compared (core; official PDFs checked)

| Item | EBU R128 (Europe) | ATSC A/85:2013 (US) |
| --- | --- | --- |
| Target | **-23.0 LUFS** | **-24 LKFS** |
| Tolerance | Pre-recorded ±0.2 LU (QC); live / difficult material ±1.0 LU | About ±2 dB measurement tolerance |
| True Peak | **-1 dBTP** (production, linear audio), measurement tolerance ±0.3 dB | **< -2 dBTP** (encoding headroom) |
| Measurement basis | ITU-R BS.1770 + **EBU Tech 3341** (including gating) | ITU-R **BS.1770-3** |
| What is measured | The whole programme; no emphasis on dialogue / music / effects | Anchor element (dialogue) for long form; whole programme for short form |
| Gating | Relative gate -10 LU (BS.1770 Eq.7 since the 2014 revision; -8 LU in the 2011 original) | BS.1770 gating |
| Metadata | Loudness Metadata must state the actual loudness truthfully | **dialnorm** (AC-3, mandatory per A/53 Part 5) |
| Regulation | Broadcaster delivery specs (e.g. BBC/DPP) | **CALM Act**, FCC under 47 CFR 73.682(e) |
| Notes | R128 s1 for short content; s2 for streaming; s3 + Tech 3401 for radio; s4 for film | PBS TOS: -24 LKFS ±2 LU; 5.1 downmixes must also comply |

### Table 4 The EBU PLOUD document family (do not mix them up)

| Document | Scope |
| --- | --- |
| **Tech 3341** | Loudness meter spec: EBU mode, the three M/S/I time windows, the -10 LU relative gate, True Peak measurement |
| **Tech 3342** | Definition and statistical basis of Loudness Range (LRA) |
| **Tech 3343** | Production and implementation workflow; Max Short-term Loudness for short content (s1) is -18.0 LUFS |
| **Tech 3344** | Distribution and transmission; the maximum permitted True Peak may be lower under some codecs and bitrates |

### Table 5 Broadcast vs. streaming loudness targets

| Platform / standard | Target | True Peak | Notes |
| --- | --- | --- | --- |
| EBU R128 | -23 LUFS | -1 dBTP | European broadcast |
| ATSC A/85 | -24 LKFS | -2 dBTP | US broadcast |
| YouTube | -14 LUFS | -1 dBTP | No official published figure; attenuates only, never boosts |
| Spotify | -14 LUFS | -1 dBTP (-2 recommended for louder masters) | Loud -11 / Quiet -19 |
| **Apple Music (Sound Check)** | **About -16 LUFS** | -1 dBTP | Approximation; Apple has not published a figure, TO VERIFY |
| Apple Podcasts | -16 LKFS ±1 dB | -1 dBFS | BS.1770-5 |
| Tidal / Amazon Music / SoundCloud | -14 LUFS | -1 / -2 dBTP | Amazon recommends -2 |
| Deezer | -15 LUFS | -1 dBTP | Single source, TO VERIFY |
| Netflix | -27 LKFS ±2 LU (dialogue-gated) | -2 dBTP | -24 LKFS over the whole programme when dialogue is under 15% |
| AES TD1004.1.15-10 (2015) | **-16 to -20 LUFS window** | -1 dBTP | Superseded by TD1008 |
| AES TD1008 (2021) / AES77-2023 | Music -16 LUFS, speech **-18 LUFS** | -1 dBTP | See the TO VERIFY note below |
| EBU R128 s2 (2023) | -23 LUFS; provisionally -20 to -16 LUFS when no metadata is present | — | Streaming supplement |

### Table 6 Dialogue / music / SFX level relationships (reference before mastering)

| Element | Level reference | Relationship |
| --- | --- | --- |
| Dialogue / narration (anchor) | Peaks -12 to -6 dBFS, average -18 to -14 dBFS | Set this first; balance everything else against it |
| Music (under narration) | -18 to -24 dBFS | 6-12 dB below the voice; 12-18 dB below in dense passages |
| Sound effects | Around -6 dBFS peak | Transients may go higher, but must not bury dialogue |
| Ambience | Bed / mid / accent ≈ -30 / -24 / -18 dBFS | Sits underneath |
| Foley | 6-10 dB below dialogue | Supports, does not steal focus |
| Final mix | Per the LUFS targets in Table 5 | True Peak must stay below the ceiling |

### Table 7 Ducking / sidechain parameters

| Parameter | Range |
| --- | --- |
| Music attenuation | -2 to -6 dB (3-6 dB typical) |
| Ambience attenuation | -1 to -3 dB |
| Attack | < 10 ms |
| Release | 200-400 ms |
| Ratio | 2:1 to 3:1 |
| Band-selective ducking | Use a dynamic EQ or multiband compressor to duck only 1-4 kHz, keeping the low end and air |
| Abort criterion | If dialogue is only intelligible with more than 10 dB of ducking, the cue or the frequency balance is wrong — change the track |

### Table 8 Compliance tolerances before delivery

| Scenario | Target | Permitted deviation | True Peak ceiling |
| --- | --- | --- | --- |
| EBU R128 pre-recorded | -23 LUFS | ±0.2 LU (QC); some broadcasters ±0.5 LU | -1 dBTP |
| EBU R128 live | -23 LUFS | ±1.0 LU | -1 dBTP |
| ATSC A/85 | -24 LKFS | ±2 dB | -2 dBTP |
| R128 s1 short content | -23 LUFS | Same as R128 | Max Short-term -18 LUFS |

## Procedure / Workflow (commands tested locally on ffmpeg 8.1.2)

### Step 1 Full vocal chain
```
ffmpeg -i raw.wav -af "highpass=f=80,afftdn=nf=-25,deesser=i=0.4:m=0.5,equalizer=f=300:t=q:w=1:g=-2,acompressor=threshold=0.1:ratio=3:attack=20:release=200,loudnorm=I=-23:TP=-1:LRA=7" -ar 48000 -ac 1 -c:a pcm_s24le vo.wav
```

### Step 2 Measure (mandatory before delivery)
```
ffmpeg -hide_banner -i mix.wav -af "ebur128=peak=true" -f null - 2>&1
```
The summary prints Integrated loudness / Threshold / LRA / True peak. Measured locally on a 1 kHz sine: I=-21.1 LUFS, Threshold=-31.1 LUFS, Peak=-18.1 dBFS — Threshold is exactly I minus 10 LU, confirming the -10 LU relative gate.

Machine-readable measurement (first pass of two):
```
ffmpeg -hide_banner -i mix.wav -af "loudnorm=I=-23:TP=-1:LRA=7:print_format=json" -f null - 2>&1
```
Returns `input_i` / `input_tp` / `input_lra` / `input_thresh` / `output_i` / `output_tp` / `output_lra` / `output_thresh` / `normalization_type` / `target_offset`.

### Step 3 Two-pass linear normalization (the only recommended route for compliant delivery)
```
ffmpeg -i mix.wav -af "loudnorm=I=-23:TP=-1:LRA=7:measured_I=-21.05:measured_TP=-18.06:measured_LRA=0.00:measured_thresh=-31.05:offset=0.05:linear=true" -ar 48000 -c:a pcm_s24le out_ebu.wav
```
Copy the `input_*` values from Step 2 into `measured_*`, and `target_offset` into `offset`. Measured locally, the output is -23.1 LUFS, Linear, 48000 Hz. For ATSC use `I=-24:TP=-2`; for streaming use `I=-14:TP=-1:LRA=11`.

> **The trap**: `loudnorm` in dynamic mode writes the output at **192000 Hz** by default (measured locally), so `-ar 48000` must be explicit; single-pass dynamic mode also compresses the tone and drifts by roughly 5%-10%, which rules it out for contractual delivery.

### Step 4 Ducking / sidechain
```
ffmpeg -i music.wav -i vo.wav -filter_complex "[0:a][1:a]sidechaincompress=threshold=0.05:ratio=4:attack=10:release=300[ducked]" -map "[ducked]" -ar 48000 -c:a pcm_s24le music_ducked.wav
```
Here main is the music and sidechain is the dialogue; the output is the attenuated music, which you then `amix` with the dialogue.

### Step 5 Pre-delivery measurement and compliance tolerances
1. Measure the Integrated I of the **whole programme** (first frame to last), not the Short-term peak.
2. I must land within the target ± tolerance and True Peak below the ceiling; otherwise apply linear gain with `volume=XdB` (X = target - measured) or redo the two-pass linear pass.
3. If the gain pushes True Peak over the ceiling, use a **limiter** around -2.3 dBFS instead of pulling the whole mix down.
4. Measure and normalize every deliverable independently, including the stereo fold-down, M&E, and each language track.
5. Write the measured values into the delivery notes/metadata; every language track must comply on its own.

## Common errors and troubleshooting

| Error | Consequence | Fix |
| --- | --- | --- |
| Peak normalization instead of loudness normalization | Loudness jumps between programmes | Always use a BS.1770 loudness meter |
| Confusing LUFS with LU | Unit and communication errors | LUFS for absolute levels, LU for differences |
| Single-pass loudnorm for compliant delivery | Large drift and squashed tone | Two-pass with `linear=true` |
| Forgetting `-ar 48000` | 192 kHz output, delivery rejected | Specify the sample rate explicitly |
| Setting TP to 0 dBTP | Clipping after lossy encoding | Set -1 / -2 dBTP |
| Chain in the wrong order (compress before noise reduction) | Noise gets amplified | Subtract first, add second |
| Fighting dialogue/music frequency collision with heavy ducking | Still unintelligible even above 10 dB | Change the track, or use band-selective EQ |
| Normalizing twice | Dynamics flattened repeatedly | Measure, then process once |
| Measuring only the primary language track | Inconsistent loudness across languages | Normalize each track independently |
| Using Short-term peak instead of Integrated | Non-compliant delivery | Measure I over the whole programme |

## Quick reference

- [ ] Chain order: dereverb → noise reduction → high-pass → de-esser → corrective EQ → compression → loudness
- [ ] Noise reduction strength <=50%, compression GR 3-6 dB, ratio <=4:1
- [ ] Delivery target fixed: broadcast -23 LUFS / -24 LKFS, streaming -14 / -16 LUFS
- [ ] Measure whole-programme I, LRA, and True Peak with `ebur128=peak=true`
- [ ] Compliant delivery uses two-pass `linear=true`, plus `-ar 48000`
- [ ] True Peak: EBU <= -1 dBTP, ATSC <= -2 dBTP
- [ ] Dialogue is the anchor, music 6-12 dB below, ducking 2-6 dB
- [ ] Measure every track, fold-down, and M&E individually and record the measured values
- [ ] Keep LUFS (absolute) and LU (difference) apart; treat LKFS as identical to LUFS

## References

- EBU, Recommendation R 128 (2014 revision, official PDF) — https://tech.ebu.ch/docs/r/r128.pdf
- EBU, R 128 (2011 original, official PDF) — https://www.ebu.ch/files/live/sites/ebu/files/News/2011/r128%255B1%255D.pdf
- EBU, "10 things you need to know about R 128" — https://tech.ebu.ch/docs/events/ibc10/presentations/ebu_ibc10_r128.pdf
- BBC R&D, White Paper WHP 202: Terminology for loudness and levels (LU/LUFS/LKFS disambiguation) — http://downloads.bbc.co.uk/rd/pubs/whp/whp-pdf-files/WHP202.pdf
- ITU-R, Recommendation BS.1770-4 (official Chinese-language PDF; -70 LKFS and -10 LU gating) — https://www.itu.int/dms_pubrec/itu-r/rec/bs/R-REC-BS.1770-4-201510-S!!PDF-C.pdf
- ATSC, Recommended Practice A/85:2013 (official PDF) — http://www.atsc.org/wp-content/uploads/2015/03/Techniques-for-establishing-and-maintaining-audio-loudness.pdf
- PBS, Technical Operating Specification Part 1 — https://bento.pbs.org/prod/filer_public/pbsproducerhandbook-bento-live-pbs/c757f1a4a9_2023%20TOS%20Pt%201.pdf
- BBC, Audio Quality Information & Standards for Radio — https://www.bbc.co.uk/commissioning/radio/documents/technicalspecificationradiojuly2022_v01.7.pdf
- CineMath, Loudness Standards by Platform — https://www.cinemath.app/guides/workflows/loudness-standards
- CineMath, Loudness Specs Cheat Sheet — https://www.cinemath.app/resources/loudness-specs
- Production Expert, What Is Loudness (history of AES TD1004 / TD1008) — https://www.production-expert.com/production-expert-1/what-is-loudness-lufs-lkfs-and-delivery-specs-explained-2026
- 4RFV, Worldwide Loudness Delivery Standards (TD1004 -16 to -20 LUFS) — https://www.4rfv.com/ULKLGX7KZSZW/worldwide-loudness-delivery-standards.htm
- MpegFlow, Loudness-normalize audio with FFmpeg — https://www.mpegflow.com/recipes/loudness-normalize-audio
- BrowserBasedTools, How to measure loudness to a broadcast target — https://browserbasedtools.com/how-to/measure-loudness-to-a-broadcast-target
- TabDSP, Professional Metering (BS.1770-4 implementation details) — https://tabdsp.com/v2/pages/metering.html
- FFmpeg official documentation (filter syntax) — https://www.ffmpeg.org/ffmpeg-filters.html

Retrieved: 2026-11-10

**TO VERIFY**: ① The "-16 LUFS" figure for Apple Music Sound Check is an industry approximation; Apple has not published an exact target; ② The "AES TD1004 -18 LUFS" figure in the source brief does not match the research — TD1004.1.15-10 (2015) is actually a **-16 to -20 LUFS window**, and -18 LUFS is the later target for **speech** under TD1008 (2021) / AES77-2023; the text here clarifies this and flags it for verification; ③ ATSC A/85 has a new revision approved in 2026-07; the figures here follow the A/85:2013 official PDF and the new clauses have not been checked line by line; ④ The -3 dBTP recommendation for the distribution stage in EBU Tech 3344 comes from secondary sources; the original Tech 3344 document has not been read; ⑤ Figures for Netflix / Disney / Deezer / Amazon and similar platforms come from summary tables, not each platform's own specification; ⑥ The EQ, compression, ducking, and level ranges in Tables 1, 2, 6, and 7 are engineering rule-of-thumb values, not mandates; ⑦ ffmpeg has no native dereverb filter and requires an external plugin such as iZotope RX; the voice-booth RT60 <=0.3 s figure is a rule of thumb; ⑧ The 5%-10% drift of single-pass loudnorm is a secondary-source rule of thumb.
