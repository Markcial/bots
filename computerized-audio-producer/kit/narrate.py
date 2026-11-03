#!/usr/bin/env python3
"""narrate.py: turn a script file into narration with an open text-to-speech model, on the CPU.

  python3 narrate.py --script script.txt --out out/narration --voice Harper
  python3 narrate.py --script script.txt --out out/narration --voice Juniper --seed 2 --normalize -14
  python3 narrate.py --list-voices

Default engine: Phonon 31M (gradium/phonon-31m-en), Apache-2.0, English only, runs on the CPU, no GPU and
no account. It is driven through the `ptts` command (setup.sh installs it into .venv; without it the script
falls back to `uvx ptts`). The model downloads on first use (about 60 MB) from Hugging Face, no login.

Script file: one line per segment. Blank lines and lines starting with # are ignored.
  Welcome to the show.                      a segment in the default voice (--voice)
  [Easton] This line is read by Easton.     a segment with its own voice (name or catalog voice ID)
  [pause 1.5]                               extra silence of 1.5 s at that point

Output: OUT.wav (or OUT.mp3 with --format mp3) and OUT.json, a manifest with the start, end and text of every
segment. Segments are joined with --pause seconds of silence between them (plus any [pause N] line).
Check the result with: check_song.py OUT.wav --kind narration --manifest OUT.json

Licence guard: Phonon 40M models are CC BY-NC (non-commercial). They are refused unless you pass
--non-commercial, and the manifest then says commercial_use=false. Any other model or engine needs
--licence TEXT, the licence you read on its model page; it is written into the manifest.

No voice cloning: voices are only the stock names of the voice catalog. Reference audio, voice files and
voice prompts are not supported. Models that clone a voice from a clip must not be used for a real person.

Other engines (the owner's choice, not tested here): --engine command --engine-cmd 'mytts --text {text}
--voice {voice} --out {out}' --licence "Apache-2.0". The command must write a WAV file to {out}.
Standard library only. Needs ffmpeg and ffprobe. Nothing leaves the computer except the one-time model download.
"""
import argparse
import datetime
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import wave

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_MODEL = "hf://gradium/phonon-31m-en"
DEFAULT_VOICE = "Harper"
KNOWN_VOICES = "Easton, Harper, Juniper, Imogen (more: --list-voices)"
OK_MODEL = re.compile(r"phonon-31m", re.I)      # Apache-2.0, checked on the model page 2026-11-03
NC_MODEL = re.compile(r"phonon-40m", re.I)      # CC BY-NC-4.0
VOICE_RE = re.compile(r"^[A-Za-z_][\w\-\u00c0-\u024f]{0,63}$")   # a catalog name or ID, never a path or file
SEGMENT_VOICE = re.compile(r"^\[([A-Za-z_][\w\-\u00c0-\u024f]{0,63})\]\s+(.+)$")
PAUSE_LINE = re.compile(r"^\[pause\s+([0-9]+(?:\.[0-9]+)?)\]$", re.I)
RATE = 24000


def die(msg, code=2):
    print("narrate: " + msg, file=sys.stderr)
    sys.exit(code)


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


