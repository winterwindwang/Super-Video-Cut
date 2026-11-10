# Cache store · Directory and data conventions

> Category: Material memory | Topic: Cache directory structure, index and accounting fields, append-only and privacy conventions | Compiled: 2026-11-10 | Applies to: Before the first run of `material_cache.py`; when troubleshooting unexpected hits or auditing reuse history

> ⚠️ This volume is a reference for engineering workflows and **does not constitute legal advice**. The cache may contain faces, locations, and licensing information, and must be managed under `../../05-copyright/04` and your internal data policy.

---

## Directory structure

This directory stores **descriptions and indexes only**, never the original video. The tool creates the files below automatically on the first run of `register` / `use`.

```
09-material-memory/cache/
├── README.md                 ← this file
├── _config.json              ← global switches (kill switch, etc.)
├── index.csv                 ← master material index, one row per item
├── usage.csv                 ← ledger of every lookup / use (token accounting)
├── audit.log                 ← append-only audit log
├── cards/
│   ├── <MID>.yaml            ← authoritative description card (mdc-v1)
│   └── <MID>.v<N>.yaml       ← historical versions after corrections (kept; the current card is never overwritten)
├── themes/
│   └── <MID>.csv             ← which topics adopted this item (L2 adaptation layer)
└── thumbnails/               ← optional frame contact sheets (manage as sensitive if they contain faces or plates)
```

---

## Field definitions

### `index.csv`

| Column | Description |
| --- | --- |
| `mid` | `MID-<first 12 hex chars of sha256>`, the primary key |
| `quick_sha` / `full_sha` | Sampled hash / whole-file hash (populated when `--full` is used) |
| `hash_mode` | `sampled` / `full`; determines how strict `verify` is |
| `size_bytes` / `duration_s` | Used for identity decisions and token estimates |
| `card` | Relative path to `cards/<MID>.yaml` |
| `card_version` | Starts at 1 and increments with each correction |
| `status` | `active / superseded / blocked / unverified` |
| `rights_status` | `cleared / pending / restricted / blocked / unknown` |
| `aliases` | Semicolon-separated file names and codes; **for retrieval only** |
| `source_path` | The absolute path recorded at registration; `lookup` uses it to detect the `STALE` case where "the path is the same but the bytes have changed" |
| `created` / `updated` | ISO dates |

### `usage.csv`

| Column | Description |
| --- | --- |
| `ts` | ISO 8601 local time |
| `event` | `MISS / HIT / HIT_BLOCKED / STALE / UNVERIFIED / USE / VERIFY / BLOCK` |
| `mid` / `theme` | Material ID / topic ID (use `-` when there is no topic) |
| `hash_mode` / `duration_s` | Used for estimation |
| `est_tokens` | `ceil(duration_s × rate)`, with `rate` defaulting to 100 tok/s |
| `actual_tokens` | The measured `usage_metadata` value; leave blank if unavailable |
| `model` | Model name and version (filled on MISS only) |
| `note` | Free-text note, e.g. "read the card directly; no model request" |

### `themes/<MID>.csv`

`ts, theme_id, theme_title, clip_ranges, narrative_role, rights_scope_check, note, outcome`
— field meanings are in `../templates/topic-adaptation-record.md`. De-duplicated on `(theme_id, clip_ranges)`; a repeated `use` only updates the timestamp.

### `_config.json`

```json
{
  "cache_enabled": true,
  "default_token_rate": 100,
  "high_res_token_rate": 300,
  "default_hash_mode": "sampled",
  "require_full_hash_for_delivery": true,
  "block_unknown_rights": true
}
```

`cache_enabled: false` is the kill switch: `lookup` then always returns `MISS`, which is used when investigating cache poisoning or description contamination; **it deletes no data**. `default_token_rate` and `high_res_token_rate` are estimation bases that differ between vendors — re-check the official documentation before changing them.

---

## Governance conventions

