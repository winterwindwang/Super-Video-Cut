# Working with RSI self-evolution and the other volumes

> Category: Material memory | Topic: Wiring material memory into the RSI six-layer architecture, cross-session persistence, guardrails, and library-wide routing | Compiled: 2026-11-10 | Applies to: Assembling Volumes 00–09 into a callable editing skill; and every task where a reference video and your own material appear together

> ⚠️ This volume is a reference for creative and engineering workflows and **does not constitute legal advice**. Compliance and review conclusions are governed by `../05-copyright/` and `../06-delivery-qc/`; for commercial projects, have legal review them.

---

## 1. "Remembering" means writing to disk, not keeping it in context

When the user says "you need to remember this", the phrase has a precise technical meaning in this knowledge base:

| Form of memory | How long it survives | After a change of topic or session | Choice in this volume |
| --- | --- | --- | --- |
| Conversation context | A single session, bounded by the context window | Lost | ✗ |
| Model parameters (fine-tuning / memory features) | Long, but unauditable and not reversible | Unexplainable | ✗ |
| **File-based description card + content-hash index** | Permanent, diffable, reversible, greppable | **Fully preserved** | ✓ |

So "remember what the material shows, where it was shot, and what it looks like" lands in `cache/cards/<MID>.yaml`, identity lands in `index.csv`, and every reuse lands in `usage.csv` and `themes/<MID>.csv`. Any new session that can read this directory has the whole memory; nothing depends on my "happening to remember".

This matters especially for RSI: the self-evolution in Volume 08 depends on **historical inputs that stay comparable across tasks**. If every act of material understanding leans on ad-hoc context, the "input" in the regression set is simply not reproducible, and step 4 of the nine-step gate — "run the candidate against the frozen regression set" — has nothing to run on. The MDC turns the input snapshot into a static file, and only then does regression become possible.

---

## 2. Plugging into the RSI six-layer architecture

| RSI layer (Volume 08) | Original responsibility | What Volume 09 adds |
| --- | --- | --- |
| **L0 perception layer** | Objective probing + timecoded observation | **Persistence**: `fingerprint` + ffprobe + `reference_probe.sh` results written into MDC `identity` / `style.measured`, so one measurement serves the whole project |
| L1 evaluation layer | 7-dimension reference-video evaluation + five-part notes | MDC `style.style_notes` uses the same note constraints and E1–E4 grades, keeping the basis consistent |
| L2 representation layer | `sfp-v1` style fingerprint | `mdc-v1` description cards; the two cross-reference through `source_material_ids` and are **not merged** |
| L3 execution layer | Fingerprint → edit plan → timeline | The L2 topic adaptation layer supplies "which material, in what role, cut how" — the direct input to execution |
| L4 review layer | Deviation check between the finished film and the fingerprint + Volume 06 review | `verify` and `rights_status` act as review preconditions; `blocked/unknown` is a hard stop |
| L5 meta layer | Error attribution, candidate revisions, rule evolution | Hit rate, description accuracy, STALE rate, and topic `outcome` become new attribution signals |

Volume 08 defines L5 as "improving L1 evaluation weights and L3 mapping rules". Volume 09 adds no new self-modifiable layer; it only supplies **reproducible inputs and observable signals** — precisely the foundation L5 had been missing.

---

## 3. The complete trigger flow once merged

When an instruction contains both "reference the style of this viral video" and "use this material of mine":

```
S1 Compliance first (08/01 §6 + Volume 05): analyse the reference only, never reuse its expression
M1 fingerprint every item of owned material
M2 lookup
     ├─ HIT  → read the MDC, 0 model requests
     └─ MISS → local E1 probing → one full model request → validate → register
S2 Run reference_probe.sh on the reference video (Volume 08)
S3 Watch the whole film twice + go frame by frame through key sections
S4 Fill in the Volume 08 evaluation sheet (7 dimensions, five-part notes for each)
S5 Produce the sfp-v1 style fingerprint + a one-page conclusion
     ★ The conclusion must list the "material available for this film" — cite MDC affordances
       directly and do not launch another model analysis of the material
S6 ★ User confirmation gate ★ (no finished film is output without it)
S7 Mapping: fingerprint parameters × MDC facts × L2 topic adaptation → edit plan → timeline
        every use record writes (mid, theme, clip, role)
S8 Volume 06 finished-film review + verify → release feedback → Volume 08 self-evolution record (a candidate; not applied directly)
```

