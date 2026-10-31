---
layout: post
title: "Session 13 — The overture and piece 1 are on Medium"
date: 2026-10-31
session: "13"
pieces: ["00", "01"]
sbx_version: "v0.50.0"
model: "claude-opus-5-5 (Claude Opus 5.5)"
sandbox_runs: { cloud: 0, local: 0 }
---

## Goal

After merging PR #10, the author published the two articles by following `articles/PUBLISHING.md`, and asked Claude to do everything else (translated from Italian). During the publication they asked two quick questions: whether `status: ready` was right, given that the checklist's first step says `review`, and why `fig-grid-paths.png` isn't in piece 1.

## What we did

- **The `piece-01-v1` tag** (annotated, on `d8687ce`, the merge of PR #10). It's the state in which a fresh Codespace passes everything, `make lint` included.
- **A check of every link in both articles** while the author was publishing. All ten external links returned 200, and all the images exist. The site had already redeployed from `d8687ce`.
- **The author published** piece 1, then the overture, in Docker Captains Wisdom, by 2026-10-31:
  - [Five Easy Pieces on Agentic AI w/ Docker Sandboxes](https://medium.com/docker-captains-wisdom/five-easy-pieces-on-agentic-ai-w-docker-sandboxes-53d5acb6e2e4)
  - [Piece 1/5 — The simple reflex agent](https://medium.com/docker-captains-wisdom/piece-1-5-the-simple-reflex-agent-b34c17054a7b)
- **The repository follows Medium:** both articles are `published`, with their URLs. Their series lists carry the links, example 1 is `frozen` at the tag, and the README links both articles. The site's Home page turns `medium_url` into links by itself.
- **Two badges from the CLAUDE.md §9.3 backlog:**
  - "Latest tag" (`25500c3`). It sorts by date, because the tags aren't semver.
  - "Articles published 2/7". shields.io can read a value from a YAML file but can't count, so `series.yml` gained a `published: "N/7"` field, and `make site-check` fails if it disagrees with the statuses (`0a10cb0`). Tested with a correct value, a wrong one and a missing field.
- **`articles/PUBLISHING.md`:**
  - Step 1 now says `review` comes first and step 6 moves the article on to `ready`, after the author's question.
  - Step 4 now mentions the published count and the repository's own series lists, which this first publication showed were missing.
- **The metrics catch up:** `sandbox.yml` had run after the merges of PRs #8 and #9 (11 s and 10 s, both identical), and neither run had been counted.

## Commands that mattered

From the `Makefile`, and the check behind the new badge:

```bash
make article-check   # both articles at status published
make site-check      # fails if published: "N/7" disagrees with the statuses
```

## Decisions

- No ADR. The publication follows ADR-0007 and ADR-0008. The `published` field implements a badge already agreed in CLAUDE.md §9.3.
- **`fig-grid-paths.png` stays out of piece 1.** The author asked why it wasn't used, heard the reason and chose to leave the article as it is. The chart stays in the repository.

## Dead ends and surprises

- **The checklist had a confusing first step.** "The front matter says `status: review`" read as if `ready` were wrong, and the author stopped to ask mid-publication. A checklist is tested only when someone follows it for real.
- **No recorded reason for leaving out a chart.** Session 08 used three of the four charts and didn't say why this one went. The answer to the author had to be reconstructed, and was given as such: it mostly repeats the heatmap, which also says when.
- **Nothing here can read the published pages.** Medium's Cloudflare answers 403 to scripts. So the URLs are recorded as the author sent them, and the links on Medium weren't checked from here.
- **A heredoc inside a heredoc.** A script for `site-check` ended early, because both used the same delimiter. Nothing was written, and the edit went through the editor instead.

## Who did what

- **The author:** merged PR #10, published both articles, chose to leave the chart out, and sent the URLs.
- **Claude:** created the tag, checked the links, added the badges and the `published` check, updated the repository to match Medium, and closed the session.

## Next

1. **Example 2, the model-based reflex agent:** internal state, and a run where that state survives stopping and restarting the cloud sandbox.
2. **Draft piece 2.** The series goes out one piece a week (ADR-0007).
3. **The author:** check that the two series links work on Medium, since nothing here can read those pages.
