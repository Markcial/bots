#!/usr/bin/env bash
# Superconnected Research Entity kit: self-check. Scaffolds a test experiment and a test report, and runs the link checker against
# one URL that must open and one that must be reported broken.  bash doctor.sh
set -u
cd "$(dirname "$0")"
mkdir -p work reports experiments
REPORT=work/doctor-report.txt; : > "$REPORT"
FAIL=0
say()  { echo "$*" | tee -a "$REPORT"; }
pass() { say "  PASS  $*"; }
fail() { say "  FAIL  $*"; FAIL=1; }
warn() { say "  WARN  $*"; }
now()  { date +%s.%N; }
secs() { awk -v a="$1" -v b="$(now)" 'BEGIN{printf "%.1f", b-a}'; }
say "== Superconnected Research Entity kit: doctor ($(date '+%Y-%m-%d %H:%M %Z')) =="

say "-- tools"
for t in curl git; do command -v "$t" >/dev/null 2>&1 && pass "$t found" || fail "$t missing (bash setup.sh)"; done
[ "$FAIL" = 1 ] && { say "DOCTOR FAIL: fix the tools first."; exit 1; }

say "-- experiment scaffold"
T=$(now); TMP=$(mktemp -d)
E=$(bash scripts/new-experiment.sh doctor-check --dir="$TMP" 2>&1 | tail -1)
if [ -f "$E/experiment.md" ] && [ -f "$E/environment.txt" ] && [ -d "$E/results" ]; then
  # the stub run.sh must run and write a results file
  ( cd "$E" && bash run.sh 1 >/dev/null 2>&1 )
  if [ -s "$E/results/run-1.txt" ] && grep -q "^## Question\|^## Hypothesis" "$E/experiment.md"; then pass "scaffold and run.sh work in $(secs "$T") s (sample: $E)"; else fail "scaffold exists but run.sh wrote no results"; fi
else fail "new-experiment.sh did not create the expected files: $E"; fi

say "-- report template"
if bash scripts/new-report.sh doctor-check >/dev/null 2>&1; then
  RF="reports/$(date +%Y-%m-%d)-doctor-check.md"
  for h in "## Conclusion" "## Evidence" "## Opinion" "## Options and tradeoffs" "## Costs" "## Could not verify" "## Next step"; do grep -q "^$h" "$RF" || { fail "report template lacks '$h'"; break; }; done
  [ "$FAIL" = 0 ] && pass "report template has all sections of the report-findings skill ($RF)"
  rm -f "$RF"
else fail "new-report.sh failed"; fi

say "-- link checker (needs internet)"
T=$(now)
printf 'Good: [Example Domain](https://example.com).\nBad: [Missing](https://example.com/mvs-doctor-404).\n' > work/doctor-links.md
OUT=$(bash scripts/linkcheck.sh work/doctor-links.md --timeout=10 2>&1); RC=$?
if echo "$OUT" | grep -qE "BROKEN +(000|-)" || { ! echo "$OUT" | grep -q " 200 " && ! echo "$OUT" | grep -q "BROKEN +404"; }; then
  warn "no internet or the test site is unreachable, so the link checker could not be verified: $(echo "$OUT" | tail -1)"
elif echo "$OUT" | grep -qE "^OK +200 +https://example.com$" && echo "$OUT" | grep -qE "^BROKEN +404 +https://example.com/mvs-doctor-404$" && [ "$RC" = 1 ]; then
  pass "link checker found 1 ok and 1 broken (404) and exited 1, as it should, in $(secs "$T") s"
else fail "link checker gave unexpected results (exit $RC):"; echo "$OUT" | tee -a "$REPORT"; fi

rm -rf "$TMP"
say
if [ "$FAIL" = 0 ]; then say "DOCTOR PASS"; exit 0; else say "DOCTOR FAIL (details above)"; exit 1; fi
