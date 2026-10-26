---
title: "ADR-0008 — Publish in the Docker Captains Wisdom publication"
adr: "0008"
status: accepted
date: 2026-10-26
---

**Status:** accepted, 2026-10-26. Decided by the author (open decision D7) in [session 01]({{ "/journal/2026-10-26-01-bootstrap/" | relative_url }}).

## Context

Medium articles can go out on the author's own profile or inside a publication. A publication brings its readers and its conventions.

## Options considered

1. The author's own Medium profile.
2. A Medium publication.

## Decision

Option 2: all seven articles are published in **Docker Captains Wisdom**, <https://medium.com/docker-captains-wisdom>.

## Consequences

- Every `medium_url` in `site/_data/series.yml` will point under `medium.com/docker-captains-wisdom/`.
- Before the first article goes out, check the publication's own formatting conventions (tags, cover image, subtitle) against the Medium constraints in CLAUDE.md §3.3.
- The disclosure line (CLAUDE.md §3.2) is still an open author decision. The publication's name refers to Docker's community program and the series features a Docker product, so the wording should settle whether that relationship is disclosed.
