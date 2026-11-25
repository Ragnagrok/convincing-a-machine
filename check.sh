#!/usr/bin/env bash
# Re-runs every check over the recorded runs of both rounds and fails if any number differs from
# the committed results.json. The agents don't run again here: what this checks is that the
# numbers in the README come out of the code in this repo.
set -euo pipefail
cd "$(dirname "$0")"
export TSC="${TSC:-tsc}"

# Without tsc, every run of the types task would score as failed. Stop before scoring anything.
if ! "$TSC" --version >/dev/null 2>&1; then
  echo "check.sh needs tsc (TypeScript 7) on the path, or its path in \$TSC; '$TSC' doesn't run." >&2
  exit 1
fi

# Score a copy of each round, so that a bad run never overwrites the committed results.json.
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT

status=0
for round in round1 round2; do
  echo "== results/$round"
  cp -r "results/$round" "$work/$round"
  rm -f "$work/$round/results.json"
  python3 run/score.py "$work/$round"
  echo
  # If anything differs, the diff shows which run and which field.
  diff -u "results/$round/results.json" "$work/$round/results.json" || status=1
done

[ "$status" -eq 0 ] || { echo "FAIL: the scores differ from the committed results.json." >&2; exit 1; }
echo "OK: both rounds reproduce."
