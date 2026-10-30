#!/usr/bin/env bash
# Install the pinned shellcheck and actionlint that `make lint` uses (CLAUDE.md §6).
# Run by scripts/post-create.sh. Without them, the Makefile falls back to the tools' Docker
# images, and a fresh Codespace has no Docker (session 12). The versions match those images.
# Bump them deliberately, with new hashes, and note it in the journal.
set -euo pipefail

SHELLCHECK_VERSION="0.10.0"
ACTIONLINT_VERSION="1.7.12"
dest="/usr/local/bin"

# actionlint's hashes match its release's checksums file. shellcheck publishes none, so its
# hashes are those of the release archives as downloaded on 2026-10-29.
case "$(uname -m)" in
  x86_64)
    sc_arch="x86_64";  sc_sha="6c881ab0698e4e6ea235245f22832860544f17ba386442fe7e9d629f8cbedf87"
    al_arch="amd64";   al_sha="8aca8db96f1b94770f1b0d72b6dddcb1ebb8123cb3712530b08cc387b349a3d8" ;;
  aarch64|arm64)
    sc_arch="aarch64"; sc_sha="324a7e89de8fa2aed0d0c28f3dab59cf84c6d74264022c00c22af665ed1a09bb"
    al_arch="arm64";   al_sha="325e971b6ba9bfa504672e29be93c24981eeb1c07576d730e9f7c8805afff0c6" ;;
  *) echo "install-linters: no pinned build for $(uname -m); make lint will try Docker" >&2; exit 0 ;;
esac

work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT

# fetch <url> <sha256>: download into $work and refuse anything whose hash doesn't match.
fetch() {
  local file
  file="$work/$(basename "$1")"
  curl -fsSL "$1" -o "$file"
  echo "$2  $file" | sha256sum -c --quiet - || { echo "install-linters: checksum mismatch for $1" >&2; exit 1; }
  echo "$file"
}

if command -v shellcheck >/dev/null && shellcheck --version | grep -qx "version: ${SHELLCHECK_VERSION}"; then
  echo "install-linters: shellcheck ${SHELLCHECK_VERSION} already installed"
else
  echo "install-linters: installing shellcheck ${SHELLCHECK_VERSION}"
  archive="$(fetch "https://github.com/koalaman/shellcheck/releases/download/v${SHELLCHECK_VERSION}/shellcheck-v${SHELLCHECK_VERSION}.linux.${sc_arch}.tar.xz" "$sc_sha")"
  tar -xJf "$archive" -C "$work"
  sudo install -m 0755 "$work/shellcheck-v${SHELLCHECK_VERSION}/shellcheck" "$dest/shellcheck"
fi

if command -v actionlint >/dev/null && [ "$(actionlint -version | head -1)" = "${ACTIONLINT_VERSION}" ]; then
  echo "install-linters: actionlint ${ACTIONLINT_VERSION} already installed"
else
  echo "install-linters: installing actionlint ${ACTIONLINT_VERSION}"
  archive="$(fetch "https://github.com/rhysd/actionlint/releases/download/v${ACTIONLINT_VERSION}/actionlint_${ACTIONLINT_VERSION}_linux_${al_arch}.tar.gz" "$al_sha")"
  tar -xzf "$archive" -C "$work" actionlint
  sudo install -m 0755 "$work/actionlint" "$dest/actionlint"
fi
