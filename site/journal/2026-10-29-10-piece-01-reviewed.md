---
layout: post
title: "Session 10 — Piece 1 reviewed, both articles ready"
date: 2026-10-29
session: "10"
pieces: ["00", "01"]
sbx_version: "v0.50.0"
model: "claude-opus-5-5 (Claude Opus 5.5)"
sandbox_runs: { cloud: 1, local: 0 }
---

## Goal

After merging session 09's pull request, the author asked for two site changes (translated from Italian):

- put "(the making-of)" in parentheses in the site title;
- drop the "— session NN" suffix from the prompts list.

Then they read the draft of piece 1 and sent comments one at a time, while they kept reading. At the end they ran piece 1 themselves from the Codespace, and declared the overture and piece 1 ready to merge and publish.

## What we did

**The site**

- **The title** is now "Five Easy Pieces on Agentic AI (the making-of)" (`7aa3705`).
- **The prompts list** shows the quote only (`d23f943`). Each prompt's own page keeps the session number in its title.
- **The header is twice the size** (`73dea0c`). The title went from 26 to 52 px and the logo from 40 to 112 px. On phones the increase is about one and a half times, because at twice the size the title would fill half the screen.
  - "(the making-of)" stays on one line, and wide screens balance the title's three lines.
  - This was checked with screenshots at 1100 and 390 px of a build made with GitHub's Pages image.

**Piece 1, comment by comment**

- **"What happened" explains the example the way AIMA builds it** (`ac27b77`): the two-square world, the four cases, why the best score is 20, the blind agent stuck at the wall, the coin flip, then the 4×4 grid. Before, the charts carried most of it.
- **"Run it in a sandbox" explains the sandbox** (`dee1132`). It says what a sandbox is: a microVM locally, the same kind of environment on Docker's infrastructure in the cloud. It gives the reason for each setting on the `create` line, with four links to the Docker docs. All four pages were opened before writing, and every flag was checked against `--help`.
- **The network-policy analogy** now says it's only an analogy, and names which agent is which (`dee1132`). The author later dropped the section that held it, "Why it still matters", for this piece only (`8e79092`): the hook already names today's reflex agents.
- **"Reproduce it" says where the run works and what a rerun prints** (`dee1132`):
  - in a Codespace from the repository, or on any machine with `git`, `make`, Python 3.12+ and `sbx`, tested on Linux only;
  - `make compare-01` should print `compare: identical`.
- **"The host" now says where it is** (`673d42c`): the Codespace, running the program directly, with no sandbox at all.
- **The local tier waits for a new laptop** (`8586937`, `d39313e`). Wherever the series said "a capable machine", it now says the author's laptop is too old, and adds: thank heaven for the cloud.
- **The disclosure line** now reads "I'm a Docker Captain, and I ❤️ this technology" (`c650564`), in both articles and in ADR-0013.
- **Length:** each comment added explanation, and the piece went from 893 to 1,178 words. ADR-0017 raised the pieces' target to 1,200 words (`7657948`). After dropping the section, piece 1 is at 1,092.

**The overture**

- **A paragraph on the pictures** (`1ffe05f`):
  - a cleaner fish (the vacuum agent) in a glass sphere (the sandbox);
  - the glass thickening across the five pieces as the fence becomes necessary;
  - the whale as the cloud;
  - piece 1's sand dollar as the coin flip.

  The author had asked why piece 1's header shows a coin. To stay within 2,000 words, four sentences that later pieces repeat are shorter. The overture is at 1,999.

**Getting ready to publish**

- **The author ran piece 1** with `make check-env` and `make compare-01`:
  - the same sha256 on the host (Python 3.14.2) and in the cloud (3.14.4);
  - exit code 0, 13 s;
  - `sbx --cloud ls` empty afterwards.

  The example README records the rerun.
- **`/verify-sbx` on piece 1 and its scripts:** every subcommand and flag exists in v0.50.0 with the meaning the text assumes. Both articles are now `ready`, with `verified_with: "sbx v0.50.0 (2026-10-29)"` (`c7a122a`).
- **An "Open in GitHub Codespaces" badge** (`9940058`), added at the author's request ahead of its trigger in CLAUDE.md §9.3. The test on a fresh Codespace is still to do.
- **`article-check` accepts relative paths** (`c31642a`). Before, it crashed on them.

## Commands that mattered

From the `Makefile`, as the author ran them:

```bash
make check-env    # Tier C (cloud) ready: yes
make compare-01   # piece 1 on the host and in a cloud sandbox; fails unless results.json matches
sbx --cloud ls    # nothing left behind
```

## Decisions

- [ADR-0017]({{ "/decisions/ADR-0017-pieces-up-to-1200-words/" | relative_url }}): the pieces run to 1,200 words (was 900). CLAUDE.md §1 and `article-check` follow.
- [ADR-0013]({{ "/decisions/ADR-0013-disclosure-line/" | relative_url }}) amended: the new wording of the disclosure line.
- No ADR for dropping "Why it still matters" from piece 1. It's an edit to one article, and the skeleton in CLAUDE.md §3.4 keeps that step for the other pieces until the author says otherwise.
- The Codespaces badge went up before its trigger, by the author's choice. CLAUDE.md §9.3 records that, along with the test still owed.

## Dead ends and surprises

- **The article contradicted the record.** Piece 1 said the Codespace runs Python 3.12. The `sbx` notes had said since session 01 that the Codespace's default `python3` is 3.14.2, and the author's rerun used it. The bytes were identical either way, but the sentence was wrong until the rerun exposed it. That's also a hint that this Codespace isn't a clean build of the current `.devcontainer/`, which pins 3.12. The fresh-Codespace test will tell.
- **A word cap against a reviewer who wants explanations.** Every comment asked for more, and none of it was padding. Keeping 900 would have meant cutting exactly what was asked for, so the target moved instead (ADR-0017).
- **Doubling the title exposed two layout bugs.** At 52 px the title broke at the hyphen in "making-of", leaving "of)" alone on a line. And the phone size for the logo had never applied, because a later CSS rule overrode it.
- **Stray escape sequences in the author's terminal.** `^[]11;rgb:…` and `^[[?1;2c` appeared around each `sbx --cloud cp` and `rm`, and once at the prompt after the run. They look like replies to terminal queries (background colour, device attributes) that arrive after `sbx` has stopped reading. They're cosmetic, and nothing is fixed yet.
- **sbx v0.50.1 appeared mid-session.** Its release notes list one fix and no flag changes. The series stays on v0.50.0, which every run used.

## Who did what

- **The author:**
  - reviewed piece 1 comment by comment, and asked for the explanations, the laptop line and the header size;
  - chose the 1,200-word target, the badge and the new disclosure wording;
  - edited a heading of piece 1 themselves ("What the sandbox adds, here: disposability");
  - dropped "Why it still matters";
  - ran piece 1 from the Codespace;
  - declared both articles ready.
- **Claude:** rewrote the sections, checked every docs link and flag, wrote ADR-0017, changed the header, ran `/verify-sbx`, and closed the session.

## Next

1. **The author:** open a fresh Codespace from the README badge and run `make check-env` and `make compare-01` there. If anything fails, fix `.devcontainer/` or the "Where" line in piece 1 before tagging.
2. **After the merge:** tag `piece-01-v1` on `master` and check that piece 1's code links resolve. Add the "Latest tag" badge.
3. **Publish piece 1, then the overture,** following `articles/PUBLISHING.md`. Then record the URLs in `series.yml` and add the "Articles published 2/7" badge.