| Convention | Content |
| --- | --- |
| **Append-only** | `usage.csv`, `audit.log`, and historical card versions are append-only; no rows are deleted and signed records are never overwritten |
| **Corrections do not overwrite** | The original card is copied to `<MID>.v<N>.yaml` before the new one is written; `corrections` records field / old value / new value / basis / signature |
| **Licence expiry** | `status: blocked` + an audit entry; **do not delete the card**. Every adaptation record that references it is kept but marked invalid |
| **Concurrency** | The tool uses an exclusive lock plus atomic writes (temp file, `os.replace`); a failure never leaves half a card behind |
| **Degrade on corruption** | If a card or the index fails to parse, treat it as `MISS` and log it; never interrupt the editing pipeline |
| **Privacy** | The original video is never cached; `subjects` records no real names or identities; `geo_hint` stores no exact GPS; thumbnails containing faces or plates are treated as sensitive material |
| **Backup** | `usage.csv`, `index.csv`, and `cards/` fall under 3-2-1 backup (basis in `../../01-editing-craft/03`); rebuilding a description costs more than storing it |
| **Volatile information** | Token rates, model versions, and vendor cache TTLs are volatile; re-check the latest official documentation before citing them |

---

## First use

```bash
PY="scripts/material_cache.py"

# 1. Check the cache (on a HIT, read cards/<MID>.yaml and do not ask the model again)
python "$PY" lookup "D:/footage/example.mp4"

# 2. On a miss: local probing → one full model request → fill ../templates/material-description-card.yaml
python "$PY" validate /tmp/MID-xxxxxxxxxxxx.yaml
python "$PY" register "D:/footage/example.mp4" --card /tmp/MID-xxxxxxxxxxxx.yaml --tokens 18000

# 3. After that, record one line per topic
python "$PY" use "D:/footage/example.mp4" --theme "T-2026-example-topic" --clip "00:00:03-00:00:08" --note "opening B-roll"

# 4. Health check and statistics
python "$PY" verify "D:/footage/example.mp4"
python "$PY" stats
```

The tool has zero third-party dependencies (Python standard library only) and runs directly on the local machine. `fingerprint` calls the local `ffprobe` (tested on 8.1.2) to read specs; if the call fails it degrades to "hash + file size only" and notes that in the log.

---

## Troubleshooting quick reference

| Symptom | Check first |
| --- | --- |
| `MISS` even though the material was analysed | Whether the file bytes changed (re-export or transcode); `cache_enabled` in `_config.json`; whether the cache directory was moved |
| `HIT` but the description does not match | Have `verify` recompute the hash; if `hash_mode: sampled`, recheck with `--full` (changes in unsampled regions can be missed) |
| `HIT_BLOCKED` | `rights_status` or `rights_expiry`; once the licence documentation is in place, edit the card by hand and leave `corrections` |
| Abnormally high hit rate | Different items may be collapsing onto the same hash, or hits are being forced to inflate the metric; spot-check three cards against the original footage |
| `stats` diverges widely from the invoice | The estimate covers video input tokens only; fill `actual_tokens` with measured `usage_metadata` |
| A card field is missing | `python "$PY" validate <card>` and fill in what the V1–V8 messages ask for |

---

## References

- This volume's `../01-material-description-card-spec.md` (V1–V8), `../02-cache-reuse-protocol-and-token-savings.md` (state machine, accounting, concurrency, privacy), `../03-multi-topic-adaptation-and-references.md`
- Content-Hash File Cache Pattern (content hashing, path-independence, corrupted entries degraded to misses): https://lobehub.com/ru/skills/sehoon787-my-claude-content-hash-cache-pattern
- Google, "Video understanding" and "Context caching" (token rates and caching basis): https://ai.google.dev/gemini-api/docs/video-understanding , https://ai.google.dev/gemini-api/docs/caching
- `../../01-editing-craft/03-editing-workflow-and-project-standards.md` (3-2-1 backup), `../../08-rsi/06-case-library-and-version-governance.md` (append-only practice and rollback)

Retrieved: 2026-11-10. The directory structure, CSV fields, and `_config.json` switches are conventions defined by this knowledge base, not industry standards.
