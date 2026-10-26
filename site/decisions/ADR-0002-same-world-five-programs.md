---
title: "ADR-0002 — Same world, five programs"
adr: "0002"
status: accepted
date: 2026-10-26
---

**Status:** accepted, 2026-10-26. Decided by the author in the project brief (CLAUDE.md §4); recorded by Claude in [session 01]({{ "/journal/2026-10-26-01-bootstrap/" | relative_url }}).

## Context

The series walks through AIMA's five agent types (§2.4.2–§2.4.6). Each piece needs runnable code that shows what that agent type can do that the previous one could not. AIMA's own thesis is *agent = architecture + program*: the series maps the architecture onto a Docker Sandbox.

## Options considered

1. **A different toy problem per piece**, each chosen to flatter its agent type. Easy to write, but readers can't compare the pieces, and every piece spends words on a new world.
2. **One shared environment and five agent programs.** Each piece swaps the program and keeps the world and the architecture fixed.
3. **LLM-based agents throughout.** Topical, but nondeterministic, costly to rerun, and they hide the textbook mechanisms behind a model.

## Decision

Option 2. One small environment package, `examples/_shared/worlds/`, based on AIMA's vacuum world and generalized to an N×M grid. Switches turn on partial observability, stochastic actions and dynamic dirt. Each piece adds one agent program and showcases exactly one Docker Sandboxes feature:

- 01 simple reflex: disposability (create, run, remove; identical output local and cloud)
- 02 model-based reflex: persistence (stop/resume, template save)
- 03 goal-based: network policy (deny by default, explicit allowlist)
- 04 utility-based: parallel sandboxes, sizes and TTL as a cost term
- 05 learning: critic isolation (critic outside, agent inside)

Environments and agent cores use Python 3.12, standard library only, with `unittest` tests. Optional LLM "today's twin" variants live apart in `agent_llm/` and depend on decision D2.

## Consequences

- The deterministic path needs nothing installed inside a sandbox, so runs are reproducible and need no network: egress can be blocked.
- The shared world has to be designed before piece 01. Its switches are a public interface that all five pieces depend on.
- The sequence of pieces makes one argument: each piece shows the previous program failing in an environment the new one handles. The articles must show that failure, not just assert it.
- Changing the shared world after a piece is tagged means re-running and re-tagging that piece.
