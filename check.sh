#!/usr/bin/env bash
# Re-runs every check over the recorded runs of both rounds and fails if any number differs from
# the committed results.json. The agents don't run again here: what this checks is that the
# numbers in the README come out of the code in this repo.
set -euo pipefail
cd "$(dirname "$0")"
export TSC="${TSC:-tsc}"

for round in results/round1 results/round2; do
  echo "== $round"
  python3 run/score.py "$round"
  echo
done

# If anything differs, the diff shows which run and which field.
git diff --exit-code -- results/*/results.json
echo "OK: both rounds reproduce."
