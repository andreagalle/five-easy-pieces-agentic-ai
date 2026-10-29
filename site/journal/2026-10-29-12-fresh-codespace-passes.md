---
layout: post
title: "Session 12 — A fresh Codespace runs piece 1 end to end"
date: 2026-10-29
session: "12"
pieces: ["01"]
sbx_version: "v0.50.0"
model: "claude-opus-5-5 (Claude Opus 5.5)"
sandbox_runs: { cloud: 1, local: 0 }
---

## Goal

After merging PR #9, the author built a second fresh Codespace from the README badge, on `master` at `cd894cd`, and ran every check from session 11's "Next". They pasted the output, along with the output of `/series-status` from a new Claude session in that Codespace.

## What we did

- **The test the badge owed, passed.** In the fresh Codespace:
  - `make check-env` reported `signed in: yes` and `Tier C (cloud) ready: yes`, with Python 3.12.16. The author hadn't run `make login`, so the setup script signed in by itself: Codespaces does pass the secrets to `postCreateCommand`.
  - `make test` (15 tests), `make article-check` and `make site-check` passed.
  - `make compare-01` reported identical results: host Python 3.12.16, cloud 3.14.4, 12 s, sha256 `efae1944…`.
  - `sbx --cloud ls` was empty afterwards.
  - `/series-status`, the renamed command, gave the summary in a new Claude session and changed no files.
- **One failure: `make lint`** stopped with `docker: not found`. The Makefile uses `shellcheck` and `actionlint` from the system, and otherwise falls back to their Docker images. The old Codespace and CI's runner have Docker; a Codespace built from this devcontainer has neither the tools nor Docker.
- **`scripts/install-linters.sh`** (`e1888d2`), run by `post-create.sh`:
  - it installs `shellcheck` 0.10.0 and `actionlint` 1.7.12, the same versions as the Docker images;
  - it refuses any archive whose SHA-256 doesn't match. `actionlint`'s hashes match its release's checksums file. `shellcheck` publishes none, so its hashes are those downloaded today.

  Tested in the old Codespace: a fresh install, a second run (already installed), a tampered hash (refused, exit 1), and `make lint` passing with the binaries. Its first `make lint` caught an issue in the installer itself (SC2155), fixed before the commit.
- **The record:** CLAUDE.md §9.3 now says the Codespaces badge has passed its test. The `sbx` notes record the second fresh build.

## Commands that mattered

As the author ran them in the fresh Codespace, from the `Makefile`:

```bash
make check-env      # signed in: yes; Tier C (cloud) ready: yes
make test           # 15 tests
make lint           # failed without Docker; fixed by scripts/install-linters.sh
make article-check
make site-check
make compare-01     # compare: identical
sbx --cloud ls      # No sandboxes found
```

## Decisions

- No ADR. Installing the linters' release binaries instead of adding Docker to the devcontainer keeps the Codespace light and unprivileged. The Docker fallback stays for machines that have Docker.

## Dead ends and surprises

- **The old Codespace hid a second gap.** Its Docker made `make lint` work without anyone choosing that. CI's runner has Docker too. Only the fresh build showed that the devcontainer alone couldn't lint.
- **Two Claude sessions at once.** The author opened a new session in the fresh Codespace while this one, in the old Codespace, kept the work going. The new session only read files, so nothing collided. Two sessions writing to the same branch would collide.
- **No stray escape sequences this time.** The `^[]11;rgb:…` lines from session 10 didn't appear in the fresh Codespace's terminal, so they depend on the terminal more than on `sbx`.

## Who did what

- **The author:** merged PR #9, built the second fresh Codespace, ran every check and pasted the results, and ran `/series-status` there.
- **Claude:** read the results, wrote and tested the linter installer, and updated the record.

## Next

1. **The author:** merge this PR.
2. **Claude:** tag `piece-01-v1` on the merge commit, check that piece 1's code links resolve, and add the "Latest tag" badge.
3. **The author:** publish piece 1, then the overture, following `articles/PUBLISHING.md`, and send the two URLs.
