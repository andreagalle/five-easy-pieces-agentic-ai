---
description: Verify every sbx command used by an article or example against the installed CLI and the docs
argument-hint: "<article-or-example path, e.g. articles/01-simple-reflex or examples/03-goal-based>"
---

Run the verification protocol in CLAUDE.md §5.5 on `$ARGUMENTS`.

1. Record `sbx version`.
2. Collect every `sbx` invocation in `$ARGUMENTS`, plus the scripts it calls (`run.sh` → `scripts/sbx-run.sh`). List each subcommand and flag, separating local from `--cloud`.
3. For each one, run `sbx [--cloud] <command> --help` and confirm that the subcommand and every flag exist with the meaning the text assumes.
4. Cross-check the docs at https://docs.docker.com/ai/sandboxes/ (raw Markdown: append `.md`) and the release notes since the last verified version at https://github.com/docker/sbx-releases/releases.
5. Where docs and `--help` disagree, trust `--help`, then note the discrepancy in `references/sbx-notes.md` and in the journal.
6. Report a table: command, local/cloud, verified yes/no, notes. Propose fixes, but don't apply them without asking.
7. Once everything passes, set `verified_with: "sbx vX.Y.Z (YYYY-MM-DD)"` in the article front matter or the example README.
