---
layout: post
title: "Session 05 — Real sandboxes in CI, charts from real runs, and how to publish"
date: 2026-10-27
session: "05"
pieces: ["00", "01"]
sbx_version: "v0.50.0"
model: "claude-opus-5-5 (Claude Opus 5.5)"
sandbox_runs: { cloud: 3, local: 0 }
---

## Goal

The author's requests (translated from Italian):

- **Sandboxes in CI:** the author brought the cloud rates from their Docker Console and asked to add sandboxes to CI. Pieces 03–05 must not spend OpenRouter credit there: use a fake model, or no token at all, and say so explicitly. Add a job time limit and a final cleanup check.
- **Secrets:** what's the difference between repository and environment secrets for Actions?
- **The article check:** clarify whether the "problems" it listed were real.
- **Publishing:** how will the hub and piece 01 be published?
- **Charts:** add charts to the articles (matplotlib, trajectories, heatmaps, comparisons between agents and their results), right away.

## What we did

- **[ADR-0014]({{ "/decisions/ADR-0014-sandboxes-in-ci/" | relative_url }}) and `.github/workflows/sandbox.yml`** (`0bea0ab`, `47b203c`). After each merge to `master` that touches an example, and on demand, CI:
  - installs the same pinned `sbx` as the Codespace (`scripts/install-sbx.sh`, now shared);
  - signs in from the `cloud-sandboxes` environment;
  - runs `make compare-01`, which runs the program on the runner and in a cloud sandbox and fails unless both `results.json` files are byte-identical;
  - keeps `RUNINFO.json` as an artifact.

  Guards: a 15-minute job timeout, a 10-minute sandbox TTL (so the sandbox deletes itself even if the runner dies), a final check for leftovers, and no overlapping runs. Pieces 03–05 will run there against a fake model, with no OpenRouter key in CI at all. `make lint` gained `actionlint`, because `sandbox.yml` only ever runs after a merge.
- **The cloud rates**, as the author read them in the Console, are recorded in `references/sbx-notes.md`. One run of piece 01 costs about $0.0002–0.0003.
- **Charts** (`404afc4`, `ead7a3f`, `795ffb8`, `5fcfacf`):
  - The shared world now records each step's location and clean count, and piece 01's `results.json` carries them.
  - `scripts/plots.py` (`make plots-01`, matplotlib 3.11.2 in a git-ignored `.venv`) draws four figures from the reference cloud run: position over time in the two-square world; paths on the 4×4 grid; the step at which each square was first cleaned; and clean squares over time, whose area is AIMA's score.
  - The palette comes from the illustrations and was validated with the dataviz checks. Coral is the agent that loops, cerulean every agent that works.
  - Every footer names its run, and `plots.json` records it.
- **A new reference run of piece 01** at `795ffb8`: clean tree, 10 s, the same `results.json` on Python 3.12.3, 3.14.2 and 3.14.4 (sha256 `efae1944…`). The scores are unchanged.
- **`articles/PUBLISHING.md`** (`c324a0a`): readiness in the repository, the paste into Medium, the order for the hub and piece 01, and the record afterwards.

## Commands that mattered

From the `Makefile`:

```bash
make compare-01   # piece 01 on the host and in a cloud sandbox; fails unless results.json matches
make plots-01     # piece 01's charts from its last recorded run
make lint         # shellcheck, actionlint, py_compile
```

## Decisions

- [ADR-0014 — Real cloud sandboxes in CI, after merges]({{ "/decisions/ADR-0014-sandboxes-in-ci/" | relative_url }})
- **Chart conventions,** in CLAUDE.md §3.3: palette, colour follows the agent, emphasis rather than more hues for comparisons across pieces, provenance on every figure.

## Dead ends and surprises

- **Docker's rates aren't in its docs.** The docs describe per-second billing by size but not the prices, which only the Console shows. The author read them there. The price doubles with each size, exactly like the resources. Billed time was 31.277 s against about 41 s of client wall clock: the meter counts sandbox runtime, not the time spent creating, copying and removing.
- **Medium's API is closed to new users**, since 1 January 2025. Publishing will be a paste, so the checklist has to be precise.
- **A third colour wasn't possible.** With cerulean and coral fixed, no third hue from the brand passed the "every pair against every pair" checks. The dataviz method's answer is emphasis: in comparisons across pieces, the piece's own agent in colour, the others in grey.
- **The first teal ramp failed** the light-end contrast check (1.32:1 on white). It was darkened until the lightest step reached 2.07:1.
- **A reference run marked dirty.** The first new reference run recorded `git_dirty: true`, because an uncommitted change sat in `scripts/`. The commit came first, and the run was repeated, so the charts point to a clean commit.
- **Three layout problems found by looking, not by any check:**
  - a subtitle running off the figure;
  - a label spilling into the next panel;
  - a colorbar label on top of the footer.

  The dataviz method says to render and look; the colour validator can't see overlaps.
- **The scratchpad vanished between sessions,** and Docker then created the output folder as `root`, so the site build failed silently. The fix: always create the folder before mounting it.
- **`shellcheck` flagged `A && B || C`** in the new comparison script. It isn't an if-then-else, so it became one.

## Who did what

- **The author:** brought the cloud rates; decided on sandboxes in CI, with a fake model for the LLM pieces; asked for the charts; and is setting up the `cloud-sandboxes` environment.
- **Claude:** wrote ADR-0014, the workflow, the shared installer and the comparison script; extended the world's records; designed, validated and drew the charts; wrote the publishing checklist and this entry.

## Next

1. **The author:** create the `cloud-sandboxes` environment, limited to `master`, with `DOCKER_ID` and `DOCKER_PAT`, before merging this session's PR. Its merge touches `examples/` and starts the first `sandbox.yml` run.
2. **The author:** review the hub draft and send comments.
3. **Draft piece 01,** using two or three of its four charts. Then the hub and 01 follow `articles/PUBLISHING.md`.
