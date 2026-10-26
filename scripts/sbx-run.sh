#!/usr/bin/env bash
# Run one example in a disposable Docker Sandbox (CLAUDE.md §5.3, ADR-0001, ADR-0010).
#
#   scripts/sbx-run.sh <example-dir> <command> [args...]
#
# Copies examples/_shared and the example into a fresh sandbox, runs the command in the
# example's directory, copies <example>/out back, writes out/RUNINFO.json, and removes
# the sandbox on exit, whatever happened.
#
# Environment:
#   SBX_TARGET   cloud (default) | local (refused until the local tier is tested: ADR-0010)
#   SBX_CPUS     vCPUs (default 1)     } together they must name a billable cloud shape:
#   SBX_MEMORY   memory (default 2g)   } 1/2g micro, 2/4g small, 4/8g medium, 8/16g large
#   SBX_TTL      time to live (default 30m); the sandbox is deleted when it lapses
#   SBX_NETWORK  deny-all (default) | open
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
die() { echo "sbx-run: $*" >&2; exit 2; }

[ $# -ge 2 ] || die "usage: scripts/sbx-run.sh <example-dir> <command> [args...]"
[ -d "$1" ] || die "no such example directory: $1"
example="$(cd "$1" && pwd)"
shift
example_name="$(basename "$example")"
piece="${example_name%%-*}"

target="${SBX_TARGET:-cloud}"
cpus="${SBX_CPUS:-1}"
memory="${SBX_MEMORY:-2g}"
ttl="${SBX_TTL:-30m}"
network="${SBX_NETWORK:-deny-all}"
agent="shell"
workspace="/home/agent/workspace"
dest="$workspace/fep"

case "$target" in
  cloud) ;;
  local) die "SBX_TARGET=local isn't available yet: the local tier is published once it has been tested (ADR-0010)" ;;
  *) die "SBX_TARGET must be 'cloud' or 'local', not '$target'" ;;
esac
case "$network" in
  deny-all) network_flags=(--deny-network '**') ;;
  open) network_flags=() ;;
  *) die "SBX_NETWORK must be 'deny-all' or 'open', not '$network'" ;;
esac

# Preflight: sbx installed, signed in, cloud API reachable and entitled.
command -v sbx >/dev/null || die "sbx not found (see scripts/post-create.sh)"
sbx --cloud diagnose --format json 2>/dev/null | python3 -c '
import json, sys
try:
    checks = json.load(sys.stdin)["checks"]
except (ValueError, KeyError):
    sys.exit("sbx-run: could not read sbx --cloud diagnose")
failed = [c for c in checks if c.get("status") == "fail"]
for c in failed:
    print("sbx-run: cloud check failed: {}: {} {}".format(c["name"], c.get("message", ""), c.get("hint", "")), file=sys.stderr)
sys.exit(1 if failed else 0)
' || die "cloud sandboxes aren't ready (run: make check-env)"

commit="$(git -C "$root" rev-parse HEAD)"
dirty=false
[ -z "$(git -C "$root" status --porcelain -- examples scripts)" ] || dirty=true
name="fep-${piece}-$(git -C "$root" rev-parse --short HEAD)"

stage="$(mktemp -d)"
created=0
cleanup() {
  if [ "$created" = 1 ]; then
    sbx --cloud rm --force "$name" >/dev/null 2>&1 \
      && echo "sbx-run: removed $name" \
      || echo "sbx-run: WARNING: could not remove $name; check 'sbx --cloud ls'" >&2
  fi
  rm -rf "$stage"
}
trap cleanup EXIT

# Stage what the sandbox gets: the shared world and this example, without outputs or caches.
mkdir -p "$stage/fep"
tar -C "$root/examples" --exclude=out --exclude=__pycache__ -cf - _shared "$example_name" | tar -C "$stage/fep" -xf -

started="$(date +%s)"
echo "sbx-run: creating $name (cloud, ${cpus} vCPU / ${memory}, ttl ${ttl}, network ${network})"
sbx --cloud create --name "$name" --ttl "$ttl" --on-timeout delete \
  --cpus "$cpus" --memory "$memory" "${network_flags[@]}" --no-progress "$agent"
created=1

sbx --cloud inspect --format json "$name" > "$stage/inspect.json"
sbx --cloud cp "$stage/fep" "$name:$dest"
python_version="$(sbx --cloud exec "$name" python3 --version 2>&1 || echo "python3 not found")"
echo "sbx-run: running in $name ($python_version): $*"

set +e
sbx --cloud exec -w "$dest/$example_name" -e "PYTHONPATH=$dest/_shared" "$name" "$@" 2>&1 | tee "$stage/stdout.txt"
exit_code="${PIPESTATUS[0]}"
set -e

rm -rf "$example/out"
sbx --cloud cp "$name:$dest/$example_name/out" "$example/out" || mkdir -p "$example/out"
cp "$stage/stdout.txt" "$example/out/stdout.txt"
duration=$(( $(date +%s) - started ))

# RUNINFO.json: what ran, where, on which versions, and how it ended (CLAUDE.md §5.3).
RUNINFO_PATH="$example/out/RUNINFO.json" INSPECT_PATH="$stage/inspect.json" \
TARGET="$target" SBX_VERSION="$(sbx version | awk '{print $3}')" AGENT="$agent" \
CPUS="$cpus" MEMORY="$memory" TTL="$ttl" NETWORK="$network" NAME="$name" \
PYTHON_VERSION="$python_version" COMMIT="$commit" DIRTY="$dirty" \
EXIT_CODE="$exit_code" DURATION="$duration" python3 - "$@" <<'EOF'
import datetime, json, os, sys
env = os.environ
with open(env["INSPECT_PATH"]) as f:
    inspect = json.load(f)
info = {
    "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "tier": env["TARGET"],
    "sbx_version": env["SBX_VERSION"],
    "agent": env["AGENT"],
    "template_image": inspect.get("image"),
    "size": {"cpus": int(env["CPUS"]), "memory": env["MEMORY"]},
    "ttl": env["TTL"],
    "on_timeout": inspect.get("on_timeout"),
    "network": env["NETWORK"],
    "sandbox_name": env["NAME"],
    "python": env["PYTHON_VERSION"],
    "git_commit": env["COMMIT"],
    "git_dirty": env["DIRTY"] == "true",
    "command": sys.argv[1:],
    "exit_code": int(env["EXIT_CODE"]),
    "duration_seconds": int(env["DURATION"]),
}
with open(env["RUNINFO_PATH"], "w") as f:
    json.dump(info, f, indent=2)
    f.write("\n")
EOF
echo "sbx-run: exit code $exit_code, ${duration}s; outputs in ${example#$root/}/out/"
exit "$exit_code"
