# The RSI Self-Improvement Mechanism · Overview and Design Principles

> Category: RSI self-improvement | Topic: what recursive self-improvement means here, the trigger protocol, the six-layer closed loop, the nine-step cycle and the safety guardrails | Compiled: 2026-11-10 | Applies to: the mandatory workflow whenever the instruction is "cut my footage in the style of this popular video"

> ⚠️ In this volume **RSI** means **Recursive Self-Improvement**: the system improves not only the result of a single edit but also the set of evaluation–mapping–review rules that produces the improvement. If you mean something else by it, say so first and I will realign.

---

## 1. The problem this solves

When a user says "cut my footage in the style of this hit video", three failures are the most likely:

| Failure mode | Symptom | Consequence |
| --- | --- | --- |
| **Impressionistic imitation** | Watching the reference and saying "fast pace, great energy, premium grade", then cutting by feel | The style never lands on parameters, so it cannot be reproduced, reviewed or attributed |
| **Borrowing at the level of expression** | Lifting the reference's shot order, signature sound effects or kinetic-typography styling wholesale | Crosses the idea/expression line and creates copyright and unfair-competition exposure |
| **One-off judgement** | Evaluating from scratch every time, retaining nothing learned last time | The twentieth task is as slow and as inaccurate as the first |

The mechanism answers each failure with one thing: **structured multi-dimensional evaluation, where every item must carry an explanation** → **a parameterised style fingerprint** → **feedback that flows back under guardrails**.

---

## 2. The P0 trigger protocol (mandatory, cannot be skipped)

When an instruction contains "reference / imitate / benchmark against / in the style of / make it feel like" and points at a specific video, enter the following state machine immediately:

```
[reference video received]
   → S1 Compliance pre-check: is the source legitimate? Is it used for analysis only, with none of its expression reused? (see the 05 volume + §6 of this volume)
   → S2 Objective probe: run scripts/reference_probe.sh for reproducible numbers
   → S3 Human / multimodal observation: review the contact sheets, listen to the whole track, mark timecodes
   → S4 Multi-dimensional evaluation: fill in templates/reference-video-evaluation.md (7 dimensions, a five-part explanation for each item)
   → S5 Synthesis: produce a style-fingerprint YAML + a one-page evaluation conclusion
   → S6 [USER CONFIRMATION GATE] hand the conclusion to the user to confirm or correct
        ├─ not confirmed / corrections raised → back to S4 to revise; editing still does not start
        └─ confirmed → S7
   → S7 Map to an edit plan (04) → execute the edit → review the finished cut (06 volume)
   → S8 Collect real feedback after publication → self-improvement record (05)
```

**Hard constraint**: `no edited output or final timeline may be produced before S6 is passed`. What is permitted: evaluating, asking questions, clarifying, and confirmation prompts such as "do you mean A or B?" This constraint is itself one of the guardrails that RSI cannot modify.

If you have only a link and no local file: state up front how the file will be obtained (user upload / compliant download) and what risk the platform's terms create. If you have only a text description, the evaluation drops to **low-confidence hypothesis mode**: every item is forced to "low" confidence, the fingerprint must carry `evidence_level: E4_assumed`, and this must be disclosed to the user explicitly at S6.

---

## 3. The six-layer architecture

| Layer | Name | Responsibility | Output | Self-modifiable? |
| --- | --- | --- | --- | --- |
| L0 | Perception | Objective probing + timecoded human observation | Cut list, loudness, colour statistics, contact sheets | No (the tools are fixed) |
| L1 | Evaluation | 7-dimension evaluation, with the five-part explanation enforced | Reference-video evaluation table | **Editable only after human confirmation** |
| L2 | Representation | Compress the evaluation into a parameterised style fingerprint | `sfp-v1` YAML | Fields may be added; mandatory fields may not be deleted |
| L3 | Execution | Fingerprint → edit plan → timeline | Edit plan, finished cut | Mapping weights adjustable (subject to the gate) |
| L4 | Review | Deviation comparison between the finished cut and the fingerprint + the 06 volume review | Deviation table, review table | **No** (standards may not be lowered) |
| L5 | Meta | Error attribution, generating candidate revisions, driving the evolution of L1/L3 | Candidate diffs, versions, regression results | **Bound by the nine-step gate** |

