# Bibliography

Full references for the series. Citation and quoting rules: CLAUDE.md §2.

## Primary

- Russell, S. & Norvig, P. *Artificial Intelligence: A Modern Approach*, 4th ed. Pearson. Chapter 2, "Intelligent Agents".
  - **Cited as** *(AIMA 4e, §2.x)*. The 4th edition exists as the US edition (Pearson, 2020, ISBN 978-0134610993) and a Global Edition (ISBN 9781292401133), per the authors' [list of editions and translations](https://people.eecs.berkeley.edu/~russell/aima/translations.html).
  - **The author's copy:** the Italian translation of the 4th edition, *Intelligenza artificiale. Un approccio moderno*, Pearson Italia, ed. Francesco Amigoni, ISBN-10 8891904457 (ISBN-13 9788891904454). Library catalogs record it in two volumes, 2021 and 2022. The sources we checked don't say whether it was translated from the US or the Global Edition.
  - **Consequence (ADR-0012):** section numbers are checked against the Italian copy. Direct quotes are used only if verified against an English 4th-edition text; otherwise we paraphrase.

## Secondary (linked from the hub as a free summary)

- Z. Yu, "Chapter 2 Intelligent Agents", *ArtificialIntelligence* notes on Read the Docs, 2021. <https://artificialintelligence.readthedocs.io/en/latest/part1/chap2.html> (HTTP 200 on 2026-10-26).
  - Study notes on the book, not the book: cite AIMA for ideas, link the notes for convenience.
  - The notes' table of contents skips §2.4.4 (goal-based agents). The text is on the page but has no anchor: link to the page and write "§2.4.4" in prose.

## Optional code reference

- AIMA code repositories on GitHub, <https://github.com/aimacode>. Check each repository's license before reusing anything; the series writes its own code.

## Other works mentioned

- Feynman, R. P. *Six Easy Pieces: Essentials of Physics Explained by Its Most Brilliant Teacher*. Addison-Wesley. Catalogs date the book 1995, some 1994. Its six chapters come from *The Feynman Lectures on Physics* (early 1960s). The series title nods to it (CLAUDE.md §3.2). The hub says "mid-1990s" because the sources disagree on the year.

## Docker Sandboxes

- Docker Sandboxes documentation, <https://docs.docker.com/ai/sandboxes/>. Raw Markdown: append `.md` to a page URL (see `sbx-notes.md` for one exception).
- `sbx` release notes, <https://github.com/docker/sbx-releases/releases>.

## Claude Code

- Development containers, <https://code.claude.com/docs/en/devcontainer>, the source for the Claude Code devcontainer feature used in `.devcontainer/devcontainer.json`.
