---
title: "ADR-0009 — Claude Code stays outside the sandbox"
adr: "0009"
status: accepted
date: 2026-10-26
---

**Status:** accepted, 2026-10-26. Decided by the author (open decision D5) in session 02.

## Context

The series argues that agents need a fence: tools are actuators, and a sandbox limits what those actuators can reach without rewriting the agent program. The agent writing the series, Claude Code, runs directly in the GitHub Codespace. It has the whole filesystem, the network, the author's GitHub token and passwordless `sudo`. In session 01 it used that `sudo` to add an apt repository and install packages.

D5 asked whether, for some sessions, Claude Code should run inside a cloud sandbox (`sbx --cloud run claude`) instead: the author of a series about fences, working inside one.

## Options considered

1. **Yes, for some writing sessions.** Claude works on a git clone inside a cloud sandbox and pushes a branch. Examples still run from the Codespace, because launching sandboxes from inside a sandbox would need Docker credentials inside it, which CLAUDE.md §5.4 forbids.
2. **No.** Claude Code keeps running in the Codespace, as in session 01.

## Decision

Option 2. The author's answer: *absolutely not.*

For the record, and at the author's own request: **the correct answer would definitely have been yes.** A series that tells readers to fence their agents is being written by an agent with root access. Article 06 owes its readers that sentence.

## Consequences

- The workflow stays as it is. Claude Code runs in the Codespace, in the VS Code panel, with the permissions the author grants it session by session.
- Article 06 states the inconsistency plainly rather than hiding it.
- Nothing stops a later ADR from reversing this. Running one writing session in a cloud sandbox would cost cloud minutes and a GitHub credential stored with `sbx --cloud secret`.
