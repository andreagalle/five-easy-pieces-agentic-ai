---
title: "ADR-0014 — Real cloud sandboxes in CI, after merges"
adr: "0014"
status: accepted
date: 2026-10-27
---

**Status:** accepted, 2026-10-27. Decided by the author in session 05; CLAUDE.md §5.2 requires an ADR before sandboxes run in CI.

## Context

Until now CI ran only host-side checks. The series' central claim, that the architecture doesn't change the program, had been checked by hand in the Codespace. The author wanted real sandboxes in CI and asked what that would cost.

The facts:

- **GitHub:** Actions on GitHub's standard runners are free for public repositories.
- **Docker:** cloud sandboxes are billed by the second of runtime, at a rate that depends on the size. There's no subscription fee. The rates come from the author's Agentic Platform Console on 2026-10-27; the docs don't publish them:
  - micro: $0.00001944/s, about $0.07 per hour
  - small: $0.00003889/s, about $0.14 per hour
  - medium: $0.00007778/s, about $0.28 per hour
  - large: $0.00015556/s, about $0.56 per hour
  - xl: $0.00031111/s, about $1.12 per hour
- **Our usage:** a run of piece 01 lasts 10–17 s on micro (from `RUNINFO.json`), about **$0.0002–0.0003 per run**.
- **The other cost:** pieces 03–05 will call a model through OpenRouter. Each real call spends the author's OpenRouter credit, which is capped at $5 on the key.

## Options considered

1. **No sandboxes in CI.** Free, but the central claim is checked only when someone remembers to.
2. **Sandboxes on every push and pull request.** Maximum coverage, but pull requests are where untrusted changes arrive, and the Docker credentials would be exposed to more of them.
3. **Sandboxes after each merge and on demand.** Deterministic pieces for real; LLM pieces with a fake model and no OpenRouter key.

## Decision

Option 3, in `.github/workflows/sandbox.yml`:

- **When:** after each push to `master` that touches `examples/`, the wrapper or the workflow itself, plus a manual "Run workflow" button. **Never on pull requests.**
- **What:** for each deterministic piece (01 now, 02 next), `make compare-NN` runs the program on the runner and in a cloud sandbox, and fails unless the two `results.json` files are byte-identical. `RUNINFO.json`, `results.json` and `stdout.txt` are kept as a downloadable artifact.
- **LLM pieces (03–05), once they exist:** they run in CI against a **fake model**, a scripted stand-in with deterministic answers. **CI holds no OpenRouter key at all**, so no CI run can spend model credit, even by mistake. A probe without a key checks the network policy: `openrouter.ai` is reachable (its public model list answers without authentication), and any other host is blocked. CI therefore tests everything except the real model call. The workflow, the piece's README and the article all say so explicitly.
- **Credentials:** `DOCKER_ID` and `DOCKER_PAT` are **environment secrets** of an environment called `cloud-sandboxes`, whose deployment branches are restricted to `master`. Why an environment rather than repository secrets: only a job that declares that environment, running on `master`, can read them. A workflow edited on another branch can't. Ideally the PAT is a dedicated token for CI, so it can be revoked without touching the Codespace's.
- **Guards against leftovers:**
  - The job times out after 15 minutes.
  - The sandbox's TTL in CI is 10 minutes, shorter than the job's timeout, with delete on expiry. If the runner dies before the wrapper's exit trap runs, the sandbox deletes itself anyway.
  - A final step removes this run's sandbox if it's still alive, then lists everything.
  - Runs never overlap.

## Consequences

- Every merge that touches an example re-proves "identical on the host and in the cloud" for a fraction of a cent.
- The scripts that install `sbx` and compare runs are shared with the Codespace (`scripts/install-sbx.sh`, `scripts/compare-host-cloud.sh`), so CI and the author run the same thing.
- The author creates the `cloud-sandboxes` environment and its two secrets once (Settings → Environments).
- Pieces 03–05 must be built with a fake-model switch from the start.
- The README gains a badge for this workflow once it has passed on `master` (CLAUDE.md §9.3).
