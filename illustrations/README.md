# Illustrations

One header image per article, all in the same visual series: a small cleaner fish (the vacuum agent) inside a glass sphere on the seabed (the sandbox). From piece to piece the glass goes from barely there to sealed, matching the arc on the [pieces page](../site/pieces.md): the sandbox goes from a formality to the thing that makes the agent safe.

## How to make one

```bash
make header-01                                  # draft -> articles/01-*/assets/drafts/header-<UTC>.png
scripts/gen-header.py 01 --keep header-<UTC>.png  # promote the chosen draft to assets/header.png
scripts/gen-header.py 01 --dry-run              # print the exact prompt; costs nothing
```

Only the kept `header.png` is committed. Drafts are git-ignored, because they're large and only one per article matters. Every generation and every keep is appended to [`log.jsonl`](log.jsonl): model, resolution, prompt hash, reference, size and **cost**. Article 06 can quote the real spend.

## What goes into the prompt, and why

The prompt is assembled from four files, in this order:

1. [`style.txt`](style.txt): the author's style, palette, composition and "strictly avoid" rules, **verbatim**.
2. [`cast.txt`](cast.txt): the recurring cast (cleaner, sphere, whale, moon), described identically every time, **verbatim**. Each image is generated without memory of the others, so the characters stay consistent only if they're described the same way every time.
3. [`rules.txt`](rules.txt): **our corrections**, kept separate so the author's text stays untouched. They come from the first drafts. A "sealed" sphere came out opaque and lost its cleaner, grids appeared on the open seabed, and the hub image, used as a reference, pushed its whale into piece 01.
4. [`subjects/NN.txt`](subjects/): the author's subject for that article, **verbatim**.

For every article except 00, the kept hub header is attached as a **style reference**, with a note to copy its style but not its composition. Why: a picture pins the look of the cleaner and the sphere much better than words do.

## Choices, and why

- **Model: Nano Banana 2** (`google/gemini-3.1-flash-image`) via OpenRouter's Image API. Nano Banana 2.1 is newer and half the price, but on 2026-10-26 its only provider answered HTTP 429 ("quota exceeded"). Nano Banana 2 has three providers. One model for the whole series keeps the style consistent. Override with `HEADER_MODEL`.
- **Resolution: 1K (1376×768).** At 2K one image used 8,400 output tokens and cost **$0.51**; at 1K it costs **$0.068**. The OpenRouter key has a $5 limit shared with pieces 03–05, so the series can't afford 2K. Override with `HEADER_RESOLUTION`.
- **Budget guard: $1.50 for images** (`IMAGE_BUDGET_USD`). The script refuses to generate past it, so at least $3.50 stays for the LLM pieces.
- **Runs on the host, not in a sandbox.** It's a short, trusted script we wrote, it runs no generated code, and it only calls one API. By the series' own logic (pieces 01–02), it doesn't need a fence. The key comes from the `OPENROUTER_API_KEY` Codespaces secret and is never printed or logged.
- **Disclosure:** every article says the header is AI-generated, and with which model ([ADR-0013](../site/decisions/ADR-0013-disclosure-line.md)).

## What each image means

- **00 Hub:** five spheres in an arc, glass from almost invisible to sealed: the five pieces and the progression. The whale overhead is the cloud running every sphere.
- **01 Simple reflex:** a ring of bubbles looping back on itself is the infinite loop. The spinning sand dollar (a sea "coin") is the coin flip that breaks it. The flimsy glass: here the sandbox is a formality.
- **02 Model-based:** pearls on the cleaned stones are the internal state and the orderly sweep. They keep glowing while the sphere is switched off: state that survives stop and restart.
- **03 Goal-based:** one thread of light leaving the sealed sphere is the policy that denies everything except `openrouter.ai`. The glowing corner is the goal; placing stones is writing code.
- **04 Utility-based:** N spheres of different sizes are parallel sandboxes. Those dissolving into bubbles are hitting their TTL. The one glowing is the candidate with the best utility.
- **05 Learning:** the moon is the critic, fixed, outside and out of reach. The bottles are `sbx --cloud cp`, and the ghost trails are the agent improving.
- **06 Making-of:** the boat is the Codespace, the logbook is the journal and this site, and the second lantern is a quiet nod to Claude, with no logo. Below the waterline are the five runs.

The whale appears only in 00 and 06, bookending the series; the moon only in 05. Keeping each to one or two images keeps them meaningful.
