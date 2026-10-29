---
description: Summarize where the series stands and propose the next step
---

Report project status (CLAUDE.md §9.4). Reply in English.

(Named `series-status`, not `status`: Claude Code's built-in `/status` takes precedence over a project command with that name.)

1. Read `site/_data/series.yml`, `site/_data/metrics.yml` and the journal entry in `site/journal/` with the highest session number.
2. List the open decisions in CLAUDE.md §12 that have no ADR in `site/decisions/` yet.
3. Run `sbx --cloud ls` (read-only). If `sbx` is missing or not signed in, say so instead.
4. Answer in at most ten bullets: the status of each article and example, the outcome of the last session, open decisions, live cloud sandboxes.
5. Propose one next step and say why it comes first.

Change no files.
