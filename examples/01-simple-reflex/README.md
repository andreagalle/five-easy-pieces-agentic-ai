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
- **Needs:** `sbx` signed in to Docker with cloud sandboxes enabled (`make check-env` says "Tier C (cloud) ready: yes")
- **Sandbox:** cloud, agent `shell`, image `docker/sandbox-templates:shell-docker`, 1 vCPU / 2 GiB, TTL 30m with delete on timeout, no egress
- **Verified with:** `sbx v0.50.0 (2026-10-26)`
- **Local sandboxes:** a locally tested version will follow once the author has a capable machine. It isn't published until it has been run (ADR-0010).

## Reference run

Cloud, 2026-10-26T21:40:47Z, commit `09759d7`, clean tree, Python 3.14.4 in the sandbox, exit code 0, 10 s from creation to copy-out. `results.json` sha256 `9fbec0343e22d499…`, identical to host runs on Python 3.12.3 and 3.14.2.

- `sighted`, two squares, location sensor on: score 18/20, all clean at step 3
- `blind`, two squares, no location sensor: score 10/20, square A dirty forever
- `blind-random`, two squares, coin flip on clean squares: score 18/20, all clean at step 3
- `grid-blind`, 4×4, no location sensor: score 788/3200, 12 squares still dirty after 200 steps
- `grid-random`, 4×4, random move on clean squares: score 2666/3200, all clean at step 82

Score is AIMA's performance measure: one point per clean square per time step.
