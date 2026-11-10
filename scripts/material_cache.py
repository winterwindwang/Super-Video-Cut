#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
material_cache.py - 素材描述缓存工具（零第三方依赖，Python 3.8+）

目的：一段视频素材只让视频模型「看」一次；描述落盘后跨主题、跨会话复用。
命令：fingerprint / lookup / register / use / verify / themes / stats / validate
详见 references/09-素材记忆/README.md 与 02-缓存复用协议与Token节省.md
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
    """缓存根目录：优先环境变量 $MDC_HOME，否则用当前工作目录下的「素材缓存」。

    刻意不使用脚本自身位置推算：素材描述属于项目数据，不应写进 skill 安装目录。
    """
    env = os.environ.get("MDC_HOME")
    if env:
        return Path(env).expanduser().resolve()
    return Path.cwd() / "素材缓存"


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


# ---------- 基础工具 ----------

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
    if rows and rows[0].get(fields[0]) == fields[0]:  # 兼容旧文件自带表头
        rows = rows[1:]
    rows.append(row)
    write_csv(path, fields, rows)


def append_log(root, line):
    p = root / "audit.log"
    old = p.read_text(encoding="utf-8") if p.is_file() else ""
    atomic_write(p, old + "%s | %s\n" % (now(), line))


class Lock:
    """极简独占锁，防止两个任务同时写同一缓存目录。"""

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
                    raise TimeoutError("缓存锁超时：%s" % self.path)
                time.sleep(0.02)

    def __exit__(self, *exc):
        try:
            self.path.unlink()
        except OSError:
            pass


def section(text, name):
    """取一个顶层 YAML 节（到下一个顶层键为止），零依赖文本切分。"""
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


# ---------- 指纹与规格 ----------

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
        raise FileNotFoundError("素材不存在：%s" % p)
    size = p.stat().st_size
    quick = sha_sampled(str(p), size)
    fullsha = sha_full(str(p)) if full else ""
    # MID 恒基于采样哈希：同一文件无论用 sampled 还是 full 校验，身份都不变。
    # full_sha 只作为附加校验值，不参与身份计算。
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


# ---------- 校验 ----------

def validate_card(card_path, video=None, fp=None):
    text = Path(card_path).read_text(encoding="utf-8")
    results = []

    def add(code, ok, msg, warn=False):
        results.append((code, "WARN" if (warn and not ok) else ("PASS" if ok else "FAIL"), msg))

    add("V1", field_value(text, "mdc_version") == "mdc-v1" and
        bool(re.match(r"^MID-[0-9a-f]{12}$", field_value(text, "material_id"))),
        "mdc_version 与 material_id 格式")
    names = ["content", "where", "style", "usability", "meta"]
    missing = [n for n in names if not section(text, n).strip()]
    add("V2", not missing, "四组必填节齐全" + ("（缺 %s）" % ",".join(missing) if missing else ""))

    hash_in_card = field_value(text, "content_hash").replace("sha256:", "")
    if fp is not None or video:
        f = fp or fingerprint(video)
        match = bool(hash_in_card) and (hash_in_card == f["quick_sha"] or
                                       hash_in_card == f["full_sha"])
        add("V3", match, "content_hash 与实际文件一致（实测 %s…）" % f["quick_sha"][:12])
    else:
        add("V3", bool(hash_in_card), "content_hash 非空（未传 --video，跳过实测比对）", warn=True)

    c = section(text, "content")
    summary = field_value(c, "summary")
    anchors = len(re.findall(r"\btc\s*:", c))
    add("V4", bool(summary) and len(summary) <= 80 and anchors >= 3,
        "summary ≤80 字且 timeline ≥3 个锚点（当前 %d 字 / %d 锚点）" % (len(summary), anchors))

    w = section(text, "where")
    place = field_value(w, "place_name")
    basis = field_value(w, "place_basis")
    place_ok = place.lower() in ("", "null", "~", "none") or (basis and basis not in ("无", '""', "''"))
    add("V5", place_ok, "有地名则必须有依据（place_name=%s, place_basis=%s）" % (place or "null", basis or "空"))

    s = section(text, "style")
    notes = section(s, "style_notes") if "style_notes" in s else ""
    # style_notes 是 style 内的二级节，section() 只切顶层，这里单独切
    m = re.search(r"^\s*style_notes\s*:.*?$([\s\S]*?)(?=^\s{0,2}[A-Za-z_\u4e00-\u9fa5][\w\u4e00-\u9fa5]*\s*:|^\S|\Z)",
                  s, re.M)
    notes = (m.group(1) if m else "")
    n_obs = len(re.findall(r"观察\s*:", notes))
    keys_ok = all(len(re.findall(r"%s\s*:" % k, notes)) >= n_obs for k in
                  ["依据", "推断", "动作项", "置信度"])
    add("V6", n_obs >= 1 and keys_ok,
        "style_notes 每条五段式齐全（%d 条观察）" % n_obs)

    u = section(text, "usability")
    rights = field_value(u, "rights_status") or "unknown"
    nou = field_value(text, "no_use_until_cleared")
    add("V7", rights == "cleared" or nou == "true",
        "授权未清时 no_use_until_cleared=true（rights=%s）" % rights)

    body = "\n".join(section(text, n) for n in names[:4])
    theme_words = re.findall(r"主题|项目代号|T-20\d\d", body)
    add("V8", not theme_words, "四组字段主题中立（命中 %d 处，需人工确认）" % len(theme_words), warn=True)

    return results


