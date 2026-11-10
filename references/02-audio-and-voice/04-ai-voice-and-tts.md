# AI Voice-over and TTS in Practice

> Category: Audio and voice | Topic: TTS engine selection, SSML and pronunciation control, voice-cloning compliance, hybrid AI and human workflows | Compiled: 2026-11-10 | Applies to: Batch narration / multilingual voice-over, digital-human presentation, audiobooks, commercial projects that require licensed synthetic speech

## Core principles

Modern TTS has reached **end-to-end neural synthesis** (Transformers capture long-range semantic dependencies) and can read a turn in the sentence — a "but", a concession — and reflect it in the intonation. The goal, though, is "natural enough", not "indistinguishable from a human" (100% natural is a real recording). Quality is decided at three levels: **engine and voice** (the acoustic foundation), **text preprocessing** (sentence splitting, polyphonic characters, number reading, abbreviation expansion — often more effective than switching engines), and **SSML control** (pauses, rate, emphasis, pronunciation). A robotic tone, odd pauses, and a rushed ending usually come from the **script**, not the engine.

Voice cloning turns a voice into a contractual asset: a short audio sample is enough to replicate a voiceprint, which makes licensing, consent, disclosure, and provenance more important than any technical parameter. Compliance is procedural: define the use → choose a stock voice or a custom voice with consent → prepare clean licensed material → generate and edit in segments → human review → keep a full audit trail.

## Specifications and parameter tables

### Table 1 Capabilities and selection of mainstream TTS engines (compiled from 2026 tutorials; metrics TO VERIFY)

| Engine / family | Representative voices | Strengths | Limits |
| --- | --- | --- | --- |
| Azure Neural TTS | zh-CN-XiaoxiaoNeural / YunxiNeural | Full SSML, polyphonic character tagging, stable on long text, MOS≈4.2/5, first packet ≈120 ms | Complex configuration, usage-based billing, network setup needed in mainland China |
| Google Cloud TTS | cmn-CN-Wavenet / Neural2 | Fine prosody control, rate 0.25-4.0×, free tier about 1 million characters/month | Network setup needed in mainland China |
| Amazon Polly | Neural | Near-complete SSML plus extensions (breath / whisper / DRC) | Fewer Chinese voices |
| Volcano Engine TTS (火山引擎) | Technical-domain voices | Accurate terminology; rate 0.9-1.0 with SSML | Requires code integration |
| Edge TTS / CapCut / Dingding | Xiaoxiao, Yunxi, and others | Free and easy, smart pauses 0.3-0.8 s | Some do not support SSML; abbreviation reading is unreliable |
| ElevenLabs | Multilingual + cloning | Strong emotion, Stability slider | Chinese quality and commercial terms need assessment |
| Qwen3-TTS and other open source | End-to-end neural | Can be self-hosted, data never leaves the intranet | Deployment cost |

### Table 2 Selection criteria (more important than "who is best")

| Criterion | What to check |
| --- | --- |
| Pronunciation | Names, abbreviations, brands, dates, currency, foreign words, technical terms, code |
| Timing and prosody | Pauses, stress, rate, rhythm, sentence endings, lists |
| Speaker consistency | Does timbre or style drift across requests / paragraphs / chapters / regenerations |
| Controllability | SSML / explicit controls / prompts / multi-speaker; can the same request be reproduced |
| Runtime behaviour | Time to first packet, completion time, concurrency and throughput, P50/P95/P99, retries |
| Workflow fit | Batch mode, export formats, API, version pinning, logs, commercial terms |
| Cost | Per-character or per-minute billing plus retries, regeneration, storage, and review across the board |

Method: use **one test script containing polyphonic characters, numbers, punctuation, and abbreviations**, test 3 voices per vendor plus short/medium/long inputs, record the voice ID, settings, date, and output, and have a native speaker review.

### Table 3 Speaking rate, sentence segmentation, and text preprocessing

| Item | Parameter |
| --- | --- |
| Narration / tutorial rate | 0.9-1.1× |
| News reading / fast-paced | 1.2-1.5× |
| Long-form audiobook | 0.85-0.95× |
| Pitch adjustment | Within ±5% (more than that distorts) |
| Sentence length | Chinese <=20 characters per sentence (15-20 words in English) |
| Inter-sentence pause | 0.3-0.8 s breath break |
| Long text | Generate in segments; never submit 2000 characters at once, and hard-cutting by character count causes timbre drift between segments |
| Normalization | Expand abbreviations (WHO → World Health Organization); write dates and IDs the way they are spoken |
| Emotion control | `<prosody>` / `<emphasis>` or engine style tags, applied in small increments |

