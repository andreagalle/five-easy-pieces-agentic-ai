---
title: "ADR-0012 — AIMA edition: cite the 4th edition, read in Italian, paraphrase"
adr: "0012"
status: accepted
date: 2026-10-26
---

**Status:** accepted, 2026-10-26. Based on the author's answer in session 03 about their copy of AIMA (CLAUDE.md §2.1). Amended by [ADR-0015]({{ "/decisions/ADR-0015-cite-the-book-not-the-notes/" | relative_url }}): the hub opens with the full US reference, and the US/Global sentence moves out of the article into the bibliography.

## Context

The series rests on Chapter 2 of Russell & Norvig, *Artificial Intelligence: A Modern Approach*. CLAUDE.md asks to confirm the edition against the author's copy before the first citation. The author reads the **Italian translation of the 4th edition**: *Intelligenza artificiale. Un approccio moderno*, Pearson Italia, edited by Francesco Amigoni, ISBN-10 8891904457.

What the sources say:

- The 4th edition exists as the **US edition** (Pearson, 2020, ISBN 978-0134610993) and a **Global Edition** (ISBN 9781292401133), per the authors' own [list of editions and translations](https://people.eecs.berkeley.edu/~russell/aima/translations.html). That list doesn't yet include the Italian 4th edition.
- A university library catalog (Sapienza, Rome) records the Italian 4th edition as Pearson Italia, two volumes, 2021 and 2022.
- None of the sources we checked says whether the Italian translation was made from the US or the Global Edition.

The series is written in English, so a direct quotation would have to come from the English text, which the author's Italian copy can't confirm. Translating the Italian back into English and calling it a quote would put words in the authors' mouths.

## Options considered

1. Cite the Italian edition and translate quotes ourselves.
2. Cite the English 4th edition, check section numbers against the Italian copy, and paraphrase instead of quoting.
3. Get an English copy before writing.

## Decision

Option 2, stated openly:

- Articles cite **AIMA 4th edition (Pearson, 2020)** by section number, e.g. *(AIMA 4e, §2.4.2)*.
- Section numbers are checked against the author's Italian copy.
- **Paraphrase only.** A direct quotation appears only if it has been checked against an English 4th-edition text. Without that check, we paraphrase. CLAUDE.md §2.2 already prefers paraphrase; this makes it a rule.
- The hub states this once, in one sentence: the series follows the 4th edition, the author reads it in the Italian translation, and the sources don't say whether that translation was made from the US or the Global Edition.

## Consequences

- No misattributed wording: every sentence in quotation marks will have been verified in English.
- Section numbers stay reliable for readers of any edition that follows the 4th-edition structure.
- `references/bibliography.md` carries all three ISBNs and the uncertainty about US vs Global.
- If the author gets an English copy later, short quotes become possible again, still within the CLAUDE.md §2.2 budget.