def print_validation(results):
    for code, status, msg in results:
        print("  [%s] %s %s" % (status, code, msg))
    fails = [r for r in results if r[1] == "FAIL"]
    print("  结果：%s（%d 项失败 / %d 项警告）" %
          ("通过" if not fails else "未通过", len(fails),
           len([r for r in results if r[1] == "WARN"])))
    return not fails


# ---------- 命令 ----------

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
    return "摘要：%s | 地点：%s | 体裁：%s | 用途标签：%s" % (
        summary or "（空）", place or "null", genre or "（空）", aff or "（空）")


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
        reason = "kill switch cache_enabled=false，强制未命中"
        log_usage(root, state, fp, cfg, note=reason)
    else:
        _, exact, same_path = find_index(root, fp)
        if exact:
            status = exact.get("status", "active")
            rights = exact.get("rights_status", "unknown")
            if status != "active":
                state, reason = "UNVERIFIED", "卡片状态 %s，需补齐或复核" % status
            elif rights not in ("cleared",):
                state, reason = "HIT_BLOCKED", "授权状态 %s，可读描述但禁止进入时间线" % rights
            else:
                state, reason = "HIT", "内容哈希一致，卡片有效、授权已清"
        elif same_path:
            state, reason = "STALE", "同一路径的素材字节已变化（旧 MID %s）" % same_path[0]["mid"]
            # 旧卡转 superseded 并留痕；卡片本体与历史版本一律保留
            with Lock(root):
                rows2, _, _ = find_index(root, fp)
                for r in rows2:
                    if r.get("source_path") == fp["source_path"] and r.get("status") != "superseded":
                        r["status"] = "superseded"
                        r["updated"] = now()
                write_csv(root / "index.csv", INDEX_FIELDS, rows2)
                append_log(root, "STALE | %s | 旧卡标记 superseded | 新 MID %s" %
                           (same_path[0]["mid"], fp["mid"]))
        else:
            state, reason = "MISS", "无登记记录"
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
        print("=== 素材缓存查询 ===")
        print("  文件    : %s" % fp["filename"])
        print("  状态    : %s" % state)
        print("  原因    : %s" % reason)
        print("  MID     : %s  (%s, %.3f s)" % (fp["mid"], fp["hash_mode"], fp.get("duration_s", 0)))
        if "digest" in out:
            print("  卡片    : %s" % out["card"])
            print("  %s" % out["digest"])
        if state == "HIT":
            print("  ★ 禁止再次调用视频模型：直接读上述卡片，只做主题适配。"
                  "本次估算节省 %d 视频输入 token。" % out["est_tokens_saved"])
        elif state == "HIT_BLOCKED":
            print("  ★ 可读描述用于讨论，但禁止进入时间线；先补授权。")
        elif state == "STALE":
            print("  ★ 旧卡转 superseded；重新本地探测 + 一次全量模型请求 + 新卡。")
        elif state == "MISS":
            print("  ★ 允许发起【一次】全量模型请求：先本地 E1 探测，再用")
            print("    references/09-素材记忆/模板/模型分析提示词.md 一次问全，填卡 → validate → register。")
    return 0


