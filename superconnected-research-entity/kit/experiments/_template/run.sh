#!/usr/bin/env bash
# Put the exact commands of this experiment here. Run it with: bash run.sh [run-number]
# Output of each run is saved in results/run-<n>.txt, with the start and end time and the exit code.
set -u
cd "$(dirname "$0")"
N="${1:-1}"
mkdir -p results scratch
{
  echo "# run $N started $(date -Is)"
  # ---- replace this block with the commands under test, working inside ./scratch ----
  echo "TODO: add the commands under test"
  # -----------------------------------------------------------------------------------
  echo "# exit code $? at $(date -Is)"
} 2>&1 | tee "results/run-$N.txt"
