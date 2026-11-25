#!/usr/bin/env bash

set -euo pipefail

todos_dir="${1:-.claude/todos}"

if [ ! -d "$todos_dir" ]; then
  echo "(no stashed tasks)"
  exit 0
fi

shopt -s nullglob
files=("$todos_dir"/*.md)

if [ ${#files[@]} -eq 0 ]; then
  echo "(no stashed tasks)"
  exit 0
fi

extract_row() {
  local f="$1" slug
  slug="$(basename "$f" .md)"
  awk -v slug="$slug" '
    /^---[[:space:]]*$/ { c++; if (c == 2) exit; next }
    c == 1 {
      if (sub(/^task:[[:space:]]*/, ""))             task = $0
      else if (sub(/^title:[[:space:]]*/, ""))       title = $0
      else if (sub(/^status:[[:space:]]*/, ""))      status = $0
      else if (sub(/^stashed_at:[[:space:]]*/, ""))  stashed_at = $0
    }
    END {
      if (task == "")        task = (title != "" ? title : "-")
      if (status == "")      status = "-"
      if (stashed_at == "")  stashed_at = "-"
      printf "%s\t%s\t%s\t%s\n", stashed_at, slug, status, task
    }
  ' "$f"
}

rows=()
while IFS= read -r line; do
  rows+=("$line")
done < <(
  for f in "${files[@]}"; do
    extract_row "$f"
  done | awk -F'\t' '$3 != "popped" && $3 != "dropped"' | sort -r
)

if [ ${#rows[@]} -eq 0 ]; then
  echo "(no stashed tasks)"
  exit 0
fi

{
  printf 'STASHED_AT\tSLUG\tSTATUS\tTASK\n'
  for r in "${rows[@]}"; do
    printf '%s\n' "$r"
  done
} | column -t -s "$(printf '\t')"
