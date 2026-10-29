# sbx notes

Working notes on Docker Sandboxes and the `sbx` CLI. Started from CLAUDE.md §5.1 (checked 2026-10-21, sbx v0.49.2 era) and re-verified below. Anything a script or article relies on must appear in the "Verified" section with the version it was checked against (protocol: CLAUDE.md §5.5).

## Version log

| Date | Version | Source | Notes |
|------|---------|--------|-------|
| 2026-10-26 | v0.50.0 (`30d023cb`) | `docker-sbx` 0.50.0-1~ubuntu.24.04~noble from Docker's apt repo | Released the same day (2026-10-26 14:44 UTC). Previous: v0.49.2 (2026-10-21). |
| 2026-10-29 | v0.50.1 seen, not installed | `sbx diagnose`: "update available"; release notes | Released 2026-10-28. One line of notes: "fixes an issue that prevented sandboxes from starting". No flag changes, so the series stays pinned at v0.50.0, which every run used. Re-verified on v0.50.0 in session 10 (`/verify-sbx`). |

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

## Cloud sandbox facts, from a probe and two runs (2026-10-26, sbx v0.50.0)

- **`shell` in the cloud:** image `docker/sandbox-templates:shell-docker`, Ubuntu 26.04.1 LTS, x86_64, user `agent`, `HOME=/home/agent`, working directory `/home/agent/workspace` (empty at creation).
- **Python:** `/usr/bin/python3` is **3.14.4**. No install is needed for stdlib-only code. The host uses 3.12, so example output must not depend on the Python version (checked: byte-identical results on 3.12.3, 3.14.2 and 3.14.4).
- **Timing (micro shape):** `create` ≈5 s, and a full run of example 01 (create, cp in, tests, run, cp out) takes 10–17 s.
- **`sbx --cloud cp DIR sbx:/abs/path`:** when the destination is missing, it's created as a copy of DIR. Copying out works the same way.
- **`--deny-network '**'` at creation:** an HTTPS request from inside fails at DNS resolution ("Temporary failure in name resolution"). Nothing leaves the sandbox.
- **`sbx --cloud exec -w DIR -e K=V`:** both work, and the command's exit status is passed through (tested with 3).
- **`sbx --cloud inspect --format json`:** fields `id`, `name`, `agent`, `state`, `image`, `cpus`, `memory_mib`, `on_timeout`, `auto_resume`, `age`, `created_at`, `expires_at`. There's no image digest, so `RUNINFO.json` records the tag only.
- **Headless sign-in** (`printf '%s\n' "$DOCKER_PAT" | sbx login --username "$DOCKER_ID" --password-stdin`) works. Without a keychain, sbx warns that the credential is stored on disk, protected by file permissions; it's under `~/.config/com.docker.sandboxes` (mode 700), outside the repository.

### Cloud pricing (from the author's Agentic Platform Console, 2026-10-27)

The docs describe the billing model but don't publish rates: pay-as-you-go, metered by the second on runtime and size, with no subscription fee and a one-time promotional credit at signup (`/agentic-platform/signup.md`, `/subscription-billing/plans/docker-agentic-platform.md`). The rates shown in the Console:

| Shape | vCPU / memory | $ per second | ≈ $ per hour |
|-------|---------------|--------------|--------------|
| micro | 1 / 2 GiB | 0.00001944 | 0.07 |
| small | 2 / 4 GiB | 0.00003889 | 0.14 |
| medium | 4 / 8 GiB | 0.00007778 | 0.28 |
| large | 8 / 16 GiB | 0.00015556 | 0.56 |
| xl | 16 / 32 GiB | 0.00031111 | 1.12 |

The price doubles with each shape, exactly like the resources. Billed usage to 2026-10-27 was **31.277 s of micro**, for a probe and two runs whose wall-clock time was about 41 s: the meter counts sandbox runtime, not the client's create/copy/remove time. One run of piece 01 costs about $0.0002–0.0003.

### Docs pages linked from the articles (checked 2026-10-27; piece 01's added 2026-10-29)

