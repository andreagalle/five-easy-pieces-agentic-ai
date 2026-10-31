---
id: "02"
title: "Piece 2/5 — The model-based reflex agent"
status: draft
drafted_by: claude
edited_by: author
verified_with: "sbx v0.50.0 (2026-10-31)"
code_tag: "piece-02-v1"
medium_url: ""
---


# Piece 2/5 — The model-based reflex agent

*It can't see where it is, so it takes notes.*

![Inside a dimmed glass sphere in dark water, a small blue cleaner fish rests motionless above a grid of stones. Each stone it has already cleaned holds a small glowing pearl, in tidy rows, and the pearls keep glowing while everything else sleeps.](assets/header.jpg)

*AI-generated illustration.*

Look inside a coding agent's working folder and you'll often find a small file it wrote to itself: a plan, a to-do list, notes on what it has already tried. The model forgets everything between sessions, and the file doesn't. That file is the difference between the agent of piece 1 and the agent of this one.

## What AIMA says

A reflex agent fails when the right action depends on something it can't see right now. The book's answer is to keep track of what can't be seen: an *internal state*, built up from everything perceived so far (AIMA 4e, §2.4.3).

Keeping that state current takes two kinds of knowledge. A *transition model* says how the world changes, including what the agent's own actions do. A *sensor model* says how the world shows up in what the agent perceives. The rules then read the state, not the raw percept.

The book adds a caveat that has aged well: in a partially observable world, the state is a best guess, not the truth.

## PEAS and environment

The same world as piece 1, on purpose:

- **Performance measure:** one point for every clean square at every time step.
- **Environment:** the same two squares, then the same 4×4 grid, for 200 steps. Dirt stays where it started.
- **Actuators:** Suck, Left, Right, Up, Down, and now NoOp, because this agent knows when to stop.
- **Sensors:** is this square dirty, and did I just hit a wall. No location sensor, as for piece 1's blind agent.
- **Properties:** partially observable, single-agent, deterministic, sequential, static, discrete, known.

## The program

The agent's two models and its rules ([full code](https://github.com/andreagalle/five-easy-pieces-agentic-ai/tree/piece-02-v1/examples/02-model-based), docstrings trimmed):

```python
def update_state(state: State, percept: Percept) -> None:
    action, (x, y) = state.last_action, state.position
    if percept.bumped and action in WALL_HIT:
        # Sensor model: a bump means the move failed, and this square is the last on that side.
        state.walls[WALL_HIT[action]] = x if action in (Action.LEFT, Action.RIGHT) else y
    elif action in MOVES:
        # Transition model: without a bump, a move shifts the agent by exactly one square.
        dx, dy = MOVES[action]
        state.position = (x + dx, y + dy)
    if percept.dirty:
        state.clean.discard(state.position)
    else:
        state.clean.add(state.position)


def choose_action(state: State) -> Action:
    x, y = state.position
    if state.position not in state.clean:
        return Action.SUCK
    if finished(state):
        return Action.NOOP
    if "left" not in state.walls:
        return Action.LEFT
    if "top" not in state.walls:
        return Action.UP
    rightward = (y - state.walls["top"]) % 2 == 0
    if x == state.walls.get("right" if rightward else "left"):
        return Action.DOWN  # a known wall ahead: turn without bumping into it again
    return Action.RIGHT if rightward else Action.LEFT
```

Look at what `choose_action` takes: the state, and no percept. Everything the agent knows has to get in through `update_state`.

## What happened

Start with the case that beat piece 1's blind agent: two squares, starting on B. That agent pushed against the wall forever and scored 10 out of 20. This one sucks, moves left and sucks: all clean by step 3, 18 out of 20, no coin needed. It then walks the edges until its map is complete and stops, so the pointless shuttling of piece 1 is gone too.

On the 4×4 grid it first finds the top-left corner, by moving left and then up until it bumps. Then it sweeps row by row. It bumps into each wall once, four bumps in the whole run, because a wall it has hit is a wall it remembers. All 16 squares are clean at step 34, and the score is 2918 out of 3200. In piece 1, the random agent finished at step 82 with 2666, and the blind one never finished, with 788.

To see what the state is worth, the right-hand panel wipes it at step 18, halfway through. The world stays as it is, but the agent starts again from nothing.

