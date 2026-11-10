# Self-Improvement Record (one per task)

> Category: RSI self-improvement | Topic: leaving a trail of predicted vs actual feedback, attribution, candidates and gates | Compiled: 2026-11-10 | Applies to: stage S8, written to `case-library/<CASE-ID>/self-improvement-record.md`

> ⚠️ This document is a reference for the creative workflow and **does not constitute legal advice**; for decisions involving clearance and compliance, see the 05-copyright volume and have counsel review.

> ⚠️ Self-improvement may not start without real feedback; passing an internal review counts only as a diagnostic signal, not as "it got better". A single case produces candidates only — it never changes a rule directly.

---

## 0. Related information

| Field | Entry |
| --- | --- |
| Case ID / fingerprint ID | |
| Rules-library version used | `rules-vN` |
| Task date / recorded by | |
| Feedback collection date / time window | |
| Are all four signal groups available | ☐ Platform data　☐ User confirmation　☐ L4 deviation　☐ Review pass rate |

---

## 1. Prediction (from the fingerprint and the edit plan)

| Rule ID | Prediction | Quantified expectation | Confidence |
| --- | --- | --- | --- |
| R-___ | | | |
| R-___ | | | |

---

## 2. Actual observation

| Signal group | Metric | Value | Data source / time window | External confounders |
| --- | --- | --- | --- | --- |
| ① Platform metrics | Completion rate / retention / conversion / views | | | Promotion, time of day, thumbnail, topic momentum |
| ② User confirmation | Subjective verdict / adopted or not / corrections | | | — |
| ③ L4 deviation | Shot duration / density / loudness / brightness deviation | | Finished cut compared against the fingerprint | — |
| ④ Review | Review verdict from the 06 volume / number of blocking items | | | — |

---

## 3. Error attribution (mandatory)

| Rule ID | Predicted vs actual | Attribution category | Reason |
| --- | --- | --- | --- |
| | | A measurement / B evaluation / C representation / D mapping / E execution / F external / unattributed | |

> If the attribution is **E execution / F external / unattributed**, stop here and generate no candidate.

---

## 4. Candidate revisions (one minimal diff each)

| Candidate ID | Field changed | Before → after | Basis cases (≥5 in the same direction) | Support | Drift | Cooldown | Expected impact | Rollback point |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CAND-___-01 | `derived_rules[].weight` | | | | ≤0.1 | ☐ Not violated | | `rules-vN` |

Weight calculation (optional):

```
error_r  = __        # clip(normalize(observed - predicted), -1, 1)
support  = __        # min(1, n_same / 5)
recency  = __        # 0.9 ^ (Δt_days / 30)
Δw       = 0.05 * error_r * conf_r * support * recency
w_cand   = __        # and |w_cand - w_old| <= 0.1
```

**Hard-guardrail confirmation**: ☐ P0 confirmation gate　☐ Mandatory-explanation constraint　☐ 05 volume compliance verdict　☐ 06 volume blocking items　☐ Frozen set read-only　☐ History / counterexamples / logs not deleted　☐ Drift bound and per-round item count

---

## 5. Nine-step gate results

| # | Step | Result | Evidence / value | Rejection reason |
| --- | --- | --- | --- | --- |
| 1 | Observe | ☐ Pass ☐ Awaiting feedback | All four signal groups present | |
| 2 | Diagnose | ☐ Pass ☐ Stop | Attribution category | |
| 3 | Propose | ☐ Pass ☐ Rejected | Minimality / support / drift | |
| 4 | Test on the frozen regression set | ☐ Pass ☐ Rejected | Four meta-metric groups vs baseline, none down by ≥2% | |
| 5 | Compare on the holdout set | ☐ Pass ☐ Rejected | Holdout-set performance; proxy and real metrics moving in the same direction | |
| 6 | Approve (human sign-off) | ☐ Pass ☐ Awaiting signature | Evidence pack: regression results / diff / blast radius / rollback point | |
| 7 | Version | ☐ Done | New version / `last-known-good` retained | |
| 8 | Deploy | ☐ Shadow ☐ Canary ☐ Full rollout ☐ Rollback | Shadow ≥3 cases, canary ≤20% | |
| 9 | Monitor | ☐ Normal ☐ Abnormal | Drift, rejection rate, kill switch available | |

**Pass threshold**: at least one primary metric improves by ≥3%, and no metric falls by ≥2%.

| Signatory | Name | Date |
| --- | --- | --- |
| Proposer (engine / evaluator) | | |
| Evaluator (regression run) | | |
| Approver (human, must differ from the proposer) | | |
| Deployment | | |

---

## 6. Decision

| Item | Content |
| --- | --- |
| Final decision | ☐ Approve deployment　☐ Reject　☐ Hold for observation　☐ Roll back |
| New rules-library version / `last-known-good` retained | |
| Audit-log line (copied to `_audit/audit-YYYY.md`) | |
| Counterexample ID (mandatory on rejection, written to `_counterexamples/`) | `CX-___-__` |
| Reason for the counterexample and evidence retained | |
| Follow-up validation plan | |

---

## 7. Meta-metric update (for cross-case monitoring)

| Metric | Value for this case | Baseline | Trend |
| --- | --- | --- | --- |
| Completeness rate of the four-part explanation per evaluation item | | 100% | |
| Share of E1 objective evidence | | | |
| S6 first-pass rate | | | |
| Prediction deviation of fingerprint parameters | | | |
| Candidate rejection rate / number of rollbacks | | | |

**Warning-sign check**: ☐ Proxy improves while the real metric falls　☐ Internal scores suspiciously smooth　☐ Repeatedly accepting then rolling back similar changes　☐ Candidate rejection rate stuck at 0　☐ Proposals that touch a hard guardrail

---

## References

- `../05-feedback-loop-and-self-improvement.md` (attribution categories, the weight formula, the nine-step gate)
- `../06-case-library-and-version-governance.md` (audit log, versions and rollback)
- `../01-overview-and-design-principles.md` (the seven hard guardrails and the meta-metrics)

Retrieved: 2026-11-10.
