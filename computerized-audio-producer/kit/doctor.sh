#!/usr/bin/env bash
# Computerized Audio Producer kit: self-check. Prints PASS / WARN / FAIL lines and spends no GPU time.
#   bash doctor.sh              everything
#   bash doctor.sh --offline    skip the network checks
# It never prints a token. It calls `kaggle quota` and `kaggle config view`, which show quota and username only.
# shellcheck disable=SC2015  # pass/warn/fail always return 0, so A && B || C is safe here
set -u
cd "$(dirname "$0")" || exit 1
OFFLINE=0
for a in "$@"; do
  case "$a" in
    --offline) OFFLINE=1 ;;
    -h|--help) sed -n '2,6p' "$0"; exit 0 ;;
    *) echo "unknown option: $a"; exit 2 ;;
  esac
done
mkdir -p work
FAIL=0
pass() { echo "  PASS  $*"; }
warn() { echo "  WARN  $*"; }
fail() { echo "  FAIL  $*"; FAIL=1; }
have() { command -v "$1" >/dev/null 2>&1; }
KG=""; [ -x .venv/bin/kaggle ] && KG=.venv/bin/kaggle || { have kaggle && KG=$(command -v kaggle); }
PYBIN=python3; [ -x .venv/bin/python ] && PYBIN=.venv/bin/python
echo "== Computerized Audio Producer kit: doctor ($(date '+%Y-%m-%d %H:%M %Z')) =="

echo "-- tools"
for t in python3 curl ffmpeg ffprobe; do have "$t" && pass "$t found" || fail "$t missing (bash setup.sh)"; done
if have ffmpeg; then ffmpeg -hide_banner -filters 2>/dev/null | grep -q loudnorm && pass "ffmpeg loudnorm filter present" || fail "ffmpeg has no loudnorm filter"; fi
if [ -z "$KG" ]; then fail "kaggle CLI missing (bash setup.sh)"
elif KV=$($KG --version 2>&1); then pass "kaggle CLI: $(echo "$KV" | head -1)"
else fail "kaggle CLI is installed but crashes at start (bash setup.sh reinstalls it with the missing 'six' package)"; fi
if "$PYBIN" -c 'import faster_whisper' 2>/dev/null; then pass "faster-whisper importable"; else warn "faster-whisper missing: check_song.py --lyrics will not work (bash setup.sh)"; fi
# Narration (optional): the ptts command, from .venv, the PATH or uvx
PT=""; [ -x .venv/bin/ptts ] && PT=.venv/bin/ptts || { have ptts && PT=$(command -v ptts); }
if [ -n "$PT" ] && PV=$("$PT" --version 2>&1); then pass "ptts for narration: $(echo "$PV" | head -1)"
elif have uvx; then warn "ptts is not installed, but uvx is present: narrate.py will run 'uvx ptts' (first run downloads it)"
else warn "ptts missing: narrate.py will not work (bash setup.sh, or install uv)"; fi
[ "$FAIL" = 1 ] && { echo "DOCTOR FAIL: fix the tools first."; exit 1; }

echo "-- sound effects and narration scripts (no network, nothing downloaded)"
if "$PYBIN" make_sfx.py beep click --out-dir work/doctor-sfx >work/sfx.txt 2>&1; then
  pass "make_sfx.py synthesises effects with this ffmpeg"
else fail "make_sfx.py failed with this ffmpeg: $(tail -1 work/sfx.txt)"; fi
rm -rf work/doctor-sfx
printf 'This is a doctor test.\n' > work/doctor-script.txt
if "$PYBIN" narrate.py --script work/doctor-script.txt --out work/doctor-narration --dry-run >work/narrate.txt 2>&1; then
  pass "narrate.py reads a script and passes its licence guard (default model Phonon 31M, Apache-2.0)"
else fail "narrate.py dry run failed: $(tail -1 work/narrate.txt)"; fi
rm -f work/doctor-script.txt
ffmpeg -hide_banner -encoders 2>/dev/null | grep -q libmp3lame && pass "ffmpeg can write MP3" || warn "ffmpeg has no MP3 encoder (libmp3lame): use --format wav"

echo "-- credentials (presence only, never printed)"
FOUND=0
[ -n "${KAGGLE_API_TOKEN:-}" ] && { pass "KAGGLE_API_TOKEN is set"; FOUND=1; }
[ -n "${KAGGLE_KEY:-}" ] && [ -n "${KAGGLE_USERNAME:-}" ] && { pass "KAGGLE_USERNAME and KAGGLE_KEY are set"; FOUND=1; }
for f in "$HOME/.kaggle/access_token" "$HOME/.kaggle/kaggle.json"; do
  if [ -f "$f" ]; then
    FOUND=1
    mode=$(stat -c %a "$f" 2>/dev/null || stat -f %Lp "$f" 2>/dev/null || echo "?")
    if [ "$mode" = 600 ] || [ "$mode" = 400 ]; then pass "$f exists (mode $mode)"; else warn "$f is readable by others (mode $mode). Run: chmod 600 $f"; fi
  fi