**M2 must come before S4**: knowing what material you actually hold is the precondition for judging, while evaluating the reference, whether "my material can carry this style parameter" (the "material downgrade" step in 08/04). Reverse the order and you lock in a rhythm you cannot achieve, then have to rework.

---

## 4. Additional guardrail (supplements §5 of Volume 08 without renumbering its seven rules)

Volume 08 lists seven immutable baselines. With caching introduced, Volume 09 **adds one constraint that the self-evolution engine may not modify on its own**:

> **8. The L1 objective description layer is read-only**: the `E1`/`E2` fields of `mdc-v1` (identity, content facts, timecodes, location documentation, objective measurements, rights status) must not be rewritten automatically by the self-evolution engine. Corrections may only be made by a human, producing `card_version+1` and leaving `corrections` behind. What the engine may propose changing is the prompt template, field weights, and adaptation-layer rules — and those must pass through the nine-step gate and a human sign-off.

The reason: a cache amplifies a single error into every topic that follows. Were the engine allowed to change the fact layer whenever it "thinks it is more accurate", errors would spread as the hit rate rose — and the `HIT` rows in `usage.csv` would look entirely normal, making the problem very hard to find.

Four supporting operating constraints:
- After a `HIT`, no further video-understanding request may be made against the same file (the supplementary path is in `02` §4).
- An MDC must not contain topic names, project names, or usage conclusions (V8).
- While the rights status is anything other than `cleared`, no self-evolution experiment may add that material to a regression set or a training set.
- `cache/audit.log` and `usage.csv` are append-only and receive the same protection as "historical versions and audit logs" in Volume 08.

---

## 5. New meta-metrics (folded into the four groups in §8 of Volume 08)

| Group | New metric | Definition | Warning signal |
| --- | --- | --- | --- |
| Evaluation quality | **Description accuracy** | Quarterly spot check of the E2 facts and timecodes on ≥10 cards, compared against the original footage | Below 95%, pause automatic reuse and inspect the prompts |
| System health | **Cache hit rate** | `HIT / (HIT + MISS)` | Persistently low → the hashing basis or the directory configuration is wrong, or material is being replaced constantly |
| System health | **STALE rate** | `STALE / total lookups` | High → material management is chaotic; put versions in order before discussing evolution |
| Resource | **Estimated tokens saved** | `Σ HIT × duration × rate` | For trend observation only; **never an optimisation target** (it invites indiscriminate reuse purely to inflate the hit rate) |
| Outcome quality | **Topic `outcome` distribution** | Ratio of adopted to dropped, with reason categories | One class of material repeatedly dropped → the `affordances` tag definitions need fixing |

Important: hit rate and tokens saved are **efficiency metrics**, not quality metrics. Treating them as KPIs invites gaming such as "forcing a hit even though the material has changed" — a textbook case of proxy-metric over-optimisation (already flagged in Volume 08 §8).

---

## 6. Library-wide routing table

| Existing volume | Interface with Volume 09 |
| --- | --- |
| `01-editing-craft/03` engineering standards | `identity.aliases` aligns with project naming; `edit_notes.handles_frames` follows its handles convention |
| `02-audio-and-voice` | L2 `audio_handling` refers to its loudness basis; the MDC `audio` block records whether native sound is usable |
| `03-subtitles` | `content.onscreen_text` and `spoken.transcript_ref` are inputs for transcription and proofreading |
| `04-genre-playbooks` | The L2 `narrative_role` maps onto the segment positions in each genre's structure template |
| `05-copyright` | Supplies the basis for `provenance` / `rights_status` / `releases` / `privacy_flags`; **a card is not a rights conclusion** |
| `06-delivery-qc` | `qc_scan.sh` output fills `quality_issues` / `qc_ref`; the Table C material ledger can be drafted from `index.csv`, but still needs a human signature |
| `07-tools-and-resources` | Checking material sources and licence types; ffmpeg/ffprobe are the tools that execute E1 measurements |
| `08-rsi` | Six-layer architecture, five-part notes, E1–E4, the nine-step gate, append-only auditing, the S6 confirmation gate; `reference_probe.sh` is reused as the MDC's E1 probe |
| `00-overview` | The same source-credibility grading applies; `manifest.csv` registers every document and script in this volume |

