#!/usr/bin/env bash
# Check that every URL in a report opens. Public pages only, read-only (HEAD, then GET if the server refuses HEAD).
#   bash scripts/linkcheck.sh <report.md> [--strict] [--timeout=15]
# Result per URL:
#   OK       2xx or 3xx that ends in 2xx
#   BROKEN   404, 410, other 4xx/5xx except the blocked codes below, DNS failure, timeout, or connection error  -> fails the check
#   BLOCKED  401, 403, 429 (the site refuses automated requests; open it by hand)  -> warning, fails only with --strict
#   SKIPPED  localhost or private-network URLs (127.0.0.1, 192.168.x.x, *.local, ...). They are not public sources.
# Known limit: a URL that itself contains parentheses (some Wikipedia links) is cut at the first one; check those by hand.
# Exit code 0 when nothing is BROKEN (and nothing BLOCKED with --strict), else 1. The last line is a one-line summary to paste into the report.
set -u
FILE="${1:-}"; [ -n "$FILE" ] && [ -f "$FILE" ] || { echo "usage: bash scripts/linkcheck.sh <report.md> [--strict] [--timeout=15]"; exit 2; }
STRICT=0; TO=15
for a in "$@"; do case "$a" in --strict) STRICT=1;; --timeout=*) TO="${a#--timeout=}";; esac; done
command -v curl >/dev/null 2>&1 || { echo "curl is required"; exit 2; }

# Extract http(s) URLs, strip trailing punctuation and markdown/HTML closers, de-duplicate.
mapfile -t URLS < <(grep -oE "https?://[^][()<>\"' ]+" "$FILE" | sed -E 's/[.,;:!?*_`]+$//' | awk '!seen[$0]++')
[ "${#URLS[@]}" -gt 0 ] || { echo "no URLs found in $FILE"; echo "LINKCHECK: 0 URLs (a report with factual claims should have sources)"; exit 0; }

OK=0; BROKEN=0; BLOCKED=0; SKIPPED=0
printf '%-8s %-5s %s\n' RESULT CODE URL
for u in "${URLS[@]}"; do
  host=$(echo "$u" | sed -E 's|^https?://([^/:?#]+).*|\1|')
  if echo "$host" | grep -qiE '^(localhost|127\.|10\.|192\.168\.|172\.(1[6-9]|2[0-9]|3[01])\.|0\.0\.0\.0)|\.(local|internal)$'; then
    printf '%-8s %-5s %s\n' SKIPPED - "$u"; SKIPPED=$((SKIPPED+1)); continue
  fi
  code=$(curl -sS -o /dev/null -I -L -m "$TO" -A "Mozilla/5.0 (linkcheck)" -w '%{http_code}' "$u" 2>/dev/null) || code=000
  if [ "$code" = 000 ] || [ "$code" -ge 400 ] 2>/dev/null; then   # some servers refuse HEAD: retry with GET
    code=$(curl -sS -o /dev/null -L -m "$TO" -A "Mozilla/5.0 (linkcheck)" -w '%{http_code}' "$u" 2>/dev/null) || code=000
  fi
  case "$code" in
    2*|3*) printf '%-8s %-5s %s\n' OK "$code" "$u"; OK=$((OK+1)) ;;
    401|403|429) printf '%-8s %-5s %s\n' BLOCKED "$code" "$u"; BLOCKED=$((BLOCKED+1)) ;;
    *) printf '%-8s %-5s %s\n' BROKEN "$code" "$u"; BROKEN=$((BROKEN+1)) ;;
  esac
done
echo
SUMMARY="LINKCHECK $(date +%Y-%m-%d): ${#URLS[@]} URLs, $OK ok, $BROKEN broken, $BLOCKED blocked (open by hand), $SKIPPED skipped"
echo "$SUMMARY"
[ "$BROKEN" -eq 0 ] && { [ "$STRICT" -eq 0 ] || [ "$BLOCKED" -eq 0 ]; }
