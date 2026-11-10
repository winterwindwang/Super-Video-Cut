# 09 · Material memory and description cache

> Category: Material memory | Topic: One video-model call produces a reusable material description, and later topics read the cache directly | Compiled: 2026-11-10 | Applies to: Any task that involves analysing, understanding, or adopting a piece of video material — above all where the same material is adopted repeatedly by several topics

> ⚠️ This volume is a reference for creative and engineering workflows and **does not constitute legal advice**. Licence, likeness, location, and provenance information in a card must be reviewed by a human; for commercial projects, have legal review it. See `../05-copyright/`.

**In one sentence**: let the video model watch a piece of material exactly once. Then write **what it shows, where it was shot, what it looks like, and whether it can be used** into a structured material description card (MDC) on disk; from that point on, no matter how many topics, how many days, or how many sessions later, check the cache first and — on a hit — read the card. **The video model is never asked again.**

---

## P0 protocol (pin this to the wall)

```
Received "cut an XX-topic video from this material" or "analyse this material"
  → M1 compute the content fingerprint (material_cache.py fingerprint)
  → M2 check the cache (material_cache.py lookup)
       ├─ HIT  → ★ do not call the video model again ★
       │         read cards/<MID>.yaml directly; make only the light "topic adaptation" judgement
       │         write one use record (topic / clip used / purpose)
       └─ MISS → run local objective probing first (ffprobe + reference_probe.sh / qc_scan.sh)
               → make exactly one full description request with templates/model-analysis-prompt.md
               → fill templates/material-description-card.yaml → register to write the cache
               → then move on to topic adaptation
  → M3 if the bytes change / the description is disproved / the licence expires → invalidate and redo, or mark blocked
```

**Four non-negotiables**:
1. **A hit means read-only**: after a HIT, the same file must not be sent for video understanding again; if something genuinely needs supplementing, prefer local means (frame extraction, ASR, ffprobe), write the result back into the card, and record a `reason`.
2. **Write it all at once**: the single model request on a MISS must ask for everything — "content / location / style / usability / timecode events" — and must not be split into repeated asks for different topics.
3. **Keep the objective and the adaptation apart**: the description of the material itself (the MDC) is permanent and topic-independent; how a given topic uses it (the topic adaptation layer) is stored separately and never written back to contaminate the MDC.
4. **A description is not a licence**: the `rights` block in a card is only a ledger pointer; whether the material may be used still goes through `../05-copyright/` and `../06-delivery-qc/02`.

---

## The three-layer structure, and why the layers exist

| Layer | What it stores | Does it change with the topic? | Lifecycle |
| --- | --- | --- | --- |
| **L0 file identity layer** | Content hash, byte count, ffprobe specs, aliases and paths | No | Valid forever as long as the bytes do not change |
| **L1 material description layer (MDC)** | What it shows, where it was shot, what it looks like, visual and audio facts, usability | **No** | One card per item; corrections add versions, never overwrite |
| **L2 topic adaptation layer** | Which seconds this topic uses, in what narrative role, why it fits, how it performed | **Yes** | One record per material × topic, appended without limit |

> The user's own words were "one piece of material can be adopted by many different topics at once" — which is exactly why L1 and L2 have to be separate layers. Write "good for a nostalgic opening" into L1, and the moment the topic becomes "tech review" that description turns into noise, or worse, into a trap.

**Where the boundary with Volume 08 lies** (the easiest thing to get wrong):

| | Reference-video evaluation (Volume 08) | Material description card (this volume) |
| --- | --- | --- |
| Object | Someone else's viral video, used to **extract style parameters** | Your own material headed for the timeline, used to **understand the content** |
| Purpose | "Why does this film look good?" → style fingerprint `sfp-v1` | "What is in this piece of material?" → description card `mdc-v1` |
| Depth | 7 dimensions, 30+ items, five-part notes for each, S6 user confirmation gate | 4 groups of factual fields + style inference notes, human spot check |
| Reuse | Usually one-off; the conclusions enter the rule library | **High-frequency reuse; a hit means read** |
| One file serving both roles | Allowed, but the evaluation sheet and the MDC must be produced separately, with the two IDs cross-referencing | Same as left |

---

## Contents

| File | Contents |
| --- | --- |
| **`01-material-description-card-spec.md`** | ★ Full `mdc-v1` field dictionary, evidence grades E1–E4 (identical to Volume 08), the four groups content / location / style / usability, the mandatory form for style notes, 8 validation rules |
| **`02-cache-reuse-protocol-and-token-savings.md`** | ★ Hit and invalidation decisions, the write-it-all-at-once prompt strategy, token estimation and accounting, concurrency and idempotency, privacy and the kill switch |
| `03-multi-topic-adaptation-and-references.md` | The reference model for one material across many topics, adaptation fields, conflict resolution, reference counts and revocation, correction write-back |
| `04-integration-with-rsi-and-other-volumes.md` | Material memory as the RSI L0 persistence layer, how description corrections enter the nine-step gate, the no-automatic-rewrite guardrail, library-wide routing |
| `templates/material-description-card.yaml` | The empty `mdc-v1` card (machine-readable, for tool registration) |
| `templates/material-description-card.md` | Human-readable filling guide + one complete worked example |
| **`templates/model-analysis-prompt.md`** | ★ The prompt for that one model request: asks all five dimensions at once and demands structured output |
| `templates/topic-adaptation-record.md` | The L2 record, one per material per topic |
| `scripts/material_cache.py` | Zero-dependency Python tool: fingerprint / lookup / register / use / verify / stats / themes / validate |
| `cache/README.md` | Cache directory structure, `index.csv` / `usage.csv` fields, privacy and append-only conventions |

