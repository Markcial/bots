#!/usr/bin/env bash
# Scaffold a new experiment folder from the template.
#   bash scripts/new-experiment.sh <slug> [--dir=experiments]
# Creates experiments/<YYYY-MM-DD>-<slug>/ with experiment.md, run.sh, results/, scratch/ and environment.txt (OS and tool versions).
set -eu
cd "$(dirname "$0")/.."
SLUG="${1:-}"; [ -n "$SLUG" ] || { echo "usage: bash scripts/new-experiment.sh <slug> [--dir=experiments]"; exit 2; }
DIR=experiments; for a in "$@"; do case "$a" in --dir=*) DIR="${a#--dir=}";; esac; done
SLUG=$(echo "$SLUG" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/-/g; s/^-|-$//g')
D="$DIR/$(date +%Y-%m-%d)-$SLUG"
[ ! -e "$D" ] || { echo "already exists: $D"; exit 1; }
mkdir -p "$D/results" "$D/scratch"
cp experiments/_template/experiment.md experiments/_template/run.sh "$D/"
sed -i "s|<YYYY-MM-DD>|$(date +%Y-%m-%d)|; s|experiments/<date>-<slug>/|$D/|" "$D/experiment.md"
{
  echo "date: $(date -Is)"
  echo "os: $(uname -srm)"
  for t in node npm python3 git curl ffmpeg uv; do command -v "$t" >/dev/null 2>&1 && echo "$t: $("$t" --version 2>&1 | head -1)"; done
} > "$D/environment.txt"
echo "$D"
