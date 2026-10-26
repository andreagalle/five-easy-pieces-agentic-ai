---
title: "ADR-0004 — LLM \"today's twin\" variants: deferred"
adr: "0004"
status: superseded
date: 2026-10-26
---

**Status:** superseded by [ADR-0011]({{ "/decisions/ADR-0011-one-mode-per-piece/" | relative_url }}) in session 02. Originally deferred, 2026-10-26: the author postponed open decision D2 in [session 01]({{ "/journal/2026-10-26-01-bootstrap/" | relative_url }}). It must be decided before example 03 is scaffolded.

## Context

Each piece has a deterministic core: a standard-library Python agent in the shared vacuum world ([ADR-0002]({{ "/decisions/ADR-0002-same-world-five-programs/" | relative_url }})). CLAUDE.md §4 also sketches an optional LLM-powered "today's twin" per piece, the same agent type in its present-day form:

- 03 goal-based: a coding agent in a sandbox whose goal is a test predicate ("all tests pass")
- 04 utility-based: best-of-N candidates scored by a utility that includes cloud cost
- 05 learning: an agent that rewrites its own instruction file from a critic's feedback

For 01 and 02 the twin can stay in prose (a guardrail as a reflex agent; a memory file as internal state).

A "yes" brings a model provider and model, credentials (an API key stored with `sbx secret`, or a subscription sign-in inside the sandbox), network egress to the provider only, per-run model costs on top of sandbox minutes, and nondeterministic output. The articles would report one recorded run rather than promise identical results.

## Options considered

1. **Yes**, for some or all of pieces 03–05, with a provider, model and budget cap.
2. **No.** The twins appear only in prose.
3. **Decide later.** Pieces 01–02 don't depend on the answer.

## Decision

Option 3: decide before example 03 is scaffolded (`/new-piece 03` checks this ADR).

## Consequences

- Pieces 01 and 02 are built with deterministic cores only. Their "Why it still matters" sections describe the twin in prose.
- No `agent_llm/` directories, no `ANTHROPIC_API_KEY` secret and no model egress for now.
- When this is revisited, the answer must cover: which pieces, provider and model, a budget cap, and the authentication path.
