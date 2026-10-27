---
title: "ADR-0016 — The first article is the overture"
adr: "0016"
status: accepted
date: 2026-10-27
---

**Status:** accepted, 2026-10-27. Decided by the author in session 07.

## Context

The project brief called article 00 "the hub". The term comes from the hub-and-spokes model of editorial content strategy: one central article that links to all the others. It's clear to people who work on content and cold to everyone else. Reviewing the article, the author asked why it was called that and for something better. "Intro" sold it short.

## Options considered

1. **Overture.** In music, the opening piece that introduces the themes of everything that follows.
2. **Prelude.** The piece before the main work; lighter, and it doesn't promise to introduce all the themes.
3. **Piece 0.** Zero-based, like its file name, but it makes the frame sound like one of the pieces.
4. **Keep "hub".**

## Decision

Option 1: **overture**. It describes what the article does, introducing the themes of the five pieces, and it fits a series made of "pieces".

## Consequences

- The folder is now `articles/00-overture/`, and the series list in `site/_data/series.yml` says `kind: overture`.
- CLAUDE.md, the README, the publishing checklist, the illustrations README and the article itself use "overture".
- **The record isn't rewritten.** ADR-0001 to ADR-0015 and the journal entries for sessions 01–06 say "hub", because that's what it was called when they were written. Read "hub" there as "overture".
