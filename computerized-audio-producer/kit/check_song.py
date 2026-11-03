#!/usr/bin/env python3
"""check_song.py: check generated takes (songs, narration, sound effects) before anyone hears them.

  python3 check_song.py out/*.mp3 --duration 30
  python3 check_song.py out/*.mp3 --results runs/RUN_ID/output/out/results.json \\
      --lyrics lyrics.txt --language en --json report.json
  python3 check_song.py out/narration.wav --kind narration --manifest out/narration.json
  python3 check_song.py out/sfx/*.wav --kind sfx

Per take, with ffmpeg (needs ffmpeg and ffprobe on the PATH):
  duration   within 5% of the requested length                      (FAIL if not)
  clipping   volumedetect max_volume at 0.0 dB                      (FAIL)
  silence    mean volume below -50 dB, or silence over 3 s inside   (FAIL)
  loudness   loudnorm integrated LUFS and true peak vs the target   (WARN: fix it with a loudnorm pass)
Optional, with --lyrics (needs faster-whisper, free, runs on the CPU):
  lyrics     share of the lyrics words heard back, per section. PASS >= 85%, WARN 65-85%, FAIL < 65%.
             Speech-to-text under-hears singing, so treat the score as a guide.
With --kind narration and --manifest (the JSON that narrate.py writes), the requested length and the script words
come from the manifest, and the words heard back are compared with the script: PASS >= 95%, WARN 85-95%, FAIL < 85%,
and words heard that are not in the script are counted. Write numbers as words in the script for a clean comparison.
With --kind sfx the loudness target is skipped (effects are too short to measure): the peak and the silence are checked.
Exit code 0 if at least one take passes without FAIL, 1 if every take fails, 2 on a usage error.
Standard library only, plus faster-whisper for --lyrics. Nothing leaves the computer.
"""
import argparse
import difflib
import json
import os
import re
import shutil
import subprocess
import sys

PASS, WARN, FAIL = "PASS", "WARN", "FAIL"
RANK = {PASS: 0, WARN: 1, FAIL: 2}


def worst(*levels):
    return max(levels, key=lambda x: RANK[x])


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def probe_duration(path):
    rc, out = run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path])
    try:
        return float(out.strip().splitlines()[-1])
    except (ValueError, IndexError):
        return None


def loudness(path):
    rc, out = run(["ffmpeg", "-hide_banner", "-nostats", "-i", path,
                   "-af", "loudnorm=I=-14:TP=-1:LRA=11:print_format=json", "-f", "null", "-"])
    m = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", out, re.S)
    if not m:
        return None, None
    d = json.loads(m.group(0))
    try:
        return float(d["input_i"]), float(d["input_tp"])
    except (KeyError, ValueError):
        return None, None


def volume(path):
    rc, out = run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-af", "volumedetect", "-f", "null", "-"])
    mx = re.search(r"max_volume:\s*(-?[\d.]+) dB", out)
    mean = re.search(r"mean_volume:\s*(-?[\d.]+) dB", out)
    return (float(mx.group(1)) if mx else None), (float(mean.group(1)) if mean else None)


def silences(path, duration):
    """List of (start, end) of silences longer than 3 s at -50 dB."""
    rc, out = run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-af", "silencedetect=n=-50dB:d=3", "-f", "null", "-"])
    starts = [float(x) for x in re.findall(r"silence_start:\s*(-?[\d.]+)", out)]
    ends = [float(x) for x in re.findall(r"silence_end:\s*(-?[\d.]+)", out)]
    res = []
    for i, s in enumerate(starts):
        res.append((max(0.0, s), ends[i] if i < len(ends) else duration))
    return res


# ----------------------------------------------------------------- lyrics
def words(text):
    text = re.sub(r"\[[^\]]*\]", " ", text)                      # drop [Verse 1] tags
    return re.findall(r"[^\W_]+(?:'[^\W_]+)?", text.lower(), re.U)


