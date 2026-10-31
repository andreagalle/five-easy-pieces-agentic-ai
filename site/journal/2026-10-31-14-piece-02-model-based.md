---
layout: post
title: "Session 14 — The agent that takes notes, and a stop in the middle of its run"
date: 2026-10-31
session: "14"
pieces: ["02"]
sbx_version: "v0.50.0"
model: "claude-opus-5-5 (Claude Opus 5.5)"
sandbox_runs: { cloud: 3, local: 0 }
---

## Goal

The author checked the links on Medium, merged PR #11 and said to proceed (translated from Italian). The next step in the plan was example 2 and the draft of piece 2.

## What we did

- **The model-based reflex agent** (`a660c56`, `examples/02-model-based/`). It has the same sensors as piece 1's blind agent, plus internal state: where it believes it is, the walls it has hit, the squares it has seen clean. `update_state` holds the transition and sensor models. `choose_action` holds the rules, and it takes the state and no percept. Scaffolded with `/new-piece`. 14 unit tests.
- **The state does real work.** The agent learns each wall by hitting it once, turns before it next time, and uses the map to know when it has finished. It can start on any square.
- **The results, on piece 1's own scenarios:**
  - two squares from B, where the blind agent looped forever: 18/20, all clean at step 3, no coin;
  - the 4×4 grid: 2918/3200, all clean at step 34, four bumps (piece 1's random agent: 2666, step 82).
- **A stop in the middle of the run.** `agent.run` can stop at a step and resume from its saved state, and both routes write the same `results.json`, byte for byte (a unit test checks four stop points). `scripts/sbx-run.sh` gained `SBX_AFTER_RESTART`: after the first command succeeds, it stops the sandbox, waits for `stopped` and runs the second command in it. Piece 1 doesn't set it, and `make compare-01` still gives its hash, `efae1944…`.
- **The reference run** (`a660c56`, `make compare-02`): half a sweep in a cloud sandbox, stop, restart, the other half. It took 57 s, 44 of them waiting for `stopped`. `results.json` came out identical to an uninterrupted host run, sha256 `aee06cc3…`, with Python 3.14.4 in the cloud and 3.14.2 and 3.12.3 on the host.
- **What losing the state costs:** the `grid-amnesia` scenario wipes it at step 18. The agent doesn't get stuck. It rebuilds the map, and the grid is clean at step 45 with 2830 points: 11 steps and 88 points lost.
- **Two charts** (`f8c29c9`): the sweep with and without its state, and clean squares over time against piece 1's agents in grey.
- **The draft of piece 2** (`70cd411`), 1,148 words, from the recorded run.
- **`sandbox.yml`** now runs piece 2 as well.

## Commands that mattered

From the `Makefile` and `examples/02-model-based/run.sh`:

```bash
make test
make compare-02   # one go on the host, two halves in a cloud sandbox; fails unless results match
make plots-02
```

```bash
export SBX_AFTER_RESTART="python3 -m agent.run --resume --out out"
exec "$here/../../scripts/sbx-run.sh" "$here" \
  sh -c 'python3 -m unittest discover -s tests -t . && python3 -m agent.run --stop-at 18 --out out'
```

## Decisions

- No ADR yet. The agent, the wrapper option and the scenarios follow CLAUDE.md §4.
- **`sbx --cloud template save` is left out for now, and that's the author's call to confirm.** CLAUDE.md §4 and the pieces page mentioned it as a snapshot. The help says templates are multi-GB and take several minutes, the pages we read don't give a storage price, and the lesson doesn't need it. The pieces page no longer promises it. CLAUDE.md §4 still lists it until the author decides.
- **The chart that wipes the state at every step stayed out.** It was a one-off script, not a recorded run, so its numbers aren't in the article (CLAUDE.md §3.2).

## Dead ends and surprises

- **Amnesia is less dramatic than expected.** The plan was an agent that forgets and fails. With the corner-finding step, which lets it start anywhere, it recovers from any interruption, and only loses time. Wiping the state at each step in a one-off script never left a dirty square. The article reports that, because it's true and it's the better lesson: a good model can be rebuilt from percepts, at a price.
- **`stop` returns before the sandbox stops.** The command took under a second, and the sandbox reached `stopped` about 45 s later, so the wrapper has to poll.
- **The cloud stop is a true suspend.** In the probe, a background process survived the stop, unaware of it, and the VM's uptime advanced by only about 5 s. The article says why it uses a file all the same: a file can be read, copied out and checked.
- **A stopped sandbox has no running TTL,** so `--on-timeout delete` can't clean it up. The policy, the wrapper's comments and the article all say so.
- **The random agent keeps pace for 18 steps.** On a fully dirty grid, nearly any square is worth landing on. The chart showed it, and the article says it.
- **The commit counter broke quietly.** After `dev` fast-forwarded to `master`, `git rev-list --count` started counting merge commits. The metric now counts non-merge commits, which matches all the earlier values.

## Who did what

- **The author:** checked the Medium links, merged PR #11, and said to proceed.
- **Claude:** designed and wrote the agent, the tests, the wrapper option and the charts, ran the probe and the reference run, drafted the article and closed the session.
- **Still with the author:** the review of the draft, and the decision on `template save`.

## Next

1. **The author:** review the draft of piece 2.
2. **After review:** tag `piece-02-v1`, run `/verify-sbx`, and publish, one week after piece 1 (ADR-0007).
3. **Piece 3:** the first LLM agent, and the first time the fence is needed.
