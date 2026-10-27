---
title: "ADR-0015 — Cite the book properly; drop the third-party study notes"
adr: "0015"
status: accepted
date: 2026-10-27
---

**Status:** accepted, 2026-10-27. Decided by the author in session 06, while reviewing the hub. Amends [ADR-0012]({{ "/decisions/ADR-0012-aima-edition-and-quotes/" | relative_url }}) and CLAUDE.md §2.1.

## Context

The project brief named a free secondary source for the hub: a student's study notes on AIMA's Chapter 2, hosted on Read the Docs. The first draft of the hub linked them "for convenience". ADR-0012 also had the hub explain, in a "note on sources" at the end, that the sources we checked don't say whether the author's Italian copy was translated from the US or the Global Edition.

Reviewing the draft, the author made three points:

- The notes shouldn't be cited at all. They are someone else's summary of a copyrighted book, and it isn't clear they are published with the rights holders' permission.
- The book deserves a proper, precise reference, with due prominence, rather than a note at the end.
- The author's Italian copy is worth mentioning, in passing, as part of how the series started, not as a caveat.

## Options considered

1. Keep the notes as a convenience link, with a disclaimer.
2. Drop the notes, and cite the book in full once, prominently, at the start of the hub.

## Decision

Option 2:

- **No reference to the study notes anywhere.** Not in the articles, CLAUDE.md, the bibliography or the site.
- **The hub opens with the full reference** to the edition the series follows, set apart as a quotation block:

  > Stuart Russell and Peter Norvig, *Artificial Intelligence: A Modern Approach*, 4th edition (US). Pearson, 2020. ISBN 978-0-13-461099-3.

  The pieces then cite it by section, e.g. *(AIMA 4e, §2.4.2)*.
- **The Italian copy** is mentioned once, in the hub's opening, as the copy the author studied years ago. It also explains, in one light sentence, why the series paraphrases instead of quoting (ADR-0012).
- **The US/Global sentence leaves the article.** Section numbers are still checked against the Italian copy, and `references/bibliography.md` keeps all the ISBNs and that open question.

## Consequences

- CLAUDE.md §2.1 loses its "secondary source", and §2.2 its mention of the notes' images.
- The hub has no "note on sources" section. Its content moved to the opening, where it also serves as the story of how the series began.
- The quoting rules don't change: paraphrase, unless a quote has been checked against an English copy.