# ----------------------------------------------------------------- script
def parse_script(path, default_voice):
    """Returns a list of items: {"voice","text"} or {"pause": seconds}."""
    try:
        with open(path, encoding="utf-8") as f:
            lines = f.read().splitlines()
    except OSError as e:
        die("cannot read the script: %s" % e)
    items = []
    for n, raw in enumerate(lines, 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        m = PAUSE_LINE.match(line)
        if m:
            items.append({"pause": float(m.group(1)), "line": n})
            continue
        voice, text = default_voice, line
        m = SEGMENT_VOICE.match(line)
        if m:
            voice, text = m.group(1), m.group(2).strip()
        if not re.search(r"\w", text):
            die("line %d has no words to read" % n)
        items.append({"voice": voice, "text": text, "line": n})
    if not any("text" in i for i in items):
        die("the script has no text lines")
    return items


# ----------------------------------------------------------------- licence guard
def licence_guard(args):
    """Returns (engine_name, model, licence_text, commercial_use). Exits on a refused model."""
    if args.engine == "command":
        if not args.engine_cmd:
            die("--engine command needs --engine-cmd")
        if not args.licence:
            die("--engine command needs --licence: write down the licence of the model you read on its page")
        if re.search(r"non[- ]?commercial|\bnc\b|cc[- ]by[- ]nc", args.licence, re.I) and not args.non_commercial:
            die("that licence looks non-commercial. Pass --non-commercial to use it for private, non-commercial work only.")
        return "command", None, args.licence, not args.non_commercial
    model = args.model or DEFAULT_MODEL
    if NC_MODEL.search(model):
        if not args.non_commercial:
            die("%s is a Phonon 40M model, CC BY-NC: non-commercial only. Use the default Phonon 31M (Apache-2.0), "
                "or pass --non-commercial if this audio will never be published or sold." % model, 3)
        print("narrate: NOTE %s is CC BY-NC. Do not publish or sell this audio. The manifest says commercial_use=false."
              % model, file=sys.stderr)
        return "ptts", model, "CC BY-NC-4.0", False
    if OK_MODEL.search(model):
        return "ptts", model, "Apache-2.0", not args.non_commercial
    if not args.licence:
        die("unknown model %s. Read its licence on the model page, then pass --licence TEXT (for example "
            "--licence Apache-2.0). Models marked non-commercial also need --non-commercial." % model, 3)
    if re.search(r"non[- ]?commercial|\bnc\b|cc[- ]by[- ]nc", args.licence, re.I) and not args.non_commercial:
        die("that licence looks non-commercial. Pass --non-commercial to use it for private, non-commercial work only.", 3)
    return "ptts", model, args.licence, not args.non_commercial


def check_voice(voice):
    if not VOICE_RE.match(voice) or voice.lower().endswith((".wav", ".mp3", ".safetensors", ".flac")):
        die("voice %r is not a catalog voice name. Voice files and reference audio are not supported "
            "(no voice cloning). Known voices: %s" % (voice, KNOWN_VOICES))


# ----------------------------------------------------------------- engines
def ptts_base():
    local = os.path.join(HERE, ".venv", "bin", "ptts")
    if os.path.isfile(local):
        return [local]
    if shutil.which("ptts"):
        return ["ptts"]
    if shutil.which("uvx"):
        return ["uvx", "ptts"]
    return None


def synth_ptts(base, text, voice, out, args, seed, model):
    cmd = base + ["--lang", args.lang, "--quant", args.quant, "--voice", voice, "--seed", str(seed), "-o", out]
    if model != DEFAULT_MODEL:
        cmd += ["--model", model]
    if args.temperature is not None:
        cmd += ["--temperature", str(args.temperature)]
    if args.threads:
        cmd += ["--threads", str(args.threads)]
    cmd += ["--", text]
    r = run(cmd)
    return r.returncode, (r.stderr or r.stdout)[-400:]


def synth_command(template, text, voice, out):
    parts = [p.replace("{text}", text).replace("{voice}", voice).replace("{out}", out) for p in shlex.split(template)]
    r = run(parts)
    return r.returncode, (r.stderr or r.stdout)[-400:]


# ----------------------------------------------------------------- audio helpers
def to_pcm(src, dst, rate):
    r = run(["ffmpeg", "-v", "error", "-y", "-i", src, "-ac", "1", "-ar", str(rate), "-c:a", "pcm_s16le", dst])
    return r.returncode == 0 and os.path.getsize(dst) > 44


def wav_frames(path):
    with wave.open(path, "rb") as w:
        return w.getnframes(), w.readframes(w.getnframes())


def measure_loudness(path):
    r = run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-af",
             "loudnorm=I=-14:TP=-1:LRA=11:print_format=json", "-f", "null", "-"])
    m = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", (r.stdout or "") + (r.stderr or ""), re.S)
    return json.loads(m.group(0)) if m else None


