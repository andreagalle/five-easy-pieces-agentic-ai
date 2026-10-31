# 02-model-based — Model-based reflex agent

**AIMA 4e §2.4.3.** The same blind vacuum agent as piece 01, with one addition: internal state. It can't sense where it is, so it tracks where it believes it is, learns the walls by bumping into them once, and remembers which squares it has seen clean. Its rules read that state, not the percept. The state is a small JSON file that survives stopping and restarting the cloud sandbox.

**Is the fence needed here? No.** It's a small program we wrote and read, with no network and no secrets. What changes is what's at stake inside the sandbox: the agent's memory now lives there.

- `agent/programs.py` — the agent: its state, the transition and sensor models, and the rules
- `agent/run.py` — the scenarios. Runs in one go, or stops at a step and resumes from the saved state, and both routes write the same `out/results.json`, byte for byte.
- `tests/` — unit tests, run on the host (`make test`) and inside the sandbox (`run.sh`)
- `run.sh` — tests and half a sweep, stop, restart, the other half, via `scripts/sbx-run.sh`
- `policy.md` — network policy, and why

## Reproduce it

- **Commands:** `make login`, then `make run-02` (runs `examples/02-model-based/run.sh`)
- **Check it:** `make compare-02` runs the program in one go on the host, and in two halves in a cloud sandbox, stopped and restarted in between. Expect `compare: identical`, and a `results.json` sha256 starting `aee06cc3`.
- **Needs:** `sbx` signed in to Docker with cloud sandboxes enabled (`make check-env` says "Tier C (cloud) ready: yes")
- **Sandbox:** cloud, agent `shell`, image `docker/sandbox-templates:shell-docker`, 1 vCPU / 2 GiB, TTL 30m with delete on timeout, no egress
- **Verified with:** `sbx v0.50.0 (2026-10-31)`
- **Local sandboxes:** not yet. The author's laptop is too old to run them (ADR-0010).

## Reference run

Cloud, 2026-10-31T17:45:13Z, commit `a660c56`, clean tree, Python 3.14.4 in the sandbox, exit code 0, 57 s from creation to copy-out, 44 s of which were spent waiting for the sandbox to reach `stopped` (`make compare-02`). `results.json` sha256 `aee06cc3e9d7d200…`, identical to one-go host runs on Python 3.12.3 and 3.14.2.

- `two-squares`, location sensor off, starting on B: score 18/20, all clean at step 3, where piece 01's blind agent scored 10/20 and looped forever
- `grid-model`, 4×4, location sensor off: score 2918/3200, all clean at step 34, four bumps, stopped and restarted at step 18
- `grid-amnesia`, the same sweep with the state wiped at step 18: score 2830/3200, all clean at step 45

For comparison, on the same grid piece 01's random agent scored 2666/3200 and finished at step 82, and its blind agent scored 788/3200 and never finished.

## Charts

`make plots-02` draws two figures from the last recorded runs of pieces 02 and 01 into `articles/02-model-based/assets/`, plus `plots.json`, which records the runs they came from.

- `fig-sweep.png`: the sweep with its state kept, and with its state lost at step 18.
- `fig-performance.png`: clean squares over time, against piece 01's agents in grey.
