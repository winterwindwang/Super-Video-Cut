#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
material_cache.py - material description cache (zero third-party dependencies, Python 3.8+)

Goal: let the video model "look" at a piece of footage only once; the description is
written to disk and then reused across themes and across sessions.
Commands: fingerprint / lookup / register / use / verify / themes / stats / validate
See references/09-material-memory/README.md and 02-cache-reuse-protocol-and-token-savings.md
"""

import argparse
import csv
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

def default_root():
    """Cache root: $MDC_HOME when set, otherwise "material-cache" under the current working directory.

    Deliberately not derived from the script's own location: material descriptions are
    project data and must not be written into the skill installation directory.
    """
    env = os.environ.get("MDC_HOME")
    if env:
        return Path(env).expanduser().resolve()
    return Path.cwd() / "material-cache"


CHUNK = 64 * 1024
SAMPLE = 2 * 1024 * 1024

DEFAULT_CONFIG = {
    "cache_enabled": True,
    "default_token_rate": 100,
    "high_res_token_rate": 300,
    "default_hash_mode": "sampled",
    "require_full_hash_for_delivery": True,
    "block_unknown_rights": True,
}

INDEX_FIELDS = ["mid", "quick_sha", "full_sha", "hash_mode", "size_bytes",
                "duration_s", "card", "card_version", "status", "rights_status",
                "aliases", "source_path", "created", "updated"]
USAGE_FIELDS = ["ts", "event", "mid", "theme", "hash_mode", "duration_s",
                "est_tokens", "actual_tokens", "model", "note"]
THEME_FIELDS = ["ts", "theme_id", "theme_title", "clip_ranges",
                "narrative_role", "rights_scope_check", "note", "outcome"]


# ---------- Basic helpers ----------

def now():
    return datetime.now().replace(microsecond=0).isoformat()


def read_config(root):
    p = root / "_config.json"
    if not p.is_file():
        return dict(DEFAULT_CONFIG)
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
        merged = dict(DEFAULT_CONFIG)
        merged.update(d)
        return merged
    except (OSError, ValueError):
        return dict(DEFAULT_CONFIG)


def ensure_root(root):
    root.mkdir(parents=True, exist_ok=True)
    (root / "cards").mkdir(exist_ok=True)
    (root / "themes").mkdir(exist_ok=True)
    (root / "thumbnails").mkdir(exist_ok=True)
    cfg = root / "_config.json"
    if not cfg.is_file():
        atomic_write(cfg, json.dumps(DEFAULT_CONFIG, ensure_ascii=False, indent=2) + "\n")


def atomic_write(path, text):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".tmp_")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
            f.write(text)
        os.replace(tmp, path)
    except Exception:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def read_csv(path, fields):
    path = Path(path)
    if not path.is_file():
        return []
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as f:
            return [dict(r) for r in csv.DictReader(f, fieldnames=fields)]
    except (OSError, UnicodeError, csv.Error):
        return []


def write_csv(path, fields, rows):
    import io
    buf = io.StringIO(newline="")
    w = csv.DictWriter(buf, fieldnames=fields, extrasaction="ignore", lineterminator="\n")
    w.writeheader()
    for r in rows:
        w.writerow({k: r.get(k, "") for k in fields})
    atomic_write(path, buf.getvalue())


def append_csv(path, fields, row):
    rows = read_csv(path, fields)
    if rows and rows[0].get(fields[0]) == fields[0]:  # tolerate a legacy file that carries its own header row
        rows = rows[1:]
    rows.append(row)
    write_csv(path, fields, rows)


def append_log(root, line):
    p = root / "audit.log"
    old = p.read_text(encoding="utf-8") if p.is_file() else ""
    atomic_write(p, old + "%s | %s\n" % (now(), line))


class Lock:
    """Minimal exclusive lock so two jobs cannot write the same cache directory at once."""

    def __init__(self, root, timeout=5.0):
        self.path = Path(root) / ".lock"
        self.timeout = timeout

    def __enter__(self):
        deadline = time.time() + self.timeout
        while True:
            try:
                fd = os.open(str(self.path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                os.write(fd, str(os.getpid()).encode("ascii"))
                os.close(fd)
                return self
            except FileExistsError:
                if time.time() > deadline:
                    raise TimeoutError("cache lock timed out: %s" % self.path)
                time.sleep(0.02)

    def __exit__(self, *exc):
        try:
            self.path.unlink()
        except OSError:
            pass


def section(text, name):
    """Take one top-level YAML section (up to the next top-level key), dependency-free text split."""
    lines = text.splitlines()
    out, inside = [], False
    for line in lines:
        if re.match(r"^[A-Za-z_][A-Za-z_0-9]*:", line):
            if inside:
                break
            inside = line.split(":", 1)[0].strip() == name
        if inside:
            out.append(line)
    return "\n".join(out)


def field_value(text, key):
    m = re.search(r"^\s*%s\s*:\s*(.*?)\s*$" % re.escape(key), text, re.M)
    return m.group(1).strip().strip('"').strip("'") if m else ""


# ---------- Fingerprints and specs ----------

def sha_full(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(CHUNK)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def sha_sampled(path, size):
    h = hashlib.sha256()
    h.update(str(size).encode("ascii"))
    with open(path, "rb") as f:
        h.update(f.read(SAMPLE))
        if size > 3 * SAMPLE:
            f.seek(size // 2 - SAMPLE // 2)
            h.update(f.read(SAMPLE))
        if size > SAMPLE:
            f.seek(max(0, size - SAMPLE))
            h.update(f.read(SAMPLE))
    return h.hexdigest()


def probe(path):
    cmd = ["ffprobe", "-v", "error", "-show_entries",
           "format=duration:stream=codec_type,codec_name,width,height,"
           "r_frame_rate,pix_fmt,sample_rate,channels", "-of", "json", str(path)]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True,
                             encoding="utf-8", errors="replace", timeout=30)
        if out.returncode != 0:
            return {}
        d = json.loads(out.stdout)
    except (OSError, ValueError, subprocess.SubprocessError):
        return {}
    v = next((s for s in d.get("streams", []) if s.get("codec_type") == "video"), {})
    a = next((s for s in d.get("streams", []) if s.get("codec_type") == "audio"), {})
    try:
        duration = float(d.get("format", {}).get("duration", 0) or 0)
    except (TypeError, ValueError):
        duration = 0.0
    return {"duration_s": round(duration, 3), "vcodec": v.get("codec_name", ""),
            "resolution": "%sx%s" % (v.get("width", ""), v.get("height", ""))
            if v.get("width") else "", "fps": v.get("r_frame_rate", ""),
            "pix_fmt": v.get("pix_fmt", ""), "acodec": a.get("codec_name", ""),
            "sample_rate": a.get("sample_rate", ""), "channels": a.get("channels", "")}


def fingerprint(video, full=False, do_probe=True):
    p = Path(video)
    if not p.is_file():
        raise FileNotFoundError("material not found: %s" % p)
    size = p.stat().st_size
    quick = sha_sampled(str(p), size)
    fullsha = sha_full(str(p)) if full else ""
    # MID is always derived from the sampled hash: the same file keeps the same identity
    # whether it is checked in sampled or full mode.
    # full_sha is only an extra check value and never takes part in identity computation.
    d = {"mid": "MID-" + quick[:12], "quick_sha": quick, "full_sha": fullsha,
         "hash_mode": "full" if full else "sampled", "size_bytes": size,
         "source_path": str(p.resolve()), "filename": p.name}
    d.update(probe(str(p)) if do_probe else {"duration_s": 0.0})
    return d


def est_tokens(duration_s, rate):
    try:
        return int(-(-float(duration_s) // 1) * int(rate))  # ceil(duration) * rate
    except (TypeError, ValueError):
        return 0


# ---------- Validation ----------

def validate_card(card_path, video=None, fp=None):
    text = Path(card_path).read_text(encoding="utf-8")
    results = []

    def add(code, ok, msg, warn=False):
        results.append((code, "WARN" if (warn and not ok) else ("PASS" if ok else "FAIL"), msg))

    add("V1", field_value(text, "mdc_version") == "mdc-v1" and
        bool(re.match(r"^MID-[0-9a-f]{12}$", field_value(text, "material_id"))),
        "mdc_version and material_id format")
    names = ["content", "where", "style", "usability", "meta"]
    missing = [n for n in names if not section(text, n).strip()]
    add("V2", not missing, "all four required sections present"
        + (" (missing %s)" % ",".join(missing) if missing else ""))

    hash_in_card = field_value(text, "content_hash").replace("sha256:", "")
    if fp is not None or video:
        f = fp or fingerprint(video)
        match = bool(hash_in_card) and (hash_in_card == f["quick_sha"] or
                                       hash_in_card == f["full_sha"])
        add("V3", match, "content_hash matches the actual file (measured %s...)" % f["quick_sha"][:12])
    else:
        add("V3", bool(hash_in_card),
            "content_hash is non-empty (no --video given, on-disk comparison skipped)", warn=True)

    c = section(text, "content")
    summary = field_value(c, "summary")
    anchors = len(re.findall(r"\btc\s*:", c))
    add("V4", bool(summary) and len(summary) <= 80 and anchors >= 3,
        "summary <=80 chars and timeline has >=3 anchors (currently %d chars / %d anchors)" % (len(summary), anchors))

    w = section(text, "where")
    place = field_value(w, "place_name")
    basis = field_value(w, "place_basis")
    place_ok = place.lower() in ("", "null", "~", "none") or (
        basis and basis.lower() not in ("无", "none", "n/a", '""', "''"))
    add("V5", place_ok, "a place name requires a basis (place_name=%s, place_basis=%s)"
        % (place or "null", basis or "empty"))

    s = section(text, "style")
    notes = section(s, "style_notes") if "style_notes" in s else ""
    # style_notes is a second-level section inside style and section() only splits top-level keys,
    # so it is cut out separately here
    m = re.search(r"^\s*style_notes\s*:.*?$([\s\S]*?)(?=^\s{0,2}[A-Za-z_\u4e00-\u9fa5][\w\u4e00-\u9fa5]*\s*:|^\S|\Z)",
                  s, re.M)
    notes = (m.group(1) if m else "")
    # Five-part entries: canonical English keys, legacy Chinese keys still accepted.
    n_obs = len(re.findall(r"(?:observation|观察)\s*:", notes))
    keys_ok = all(len(re.findall(r"(?:%s|%s)\s*:" % (en, zh), notes)) >= n_obs
                  for en, zh in [("basis", "依据"), ("inference", "推断"),
                                 ("action", "动作项"), ("confidence", "置信度")])
    add("V6", n_obs >= 1 and keys_ok,
        "style_notes has all five parts in every entry (%d observation(s))" % n_obs)

    u = section(text, "usability")
    rights = field_value(u, "rights_status") or "unknown"
    nou = field_value(text, "no_use_until_cleared")
    add("V7", rights == "cleared" or nou == "true",
        "no_use_until_cleared=true while rights are not cleared (rights=%s)" % rights)

    body = "\n".join(section(text, n) for n in names[:4])
    theme_words = re.findall(r"theme|topic|project code|T-20\d\d", body, re.I)
    add("V8", not theme_words, "the four sections stay topic-neutral (%d hit(s), needs human confirmation)"
        % len(theme_words), warn=True)

    return results


def print_validation(results):
    for code, status, msg in results:
        print("  [%s] %s %s" % (status, code, msg))
    fails = [r for r in results if r[1] == "FAIL"]
    print("  Result: %s (%d failed / %d warning(s))" %
          ("PASSED" if not fails else "FAILED", len(fails),
           len([r for r in results if r[1] == "WARN"])))
    return not fails


# ---------- Commands ----------

def cmd_fingerprint(a):
    fp = fingerprint(a.video, full=a.full, do_probe=not a.no_probe)
    if a.json:
        print(json.dumps(fp, ensure_ascii=False, indent=2))
    else:
        for k, v in fp.items():
            print("  %-14s %s" % (k, v))
    return 0


def find_index(root, fp):
    rows = read_csv(root / "index.csv", INDEX_FIELDS)
    rows = [r for r in rows if r.get("mid", "").startswith("MID-")]
    exact = next((r for r in rows if r["mid"] == fp["mid"]), None)
    same_path = [r for r in rows if r.get("source_path") == fp["source_path"]]
    return rows, exact, same_path


def card_digest(root, mid):
    p = root / "cards" / (mid + ".yaml")
    if not p.is_file():
        return ""
    text = p.read_text(encoding="utf-8")
    summary = field_value(section(text, "content"), "summary")
    place = field_value(section(text, "where"), "place_name")
    genre = field_value(section(text, "style"), "genre")
    aff = field_value(section(text, "content"), "affordances")
    return "Summary: %s | Place: %s | Genre: %s | Use tags: %s" % (
        summary or "(empty)", place or "null", genre or "(empty)", aff or "(empty)")


def log_usage(root, event, fp, cfg, theme="-", model="", note="", actual="", est=None):
    rate = int(cfg.get("default_token_rate", 100))
    e = est if est is not None else (est_tokens(fp.get("duration_s", 0), rate)
                                    if event in ("HIT", "MISS", "HIT_BLOCKED", "STALE") else 0)
    append_csv(root / "usage.csv", USAGE_FIELDS,
               {"ts": now(), "event": event, "mid": fp["mid"], "theme": theme,
                "hash_mode": fp["hash_mode"], "duration_s": fp.get("duration_s", 0),
                "est_tokens": e, "actual_tokens": actual, "model": model, "note": note})
    return e


def cmd_lookup(a):
    root = Path(a.root).resolve() if a.root else default_root()
    ensure_root(root)
    cfg = read_config(root)
    fp = fingerprint(a.video, full=a.full, do_probe=not a.no_probe)
    if not cfg.get("cache_enabled", True):
        state = "MISS"
        reason = "kill switch cache_enabled=false, forced miss"
        log_usage(root, state, fp, cfg, note=reason)
    else:
        _, exact, same_path = find_index(root, fp)
        if exact:
            status = exact.get("status", "active")
            rights = exact.get("rights_status", "unknown")
            if status != "active":
                state, reason = "UNVERIFIED", "card status %s, must be completed or re-reviewed" % status
            elif rights not in ("cleared",):
                state, reason = "HIT_BLOCKED", "rights status %s, description readable but blocked from the timeline" % rights
            else:
                state, reason = "HIT", "content hash matches, card valid and rights cleared"
        elif same_path:
            state, reason = "STALE", "bytes at the same path changed (old MID %s)" % same_path[0]["mid"]
            # Old card becomes superseded and the change is recorded; the card itself and all
            # historical versions are always kept
            with Lock(root):
                rows2, _, _ = find_index(root, fp)
                for r in rows2:
                    if r.get("source_path") == fp["source_path"] and r.get("status") != "superseded":
                        r["status"] = "superseded"
                        r["updated"] = now()
                write_csv(root / "index.csv", INDEX_FIELDS, rows2)
                append_log(root, "STALE | %s | old card marked superseded | new MID %s" %
                           (same_path[0]["mid"], fp["mid"]))
        else:
            state, reason = "MISS", "no registry entry"
        log_usage(root, state, fp, cfg, note=reason)

    out = {"state": state, "reason": reason, "mid": fp["mid"],
           "duration_s": fp.get("duration_s", 0), "hash_mode": fp["hash_mode"],
           "card": str(root / "cards" / (fp["mid"] + ".yaml")),
           "est_tokens_saved": est_tokens(fp.get("duration_s", 0),
                                          int(cfg.get("default_token_rate", 100)))
           if state == "HIT" else 0}
    if state in ("HIT", "HIT_BLOCKED", "UNVERIFIED"):
        out["digest"] = card_digest(root, fp["mid"])
    if a.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print("=== Material cache lookup ===")
        print("  File    : %s" % fp["filename"])
        print("  State   : %s" % state)
        print("  Reason  : %s" % reason)
        print("  MID     : %s  (%s, %.3f s)" % (fp["mid"], fp["hash_mode"], fp.get("duration_s", 0)))
        if "digest" in out:
            print("  Card    : %s" % out["card"])
            print("  %s" % out["digest"])
        if state == "HIT":
            print("  ★ Do NOT call the video model again: read the card above and only adapt it "
                  "to the theme. This run saves an estimated %d video input tokens." % out["est_tokens_saved"])
        elif state == "HIT_BLOCKED":
            print("  ★ The description may be read for discussion but must not enter the timeline; clear the rights first.")
        elif state == "STALE":
            print("  ★ The old card becomes superseded; re-probe locally + one full model request + a new card.")
        elif state == "MISS":
            print("  ★ You may make ONE full model request: probe locally with E1 first, then")
            print("    references/09-material-memory/templates/model-analysis-prompt.md asks everything at once; fill the card → validate → register.")
    return 0


def cmd_register(a):
    root = Path(a.root).resolve() if a.root else default_root()
    ensure_root(root)
    cfg = read_config(root)
    fp = fingerprint(a.video, full=a.full, do_probe=not a.no_probe)
    results = validate_card(a.card, fp=fp)
    print("=== Card validation ===")
    if not print_validation(results):
        print("  Validation failed: fix the card and retry.")
        if not a.force:
            print("  Registration aborted (use --force only for a dry run; never in the real flow).")
            return 2
        print("  --force enabled: dry-run / state-machine testing only, never in the real flow.")
    with Lock(root):
        target = root / "cards" / (fp["mid"] + ".yaml")
        if target.is_file():
            atomic_write(root / "cards" / (fp["mid"] + ".v%d.yaml" % int(time.time())),
                         target.read_text(encoding="utf-8"))
        atomic_write(target, Path(a.card).read_text(encoding="utf-8"))
        rows, _, _ = find_index(root, fp)
        rows = [r for r in rows if r["mid"] != fp["mid"]]
        card_text = target.read_text(encoding="utf-8")
        rights = field_value(section(card_text, "usability"), "rights_status") or "unknown"
        status = field_value(section(card_text, "meta"), "status") or "active"
        rows.append({"mid": fp["mid"], "quick_sha": fp["quick_sha"],
                     "full_sha": fp["full_sha"], "hash_mode": fp["hash_mode"],
                     "size_bytes": fp["size_bytes"], "duration_s": fp.get("duration_s", 0),
                     "card": "cards/%s.yaml" % fp["mid"],
                     "card_version": field_value(section(card_text, "meta"), "card_version") or "1",
                     "status": status, "rights_status": rights,
                     "aliases": fp["filename"], "source_path": fp["source_path"],
                     "created": now(), "updated": now()})
        write_csv(root / "index.csv", INDEX_FIELDS, rows)
        # If the caller skipped lookup, record one MISS so the hit-rate denominator equals
        # the number of new analyses
        have_miss = any(r.get("event") == "MISS" and r.get("mid") == fp["mid"]
                        for r in read_csv(root / "usage.csv", USAGE_FIELDS))
        if not have_miss:
            log_usage(root, "MISS", fp, cfg, note="cache not looked up before registration, MISS recorded")
        log_usage(root, "REGISTER", fp, cfg, model=a.model or "",
                  actual=a.tokens or "", note="first full analysis, registered", est=0)
        append_log(root, "REGISTER | %s | %s | card=%s | model=%s" %
                   (fp["mid"], fp["filename"], target.name, a.model or "-"))
    print("  Registered: %s → %s" % (fp["mid"], target))
    return 0


def cmd_use(a):
    root = Path(a.root).resolve() if a.root else default_root()
    ensure_root(root)
    cfg = read_config(root)
    fp = fingerprint(a.video, full=a.full, do_probe=not a.no_probe)
    _, exact, _ = find_index(root, fp)
    if not exact:
        print("  ERROR: material is not registered yet, run register first. The current lookup is MISS.")
        return 2
    if exact.get("rights_status") != "cleared" and cfg.get("block_unknown_rights", True):
        print("  ERROR: rights status %s, must not be used. Clear the rights and edit the card manually first." %
              exact.get("rights_status"))
        return 2
    with Lock(root):
        p = root / "themes" / (fp["mid"] + ".csv")
        rows = [r for r in read_csv(p, THEME_FIELDS) if r.get("theme_id", "").startswith("T-")]
        key = (a.theme, a.clip or "")
        dup = next((r for r in rows if (r.get("theme_id"), r.get("clip_ranges")) == key), None)
        if dup:
            dup["ts"] = now()
            dup["note"] = a.note or dup.get("note", "")
            action = "updated existing fit record"
        else:
            rows.append({"ts": now(), "theme_id": a.theme, "theme_title": a.theme,
                         "clip_ranges": a.clip or "", "narrative_role": a.role or "",
                         "rights_scope_check": "in_scope", "note": a.note or "",
                         "outcome": ""})
            action = "added new fit record"
        write_csv(p, THEME_FIELDS, rows)
        log_usage(root, "USE", fp, cfg, theme=a.theme, note="%s; card read directly, no model request" % action)
        append_log(root, "USE | %s | %s | clip=%s | %s" %
                   (fp["mid"], a.theme, a.clip or "-", a.note or "-"))
    print("  %s: %s x %s (%s)" % (action, fp["mid"], a.theme, a.clip or "full clip"))
    print("  ★ This reuse made 0 video model requests; read cards/%s.yaml directly" % fp["mid"])
    return 0


def cmd_verify(a):
    root = Path(a.root).resolve() if a.root else default_root()
    ensure_root(root)
    cfg = read_config(root)
    fp = fingerprint(a.video, full=a.full, do_probe=not a.no_probe)
    _, exact, same_path = find_index(root, fp)
    if exact:
        card = root / "cards" / (fp["mid"] + ".yaml")
        ok = card.is_file() and field_value(card.read_text(encoding="utf-8"),
                                            "content_hash").replace("sha256:", "") in (
            fp["quick_sha"], fp["full_sha"] or "_")
        verdict = "OK" if ok else "MISMATCH"
        print("  [%s] %s: hash %s, card %s" %
              (verdict, fp["mid"], "matches" if ok else "differs", "present" if card.is_file() else "missing"))
        print("       hash_mode=%s (%s)" %
              (fp["hash_mode"], "whole file, no sampling blind spot" if a.full
               else "sampled mode, changes in unsampled regions may be missed; --full recommended for delivery"))
    elif same_path:
        print("  [STALE] bytes at the same path changed: old MID %s, re-analysis required." % same_path[0]["mid"])
    else:
        print("  [MISS] no registry entry.")
    log_usage(root, "VERIFY", fp, cfg, note="verify")
    append_log(root, "VERIFY | %s | %s" % (fp["mid"], a.video))
    return 0


def cmd_themes(a):
    root = Path(a.root).resolve() if a.root else default_root()
    fp = fingerprint(a.video, do_probe=False)
    rows = [r for r in read_csv(root / "themes" / (fp["mid"] + ".csv"), THEME_FIELDS)
            if r.get("theme_id", "").startswith("T-")]
    print("=== Fit records for %s (%d) ===" % (fp["mid"], len(rows)))
    for r in rows:
        print("  %s | %s | %s | %s | %s" %
              (r["ts"], r["theme_id"], r.get("clip_ranges", ""),
               r.get("narrative_role", ""), r.get("outcome", "") or "pending"))
    return 0


def cmd_stats(a):
    root = Path(a.root).resolve() if a.root else default_root()
    cfg = read_config(root)
    usage = [r for r in read_csv(root / "usage.csv", USAGE_FIELDS)
             if r.get("event") in ("HIT", "MISS", "HIT_BLOCKED", "STALE",
                                   "UNVERIFIED", "USE", "REGISTER", "VERIFY")]
    idx = [r for r in read_csv(root / "index.csv", INDEX_FIELDS)
           if r.get("mid", "").startswith("MID-")]
    hits = [r for r in usage if r["event"] == "HIT"]
    miss = [r for r in usage if r["event"] == "MISS"]
    uses = [r for r in usage if r["event"] == "USE"]
    themes = sorted(set(r["theme"] for r in usage if r.get("theme") not in ("", "-")))
    saved = sum(int(r.get("est_tokens") or 0) for r in hits)
    actual = sum(int(r.get("actual_tokens") or 0) for r in usage)
    denom = len(hits) + len(miss)
    rate = (len(hits) / denom * 100) if denom else 0.0
    out = {"materials": len(idx), "themes": len(themes), "hits": len(hits),
           "misses": len(miss), "uses": len(uses), "hit_rate_pct": round(rate, 1),
           "est_saved_input_tokens": saved, "actual_tokens_logged": actual,
           "blocked_materials": len([r for r in idx if r.get("rights_status") != "cleared"]),
           "estimate_only": True,
           "token_rate": int(cfg.get("default_token_rate", 100))}
    if a.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print("=== Cache stats (all figures are estimates, not a bill) ===")
        for k, label in [("materials", "registered materials"), ("themes", "themes touched"),
                         ("hits", "HIT count"), ("misses", "MISS count"),
                         ("uses", "theme reuses"), ("hit_rate_pct", "hit rate (%)"),
                         ("est_saved_input_tokens", "est. input tokens saved"),
                         ("actual_tokens_logged", "measured tokens logged"),
                         ("blocked_materials", "rights uncleared materials")]:
            print("  %-26s %s" % (label, out[k]))
        print("  Estimated rate: %d token/s; real usage comes from usage_metadata." % out["token_rate"])
        print("  Saving ratio (for N reuses): 1 - 1/N, video input tokens only.")
    return 0


def cmd_validate(a):
    fp = fingerprint(a.video) if a.video else None
    return 0 if print_validation(validate_card(a.card, fp=fp)) else 2


def main():
    ap = argparse.ArgumentParser(description="Material description cache tool (zero dependencies)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    def common(p, video=True):
        if video:
            p.add_argument("video", help="path to the material file")
        p.add_argument("--root", help="cache root (default $MDC_HOME, otherwise ./material-cache)")
        p.add_argument("--full", action="store_true", help="use a full-file SHA-256 (6 MiB sampling by default)")
        p.add_argument("--no-probe", action="store_true", help="skip ffprobe (testing only)")

    p = sub.add_parser("fingerprint", help="content hash and ffprobe specs")
    common(p)
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_fingerprint)

    p = sub.add_parser("lookup", help="★ first step before analysing any material")
    common(p)
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_lookup)

    p = sub.add_parser("register", help="register a description card (auto-validated)")
    common(p)
    p.add_argument("--card", required=True, help="mdc-v1 YAML card")
    p.add_argument("--model", default="", help="model name and version")
    p.add_argument("--tokens", default="", help="measured token count (usage_metadata)")
    p.add_argument("--force", action="store_true", help="register even if validation fails (dry run only)")
    p.set_defaults(func=cmd_register)

    p = sub.add_parser("use", help="record one theme reuse (no model request)")
    common(p)
    p.add_argument("--theme", required=True, help="T-YYYY-<short name>")
    p.add_argument("--clip", default="", help="MM:SS-MM:SS")
    p.add_argument("--role", default="", help="narrative role")
    p.add_argument("--note", default="", help="note")
    p.set_defaults(func=cmd_use)

    p = sub.add_parser("verify", help="recompute the hash and compare it with the card")
    common(p)
    p.set_defaults(func=cmd_verify)

    p = sub.add_parser("themes", help="list the themes this material has been used in")
    common(p)
    p.set_defaults(func=cmd_themes)

    p = sub.add_parser("stats", help="hit rate and estimated savings")
    p.add_argument("--root")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_stats)

    p = sub.add_parser("validate", help="validate an mdc-v1 card (V1–V8)")
    p.add_argument("card")
    p.add_argument("--video", help="also compare content_hash with the actual file")
    p.set_defaults(func=cmd_validate)

    a = ap.parse_args()
    try:
        return a.func(a)
    except (FileNotFoundError, TimeoutError, OSError) as e:
        print("  ERROR: %s" % e, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