L5 is where the recursion lives: what it improves is not how one video gets cut, but the evaluation-dimension weights of L1 and the mapping rules of L3. Ordinary self-improvement only tunes L3 parameters; RSI is allowed to change the rules of L1/L3 themselves, once they are validated.

---

## 4. The nine-step self-improvement cycle

Use "observe → diagnose → propose → test → compare → approve → version → deploy → monitor"; a direct **observe → change → deploy** path is forbidden:

| # | Step | Action | Stop on failure |
| --- | --- | --- | --- |
| 1 | Observe | Record predictions (fingerprint parameters, expected effect) against what actually happened (platform data, user feedback, review deviations) | — |
| 2 | Diagnose | Attribute to L0 measurement / L1 evaluation / L2 representation / L3 mapping / source material / external environment | If attribution is unclear, record "unattributed" and do not proceed to the next step |
| 3 | Propose | Generate the **smallest candidate diff** (e.g. "opening-shot duration weight for short-form video +0.1"), with the source case ID attached | Reject any diff that exceeds the per-round drift bound |
| 4 | Test | Run the candidate against the frozen regression set and compare with the baseline | Reject if any single dimension falls below the baseline |
| 5 | Compare | Compare against the holdout set and the counterexample set; check that the proxy metric moves in the same direction as the real goal | Proxy up, real metric down → call it overfitting and reject |
| 6 | Approve | Submit for human confirmation with the evidence pack (regression results, diff, blast radius, rollback point) | **No effect without a signature** |
| 7 | Version | Issue a new version number and keep the previous version as last-known-good | — |
| 8 | Deploy | Shadow run first, then a small canary share, then full rollout | Roll back immediately if the canary metrics go abnormal |
| 9 | Monitor | Continuously monitor drift, resources and anomalies; keep the kill switch available | — |

A single case may produce **candidates only** and never changes a rule directly. "One hit video performed well" is never sufficient reason to change a rule.

---

## 5. The seven hard guardrails (the part of RSI that cannot modify itself)

The items below are the **immutable baseline**. No self-improvement round may alter, bypass or downgrade them; an attempt to do so fails the candidate on the spot and is written to the audit log:

1. **The P0 trigger protocol and the S6 user confirmation gate.**
2. **The mandatory-explanation constraint**: every evaluation must have observation / evidence / inference / action item / confidence, and an item missing any one of them is void (see `02`).
3. **Every compliance conclusion and disclaimer in the `05-copyright` volume** — they may not be relaxed on the grounds that "it was fine last time".
4. **Every blocking item and technical standard in the `06-delivery-qc` volume** (loudness, True Peak, A/V sync and so on).
5. **The frozen regression set and the holdout set**: evaluation assets and the self-improvement engine are kept under separate permissions, and the engine may not write to the evaluation set.
6. **Historical versions, counterexamples and the audit log**: append-only, never deleted, never overwritten.
7. **Per-round drift bound**: weight change ≤0.1, rule changes ≤2, and at most 1 candidate admitted to approval per round.

Supporting boundaries: resource caps (maximum analysis time and file count per task), separation of permissions (proposing, evaluating, approving and deploying are different roles), shadow runs first, and a kill switch that stops everything within seconds.

