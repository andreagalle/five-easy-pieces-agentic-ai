#!/usr/bin/env bash
# Piece 02 in a cloud sandbox: unit tests, half a sweep, stop, restart, the other half.
# Settings (size, TTL, network) are scripts/sbx-run.sh defaults: 1 vCPU / 2g, 30m, no egress.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
export SBX_AFTER_RESTART="python3 -m agent.run --resume --out out"
exec "$here/../../scripts/sbx-run.sh" "$here" \
  sh -c 'python3 -m unittest discover -s tests -t . && python3 -m agent.run --stop-at 18 --out out'
