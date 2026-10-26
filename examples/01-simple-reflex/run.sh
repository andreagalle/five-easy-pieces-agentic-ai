#!/usr/bin/env bash
# Piece 01 in a cloud sandbox: unit tests first, then the scenarios.
# Settings (size, TTL, network) are scripts/sbx-run.sh defaults: 1 vCPU / 2g, 30m, no egress.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
exec "$here/../../scripts/sbx-run.sh" "$here" \
  sh -c 'python3 -m unittest discover -s tests -t . && python3 -m agent.run --out out'