Typical polyphonic cases: the character 行 in 银行 (bank) versus 行走 (to walk). Typical number cases: whether 2026 is read as "two zero two six" or "two thousand and twenty-six", whether -23 is read as "minus two three" or "minus twenty-three" — both must be specified explicitly.

### Table 4 Core SSML tags (vendor subsets differ; verify on the target platform)

| Tag | Purpose | Main attributes / values |
| --- | --- | --- |
| `<speak>` | Root element | Wraps the whole passage |
| `<voice>` | Switch voice | `name` |
| `<break>` | Insert a pause | `time="500ms"` / `"1s"`; `strength` = none/x-weak/weak/medium/strong/x-strong (about 0/250/500/750/1000/1500 ms) |
| `<prosody>` | Pitch / rate / volume | `rate` (x-slow..x-fast or 80%/120%), `pitch` (x-low..x-high or ±%), `volume` (silent..x-loud or ±dB) |
| `<emphasis>` | Word-level stress | `level` = strong / moderate / reduced / none |
| `<say-as>` | Number/date reading | `interpret-as` = characters / cardinal / ordinal / digits / date / time / telephone / currency |
| `<phoneme>` | Force an IPA pronunciation | `alphabet="ipa"`, `ph="..."` |
| `<sub>` | Substitute spoken text for displayed text | `alias="..."` |
| `<p>` / `<s>` | Paragraph / sentence boundaries | Improves prosodic structure |
| `<audio>` | Insert pre-recorded audio (Polly and others) | `src` |
| Vendor extensions | Azure `<mstts:express-as>` (cheerful/empathetic/customerservice), Polly `<amazon:breath>` / `<amazon:effect>` | Not portable between engines |

SSML example (ASCII straight quotes):
```
<speak>
  <voice name="zh-CN-XiaoxiaoNeural">
    <prosody rate="0.95">
      This episode covers the <say-as interpret-as="cardinal">2026</say-as> loudness standards,
      <break time="400ms"/>
      targeting <say-as interpret-as="digits">-23</say-as> LUFS.
    </prosody>
    <sub alias="中国工商银行">工行</sub> and <phoneme alphabet="ipa" ph="ɕiŋ">行</phoneme>业 must both be checked.
  </voice>
</speak>
```

> Note: the millisecond mapping of `<break strength>` is approximate; only `time="500ms"` gives a precise, reproducible timeline. XML must be well-formed — a malformed tag makes the whole passage fail to parse.

### Table 5 Keeping speaking rate in sync with subtitle length

| Item | Method |
| --- | --- |
| Estimating | Chinese narration runs about 160-180 characters/min ≈ 2.7-3 characters/s; `duration (s) = character count / characters per minute * 60` |
| Subtitles | Aim for <=15-18 characters per line and >=1.2 s on screen (rule of thumb, TO VERIFY) |
| Alignment | Read the actual audio duration with `ffprobe` and build the timeline from it — **not** from the theoretical duration |
| Handling conflicts | If the subtitle is too cramped, raise `rate` or condense the copy; never squeeze the on-screen time |
| Consistency | Normalize every segment to the same LUFS before splicing; the same voice and settings can still differ in level across sessions |

### Table 6 Voice-cloning consent and ethical risk

| Item | Requirement |
| --- | --- |
| Consent | **Written, explicit, traceable**: specific / time-bound / revocable / use category; verbal consent is not enough for commercial use |
| Scope of licence | Language, use, platform, territory, term, exclusivity; how already-published material is handled after withdrawal must be written into the contract |
| Legal frameworks | EU AI Act (transparency obligations from 2025), GDPR (voiceprints are biometric data, Article 9), the US NO FAKES Act and similar (clause status TO VERIFY; consult a lawyer) |
| Platform rules | Clone only yourself or people who have given written consent; never clone celebrities (not even for parody or private use); embed a watermark in generated files |
| Cloning threshold | ElevenLabs Instant about 1 minute, Professional about 30 minutes of clean audio (third-party source, TO VERIFY) |
| Provenance / retention | C2PA watermark, generation logs, provenance; take withdrawn material down within 48 hours; retain evidence (agreement, licence, disclosure, invoice, settings, revision history) for about 12 months (industry practice, not a universal regulation) |
| Disclosure / prohibitions | Label advertising explicitly as "AI-generated voice" — on-camera delivery is stronger than text alone; never treat public audio as a free training set |

