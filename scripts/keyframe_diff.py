#!/usr/bin/env python3
"""
keyframe_diff.py - per-shot keyframe baseline and structural diff (zero third-party dependencies).

Purpose
  A style fingerprint records parameters (median shot length, cut density, loudness).
  This tool records the frame-level anchors those parameters were derived from, so that
  after the cut is finished you can diff the result against the reference in one step.

  It does NOT compare pixels. Different footage can never match pixel for pixel, and a
  pixel diff would flag every legitimate difference while missing real drift. What is
  compared is the structure: how many shots, how long each one is, where the cuts land
  after time normalisation, and the objective per-shot image statistics (luma, saturation,
  colour cast) as a trend. Paired keyframes are rendered side by side for human judgement.

Commands
  extract <video> --out DIR      build a baseline (shots.csv + frames/mid/ + sheet + kfs.json)
  compare <ref_dir> <cur_dir>    structural diff of two baselines (report + paired sheet)

Usage
  python keyframe_diff.py extract ref.mp4 --out case/ref_kfs
  python keyframe_diff.py compare case/ref_kfs case/mine_kfs --out case/diff

Exit codes
  extract: 0 ok, 1 usage/input error, 2 ffmpeg failure
  compare: 0 pass or informational only, 2 blocking difference found, 1 usage error

Tested on ffmpeg / ffprobe 8.1.2 (Windows, Git Bash) and Python 3.13.
Note: on Windows a drive-letter colon breaks metadata=print:file=, so per-frame statistics
are parsed from stderr instead of being written to an intermediate file.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

TOOL_VERSION = "kfs-1"

# Comparison tolerances. These are starting values, not validated optima: calibrate them
# against real cases and keep them marked TO VERIFY until then.
DUR_TOTAL_TOL = 0.02          # total runtime drift that is still acceptable
SHOT_COUNT_TOL = 0.15         # shot count drift before the structure is called wrong
CUT_DRIFT_WARN_S = 0.16       # ~4 frames at 25 fps
CUT_DRIFT_BLOCK_S = 0.32      # ~8 frames at 25 fps
MEDIAN_DUR_WARN_RATIO = 0.25  # median shot length drift
DENSITY_CORR_WARN = 0.70      # Pearson correlation of the cut-density curves
LUMA_SHIFT_WARN = 0.15        # SYSTEMATIC (median across shots) luma shift
SAT_SHIFT_WARN = 0.20         # SYSTEMATIC saturation shift
CAST_SHIFT_WARN = 6.0         # mean U/V drift, in signalstats units (~0-255)
TREND_FLIP_WARN = 0.0         # first-vs-last luma trend direction flip


def run(cmd, capture=True):
    """Run a command, returning (code, stdout, stderr)."""
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                       text=True, encoding="utf-8", errors="replace")
    return p.returncode, p.stdout or "", p.stderr or ""


def need_ffmpeg():
    for exe in ("ffmpeg", "ffprobe"):
        code, _, _ = run([exe, "-version"])
        if code != 0:
            sys.stderr.write("ERROR: %s not found on PATH. Objective measurement is impossible without it.\n" % exe)
            sys.exit(1)


def probe(video):
    code, out, err = run([
        "ffprobe", "-v", "error",
        "-show_entries",
        "stream=index,codec_type,codec_name,width,height,r_frame_rate,avg_frame_rate,pix_fmt,"
        "color_space,color_transfer,sample_rate,channels:format=duration,size,bit_rate",
        "-of", "json", str(video),
    ])
    if code != 0:
        sys.stderr.write("ERROR: ffprobe failed on %s\n%s\n" % (video, err.strip()[:400]))
        sys.exit(2)
    return json.loads(out)


def parse_fps(probe_json):
    for s in probe_json.get("streams", []):
        if s.get("codec_type") != "video":
            continue
        for key in ("avg_frame_rate", "r_frame_rate"):
            v = s.get(key) or ""
            if "/" in v:
                num, den = v.split("/")[:2]
                try:
                    num, den = float(num), float(den)
                    if num > 0 and den > 0:
                        return num / den
                except ValueError:
                    pass
            else:
                try:
                    f = float(v)
                    if f > 0:
                        return f
                except ValueError:
                    pass
    return 25.0


def detect_cuts(video, threshold):
    """Return cut times in seconds using scene-change detection (E1, reproducible)."""
    code, _, err = run([
        "ffmpeg", "-hide_banner", "-nostdin", "-i", str(video),
        "-vf", "select='gt(scene,%s)',showinfo" % threshold,
        "-an", "-f", "null", "-",
    ])
    cuts = []
    for m in re.finditer(r"pts_time:([0-9.]+)", err):
        cuts.append(round(float(m.group(1)), 3))
    return sorted(set(cuts))


def frame_stats(video):
    """Per-frame luma/saturation statistics. Parsed from stderr; see the Windows note above."""
    code, _, err = run([
        "ffmpeg", "-hide_banner", "-nostdin", "-i", str(video),
        "-vf", "signalstats,metadata=print", "-an", "-f", "null", "-",
    ])
    frames, cur = [], None
    for line in err.splitlines():
        m = re.search(r"pts_time:([0-9.]+)", line)
        if m:
            if cur is not None:
                frames.append(cur)
            cur = {"t": float(m.group(1))}
            continue
        if cur is None:
            continue
        # ffmpeg prefixes every line with "[Parsed_metadata_1 @ 0x...] ", so search, never match.
        kv = re.search(r"lavfi\.signalstats\.([A-Z]+)=([-0-9.]+)", line)
        if kv:
            cur[kv.group(1)] = float(kv.group(2))
    if cur is not None:
        frames.append(cur)
    return frames


def shot_bounds(cuts, duration):
    """Turn cut times into [start, end) shot ranges, always covering the whole clip."""
    edges = [0.0] + [c for c in cuts if 0.0 < c < duration] + [duration]
    out = []
    for i in range(len(edges) - 1):
        a, b = edges[i], edges[i + 1]
        if b - a <= 0.001:
            continue
        out.append((a, b))
    return out


def value_at(frames, t):
    """Nearest measured frame to time t."""
    if not frames:
        return {}
    lo, hi = 0, len(frames) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if frames[mid]["t"] < t:
            lo = mid + 1
        else:
            hi = mid
    cand = [frames[max(0, lo - 1)], frames[lo]]
    return min(cand, key=lambda f: abs(f["t"] - t))


def extract_frames(video, shots, offsets, outdir, width, fps):
    """One ffmpeg pass: pull the mid-shot frame of every shot into frames/mid/shotNNN.png."""
    middir = outdir / "frames" / "mid"
    middir.mkdir(parents=True, exist_ok=True)
    for old in middir.glob("shot*.png"):
        old.unlink()

    picks = []
    for i, (a, b) in enumerate(shots, 1):
        t = a + (b - a) * 0.5
        picks.append((i, t, int(round(t * fps))))

    sel = "+".join("eq(n,%d)" % n for _, _, n in picks)
    tmp = outdir / "frames" / "_raw"
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir(parents=True, exist_ok=True)

    code, _, err = run([
        "ffmpeg", "-hide_banner", "-nostdin", "-i", str(video),
        "-vf", "select='%s',scale=%d:-2" % (sel, width),
        "-fps_mode", "passthrough", "-an",
        str(tmp / "f%04d.png"),
    ])
    produced = sorted(tmp.glob("f*.png"))
    if code != 0 or len(produced) != len(picks):
        sys.stderr.write(
            "WARN: expected %d keyframes, got %d (ffmpeg exit %d). "
            "Falling back to per-shot seeking, which is slower.\n"
            % (len(picks), len(produced), code))
        for i, t, _ in picks:
            dst = middir / ("shot%03d.png" % i)
            run(["ffmpeg", "-hide_banner", "-v", "error", "-ss", "%.3f" % t,
                 "-i", str(video), "-frames:v", "1",
                 "-vf", "scale=%d:-2" % width, "-y", str(dst)])
    else:
        for (i, _, _), src in zip(picks, produced):
            shutil.copyfile(src, middir / ("shot%03d.png" % i))
    shutil.rmtree(tmp, ignore_errors=True)
    return middir


def build_sheet(middir, out_png, fps_ignored=1):
    files = sorted(middir.glob("shot*.png"))
    if not files:
        return False
    n = len(files)
    code, _, err = run([
        "ffmpeg", "-hide_banner", "-v", "error", "-framerate", "1",
        "-i", str(middir / "shot%03d.png"),
        "-vf", "scale=240:-2,tile=1x%d" % n, "-frames:v", "1",
        "-update", "1", "-y", str(out_png),
    ])
    return code == 0 and out_png.exists()


def cmd_extract(args):
    need_ffmpeg()
    video = Path(args.video)
    if not video.is_file():
        sys.stderr.write("ERROR: video not found: %s\n" % video)
        return 1
    outdir = Path(args.out)
    (outdir / "frames" / "mid").mkdir(parents=True, exist_ok=True)

    pj = probe(video)
    fps = parse_fps(pj)
    duration = float(pj.get("format", {}).get("duration") or 0.0)
    if duration <= 0:
        sys.stderr.write("ERROR: could not read duration\n")
        return 2

    cuts = detect_cuts(video, args.scene)
    if args.cuts:
        p = Path(args.cuts)
        if not p.is_file():
            sys.stderr.write("ERROR: cuts file not found: %s\n" % p)
            return 1
        cuts = sorted({round(float(x), 3) for x in p.read_text(encoding="utf-8").split() if x.strip()})

    shots = shot_bounds(cuts, duration)
    frames = frame_stats(video)
    offsets = [float(x) for x in args.offsets.split(",") if x.strip()]

    rows = []
    for i, (a, b) in enumerate(shots, 1):
        dur = b - a
        samples = {}
        for off in offsets:
            f = value_at(frames, a + dur * off)
            samples[off] = f
        mid = samples.get(0.5) or value_at(frames, a + dur * 0.5)
        row = {
            "idx": i,
            "t_in": round(a, 3),
            "t_out": round(b, 3),
            "dur_s": round(dur, 3),
            "y_mid": round(mid.get("YAVG", 0.0), 2),
            "sat_mid": round(mid.get("SATAVG", 0.0), 2),
            "u_mid": round(mid.get("UAVG", 0.0), 2),
            "v_mid": round(mid.get("VAVG", 0.0), 2),
            "frame_file": "frames/mid/shot%03d.png" % i,
            "shot_size": "",
            "composition": "",
            "note": "",
        }
        for off in offsets:
            tag = "y%d" % int(off * 100)
            row[tag] = round(samples[off].get("YAVG", 0.0), 2)
        rows.append(row)

    middir = extract_frames(video, shots, offsets, outdir, args.width, fps)
    sheet_ok = build_sheet(middir, outdir / "kfs_sheet.png")

    header = ["idx", "t_in", "t_out", "dur_s"] + \
             ["y%d" % int(o * 100) for o in offsets] + \
             ["y_mid", "sat_mid", "u_mid", "v_mid", "frame_file", "shot_size", "composition", "note"]
    with (outdir / "shots.csv").open("w", encoding="utf-8", newline="") as f:
        f.write(",".join(header) + "\n")
        for r in rows:
            f.write(",".join(str(r.get(k, "")) for k in header) + "\n")

    meta = {
        "kfs_version": TOOL_VERSION,
        "source": str(video.resolve()),
        "filename": video.name,
        "duration_s": round(duration, 3),
        "fps": round(fps, 3),
        "shot_count": len(rows),
        "cut_count": len(cuts),
        "cut_times": cuts,
        "scene_threshold": args.scene,
        "sample_offsets": offsets,
        "sheet": "kfs_sheet.png" if sheet_ok else None,
        "probe": pj,
        "columns_for_human": ["shot_size", "composition", "note"],
        "note": "shot_size / composition are filled in by a human; the tool measures only the numbers.",
    }
    (outdir / "kfs.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")

    durs = sorted(r["dur_s"] for r in rows)
    med = durs[len(durs) // 2] if durs else 0.0
    print("=== Keyframe baseline ===")
    print("  source      : %s" % video.name)
    print("  duration    : %.2f s | fps %.3f" % (duration, fps))
    print("  shots       : %d (median %.2f s, shortest %.2f s, longest %.2f s)"
          % (len(rows), med, durs[0] if durs else 0, durs[-1] if durs else 0))
    print("  keyframes   : %s" % middir)
    print("  sheet       : %s" % (outdir / "kfs_sheet.png" if sheet_ok else "FAILED"))
    print("  table       : %s" % (outdir / "shots.csv"))
    print("  NEXT: fill shot_size / composition in shots.csv by hand, then cut, then run compare.")
    return 0


def read_shots(d):
    p = Path(d) / "shots.csv"
    if not p.is_file():
        return None
    lines = p.read_text(encoding="utf-8").splitlines()
    if not lines:
        return None
    head = lines[0].split(",")
    rows = []
    for ln in lines[1:]:
        if not ln.strip():
            continue
        parts = ln.split(",")
        if len(parts) < len(head):
            parts += [""] * (len(head) - len(parts))
        r = {}
        for k, v in zip(head, parts):
            r[k] = v
        try:
            r["_idx"] = int(r["idx"])
            r["_dur"] = float(r["dur_s"])
            r["_y"] = float(r["y_mid"] or 0)
            r["_sat"] = float(r["sat_mid"] or 0)
            r["_u"] = float(r["u_mid"] or 0)
            r["_v"] = float(r["v_mid"] or 0)
            r["_tin"] = float(r["t_in"] or 0)
        except ValueError:
            continue
        rows.append(r)
    return rows


def rel_drift(a, b, floor=1.0):
    base = max(abs(a), floor)
    return abs(b - a) / base


def pearson(xs, ys):
    n = min(len(xs), len(ys))
    if n < 3:
        return 1.0
    xs, ys = xs[:n], ys[:n]
    mx, my = sum(xs) / n, sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    dx = sum((x - mx) ** 2 for x in xs) ** 0.5
    dy = sum((y - my) ** 2 for y in ys) ** 0.5
    if dx == 0 or dy == 0:
        return 1.0
    return num / (dx * dy)


def density_curve(rows, duration, buckets=8):
    counts = [0] * buckets
    for r in rows:
        b = int(r["_tin"] / max(duration, 0.001) * buckets)
        counts[min(b, buckets - 1)] += 1
    span = duration / buckets
    return [c / span * 60.0 for c in counts] if span > 0 else counts


def cmd_compare(args):
    ref_dir, cur_dir = Path(args.ref), Path(args.cur)
    ref, cur = read_shots(ref_dir), read_shots(cur_dir)
    if ref is None or cur is None:
        sys.stderr.write("ERROR: shots.csv missing in %s\n"
                         % (ref_dir if ref is None else cur_dir))
        return 1

    ref_meta = json.loads((ref_dir / "kfs.json").read_text(encoding="utf-8")) \
        if (ref_dir / "kfs.json").is_file() else {}
    cur_meta = json.loads((cur_dir / "kfs.json").read_text(encoding="utf-8")) \
        if (cur_dir / "kfs.json").is_file() else {}

    outdir = Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)

    dur_r = float(ref_meta.get("duration_s") or sum(r["_dur"] for r in ref))
    dur_c = float(cur_meta.get("duration_s") or sum(r["_dur"] for r in cur))
    fps = float(cur_meta.get("fps") or ref_meta.get("fps") or 25.0)

    findings = []   # (tier, code, message)

    def add(tier, code, msg):
        findings.append((tier, code, msg))

    # --- tier 1: structure -------------------------------------------------------
    if dur_r > 0:
        d = abs(dur_c - dur_r) / dur_r
        if d > DUR_TOTAL_TOL:
            add("BLOCK", "T1-duration", "Runtime %.2f s vs reference %.2f s (%.1f%% off, tolerance %.0f%%)"
                % (dur_c, dur_r, d * 100, DUR_TOTAL_TOL * 100))

    n_r, n_c = len(ref), len(cur)
    count_gap = abs(n_c - n_r) / max(n_r, 1)
    if count_gap > SHOT_COUNT_TOL:
        add("BLOCK", "T1-shotcount",
            "Shot count %d vs reference %d (%.0f%% off, tolerance %.0f%%) - the structure differs, "
            "not just the timing" % (n_c, n_r, count_gap * 100, SHOT_COUNT_TOL * 100))
    elif n_c != n_r:
        add("WARN", "T1-shotcount",
            "Shot count %d vs reference %d (%+d) - within tolerance but the beat pattern shifted"
            % (n_c, n_r, n_c - n_r))

    # time-normalised cut positions
    drift_worst = (0.0, 0)
    n = min(n_r, n_c)
    for i in range(n):
        tr = ref[i]["_tin"] / max(dur_r, 0.001)
        tc = cur[i]["_tin"] / max(dur_c, 0.001)
        drift_s = abs(tr - tc) * dur_r
        if drift_s > drift_worst[0]:
            drift_worst = (drift_s, i + 1)
    if drift_worst[0] > CUT_DRIFT_BLOCK_S:
        add("BLOCK", "T1-cutdrift",
            "Cut %d lands %.2f s away from the reference position after time normalisation "
            "(limit %.2f s)" % (drift_worst[1], drift_worst[0], CUT_DRIFT_BLOCK_S))
    elif drift_worst[0] > CUT_DRIFT_WARN_S:
        add("WARN", "T1-cutdrift",
            "Cut %d drifts %.2f s from the reference position (watch threshold %.2f s)"
            % (drift_worst[1], drift_worst[0], CUT_DRIFT_WARN_S))

    # --- tier 2: rhythm and image profile ---------------------------------------
    med_r = sorted(r["_dur"] for r in ref)[n_r // 2]
    med_c = sorted(r["_dur"] for r in cur)[n_c // 2]
    if med_r > 0 and abs(med_c - med_r) / med_r > MEDIAN_DUR_WARN_RATIO:
        add("WARN", "T2-median",
            "Median shot %.2f s vs reference %.2f s (%.0f%% off)" % (med_c, med_r, abs(med_c - med_r) / med_r * 100))

    dens_r = density_curve(ref, dur_r)
    dens_c = density_curve(cur, dur_c)
    corr = pearson(dens_r, dens_c)
    if corr < DENSITY_CORR_WARN:
        add("WARN", "T2-density",
            "Cut-density curve correlation %.2f (below %.2f) - the pacing shape differs"
            % (corr, DENSITY_CORR_WARN))

    # Image profile. A per-shot comparison is dominated by content: the two clips use different
    # footage by definition, so shot 3 being darker than the reference's shot 3 proves nothing.
    # Only a SYSTEMATIC shift across the whole clip points at a grade, LUT or transfer problem,
    # so that is what gets flagged. Per-shot outliers are listed as an INFO prompt to look at
    # specific rows of the paired sheet.
    def med(vals):
        v = sorted(vals)
        return v[len(v) // 2] if v else 0.0

    if n:
        my_r = med([ref[i]["_y"] for i in range(n)])
        my_c = med([cur[i]["_y"] for i in range(n)])
        if my_r > 0 and abs(my_c - my_r) / my_r > LUMA_SHIFT_WARN:
            add("WARN", "T2-luma",
                "Systematic luma shift: median %.1f vs reference %.1f (%.0f%%) - check grade, "
                "LUT and transfer function before blaming the content"
                % (my_c, my_r, abs(my_c - my_r) / my_r * 100))

        ms_r = med([ref[i]["_sat"] for i in range(n)])
        ms_c = med([cur[i]["_sat"] for i in range(n)])
        if ms_r > 0 and abs(ms_c - ms_r) / ms_r > SAT_SHIFT_WARN:
            add("WARN", "T2-saturation",
                "Systematic saturation shift: median %.1f vs reference %.1f (%.0f%%)"
                % (ms_c, ms_r, abs(ms_c - ms_r) / ms_r * 100))

        du = med([cur[i]["_u"] for i in range(n)]) - med([ref[i]["_u"] for i in range(n)])
        dv = med([cur[i]["_v"] for i in range(n)]) - med([ref[i]["_v"] for i in range(n)])
        if abs(du) > CAST_SHIFT_WARN or abs(dv) > CAST_SHIFT_WARN:
            add("WARN", "T2-cast",
                "Colour cast: mean U %+.1f / V %+.1f against the reference - the balance is "
                "shifting towards %s" % (du, dv, "blue" if du + dv > 0 else "red"))

        if n >= 4:
            tr = ref[n - 1]["_y"] - ref[0]["_y"]
            tc = cur[n - 1]["_y"] - cur[0]["_y"]
            if tr * tc < 0 and abs(tr) > 4 and abs(tc) > 4:
                add("WARN", "T2-lumatrend",
                    "Luma trend direction flipped: reference %+.0f over the clip, current %+.0f"
                    % (tr, tc))

        worst = sorted(range(n), key=lambda i: -rel_drift(ref[i]["_y"], cur[i]["_y"]))[:3]
        add("INFO", "T3-spread",
            "Largest per-shot luma gaps (content normally differs - look at these rows in the sheet, "
            "do not auto-fix): " + ", ".join(
                "shot %d %.1f->%.1f" % (i + 1, ref[i]["_y"], cur[i]["_y"]) for i in worst))

    # --- tier 3: human fields ---------------------------------------------------
    fill_r = sum(1 for r in ref if (r.get("shot_size") or "").strip())
    fill_c = sum(1 for r in cur if (r.get("shot_size") or "").strip())
    if fill_r == 0:
        add("INFO", "T3-annotation",
            "Reference shot_size is empty - the shot-size sequence was not compared. "
            "Fill it in shots.csv to enable that check.")
    if fill_r and fill_c:
        mismatch = []
        for i in range(n):
            a = (ref[i].get("shot_size") or "").strip().upper()
            b = (cur[i].get("shot_size") or "").strip().upper()
            if a and b and a != b:
                mismatch.append((i + 1, a, b))
        if mismatch:
            add("WARN", "T3-shotsize",
                "Shot-size sequence diverges at %d of %d shots (first: shot %d %s -> %s)"
                % (len(mismatch), n, mismatch[0][0], mismatch[0][1], mismatch[0][2]))
    elif fill_r and not fill_c:
        add("INFO", "T3-annotation",
            "Current cut shot_size is empty - fill it in to compare the shot-size sequence.")

    # --- paired sheet -----------------------------------------------------------
    sheet_ok = build_diff_sheet(ref_dir, cur_dir, n, outdir)
    if not sheet_ok:
        add("INFO", "T3-sheet", "Paired keyframe sheet could not be built (missing frames/mid).")

    # --- report -----------------------------------------------------------------
    order = {"BLOCK": 0, "WARN": 1, "INFO": 2}
    findings.sort(key=lambda f: order[f[0]])
    blocks = [f for f in findings if f[0] == "BLOCK"]
    warns = [f for f in findings if f[0] == "WARN"]

    L = []
    L.append("# Structural diff: reference vs current cut\n")
    L.append("> Generated by `scripts/keyframe_diff.py` (%s). Structural and parametric only - "
             "pixels are never compared, because different footage cannot match pixel for pixel.\n" % TOOL_VERSION)
    L.append("| | Reference | Current |")
    L.append("| --- | --- | --- |")
    L.append("| File | %s | %s |" % (ref_meta.get("filename", "?"), cur_meta.get("filename", "?")))
    L.append("| Runtime | %.2f s | %.2f s |" % (dur_r, dur_c))
    L.append("| Shots | %d | %d |" % (n_r, n_c))
    L.append("| Median shot | %.2f s | %.2f s |" % (med_r, med_c))
    L.append("| Cut density corr | | %.2f |" % corr)
    L.append("")
    L.append("## Verdict")
    if blocks:
        L.append("**BLOCKING - %d item(s) must be fixed before delivery.**" % len(blocks))
    elif warns:
        L.append("**PASS with %d warning(s)** - deliverable once each warning is either fixed or accepted in writing." % len(warns))
    else:
        L.append("**PASS** - no structural difference outside tolerance.")
    L.append("")
    if findings:
        L.append("| Tier | Code | Finding |")
        L.append("| --- | --- | --- |")
        for tier, code, msg in findings:
            L.append("| %s | `%s` | %s |" % (tier, code, msg.replace("|", "/")))
        L.append("")
    else:
        L.append("No findings at all: structure, rhythm and image profile all sit inside tolerance.\n")

    L.append("## Per-shot table (first %d shots)\n" % min(n, 40))
    L.append("| # | ref in | cur in | ref dur | cur dur | ref luma | cur luma | ref sat | cur sat |")
    L.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for i in range(min(n, 40)):
        L.append("| %d | %.2f | %.2f | %.2f | %.2f | %.1f | %.1f | %.1f | %.1f |"
                 % (i + 1, ref[i]["_tin"], cur[i]["_tin"],
                    ref[i]["_dur"], cur[i]["_dur"], ref[i]["_y"], cur[i]["_y"],
                    ref[i]["_sat"], cur[i]["_sat"]))
    L.append("")
    L.append("## How to read the paired sheet")
    L.append("`diff_sheet.png`: one row per shot, **left = reference, right = current cut**. "
             "Rows are matched by shot index after time normalisation, so row 1 is the first shot of each. "
             "Use it to judge composition, shot size and subject placement - the things the numbers cannot see.")
    L.append("")
    L.append("## What this diff cannot tell you")
    L.append("- Whether the shot is *good*: composition quality, performance, whether the subject is on brand.")
    L.append("- Whether a different flat grade is intentional: luma and saturation drift may be a deliberate choice, "
             "so a WARN is a prompt to look, not a defect.")
    L.append("- Anything about sound. Loudness and J/L-cut offsets are checked by `qc_scan.sh` and the audio volume.")
    L.append("")
    L.append("Tolerances in this report are starting values, not validated optima: TO VERIFY against real cases.")
    (outdir / "diff_report.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    with (outdir / "diff.csv").open("w", encoding="utf-8", newline="") as f:
        f.write("idx,ref_t_in,cur_t_in,ref_dur,cur_dur,ref_luma,cur_luma,ref_sat,cur_sat,"
                "dur_delta_s,luma_drift,sat_drift\n")
        for i in range(n):
            f.write("%d,%.3f,%.3f,%.3f,%.3f,%.2f,%.2f,%.2f,%.2f,%.3f,%.3f,%.3f\n" % (
                i + 1,
                ref[i]["_tin"], cur[i]["_tin"],
                ref[i]["_dur"], cur[i]["_dur"], ref[i]["_y"], cur[i]["_y"],
                ref[i]["_sat"], cur[i]["_sat"],
                cur[i]["_dur"] - ref[i]["_dur"],
                rel_drift(ref[i]["_y"], cur[i]["_y"]),
                rel_drift(ref[i]["_sat"], cur[i]["_sat"])))

    print("=== Structural diff ===")
    print("  reference : %s (%d shots, %.2f s)" % (ref_meta.get("filename", "?"), n_r, dur_r))
    print("  current   : %s (%d shots, %.2f s)" % (cur_meta.get("filename", "?"), n_c, dur_c))
    print("  blocking  : %d | warning: %d | info: %d" % (len(blocks), len(warns), len(findings) - len(blocks) - len(warns)))
    for tier, code, msg in findings:
        print("    [%s] %s: %s" % (tier, code, msg))
    print("  report    : %s" % (outdir / "diff_report.md"))
    print("  sheet     : %s" % (outdir / "diff_sheet.png" if sheet_ok else "FAILED"))
    print("  table     : %s" % (outdir / "diff.csv"))
    return 2 if blocks else 0


def build_diff_sheet(ref_dir, cur_dir, n, outdir):
    """Left = reference mid-frames, right = current mid-frames, one row per shot."""
    if n <= 0:
        return False
    rm = ref_dir / "frames" / "mid"
    cm = cur_dir / "frames" / "mid"
    if not rm.is_dir() or not cm.is_dir():
        return False

    strips = []
    for d, tag in ((rm, "ref"), (cm, "cur")):
        out = outdir / ("_strip_%s.png" % tag)
        code, _, err = run([
            "ffmpeg", "-hide_banner", "-v", "error", "-framerate", "1",
            "-i", str(d / "shot%03d.png"),
            "-vf", "scale=240:-2,tile=1x%d" % n, "-frames:v", "1",
            "-update", "1", "-y", str(out),
        ])
        if code != 0 or not out.exists():
            sys.stderr.write("WARN: strip %s failed: %s\n" % (tag, err.strip()[:200]))
            return False
        strips.append(out)

    code, _, err = run([
        "ffmpeg", "-hide_banner", "-v", "error",
        "-i", str(strips[0]), "-i", str(strips[1]),
        "-filter_complex", "[0:v][1:v]hstack=inputs=2[v]",
        "-map", "[v]", "-frames:v", "1", "-update", "1", "-y",
        str(outdir / "diff_sheet.png"),
    ])
    for s in strips:
        s.unlink(missing_ok=True)
    return code == 0 and (outdir / "diff_sheet.png").exists()


def main():
    ap = argparse.ArgumentParser(
        description="Per-shot keyframe baseline and structural diff (zero third-party dependencies)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    e = sub.add_parser("extract", help="build a keyframe baseline from a video")
    e.add_argument("video")
    e.add_argument("--out", required=True, help="output directory")
    e.add_argument("--scene", default="0.25", help="scene-change threshold (default 0.25, TO VERIFY)")
    e.add_argument("--offsets", default="0.15,0.5,0.85",
                   help="normalised sample positions inside each shot")
    e.add_argument("--width", type=int, default=240, help="keyframe width in px (default 240)")
    e.add_argument("--cuts", help="reuse an existing cuts.txt instead of detecting again")

    c = sub.add_parser("compare", help="structurally diff two baselines")
    c.add_argument("ref", help="reference baseline directory")
    c.add_argument("cur", help="current cut baseline directory")
    c.add_argument("--out", required=True, help="output directory")

    args = ap.parse_args()
    if args.cmd == "extract":
        return cmd_extract(args)
    return cmd_compare(args)


if __name__ == "__main__":
    sys.exit(main())
