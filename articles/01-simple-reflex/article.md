---
id: "01"
title: "Piece 1/5 — The simple reflex agent"
status: draft
drafted_by: claude
edited_by: author
verified_with: "sbx v0.50.0 (2026-10-26)"
code_tag: "piece-01-v1"
medium_url: ""
---

# Piece 1/5 — The simple reflex agent

*It has rules, no memory, and a wall it will push against forever.*

![Inside a glass sphere so thin it is barely there, a small blue cleaner fish swims above a few sand-coloured stones, trailing a ring of bubbles that loops back on itself. Beside it, a sand dollar stands upright on its edge with a small red glint.](assets/header.jpg)

*AI-generated illustration.*

Every guardrail that blocks a tool call because it matches a pattern is a simple reflex agent. So is a thermostat, a spam rule, and the pre-commit hook that rejects your commit at six on a Friday evening. They look at what's in front of them, apply a rule, and act. They remember nothing, and most of the time that's exactly why they work.

## What AIMA says

The simplest agent in the book picks its action from the current percept alone, ignoring everything it perceived before (AIMA 4e, §2.4.2). Its program is a list of condition–action rules, such as *if the square is dirty, suck*. That's enough when the right action can be read off the present moment, which in the book's terms means the environment is fully observable.

Take away part of the view and things go wrong fast. A reflex agent that can't tell where it is can repeat the same useless action forever. The book's way out is a coin flip: pick a random move when the rules can't decide. It's also candid that this is a patch. With a single agent in the world, a more sophisticated agent that doesn't gamble usually does better. That agent is piece 2.

## PEAS and environment

- **Performance measure:** one point for every clean square at every time step.
- **Environment:** two squares, the book's A and B, then a 4×4 grid. Dirt stays where it started.
- **Actuators:** Suck, Left, Right, Up, Down.
- **Sensors:** is this square dirty, did I just hit a wall, and (switchable) where am I.
- **Properties:** partially observable (badly so without the location sensor), single-agent, deterministic, sequential, static, discrete, known.

## The program

Three agents, a line or two apart ([full code](https://github.com/andreagalle/five-easy-pieces-agentic-ai/tree/piece-01-v1/examples/01-simple-reflex), docstrings trimmed):

```python
def reflex_vacuum_agent(percept: Percept) -> Action:
    """The two-square agent: suck if dirty, otherwise go to the other square."""
    if percept.dirty:
        return Action.SUCK
    if percept.location == (0, 0):
        return Action.RIGHT
    return Action.LEFT


def blind_reflex_agent(percept: Percept) -> Action:
    """The same rules without a location sensor."""
    if percept.dirty:
        return Action.SUCK
    return Action.RIGHT


class RandomizedReflexAgent:
    """Blind too, but flips a coin on clean squares."""

    def __init__(self, seed: int, moves: Sequence[Action] = (Action.LEFT, Action.RIGHT)):
        self.rng = random.Random(seed)
        self.moves = tuple(moves)

    def __call__(self, percept: Percept) -> Action:
        if percept.dirty:
            return Action.SUCK
        return pick(self.rng, self.moves)
```

The blind agent isn't stupid. It's the sighted agent's rules, minus the one fact they depended on.

## What happened

On two squares the sighted agent has both clean by step 3 and scores 18 out of 20. The blind one starts at B, sucks, turns right, hits the wall, and keeps pushing. Square A stays dirty forever: 10 out of 20. The coin flip gets it back to 18.

![Three small step charts over ten time steps, each showing whether the agent is on square A or B. With a location sensor the agent alternates between A and B and everything is clean at step 3. Blind, the line stays flat on B for all ten steps and square A is never cleaned. Blind with a coin flip, it reaches A and everything is clean at step 3.](assets/fig-two-squares.png)

On a 4×4 grid the difference grows. The blind agent cleans the top row, then spends 194 of its 200 steps pushing against the right-hand wall. The random one cleans all 16 squares, but needs 82 steps to do it, because it gets there by wandering.

![Two 4×4 heatmaps of the step at which each square was first cleaned. Blind, only the top row is cleaned, at steps 1, 3, 5 and 7; the other twelve squares are marked never. Random, every square is cleaned, the last ones in the top-right corner at steps 77, 80 and 82.](assets/fig-grid-cleaned-at.png)

![A line chart of clean squares over 200 time steps. The random agent climbs in steps to all 16 squares clean at step 82 and stays there, for a score of 2666. The blind agent reaches 4 clean squares at step 7 and never changes again, for a score of 788. Each score is the area under its line.](assets/fig-grid-performance.png)

## Run it in a sandbox

```bash
make run-01
```

That creates a cloud sandbox, copies the code in, runs the tests and then the scenarios, copies the results out with a `RUNINFO.json`, and deletes the sandbox. This is the line in `scripts/sbx-run.sh` that creates it, with the network denied by default:

```bash
sbx --cloud create --name "$name" --ttl "$ttl" --on-timeout delete \
  --cpus "$cpus" --memory "$memory" "${network_flags[@]}" --no-progress "$agent"
```

A locally tested version will follow once I've run it on a capable machine.

## What the sandbox adds: disposability

The sandbox lives for about ten seconds, on the smallest size, with no network at all, and it deletes itself if anything goes wrong first. What comes back is a `results.json` that's byte for byte identical to the one produced on the host, even though the sandbox runs Python 3.14 and the host 3.12. CI checks it again after every merge that touches the code.

Does this agent need a fence? No. It's forty lines of code I've read, with no network and no secrets. We fence it anyway, for two reasons. We learn the mechanics on a run where nothing can go wrong. And we show that changing the architecture doesn't change the program.

## Why it still matters

The sandbox's own network policy is a simple reflex agent: for each outbound request, if the host is on the list, allow it, otherwise deny it. It shares the reflex agent's blind spot, too. It judges each request alone, so it can't see what a hundred allowed requests add up to. Rules are fast and cheap. Memory is what piece 2 adds.

## Reproduce it

- **Code:** [`examples/01-simple-reflex`](https://github.com/andreagalle/five-easy-pieces-agentic-ai/tree/piece-01-v1/examples/01-simple-reflex) at tag `piece-01-v1`
- **Command:** `make run-01`
- **Sandbox:** cloud, `shell` template (`docker/sandbox-templates:shell-docker`), 1 vCPU / 2 GiB, no egress
- **Verified with:** `sbx` v0.50.0
- **Reference run:** 2026-10-27, commit `795ffb8`, `results.json` sha256 `efae1944…`

## The series

- Five Easy Pieces on Agentic AI w/ Docker Sandboxes (overture, link added at publication)
- **Piece 1/5 — The simple reflex agent** (you are here)
- Next: Piece 2/5 — The model-based reflex agent (coming soon)

*Disclosure: I'm a Docker Captain, and I'm enthusiastic about this technology. This article was written with the assistance of Claude (Anthropic), and the header image is AI-generated (Google's Nano Banana 2, via OpenRouter). The code and every run are reproducible from [five-easy-pieces-agentic-ai](https://github.com/andreagalle/five-easy-pieces-agentic-ai/tree/piece-01-v1) at tag `piece-01-v1`.*
