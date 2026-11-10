# Feedback Return and the Self-Improvement Algorithm (bounded RSI)

> Category: RSI self-improvement | Topic: error attribution, candidate revisions, weight updates, the nine-step gate and drift prevention | Compiled: 2026-11-10 | Applies to: after each task is finished and real feedback has been collected; the L5 meta layer

> ⚠️ This document is a reference for the creative workflow and **does not constitute legal advice**; for decisions involving clearance and compliance, see the 05-copyright volume and have counsel review.

> ⚠️ The core constraint of this volume: **a single case may produce candidates only and never changes a rule directly**. Every self-improvement must pass through the gate, obtain a human signature and produce a new version. Any direct "observe → change → deploy" path is a violation.

---

## 1. Data flow

```
evaluation table + fingerprint (prediction)
   → edit plan (including downgrades and conflict rulings)
   → finished cut + 06 volume review + L4 deviation table
   → real feedback after publication (platform data / user comments / repeat purchase and reuse)
   → [self-improvement record] prediction vs. actual
   → error attribution
   → candidate diff (no effect yet)
   → nine-step gate
   → new rules-library version or rejection (counterexample archived)
```

**Without real feedback**, self-improvement must not start. The task may be marked `pending_feedback`, but "I think it turned out well" may not stand in for observation. Passing the review and meeting the L4 deviation tolerance are **internal signals**: they serve diagnosis and do not prove that anything "got better".

---

## 2. Self-improvement record fields

One record per task, written to `case-library/<CASE-ID>/self-improvement-record.md` (template in `templates/self-improvement-record.md`):

| Field | Description |
| --- | --- |
| `case_id` / `sfp_id` / `rules_version` | Links the three-piece set to the rules version in use |
| `predictions` | The expected effect of each active rule (quantifiable ones preferred) |
| `observed` | Platform data + user confirmation + measured L4 deviation + the 06 volume review verdict |
| `signal_sources` | Where the data came from, the time window, the sample size, and whether delivery, time slot, cover image or other external factors interfered |
| `attribution` | The attribution conclusion (see §3); "unattributed" must be written down as well |
| `candidate_diffs` | The minimal revision proposal, with blast radius and rollback point |
| `gate_results` | The result, evidence and rejection reason for each of the nine steps |
| `decision` | Approved / rejected / pending observation; signatory and date |
| `counterexample` | If rejected, retained permanently as a counterexample |

**Multi-signal principle**: record at least ① platform quantitative data, ② the user's own confirmation, ③ L4 deviation and ④ review pass rate together. Driving rule changes on completion rate alone is the most typical entry point to overfitting.

---

## 3. Error attribution categories (diagnose before proposing)

| Category | Typical symptom | Which layer to touch | Self-improvement allowed |
| --- | --- | --- | --- |
| **A Measurement error** | Probe-log values disagree with human re-check; false-positive cut points | L0 tool parameters (thresholds) | Yes, but threshold changes also go through the gate |
| **B Evaluation error** | The item is fully explained but the conclusion is wrong; low confidence treated as a hard constraint | L1 dimension weights / confidence thresholds | Yes |
| **C Representation error** | The fingerprint loses a key relationship (only the mean kept, the curve dropped) | L2 field structure | Requires human approval (structural change) |
| **D Mapping error** | Scaling or adaptation is unreasonable; the conflict ruling was wrong | L3 mapping rules and weights | Yes; this is the main object of operation |
| **E Execution error** | The plan was right but the edit did not follow it, or the export parameters were wrong | **Do not change the rules**; fix the execution | No |
| **F External environment** | Delivery time slot, cover image, topic momentum, platform algorithm change, material quality | **Do not change the rules** | No |

Attribution is **mandatory**. When it is unclear, write "unattributed" and stop at step 2 without generating a candidate. In practice a large share of "it did not perform well" turns out to be E or F; letting the self-improvement engine rewrite the rules only bends them further out of shape.

---

## 4. Rules for generating a candidate revision

A candidate must satisfy:

