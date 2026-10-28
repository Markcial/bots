#!/usr/bin/env bash
# Start a report from the template: bash scripts/new-report.sh <slug>   ->  reports/<YYYY-MM-DD>-<slug>.md
set -eu
cd "$(dirname "$0")/.."
SLUG="${1:-}"; [ -n "$SLUG" ] || { echo "usage: bash scripts/new-report.sh <slug>"; exit 2; }
SLUG=$(echo "$SLUG" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/-/g; s/^-|-$//g')
F="reports/$(date +%Y-%m-%d)-$SLUG.md"
mkdir -p reports
[ ! -e "$F" ] || { echo "already exists: $F"; exit 1; }
sed "s|<YYYY-MM-DD>|$(date +%Y-%m-%d)|" templates/report.md > "$F"
echo "$F"
