# sbx notes

Working notes on Docker Sandboxes and the `sbx` CLI. Started from CLAUDE.md §5.1 (checked 2026-10-21, sbx v0.49.2 era) and re-verified below. Anything a script or article relies on must appear in the "Verified" section with the version it was checked against (protocol: CLAUDE.md §5.5).

## Version log

| Date | Version | Source | Notes |
|------|---------|--------|-------|
| 2026-10-26 | v0.50.0 (`30d023cb`) | `docker-sbx` 0.50.0-1~ubuntu.24.04~noble from Docker's apt repo | Released the same day (2026-10-26 14:44 UTC). Previous: v0.49.2 (2026-10-21). |

## Verified with sbx v0.50.0 (2026-10-26)

Checked with `sbx <command> --help` in the Codespace, cross-checked with the docs and the v0.50.0 release notes.

### Install (Ubuntu 24.04)

- Docs page: <https://docs.docker.com/ai/sandboxes/install/> (raw: `/ai/sandboxes/install.md`).
- `curl -fsSL https://get.docker.com | sudo REPO_ONLY=1 sh` then `sudo apt install docker-sbx`. With `REPO_ONLY=1` the script installs `ca-certificates` and `curl`, adds Docker's key and apt source, and exits. It doesn't install Docker Engine.
- Local sandboxes need KVM and the user in the `kvm` group. The docs say: `sudo usermod -aG kvm $USER`, then sign out and back in, or run `newgrp kvm`.

### Commands and flags the wrapper will need

- **Agents** (`sbx create --help`): claude, codex, copilot, cursor, devin, docker-agent, droid, gemini, kiro, opencode, shell.
- **`shell` is accepted with `--cloud`.** It is listed under `sbx --cloud create --help` → Available Commands. (Open question in CLAUDE.md §5.3, now answered.)
- **`sbx create AGENT [PATH...]`**: omitting PATH creates a sandbox *without* a workspace bind mount (what the copy-in/copy-out design wants locally).
- **Cloud sizing**: `--cpus` and `--memory` must name a billable shape: micro (1 vCPU / 2048 MiB), small (2 / 4096), medium (4 / 8192), large (8 / 16384), xl (16 / 32768). Default 2 / 4 GiB.
- **Local sizing defaults differ**: `--cpus 0` means all host CPUs; memory defaults to 50% of host memory (512 MiB–32 GiB). For local-vs-cloud comparisons, pass sizes explicitly.
- **`--ttl`** (cloud only), e.g. `30m`, `2h`, `1h30m`. **`--on-timeout stop|restart|delete`**. If omitted, the server stops the sandbox when it can be restarted and deletes it otherwise. `restart` needs `--ttl` ≥ 1h.
- **`sbx --cloud ttl [+DURATION] SANDBOX`**: shows or extends the TTL. It can't shorten it, and there's a hard ceiling 24 h after creation.
- **Cloud names**: at least 2 characters, letters, digits and hyphens only (no periods); `default` is reserved.
- **`sbx --cloud run`** refuses non-interactive use without `--detach`. Scripts use `create` (or `run -d`) and then `exec`.
- **`sbx exec [flags] SANDBOX COMMAND [ARG...]`**: starts a stopped sandbox first. `-w/--workdir`, `-e/--env`, `-i`, `-t`. With `--cloud`, the flags `-d`, `--user` and `--privileged` are rejected. Exit status is the command's. It's 125 when sbx couldn't run the command (e.g. no such sandbox) and 127 when the command is missing (a cloud backend may report 125 instead).
- **`sbx cp SRC DST`**: one side is `SANDBOX:PATH` (absolute path). Copying a directory places the directory itself at the destination. If DST exists as a directory, the source goes inside it. Copying from one sandbox to another isn't supported. With `--cloud`, transfers go through the cloud file API.
- **`sbx rm --force SANDBOX...`**: `--force` skips confirmation (needed in scripts). With `--cloud`, `--all` is deliberately disabled, so pass IDs or names explicitly. Cloud `rm` waits up to 60 s per sandbox and may exit 0 while deletion is still completing, so verify with `sbx --cloud ls`.
- **Network at creation**: local `--deny-network HOST` (narrows only). Cloud `--allow-network PATTERN` / `--deny-network PATTERN`. Account defaults with `sbx --cloud policy init <allow-all|balanced|deny-all>`.
- **`sbx inspect SANDBOX [--format json]`** (new in v0.50.0): with `--cloud` it reports template, sizing, timeout behaviour and port URLs. That's useful for `RUNINFO.json`.
- **`sbx diagnose --format json`** and **`sbx --cloud diagnose --format json`**: machine-readable checks, used by `scripts/check-env.sh`. Never use `--upload`, which sends the report to Docker support.

### Discrepancies (trust `--help`, per CLAUDE.md §5.5)

- `sbx --cloud inspect` is announced in the v0.50.0 release notes and works (`sbx --cloud inspect --help`), but it isn't listed in `sbx --help` or `sbx --cloud --help`.
- The docs link the install page as `/ai/sandboxes/get-started/install/`. Its raw Markdown is served at `/ai/sandboxes/install.md`, and the "append `.md`" rule gives a 404 for the linked path.
- The CLI's own help text for `--cloud` says "Docker Cloud Sandboxes API". In articles, still write "cloud sandboxes (`sbx --cloud`)" and never "Docker Cloud" (CLAUDE.md §5.1).

## Codespace facts (2026-10-26)

- `/dev/kvm` is present (`crw-rw----`, owner root, GID 109, which has no name in `/etc/group`). The `codespace` user isn't in that group, so `sbx diagnose` reports *Virtualization — not accessible*. Not worked around (CLAUDE.md §5.2). See ADR-0001 and the session 01 journal.
- Default `python3` in the current Codespace image is 3.14.2. `python3.12` (3.12.3) is also present and is what `make test` uses. The devcontainer pins 3.12.

## Still to verify (before the wrapper or any article relies on it)

- `sbx login --username … --password-stdin` (headless sign-in) and where credentials land on Linux without a keyring.
- `sbx secret`, `sbx policy` (local and cloud) and `sbx template save`.
- Whether the `shell` template has `python3`, and which version, locally and in the cloud.
- `sbx stop` / resume semantics (piece 02) and `sbx move`.
- Cloud network policy defaults for a new account.