---

## How much a single call saves (estimation basis)

Google's official documentation for static video processing: 1 FPS sampling by default; at low `media_resolution`, 66 tokens per frame plus 32 tokens per second of audio, roughly **100 tokens per second of video**; at high resolution, 258 tokens per frame, roughly **300 tokens per second**. A separate official Firebase document gives another basis of **263 tokens per second** (different version and scope — marked TO VERIFY).

On that basis, **a 3-minute piece of material costs about 18,000 input tokens at low resolution**. If it is adopted by 4 topics (the initial `MISS` doubles as the first topic, followed by 3 `HIT`s):

| Approach | Video-model requests | Estimated video input tokens |
| --- | --- | --- |
| No cache, re-watch for every topic | 4 | 72,000 |
| Vendor Files API / context caching | 4 (still billed each time; only bandwidth or unit price improves) | 4 billed at the cached unit price, subject to TTL expiry |
| **The MDC cache in this volume** | **1** | **18,000** |

How `stats` computes it: `hit rate = HIT/(HIT+MISS) = 3/4 = 75%`, `estimated saving = Σ(HIT × est_tokens) = 3 × 18,000 = 54,000`, consistent with the no-cache baseline `72,000 − 18,000 = 54,000`; the general form is `1 − 1/N` (N being the number of topics). If card creation is treated as a standalone step bound to no topic, there is one extra `HIT` and the statistics skew slightly optimistic, which is normal.

The saving is not an exact invoice figure: the table counts video input tokens only, excluding prompt, output, and reasoning tokens. The real saving is whatever `usage_metadata` returns, and the tool can write measured values into `usage.csv`. **Vendor-side caching and the caching in this volume stack; they are not an either/or choice.**

---

## Command quick reference

```bash
PY="scripts/material_cache.py"

# 1. Ask the cache first (step one before analysing any material)
python "$PY" lookup "D:/footage/sunset-beach.mp4"

# 2. On a miss: local objective probing (costs no model tokens)
bash "scripts/reference_probe.sh" "D:/footage/sunset-beach.mp4" /tmp/probe
ffprobe -v error -show_format -show_streams -of json "D:/footage/sunset-beach.mp4"

# 3. One full description with the template prompt → fill the MDC → register
python "$PY" register "D:/footage/sunset-beach.mp4" --card "/tmp/MID-xxx.yaml" --model "<model name>" --tokens 18000

# 4. Reuse from any later topic: record one adaptation, never touch the model
python "$PY" use "D:/footage/sunset-beach.mp4" --theme "T-2026-autumn-nostalgia" --clip "00:00:03-00:00:08" --note "opening B-roll"
python "$PY" use "D:/footage/sunset-beach.mp4" --theme "T-2026-climate-science" --clip "00:00:12-00:00:19" --note "cloud-layer illustration"

# 5. Health check and statistics
python "$PY" verify "D:/footage/sunset-beach.mp4"
python "$PY" themes "D:/footage/sunset-beach.mp4"
python "$PY" stats
```

When `lookup` prints `HIT`, the output includes an explicit line: "**do not call the video model again**". That is a hard reminder to the operator, not a suggestion.

---

## Quick reference

- [ ] Run `lookup` before analysing any material; on a HIT, read the card directly
- [ ] On a MISS, probe locally first, then send the "write it all at once" prompt to the model
- [ ] All four card groups are present — content / shooting location / style / usability — each with an evidence grade
- [ ] Location and identity are never guessed without support; mark them `E3 inference` or `E4 assumption`
- [ ] Style inferences use the five-part form (observation / basis / inference / action item / confidence)
- [ ] `register` only enters the store after `validate` passes; corrections produce `v+1` and never overwrite the old version
- [ ] Write a `use` record for every reuse; topic adaptation is never written back into the MDC
- [ ] On licence expiry, mark `blocked` instead of deleting the card; Table C in `06-delivery-qc/02` still needs a human signature
- [ ] The savings in `stats` are estimates; reconcile the invoice against `usage_metadata`

---

## References

- Google AI for Developers, "Video understanding" (1 FPS sampling, 66/258 tokens per frame, 32 tokens/s of audio, roughly 100/300 tokens per second, guidance on the Files API and context caching): https://ai.google.dev/gemini-api/docs/video-understanding
- Google, "Context caching" (implicit and explicit caching, TTL, the repeated-analysis-of-long-video scenario): https://ai.google.dev/gemini-api/docs/caching
- Firebase AI Logic, "Count tokens for Gemini models" (video at 263 tokens/s, audio at 32 tokens/s — an alternative basis): https://firebase.google.com/docs/ai-logic/count-tokens
- Content-Hash File Cache Pattern (chunked SHA-256 content hashing, path-independence, automatic invalidation on content change, corrupted entries treated as misses): https://lobehub.com/ru/skills/sehoon787-my-claude-content-hash-cache-pattern
- EBUCore / PBCore audiovisual metadata standards (layering of descriptive, technical, and rights metadata; separation of assets from instantiations): https://msi.dublincore.org/standards/ebucore , https://msi.dublincore.org/standards/pbcore
- MPEG-7 and an overview of AV archive metadata (temporal structure, scenes, colour and motion descriptors): https://www.nedcc.org/fundamentals-of-av-preservation-textbook/chapter-4-introduction/chapter-4-section-5
- This volume's `01`–`04`; `../08-rsi/01` (six-layer architecture and hard guardrails), `../06-delivery-qc/02` (material ledger)

Retrieved: 2026-11-10. Token prices, model versions, and vendor billing bases change frequently and are **volatile information**; re-check the latest official documentation before use. All ratios in this volume are our own estimation basis.
