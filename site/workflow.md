---
layout: page
title: Workflow
permalink: /workflow/
---

How the series is made, as of session 01. This page changes when the workflow changes, and every change is noted in the [journal]({{ "/journal/" | relative_url }}).

![Workflow: the author prompts Claude Code in a GitHub Codespace; Claude Code edits the repository and runs examples through scripts/sbx-run.sh, which drives the sbx CLI; cloud sandboxes (or local ones, where KVM is available) run the example and results are copied back into the repository; article drafts and this site are built from the repository; the author edits and approves the drafts before they go to Medium.]({{ "/assets/img/workflow.png" | relative_url }})

*Diagram source: `site/assets/img/workflow.mmd`, rendered with `make diagrams`.*

## The pieces

- **The Codespace** is the only workstation. Its devcontainer (`.devcontainer/devcontainer.json`) installs Python 3.12, Node, the GitHub CLI and Claude Code. `scripts/post-create.sh` installs a pinned `sbx` and mermaid-cli, then prints a read-only environment report (`make check-env`).
- **Claude Code** runs in the Codespace, not in a sandbox. The author's answer to running it inside one was "absolutely not"; the honest answer would have been yes ([ADR-0009]({{ "/decisions/ADR-0009-claude-code-stays-outside/" | relative_url }})). It reads `CLAUDE.md` at the start of every session: the project brief, the rules, and the record-keeping duties.
- **The author** prompts, answers the open decisions, edits every article and approves every commit. Prompts may be in Italian; everything in the repository is English.
- **Sandboxes** are where the examples run. Every run will go through `scripts/sbx-run.sh`, which creates a sandbox, copies the example in, runs it, copies results and a `RUNINFO.json` out, and removes the sandbox. The wrapper is designed to work the same way in the cloud (`sbx --cloud`) and locally (`SBX_TARGET=local`), but for now only the cloud tier is used and published: the local tier waits until the author can test it on a capable machine. See [ADR-0001]({{ "/decisions/ADR-0001-execution-tiers/" | relative_url }}) and [ADR-0010]({{ "/decisions/ADR-0010-cloud-only-until-local-is-tested/" | relative_url }}).
- **The record** is written as the work happens: one journal entry per session, an ADR per decision, notable prompts, `series.yml` for status and `metrics.yml` for the numbers article 06 will quote.

## A session

1. Claude reads `CLAUDE.md`, `site/_data/series.yml` and the latest journal entry, then states what the session will do.
2. Work happens in small steps. `make test` runs after any change to an example, and sandboxes run only through the wrapper.
3. Article prose is written only about runs that happened and left a `RUNINFO.json`.
4. `/wrap` writes the journal entry, updates the data files, lists live cloud sandboxes and commits.

## Current state

As of session 01, no sandbox has run yet. `sbx` v0.50.0 is installed, but the Codespace isn't signed in to Docker, and local sandboxes can't start here because `/dev/kvm` isn't accessible to the Codespace user.
