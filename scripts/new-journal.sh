#!/usr/bin/env bash
# Create the skeleton of the next journal entry (CLAUDE.md §9.1) and print its path.
# Usage: scripts/new-journal.sh <slug> ['"01", "03"']
set -euo pipefail

slug="${1:?usage: new-journal.sh <slug> [pieces, e.g. '\"01\", \"03\"']}"
pieces="${2:-}"

root="$(cd "$(dirname "$0")/.." && pwd)"
dir="$root/site/journal"
mkdir -p "$dir"

last="$(grep -h '^session:' "$dir"/*.md 2>/dev/null | tr -dc '0-9\n' | sort -n | tail -1 || true)"
next="$(printf '%02d' $((10#${last:-0} + 1)))"
day="$(date -u +%Y-%m-%d)"
file="$dir/$day-$next-$slug.md"

if [ -e "$file" ]; then
  echo "error: $file already exists" >&2
  exit 1
fi

sbx_version="$(sbx version 2>/dev/null | awk '{print $3}' || true)"

cat > "$file" <<EOF
---
layout: post
title: "Session $next — "
date: $day
session: "$next"
pieces: [$pieces]
sbx_version: "${sbx_version:-unknown}"
model: ""
sandbox_runs: { cloud: 0, local: 0 }
---

## Goal

## What we did

## Commands that mattered

## Decisions

## Dead ends and surprises

## Who did what

## Next
EOF

echo "$file"
