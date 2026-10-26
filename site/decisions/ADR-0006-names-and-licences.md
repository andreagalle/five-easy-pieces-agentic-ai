---
title: "ADR-0006 — Repository name, handle and licences"
adr: "0006"
status: accepted
date: 2026-10-26
---

**Status:** accepted, 2026-10-26. Decided by the author (open decision D4) in [session 01]({{ "/journal/2026-10-26-01-bootstrap/" | relative_url }}).

## Context

The project brief kept the author's public handle as a placeholder (`<AUTHOR_HANDLE>`) and proposed licences: MIT for code, CC BY 4.0 for article text. It also forbids the author's legal name anywhere in the repository. Two places carry the author's configured git identity anyway: commit metadata and the copyright line of the `LICENSE` file GitHub generated in the initial commit.

## Options considered

- Repository name: keep `five-easy-pieces-agentic-ai`, or rename before anything links to it.
- Licences: the proposed pair, or alternatives (Apache-2.0 for code; CC BY-SA or all rights reserved for text).
- Git identity and `LICENSE` holder: keep the configured identity, or switch both to the handle.

## Decision

- Repository name: **`five-easy-pieces-agentic-ai`**, unchanged.
- Author handle: **`andreagalle`**. It replaces `<AUTHOR_HANDLE>` everywhere.
- Code: **MIT**, the existing `LICENSE` file.
- Article text and site prose: **CC BY 4.0**, excluding quoted AIMA material and other third-party quotations, which stay under their owners' copyright. Stated in `LICENSE-text.md`.
- Git commit metadata and the `LICENSE` copyright line **keep the configured git identity**, by the author's choice. Everywhere else, the handle is used.

## Consequences

- `site/_config.yml` and the README use the handle. Future sessions don't flag the git identity or the `LICENSE` copyright line again; CLAUDE.md §0.6 records the exception.
- Published articles carry the CC BY 4.0 notice. The quote budget in CLAUDE.md §2.2 keeps AIMA excerpts short enough that the exclusion stays simple to state.