def cmd_register(a):
    root = Path(a.root).resolve() if a.root else default_root()
    ensure_root(root)
    cfg = read_config(root)
    fp = fingerprint(a.video, full=a.full, do_probe=not a.no_probe)
    results = validate_card(a.card, fp=fp)
    print("=== 卡片校验 ===")
    if not print_validation(results):
        print("  校验未通过：请修正后重试。")
        if not a.force:
            print("  登记中止（如需演练可显式 --force，正式流程禁止使用）。")
            return 2
        print("  --force 已启用：仅用于演练/状态机测试，正式流程禁止使用。")
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
        # 若调用方跳过了 lookup，补记一次 MISS，保证命中率分母 = 新分析次数
        have_miss = any(r.get("event") == "MISS" and r.get("mid") == fp["mid"]
                        for r in read_csv(root / "usage.csv", USAGE_FIELDS))
        if not have_miss:
            log_usage(root, "MISS", fp, cfg, note="登记前未查询缓存，补记一次未命中")
        log_usage(root, "REGISTER", fp, cfg, model=a.model or "",
                  actual=a.tokens or "", note="首次全量分析并登记", est=0)
        append_log(root, "REGISTER | %s | %s | card=%s | model=%s" %
                   (fp["mid"], fp["filename"], target.name, a.model or "-"))
    print("  已登记：%s → %s" % (fp["mid"], target))
    return 0


