# Bibliography

Full references for the series. Citation and quoting rules: CLAUDE.md §2.

## Primary

- Russell, S. & Norvig, P. *Artificial Intelligence: A Modern Approach*, 4th ed. Pearson. Chapter 2, "Intelligent Agents".
  - **Reference used in the articles (ADR-0015):** Stuart Russell and Peter Norvig, *Artificial Intelligence: A Modern Approach*, 4th edition (US). Pearson, 2020. ISBN 978-0-13-461099-3. The overture opens with it; the pieces cite it as *(AIMA 4e, §2.x)*.
  - The 4th edition exists as the US edition (Pearson, 2020, ISBN 978-0134610993) and a Global Edition (ISBN 9781292401133), per the authors' [list of editions and translations](https://people.eecs.berkeley.edu/~russell/aima/translations.html).
  - **The author's copy:** the Italian translation of the 4th edition, *Intelligenza artificiale. Un approccio moderno*, Pearson Italia, ed. Francesco Amigoni, ISBN-10 8891904457 (ISBN-13 9788891904454). Library catalogs record it in two volumes, 2021 and 2022. The sources we checked don't say whether it was translated from the US or the Global Edition.
  - **Consequence (ADR-0012):** section numbers are checked against the Italian copy. Direct quotes are used only if verified against an English 4th-edition text; otherwise we paraphrase.

## Secondary sources

None. Third-party study notes on the book are deliberately not cited (ADR-0015): their rights status is unclear, and the book itself is the reference.

## Optional code reference

- AIMA code repositories on GitHub, <https://github.com/aimacode>. Check each repository's license before reusing anything; the series writes its own code.

## Other works mentioned

- Feynman, R. P. *Six Easy Pieces: Essentials of Physics Explained by Its Most Brilliant Teacher*. Addison-Wesley. Catalogs date the book 1995, some 1994. Its six chapters come from *The Feynman Lectures on Physics* (early 1960s). The series title nods to it (CLAUDE.md §3.2). The overture says "mid-1990s" because the sources disagree on the year.

## Docker Sandboxes

- Docker Sandboxes documentation, <https://docs.docker.com/ai/sandboxes/>. Raw Markdown: append `.md` to a page URL (see `sbx-notes.md` for one exception).
- `sbx` release notes, <https://github.com/docker/sbx-releases/releases>.

## Claude Code

- Development containers, <https://code.claude.com/docs/en/devcontainer>, the source for the Claude Code devcontainer feature used in `.devcontainer/devcontainer.json`.
