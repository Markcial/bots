#!/usr/bin/env bash
# Superconnected Research Entity kit: set up the light harness. Safe to run again (idempotent).
#   bash setup.sh                  check the tools, create the folders
#   bash setup.sh --install-system also install missing curl/git/jq/python3 with the system package manager (apt/brew)
# Needs no account, card, or API key. Prints what is missing and the exact command to fix it.
set -u
cd "$(dirname "$0")"
INSTALL_SYSTEM=0
for a in "$@"; do case "$a" in --install-system) INSTALL_SYSTEM=1;; *) echo "unknown option: $a"; exit 2;; esac; done
[ "${SRE_ALLOW_SYSTEM_INSTALL:-0}" = 1 ] && INSTALL_SYSTEM=1
have() { command -v "$1" >/dev/null 2>&1; }
SUDO=""; if [ "$(id -u)" != 0 ]; then have sudo && sudo -n true 2>/dev/null && SUDO="sudo"; fi
MISSING=()
ok()   { printf '  [ok]       %s\n' "$*"; }
warn() { printf '  [optional] %s\n' "$*"; }
bad()  { printf '  [MISSING]  %s\n' "$1"; MISSING+=("$1"); }
try_install() { # try_install <apt> <brew>
  [ "$INSTALL_SYSTEM" = 1 ] || return 1
  if have apt-get && { [ "$(id -u)" = 0 ] || [ -n "$SUDO" ]; }; then $SUDO apt-get update -qq && $SUDO apt-get install -y -qq "$1"; return $?; fi
  if have brew; then brew install "$2"; return $?; fi
  return 1
}

echo "== Superconnected Research Entity kit: setup =="
echo "-- required"
for pair in "curl:curl:curl" "git:git:git"; do
  IFS=: read -r tool apt brew <<<"$pair"
  have "$tool" || try_install "$apt" "$brew" >/dev/null 2>&1 || true
  if have "$tool"; then ok "$tool $("$tool" --version 2>&1 | head -1 | cut -c1-48)"; else bad "$tool"; echo "             fix: sudo apt-get install -y $apt  |  brew install $brew  |  or: bash setup.sh --install-system"; fi
done
echo "-- optional (used by some experiments; not needed for reports or link checks)"
for t in python3 node jq; do if have "$t"; then ok "$t $("$t" --version 2>&1 | head -1 | cut -c1-48)"; else warn "$t not found. Install it only if an experiment needs it."; fi; done

echo "-- folders"
mkdir -p reports experiments work && ok "reports/  experiments/  work/ (scratch)"
chmod +x scripts/*.sh experiments/_template/run.sh 2>/dev/null

echo
if [ "${#MISSING[@]}" -eq 0 ]; then echo "SETUP OK. Next: bash doctor.sh"; exit 0; fi
echo "SETUP INCOMPLETE. Missing: ${MISSING[*]}"; exit 1
