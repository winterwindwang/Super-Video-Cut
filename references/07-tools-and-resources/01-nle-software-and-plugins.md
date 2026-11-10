# Editing Software and the Plug-in Ecosystem

> Category: Tools and resources | Topic: NLE selection, proxies and colour grading, plug-in collaboration, hardware | Compiled: 2026-11-10 | Applies to: building an editing workstation, choosing software, proxy workflows and final delivery

## 1. Core principles and concept comparison

Choosing an NLE is not a feature-sheet contest. It comes down to three constraints: **project scale and how the team collaborates**, **depth of grading and finishing**, and **platform and cost model**. One film often involves more than one application: the edit in one place, grading and mixing in another, batch processing and muxing on the command line.

| Workflow concept | Definition | Why it matters |
| --- | --- | --- |
| Proxy | Edit from a low-resolution / low-bitrate copy and relink to the originals on output | 4K/RAW stays responsive on a modest machine |
| Offline / online | Low-bitrate edit → conform to the originals → high-bitrate finishing and output | Keeps proxy compromises out of the delivered picture |
| Primary grade | White balance, exposure, contrast, highlights and shadows, saturation | Makes exposure and colour temperature consistent across the film |
| Secondary grade | HSL, curves, qualifiers, PowerWindows, tracking, skin-tone correction | Local fixes and stylisation |
| LUT | Technical LUTs (LOG→Rec.709) and creative LUTs (stylisation) | A starting point, not the destination; 60%-80% strength recommended |
| Review / collaboration | Version turnover with timecode-accurate notes | Sets how fast a team can deliver |

## 2. Positioning and use cases by application

| Application | Platform | Licensing (third-party compilation; all TO VERIFY) | Core strengths | Main limitations | Best suited to |
| --- | --- | --- | --- | --- | --- |
| Adobe Premiere Pro | Win / Mac | Subscription, about $22.99/month | Creative Cloud dynamic link with AE / Audition / Photoshop, multicam, nested sequences, Lumetri grading, speech-to-text captions, Essential Graphics, the richest plug-in ecosystem | Endless subscription cost, large projects stutter, grading depth short of Resolve | Agencies, in-house teams, cross-platform commercial work |
| DaVinci Resolve | Win / Mac / Linux | Free version fully featured; Studio about $295 one-time | Node-based grading on the Color page is the industry standard, HDR / tracking / PowerWindows, Fusion VFX, Fairlight audio, Blackmagic Cloud multi-user projects, Cut and Edit pages | Steepest learning curve; Fusion and grading are GPU-hungry | Grading, independent film, cinema-grade finishing, professionals on a budget |
| Final Cut Pro | macOS only | About $299.99 perpetual | Magnetic timeline keeps sync automatically, Apple Silicon performance, zero-configuration automatic proxies, ProRes RAW, Compressor batch export | Team and collaboration ecosystem weaker than PR, fewer third-party plug-ins, no Windows version | Individual Mac creators, YouTube, fast-turnaround editing |
| Avid Media Composer | Win / Mac | About $49/month or $1999 perpetual | Bin-based media management, shared projects and shared storage, broadcast-grade real-time DNxHD/DNxHR, strict delivery conventions, long-term stability | Workflow logic unlike consumer software, highest learning cost | Film, TV drama, broadcasters, large teams |
| Jianying Pro (剪映专业版) / CapCut | Win / Mac / mobile | Free plus paid add-ons | AI auto-captions, smart matting, one-tap edits, a template and kinetic-typography ecosystem, tight integration with Douyin (抖音), lowest learning curve | Limited precision on complex effects and colour management, performance ceiling on large projects, batch reliability only average | Daily short-form output, MCN volume work, lightweight commercial projects |
| VEGAS Pro | Windows | About $219.95 one-time | Fast editing on Windows, comfortable audio workflow | Smaller cross-platform and collaboration ecosystem | Quick Windows edits, event films |
| Shotcut | Win / Mac / Linux | Free and open source | Lightweight, broad format support, no subscription, no watermark | No advanced collaboration or deep grading | Beginners, lightweight tasks, open-source preference |
| ffmpeg | Cross-platform CLI | Open source, free | Transcoding, muxing, filters, batch processing, automation, headless operation | No timeline editing, no GUI, unsuited to creative editing | Pipeline automation, proxy generation, subtitle muxing and burn-in |

Prices and versions are third-party review figures as of 2026 and are **TO VERIFY**; each vendor's own price on the day is authoritative.

## 3. Proxy and grading compared