- Overview: <https://docs.docker.com/ai/sandboxes/> ("Docker Sandboxes").
- Security model: <https://docs.docker.com/ai/sandboxes/security/>. It says the microVM is "the primary trust boundary". It describes local sandboxes and points to a local-vs-cloud comparison for the cloud.
- Cloud sandboxes: <https://docs.docker.com/ai/sandboxes/cloud/>.
- Piece 01: isolation layers <https://docs.docker.com/ai/sandboxes/security/isolation/> (microVM, own kernel, network policy through a host proxy; describes local sandboxes), cloud sandboxes <https://docs.docker.com/ai/sandboxes/cloud/>, expiration <https://docs.docker.com/ai/sandboxes/cloud/usage/#configure-expiration> (default TTL one hour) and cloud network policy <https://docs.docker.com/ai/sandboxes/cloud/network-policy/> (rules match destinations only, no method or path). The cloud pages don't call a cloud sandbox a microVM, so the article doesn't either.
- **Agentic Platform Console** (<https://agentic-platform.docker.com/>): **Sandboxes** lists running and paused cloud sandboxes; **Usage & billing** shows runtime and estimated cost, and the docs say it can take up to 48 hours to update (<https://docs.docker.com/agentic-platform/signup/>).
- **Broken link in the docs:** the credentials page links to `/ai/sandboxes/configuration/security/#trust-boundaries`, which returns 404. The security model lives at `/ai/sandboxes/security/`.

### OpenRouter in the cloud: docs vs `--help`

- `sbx --cloud secret set --help` lists `openrouter` among the built-in services.
- The cloud credentials page (`/ai/sandboxes/cloud/credentials.md`) says `openrouter` needs a custom secret in the cloud: `sbx --cloud secret set-custom --host openrouter.ai --env OPENROUTER_API_KEY`. The proxy then sets `Authorization: Bearer <key>` on requests to `openrouter.ai`, and the sandbox sees a placeholder.
- Not tried yet. To settle at piece 03.

## Codespace facts (2026-10-26)

- `/dev/kvm` is present (`crw-rw----`, owner root, GID 109, which has no name in `/etc/group`). The `codespace` user isn't in that group, so `sbx diagnose` reports *Virtualization — not accessible*. Not worked around (CLAUDE.md §5.2). See ADR-0001 and the session 01 journal.
- Default `python3` in the current Codespace image is 3.14.2. `python3.12` (3.12.3) is also present and is what `make test` uses. The devcontainer pins 3.12.

## Sign-in (verified 2026-10-29, sbx v0.50.0)

- `sbx login --username USER --password-stdin` (`--help`: "Non-interactive sign-in, for CI") signs in from a token on stdin. `scripts/sbx-login.sh` (`make login`) uses it with the `DOCKER_ID` and `DOCKER_PAT` secrets.
- On Linux without a keyring, it warns "no keychain detected; this secret will be stored on disk, protected by file permissions". The credentials land under `~/.config/com.docker.sandboxes`, outside the repository.
- Bare `sbx` when signed out starts the browser device flow (a URL and a one-time code). So does `sbx login` without flags.
- `sbx logout` stops running local sandboxes and signs out.

## A fresh Codespace from `.devcontainer/` (2026-10-29)

The first one built from the README badge, from `master` after PR #8:

- Ubuntu 24.04.3, `python3` 3.12.16 (the devcontainer's pin), Node 26.13.0, `sbx` v0.50.0, mermaid-cli 12.0.0.
- `/dev/kvm` absent ("no hypervisor present"), and no Docker, so `make site-build` skips the local build there. CI builds the site on every pull request.
- **Not signed in**: nothing used the `DOCKER_ID` and `DOCKER_PAT` secrets. Since session 11, `post-create.sh` runs `make login` when both are set.
- The old Codespace (sessions 01–11) wasn't a clean build of the current `.devcontainer/`: its default `python3` is 3.14.2, it has Docker, and its `/dev/kvm` exists but isn't accessible.

## Still to verify (before the wrapper or any article relies on it)

- `sbx secret`, `sbx policy` (local and cloud) and `sbx template save`.
- Whether the `shell` template has `python3` locally. (In the cloud: yes, Python 3.14.4, every run since session 02.)
- `sbx stop` / resume semantics (piece 02) and `sbx move`.
- Cloud network policy defaults for a new account.
