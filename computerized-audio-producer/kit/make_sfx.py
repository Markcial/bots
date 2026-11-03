#!/usr/bin/env python3
"""make_sfx.py: synthesise simple sound effects with ffmpeg alone. No external assets, no network, no GPU.

  python3 make_sfx.py --list
  python3 make_sfx.py whoosh riser boom --out-dir out/sfx
  python3 make_sfx.py riser --duration 4 --pitch 150 --out-dir out/sfx --format mp3
  python3 make_sfx.py --import-dir my-cc0-sounds --licence "CC0" --out-dir out/sfx

Presets (--duration in seconds and --pitch in Hz change them; both are optional):
  whoosh       pink noise swept up through a band-pass, bell-shaped volume       0.8 s, pitch 300 Hz
  riser        rising tone plus noise that builds up, cut off at the top         3.0 s, pitch 200 Hz
  boom         impact: a sine that drops in pitch, plus a low noise thump        1.5 s, pitch 140 Hz
  click        very short noise tick                                             0.04 s, pitch 3000 Hz
  glitch       gated, bit-crushed square-wave stutter (the --seed changes it)    0.6 s, pitch 400 Hz
  sweep        white noise swept through a band-pass (use --down for a fall)     2.0 s, pitch 200 Hz
  beep         one sine beep with a short fade                                   0.2 s, pitch 880 Hz
Every preset is peak-normalised to --peak dBFS (default -3), so it cannot clip. Output: WAV (default),
MP3 or FLAC, plus sfx-manifest.json listing preset, duration, pitch, seed and licence of each file.

CC0 or public-domain sounds you provide: --import-dir FOLDER --licence "CC0" converts every audio file in
the folder to the output format with the same peak normalisation, and records the licence text you give
in the manifest. Cap does not download sound libraries. Read the licence on the page you got each file from
(CC BY needs credit, CC BY-NC and "free for personal use" are not enough to publish) and keep a SOURCES.md
in that folder with one line per file: name, URL, author, licence.
Standard library only. Needs ffmpeg and ffprobe.
"""
import argparse
import datetime
import json
import os
import re
import shutil
import subprocess
import sys

RATE = 44100
AUDIO_EXT = (".wav", ".mp3", ".flac", ".ogg", ".opus", ".aac", ".m4a")
SYNTH_LICENCE = "Synthesised from math and noise by ffmpeg; no external assets, nothing to credit."

# name: (default duration, default pitch Hz, description)
PRESETS = {
    "whoosh": (0.8, 300, "pink noise swept up, bell-shaped volume"),
    "riser": (3.0, 200, "rising tone plus building noise"),
    "boom": (1.5, 140, "impact: dropping sine plus low thump"),
    "click": (0.04, 3000, "very short noise tick"),
    "glitch": (0.6, 400, "gated, bit-crushed stutter"),
    "sweep": (2.0, 200, "white noise through a swept band-pass"),
    "beep": (0.2, 880, "one sine beep"),
}


def die(msg, code=2):
    print("make_sfx: " + msg, file=sys.stderr)
    sys.exit(code)


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def sweep_cmds(name, d, f0, f1, steps_per_s=50):
    """asendcmd script that moves the band-pass `name` from f0 to f1 (log scale) over d seconds."""
    n = max(2, int(d * steps_per_s))
    out = []
    for i in range(n + 1):
        t = d * i / n
        f = f0 * (f1 / f0) ** (i / n)
        out.append("%.3f %s f %.1f" % (t, name, f))
    return "; ".join(out)


def noise_band(color, d, f0, f1, amp, seed, q=1.5):
    """A noise source through a band-pass swept from f0 to f1. Returns a filtergraph chunk ending in [label-less] stream."""
    return ("anoisesrc=d=%.3f:c=%s:r=%d:a=%.2f:seed=%d,asendcmd=c='%s',bandpass@bp=f=%.1f:width_type=q:w=%.1f"
            % (d, color, RATE, amp, seed, sweep_cmds("bandpass@bp", d, f0, f1), f0, q))


