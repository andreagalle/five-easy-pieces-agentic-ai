---
title: "ADR-0007 — Publication order and cadence"
adr: "0007"
status: accepted
date: 2026-10-26
---

**Status:** accepted, 2026-10-26. Decided by the author (open decision D6) in [session 01]({{ "/journal/2026-10-26-01-bootstrap/" | relative_url }}).

## Context

The hub (00) frames the series and links to every piece. Publishing it alone means a page full of "coming soon" links. Publishing pieces first leaves them without the frame that explains why they belong together.

## Options considered

1. **Hub first**, with "coming soon" links, then the pieces.
2. **All pieces first**, hub last.
3. **Hub and piece 01 together**, then one piece a week, the making-of last.

## Decision

Option 3:

- Week 0: hub (00) and piece 01, the same day.
- Weeks 1–4: pieces 02, 03, 04, 05, one a week.
- Then: the making-of (06), once 05 is out.

## Consequences

- The hub and piece 01 must reach `ready` together, with the `piece-01-v1` tag in place.
- The hub's links to 02–05 say "coming soon" at first. Each is replaced with the Medium URL as that piece is published (tracked in `site/_data/series.yml`).
- Each weekly piece should be `ready`, with its code tagged, before the previous one goes out, so that one late piece doesn't stall the series.
- Article 06 is written last and can cover the whole run of the series.