**Item 8 (introduced on 2026-11-10 by the `09-material-memory` volume; the original seven keep their numbering)**: **the objective layer of a material description card is read-only.** The `E1`/`E2` fields of `mdc-v1` (content hash, timecode facts, location evidence, objective measurements, clearance status) may not be rewritten automatically by the self-improvement engine; a correction can only be made by human confirmation, producing `card_version+1` and retaining a `corrections` entry. The only things the engine may propose changing are the analysis prompt templates, the field weights and the topic-adaptation rules — and those still go through the nine-step gate and a human signature. The reason: a cache propagates one error into every later topic, and the hit record still looks perfectly normal, which makes it very hard to notice. See `../09-material-memory/04-integration-with-rsi-and-other-volumes.md`.

---

## 6. Compliance precondition: style may be borrowed, expression may not be copied

This boundary has to be drawn before the reference video is evaluated, because it determines which dimensions are **allowed** into the fingerprint:

- Copyright law's idea/expression dichotomy: expression is protected, ideas, concepts, formulas and methods are not. Expert commentary republished by the National Copyright Administration of China (国家版权局) draws a clear line between "borrowing an idea and creating anew" and "copying a formed expression"; the Hubei Copyright Protection Center (湖北省版权保护中心) likewise holds that standardised story formulas belong to the level of ideas.
- **Extractable** (written into the fingerprint): shot-duration distribution, cut density, rhythm curve, transition-type mix, loudness target, SFX density, colour tendency, structural proportions, emotion curve — these are parameters and structure.
- **Not extractable** (forbidden in the finished cut): the specific content of shots, signature lines of dialogue, distinctive character design and styling, the original music and sound-effect assets, the exact wording and unique graphics of kinetic typography, and recognisable replication of the shot staging.
- The test: if the two videos were shown side by side, and a viewer could say "this is the same piece of content performed again", you have crossed the line; if the viewer only feels "the rhythm and the mood are alike", you are still at the level of style.
- Infringement practice commonly applies "access + substantial similarity", and substantial similarity compares the **selections, choices, arrangements and designs within the expression**, not the subject, the idea or the emotion. A reference video is a publicly released hit, so "access" is almost certainly established — which is all the more reason to stay strictly inside the parameter layer.

> This section constrains the creative workflow; it is not legal advice. Have counsel review high-risk projects; see `../05-copyright/`.

---

## 7. How this fits the other seven volumes

| Existing volume | Role in this mechanism |
| --- | --- |
| `01-editing-craft` | Source of the criteria for dimension A (180°, 30°, match cuts, J/L-cut) |
| `02-audio-and-voice` | Criteria and loudness conventions for dimension B (EBU R128 / streaming targets) |
| `03-subtitles` | Criteria for dimension D (character count, dwell time, format) |
| `04-genre-playbooks` | Determines which category the reference video belongs to, and which structural template to compare against |
| `05-copyright` | The authoritative basis for the §6 compliance precondition and the "borrowable boundary" |
| `06-delivery-qc` | The L4 review layer; `qc_scan.sh` compares objective metrics of the finished cut against the reference |
| `07-tools-and-resources` | Probing tools, software and material sources |
| `00-overview` | The same source-reliability grading applies to this volume's evaluation conclusions |

---

## 8. Meta-metrics: how to know the mechanism is actually getting better

One metric alone is not enough (it invites overfitting). Watch at least four groups at once:

| Group | Metric | Note |
| --- | --- | --- |
| Evaluation quality | Completeness rate of the five-part explanation (target 100%), share of E1 objective evidence, first-pass rate at S6 | Explanation completeness is a hard threshold, not a KPI |
| Predictive power | Deviation between fingerprint predictions and measured values in the finished cut (median shot duration, cut density, loudness) | Converging deviation = the evaluation is getting more accurate |
| Outcome quality | Real platform feedback (completion rate / retention / conversion) + the user's own confirmation + the 06 volume review pass rate | Multiple signals, and proxy metrics must move with the real goal |
| System health | Candidate rejection rate, rollback count, number of rule versions, counterexamples retained, drift amount | A high rejection rate is not bad news; it means the gate is working |