1. **Minimality**: change one thing per round (one weight, one threshold, or one rule's `status`).
2. **Attributability**: bind at least `N_min = 5` **same-direction** attribution samples, and those samples may not all come from the same video or the same account.
3. **Quantifiability**: state the before value, the after value, the expected impact and the rollback point.
4. **No contact with the hard guardrails** (see `01` §5).
5. **Per-round drift bound**: weight change `|Δw| ≤ 0.1`; rule changes ≤2; at most 1 candidate admitted to approval per round.
6. **Cooldown**: the same rule is not revised twice within 7 days, to prevent oscillation.

### Weight update (produces a candidate value only; never written directly)

```
error_r   = clip( normalize(observed - predicted), -1, 1 )
support   = min(1, n_same_direction / N_min)             # N_min = 5
recency   = decay ^ (Δt_days / τ)                        # decay=0.9, τ=30 days
Δw        = η · error_r · conf_r · support · recency     # η = 0.05
w_cand    = clip( w_old + Δw, w_min, w_max )             # [0.0, 1.0]
           and enforce |w_cand - w_old| ≤ δ              # δ = 0.1
```

- `conf_r`: the rule's confidence coefficient (high 1.0 / medium 0.6 / low 0.2).
- `decay`: lets old evidence lose weight naturally, so that a platform environment from three years ago does not still dominate today's parameters.
- **This formula produces `w_cand` only**, written into the candidate diff; it becomes the new `w` only after passing the gate in §5.
- Structural changes (adding or removing a dimension, changing the fingerprint schema) are outside this formula and always go to human review.

**Counterexamples must be retained**: any rejected candidate is archived permanently together with the reason. If the same direction is rejected 3 times in a row, that direction enters a frozen list and is not proposed again unless strong new evidence appears.

---

## 5. Decision criteria for the nine-step gate

| # | Step | Pass condition | On rejection |
| --- | --- | --- | --- |
| 1 | Observe | All four signal groups present; `signal_sources` traceable | Record `pending_feedback` |
| 2 | Diagnose | Attributed to one of A–D with the reasoning stated | Record "unattributed" and stop |
| 3 | Propose | Satisfies all 6 conditions in §4 | Archive as a counterexample |
| 4 | Test | On the **frozen regression set** (a fixed 10 reference cases + human-annotated baselines), **none of the four meta-metric groups falls more than 2% below baseline** | Archive with the regression results |
| 5 | Compare | The **holdout set** (3 cases, never used in candidate generation) shows no regression; proxy metrics move with the real goal | Judge it overfitted and archive |
| 6 | Approve | Human signature; the evidence includes regression results, diff, blast radius and rollback point | No effect |
| 7 | Version | Produce `rules-vN+1`, mark the previous version `last-known-good`, and make it undeletable | — |
| 8 | Deploy | Shadow run on ≥3 cases → canary (≤20% of cases) → full rollout | Roll back immediately if any stage goes abnormal |
| 9 | Monitor | Continuously monitor drift, candidate rejection rate, rollback count and kill-switch availability | Any anomaly triggers the kill switch |

**Pass threshold**: at least one primary metric improves by ≥3%, and no metric drops by ≥2%. Better to change too little than too much.

---

## 6. Drift prevention mechanisms (none is optional)

| Mechanism | How it is done |
| --- | --- |
| **Immutable baseline** | The frozen regression set and the holdout set are stored separately, and the self-improvement engine has **no write access**; they are maintained by hand |
| **Separation of permissions** | The four roles of proposing, evaluating, approving and deploying are separated; the engine may not approve its own proposals |
| **Multi-signal validation** | Platform data + user confirmation + L4 deviation + review pass rate; holdout set + adversarial samples |
| **Counterexample retention** | Rejected candidates, failed cases and negative feedback are retained permanently, to prevent systematic overestimation |
| **Drift bounds and cooldown** | δ=0.1, ≤2 changes per round, 7-day cooldown; anything beyond is rejected |
| **Shadow and canary** | Shadow first (recorded, no effect), then canary, then full rollout |
| **Rollback capability** | Every version keeps a `last-known-good`; rollback is a command, not a prayer |
| **Kill switch** | Setting `evolution_enabled: false` in `case-library/_config.yaml` disables everything globally and returns immediately to `last-known-good` |
| **Audit log** | Append-only: who, when, what was proposed, on what basis, gate results, signature, rollback point |

**Warning signals and how to handle them**:

| Signal | Suspected problem | Handling |
| --- | --- | --- |
| Proxy metrics keep rising while real feedback stays flat | Overfitting / evaluation-set contamination | Stop the round; inspect evaluation-set permissions and the holdout set |
| Internal scores suspiciously smooth with no external improvement | The evaluator is contaminated | Re-check with an independently maintained evaluation suite |
| The same change repeatedly accepted then rolled back | Oscillation | Lower η, extend the cooldown, raise the support-sample threshold |
| Candidate rejection rate stuck at 0 | The gate is decorative | Audit the gate decisions by hand |
| A proposal that touches a hard guardrail | Goal drift | Fail the candidate outright and write it to the audit log |

---

## 7. Pseudocode

```text
function evolve(case):
    rec = load_record(case)
    if not rec.signal_sources.complete:        return PENDING_FEEDBACK
    cause = attribute(rec)
    if cause in {E_EXECUTION, F_EXTERNAL, UNATTRIBUTED}:  return ARCHIVE_NO_CHANGE

    cand = propose_min_diff(cause, rec)
    if not passes_hard_rails(cand) or drift(cand) > DELTA:
        archive_counterexample(cand, "rail_or_drift"); return REJECTED
    if support(cand) < N_MIN or in_cooldown(cand):
        archive_counterexample(cand, "support_or_cooldown"); return REJECTED

    if regression(cand, FROZEN_SET) degrades_any(threshold=0.02):
        archive_counterexample(cand, "regression"); return REJECTED
    if hidden_eval(cand) degrades or proxy_diverges_from_true:
        archive_counterexample(cand, "hidden_or_proxy"); return REJECTED

    if not human_signoff(cand, evidence_pack):
        return AWAITING_APPROVAL

    version = commit_rules(cand, keep_last_known_good=True)
    if not shadow_run(version, cases=3):        rollback(version); return REJECTED
    if not canary(version, share=0.2):          rollback(version); return REJECTED
    promote(version)
    monitor(version)
    return PROMOTED
```

Note that `human_signoff` is a **synchronous blocking point that cannot be bypassed**; a failed shadow run or canary rolls back directly — there is no "let's watch it a bit longer".

---

## 8. Self-modification that is allowed and forbidden

| Object | Allowed | Condition |
| --- | --- | --- |
| `derived_rules[].weight` | ✅ | Full gate + drift bounds |
| `derived_rules[].status` (active/candidate/retired) | ✅ | Full gate + human signature |
| Mapping-rule thresholds (e.g. deviation tolerance) | ✅ | Full gate + regression set |
| Objective probe thresholds (scene / silence) | ✅ | Must include a comparison of old and new thresholds on the regression set |
| Evaluation-dimension weights (L1) | ⚠️ Limited | Human review + the structural-change process |
| Mandatory keys of the fingerprint schema | ❌ | Only a wholesale upgrade to `sfp-v2` with manual migration |
| The mandatory explanation / the S6 confirmation gate / the seven hard guardrails | ❌ | Never |
| Compliance conclusions in the 05 volume, blocking items in the 06 volume review | ❌ | Never |
| The frozen regression set, the holdout set, historical versions, counterexamples, the audit log | ❌ | Append-only |

---

## 9. Common errors and troubleshooting

| Error | Consequence | Correction |
| --- | --- | --- |
| Changing a rule after one hit | Mistaking noise for pattern | N_min=5 same-direction samples |
| Changing a rule because results were poor | Writing execution or external factors into the rules | Attribute first; leave E and F alone |
| Using internal scores to prove it "got better" | Proxy over-optimisation | Holdout set + real feedback across multiple signals |
| Letting the engine write to the evaluation set | Contaminated evaluator | Separation of permissions, frozen sets |
| Deleting failed cases | Systematic overestimation | Counterexamples retained permanently |
| Shipping several changes at once | Cannot attribute, cannot roll back | One change per round, minimal diff |
| Continuing to watch after a shadow/canary anomaly | Blast radius grows | Roll back immediately |
| Not auditing the gate for a long time | The gate stops working | Audit the rejection rate and signatures periodically |

---

## 10. Quick reference

- [ ] All four signal groups present; `signal_sources` traceable
- [ ] Attribution complete; E / F / unattributed cases stopped
- [ ] Candidate meets minimality, N_min=5, drift bounds and cooldown
- [ ] None of the seven hard guardrails touched
- [ ] Frozen regression set and holdout set both passed
- [ ] Human signature obtained; evidence pack complete
- [ ] New version produced; `last-known-good` retained
- [ ] Shadow → canary → full rollout, with instant rollback available
- [ ] Audit log and counterexamples appended
- [ ] Kill switch available and verified

---

## References

- Lyzr, "What Is an AI Agent Self-Improvement Loop?" (observe→diagnose→propose→test→compare→approve→version→deploy→monitor; episodic / semantic / procedural memory tiers): https://www.lyzr.ai/blog/ai-agent-self-improvement-loop/
- Datarekha, "Recursive self-improvement" (immutable baseline, proxy over-optimisation, evaluator contamination, oscillation, separation of permissions): https://datarekha.com/gen-ai/recursive-self-improvement
- Future AGI, "Self-Improving AI Agents: A Pre-Deployment Checklist 2026" (regression baseline, drift bounds, shadow/canary, kill switch, fail-fast blocking): https://futureagi.com/blog/self-improving-ai-agents-pre-deployment-checklist-2026/
- arXiv, "Your Agent May Misevolve: Emergent Risks in Self-evolving LLM Agents" (immutable audit logs, rollback, continuous behaviour monitoring, human gates on high-impact actions): https://arxiv.org/html/2509.26354v2
- AI Governance Institute (the change-management gap for self-modifying agents, and the case for continuous evaluation): https://aigovernance.com/news/self-evolving-ai-agents-break-the-assumption-underlying-every-change-control
- This volume, `01-overview-and-design-principles.md`, `03-style-fingerprint-spec.md` and `04-fingerprint-to-edit-plan-mapping.md`

Retrieved: 2026-11-10. The values of η, δ, N_min, decay, the tolerances and the sample sizes here are all **initial suggested parameters** with no codified industry standard; they must be calibrated to actual task volume and risk level and marked TO VERIFY. Most of the governance sources are 2026 industry articles and preprints and serve as methodological reference.