def sections(lyrics):
    """[(name, [words])] split on [Section] tag lines. Lines before the first tag go to 'Lyrics'."""
    out, name, buf = [], "Lyrics", []
    for line in lyrics.splitlines():
        m = re.fullmatch(r"\s*\[([^\]]+)\]\s*", line)
        if m:
            if words(" ".join(buf)):
                out.append((name, words(" ".join(buf))))
            name, buf = m.group(1).strip(), []
        else:
            buf.append(line)
    if words(" ".join(buf)):
        out.append((name, words(" ".join(buf))))
    return out


def score_lyrics(lyrics_text, heard_words):
    secs = sections(lyrics_text)
    flat = [w for _, ws in secs for w in ws]
    if not flat:
        return None
    sm = difflib.SequenceMatcher(a=flat, b=heard_words, autojunk=False)
    hit, heard_hit = set(), 0
    for blk in sm.get_matching_blocks():
        hit.update(range(blk.a, blk.a + blk.size))
        heard_hit += blk.size
    per, pos = [], 0
    for name, ws in secs:
        n = sum(1 for i in range(pos, pos + len(ws)) if i in hit)
        per.append({"section": name, "words": len(ws), "heard": n, "pct": round(100.0 * n / len(ws), 1)})
        pos += len(ws)
    total = round(100.0 * len(hit) / len(flat), 1)
    missed = [flat[i] for i in range(len(flat)) if i not in hit]
    return {"pct": total, "sections": per, "missed_words": missed[:40],
            "extra_words": max(0, len(heard_words) - heard_hit), "script_words": len(flat)}


_WHISPER = {}


def decode_16k(path):
    """Decode to 16 kHz mono float32 with ffmpeg, so faster-whisper never needs its own audio decoder."""
    import numpy as np
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                       capture_output=True)
    if r.returncode != 0 or not r.stdout:
        raise RuntimeError("ffmpeg could not decode the file")
    return np.frombuffer(r.stdout, dtype=np.float32)


def transcribe(path, model_name, language):
    """Returns (text, language) or (None, reason)."""
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        return None, "faster-whisper is not installed (bash setup.sh installs it)"
    try:
        if model_name not in _WHISPER:
            _WHISPER[model_name] = WhisperModel(model_name, device="cpu", compute_type="int8")
        segs, info = _WHISPER[model_name].transcribe(decode_16k(path), language=language, vad_filter=False, beam_size=5)
        return " ".join(s.text for s in segs), info.language
    except Exception as e:  # a broken model download or decoder must not crash the whole check
        return None, "speech-to-text failed: %s" % str(e)[:150]


def verdict_lyrics(pct, kind="song"):
    if kind == "narration":
        return PASS if pct >= 95 else WARN if pct >= 85 else FAIL
    return PASS if pct >= 85 else WARN if pct >= 65 else FAIL


