---
layout: post
title: "Session 11 — A fresh Codespace that couldn't sign in"
date: 2026-10-29
session: "11"
pieces: ["00", "01"]
sbx_version: "v0.50.0"
model: "claude-opus-5-5 (Claude Opus 5.5)"
sandbox_runs: { cloud: 0, local: 0 }
---

## Goal

After merging PR #8, the author built a fresh Codespace from the README's "Open in GitHub Codespaces" badge. The badge had been added ahead of its trigger, and this was the test it still owed. In the new Codespace they ran `make check-env` and `make compare-01`, and pasted the output. They then asked to rename the project's `/status` command, and to merge and rebuild the Codespace from `master` to rerun every test (translated from Italian).

## What we did

- **Read the fresh Codespace's report.**
  - **What worked:** `post-create.sh` installed `sbx` v0.50.0, mermaid-cli 12.0.0 and the charts' `.venv`, and `python3` was 3.12.16, the devcontainer's pin.
  - **What didn't:** `sbx` wasn't signed in. The `DOCKER_ID` and `DOCKER_PAT` secrets were set, but nothing used them. Bare `sbx` started the browser sign-in, which the author interrupted, and `make compare-01` stopped at its cloud check. No sandbox was created.
- **`make login`** (`e69938d`, `scripts/sbx-login.sh`):
  - with both secrets set, it signs in headless (`sbx login --username … --password-stdin`), and the token never reaches the output;
  - without them, it starts `sbx`'s browser flow, which needs a terminal;
  - `post-create.sh` runs it when both secrets are set;
  - `check-env` and `sbx-run` point to it when `sbx` isn't signed in.

  Tested in the old Codespace after `sbx logout`. Without secrets and without a terminal, it stops with a clear message (exit 2). With them, it signs in and `check-env` says "Tier C (cloud) ready: yes".
- **The docs put `make login` before `make run-01`** (`c5bd8cf`): the overture's "Run it yourself", piece 1's "Reproduce it", the example README and the README. The overture stays within 2,000 words.
- **`/status` is now `/series-status`** (`8c7fd2e`). In the new Codespace the author typed `/status` and got Claude Code's own status panel. A built-in command takes precedence over a project command with the same name, so ours had never run.
- **The `sbx` notes** record the sign-in facts and what a fresh Codespace looks like.

## Commands that mattered

From the `Makefile`:

```bash
make login        # sign sbx in to Docker: headless with the DOCKER_ID/DOCKER_PAT secrets, else in the browser
make check-env    # signed in: yes; Tier C (cloud) ready: yes
make compare-01   # piece 1 on the host and in a cloud sandbox
```

## Decisions

- No ADR. `make login` is a script that closes a gap. The rename is a process change, recorded in CLAUDE.md §9.4.
- `post-create.sh` signs in on its own when both secrets are set. A reader who sets the secrets the devcontainer asks for gets a Codespace that can run the pieces straight away. Without the secrets, nothing is attempted, and `check-env` says what to run.

## Dead ends and surprises

- **The old Codespace hid the gap.** The author had signed `sbx` in by hand in session 02, and every run since then relied on that. It also wasn't a clean build of the current `.devcontainer/`: it has Python 3.14.2 as `python3`, Docker, and a `/dev/kvm` it can't use. The fresh one has Python 3.12, no Docker and no `/dev/kvm`. Only a fresh build tests what readers get. That's why the badge's trigger in CLAUDE.md §9.3 asked for one.
- **A built-in command hid a project command.** `/status` had been in CLAUDE.md since session 01, and in this Codespace it was always run through the skill list rather than typed. The clash showed only when the author typed it.
- **Two Codespaces, one conversation.** The author tested in the new Codespace while this session kept running in the old one, so the output was pasted across. That worked, but notes kept in Claude's memory stay with the old Codespace. The journal is the record that travels.
- **Not known yet:** whether Codespaces hands the secrets to `postCreateCommand` at creation. If it doesn't, `check-env` says "signed in: no (…; run: make login)", and it's one command anyway. The next fresh build will tell.

## Who did what

- **The author:** merged PR #8, built the fresh Codespace, ran the tests and pasted the results, chose the rename, and decided to rebuild from `master` after the merge.
- **Claude:** found the cause, wrote `make login` and tested both paths, updated the docs and notes, renamed the command, and closed the session.

## Next

1. **The author:** merge PR #9, then build a fresh Codespace from the badge on `master` and run:
   - Check that the creation log shows `sbx-login: signing in with the DOCKER_ID and DOCKER_PAT secrets` (if not, `make login`).
   - `make check-env`, `make test`, `make lint`, `make article-check`, `make site-check`.
   - `make compare-01` (expect `compare: identical`), then `sbx --cloud ls` (expect nothing).
   - `/series-status` in Claude Code.

   Record the result in the next journal entry.
2. **If it all passes:** tag `piece-01-v1` on `master`, check piece 1's code links, and add the "Latest tag" badge.
3. **Publish piece 1, then the overture,** following `articles/PUBLISHING.md`.
