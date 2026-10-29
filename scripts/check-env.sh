#!/usr/bin/env bash
# Read-only report on the development environment (CLAUDE.md §6).
# Changes nothing: no installs, no sign-in, no daemon start, no uploads.
# Secrets are reported as "set" / "not set", never printed.
set -uo pipefail

section() { printf '\n== %s\n' "$1"; }
item() { printf '  %-22s %s\n' "$1" "$2"; }

# Print the checks of an `sbx diagnose --format json` report as one line each.
summarize_diagnose() {
  python3 -c '
import json, sys
try:
    report = json.load(sys.stdin)
except ValueError:
    print("  (could not parse diagnose output)")
    sys.exit(0)
for c in report.get("checks", []):
    print("  {:<6} {:<26} {}".format(c.get("status", "?"), c.get("name", "?"), c.get("message", "")))
'
}

# Status of one named check ("pass", "fail", "skip", ...) in a diagnose report.
diagnose_status() {
  python3 -c '
import json, sys
name = sys.argv[1]
try:
    report = json.load(sys.stdin)
except ValueError:
    print("unknown"); sys.exit(0)
print(next((c.get("status", "unknown") for c in report.get("checks", []) if c.get("name") == name), "unknown"))
' "$1"
}

section "Host"
item "date (UTC)" "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
# shellcheck source=/dev/null  # a system file, not part of the repository
item "os" "$(. /etc/os-release 2>/dev/null && echo "${PRETTY_NAME:-unknown}")"
item "arch" "$(uname -m)"
item "codespace" "$([ -n "${CODESPACES:-}" ] && echo yes || echo no)"

section "Python"
item "python3" "$(python3 --version 2>&1 || echo missing)"
item "python3.12" "$(command -v python3.12 >/dev/null && python3.12 --version 2>&1 || echo missing)"

section "KVM (needed for local sandboxes only)"
if [ -e /dev/kvm ]; then
  item "/dev/kvm" "present ($(stat -c '%A owner=%U group=%G gid=%g' /dev/kvm))"
  if [ -r /dev/kvm ] && [ -w /dev/kvm ]; then
    item "accessible" "yes"
  else
    item "accessible" "no (user $(id -un) is not in the group that owns /dev/kvm)"
  fi
else
  item "/dev/kvm" "absent"
fi

section "Docker Sandboxes (sbx)"
cloud_auth="unknown"
cloud_json=""
if command -v sbx >/dev/null; then
  item "binary" "$(command -v sbx)"
  item "version" "$(sbx version 2>&1 | head -1)"

  local_json="$(timeout 60 sbx diagnose --format json 2>/dev/null)"
  cloud_json="$(timeout 60 sbx --cloud diagnose --format json 2>/dev/null)"
  cloud_auth="$(printf '%s' "$cloud_json" | diagnose_status "Authentication")"
  item "signed in" "$([ "$cloud_auth" = pass ] && echo yes || echo "no ($cloud_auth; run: make login)")"

  printf '\n  sbx diagnose (local):\n'
  printf '%s' "$local_json" | summarize_diagnose
  printf '\n  sbx --cloud diagnose:\n'
  printf '%s' "$cloud_json" | summarize_diagnose
else
  item "binary" "missing (see scripts/post-create.sh)"
fi

section "Secrets present in the environment (values never shown)"
for name in DOCKER_ID DOCKER_PAT OPENROUTER_API_KEY; do
  item "$name" "$([ -n "${!name:-}" ] && echo set || echo "not set")"
done

section "Other tools"
for tool in make node mmdc gh docker; do
  if command -v "$tool" >/dev/null; then
    case "$tool" in
      mmdc) v="$(mmdc --version 2>&1 | head -1)" ;;
      *) v="$("$tool" --version 2>&1 | head -1)" ;;
    esac
    item "$tool" "$v"
  else
    item "$tool" "missing"
  fi
done

section "Summary"
cloud_ready=no
if command -v sbx >/dev/null && [ "$cloud_auth" = pass ] \
  && printf '%s' "$cloud_json" | python3 -c 'import json,sys; sys.exit(json.load(sys.stdin)["summary"]["fail"] != 0)' 2>/dev/null; then
  cloud_ready=yes
fi
local_ready=no
if command -v sbx >/dev/null && [ "$cloud_auth" = pass ] && [ -r /dev/kvm ] && [ -w /dev/kvm ]; then
  local_ready=yes
fi
item "Tier C (cloud) ready" "$cloud_ready"
item "Tier L (local) ready" "$local_ready (not published until tested on a capable machine: ADR-0010)"
exit 0