---

## 7. Minimum call sequence when shipped as a skill

If the whole library is packaged as a callable skill, the minimum execution contract for anything involving material is:

```
1. Input: a list of material paths + (optional) reference video + topic ID
2. for each item: fingerprint → lookup
3. if any MISS: local E1 probing first, then one full model request → validate → register
4. Output a "material inventory summary": one line each = MID + summary + place + style keywords + affordances + rights_status
5. If there is a reference video, enter Volume 08 S1–S6; only after confirmation use the step-4 inventory for shot selection
6. Write a use record for each selected shot; verify + Volume 06 review before delivery
7. Feedback writes outcome; produces candidates only, never changes the MDC fact layer
```

Step 4 is exactly what the user means by "just read the description of the video": written once, shared across topics, readable, greppable, and auditable.

---

## 8. Common errors and troubleshooting

| Error | Correct approach |
| --- | --- |
| Keeping memory in the conversation, so it is forgotten with the session | File-based MDC + index; `lookup` first in every session |
| Evaluating the reference film before looking at your own material | M2 before S4, or you will only discover the material cannot carry the style after the style is locked in |
| Letting the self-evolution engine edit MDC facts | Forbidden; human correction produces `v+1` and leaves a trace |
| Treating the hit rate as a quality KPI | It is an efficiency metric; quality is description accuracy and `outcome` |
| Using the MDC in place of a rights review | The card is only a ledger pointer; Table C still needs a human signature |
| Merging the MDC and the style fingerprint into one file | They cross-reference by ID but have different responsibilities; merging lets "reference-film evaluation" and "material description" contaminate each other |
| Using material with `rights_status: unknown` in the regression set | Exclude it; clear the licence first |

---

## 9. Quick reference

- [ ] Memory is persisted under `cache/`, never dependent on conversation context
- [ ] In the merged flow, M2 precedes S4, and the S6 confirmation gate has not been bypassed
- [ ] Guardrail 8 is in force: the engine cannot rewrite E1/E2 fields automatically
- [ ] The new meta-metrics are folded into the four groups in Volume 08 and are not treated as quality KPIs
- [ ] The MDC and `sfp-v1` cross-reference by ID and are not merged
- [ ] Every item in the regression set has a `cleared` rights status
- [ ] `audit.log` / `usage.csv` are append-only and backed up regularly
- [ ] Both `verify` and the Volume 06 review pass before delivery

---

## References

- `../08-rsi/01-overview-and-design-principles.md` (six-layer architecture, nine-step loop, seven hard guardrails, meta-metrics)
- `../08-rsi/05-feedback-loop-and-self-improvement.md` (error attribution, drift prevention, kill switch)
- `../08-rsi/06-case-library-and-version-governance.md` (frozen sets, append-only auditing, rollback)
- `../06-delivery-qc/02-content-and-compliance-review.md` (material ledger and the rights chain)
- arXiv, "Your Agent May Misevolve: Emergent Risks in Self-evolving LLM Agents" (proxy over-optimisation, immutable baselines, memory-contamination risk): https://arxiv.org/html/2509.26354v2
- Lyzr, "What Is an AI Agent Self-Improvement Loop?" (memory layering and levels of human involvement): https://lyzr.ai/blog/ai-agent-self-improvement-loop/
- Google, "Video understanding" (reproducible inputs and timecode verification): https://ai.google.dev/gemini-api/docs/video-understanding
- This volume's `01`, `02`, `03`

Retrieved: 2026-11-10. Guardrail 8, the five new meta-metrics, and the merged flow are conventions defined by this knowledge base, not industry standards; the governance sources are largely 2026 industry articles and preprints, and serve as methodology references rather than codified standards.