# ----------------------------------------------------------------- one take
def check_take(path, expected, args, lyrics_text):
    r = {"file": path, "checks": {}}
    dur = probe_duration(path)
    r["duration_s"] = dur
    kind = args.kind
    if dur is None or dur < (0.02 if kind == "sfx" else 1):
        r["checks"]["duration"] = (FAIL, "cannot read the duration: the file is missing or broken")
        r["verdict"] = FAIL
        return r
    if expected:
        off = abs(dur - expected) / expected * 100
        lvl = PASS if off <= 5 else FAIL
        r["checks"]["duration"] = (lvl, "%.1f s, asked for %.1f s (%.1f%% off)" % (dur, expected, off))
    else:
        r["checks"]["duration"] = (PASS, "%.1f s (no requested length given)" % dur)

    mx, mean = volume(path)
    r["max_volume_db"], r["mean_volume_db"] = mx, mean
    if mx is None:
        r["checks"]["clipping"] = (FAIL, "volumedetect gave no result")
    elif mx >= -0.01:
        r["checks"]["clipping"] = (FAIL, "max volume %.1f dB: the take clips" % mx)
    else:
        r["checks"]["clipping"] = (PASS, "max volume %.1f dB" % mx)

    sil = silences(path, dur)
    r["silences"] = [[round(a, 1), round(b, 1)] for a, b in sil]
    if mean is None or mean < -50:
        r["checks"]["silence"] = (FAIL, "mean volume %s dB: the take is silent or nearly silent" % mean)
    else:
        middle = [(a, b) for a, b in sil if a > 1.0 and b < dur - 1.0]
        edges = [(a, b) for a, b in sil if (a, b) not in middle]
        if middle:
            r["checks"]["silence"] = (FAIL, "silence over 3 s inside the take at %s s" % ", ".join("%.0f-%.0f" % x for x in middle))
        elif edges:
            r["checks"]["silence"] = (WARN, "long silence at the start or end: %s s" % ", ".join("%.0f-%.0f" % x for x in edges))
        else:
            r["checks"]["silence"] = (PASS, "mean volume %.1f dB, no long silence" % mean)

    lufs, tp = loudness(path)
    r["lufs"], r["true_peak_db"] = lufs, tp
    if kind == "sfx":
        r["checks"]["loudness"] = (PASS, "not measured for short effects (peak %s dB is what matters)" % mx)
    elif lufs is None:
        r["checks"]["loudness"] = (WARN, "loudnorm gave no result")
    else:
        bad = abs(lufs - args.target) > 2 or (tp is not None and tp > args.peak + 0.1)
        msg = "%.1f LUFS, true peak %.1f dBTP (target %.0f LUFS, peak <= %.0f dBTP)" % (lufs, tp if tp is not None else float("nan"), args.target, args.peak)
        r["checks"]["loudness"] = (WARN if bad else PASS, msg + (": normalise before publishing" if bad else ""))

    key = "words" if kind == "narration" else "lyrics"
    if lyrics_text and not args.no_lyrics_check:
        if r["checks"]["silence"][0] == FAIL:
            r["checks"][key] = (FAIL, "skipped: the take is silent")
            r["lyrics_pct"] = 0.0
        else:
            heard, lang = transcribe(path, args.whisper_model, args.language)
            if heard is None:
                r["checks"][key] = (WARN, lang)
            else:
                heard_w = words(heard)
                sc = score_lyrics(lyrics_text, heard_w)
                r["transcript"] = heard.strip()
                if sc is None:
                    r["checks"][key] = (WARN, "the text file has no words")
                else:
                    r["lyrics"] = sc
                    r["lyrics_pct"] = sc["pct"]
                    weak = [s["section"] + " %.0f%%" % s["pct"] for s in sc["sections"] if s["pct"] < 65]
                    lvl = verdict_lyrics(sc["pct"], kind)
                    if kind == "narration":
                        msg = "%.1f%% of the script words heard back (language %s); %d extra word(s) heard" % (
                            sc["pct"], lang, sc["extra_words"])
                        if sc["missed_words"]:
                            msg += "; not heard: " + " ".join(sc["missed_words"][:12])
                        if sc["extra_words"] > max(2, 0.05 * sc["script_words"]):
                            lvl = worst(lvl, WARN)
                        r["checks"]["words"] = (lvl, msg)
                    else:
                        msg = "%.1f%% of the lyrics words heard (language %s)" % (sc["pct"], lang)
                        if weak:
                            msg += "; weak sections: " + ", ".join(weak)
                        r["checks"]["lyrics"] = (lvl, msg)
    r["verdict"] = worst(*[c[0] for c in r["checks"].values()])
    return r


