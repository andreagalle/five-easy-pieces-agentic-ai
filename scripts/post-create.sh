#!/usr/bin/env bash
# Devcontainer postCreateCommand (CLAUDE.md §6).
# Installs the pinned sbx and mermaid-cli, then prints the read-only environment report.
# Claude Code itself comes from the devcontainer feature, not from this script.
set -euo pipefail

# Bump these deliberately and record the bump in the journal.
SBX_VERSION="${SBX_VERSION:-0.50.0}"
MERMAID_CLI_VERSION="${MERMAID_CLI_VERSION:-12.0.0}"

here="$(cd "$(dirname "$0")" && pwd)"

if ! command -v sbx >/dev/null || ! sbx version | grep -q "v${SBX_VERSION} "; then
  echo "Installing docker-sbx ${SBX_VERSION} from Docker's apt repository"
  # REPO_ONLY=1: add Docker's apt repository and key, install nothing else.
  curl -fsSL https://get.docker.com | sudo REPO_ONLY=1 sh
  pkg="$(apt-cache madison docker-sbx | awk -v v="${SBX_VERSION}-" 'index($3, v) == 1 { print $3; exit }')"
  if [ -z "$pkg" ]; then
    echo "error: docker-sbx ${SBX_VERSION} not found in the apt repository" >&2
    exit 1
  fi
  sudo DEBIAN_FRONTEND=noninteractive apt-get install -y "docker-sbx=${pkg}"
fi

if ! command -v mmdc >/dev/null || [ "$(mmdc --version 2>/dev/null)" != "$MERMAID_CLI_VERSION" ]; then
  echo "Installing @mermaid-js/mermaid-cli ${MERMAID_CLI_VERSION}"
  npm install -g "@mermaid-js/mermaid-cli@${MERMAID_CLI_VERSION}"
fi

# Shared libraries of the headless Chrome that mermaid-cli drives. List derived on
# 2026-10-26 from `ldd chrome-headless-shell` (mermaid-cli 12.0.0, Ubuntu 24.04);
# the first one was the only library missing from the default Codespace image.
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
  libasound2t64 libatk-bridge2.0-0t64 libatk1.0-0t64 libdbus-1-3 libdrm2 libgbm1 \
  libglib2.0-0t64 libnspr4 libnss3 libx11-6 libxcb1 libxcomposite1 libxdamage1 \
  libxext6 libxfixes3 libxkbcommon0 libxrandr2 fonts-liberation

# ImageMagick: scripts/gen-header.py turns each kept 7 MB PNG header into a ~1.2 MB JPEG.
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends imagemagick

"$here/check-env.sh"
