#!/usr/bin/env bash
# Methodical Visual Synthesizer kit: self-check. Renders a 2 second test clip and a test avatar, and reports PASS or FAIL with timings.
#   bash doctor.sh
set -u
cd "$(dirname "$0")"
export HF_HOME="${HF_HOME:-$PWD/.cache/hf}"
export PATH="$HOME/.local/bin:$PATH"
mkdir -p out work
REPORT=out/doctor-report.txt; : > "$REPORT"
FAIL=0
say()  { echo "$*" | tee -a "$REPORT"; }
pass() { say "  PASS  $*"; }
fail() { say "  FAIL  $*"; FAIL=1; }
warn() { say "  WARN  $*"; }
now()  { date +%s.%N; }
secs() { awk -v a="$1" -v b="$(now)" 'BEGIN{printf "%.1f", b-a}'; }

say "== Methodical Visual Synthesizer kit: doctor ($(date '+%Y-%m-%d %H:%M %Z')) =="
say "-- toolchain"
command -v node >/dev/null && [ "$(node -p 'process.versions.node.split(".")[0]')" -ge 18 ] && pass "node $(node -v)" || fail "node 18+ missing (bash setup.sh)"
command -v ffmpeg >/dev/null && command -v ffprobe >/dev/null && pass "ffmpeg $(ffmpeg -version | head -1 | awk '{print $3}')" || fail "ffmpeg/ffprobe missing (bash setup.sh)"
[ -d node_modules/@remotion/renderer ] && pass "remotion $(node -p "require('./node_modules/remotion/package.json').version")" || fail "npm packages missing (bash setup.sh)"
[ "$FAIL" = 1 ] && { say; say "DOCTOR FAIL: fix the toolchain first (bash setup.sh)."; exit 1; }

say "-- music bed (4 s, procedural)"
T=$(now)
if node scripts/music.mjs --out=work/doctor-bed.wav --duration=4 >/dev/null 2>work/doctor-bed.err && [ "$(ffprobe -v error -show_entries format=duration -of csv=p=0 work/doctor-bed.wav | cut -d. -f1)" -ge 3 ]; then pass "bed made in $(secs "$T") s (work/doctor-bed.wav)"; else fail "music bed failed: $(tail -2 work/doctor-bed.err)"; fi

say "-- narration engine"
T=$(now)
NOUT=$(node scripts/narrate.mjs "The kit is ready." --out=work/doctor-narration.wav 2>&1)
if echo "$NOUT" | grep -q "engine=phonon"; then pass "free voice works (Phonon) in $(secs "$T") s: $(echo "$NOUT" | tail -1)";
elif echo "$NOUT" | grep -q "engine=none"; then warn "narration is SILENT (captions only). Enable the free voice with: bash setup.sh --with-tts"; else fail "narration step crashed: $(echo "$NOUT" | tail -3)"; fi

say "-- 2 second test clip (1920x1080, 30 fps, captions, closing card, mix)"
T=$(now)
if node scripts/make.mjs configs/doctor.json --seconds=2 --out=out/doctor-clip.mp4 >work/doctor-clip.log 2>&1; then
  CLIP_S=$(secs "$T")
  W=$(ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 out/doctor-clip.mp4)
  D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 out/doctor-clip.mp4)
  A=$(ffprobe -v error -select_streams a:0 -show_entries stream=codec_name -of csv=p=0 out/doctor-clip.mp4)
  RS=$(node -p "require('./work/doctor/last-run.json').renderSeconds.toFixed(1)" 2>/dev/null || echo "?")
  if [ "$W" = "1920,1080" ] && [ -n "$A" ] && awk -v d="$D" 'BEGIN{exit !(d>1.5 && d<2.6)}'; then pass "clip ${W/,/x}, $(printf "%.1f" "$D") s, audio $A, total ${CLIP_S} s (Remotion render ${RS} s) -> $PWD/out/doctor-clip.mp4"; else fail "clip has wrong shape: size=$W duration=$D audio=$A"; fi
else fail "clip render failed. Last log lines:"; tail -8 work/doctor-clip.log | tee -a "$REPORT"; fi

say "-- video QA script (size, frame rate, audio, loudness)"
if [ -f out/doctor-clip.mp4 ]; then if QOUT=$(node scripts/qa.mjs out/doctor-clip.mp4 2>&1); then pass "qa.mjs works: $(echo "$QOUT" | grep 'loudness' | sed 's/^ *INFO *//')"; else fail "qa.mjs failed: $(echo "$QOUT" | tail -3 | tr '\n' ' ')"; fi; fi

say "-- brand book check (contrast pairs, licences, theme tokens)"
if BOUT=$(node scripts/brand-check.mjs --quiet 2>&1); then pass "brand check: template brand book and configs OK ($(echo "$BOUT" | grep -c WARN) warning(s)). Command: node scripts/brand-check.mjs"; else fail "brand check failed: $(echo "$BOUT" | grep FAIL | head -3 | tr '\n' ' ')"; fi
if node --input-type=module -e "import {applyBrand} from './scripts/lib.mjs'; const c=applyBrand({brand:'brand/_template/brand.json'},()=>{}).cfg; if(!c.palette.primary||!c.fonts.heading) process.exit(1)" 2>/dev/null; then pass "a config with \"brand\" takes its palette and fonts from the brand book"; else fail "applyBrand did not load brand/_template/brand.json"; fi

say "-- test avatar still (1024 px square, plus native 512/256/128/48/32 px)"
T=$(now)
if node scripts/still.mjs --out=out/doctor-avatar >work/doctor-still.log 2>&1; then
  S1=$(ffprobe -v error -show_entries stream=width,height -of csv=p=0 out/doctor-avatar-1024.png)
  S2=$(ffprobe -v error -show_entries stream=width,height -of csv=p=0 out/doctor-avatar-32.png)
  if [ "$S1" = "1024,1024" ] && [ "$S2" = "32,32" ]; then pass "avatar set in $(secs "$T") s -> $PWD/out/doctor-avatar-1024.png, $PWD/out/doctor-avatar-32.png, 32 px enlarged: $PWD/out/doctor-avatar-check32.png, sheet: $PWD/out/doctor-avatar-sheet.png"; else fail "avatar sizes wrong: 1024 file is $S1, 32 file is $S2"; fi
else fail "avatar render failed. Last log lines:"; tail -8 work/doctor-still.log | tee -a "$REPORT"; fi

say
if [ "$FAIL" = 0 ]; then say "DOCTOR PASS"; exit 0; else say "DOCTOR FAIL (details above, full logs in work/doctor-*.log)"; exit 1; fi
