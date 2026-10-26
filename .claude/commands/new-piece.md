---
description: Scaffold an article and its example from the CLAUDE.md skeletons
argument-hint: "<NN, e.g. 03>"
---

Scaffold piece `$ARGUMENTS` (CLAUDE.md §3.4, §4).

1. Locate `articles/$ARGUMENTS-*/` and `examples/$ARGUMENTS-*/`. Both directories already exist as placeholders, so don't rename them.
2. In `article.md`, keep the front matter and add the nine §3.4 sections as `##` headings, each with a one-line note on what goes there. Write no prose yet. Articles describe runs that have happened (§10.3).
3. In the example directory, create `agent/__init__.py`, `policy.md` (default: no egress, and why) and `run.sh` as a thin wrapper around `scripts/sbx-run.sh`. If `scripts/sbx-run.sh` doesn't exist yet, stop and say so. Add `tests/` together with the first real code, not as an empty placeholder: `make test` must stay green in CI.
4. Create no `agent_llm/` unless the ADR for decision D2 says yes.
5. Update `site/_data/series.yml` (status `outline` for the article, `scaffolded` for the example).
6. Run `make test` and report the result.
