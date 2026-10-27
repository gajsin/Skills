#!/usr/bin/env bash
# Interactive last resort for a bug that cannot yet be reproduced automatically.
# Usage: bash hitl-loop.template.sh '<reproduction steps>' '<exact symptom>'
set -euo pipefail

if (( $# != 2 )) || [[ -z "$1" || -z "$2" ]]; then
  printf 'Usage: %s <reproduction steps> <exact symptom>\n' "$0" >&2
  exit 2
fi

printf 'Steps: %s\n' "$1"
if ! read -r -p 'Press Enter after completing the steps: ' _; then
  printf 'No verdict recorded.\n' >&2
  exit 2
fi
if ! read -r -p "Did $2 occur? (y/n): " answer; then
  printf 'No verdict recorded.\n' >&2
  exit 2
fi

case "$answer" in
  y|Y) printf 'SYMPTOM_OBSERVED=true (human report)\n'; exit 1 ;;
  n|N) printf 'SYMPTOM_OBSERVED=false (human report)\n'; exit 0 ;;
  *) printf 'Enter y or n; no verdict recorded.\n' >&2; exit 2 ;;
esac
