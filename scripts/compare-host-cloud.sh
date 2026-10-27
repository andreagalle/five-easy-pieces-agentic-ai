#!/usr/bin/env bash
# Run a deterministic example on the host and in a cloud sandbox, and fail unless the two
# results.json files are byte-identical. This is piece 01's claim (the architecture doesn't
# change the program), re-checked by CI after every merge (ADR-0014).
#
#   scripts/compare-host-cloud.sh <example-dir>      (make compare-NN)
#
# Convention for deterministic examples: `python -m agent.run --out DIR` writes DIR/results.json.
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
if [ $# -ne 1 ] || [ ! -d "$1" ]; then
  echo "usage: scripts/compare-host-cloud.sh <example-dir>" >&2
  exit 2
fi
example="$(cd "$1" && pwd)"
python="${PYTHON:-python3}"

host_out="$(mktemp -d)"
trap 'rm -rf "$host_out"' EXIT

(cd "$example" && PYTHONPATH="$root/examples/_shared" "$python" -m agent.run --out "$host_out" >/dev/null)
"$example/run.sh"

host="$(sha256sum "$host_out/results.json" | cut -d' ' -f1)"
cloud="$(sha256sum "$example/out/results.json" | cut -d' ' -f1)"
cloud_python="$("$python" -c 'import json, sys; print(json.load(open(sys.argv[1]))["python"])' "$example/out/RUNINFO.json")"

echo "compare: host  ($("$python" --version 2>&1)) results.json sha256 $host"
echo "compare: cloud ($cloud_python) results.json sha256 $cloud"
if [ "$host" = "$cloud" ]; then
  echo "compare: identical"
else
  echo "compare: DIFFERENT: the sandbox changed what the program does" >&2
  exit 1
fi
