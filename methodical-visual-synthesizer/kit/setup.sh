#!/usr/bin/env bash
# Methodical Visual Synthesizer kit: set up the toolchain. Safe to run again (idempotent).
#   bash setup.sh                  check everything, install the user-level parts (npm packages, Remotion's headless browser)
#   bash setup.sh --install-system also install Node and ffmpeg with the system package manager (apt/brew) if they are missing
#   bash setup.sh --with-tts       also install `uv` (user-level) and warm up the free Phonon voice (about 60 MB model download)
# Nothing here needs an account, a card, or an API key. It prints what is missing and the exact command to fix it.
set -u
cd "$(dirname "$0")"
INSTALL_SYSTEM=0; WITH_TTS=0
for a in "$@"; do
  case "$a" in
    --install-system) INSTALL_SYSTEM=1 ;;
    --with-tts) WITH_TTS=1 ;;
    *) echo "unknown option: $a"; exit 2 ;;
  esac
done
[ "${MVS_ALLOW_SYSTEM_INSTALL:-0}" = 1 ] && INSTALL_SYSTEM=1

MISSING=()
ok()   { printf '  [ok]      %s\n' "$*"; }
warn() { printf '  [warn]    %s\n' "$*"; }
bad()  { printf '  [MISSING] %s\n' "$*"; MISSING+=("$1"); }
have() { command -v "$1" >/dev/null 2>&1; }
SUDO=""; if [ "$(id -u)" != 0 ]; then have sudo && sudo -n true 2>/dev/null && SUDO="sudo"; fi
CAN_SYS=0; if [ "$(id -u)" = 0 ] || [ -n "$SUDO" ]; then CAN_SYS=1; fi

sys_install() { # sys_install <apt-package> <brew-package>
  if [ "$INSTALL_SYSTEM" != 1 ]; then return 1; fi
  if have apt-get && [ "$CAN_SYS" = 1 ]; then $SUDO apt-get update -qq && $SUDO apt-get install -y -qq "$1"; return $?; fi
  if have brew; then brew install "$2"; return $?; fi
  return 1
}
hint() { # hint <what> <apt> <brew>
  echo "            fix: sudo apt-get install -y $2   (Debian/Ubuntu)   |   brew install $3   (macOS)   |   or re-run: bash setup.sh --install-system"
}

echo "== Methodical Visual Synthesizer kit: setup =="

echo "-- Node.js (18 or newer)"
node_ok() { have node && [ "$(node -p 'process.versions.node.split(".")[0]')" -ge 18 ]; }
if ! node_ok; then sys_install nodejs node >/dev/null 2>&1 || true; fi
if node_ok; then ok "node $(node -v), npm $(npm -v 2>/dev/null)"; else bad node "Node.js 18+ not found"; echo "            fix: install Node 18+ from https://nodejs.org/ or your package manager (apt-get install -y nodejs npm | brew install node), then re-run"; fi

echo "-- ffmpeg and ffprobe"
if ! have ffmpeg || ! have ffprobe; then sys_install ffmpeg ffmpeg >/dev/null 2>&1 || true; fi
if have ffmpeg && have ffprobe; then ok "$(ffmpeg -version | head -1)"; else bad ffmpeg "ffmpeg/ffprobe not found"; hint ffmpeg ffmpeg ffmpeg; fi

echo "-- npm packages (Remotion and React, from package.json)"
if node_ok && have npm; then
  if npm install --no-audit --no-fund --loglevel=error >/tmp/mvs-npm.log 2>&1; then ok "npm packages installed ($(node -p "require('./node_modules/remotion/package.json').version" 2>/dev/null || echo '?') remotion)"; else bad npm-packages "npm install failed (see /tmp/mvs-npm.log)"; tail -5 /tmp/mvs-npm.log | sed 's/^/            /'; fi
else
  warn "skipped (needs Node)"
fi

echo "-- Headless Chrome for Remotion (downloaded into node_modules, no system install)"
if [ -d node_modules/@remotion/cli ]; then
  if npx --no-install remotion browser ensure >/tmp/mvs-browser.log 2>&1; then ok "browser ready"; else
    bad chromium "Remotion could not get a headless browser (see /tmp/mvs-browser.log)"; tail -5 /tmp/mvs-browser.log | sed 's/^/            /'
    echo "            fix (Linux): the browser needs shared libraries. Try: sudo apt-get install -y libnss3 libdbus-1-3 libatk1.0-0 libgbm-dev libasound2 libxrandr2 libxkbcommon-dev libxfixes3 libxcomposite1 libxdamage1 libatk-bridge2.0-0 libpango-1.0-0 libcairo2 libcups2"
    echo "            or point Remotion at an installed Chrome: export REMOTION_BROWSER_EXECUTABLE=/path/to/chrome"
  fi
else
  warn "skipped (needs the npm packages)"
fi

echo "-- Free narration voice (optional): uv + Phonon"
export HF_HOME="${HF_HOME:-$PWD/.cache/hf}"
if have uvx; then ok "uvx found ($(uvx --version 2>/dev/null))"
elif [ "$WITH_TTS" = 1 ]; then
  echo "  installing uv (user-level, from astral.sh) ..."
  if curl -LsSf https://astral.sh/uv/install.sh | sh >/tmp/mvs-uv.log 2>&1; then export PATH="$HOME/.local/bin:$PATH"; ok "uv installed in ~/.local/bin (add it to PATH for later shells)"; else warn "uv install failed (see /tmp/mvs-uv.log). Narration will be silent; captions still work."; fi
else
  warn "uv not found. Narration will be SILENT (captions still shown). To enable the free voice: bash setup.sh --with-tts"
fi
if have uvx && [ "$WITH_TTS" = 1 ]; then
  mkdir -p work
  if uvx ptts --lang en --quant q8 --voice Harper "Ready." -o work/tts-warm.wav >/tmp/mvs-tts.log 2>&1; then ok "Phonon voice works (model cached in $HF_HOME)"; else warn "Phonon failed (see /tmp/mvs-tts.log). Narration will be silent."; fi
fi

echo
if [ "${#MISSING[@]}" -eq 0 ]; then echo "SETUP OK. Next: bash doctor.sh"; exit 0; fi
echo "SETUP INCOMPLETE. Missing: ${MISSING[*]}"; exit 1
