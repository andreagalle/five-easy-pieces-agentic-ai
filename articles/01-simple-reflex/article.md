---
id: "01"
title: "Piece 1/5 — The simple reflex agent"
status: published
drafted_by: claude
edited_by: author
verified_with: "sbx v0.50.0 (2026-10-29)"
code_tag: "piece-01-v1"
medium_url: "https://medium.com/docker-captains-wisdom/piece-1-5-the-simple-reflex-agent-b34c17054a7b"
---

# Piece 1/5 — The simple reflex agent

*It has rules, no memory, and a wall it will push against forever.*

![Inside a glass sphere so thin it is barely there, a small blue cleaner fish swims above a few sand-coloured stones, trailing a ring of bubbles that loops back on itself. Beside it, a sand dollar stands upright on its edge with a small red glint.](assets/header.jpg)

*AI-generated illustration.*

Every guardrail that blocks a tool call because it matches a pattern is a simple reflex agent. So is a thermostat, a spam rule, and the pre-commit hook that rejects your commit at six on a Friday evening. They look at what's in front of them, apply a rule, and act. They remember nothing, and most of the time that's exactly why they work.

## What AIMA says

The simplest agent in the book picks its action from the current percept alone, ignoring everything it perceived before (AIMA 4e, §2.4.2). Its program is a list of condition–action rules, such as *if the square is dirty, suck*. That's enough when the right action can be read off the present moment, which in the book's terms means the environment is fully observable.

Take away part of the view and things go wrong fast: a reflex agent that can't tell where it is can repeat the same useless action forever. The book's way out is to randomize, and it's candid that this is a patch. With a single agent in the world, a more sophisticated agent that doesn't gamble usually does better. That agent is piece 2.

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

The book's own example is the smallest world it can draw: two squares, A and B, each clean or dirty (§2.1). The agent senses which square it's on and whether it's dirty, and the sighted agent's rules cover all four cases: suck if dirty, otherwise move to the other square. Starting on A with both dirty, it sucks, moves and sucks: all clean by step 3.

Over ten steps the best possible score is 20. The sighted agent gets 18, because B stayed dirty for two steps. Then it shuttles between clean squares for nothing, a waste the book itself points out, free only because the measure doesn't charge for moves.

Without the location sensor, the rule for a clean square has to pick one direction for good. Ours goes right. From B it sucks, hits the wall and keeps pushing, so A stays dirty forever and the score drops to 10. Going left would fail the same way from A. A coin flip breaks the tie: on average the agent finds the other square in two tries, and here it scores 18 again.

![Three small step charts over ten time steps, each showing whether the agent is on square A or B. With a location sensor the agent alternates between A and B and everything is clean at step 3. Blind, the line stays flat on B for all ten steps and square A is never cleaned. Blind with a coin flip, it reaches A and everything is clean at step 3.](assets/fig-two-squares.png)

On a 4×4 grid the same rules get a bigger room to fail in. The blind agent cleans the top row (steps 1, 3, 5 and 7), reaches the right-hand wall and stays against it for the remaining 194 of its 200 steps. Twelve squares are never visited. The random agent picks one of four directions on each clean square. It does clean all 16, but a random walk keeps revisiting squares it has already cleaned, so the last corner falls only at step 82.

![Two 4×4 heatmaps of the step at which each square was first cleaned. Blind, only the top row is cleaned, at steps 1, 3, 5 and 7; the other twelve squares are marked never. Random, every square is cleaned, the last ones in the top-right corner at steps 77, 80 and 82.](assets/fig-grid-cleaned-at.png)

Each agent's score is the area under its line: 2666 for the wanderer, 788 for the one stuck at the wall, out of 3200.

![A line chart of clean squares over 200 time steps. The random agent climbs in steps to all 16 squares clean at step 82 and stays there, for a score of 2666. The blind agent reaches 4 clean squares at step 7 and never changes again, for a score of 788. Each score is the area under its line.](assets/fig-grid-performance.png)

## Run it in a sandbox

```bash
make run-01
```

