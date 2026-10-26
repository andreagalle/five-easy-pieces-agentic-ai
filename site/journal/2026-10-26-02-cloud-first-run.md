---
layout: post
title: "Session 02 — The plan settles, and piece 01 runs in the cloud"
date: 2026-10-26
session: "02"
pieces: ["01"]
sbx_version: "v0.50.0"
model: "claude-opus-5-5 (Claude Opus 5.5)"
sandbox_runs: { cloud: 3, local: 0 }
---

## Goal

The author answered the questions left open by session 01 and asked to go ahead (translated from Italian):

- **D5:** no Claude Code inside a sandbox, but say so with a joke, and say the honest answer would have been yes.
- **Local tier:** cloud only for now, because the author's laptop can't run local sandboxes yet. Mention the local version; don't publish it untested.
- **D2:** "what would a version without an LLM be good for?" After the explanation: one mode per piece, no LLM at first, and always underline the why.
- **Then:** go ahead with the secrets in place, OpenRouter for the LLM pieces, and a $5 cap.

## What we did

- **Merged session 01.** Pushed `dev` and opened PR #1; the author merged it. The Pages deploy and CI both passed, and the site is live.
- **Recorded three decisions, and why:**
  - ADR-0009, Claude Code stays outside the sandbox. It includes the confession: a series about fencing agents, written by an agent with root.
  - ADR-0010, cloud only until the local tier is tested.
  - ADR-0011, one mode per piece: no LLM in 01–02, LLM via OpenRouter in 03–05, with a $5 credit limit on the key.

  ADR-0004 is superseded and ADR-0002 amended. The new page [The five pieces]({{ "/pieces/" | relative_url }}) says, piece by piece, whether the sandbox is actually needed and why. CLAUDE.md §3.2 gained the rule "Always state the why".
- **Built the shared vacuum world:** an N×M grid with switches for partial observability, slip and dynamic dirt, 10 tests (`1a38b51`). All randomness goes through `Random.random()`, so a run is identical on any Python 3. That choice was made before we knew the sandbox would run Python 3.14, and it paid off.
- **Built example 01:** three agent programs (sighted, blind, coin-flip) and five scenarios writing a deterministic `results.json`, with 4 tests (`c8e4073`).
- **Signed in and probed.** Signed in to Docker headlessly from Codespaces secrets. A probe sandbox checked the facts the wrapper depends on: workspace path, Python 3.14.4 in the `shell` template, `cp` semantics, the network block, the exit-code pass-through and the `inspect` fields. Results are in `references/sbx-notes.md`.
- **Wrote `scripts/sbx-run.sh`** (`74f16fc`): the one wrapper for every example. It runs the cloud tier only, refuses `SBX_TARGET=local` (ADR-0010), and does create → copy in → run → copy out → `RUNINFO.json` → remove, with a trap on exit.
- **Ran example 01 in the cloud twice.** First with the wrapper still uncommitted, to validate it. Then on a clean tree, as the reference run: commit `09759d7`, 10 s, exit code 0. Both times `results.json` was byte-identical to the host runs (sha256 `9fbec034…`): Python 3.12.3 and 3.14.2 on the host, 3.14.4 in the cloud.
- **Wrote the example's README:** what it shows, why no LLM, why a fence it doesn't need, the reproduce box and the reference run.

## Commands that mattered

Sign-in (CLAUDE.md §5.1, `references/sbx-notes.md`):

```bash
printf '%s\n' "$DOCKER_PAT" | sbx login --username "$DOCKER_ID" --password-stdin
```

The run, and the sandbox it creates (from `scripts/sbx-run.sh`):

```bash
make run-01
sbx --cloud create --name "$name" --ttl "$ttl" --on-timeout delete \
  --cpus "$cpus" --memory "$memory" "${network_flags[@]}" --no-progress "$agent"
```

## Decisions

- [ADR-0009 — Claude Code stays outside the sandbox]({{ "/decisions/ADR-0009-claude-code-stays-outside/" | relative_url }}) (D5)
- [ADR-0010 — Cloud only until the local tier is tested]({{ "/decisions/ADR-0010-cloud-only-until-local-is-tested/" | relative_url }})
- [ADR-0011 — One mode per piece]({{ "/decisions/ADR-0011-one-mode-per-piece/" | relative_url }}) (D2; supersedes ADR-0004, amends ADR-0002)

## Dead ends and surprises

- **Secrets created mid-session were invisible.** The author created `DOCKER_ID` and `DOCKER_PAT` as repository Codespaces secrets while the Codespace was running. They only appeared in the environment after a restart. `gh api` showed they existed; the shell didn't.
- **The sandbox runs a different Python from the host:** 3.14.4 in the cloud `shell` template (Ubuntu 26.04), 3.12 on the host. Byte-identical output across them isn't automatic. It holds because the world draws randomness only through `Random.random()`.
- **Docs and CLI disagree about OpenRouter in the cloud.** `--help` lists it as a built-in secret service; the cloud credentials page says to use a custom secret. To be settled at piece 03, the first piece that needs it.
- **"Deny all" looks like a DNS failure.** Inside the sandbox, a blocked request fails at name resolution, not with a "forbidden". Worth one sentence in an article, so readers recognize it.
- **No keychain in the Codespace.** `sbx login` warns that the credential is stored on disk, protected by file permissions. It's under `~/.config/com.docker.sandboxes`, mode 700, outside the repository.
- **Two small mistakes of Claude's, caught by running the code:**
  - A test's expected random sequence was written from memory and was wrong; it was computed and fixed before committing.
  - `unittest discover -t .` needs `tests/__init__.py`.

## Who did what

- The author decided D2 and D5, the cloud-only rule and the $5 cap; created the three Codespaces secrets; restarted the Codespace; and merged PR #1.
- Claude explained the D2 trade-offs; wrote ADR-0009 to ADR-0011, the pieces page, the shared world, example 01, the wrapper and this entry; ran the probe and the cloud runs.

## Next

1. Draft article 01 and an outline of the hub. They are published together (ADR-0007). Before the first citation: the AIMA edition and year from the author's copy, and the wording of the disclosure line.
2. Example 02, model-based reflex: internal state that beats 01's 82-step random walk, and state that survives stopping and restarting the cloud sandbox.
3. Tag `piece-01-v1` when article 01 is ready, and point its links at the tag.
