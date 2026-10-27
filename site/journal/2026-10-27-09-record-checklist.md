---
layout: post
title: "Session 09 — The record gets a checklist"
date: 2026-10-27
session: "09"
pieces: []
sbx_version: "v0.50.0"
model: "claude-opus-5-5 (Claude Opus 5.5)"
sandbox_runs: { cloud: 0, local: 0 }
---

## Goal

The author asked why the site's prompts page had stopped growing after session 03 (translated from Italian). After the answer, they asked to:

- recover the missing prompts;
- check whether anything else was missing from `/wrap`;
- keep the selective rule for prompts as it is.

## What we did

- **Found the cause.** `/wrap` listed the journal, `series.yml`, `metrics.yml`, the workflow page and badges, but not prompts, so from session 04 on nobody asked the question.
- **Recovered six prompts** (`e5c3820`), translated from the author's actual messages in this conversation and marked as recorded after the fact:
  - "Feynman, not the film" (04);
  - "note them down and add them on your own" (04);
  - sandboxes in CI without spending OpenRouter credit (05);
  - charts right away (05);
  - start from the curiosity and cite the book properly (06);
  - "why hub?" (07).

  Where a prompt judged a third party's page, those words were replaced by a neutral phrase in brackets.
- **Extended `/wrap` to cover the whole record** (`4832539`). It now has 15 steps, each with its reason. The new ones:
  - prompts;
  - an ADR for every decision;
  - references (quotes, bibliography, `sbx` notes, reference runs);
  - the workflow page's current state every session;
  - the README status;
  - all four `make` checks;
  - metrics counted after the wrap's own commits, with OpenRouter spend and prompts recorded;
  - push and pull request, waiting for CI.

  CLAUDE.md §9.4 summarizes it.
- **Closed this session with the new checklist.** Its first use recorded this session's own prompt (step 4) and refreshed the workflow page (step 9).

## Commands that mattered

```bash
make site-build   # 39 pages, with the recovered prompts
```

## Decisions

- No ADR. This is a process change, recorded in CLAUDE.md §9.4 and in `.claude/commands/wrap.md`. The author confirmed that prompts stay selective: only those that changed the direction of the work.

## Dead ends and surprises

- **The gap was structural, not a lapse of attention.** Every step `/wrap` listed was done every time. The one it didn't list was never done. The other "missing" steps (references, ADR checks, the workflow page, push and PR) had been done by habit, which is exactly what a checklist is for.
- **The metrics had been off by two once already** (session 04), because the wrap's own commits weren't counted. The checklist now says to count after them.

## Who did what

- **The author:** noticed the gap, asked for the recovery and the review of `/wrap`, and confirmed the selective rule.
- **Claude:** explained the cause, recovered and translated the prompts, rewrote `/wrap`, and closed the session with it.

## Next

1. **The author:** review piece 1.
2. **After review:** create the `piece-01-v1` tag, run `/verify-sbx`, and move the overture and piece 1 to `review`, then `ready`.
3. Publish both, following `articles/PUBLISHING.md`.
