---
title: "ADR-0017 — The pieces run to 1,200 words"
adr: "0017"
status: accepted
date: 2026-10-29
---

**Status:** accepted, 2026-10-29. Decided by the author in session 10. Changes the target length for pieces 01–05 in CLAUDE.md §1.

## Context

CLAUDE.md §1 gave each short piece 600–900 words, about four minutes of reading. Reviewing the draft of piece 01, the author asked for more explanation three times:

- "What happened" should explain the example the way AIMA builds it, not leave it to the charts.
- "Run it in a sandbox" should say what a sandbox is, how this one is configured and why, with links to the Docker docs.
- "Reproduce it" should say where the run works and what a rerun should print.

Each request was about understanding, and piece 01 grew to 1,166 words of prose. Keeping 900 would mean cutting exactly what was asked for.

## Options considered

1. **Keep 600–900.** Move the list of sandbox settings and the "Where" and "Check it" lines into the example README behind a link, and cut the paragraph of "What AIMA says" that "What happened" now repeats. That fits, but the article stops explaining its own run.
2. **Raise the target to 600–1,200**, about five minutes of reading. The pieces stay shorter than the overture (1,500–2,000), and a ceiling still forces choices.
3. **No upper limit.** Nothing would stop each review from adding another paragraph.

## Decision

Option 2. Pieces 01–05 target **600–1,200 words** of prose. The overture (1,500–2,000) and the making-of (1,200–1,800) keep their targets.

Why: a piece is the article where the reader runs something. Explaining that run fully is worth one more minute of reading, and a 1,200-word ceiling still keeps the pieces short.

## Consequences

- CLAUDE.md §1, the default target in `scripts/article-check.py` and the placeholders for articles 02–05 now say 600–1,200. As before, the check warns on drafts and fails from status `review` on.
- Piece 01, at 1,166 words, is inside the target.
- **The record isn't rewritten.** ADR-0011 and earlier journal entries say 600–900, because that was the target when they were written.