A Docker Sandbox is a disposable computer for one agent. Locally, it's a [microVM](https://docs.docker.com/ai/sandboxes/security/isolation/) with its own kernel, filesystem, network and Docker engine: what runs inside can't see the host's files or processes, and every outbound connection must pass a network policy. A [cloud sandbox](https://docs.docker.com/ai/sandboxes/cloud/) is the same kind of environment on Docker's infrastructure. It needs no virtualization on your machine, and it can't mount your folders: files go in and out by copy.

`make run-01` creates one, copies the code in, runs the tests and the scenarios, copies the results out with a `RUNINFO.json`, and deletes the sandbox. This line in `scripts/sbx-run.sh` creates it:

```bash
sbx --cloud create --name "$name" --ttl "$ttl" --on-timeout delete \
  --cpus "$cpus" --memory "$memory" "${network_flags[@]}" --no-progress "$agent"
```

Each setting has a reason:

- **`shell`:** a template with no AI agent installed, just Bash (and, as it happens, Python 3.14). Our agent is the program we copy in.
- **1 vCPU and 2 GiB:** the smallest size. Compute is billed by the second and by size, and forty lines of Python need nothing bigger.
- **`--ttl 30m --on-timeout delete`:** if my script dies halfway, the sandbox [deletes itself](https://docs.docker.com/ai/sandboxes/cloud/usage/#configure-expiration) after half an hour.
- **`--deny-network '**'`:** the [network policy](https://docs.docker.com/ai/sandboxes/cloud/network-policy/) refuses every destination. This agent needs no network, and "nothing" is the easiest policy to check.

Local sandboxes run the same script on a machine with hardware virtualization. My laptop is too old for that, so the local version waits until I buy a new one. Thank heaven for cloud sandboxes, which don't care how old it is.

## What the sandbox adds, here: disposability

The sandbox lives about ten seconds, then nothing is left: no machine, no files, nothing running up a bill. What comes back is byte for byte the `results.json` I get by running the program directly in my Codespace, with no sandbox at all. The Python versions differ (3.14.4 in the sandbox, 3.12 or 3.14 in the Codespace), and the bytes don't. CI checks it again after every merge that touches the code.

Does this agent need a fence? No: it's forty lines of code I've read, with no network and no secrets. We fence it anyway, to learn the mechanics on a run where nothing can go wrong, and to show that changing the architecture doesn't change the program.

## Reproduce it

- **Code:** [`examples/01-simple-reflex`](https://github.com/andreagalle/five-easy-pieces-agentic-ai/tree/piece-01-v1/examples/01-simple-reflex) at tag `piece-01-v1`
- **Where:** a Codespace opened from the repository has everything installed. Elsewhere you need `git`, `make`, Python 3.12+ and `sbx`; I've tested only on Linux. Either way, `make login` signs `sbx` in to your own Docker account, which needs cloud sandboxes enabled (pay-as-you-go). In a Codespace with `DOCKER_ID` and `DOCKER_PAT` secrets, that happens on its own.
- **Commands:** `make login`, then `make run-01`
- **Check it:** `make compare-01` runs the program on your machine and in a cloud sandbox. Expect `compare: identical`, and a `results.json` sha256 starting `efae1944`.
- **Sandbox:** cloud, `shell` template (`docker/sandbox-templates:shell-docker`)
- **Verified with:** `sbx` v0.50.0
- **Reference run:** 2026-10-27, commit `795ffb8`, `results.json` sha256 `efae1944…`

## The series

- [Five Easy Pieces on Agentic AI w/ Docker Sandboxes](https://medium.com/docker-captains-wisdom/five-easy-pieces-on-agentic-ai-w-docker-sandboxes-53d5acb6e2e4) (overture)
- **Piece 1/5 — The simple reflex agent** (you are here)
- Next: Piece 2/5 — The model-based reflex agent (coming soon)

*Disclosure: I'm a Docker Captain, and I ❤️ this technology. This article was written with the assistance of Claude (Anthropic), and the header image is AI-generated (Google's Nano Banana 2, via OpenRouter). The code and every run are reproducible from [five-easy-pieces-agentic-ai](https://github.com/andreagalle/five-easy-pieces-agentic-ai/tree/piece-01-v1) at tag `piece-01-v1`.*
