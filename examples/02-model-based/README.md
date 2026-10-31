# 02-model-based — Model-based reflex agent

**AIMA 4e §2.4.3.** The same blind vacuum agent as piece 01, with one addition: internal state. It can't sense where it is, so it tracks where it believes it is, learns the walls by bumping into them once, and remembers which squares it has seen clean. Its rules read that state, not the percept. The state is a small JSON file that survives stopping and restarting the cloud sandbox.

**Is the fence needed here? No.** It's a small program we wrote and read, with no network and no secrets. What changes is what's at stake inside the sandbox: the agent's memory now lives there.

- `agent/programs.py` — the agent: its state, the transition and sensor models, and the rules
- `agent/run.py` — the scenarios. Runs in one go, or stops at a step and resumes from the saved state, and both routes write the same `out/results.json`, byte for byte.
- `tests/` — unit tests, run on the host (`make test`) and inside the sandbox (`run.sh`)
- `run.sh` — tests and half a sweep, stop, restart, the other half, via `scripts/sbx-run.sh`
- `policy.md` — network policy, and why

## Reproduce it

To be completed with the reference run.