def cmd_use(a):
    root = Path(a.root).resolve() if a.root else default_root()
    ensure_root(root)
    cfg = read_config(root)
    fp = fingerprint(a.video, full=a.full, do_probe=not a.no_probe)
    _, exact, _ = find_index(root, fp)
    if not exact:
        print("  ERROR：素材尚未登记，请先 register。当前 lookup 为 MISS。")
        return 2
    if exact.get("rights_status") != "cleared" and cfg.get("block_unknown_rights", True):
        print("  ERROR：授权状态 %s，不得采用。请先补授权并人工改卡。" %
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
            action = "更新已有适配记录"
        else:
            rows.append({"ts": now(), "theme_id": a.theme, "theme_title": a.theme,
                         "clip_ranges": a.clip or "", "narrative_role": a.role or "",
                         "rights_scope_check": "in_scope", "note": a.note or "",
                         "outcome": ""})
            action = "新增适配记录"
        write_csv(p, THEME_FIELDS, rows)
        log_usage(root, "USE", fp, cfg, theme=a.theme, note="%s；直接读卡，未请求模型" % action)
        append_log(root, "USE | %s | %s | clip=%s | %s" %
                   (fp["mid"], a.theme, a.clip or "-", a.note or "-"))
    print("  %s：%s × %s（%s）" % (action, fp["mid"], a.theme, a.clip or "全段"))
    print("  ★ 本次复用 0 次视频模型请求，直接读取 cards/%s.yaml" % fp["mid"])
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
        verdict = "OK" if ok else "不一致"
        print("  [%s] %s：哈希 %s，卡片 %s" %
              (verdict, fp["mid"], "一致" if ok else "不一致", "存在" if card.is_file() else "缺失"))
        print("       hash_mode=%s（%s）" %
              (fp["hash_mode"], "全文件，无采样盲区" if a.full else "采样模式，未采样区改动可能漏检；交付级建议 --full"))
    elif same_path:
        print("  [STALE] 同路径素材字节已变化：旧 MID %s，需重新分析。" % same_path[0]["mid"])
    else:
        print("  [MISS] 无登记记录。")
    log_usage(root, "VERIFY", fp, cfg, note="verify")
    append_log(root, "VERIFY | %s | %s" % (fp["mid"], a.video))
    return 0


def cmd_themes(a):
    root = Path(a.root).resolve() if a.root else default_root()
    fp = fingerprint(a.video, do_probe=False)
    rows = [r for r in read_csv(root / "themes" / (fp["mid"] + ".csv"), THEME_FIELDS)
            if r.get("theme_id", "").startswith("T-")]
    print("=== %s 的主题适配记录（%d 条）===" % (fp["mid"], len(rows)))
    for r in rows:
        print("  %s | %s | %s | %s | %s" %
              (r["ts"], r["theme_id"], r.get("clip_ranges", ""),
               r.get("narrative_role", ""), r.get("outcome", "") or "待回填"))
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
        print("=== 缓存统计（数值均为估算，非账单）===")
        for k, label in [("materials", "已登记素材"), ("themes", "涉及主题"),
                         ("hits", "HIT 次数"), ("misses", "MISS 次数"),
                         ("uses", "主题复用次数"), ("hit_rate_pct", "命中率 (%)"),
                         ("est_saved_input_tokens", "估算节省视频输入 token"),
                         ("actual_tokens_logged", "已登记实测 token"),
                         ("blocked_materials", "授权未清素材")]:
            print("  %-26s %s" % (label, out[k]))
        print("  估算速率：%d token/秒；真实用量以 usage_metadata 为准。" % out["token_rate"])
        print("  节省比例（按复用次数 N）：1 − 1/N，只计视频输入 token。")
    return 0


def cmd_validate(a):
    fp = fingerprint(a.video) if a.video else None
    return 0 if print_validation(validate_card(a.card, fp=fp)) else 2


def main():
    ap = argparse.ArgumentParser(description="素材描述缓存工具（零依赖）")
    sub = ap.add_subparsers(dest="cmd", required=True)

    def common(p, video=True):
        if video:
            p.add_argument("video", help="素材文件路径")
        p.add_argument("--root", help="缓存根目录（默认 $MDC_HOME，未设则为 ./素材缓存）")
        p.add_argument("--full", action="store_true", help="用全文件 SHA-256（默认 6 MiB 采样）")
        p.add_argument("--no-probe", action="store_true", help="跳过 ffprobe（仅测试用）")

    p = sub.add_parser("fingerprint", help="内容哈希与 ffprobe 规格")
    common(p)
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_fingerprint)

    p = sub.add_parser("lookup", help="★ 分析任何素材前的第一步")
    common(p)
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_lookup)

    p = sub.add_parser("register", help="登记描述卡（自动校验）")
    common(p)
    p.add_argument("--card", required=True, help="mdc-v1 YAML 卡片")
    p.add_argument("--model", default="", help="模型名与版本")
    p.add_argument("--tokens", default="", help="实测 token 数（usage_metadata）")
    p.add_argument("--force", action="store_true", help="校验失败仍登记（仅演练）")
    p.set_defaults(func=cmd_register)

    p = sub.add_parser("use", help="记录一次主题复用（不请求模型）")
    common(p)
    p.add_argument("--theme", required=True, help="T-YYYY-<短名>")
    p.add_argument("--clip", default="", help="MM:SS-MM:SS")
    p.add_argument("--role", default="", help="叙事角色")
    p.add_argument("--note", default="", help="备注")
    p.set_defaults(func=cmd_use)

    p = sub.add_parser("verify", help="重算哈希与卡片比对")
    common(p)
    p.set_defaults(func=cmd_verify)

    p = sub.add_parser("themes", help="列出该素材被哪些主题用过")
    common(p)
    p.set_defaults(func=cmd_themes)

    p = sub.add_parser("stats", help="命中率与估算节省")
    p.add_argument("--root")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_stats)

    p = sub.add_parser("validate", help="校验 mdc-v1 卡片（V1–V8）")
    p.add_argument("card")
    p.add_argument("--video", help="同时比对 content_hash 与实际文件")
    p.set_defaults(func=cmd_validate)

    a = ap.parse_args()
    try:
        return a.func(a)
    except (FileNotFoundError, TimeoutError, OSError) as e:
        print("  ERROR: %s" % e, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
