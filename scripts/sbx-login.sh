#!/usr/bin/env bash
# Sign sbx in to Docker (CLAUDE.md §5.1, §6).
#
#   scripts/sbx-login.sh        (make login; post-create.sh runs it when both secrets are set)
#
# With the DOCKER_ID and DOCKER_PAT Codespaces secrets set, the sign-in is headless: the token
# reaches sbx on stdin and is never printed or written into the repository (sbx keeps its
# credentials under ~/.config/com.docker.sandboxes). Without them, sbx starts its browser
# flow: open the URL it prints and confirm the one-time code.
set -euo pipefail

die() { echo "sbx-login: $*" >&2; exit 2; }
command -v sbx >/dev/null || die "sbx not found (see scripts/post-create.sh)"

# The same check check-env.sh and sbx-run.sh rely on: the cloud diagnose "Authentication" item.
signed_in() {
  sbx --cloud diagnose --format json 2>/dev/null | python3 -c '
import json, sys
try:
    checks = json.load(sys.stdin)["checks"]
except (ValueError, KeyError):
    sys.exit(1)
sys.exit(0 if any(c.get("name") == "Authentication" and c.get("status") == "pass" for c in checks) else 1)
'
}

if signed_in; then
  echo "sbx-login: already signed in"
  exit 0
fi

if [ -n "${DOCKER_ID:-}" ] && [ -n "${DOCKER_PAT:-}" ]; then
  echo "sbx-login: signing in with the DOCKER_ID and DOCKER_PAT secrets"
  printf '%s\n' "$DOCKER_PAT" | sbx login --username "$DOCKER_ID" --password-stdin
else
  # The browser flow waits for the user, so it needs a terminal (post-create.sh has none).
  [ -t 0 ] || die "DOCKER_ID and DOCKER_PAT aren't set, and the browser sign-in needs a terminal: run 'make login'"
  echo "sbx-login: DOCKER_ID and DOCKER_PAT aren't set; starting the browser sign-in"
  sbx login
fi

signed_in || { echo "sbx-login: still not signed in (run: make check-env)" >&2; exit 1; }
echo "sbx-login: signed in"