### Table 7 Hybrid AI and human workflow

| Use AI | Use a human |
| --- | --- |
| Large volume, structured, repeatable: onboarding prompts, product tutorials, accessibility audio, internal training, short-line libraries, multilingual expansion of an approved master | Nuanced interpretation, credible celebrity association, live creative feedback, emotionally complex characters, irony / trauma / comic timing / moral ambiguity, the one line that changes the meaning of a whole scene |

Hybrid approach: a human sets the character and direction (master performance), and the model extends it within the same licence; multilingual versions are generated after the human master is approved and reviewed by native speakers. Decision threshold: compare **20 representative lines**, counting recording, editing, licensing, and re-record costs; if it saves no review time and adds rights exposure, it is not the right tool. Keep fallback recordings and a backup vendor.

### Table 8 QC checklist

| Item | Threshold / method |
| --- | --- |
| Pronunciation | Listen line by line for polyphonic characters, names, abbreviations, numbers, terminology; fix with `<phoneme>` / `<sub>` |
| Prosody | Sentence length <=20 characters, pauses 0.3-0.8 s; no machine-gun delivery, rushed ending, or overlong pause |
| Consistency | Timbre / rate / loudness drift across paragraphs; normalize each segment to the same LUFS first |
| Artifacts | De-ess sibilance and metallic ringing with a de-esser plus a narrow notch at 5-9 kHz; do not over-compress |
| Splices | 10-30 ms crossfade at the joins; fill with continuous room tone |
| Loudness | Per the delivery platform target (see document 02); measure Integrated over the whole programme |
| Subtitles | Align the timeline to the ffprobe-measured duration; listen once at normal volume and once low |
| Multiple devices | Three systems: headphones + speakers + phone speaker |
| Compliance | Consent form, licence scope, disclosure, second-person review, and retained evidence all in place |

## Procedure / Workflow (commands tested locally on ffmpeg 8.1.2)

### A. Text and generation
1. Write a "spoken script": short sentences, full punctuation, abbreviations expanded, polyphonic characters and number readings marked.
2. Use the Table 2 test script to select an engine, then lock and record the voice ID and model version.
3. **Generate sentence by sentence or segment by segment**; regenerate any segment you are unhappy with on its own.
4. For precise control, apply the SSML from Table 4, after verifying the tag subset on the target platform.

### B. Splicing and post-processing
Splice multiple segments (tested `concat` filter):
```
ffmpeg -i seg1.wav -i seg2.wav -i seg3.wav -filter_complex "[0:a][1:a][2:a]concat=n=3:v=0:a=1[out]" -map "[out]" -ar 48000 -c:a pcm_s24le vo.wav
```
Normalize each segment first (tested `loudnorm`):
```
ffmpeg -i seg.wav -af "loudnorm=I=-16:TP=-1.5:LRA=11" -ar 48000 -c:a pcm_s24le seg_norm.wav
```
Unify the rate (tested `atempo`, range 0.5-2.0):
```
ffmpeg -i vo.wav -af "atempo=1.05" -ar 48000 -c:a pcm_s24le vo_fast.wav
```
Remove splice seams (10-30 ms crossfade, tested `acrossfade`):
```
ffmpeg -i a.wav -i b.wav -filter_complex "[0:a][1:a]acrossfade=d=0.02:c1=tri:c2=tri[out]" -map "[out]" -ar 48000 -c:a pcm_s24le out.wav
```

### C. QC and subtitle sync
```
ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 vo.wav
```
```
ffmpeg -hide_banner -i vo.wav -af "silencedetect=n=-40dB:d=0.3" -f null - 2>&1
```
### D. Compliance review
Synthetic audio involving a real person's voice is reviewed by **someone other than the person who generated it**, checking the evidence and the disclosure, and re-checking platform policy before publishing.

## Common errors and troubleshooting

