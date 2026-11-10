# Case Library and Version Governance

> Category: RSI self-improvement | Topic: case archive structure, naming, rule versions, audit and rollback | Compiled: 2026-11-10 | Applies to: keeping every evaluation, edit and self-improvement task traceable and recoverable

> ⚠️ This document is a reference for the creative workflow and **does not constitute legal advice**; for decisions involving clearance and compliance, see the 05-copyright volume and have counsel review.

---

## 1. Why governance is part of RSI

A self-improving system without version governance is not "improving", it is "drifting". The industry consensus is blunt: every self-modification must leave an immutable audit record, an identifiable known-good version, and a tested rollback path — otherwise approval, retrospective attribution and incident response all lose their footing.

This volume reduces governance to four checkable things: **directory layout, file names, version numbers and log format**.

---

## 2. Directory structure

```
08-rsi/
├── case-library/
│   ├── README.md                   case index table (a sub-file of this volume)
│   ├── _config.yaml                global switches and rules-library version pointer
│   ├── _rules/                     rules-library versions
│   │   ├── rules-v1.yaml           (initial baseline, last-known-good)
│   │   ├── rules-v2.yaml
│   │   └── CHANGELOG.md
│   ├── _frozen/                    frozen regression set + holdout set (no engine write access)
│   │   ├── regression/            ≥10 cases, human-annotated baselines
│   │   ├── hidden/                3 cases, never used in candidate generation
│   │   └── BASELINE.md            baseline values for the four meta-metric groups
│   ├── _audit/                     append-only audit log
│   │   └── audit-2026.md
│   ├── _counterexamples/           rejected candidates and failed cases (retained permanently)
│   └── CASE-YYYYMMDD-NNN/          single case: three-piece set + outputs
│       ├── evaluation.md
│       ├── style-fingerprint.yaml
│       ├── probe.log / probe.json / sheet.png
│       ├── edit-plan.md
│       ├── qc-review.md
│       └── self-improvement-record.md
```

**The three-piece set may not be split**: `evaluation` + `style fingerprint` + `probe log` reference each other through `source_case`; without any one of them the case may not enter the regression set.

---

## 3. Naming conventions

| Object | Format | Example |
| --- | --- | --- |
| Case ID | `CASE-YYYYMMDD-NNN` | `CASE-20261110-001` |
| Fingerprint ID | `SFP-YYYYMMDD-NNN` | `SFP-20261110-001` |
| Rules version | `rules-vN` | `rules-v3` |
| Candidate diff | `CAND-<CASE-ID>-NN` | `CAND-CASE-20261110-001-01` |
| Counterexample | `CX-<CASE-ID>-NN` | `CX-CASE-20261110-001-01` |
| Audit log | `audit-YYYY.md` | `audit-2026.md` |

File names never contain spaces; Chinese directory names keep this knowledge base's existing convention; dates use `YYYYMMDD` so that they sort cleanly.

---

## 4. Rules-library version governance

`_rules/rules-vN.yaml` holds the official version and weights of `derived_rules`. The fields match the `derived_rules` in `03`, plus:

```yaml
version: rules-v3
created: 2026-11-10
parent: rules-v2
status: last-known-good        # candidate | active | last-known-good | retired
source_cases: [CASE-20261110-001, CASE-20261110-004, ...]
candidate: CAND-CASE-20261110-004-01
gate_results:
  regression: pass
  hidden_eval: pass
  human_signoff: "Zhang San / 2026-11-10"
rollback_to: rules-v2
rules: [ ]
```

**Rules**:
- Every approval produces a new version number; **never overwrite in place**.
- At any moment there is exactly one `last-known-good`, and that version can be neither deleted nor modified.
- `status` lifecycle: `candidate → active → last-known-good → retired`; a rolled-back version is marked `retired` with the reason written out.
- Each `CHANGELOG.md` entry records: `version / date / candidate ID / what changed / basis cases / gate results / signatory / rollback point`.

`_config.yaml`:

```yaml
evolution_enabled: true          # kill switch: false disables everything globally at once and returns to last-known-good
active_rules_version: rules-v3
last_known_good: rules-v3
learning_rate_eta: 0.05
max_drift_delta: 0.1
min_support_n: 5
cooldown_days: 7
frozen_set_write_allowed: false  # the engine never has write access
```

---

## 5. Audit-log format (append-only)

`_audit/audit-YYYY.md` has one line per entry; historical lines may not be edited or deleted:

```markdown
| 2026-11-10 15:02 | CAND-CASE-20261110-004-01 | propose R-003 weight 0.5→0.58 | basis CASE-001/002/004/007/009 | regression pass / hidden pass | approved Zhang San | deployed rules-v4 shadow | rollback point rules-v3 |
| 2026-11-10 15:40 | CAND-CASE-20261110-004-02 | propose relaxing the shot-duration tolerance | basis CASE-004 only | regression fail (evaluation quality −3.1%) | rejected → CX-...-02 | — | — |
```

Six mandatory fields: time / candidate ID / change / basis / gate results / decision and signature. A record missing any of them is invalid, and the corresponding version may not be deployed.

---

## 6. Rollback procedure

1. Trigger conditions: canary anomaly, significant regression in real feedback, an audit finding that a guardrail was touched, or the kill switch being flipped manually.
2. Immediately point `active_rules_version` in `_config.yaml` back to `last-known-good` and set `evolution_enabled: false`.
3. Append a line to the audit log recording the trigger, the time and the blast radius.
4. Mark the rolled-back version `retired` with the reason written out; **keep its files and the candidate diff**.
5. Produce a `CX-*` counterexample with the offline versus live data compared.
6. Accept no same-direction candidate during the cooldown; self-improvement may only be re-enabled after the retrospective is complete and a human has signed off.

Rollback is **one configuration change**; it does not depend on recomputation or retraining.

---

## 7. Frozen set and holdout set

| Set | Size | Purpose | Maintained by | Engine access |
| --- | --- | --- | --- | --- |
| Frozen regression set | ≥10 cases | Check whether a candidate degrades any dimension | Human | **Read-only** |
| Holdout set | 3 cases | Detect proxy over-optimisation and evaluator contamination | Human | **Invisible, unwritable** |
| Counterexample set | All rejected candidates | Prevent repeat proposals and systematic overestimation | Engine appends, human reviews | Append-only |

`BASELINE.md` records the baselines of the four meta-metric groups (evaluation quality / predictive power / outcome quality / system health), and every regression is compared against them; a change to the baseline itself requires a human signature and retention of the old values.

---

## 8. Archiving and retention

- Every case retains at minimum: the evaluation table, the fingerprint, the probe log and contact sheets, the edit plan, the qc review table and the self-improvement record.
- Whether to retain the reference video **itself** depends on clearance and storage cost; if it is not kept, the evaluation table must state how it was obtained and where the key-frame stills live, so the conclusions stay reviewable.
- Files involving clearance evidence, appearance releases and review signatures are archived with the case, retained for no less than the work's publication cycle plus the dispute look-back period (see `../06-delivery-qc/03-qc-report-templates.md`).
- The case index (`case-library/README.md`) gains one row per new case; rows are never deleted.

---

## 9. Staying in sync with the library-wide index

When a case or a rules version is added, only the `case-library/README.md` index needs updating; `../SKILL.md` and `manifest.csv` do **not** need to change (they record capabilities and documents, not case data). But if a **document or script** in this volume is added, deleted or renamed, these must be updated in step:

- the routing table in `../SKILL.md` (only when a separate topic or a new script is added)
- `00-overview/manifest.csv` (paths relative to the references root)
- the capability-domain table in `00-overview/knowledge-map.md`
- `00-overview/sources-and-reliability.md` (if a new source or a new TO VERIFY item is introduced)

---

## 10. Quick reference

- [ ] The case's three-piece set is complete and cross-referenced through `source_case`
- [ ] Naming follows the convention and contains no spaces
- [ ] Rule versions are only ever added, never edited, and `last-known-good` is unique
- [ ] The kill switch in `_config.yaml` is available and has been verified
- [ ] Frozen and holdout sets are read-only and their baselines recorded
- [ ] Audit-log entries carry all six fields and are append-only
- [ ] Every rejected candidate has a `CX-*` counterexample
- [ ] The rollback procedure has been rehearsed once, with the rehearsal written to the audit log
- [ ] The index table is in sync with the library-wide index

---

## References

- arXiv, "Your Agent May Misevolve" (immutable audit logs, versioning and rollback, continuous monitoring): https://arxiv.org/html/2509.26354v2
- AI Governance Institute (change management, recoverable state, audit trail): https://aigovernance.com/news/self-evolving-ai-agents-break-the-assumption-underlying-every-change-control
- Future AGI, "Pre-Deployment Checklist 2026" (versioned artefacts, retaining the previous version, shadow and canary): https://futureagi.com/blog/self-improving-ai-agents-pre-deployment-checklist-2026/
- This volume, `01` and `05`; `../06-delivery-qc/03-qc-report-templates.md` (archiving checklist)

Retrieved: 2026-11-10. The directory layout and parameters are conventions defined by this knowledge base, not industry standards.