def chain(preset, d, p, seed, down=False):
    """Returns (inputs, filter_complex) for ffmpeg. The last filter output is labelled [out]."""
    hi = min(p * 12, RATE / 2 - 1000)
    if preset == "whoosh":
        a, b = (hi, p) if down else (p, hi)
        return [], ("%s,volume='pow(sin(PI*t/%.3f),2)':eval=frame[out]" % (noise_band("pink", d, a, b, 0.9, seed), d))
    if preset == "sweep":
        a, b = (hi, p) if down else (p, hi)
        return [], ("%s,afade=t=in:d=%.3f,afade=t=out:st=%.3f:d=%.3f[out]"
                    % (noise_band("white", d, a, b, 0.9, seed, 3), min(0.05, d / 4), d - min(0.1, d / 4), min(0.1, d / 4)))
    if preset == "riser":
        top = min(p * 8, RATE / 2 - 1000)
        tone = "aevalsrc='0.35*sin(2*PI*(%.1f*t+(%.1f-%.1f)*t*t/(2*%.3f)))*pow(t/%.3f,1.5)':d=%.3f:s=%d[tn]" % (p, top, p, d, d, d, RATE)
        nz = "%s,volume='pow(t/%.3f,2)':eval=frame[nz]" % (noise_band("pink", d, p * 2, top * 1.5, 0.9, seed, 2), d)
        return [], "%s;%s;[tn][nz]amix=inputs=2:normalize=0,afade=t=out:st=%.3f:d=0.02[out]" % (tone, nz, max(0.0, d - 0.02))
    if preset == "boom":
        low = max(25.0, p / 4)
        k = 6.0 / d
        body = ("aevalsrc='sin(2*PI*(%.1f*t+(%.1f-%.1f)*(1-exp(-%.3f*t))/%.3f))*exp(-t*%.3f)':d=%.3f:s=%d[bd]"
                % (low, p, low, k, k, 4.0 / d * 1.0, d, RATE))
        thump = ("anoisesrc=d=%.3f:c=brown:r=%d:a=0.9:seed=%d,lowpass=f=%.0f,volume='exp(-t*%.3f)':eval=frame[th]"
                 % (d, RATE, seed, p * 3, 14.0 / d))
        return [], "%s;%s;[bd][th]amix=inputs=2:normalize=0,afade=t=in:d=0.002[out]" % (body, thump)
    if preset == "click":
        return [], ("anoisesrc=d=%.3f:c=white:r=%d:a=0.9:seed=%d,highpass=f=%.0f,"
                    "afade=t=out:st=%.4f:d=%.4f[out]" % (d, RATE, seed, p, d * 0.25, d * 0.75))
    if preset == "beep":
        fade = min(0.08, d / 2)
        return [], ("aevalsrc='sin(2*PI*%.1f*t)':d=%.3f:s=%d,afade=t=in:d=0.005,afade=t=out:st=%.3f:d=%.3f[out]"
                    % (p, d, RATE, d - fade, fade))
    if preset == "glitch":
        # deterministic hash of the time slot: no random number generator, so the same seed gives the same sound
        slot = "floor(t*18)+%d" % seed
        h = lambda m: "mod(sin((%s)*%s)*43758.5453,1)" % (slot, m)
        gate = "gt(abs(%s),0.35)" % h("12.9898")
        freq = "(%.1f*(1+4*abs(%s)))" % (p, h("78.233"))
        wave = "sgn(sin(2*PI*%s*t))" % freq
        crush = "round(%s*0.5*4)/4" % wave
        noise = "0.3*(%s)" % h("t*40+3.1")
        return [], ("aevalsrc='%s*(%s+%s*gt(abs(%s),0.7))':d=%.3f:s=%d,lowpass=f=9000,afade=t=out:st=%.3f:d=0.03[out]"
                    % (gate, crush, noise, h("39.346"), d, RATE, max(0.0, d - 0.03)))
    die("unknown preset %r" % preset)


def peak_normalise(src, dst, peak, fmt):
    """Scale so the loudest sample sits at `peak` dBFS, then encode to fmt. Returns the final max_volume in dB."""
    rc, out = run(["ffmpeg", "-hide_banner", "-nostats", "-i", src, "-af", "volumedetect", "-f", "null", "-"])
    m = re.search(r"max_volume:\s*(-?[\d.]+) dB", out)
    if rc != 0 or not m:
        return None
    gain = peak - float(m.group(1))
    codec = {"wav": ["-c:a", "pcm_s16le"], "mp3": ["-c:a", "libmp3lame", "-q:a", "2"], "flac": ["-c:a", "flac"]}[fmt]
    rc, out = run(["ffmpeg", "-v", "error", "-y", "-i", src, "-af", "volume=%.2fdB" % gain, "-ar", str(RATE)] + codec + [dst])
    if rc != 0 or not os.path.isfile(dst):
        return None
    return peak


