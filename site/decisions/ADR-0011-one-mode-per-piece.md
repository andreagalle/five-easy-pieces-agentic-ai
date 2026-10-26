---
title: "ADR-0011 — One mode per piece: no LLM in 01–02, LLM via OpenRouter in 03–05"
adr: "0011"
status: accepted
date: 2026-10-26
---

**Status:** accepted, 2026-10-26. Decided by the author (open decision D2) in session 02. Supersedes [ADR-0004]({{ "/decisions/ADR-0004-llm-variants-deferred/" | relative_url }}) and amends [ADR-0002]({{ "/decisions/ADR-0002-same-world-five-programs/" | relative_url }}). One-page summary: [The five pieces]({{ "/pieces/" | relative_url }}).

## Context

The brief planned two versions of each piece: a deterministic core and an optional LLM "today's twin". Two questions were open: should the twins exist, and should each piece carry both versions?

The deterministic version makes AIMA's mechanisms visible: you can point at the rule that loops. It's also free and reproducible byte for byte. But it never needs a sandbox: a trusted, 40-line, stdlib-only program has nothing to contain. An LLM agent is the opposite. It runs code nobody has read, needs the network to reach its model, and will optimize whatever it can reach. That's when a fence stops being a formality.

## Options considered

1. **No LLM anywhere.** Cheapest and fully reproducible, but the series about *agentic* AI never shows an AI agent, and the sandbox never has to earn its place.
2. **Both versions in every piece** (the brief's plan). Complete, but every piece doubles: two programs, two runs, two explanations in 600–900 words.
3. **One mode per piece.** No LLM where the lesson doesn't need one, an LLM where the sandbox becomes necessary.

## Decision

Option 3:

- **Pieces 01 and 02: no LLM.** Deterministic, stdlib-only programs in the shared vacuum world.
- **Pieces 03, 04 and 05: LLM agents only**, through OpenRouter. No deterministic twin.

Starting without an LLM is deliberate, for two reasons:

1. **It isn't needed.** The lessons of 01 and 02 (rules that loop, internal state that fixes the loop) are clearest in a few lines of explicit code, and a model would only hide them.
2. **It keeps complexity down,** so the first two pieces can focus calmly on containment itself: how a sandbox is created, fed, run, emptied and destroyed, and how state survives in it. **We sandbox these programs even though they don't need it**, and the articles say so. Learning the mechanics where nothing can go wrong makes it easier to see, from piece 03 on, exactly when and why they become indispensable.

Why OpenRouter:

- **One key, many models.** Piece 04 compares models with different prices, so cost becomes a real term in the utility rather than a made-up one.
- **One host to allow,** `openrouter.ai`. The network policy of 03–05 stays a single line: deny everything, allow that host.
- **A spending cap outside the agent.** The author sets a credit limit on the OpenRouter key, so even the budget is fenced in by something the agent can't touch.

How the key travels:

1. A Codespaces secret, `OPENROUTER_API_KEY`, holds it.
2. A script uploads it to the cloud secret store as a custom secret for host `openrouter.ai`. The cloud credentials page says OpenRouter needs a custom secret in the cloud, even though `sbx --cloud secret set --help` lists it as a built-in service; the first run will settle which works.
3. The cloud proxy writes it into requests to `openrouter.ai`.

The sandbox only sees a placeholder. **Why it matters:** the agent runs model-generated code, so it must never hold a credential it could print or send elsewhere.

## Consequences

- No `agent_llm/` directories. Pieces 03–05 keep their code in `agent/`, like 01–02.
- The deterministic plans for 03–05 in CLAUDE.md §4 (BFS/A\*, one-step expected utility, tabular Q-learning) are dropped. The LLM pieces still work in the shared vacuum world: the code they write is an agent program for that world, so their results can be compared with 01 and 02. This is to be confirmed as each piece is scaffolded.
- Pieces 03–05 are nondeterministic. Each article reports one recorded run (`RUNINFO.json`, plus the model and token cost), not a promise of identical output.
- Readers need their own OpenRouter key to rerun 03–05. Pieces 01–02 stay free to reproduce.
- Still to decide when building 03: the model(s) and the credit limit on the key.