| Error | Consequence | Fix |
| --- | --- | --- |
| Reading an unpunctuated long text straight through | Machine-gun delivery, no pauses | Split into sentences of <=20 characters, add punctuation |
| Leaving polyphonic characters or numbers unmarked | Mispronunciation | `<phoneme>` / `<say-as>` / text normalization |
| Generating the whole piece in one request | Timbre drift in later sections, no local fixes | Segment the generation and regenerate individually |
| Splicing segments with mismatched loudness | Level jumps | Normalize each segment to the same LUFS first |
| Odd pauses / rushed ending | Unnatural | Regenerate line by line, assemble in an editor |
| Fixing a robotic tone by fiddling with the engine | Marginal gains | Fix the script first: short sentences, punctuation, a touch more expressiveness |
| Fighting sibilance / metallic artifacts with heavy compression | Makes it worse | De-esser + narrow notch at 5-9 kHz |
| Cloning a real voice without written consent | Civil or criminal exposure | Stop using it; obtain a licence or switch voices |

## Quick reference

- [ ] Engine / voice / model version evaluated on a single test script and documented
- [ ] Spoken script: short sentences, punctuation, abbreviations, polyphonic characters, and number readings all marked
- [ ] Generated in segments; SSML tags verified on the target platform
- [ ] Each segment normalized to the same LUFS before splicing, 10-30 ms crossfade at the joins
- [ ] Subtitle timeline aligned to the ffprobe-measured duration
- [ ] Pronunciation, prosody, artifacts, and multi-device playback all checked against Table 8
- [ ] Cloned voice: consent, licence scope, disclosure, second review, and retained evidence all in place
- [ ] Synthetic audio labelled per platform policy, evidence folder archived

## References

- Tahou (塔猴), TTS tutorial — https://www.tahou.com/article/202895101396364293
- CSDN, Choosing voice-over software — https://blog.csdn.net/luoboorz/article/details/166994490
- Sekin, How to Choose a Modern TTS Model — https://sekin.in/text-to-speech-solutions-how-to-choose-a-modern-tts-model
- OfflineTTS, SSML Complete Guide — https://offlinetts.com/blog/ssml-complete-guide/
- Typecast, Best SSML Support APIs — https://typecast.ai/learn/best-api-ssml-support
- Txtory, SSML Generator — https://txtory.com/text-utilities/text-to-speech-ssml-generator
- Decagon, What Is SSML — https://decagon.ai/glossary/what-is-ssml
- ElevenLabs Avis, Voice cloning: safety, rights — https://elevenlabs-avis.com/en/blog-3
- CloneMyVoice, AI Voice Actors Rights 2026 — https://clonemyvoice.io/knowledge/how_do_you_create_ai_voice_actors_without_infringing_anyones_rights_in_2026.php
- Audobox, AI Voice Compliance Checklist — https://audobox.com/knowledge/what_is_the_ai_voice_compliance_checklist_for_creators_in_2026.php
- Audobox, Ethical Guidelines for Voice Cloning — https://audobox.com/knowledge/what_are_the_current_ethical_guidelines_for_ai_voice_cloning_in_2026.php
- Domer AI, Using AI Voice for Video — https://domer.io/blog/ai-voice-video-creation-guide
- Domer AI, Improve Audio Quality in AI Video — https://domer.io/blog/improve-audio-quality-ai-video-voice-music
- FFmpeg official documentation — https://www.ffmpeg.org/ffmpeg-filters.html

Retrieved: 2026-11-10

**TO VERIFY**: ① The engine metrics in Table 1 (MOS 4.2/5, first packet about 120 ms, Google free tier about 1 million characters/month, rates and pricing) come from 2026 third-party tutorials and must be confirmed against the vendors' current documentation and your own tests; ② The ElevenLabs Instant/Professional cloning durations (about 1 / about 30 minutes) come from third-party blogs; ③ The status of EU AI Act Article 50, the NO FAKES Act, and GDPR Article 9 has not been checked against the statutory text; consult a local lawyer for legal conclusions; ④ C2PA watermarking, log retention, and taking material down within 48 hours of withdrawal are industry best practice, not universal regulation; ⑤ SSML vendor tag subsets differ (Azure `mstts` / Polly `amazon` extensions are not portable), and the millisecond mapping of `<break strength>` is approximate — the example must be verified on the target platform; ⑥ The per-line character count and on-screen duration for subtitles are rule-of-thumb values; ⑦ Cloning licence scopes, commercial terms, and free quotas change at any time; re-check platform policy before publishing.