def normalise(src, dst, target, peak, rate):
    """Two-pass loudnorm to `target` LUFS and `peak` dBTP. Returns True on success."""
    r = run(["ffmpeg", "-hide_banner", "-nostats", "-i", src, "-af",
             "loudnorm=I=%s:TP=%s:LRA=11:print_format=json" % (target, peak), "-f", "null", "-"])
    m = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", (r.stdout or "") + (r.stderr or ""), re.S)
    if not m:
        return False
    d = json.loads(m.group(0))
    f = ("loudnorm=I=%s:TP=%s:LRA=11:measured_I=%s:measured_TP=%s:measured_LRA=%s:measured_thresh=%s:"
         "offset=%s:linear=true" % (target, peak, d["input_i"], d["input_tp"], d["input_lra"],
                                    d["input_thresh"], d["target_offset"]))
    r = run(["ffmpeg", "-v", "error", "-y", "-i", src, "-af", f, "-ar", str(rate), "-ac", "1", "-c:a", "pcm_s16le", dst])
    return r.returncode == 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--script", help="script file: one line per segment")
    ap.add_argument("--out", help="output path without extension (for example out/narration)")
    ap.add_argument("--voice", default=DEFAULT_VOICE, help="default voice (default %s). Known: %s" % (DEFAULT_VOICE, KNOWN_VOICES))
    ap.add_argument("--pause", type=float, default=0.5, help="seconds of silence between segments (default 0.5)")
    ap.add_argument("--lead", type=float, default=0.2, help="silence at the start (default 0.2)")
    ap.add_argument("--tail", type=float, default=0.4, help="silence at the end (default 0.4)")
    ap.add_argument("--format", choices=("wav", "mp3"), default="wav")
    ap.add_argument("--seed", type=int, default=1, help="base sampling seed; segment N uses seed+N-1 (default 1). Change it for a second take.")
    ap.add_argument("--temperature", type=float, help="sampling temperature (ptts default if not set)")
    ap.add_argument("--normalize", type=float, metavar="LUFS", help="loudness-normalise the result to this LUFS (for example -14), true peak -1.5 dBTP")
    ap.add_argument("--lang", default="en", help="text normalisation language for ptts (default en; the 31M model is English only)")
    ap.add_argument("--quant", default="q8", help="weight format for ptts (default q8)")
    ap.add_argument("--threads", type=int, help="CPU threads for ptts")
    ap.add_argument("--model", help="ptts model, hf://owner/name or a folder (default %s)" % DEFAULT_MODEL)
    ap.add_argument("--licence", help="licence text you read on the model page (needed for any model that is not Phonon 31M)")
    ap.add_argument("--non-commercial", action="store_true", help="allow a non-commercial model; the audio must never be published or sold")
    ap.add_argument("--engine", choices=("ptts", "command"), default="ptts")
    ap.add_argument("--engine-cmd", help="command template with {text} {voice} {out}, for --engine command")
    ap.add_argument("--keep-parts", action="store_true", help="keep the per-segment WAV files next to the output")
    ap.add_argument("--dry-run", action="store_true", help="parse the script and the licence guard, synthesise nothing")
    ap.add_argument("--list-voices", action="store_true", help="list the stock voices of the catalog and exit")
    args = ap.parse_args(argv)

    if args.list_voices:
        base = ptts_base()
        if not base:
            die("ptts not found. Run bash setup.sh (or install uv: https://docs.astral.sh/uv/).")
        return subprocess.call(base + ["--list-voices"])
    if not args.script or not args.out:
        ap.error("--script and --out are required")
    for tool in ("ffmpeg", "ffprobe"):
        if not shutil.which(tool):
            die("%s not found. Install ffmpeg first (see README.md)." % tool)
    if args.pause < 0 or args.lead < 0 or args.tail < 0:
        die("pauses cannot be negative")

    engine, model, licence, commercial = licence_guard(args)
    check_voice(args.voice)
    items = parse_script(args.script, args.voice)
    for it in items:
        if "voice" in it:
            check_voice(it["voice"])
    n_text = sum(1 for i in items if "text" in i)
    print("narrate: %d segment(s), engine %s, model %s, licence %s%s" % (
        n_text, engine, model or "(your command)", licence, "" if commercial else " (NON-COMMERCIAL ONLY)"))
    if args.dry_run:
        print("narrate: dry run, nothing synthesised.")
        return 0

    base = None
    if engine == "ptts":
        base = ptts_base()
        if not base:
            die("ptts not found. Run bash setup.sh, or install uv (https://docs.astral.sh/uv/) so `uvx ptts` works.")

    out_dir = os.path.dirname(os.path.abspath(args.out))
    os.makedirs(out_dir, exist_ok=True)
    parts_dir = tempfile.mkdtemp(prefix="narrate-", dir=out_dir)
    try:
        pcm = []            # (kind, frames_bytes, nframes, item)
        seg_no = 0
        for it in items:
            if "pause" in it:
                pcm.append(("pause", int(it["pause"] * RATE)))
                continue
            seg_no += 1
            raw = os.path.join(parts_dir, "raw-%03d.wav" % seg_no)
            fixed = os.path.join(parts_dir, "seg-%03d.wav" % seg_no)
            seed = args.seed + seg_no - 1
            if engine == "ptts":
                rc, err = synth_ptts(base, it["text"], it["voice"], raw, args, seed, model)
            else:
                rc, err = synth_command(args.engine_cmd, it["text"], it["voice"], raw)
            if rc != 0 or not os.path.isfile(raw):
                die("segment %d (script line %d) failed: %s" % (seg_no, it["line"], err.strip()[-300:]), 1)
            if not to_pcm(raw, fixed, RATE):
                die("segment %d produced no usable audio" % seg_no, 1)
            os.remove(raw)
            nframes, data = wav_frames(fixed)
            if nframes < RATE * 0.1:
                die("segment %d is shorter than 0.1 s: the model made no speech" % seg_no, 1)
            pcm.append(("seg", data, nframes, dict(it, seg=seg_no, seed=seed)))
            print("  segment %d/%d  %.1f s  [%s] %s" % (seg_no, n_text, nframes / RATE, it["voice"], it["text"][:60]))

        # join: lead, segments with pauses between them, tail
        tmp_wav = os.path.join(parts_dir, "joined.wav")
        manifest_segs, pos, first = [], 0, True
        extra = 0
        with wave.open(tmp_wav, "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(RATE)

            def silence(seconds_frames):
                nonlocal pos
                w.writeframes(b"\x00\x00" * seconds_frames)
                pos += seconds_frames

            silence(int(args.lead * RATE))
            for entry in pcm:
                if entry[0] == "pause":
                    extra += entry[1]
                    continue
                if not first:
                    silence(int(args.pause * RATE) + extra)
                elif extra:
                    silence(extra)
                extra = 0
                first = False
                _, data, nframes, it = entry
                start = pos
                w.writeframes(data)
                pos += nframes
                manifest_segs.append({"index": it["seg"], "line": it["line"], "voice": it["voice"], "text": it["text"],
                                      "seed": it["seed"], "start_s": round(start / RATE, 3),
                                      "end_s": round(pos / RATE, 3), "duration_s": round(nframes / RATE, 3)})
            silence(int(args.tail * RATE) + extra)

        final_wav = tmp_wav
        normalised = None
        if args.normalize is not None:
            nw = os.path.join(parts_dir, "norm.wav")
            if normalise(tmp_wav, nw, args.normalize, -1.5, RATE):
                final_wav, normalised = nw, args.normalize
            else:
                print("narrate: WARNING loudness normalisation failed; the file is not normalised.", file=sys.stderr)
        out_audio = "%s.%s" % (args.out, args.format)
        if args.format == "mp3":
            r = run(["ffmpeg", "-v", "error", "-y", "-i", final_wav, "-c:a", "libmp3lame", "-q:a", "2", out_audio])
            if r.returncode != 0:
                die("mp3 encoding failed (ffmpeg without libmp3lame?). Use --format wav. %s" % r.stderr[-200:], 1)
        else:
            shutil.copyfile(final_wav, out_audio)
        if args.keep_parts:
            keep = "%s-parts" % args.out
            os.makedirs(keep, exist_ok=True)
            for fn in os.listdir(parts_dir):
                if fn.startswith("seg-"):
                    shutil.move(os.path.join(parts_dir, fn), os.path.join(keep, fn))
    finally:
        shutil.rmtree(parts_dir, ignore_errors=True)

    out = run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", out_audio]).stdout.strip()
    total = float(out) if out else pos / RATE
    manifest = {
        "output": os.path.basename(out_audio),
        "duration_s": round(total, 3),
        "segments": manifest_segs,
        "settings": {"pause_s": args.pause, "lead_s": args.lead, "tail_s": args.tail, "seed": args.seed,
                     "temperature": args.temperature, "quant": args.quant if engine == "ptts" else None,
                     "lang": args.lang if engine == "ptts" else None, "normalized_lufs": normalised},
        "engine": engine,
        "model": model,
        "licence": licence,
        "commercial_use": commercial,
        "ai_generated": True,
        "note": "AI-generated speech from a stock voice. Say so when you publish it.",
        "created": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
    }
    with open(args.out + ".json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print("narrate: wrote %s (%.1f s) and %s.json" % (out_audio, total, args.out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
