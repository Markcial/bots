#!/usr/bin/env bash
# Computerized Audio Producer kit: set up the tools. Safe to run again (idempotent).
#   bash setup.sh               check the tools, create .venv with the Kaggle CLI, faster-whisper and ptts
#   bash setup.sh --no-whisper  skip faster-whisper (no speech-to-text lyrics or narration check)
#   bash setup.sh --no-tts      skip ptts (no narration with narrate.py)
# Writes only inside this folder (.venv, work). It never reads, creates or changes Kaggle credentials,
# and it installs nothing system-wide. Free: no account or key is needed for this step.
set -u
cd "$(dirname "$0")" || exit 1
WHISPER=1
TTS=1
for a in "$@"; do
  case "$a" in
    --no-whisper) WHISPER=0 ;;
    --no-tts) TTS=0 ;;
    -h|--help) sed -n '2,7p' "$0"; exit 0 ;;
    *) echo "unknown option: $a"; exit 2 ;;
  esac
done
have() { command -v "$1" >/dev/null 2>&1; }
MISSING=()
ok()  { printf '  [ok]       %s\n' "$*"; }
opt() { printf '  [optional] %s\n' "$*"; }
bad() { printf '  [MISSING]  %s\n' "$1"; MISSING+=("$1"); [ -n "${2:-}" ] && printf '             fix: %s\n' "$2"; }

echo "== Computerized Audio Producer kit: setup =="
echo "-- required tools"
for pair in "curl:curl:curl" "git:git:git" "ffmpeg:ffmpeg:ffmpeg" "ffprobe:ffmpeg:ffmpeg"; do
  IFS=: read -r tool apt brew <<<"$pair"
  if have "$tool"; then ok "$tool"; else bad "$tool" "sudo apt-get install -y $apt  |  brew install $brew"; fi
done
if have ffmpeg; then
  if ffmpeg -hide_banner -filters 2>/dev/null | grep -q loudnorm; then ok "ffmpeg has the loudnorm filter"; else bad "ffmpeg loudnorm filter" "install a full ffmpeg build"; fi
fi

# The Kaggle CLI needs Python 3.11 or newer.
PY=""
for c in python3.13 python3.12 python3.11 python3; do
  if have "$c" && "$c" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)' 2>/dev/null; then PY="$c"; break; fi
done
if [ -n "$PY" ]; then ok "python: $($PY --version 2>&1)"; else bad "python 3.11 or newer" "sudo apt-get install -y python3 python3-venv  |  brew install python@3.12"; fi

if [ -n "$PY" ]; then
  echo "-- local environment (.venv inside this folder)"
  if [ ! -x .venv/bin/python ]; then
    if "$PY" -m venv .venv 2>/dev/null; then ok "created .venv"; else rm -rf .venv; bad "python venv module" "sudo apt-get install -y python3-venv"; fi
  else ok ".venv exists"; fi
  if [ -x .venv/bin/python ]; then
    .venv/bin/python -m pip install -q --upgrade pip >/dev/null 2>&1
    # "six" is listed explicitly: kaggle 2.2.5 imports it without declaring it, and crashes at start without it.
    if .venv/bin/python -m pip install -q kaggle six >/dev/null 2>&1 && KV=$(.venv/bin/kaggle --version 2>&1) && [ -n "$KV" ]; then
      ok "$(echo "$KV" | head -1)"
    else bad "kaggle CLI (install or start failed)" "check the internet connection and run: bash setup.sh"; fi
    if [ "$WHISPER" = 1 ]; then
      if .venv/bin/python -m pip install -q faster-whisper >/dev/null 2>&1; then ok "faster-whisper installed (the model downloads on first use, free)"; else opt "faster-whisper did not install: the lyrics check will be skipped. Retry: bash setup.sh"; fi
    else opt "faster-whisper skipped (--no-whisper)"; fi
    if [ "$TTS" = 1 ]; then
      # ptts runs the Phonon text-to-speech model on the CPU. The wheel has no weights: the default model
      # (Phonon 31M, Apache-2.0, about 60 MB) downloads on first use from Hugging Face, no login.
      if .venv/bin/python -m pip install -q ptts >/dev/null 2>&1 && PV=$(.venv/bin/ptts --version 2>&1) && [ -n "$PV" ]; then
        ok "$PV (narrate.py uses it; the voice model downloads on first use, free)"
      elif have uvx; then opt "ptts did not install here, but uvx is present: narrate.py will run it with 'uvx ptts'"
      else opt "ptts did not install: narrate.py will not work. Install uv (https://docs.astral.sh/uv/) or retry: bash setup.sh"; fi
    else opt "ptts skipped (--no-tts)"; fi
  fi
fi
mkdir -p work && ok "work/ (scratch)"

echo
echo "-- Kaggle sign-in is NOT done here. You do it yourself, once (details in README.md):"
echo "   1. free account at https://www.kaggle.com with a verified phone number"
echo "   2. https://www.kaggle.com/settings/api -> generate a token"
echo "   3. put it where the CLI reads it: run '.venv/bin/kaggle auth login', or save the token as ~/.kaggle/access_token,"
echo "      or the legacy file ~/.kaggle/kaggle.json (chmod 600), or set KAGGLE_API_TOKEN (or KAGGLE_USERNAME and KAGGLE_KEY)"
echo
if [ "${#MISSING[@]}" -eq 0 ]; then echo "SETUP OK. Next: bash doctor.sh"; exit 0; fi
echo "SETUP INCOMPLETE. Missing: ${MISSING[*]}"; exit 1