| Application | Proxy approach | Grading capability | Collaboration / review |
| --- | --- | --- | --- |
| Final Cut Pro | Automatic proxies, zero configuration, parameters customisable through Compressor | Colour wheels + curves + LUTs; adequate but not cinema-grade | Weaker team collaboration ecosystem |
| DaVinci Resolve | Proxy and Optimized Media complete in the free version | **Strongest**: node-based, scopes, HDR, tracking, LUTs, film matching | Blackmagic Cloud projects with multiple roles |
| Premiere Pro | Proxy workflow plus Media Encoder pre-transcode; presets must be configured by hand, Proxy Helper can simplify it | Lumetri (wheels / curves / HSL secondaries); adequate for broadcast | Adobe Team Projects, Frame.io |
| Avid Media Composer | Traditional "transcode to DNxHD/DNxHR" rather than modern proxies; low-resolution media has to be linked manually | Basic correction; advanced work needs Symphony or a round trip to Resolve | Shared storage + bin locking, broadcast-grade |

Conclusion: **for grading, Resolve first** (many teams cut in another application and send everything to Resolve for grading); **for proxy workflow FCP is the least effort, the Resolve free version the most complete, Premiere Pro the most steps, and Avid the most traditional**.

### Plug-ins and collaboration ecosystem

| Category | Examples | Purpose |
| --- | --- | --- |
| Colour / look | Red Giant / Maxon (Magic Bullet Looks, Universe), Boris FX Sapphire | Film emulation, light effects, transitions, stylisation; hosts AE / PR / Resolve / FCP / Avid |
| Particles / motion graphics | Trapcode Particular / Form, Maxon Studio templates | Titles, brand animation, particle effects |
| Keying / compositing | Red Giant Keying, eKey, Real Lens Flares | Green-screen keying, lens flares |
| Audio repair | iZotope RX, Fairlight's built-in noise reduction | Noise reduction, de-essing, restoration |
| Review and collaboration | Frame.io, Adobe Team Projects, Blackmagic Cloud | Timecode notes, version management, remote grading handoff |

### Hardware and disk recommendations (third-party compilation; all TO VERIFY)

| Component | Recommendation | Rationale |
| --- | --- | --- |
| GPU | For Resolve at 4K, 8GB+ VRAM; for 6K RAW with stacked nodes, 16GB; the NVIDIA CUDA ecosystem is the mainstream | Grading, noise reduction and AI features lean heavily on the GPU |
| Memory | Start at 32GB; 64GB DDR5 is the comfortable zone for 4K multicam; stability matters more than clock speed | Multitrack playback and dynamic link are memory-hungry |
| Disks | **Three separate drives**: NVMe for the OS and applications, a media drive, and a dedicated NVMe for cache and proxies (Gen4 is enough, Gen5 gains little) | Stops cache, previews and autosaves contending for the same NAND and causing write-latency spikes |
| Arrays and network | HDD array or NAS for large capacities; 10Gbps+ network and SMB3 for team sharing | RAID 0 only adds speed and **has no fault tolerance, so a separate backup is mandatory** |
| Monitor | 4K, ≥95% DCI-P3, Delta E<2, hardware calibration; for HDR grading look for HDR1000 | Makes colour decisions trustworthy |

## 4. Procedure and workflow (commands verified on local ffmpeg 8.1.2)

```bash
# ① Generate a proxy copy (scaled down, low bitrate, for editing)
ffmpeg -y -i master.mov -vf "scale=960:-2" \
  -c:v libx264 -preset veryfast -crf 23 -c:a aac -b:a 128k proxy/proxy.mp4

# ② Batch-generate proxies (Bash)
mkdir -p proxy
for f in masters/*.mov; do
  ffmpeg -y -i "$f" -vf "scale=960:-2" -c:v libx264 -preset veryfast -crf 23 \
    -c:a aac -b:a 128k "proxy/$(basename "${f%.*}").mp4"
done

# ③ Conform check on the source: resolution, frame rate, codec
ffprobe -v error -show_entries format=duration,size:stream=codec_name,width,height,r_frame_rate -of json master.mov

# ④ Review-version output (uniform scaling and bitrate, for timecoded notes)
ffmpeg -y -i master.mov -vf "scale=1920:-2" -c:v libx264 -crf 18 \
  -c:a aac -b:a 192k review_v1.mp4

# ⑤ Extract the first frame as a ledger thumbnail
ffmpeg -y -ss 0 -i master.mov -frames:v 1 -q:v 2 thumb.jpg

# ⑥ Subtitle muxing and burn-in (feeds into the 03-subtitles pipeline)
ffmpeg -y -i master.mp4 -i subs.srt -map 0:v -map 0:a -map 1 \
  -c:v copy -c:a copy -c:s mov_text -metadata:s:s:0 language=chi deliver.mp4
ffmpeg -y -i master.mp4 -vf "subtitles=subs.srt" -c:v libx264 -c:a copy social.mp4
```