def expected_for(path, args, results):
    stem = os.path.splitext(os.path.basename(path))[0]
    if results and "duration_s" in results and "segments" in results:      # narrate.py manifest
        return results["duration_s"]
    if results and stem in results.get("songs", {}):
        return results["songs"][stem].get("duration_req")
    return args.duration


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+", help="audio files to check")
    ap.add_argument("--duration", type=float, help="requested length in seconds")
    ap.add_argument("--kind", choices=("song", "narration", "sfx"), default="song",
                    help="what is being checked (default song). narration: word check against the script; sfx: no loudness target")
    ap.add_argument("--results", help="results.json from make_song.py: takes the requested length of each song from it")
    ap.add_argument("--manifest", help="narration manifest from narrate.py: takes the length and the script text from it (use with --kind narration)")
    ap.add_argument("--lyrics", help="lyrics (or, with --kind narration, script) text file: also run the speech-to-text check")
    ap.add_argument("--no-lyrics-check", action="store_true")
    ap.add_argument("--language", help="language code for speech-to-text, for example en or es (default: detect)")
    ap.add_argument("--whisper-model", default="small", help="faster-whisper model: tiny, base, small (default), medium")
    ap.add_argument("--target", type=float, default=-14.0, help="loudness target in LUFS (default -14)")
    ap.add_argument("--peak", type=float, default=-1.0, help="true peak ceiling in dBTP (default -1)")
    ap.add_argument("--json", help="write the full report to this file")
    args = ap.parse_args(argv)
    for tool in ("ffmpeg", "ffprobe"):
        if not shutil.which(tool):
            print("check_song: %s not found. Install ffmpeg first (see README.md)." % tool, file=sys.stderr)
            return 2
    results = None
    if args.results:
        try:
            with open(args.results) as f:
                results = json.load(f)
        except (OSError, ValueError) as e:
            print("check_song: cannot read --results: %s" % e, file=sys.stderr)
            return 2
    lyrics_text = None
    if args.manifest:
        if args.kind != "narration":
            print("check_song: --manifest is for --kind narration.", file=sys.stderr)
            return 2
        try:
            with open(args.manifest, encoding="utf-8") as f:
                results = json.load(f)
            lyrics_text = "\n".join(s["text"] for s in results["segments"])
        except (OSError, ValueError, KeyError) as e:
            print("check_song: cannot read --manifest: %s" % e, file=sys.stderr)
            return 2
        if args.language is None and results.get("settings", {}).get("lang"):
            args.language = results["settings"]["lang"]
    if args.lyrics:
        try:
            with open(args.lyrics, encoding="utf-8") as f:
                lyrics_text = f.read()
        except OSError as e:
            print("check_song: cannot read --lyrics: %s" % e, file=sys.stderr)
            return 2
    reports = []
    for path in args.files:
        rep = check_take(path, expected_for(path, args, results), args, lyrics_text)
        reports.append(rep)
        print("== %s: %s" % (os.path.basename(path), rep["verdict"]))
        for name, (lvl, msg) in rep["checks"].items():
            print("  %-4s %-9s %s" % (lvl, name, msg))
    usable = [r for r in reports if r["verdict"] != FAIL]
    best = None
    if usable:
        best = sorted(usable, key=lambda r: (-r.get("lyrics_pct", 0), RANK[r["verdict"]],
                                             abs((r.get("lufs") if r.get("lufs") is not None else -99) - args.target)))[0]
    print("-- summary: %d file(s), %d without FAIL" % (len(reports), len(usable)))
    if best and args.kind == "sfx":
        pass                                   # effects are independent files, not takes of one thing
    elif best:
        print("-- preferred take: %s%s" % (os.path.basename(best["file"]),
              " (%s %.1f%%)" % ("words" if args.kind == "narration" else "lyrics", best["lyrics_pct"]) if "lyrics_pct" in best else ""))
    else:
        hint = {"song": "Change the lyrics, tags or seed and run once more.",
                "narration": "Change the script wording or the seed (narrate.py --seed) and run once more.",
                "sfx": "Change the preset, duration, pitch or seed."}[args.kind]
        print("-- every take FAILED: do not hand any over. " + hint)
    print("-- reminder: these checks are numbers, not listening. Say so when you hand the takes over.")
    if args.json:
        with open(args.json, "w") as f:
            json.dump({"takes": reports, "preferred": best["file"] if best else None}, f, indent=2)
    return 0 if usable else 1


if __name__ == "__main__":
    sys.exit(main())
