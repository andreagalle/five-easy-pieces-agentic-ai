#!/usr/bin/env bash
# Install the pinned docker-sbx from Docker's apt repository (CLAUDE.md §6).
# Shared by scripts/post-create.sh (the Codespace) and .github/workflows/sandbox.yml (CI),
# so both run exactly the same sbx. Bump SBX_VERSION deliberately and note it in the journal.
set -euo pipefail

SBX_VERSION="${SBX_VERSION:-0.50.0}"

if command -v sbx >/dev/null && sbx version | grep -q "v${SBX_VERSION} "; then
  echo "install-sbx: sbx v${SBX_VERSION} already installed"
  exit 0
fi

echo "install-sbx: installing docker-sbx ${SBX_VERSION} from Docker's apt repository"
# REPO_ONLY=1: add Docker's apt repository and key, install nothing else.
curl -fsSL https://get.docker.com | sudo REPO_ONLY=1 sh
pkg="$(apt-cache madison docker-sbx | awk -v v="${SBX_VERSION}-" 'index($3, v) == 1 { print $3; exit }')"
if [ -z "$pkg" ]; then
  echo "install-sbx: docker-sbx ${SBX_VERSION} not found in the apt repository" >&2
  exit 1
fi
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y "docker-sbx=${pkg}"
sbx version