![Two 4×4 grids showing the agent's path. On the left, with its state kept, it sweeps row by row from the top-left corner, with a marker at step 18 where the sandbox was stopped and restarted, and everything is clean at step 34. On the right, its state is lost at step 18: the first two rows are in blue, then a coral line goes back to the corner, crosses both clean rows again and finishes the grid at step 45.](assets/fig-sweep.png)

It doesn't get stuck. A good model can be rebuilt from percepts. But it walks back to the corner, finds the walls again and crosses two clean rows for nothing: all clean at step 45, 2830 points. Forgetting cost 11 steps and 88 points.

![A line chart of clean squares over the first 100 steps. Piece 2's agent reaches all 16 at step 34, the one that lost its state stays flat at 8 for a while and reaches 16 at step 45, piece 1's random agent reaches 16 at step 82, and piece 1's blind agent stops at 4.](assets/fig-performance.png)

For the first 18 steps the random agent keeps pace, because nearly every square it lands on is dirty. Memory pays off as dirt gets scarce, and luck stops working.

## Run it in a sandbox

```bash
make login
make run-02
```

The sandbox is set up as in piece 1, for the same reasons: the `shell` template, the smallest size, a 30-minute TTL with delete on timeout, and no network. What's new is one interruption in the middle. Here is `run.sh`:

```bash
export SBX_AFTER_RESTART="python3 -m agent.run --resume --out out"
exec "$here/../../scripts/sbx-run.sh" "$here" \
  sh -c 'python3 -m unittest discover -s tests -t . && python3 -m agent.run --stop-at 18 --out out'
```

The first command runs the tests and half a sweep, saves the state in the sandbox and exits. The wrapper then stops the sandbox, waits until it's really stopped, and runs the second command, which has only what the sandbox kept.

The local version is still waiting for that new laptop. Thank heaven for the cloud, again.

## What the sandbox adds, here: persistence

[`sbx --cloud stop`](https://docs.docker.com/ai/sandboxes/cloud/usage/#stop-or-remove-a-sandbox) suspends a sandbox: memory and filesystem are kept, the machine is released, and compute isn't billed while it's stopped. The command returns at once, but in our run the sandbox took 44 seconds to reach `stopped`, which is why the wrapper waits. The next `exec` brought it back in a second, with the same ID.

This is everything the agent knew at step 18, from its state file:

```json
{
  "position": [0, 1],
  "last_action": "Suck",
  "walls": {"left": 0, "top": 0, "right": 3},
  "clean": [[0, 0], [1, 0], [1, 1], [2, 0], [2, 1], [3, 0], [3, 1]]
}
```

There's no bottom wall yet, because it hasn't hit one. And it lists seven clean squares while the world has eight, because it hasn't yet seen the result of its last Suck. The book's caveat, in seven coordinates: state is a belief.

After the restart the agent read that file and carried on. The report that came back is byte for byte the one from a run that was never interrupted, on different Python versions.

The stop is a true suspend: in a separate test, a background process left running simply carried on afterwards, unaware. So why a file? Because a file can be read, copied out and checked, which is the point of a series that shows its work.

One thing to watch: a stopped sandbox has no running TTL, so `--on-timeout delete` can't clean it up. The wrapper removes it on exit, and if a run is killed outright, `sbx --cloud ls` will show it.

Does this agent need a fence? Still no: it's a small program I've read, with no network and no secrets. What has changed is what deleting the sandbox costs. In piece 1, disposability was free. Here the agent's memory lives inside, and throwing the sandbox away throws that away too.

## Why it still matters

Agents that keep notes inherit the book's caveat. Stale notes get acted on with complete confidence, because to the agent they are the world. And this agent, for all its memory, doesn't want anything: it sweeps because its rules say so. Piece 3 gives it a goal.

## Reproduce it

- **Code:** [`examples/02-model-based`](https://github.com/andreagalle/five-easy-pieces-agentic-ai/tree/piece-02-v1/examples/02-model-based) at tag `piece-02-v1`
- **Where:** a Codespace opened from the repository has everything installed. Elsewhere you need `git`, `make`, Python 3.12+ and `sbx`; I've tested only on Linux. Either way, `make login` signs `sbx` in to your own Docker account, which needs cloud sandboxes enabled (pay-as-you-go). In a Codespace with `DOCKER_ID` and `DOCKER_PAT` secrets, that happens on its own.
- **Commands:** `make login`, then `make run-02`
- **Check it:** `make compare-02` runs the program in one go on your machine, and in two halves in a cloud sandbox, stopped and restarted in between. Expect `compare: identical`, and a `results.json` sha256 starting `aee06cc3`.
- **Sandbox:** cloud, `shell` template (`docker/sandbox-templates:shell-docker`)
- **Verified with:** `sbx` v0.50.0
- **Reference run:** 2026-10-31, commit `a660c56`, `results.json` sha256 `aee06cc3…`

## The series

- [Five Easy Pieces on Agentic AI w/ Docker Sandboxes](https://medium.com/docker-captains-wisdom/five-easy-pieces-on-agentic-ai-w-docker-sandboxes-53d5acb6e2e4) (overture)
- Previous: [Piece 1/5 — The simple reflex agent](https://medium.com/docker-captains-wisdom/piece-1-5-the-simple-reflex-agent-b34c17054a7b)
- **Piece 2/5 — The model-based reflex agent** (you are here)
- Next: Piece 3/5 — The goal-based agent (coming soon)

*Disclosure: I'm a Docker Captain, and I ❤️ this technology. This article was written with the assistance of Claude (Anthropic), and the header image is AI-generated (Google's Nano Banana 2, via OpenRouter). The code and every run are reproducible from [five-easy-pieces-agentic-ai](https://github.com/andreagalle/five-easy-pieces-agentic-ai/tree/piece-02-v1) at tag `piece-02-v1`.*
