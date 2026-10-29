---
title: "ADR-0013 — The disclosure line"
adr: "0013"
status: accepted
date: 2026-10-26
---

**Status:** accepted, 2026-10-26. Wording direction from the author in session 03; Claude drafted the text. Resolves the open point in [ADR-0008]({{ "/decisions/ADR-0008-medium-publication/" | relative_url }}) and makes a deliberate exception to CLAUDE.md §0.6. Amended 2026-10-29 (session 10): the author changed "I'm enthusiastic about this technology" to "I ❤️ this technology". The line below is the current wording.

## Context

CLAUDE.md §3.2 requires every article to carry a disclosure line: written with Claude's assistance, code and runs reproducible from the repository at a tag. Two more things are worth disclosing:

- **The author's connection to Docker.** The series is published in a Docker community publication and is about a Docker product.
- **The header images are AI-generated**, with Google's Nano Banana 2 model via OpenRouter.

The author's direction: say that they're a Docker Captain and enthusiastic about the technology. Low profile, minimal, and no hedging.

## Decision

Each short piece (01–05) ends with this line, in italics:

> *Disclosure: I'm a Docker Captain, and I ❤️ this technology. This article was written with the assistance of Claude (Anthropic), and the header image is AI-generated (Google's Nano Banana 2, via OpenRouter). The code and every run are reproducible from [five-easy-pieces-agentic-ai](https://github.com/andreagalle/five-easy-pieces-agentic-ai/tree/piece-0N-v1) at tag `piece-0N-v1`.*

The hub (00) and the making-of (06) use the same line, with the last sentence replaced by "The code and the full making-of live in [five-easy-pieces-agentic-ai](https://github.com/andreagalle/five-easy-pieces-agentic-ai)."

Why each part is there:

- **Docker Captain:** readers deserve to know the author's relationship with the vendor of the product being discussed. One plain clause is enough, without apology or disclaimers.
- **Claude:** the articles were drafted with an AI assistant, and the making-of (06) is about exactly that.
- **The header image:** it's AI-generated, and saying so costs one clause. The author asked for this to be stated explicitly (session 03).
- **The tag:** it's what makes "reproducible" checkable rather than a claim.

On Medium, each header image also carries a short caption, so readers learn it straight away rather than at the end of the article:

> *AI-generated illustration.*

The making-of site says the same on its home page, and covers the site icon too.

## Consequences

- CLAUDE.md §0.6 (no affiliations in the repository) gains one exception: the disclosure line states that the author is a Docker Captain. Nowhere else.
- If the model used for the header images changes, the line changes with it. The model is recorded per image in `illustrations/log.jsonl`.