**Warning signals**: proxy metrics rising steadily while real feedback stays flat → suspected overfitting; internal scores suspiciously smooth with no external improvement → suspected contamination of the evaluation set; the same change accepted and rolled back repeatedly → oscillation, so lower the learning rate and enforce a cooldown.

---

## 9. Common errors and troubleshooting

| Error | Correct approach |
| --- | --- |
| Starting to cut right after watching the reference | Complete S2–S6 first; the timeline does not move until the evaluation is confirmed |
| Using "looks good / premium / has texture" as a conclusion | Five-part explanation, landing on executable parameters |
| Carrying over the reference's music, kinetic type or shots | Extract parameters and structure only; see §6 |
| Changing a rule after one hit | Produce a candidate only, and take it through the nine-step gate |
| Driving self-improvement with a single completion rate | Four meta-metric groups + holdout set + counterexamples |
| Letting the self-improvement engine also hold write access to the evaluation set | Separate permissions; freeze the evaluation set |
| Deleting historical cases that "did not work" | Counterexamples must be retained, or the system systematically overestimates |

---

## 10. Quick reference

- [ ] P0 triggered; input form confirmed (file / link / description only)
- [ ] Compliance pre-check done and the "borrowable boundary" explained
- [ ] `reference_probe.sh` run and objective metrics saved
- [ ] 7-dimension evaluation table complete, each item with a five-part explanation + confidence
- [ ] `sfp-v1` style fingerprint produced with all fields present
- [ ] **S6 user confirmation** — no editing before it is given
- [ ] Mapped to an edit plan → edit → 06 volume review
- [ ] Prediction vs. actual recorded; candidate diff generated (not applied directly)
- [ ] Regression set / holdout set / human approval / versioning / canary / monitoring
- [ ] All seven hard guardrails confirmed untouched

---

## References

- arXiv, "Your Agent May Misevolve: Emergent Risks in Self-evolving LLM Agents" (2509.26354): https://arxiv.org/html/2509.26354v2
- AI Governance Institute, "Self-Evolving AI Agents Break the Assumption Underlying Every Change Control": https://aigovernance.com/news/self-evolving-ai-agents-break-the-assumption-underlying-every-change-control
- Lyzr, "What Is an AI Agent Self-Improvement Loop?" (the nine-step loop, memory tiers, levels of human involvement): https://www.lyzr.ai/blog/ai-agent-self-improvement-loop/
- Future AGI, "Self-Improving AI Agents: A Pre-Deployment Checklist 2026" (regression baseline, drift bounds, shadow/canary, kill switch): https://futureagi.com/blog/self-improving-ai-agents-pre-deployment-checklist-2026/
- Datarekha, "Recursive self-improvement" (immutable baseline, proxy over-optimisation, separation of permissions): https://datarekha.com/gen-ai/recursive-self-improvement
- National Copyright Administration of China (国家版权局), "How Media Should Protect Copyright in the 5G Era" (《5G时代媒体该如何保护版权》) (the idea/expression dichotomy and re-creation by borrowing ideas): https://www.ncac.gov.cn/xxfb/yjdt/201909/t20190923_49648.html
- Hubei Copyright Protection Center (湖北省版权保护中心), "Infringement Risk in Micro-Drama 'Meme-Merging' and Free-Riding" (《微短剧“融梗”“搭便车”现象须注意侵权风险》): https://www.ccct.net.cn/html/bqzx/2024/0620/5221.html
- Procuratorate Daily (检察日报), "Copycat Short Videos Grab Traffic: How Are Original Creators' Rights Protected" (《仿拍短视频抢流量 原创者权益如何保障》) (access + substantial similarity): http://newspaper.jcrb.com/2023/20230911//20230911_004/news-zgjcb-10331-20230911-m-004-300.pdf

Retrieved: 2026-11-10. Most of the governance sources above are 2026 industry articles and preprints: they are methodological references, not codified standards, and should be adjusted to your own risk level before adoption. The legal statements do not constitute legal advice.
