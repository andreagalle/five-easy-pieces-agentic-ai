# 01-simple-reflex — Simple reflex agent

**AIMA 4e §2.4.2.** A simple reflex agent picks its action from the current percept alone, through condition–action rules. It remembers nothing.

- **What it shows:** AIMA's two-square vacuum agent works when it can sense its location. Take the location sensor away and the same rules loop forever. A coin flip gets it out of the loop, but on a 4×4 grid a random walk needs 82 steps to finish the job. That cost is what piece 02's internal state will remove.
- **LLM: no.** The lesson is one rule and its loop, and you can point at the line responsible. A model would hide it (ADR-0011).
- **Sandbox feature: disposability.** Create, copy in, run, copy out, delete, with the network fully blocked ([`policy.md`](policy.md)).
- **Is the fence needed? No.** It's a trusted 40-line standard-library program with no network and no secrets. We sandbox it anyway, to learn the mechanics where nothing can go wrong, and to show that the architecture doesn't change the program: the output is byte-identical on the host and in the cloud.

## Files

- `agent/programs.py` — the three agent programs (sighted, blind, randomized)
- `agent/run.py` — the five scenarios. Writes a deterministic `out/results.json`: no timestamps or machine details, so runs compare byte for byte.
- `tests/` — unit tests, run on the host (`make test`) and inside the sandbox (`run.sh`)
- `run.sh` — runs the tests and then the scenarios in a cloud sandbox via `scripts/sbx-run.sh`
- `policy.md` — network policy, and why

## Reproduce it

- **Command:** `make run-01` (runs `examples/01-simple-reflex/run.sh`)
- **Needs:** `sbx` signed in to Docker with cloud sandboxes enabled: `make login`, which is headless with the `DOCKER_ID` and `DOCKER_PAT` secrets and runs on its own when a Codespace is created with them. `make check-env` should say "Tier C (cloud) ready: yes".
- **Sandbox:** cloud, agent `shell`, image `docker/sandbox-templates:shell-docker`, 1 vCPU / 2 GiB, TTL 30m with delete on timeout, no egress
- **Verified with:** `sbx v0.50.0 (2026-10-29)`
- **Local sandboxes:** not yet. The author's laptop is too old to run them, so a locally tested version will follow once the author has bought a new one. Thankfully, cloud sandboxes need nothing from the laptop but a browser or a terminal. Nothing is published until it has been run (ADR-0010).

## Reference run

Cloud, 2026-10-27T16:12:51Z, commit `795ffb8`, clean tree, Python 3.14.4 in the sandbox, exit code 0, 10 s from creation to copy-out (`make compare-01`). `results.json` sha256 `efae1944bf22a1d4…`, identical to host runs on Python 3.12.3 and 3.14.2. Since session 05, `results.json` also records each step's location and clean count, for the charts. The scores are unchanged from the first reference run (`09759d7`, sha256 `9fbec034…`).

- `sighted`, two squares, location sensor on: score 18/20, all clean at step 3
- `blind`, two squares, no location sensor: score 10/20, square A dirty forever
- `blind-random`, two squares, coin flip on clean squares: score 18/20, all clean at step 3
- `grid-blind`, 4×4, no location sensor: score 788/3200, 12 squares still dirty after 200 steps
- `grid-random`, 4×4, random move on clean squares: score 2666/3200, all clean at step 82

Score is AIMA's performance measure: one point per clean square per time step.

Rerun by the author on 2026-10-29 with `make compare-01`, at commit `c650564`: the same sha256 on the host (Python 3.14.2) and in the cloud (3.14.4), exit code 0, 13 s, and `sbx --cloud ls` empty afterwards.

## Charts

`make plots-01` draws four figures from the last recorded run into `articles/01-simple-reflex/assets/`, plus `plots.json`, which records the run they came from. Every figure's footer names that run.

- `fig-two-squares.png`: where each two-square agent is, step by step. The blind one is a flat line.
- `fig-grid-paths.png`: where the blind and the random agent went on the 4×4 grid.
- `fig-grid-cleaned-at.png`: the step at which each square was first cleaned, or never.
- `fig-grid-performance.png`: clean squares over time. Each score is the area under its line.
