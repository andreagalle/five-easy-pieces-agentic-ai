# Illustrations

One header image per article, all in the same visual series: a small cleaner fish (the vacuum agent) inside a glass sphere on the seabed (the sandbox). From piece to piece the glass goes from barely there to sealed, matching the arc on the [pieces page](../site/pieces.md): the sandbox goes from a formality to the thing that makes the agent safe. The site icon is the same pair, close up.

**All of these images are AI-generated**, with Google's Nano Banana 2 via OpenRouter, from the prompts in this folder. Every article and the site say so ([ADR-0013](../site/decisions/ADR-0013-disclosure-line.md)).

## How to make one

```bash
make header-01                                    # draft -> articles/01-*/assets/drafts/header-<UTC>.png
scripts/gen-header.py 01 --keep header-<UTC>.png  # promote it: assets/header.jpg (committed)
make header-favicon                               # draft -> illustrations/drafts/favicon-<UTC>.png
scripts/gen-header.py favicon --keep favicon-<UTC>.png  # derive site/favicon.ico and site/assets/img/*.png
scripts/gen-header.py 01 --dry-run                # print the exact prompt; costs nothing
```

What gets committed, and why:

- **Article headers: `assets/header.jpg` only** (JPEG q90, about 1 MB). The 2K PNG master is about 7 MB, and seven of them would add about 50 MB to the git history for no visible difference. The PNG stays local as `assets/header.png`. Drafts stay local too, because only one per article matters.
- **Favicon: the derived icons only** (`favicon.ico` with 16/32/48 px, PNGs at 16, 32, 180, 192 and 512 px). That's every size a browser or phone asks for, and nothing larger. They're cut from the draft along the sphere's rim: **round, transparent outside the circle**, and cropped so the sphere fills the icon. That's the author's request, and it also makes the shape larger at 16 px. The rim is found automatically, as the bounding box of the brightest pixels. (iOS shows transparent corners of the 180 px icon as black, then masks them with its own rounded square.)
- **[`log.jsonl`](log.jsonl):** every generation and every keep, with model, resolution, prompt hash, reference, size and **cost**. Article 06 can quote the real spend.

## What goes into the prompt, and why

The prompt is assembled from four files, in this order:

1. [`style.txt`](style.txt): the author's style, palette, composition and "strictly avoid" rules, **verbatim**.
2. [`cast.txt`](cast.txt): the recurring cast (cleaner, sphere, whale, moon), described identically every time, **verbatim**. Each image is generated without memory of the others, so the characters stay consistent only if they're described the same way every time.
3. [`rules.txt`](rules.txt): **our corrections**, kept separate so the author's text stays untouched. Each line answers something the drafts got wrong:
   - a "sealed" sphere came out opaque and lost its cleaner;
   - grids appeared on the open seabed;
   - the hub image, used as a reference, pushed its whale into piece 01;
   - "at night" produced a moon in piece 06;
   - "switched off" didn't darken piece 02.
4. [`subjects/NN.txt`](subjects/): the author's subject for that article, **verbatim**. `subjects/favicon.txt` is ours: the cleaner in its sphere, simplified so it still reads at 16 px.

For every image except the hub's, the kept hub header is attached as a **style reference**, with a note to copy its style but not its composition. Why: a picture pins the look of the cleaner and the sphere much better than words do. Exception: **04 was generated without the reference.** Its subject is also a row of spheres, and with the reference it came out almost identical to the hub.

## Choices, and why

- **Model: Nano Banana 2** (`google/gemini-3.1-flash-image`) via OpenRouter's Image API. Nano Banana 2.1 is newer and half the price, but on 2026-10-26 its only provider answered HTTP 429 ("quota exceeded"). Nano Banana 2 has three providers. One model for the whole series keeps the style consistent. Override with `HEADER_MODEL`.
- **Resolution: 2K (2752×1536) for headers, 1K (1024×1024) for the favicon.** The author preferred the 2K look. A 2K image normally bills 1,680 image tokens, **about $0.10**. The very first one billed 8,400 tokens ($0.51) and the favicon 3,360 ($0.20), and the usage report doesn't say why. We briefly switched to 1K because of that first outlier. Override with `HEADER_RESOLUTION`.
- **Budget guard: $4.00 for images** (`IMAGE_BUDGET_USD`), below the OpenRouter key's own limit. The script refuses to generate past it, so the LLM pieces 03–05 keep their share.
- **Runs on the host, not in a sandbox.** It's a short, trusted script we wrote, it runs no generated code, and it only calls one API. By the series' own logic (pieces 01–02), it doesn't need a fence. The key comes from the `OPENROUTER_API_KEY` Codespaces secret and is never printed or logged.

## What each image means

- **00 Hub:** five spheres in a row, glass from almost invisible to sealed: the five pieces and the progression. The whale overhead is the cloud running every sphere.
- **01 Simple reflex:** a ring of bubbles looping back on itself is the infinite loop. The upright sand dollar (a sea "coin") is the coin flip that breaks it. The flimsy glass: here the sandbox is a formality.
- **02 Model-based:** pearls on the cleaned stones are the internal state and the orderly sweep. They keep glowing while the dark sphere sleeps: state that survives stop and restart.
- **03 Goal-based:** one thread of light leaving the sealed sphere is the policy that denies everything except `openrouter.ai`. The glowing corner is the goal; placing stones is writing code.
- **04 Utility-based:** spheres of different sizes are parallel sandboxes. Those dissolving into bubbles are hitting their TTL. The one glowing is the candidate with the best utility.
- **05 Learning:** the moon is the critic, fixed, outside and out of reach. The bottles are `sbx --cloud cp`, and the ghost trails are the agent improving.
- **06 Making-of:** the boat is the Codespace, the logbook is the journal and the site, and the second lantern is a quiet nod to Claude, with no logo. Below the waterline are the five runs.
- **Site icon:** the protagonist alone, the cleaner in its sphere. It also links back to the site's home page.

The whale appears only in 00 and 06, bookending the series; the moon only in 05.