Key point: ffmpeg covers only the two ends of the pipeline (proxy generation, transcoding, muxing, burn-in, acceptance QC); **timeline editing and grading still belong in the NLE**. Proxy files are for editing only — relink the originals before output, and never treat a proxy as the delivery master.

## 5. Common errors and troubleshooting

| Symptom | Root cause | Fix |
| --- | --- | --- |
| Film looks soft, only 960 pixels wide | Originals were never relinked and the proxy was exported | Relink to the originals at conform, then export |
| A/V out of sync | 23.976 / 24 / 25 / 30 fps mixed, or inconsistent timebase | Check `r_frame_rate` per asset with ffprobe and unify the project frame rate |
| LOG footage looks grey | Technical LUT not applied, or colour management set wrong | Apply the LOG→Rec.709 technical LUT first, then do primary correction |
| LUT too heavy, skin tones fake | Strength pushed to 100% | Pull back to 60%-80% and trim per shot |
| Resolve stutters / spinning beachball | Not enough GPU memory | Lower the proxy resolution, clear the cache, disable heavy noise reduction, add VRAM if needed |
| Timeline drops frames on playback | Cache, previews and media crammed onto one drive | Separate the three drives and reset the Media Cache and Optimized Media paths |
| One dead drive loses everything on RAID 0 | RAID 0 treated as a backup | Keep an independent backup of the master and the project files |
| Project will not open once the subscription lapses | Continuity risk of subscription software | On archiving, export interchange formats (AAF/XML/EDL + finished MP4) |
| Cross-platform project will not open | PR / FCP / Avid project formats are not interchangeable | Exchange via AAF/XML/EDL, and record the font and plug-in versions alongside |
| Review version is colour-shifted against the master | The review transcode applied an extra colour transform | Keep the colour space identical in the review transcode; change only scale and bitrate |
| Burn-in with `-c copy` does nothing | Filters and stream copy are mutually exclusive | Re-encode the video with `-c:v libx264`; audio may stay `-c:a copy` |
| Subtitles / fonts look wrong on a colleague's machine | Font missing or a different version | Ship licensed fonts with the project and record the versions |

## 6. Quick checklist

- [ ] Primary NLE chosen on team collaboration / grading depth / platform and budget, with the outsourced step clearly identified
- [ ] Proxy specification (resolution, codec, path) fixed, and relinking to the originals confirmed before output
- [ ] Frame rate, colour space and technical LUT unified across the film
- [ ] Grading in the order primary → secondary → creative LUT (60%-80%), with skin tones checked on the vectorscope
- [ ] Plug-in host compatibility, version and licence confirmed (must match across machines)
- [ ] Review runs through Frame.io / Team Projects / Blackmagic Cloud, with timecoded notes
- [ ] Disks split three ways — system / media / cache — with an independent backup beyond RAID 0
- [ ] Archive contains interchange formats (AAF/XML/EDL) + finished film + font and plug-in list
- [ ] Every price, hardware threshold and third-party conclusion marked TO VERIFY and re-checked against the vendor's site
- [ ] Commercial licensing of fonts and assets re-checked by you (see 02 Stock assets and learning resources)

## References

- Best Professional Video Editing Software in 2026 (prices and positioning, TO VERIFY) — https://rankite.com/blog/best-professional-video-editing-software
- DaVinci Resolve Pricing, Features & Reviews (TO VERIFY) — https://umatechnology.org/davinci-resolve-pricing-features-reviews
- Top Professional Video Editing Tools 2026 (grading and hardware, TO VERIFY) — https://awingvisuals.com?p=16908/
- Side-by-side comparison of proxy workflows — https://dv123.cn/t/73889-1.html
- Mastering editing software and the practice of grading — https://www.skillsdirectory.com/skills/clowlove-marketing-short-video-editing-coach
- Red Giant / Maxon official site (plug-in host support) — http://www.redgiant.com/
- Hands-on test of separating Premiere Pro scratch disks (data TO VERIFY) — http://frameandfocal.com/post-processing/two-minor-changes-your-premiere-pro-setup-make-big-difference-when-editing-202172
- NLE workstation build list (hardware thresholds TO VERIFY) — https://www.kufanyun.com/ask/741419.html
- What Is an NVMe Scratch Disk — https://evezone.evetech.co.za/quick-bytes/what-is-an-nvme-scratch-disk-and-why-video-editors-need-one
- Which Hard Drive Should You Buy for Professional Video Editing? — https://www.itechfaqs.com/which-hard-drive-should-you-buy-for-professional-video-editing
- FFmpeg official documentation — https://ffmpeg.org/ffmpeg.html
- FFmpeg Filters Documentation — https://ffmpeg.org/ffmpeg-filters.html

Retrieved: 2026-11-10
