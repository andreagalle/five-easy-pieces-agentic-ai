---
description: End the session - journal entry, series and metrics update, cloud check, commit
argument-hint: "[short slug for the journal file name]"
---

Close the current working session (CLAUDE.md §0.2, §0.7, §9). Write everything in English.

1. Create the entry with `scripts/new-journal.sh <slug>`. Use `$ARGUMENTS` as the slug, or pick a short kebab-case one.
2. Fill in every section of the §9.1 template from this session's actual work and `git log`. Include the dead ends. If the author prompted in another language, add "(translated from <language>)" to the Goal. Use they/them for the author. Never write names, employers, secrets or account IDs.
3. Fill in `model` with the model Claude Code reports and `sandbox_runs` with the real counts.
4. Update `site/_data/series.yml`: `status`, `code_tag`, `medium_url` and `last_session` for every item touched.
5. Update `site/_data/metrics.yml` with real numbers only.
6. If the workflow changed, update `site/workflow.md` and say so in the journal.
7. Run `make site-check` and fix whatever it reports.
8. Run `sbx --cloud ls` and report every sandbox still alive (name, age, TTL). Don't remove anything without asking.
9. Commit the record changes separately from code. The journal entry gets its own commit, `journal: session NN`. Show the commit list to the author.
