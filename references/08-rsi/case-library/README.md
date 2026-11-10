# Case-Library Index

> Category: RSI self-improvement | Topic: case registration, rules versions and global configuration | Compiled: 2026-11-10 | Applies to: the archiving entry point for every reference-video evaluation and self-improvement task

> ⚠️ This document is a reference for the creative workflow and **does not constitute legal advice**; for decisions involving clearance and compliance, see the 05-copyright volume and have counsel review.

---

## Directory conventions

```
case-library/
├── README.md              ← this file (the index, append-only)
├── _config.yaml           global switches and version pointer (the kill switch lives here)
├── _rules/                rules-library versions rules-vN.yaml + CHANGELOG.md
├── _frozen/               frozen regression set / holdout set / BASELINE.md (read-only or hidden from the engine)
├── _audit/                append-only audit log audit-YYYY.md
├── _counterexamples/      rejected candidates and failed cases (retained permanently)
└── CASE-YYYYMMDD-NNN/     a single case: evaluation + fingerprint + probe log + edit plan + review form + self-improvement record
```

See `../06-case-library-and-version-governance.md` for details.

---

## Case index table (append one row per new case; never delete a row)

| Case ID | Date | Reference video / type | Fingerprint ID | Rules version | Stage completed | Real feedback | Self-improvement outcome |
| --- | --- | --- | --- | --- | --- | --- | --- |
| _(no cases yet)_ | | | | | | | |

For "Stage completed" enter: `S2 probed / S5 evaluated / S6 confirmed / S7 delivered / S8 feedback collected`.

---

## Rules-version table

| Version | Date | Status | Source candidate | Gate result | Signature |
| --- | --- | --- | --- | --- | --- |
| `rules-v1` | 2026-11-10 | `last-known-good` (initial baseline) | — | initial | — |

Allowed status values: `candidate` / `active` / `last-known-good` / `retired`.

---

## Initial contents of `_config.yaml`

```yaml
evolution_enabled: true
active_rules_version: rules-v1
last_known_good: rules-v1
learning_rate_eta: 0.05
max_drift_delta: 0.1
min_support_n: 5
cooldown_days: 7
frozen_set_write_allowed: false
```

**kill switch**: set `evolution_enabled` to `false` and point `active_rules_version` back at `last_known_good` to disable self-improvement globally. The operation needs no recomputation and no retraining; see §6 of `../05-feedback-loop-and-self-improvement.md`.

---

## Steps for adding a case

1. Create the directory `CASE-YYYYMMDD-NNN/`.
2. Run `scripts/reference_probe.sh <reference video> <this case's directory>`, which produces `probe.log` / `probe.json` / `metrics.csv` / `cuts.txt` / `shot_lengths.txt` / `loudness.txt` / `silence.txt` / `yavg.txt` / `satavg.txt` / `sheet_*.png`.
3. Copy `../templates/reference-video-evaluation.md` and `../templates/style-fingerprint.yaml` into this directory and fill them in.
4. Once the S6 user confirmation is complete, produce `edit-plan.md` (format: §5 of `../04`).
5. After delivery, fill in `qc-review.md` (using `../../06-delivery-qc/03-qc-report-templates.md`).
6. Once real feedback has been collected, fill in `../templates/self-improvement-record.md` → `self-improvement-record.md`.
7. Append one row to the index table in this file; if a rule change was approved, keep `_rules/`, `CHANGELOG.md` and `_audit/` in step.

---

## Frozen sets and baselines

| Set | Target size | Current | Permissions |
| --- | --- | --- | --- |
| `_frozen/regression/` | ≥10 cases | 0 | engine read-only, maintained by hand |
| `_frozen/hidden/` | 3 cases | 0 | not visible to the engine, not writable |
| `_counterexamples/` | all rejected candidates | 0 | append-only |

`_frozen/BASELINE.md` records the baselines of the four meta-metric groups (evaluation quality / predictive power / outcome quality / system health). **No rule change may be approved before the frozen set exists** — without a regression baseline there is no gate.

---

## References

- `../06-case-library-and-version-governance.md` (directories, naming, versions, audit, rollback)
- `../05-feedback-loop-and-self-improvement.md` (gates and the kill switch)
- `scripts/reference_probe.sh` (inventory of probe artefacts)

Retrieved: 2026-11-10.