done
[ "$FOUND" = 0 ] && warn "no token file or variable seen. The CLI may still hold a 'kaggle auth login' session; the quota check below decides."

echo "-- Kaggle login and GPU quota"
QJ=$($KG -W quota --format json 2>work/quota.err); QRC=$?
if [ "$QRC" != 0 ] || ! echo "$QJ" | "$PYBIN" -c 'import json,sys; json.load(sys.stdin)' 2>/dev/null; then
  QMSG=$( { cat work/quota.err 2>/dev/null; echo "$QJ"; } | tr '\n' ' ' | head -c 300)
  fail "kaggle quota did not work: $QMSG"
  echo "        The owner fixes this once, in their own terminal and browser (README.md, 'Kaggle setup'):"
  echo "        account + verified phone, token from https://www.kaggle.com/settings/api, saved where the CLI reads it."
else
  pass "Kaggle login works"
  USERN=$($KG -W config view 2>/dev/null | sed -n 's/^[ -]*username: *//p' | head -1)
  [ -n "$USERN" ] && [ "$USERN" != None ] && pass "kaggle user found" || warn "username not reported by the CLI; set KAGGLE_USERNAME"
  LEFT=$(echo "$QJ" | "$PYBIN" -c 'import json,sys
for r in json.load(sys.stdin):
    if str(r.get("resource","")).upper()=="GPU": print(str(r.get("remaining","")).rstrip("h")); break')
  if [ -z "$LEFT" ]; then warn "no GPU row in the quota output. Phone verification may be missing."
  elif awk -v l="$LEFT" 'BEGIN{exit !(l+0<=0)}'; then fail "no GPU hours left this week ($LEFT h). Wait for the weekly reset."
  elif awk -v l="$LEFT" 'BEGIN{exit !(l+0<1)}'; then warn "only $LEFT GPU hours left this week (a two-take test needs about 0.2)"
  else pass "GPU quota left this week: $LEFT h"; fi
fi

echo "-- kernel settings (dry run, nothing is pushed)"
if "$PYBIN" make_song.py --jobs examples/jobs.example.json --dry-run --out work/doctor-out >work/dryrun.txt 2>&1; then
  KD=$(sed -n 's/^kernel folder: //p' work/dryrun.txt | head -1)
  if "$PYBIN" - "$KD/kernel-metadata.json" <<'PY'
import json, sys
m = json.load(open(sys.argv[1]))
need = {"enable_gpu": "true", "enable_internet": "true", "machine_shape": "NvidiaTeslaT4", "is_private": "true"}
bad = {k: m.get(k) for k, v in need.items() if m.get(k) != v}
sys.exit(1 if bad else 0)
PY
  then pass "kernel-metadata.json: GPU on, internet on, T4, private"; else fail "kernel-metadata.json is missing GPU, internet, T4 or private"; fi
  if "$PYBIN" -m py_compile "$KD/script.py" 2>/dev/null; then pass "kernel script compiles"; else fail "kernel script has a syntax error"; fi
  rm -rf "$(dirname "$KD")"
else fail "dry run failed: $(tail -2 work/dryrun.txt | tr '\n' ' ')"; fi

echo "-- network"
if [ "$OFFLINE" = 1 ]; then warn "skipped (--offline)"; else
  code() { curl -sL -o /dev/null -m 15 -w '%{http_code}' "$1" 2>/dev/null; }
  [ "$(code https://www.kaggle.com)" = 200 ] && pass "kaggle.com reachable" || fail "kaggle.com not reachable from this computer"
  [ "$(code https://github.com/ace-step/ACE-Step-1.5)" = 200 ] && pass "ACE-Step repository reachable" || warn "github.com/ace-step/ACE-Step-1.5 not reachable from here (the kernel downloads it from Kaggle's side)"
  REF=$(tr -d '[:space:]' < ACE_STEP_REF 2>/dev/null)
  if [ -n "$REF" ] && [ "$REF" != main ]; then
    [ "$(code "https://github.com/ace-step/ACE-Step-1.5/commit/$REF")" = 200 ] && pass "pinned ACE-Step commit ${REF:0:12} exists upstream" || warn "pinned ACE-Step commit ${REF:0:12} not found upstream"
  fi
  [ "$(code https://huggingface.co/ACE-Step/Ace-Step1.5)" = 200 ] && pass "model weights page reachable (no login needed)" || warn "huggingface.co model page not reachable from here"
  [ "$(code https://huggingface.co/gradium/phonon-31m-en)" = 200 ] && pass "Phonon 31M voice model page reachable (narration downloads from here on first use)" || warn "huggingface.co/gradium/phonon-31m-en not reachable: narrate.py cannot download the voice model"
fi

echo "-- note"
echo "  Phone verification cannot be checked from the CLI. If a push fails or the kernel runs without a GPU or internet,"
echo "  verify the phone number in the Kaggle account settings."
echo
if [ "$FAIL" = 0 ]; then echo "DOCTOR PASS"; exit 0; else echo "DOCTOR FAIL (details above)"; exit 1; fi
