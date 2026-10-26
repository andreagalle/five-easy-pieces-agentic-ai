---
layout: post
title: "Session 03 — Seven illustrations, an icon, and the fine print"
date: 2026-10-26
session: "03"
pieces: ["00", "01", "02", "03", "04", "05", "06"]
sbx_version: "v0.50.0"
model: "claude-opus-5-5 (Claude Opus 5.5)"
sandbox_runs: { cloud: 0, local: 0 }
---

## Goal

The author's requests, all translated from Italian:

- A script to generate one header image per article through OpenRouter, using Google's "Nano Banana" models. It should follow a system prompt the author wrote and a recurring cast, with one subject per article.
- The AIMA edition: the author reads the Italian translation, and wanted that stated transparently.
- The disclosure line: say once, low-key, that the author is a Docker Captain and enthusiastic about the technology.

Later in the session:

- Choose the 2K images over 1K, generate all seven, and say plainly that they're AI-generated.
- Make a favicon in the same style, round with transparent corners, and use it on the site as a logo that links home.

## What we did

- **Two decisions recorded:**
  - [ADR-0012]({{ "/decisions/ADR-0012-aima-edition-and-quotes/" | relative_url }}): cite the 4th edition (Pearson, 2020). The author reads the Italian translation (Pearson Italia, ed. F. Amigoni), so section numbers are checked there. Direct quotes only if verified against an English copy; otherwise paraphrase. The sources don't say whether the translation was made from the US or the Global Edition, and the hub will say so.
  - [ADR-0013]({{ "/decisions/ADR-0013-disclosure-line/" | relative_url }}): the disclosure line, Docker Captain included, as the one deliberate exception to CLAUDE.md §0.6. It states that the images are AI-generated, and each Medium header carries the caption *AI-generated illustration.*
- **The image tool,** `scripts/gen-header.py` with `make header-NN` (`94b72f5`, `a8ef735`):
  - It sends OpenRouter's Image API the author's style, cast and subject, word for word, plus our separate `rules.txt`.
  - It attaches the hub image as a style reference.
  - It keeps a $4.00 budget guard and logs every call's cost.
  - It commits each header as a ~1 MB JPEG and leaves the 7 MB PNG master local.
- **Seven 2K headers** (`6059c9b`) and a **favicon** (`a5fbca2`, `6b36e18`):
  - 14 generations, 8 kept, **$1.83 in total**.
  - The favicon is cut along the sphere's rim, so it's round with transparent corners, and every icon size is derived from it.
- **The site** gained the icon, a logo inside the title link (so it leads home), the palette's colours, and a note on the home page that the illustrations are AI-generated (`a5fbca2`). Checked with a local build and a headless-Chrome screenshot.

## Commands that mattered

From the `Makefile` and `scripts/gen-header.py`:

```bash
make header-00                                    # draft a header
scripts/gen-header.py 00 --keep header-<UTC>.png  # keep it: assets/header.jpg
make header-favicon
scripts/gen-header.py favicon --keep favicon-<UTC>.png
```

## Decisions

- [ADR-0012 — AIMA edition: cite the 4th edition, read in Italian, paraphrase]({{ "/decisions/ADR-0012-aima-edition-and-quotes/" | relative_url }})
- [ADR-0013 — The disclosure line]({{ "/decisions/ADR-0013-disclosure-line/" | relative_url }}), updated later in the session to say "AI-generated" explicitly
- Not ADRs, recorded in `illustrations/README.md` with their reasons: Nano Banana 2 as the model, 2K resolution, the $4.00 image budget, and running the tool on the host.

## Dead ends and surprises

- **The newest model was out of quota.** Nano Banana 2.1's only OpenRouter provider (Google AI Studio) answered HTTP 429, twice. We moved to Nano Banana 2, which has three providers, and used it for the whole series, so the style stays consistent.
- **One outlier drove a wrong decision.**
  - The very first 2K image billed 8,400 image tokens ($0.51) and took 85 s.
  - We concluded that 2K was seven times as expensive as 1K and switched to 1K.
  - When the author chose the 2K look anyway, the next six 2K images billed 1,680 tokens each ($0.10, about 25 s).
  - The usage report never said why the first one cost five times as much.
- **A style reference copies more than style.** With the hub attached, piece 01 got the hub's whale and two cleaners, and 04 and 06 inherited its layout and a stray grid. Two fixes held it back: a separate `rules.txt` ("draw only what the subject describes") and a stricter note on the reference. Piece 04 still needed generating without the reference.
- **Words the model reads literally, and words it ignores:**
  - "Sealed and solid" produced an opaque sphere with no fish inside.
  - "At night" produced a moon nobody asked for.
  - "Dimmed, as if switched off" was ignored until a rule spelled it out.
- **The key's limit, not the account's credit, is the cap.** The author added credit ($10 in total), but the OpenRouter key still has its own $5 limit. That limit is the real fence for pieces 03–05: $3.17 remains on it.
- **A wait loop that waited for itself.** Claude used `pgrep -f` to wait for the background generations, and the loop's own command line matched the pattern, so it never ended. The images were done in under a minute; the command hit its 10-minute timeout. Then `pkill -f` killed the shell it ran in, for the same reason.
- **Headless Chrome, already installed for diagrams, earned a second job:** screenshotting the built site to check the logo and colours before committing.

## Who did what

- **The author:** wrote the illustration system prompt, the cast and the seven subjects; chose the 2K images; asked for the AI-generated label, the favicon, the round cut and the logo link; added OpenRouter credit; and decided the edition and disclosure wording.
- **Claude:** looked up the edition facts, wrote ADR-0012 and ADR-0013, built the image tool and its rules, reviewed every image against its subject, and decided which to regenerate. It also wrote the favicon subject and the site overrides, and this entry.

## Next

1. Raise the OpenRouter key's limit before piece 03. The images used $1.83 of the $5 key, and the account has more credit than the key can spend.
2. Draft article 01 and outline the hub. Hub and 01 go out together (ADR-0007), and the header images are ready.
3. Example 02 (model-based reflex) and its persistence run in the cloud.