def probe_duration(path):
    rc, out = run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path])
    try:
        return round(float(out.strip().splitlines()[-1]), 3)
    except (ValueError, IndexError):
        return None


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("presets", nargs="*", help="presets to make: %s" % ", ".join(PRESETS))
    ap.add_argument("--list", action="store_true", help="list the presets and exit")
    ap.add_argument("--out-dir", default="sfx", help="output folder (default sfx)")
    ap.add_argument("--duration", type=float, help="length in seconds (default per preset)")
    ap.add_argument("--pitch", type=float, help="base frequency in Hz (default per preset)")
    ap.add_argument("--seed", type=int, default=1, help="changes the noise and the glitch pattern (default 1)")
    ap.add_argument("--down", action="store_true", help="whoosh and sweep: sweep downwards instead of up")
    ap.add_argument("--peak", type=float, default=-3.0, help="peak level in dBFS (default -3)")
    ap.add_argument("--format", choices=("wav", "mp3", "flac"), default="wav")
    ap.add_argument("--import-dir", help="a folder of CC0 or public-domain sounds that you provide")
    ap.add_argument("--licence", help="licence of the imported sounds, for example CC0 (required with --import-dir)")
    args = ap.parse_args(argv)

    if args.list:
        for n, (d, p, desc) in PRESETS.items():
            print("%-7s %4.2f s  %5d Hz  %s" % (n, d, p, desc))
        return 0
    if not args.presets and not args.import_dir:
        ap.error("give at least one preset, or --import-dir")
    for tool in ("ffmpeg", "ffprobe"):
        if not shutil.which(tool):
            die("%s not found. Install ffmpeg first (see README.md)." % tool)
    for n in args.presets:
        if n not in PRESETS:
            die("unknown preset %r. Presets: %s" % (n, ", ".join(PRESETS)))
    if args.duration is not None and not 0.01 <= args.duration <= 60:
        die("--duration must be between 0.01 and 60 seconds")
    if args.pitch is not None and not 20 <= args.pitch <= 8000:
        die("--pitch must be between 20 and 8000 Hz")
    if args.peak > -0.5:
        die("--peak must be -0.5 dBFS or lower")
    os.makedirs(args.out_dir, exist_ok=True)
    work = os.path.join(args.out_dir, ".work")
    os.makedirs(work, exist_ok=True)
    manifest_path = os.path.join(args.out_dir, "sfx-manifest.json")
    entries = []
    try:
        for name in args.presets:
            d0, p0, _ = PRESETS[name]
            d = args.duration if args.duration is not None else d0
            p = args.pitch if args.pitch is not None else p0
            _, fc = chain(name, d, p, args.seed, args.down)
            raw = os.path.join(work, name + ".wav")
            rc, out = run(["ffmpeg", "-v", "error", "-y", "-filter_complex", fc, "-map", "[out]", "-t", "%.3f" % d,
                           "-ar", str(RATE), "-ac", "1", "-c:a", "pcm_s16le", raw])
            if rc != 0 or not os.path.isfile(raw):
                die("preset %s failed: %s" % (name, out.strip()[-300:]), 1)
            dst = os.path.join(args.out_dir, "%s-%s.%s" % (name, ("%g" % p).replace(".", "_") + "hz", args.format))
            if peak_normalise(raw, dst, args.peak, args.format) is None:
                die("could not normalise or encode %s (mp3 needs libmp3lame; use --format wav)" % name, 1)
            entries.append({"file": os.path.basename(dst), "preset": name, "duration_s": probe_duration(dst), "pitch_hz": p,
                            "seed": args.seed, "peak_dbfs": args.peak, "source": "synthesised", "licence": SYNTH_LICENCE})
            print("  %-7s %5.2f s  %s" % (name, entries[-1]["duration_s"] or 0, dst))
        if args.import_dir:
            if not args.licence or not args.licence.strip():
                die("--import-dir needs --licence: the licence of the sounds you provide (for example CC0). "
                    "Read it on the page each file came from.")
            if re.search(r"non[- ]?commercial|\bnc\b|personal use", args.licence, re.I):
                die("that licence is not enough to publish or sell the result. Use CC0 or public-domain sounds.")
            if not os.path.isdir(args.import_dir):
                die("--import-dir %s is not a folder" % args.import_dir)
            files = sorted(f for f in os.listdir(args.import_dir) if f.lower().endswith(AUDIO_EXT))
            if not files:
                die("no audio files in %s" % args.import_dir)
            if not any(f.lower() in ("sources.md", "licence.txt", "license.txt", "licence.md", "license.md")
                       for f in os.listdir(args.import_dir)):
                print("make_sfx: WARNING no SOURCES.md or LICENCE.txt in %s. Keep one line per file with its URL, "
                      "author and licence." % args.import_dir, file=sys.stderr)
            for f in files:
                stem = re.sub(r"[^\w\-]+", "-", os.path.splitext(f)[0]).strip("-") or "sound"
                dst = os.path.join(args.out_dir, "import-%s.%s" % (stem, args.format))
                if peak_normalise(os.path.join(args.import_dir, f), dst, args.peak, args.format) is None:
                    print("make_sfx: skipped %s (ffmpeg could not read it)" % f, file=sys.stderr)
                    continue
                entries.append({"file": os.path.basename(dst), "preset": None, "duration_s": probe_duration(dst),
                                "pitch_hz": None, "seed": None, "peak_dbfs": args.peak, "source": "imported: " + f,
                                "licence": args.licence.strip()})
                print("  import  %5.2f s  %s" % (entries[-1]["duration_s"] or 0, dst))
    finally:
        shutil.rmtree(work, ignore_errors=True)

    old = []
    if os.path.isfile(manifest_path):
        try:
            with open(manifest_path, encoding="utf-8") as fh:
                old = json.load(fh).get("files", [])
        except (OSError, ValueError):
            old = []
    names = {e["file"] for e in entries}
    merged = [e for e in old if e.get("file") not in names] + entries
    with open(manifest_path, "w", encoding="utf-8") as fh:
        json.dump({"created": datetime.datetime.now().astimezone().isoformat(timespec="seconds"), "files": merged}, fh, indent=2)
    print("make_sfx: %d file(s) in %s, manifest %s" % (len(entries), args.out_dir, manifest_path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
