---
layout: page
title: The five pieces
permalink: /pieces/
---

The series in one page. The world is the same in every piece, a vacuum cleaner on a grid, and each piece swaps in a new agent program. Across the five pieces the sandbox goes from **a formality** to **the thing that makes the agent safe to run**, and that progression is the point. Decisions: [ADR-0002]({{ "/decisions/ADR-0002-same-world-five-programs/" | relative_url }}), [ADR-0010]({{ "/decisions/ADR-0010-cloud-only-until-local-is-tested/" | relative_url }}), [ADR-0011]({{ "/decisions/ADR-0011-one-mode-per-piece/" | relative_url }}).

| Piece | Agent program | LLM | What the sandbox shows | Is the fence needed? |
|-------|---------------|-----|------------------------|----------------------|
| 01 Simple reflex | condition–action rules | no | disposability: create, copy in, run, copy out, delete | **No.** We use it anyway, to learn the mechanics. |
| 02 Model-based | rules plus internal state | no | persistence: state survives stop and restart | **No.** But the state now lives inside the sandbox. |
| 03 Goal-based | writes code until the tests pass | **yes** | network policy: deny everything, allow one host | **Yes.** It runs unread code and needs the network. |
| 04 Utility-based | picks the best of N candidates | **yes** | parallel sandboxes, sizes, TTL: cost in the utility | **Yes, N times,** and every fence costs money. |
| 05 Learning | rewrites its own instructions | **yes** | critic isolation: judge outside, agent inside | **Indispensable.** It must not reach its judge. |

## Why start without an LLM

Two reasons. First, **it isn't needed**: the lessons of 01 and 02 are clearest in a few lines of explicit code, and a model would hide them. Second, **it keeps complexity down**: with nothing unpredictable running, all the attention goes to containment itself.

**We sandbox 01 and 02 even though they don't need it, and we say so.** Learning a fence where nothing can go wrong is what lets you recognize, from 03 on, the moment it becomes essential.

## 01 — Simple reflex (no LLM)

**What it does.** Acts on the current percept only. Without a location sensor it loops forever; a coin flip gets it out of the loop.

**Why no LLM.** The lesson is one rule and its loop. You can point at the line responsible.

**Sandbox.** The program is trusted, uses only the standard library, needs no network and holds no secrets. The sandbox is still created, fed, run with the network fully blocked, emptied and destroyed. Why: to show the mechanics on a run where nothing is at stake, and to show that the architecture doesn't change the program. The output is byte-identical on the host and in the cloud.

## 02 — Model-based reflex (no LLM)

**What it does.** Keeps internal state: where it has probably been, and which squares are clean. With that state it sweeps the grid systematically instead of wandering, so it beats 01 on the same grid.

**Why no LLM.** Internal state is the lesson, and a small JSON file shows it better than a model's opaque memory.

**Sandbox.** Persistence: the agent's state file survives stopping and restarting the cloud sandbox, and a saved template captures it as a snapshot. The fence still isn't needed. Why show it: from 03 on, LLM agents keep their memory in files inside the sandbox too. Here we see the pattern calmly, on a file we can read.

## 03 — Goal-based (first LLM)

**What it does.** A small agent loop we write ourselves, in standard-library Python talking to a model through OpenRouter. Its goal is a test predicate: "the vacuum agent cleans the 4×4 grid within N steps". It writes code, runs the tests, reads the failures and tries again.

**Why an LLM here.** Goal-based agents search for action sequences that reach a goal. When the actions are "write code", that search is what today's LLM agents do. A breadth-first search on the grid would repeat the textbook without ever needing a fence. Writing the loop ourselves keeps the agent program readable, as in 01–02.

**Sandbox.** Network policy: deny everything, allow `openrouter.ai`. The API key is injected by the proxy, and the agent only sees a placeholder. **The fence is needed for the first time.** The agent runs code nobody has read, and it needs the network to reach its model, so "no network" is no longer an option. The question becomes *which* network.

## 04 — Utility-based (LLM)

**What it does.** Generates N candidate solutions, from different models and at different prices, each in its own sandbox. It scores them with a utility: tests passed, cleaning performance (including on the slippery grid), model cost, sandbox minutes and diff size. It keeps the best.

**Why an LLM here.** Utility means trade-offs, and OpenRouter makes the cost trade-off real: a cheaper model that is almost as good can win.

**Sandbox.** Parallel sandboxes, each with an explicit size and a TTL that deletes it on expiry. **The fence is needed N times.** The candidates are untrusted, must not interfere with each other or with the host, and a runaway candidate is capped in time and therefore in money.

## 05 — Learning (LLM)

**What it does.** Rewrites its own instruction file after each round, using feedback from a critic. The critic is a fixed benchmark in the vacuum world, run on the host.

**Why an LLM here.** An agent that edits its own instructions is today's learning agent, and the bridge to article 06: this repository's `CLAUDE.md` is exactly such a file.

**Sandbox.** Critic isolation: the critic sits outside, the agent inside, and results move only through `sbx --cloud cp`. **The fence is indispensable.** An optimizer that can reach its own scorer will eventually improve the scorer instead of itself. AIMA says the performance standard must be fixed and outside the agent; the sandbox enforces that physically.

## Credentials

- **Codespaces secrets:** `DOCKER_ID` and `DOCKER_PAT` (sign-in to Docker, needed from 01), and `OPENROUTER_API_KEY` (needed from 03).
- **Why OpenRouter:** one key for many models (04 compares them), one host to allow (`openrouter.ai`), and a credit limit on the key, so the budget is enforced outside the agent too.
- **Why the agent never sees the key:** from 03 on it runs model-generated code. A credential inside the sandbox could be printed, logged or sent elsewhere. The cloud proxy adds it to requests to `openrouter.ai`, and the sandbox only holds a placeholder.

## Local sandboxes

All published runs use cloud sandboxes for now. The local tier will be published once the author has tested it on a capable machine, expected soon ([ADR-0010]({{ "/decisions/ADR-0010-cloud-only-until-local-is-tested/" | relative_url }})).
