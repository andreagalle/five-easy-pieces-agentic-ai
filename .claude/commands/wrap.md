---
description: End the session - journal, prompts, decisions, data, references, checks, cloud check, commit, push and PR
argument-hint: "[short slug for the journal file name]"
---

Close the current working session (CLAUDE.md §0.2, §0.7, §9). Write everything in English. Each step says why it exists: skip none of them, because the record is what the site and article 06 are made of.

**The journal**

1. Create the entry with `scripts/new-journal.sh <slug>`. Use `$ARGUMENTS` as the slug, or pick a short kebab-case one.
2. Fill in every section of the §9.1 template from this session's actual work and `git log`, including the dead ends: they're the best material for article 06. If the author prompted in another language, add "(translated from <language>)" to the Goal. Use they/them for the author. Never write names, employers, secrets or account IDs.
3. Fill in `model` with the model Claude Code reports, and `sandbox_runs` with the real counts, CI runs included.

**What else this session changed**

4. **Prompts (§9.2).** Did any of the author's prompts change the direction of the work: a decision, a new rule, a change of tone, scope or process? If so, record each one in `site/prompts/YYYY-MM-DD-NN-<slug>.md`, with one line of context, the prompt in English (faithfully translated, marked "(translated from Italian)"), why it mattered, and a link to the journal entry. Be selective: most prompts don't qualify. Where a prompt names or judges a third party, replace those words with a neutral phrase in [brackets]. *Why:* sessions 04–08 skipped this step, and the records had to be recovered after the fact.
5. **Decisions (§0.8, §9.2).** Every decision taken this session has an ADR. If it changes a rule, CLAUDE.md says so and points to the ADR, and §12 is current. *Why:* a decision that exists only in the chat is lost at the next session.
6. **Status:** update `site/_data/series.yml` (`status`, `code_tag`, `medium_url`, `last_session` for every item touched), and keep each article's front matter in step with it.
7. **Metrics:** update `site/_data/metrics.yml` with real numbers only:
   - count the commits *after* the wrap's own commits;
   - include cloud runs from CI;
   - add OpenRouter spend from `illustrations/log.jsonl` and any LLM runs;
   - add the prompts recorded.
8. **References (§2, §5.5).**
   - Direct quotes used → `references/aima-ch2-map.md`.
   - New sources → `references/bibliography.md`.
   - New `sbx` facts, version bumps or docs discrepancies → `references/sbx-notes.md`.
   - A new reference run → that example's README.

   *Why:* an article must never cite something the record doesn't know about.
9. **Workflow page:** refresh the "Current state" section of `site/workflow.md` every session. If the workflow itself changed, update the page and its diagram too, and say so in the journal.
10. **README:** if the project's state changed, update the status line.
11. **Badges:** check the backlog in CLAUDE.md §9.3. Add any badge whose trigger has happened, tick it, and mention it in the journal.

**Checks, cleanup, delivery**

12. Run `make test` (if examples changed), `make lint`, `make article-check` and `make site-check`, and fix whatever they report. *Why:* a session must not end on a broken commit.
13. Run `sbx --cloud ls` and report every sandbox still alive (name, age, TTL). Don't remove anything without asking.
14. Commit the record separately from the code. The journal entry gets its own commit, `journal: session NN`.
15. Push `dev`, then open the pull request to `master` or update its title and body to cover this session. Wait for CI and report its result. Never merge: merging is the author's call.
