---
title: "“Test everything except OpenRouter, and say so” — session 05"
date: 2026-10-27
session: "05"
---

**Context:** the author had read the cloud rates in their Docker Console and wanted real sandboxes in CI, but not at the price of spending model credit on every merge. Journal: [session 05]({{ "/journal/2026-10-27-05-ci-sandboxes-and-charts/" | relative_url }}).

> I'd like to add them [sandboxes in CI]: will it cost me a lot?
>
> OK, add an exception for these [pieces 03–05], or let's replace the calls with something fake, or with an undefined token, so that everything else is tested except the interaction with OpenRouter. In that case, let's say so explicitly.
>
> [On a time limit for the job and a final check for leftover sandboxes:] Absolutely, yes!
>
> Anyway, I really like your proposal; adapt it to what I said above.

*(translated from Italian)*

Why it matters: it became ADR-0014. Deterministic pieces run in a real cloud sandbox after each merge. The LLM pieces will run against a fake model, CI holds no OpenRouter key at all, and both CI and the articles say plainly what isn't tested.

*Recorded after the fact, in session 09: `/wrap` had no step for prompts, so none was recorded between sessions 04 and 08. The text is the author's message from the session, translated.*
