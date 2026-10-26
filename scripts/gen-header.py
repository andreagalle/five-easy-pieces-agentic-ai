#!/usr/bin/env python3
"""Generate an article header illustration with OpenRouter's Image API.

    scripts/gen-header.py ID [--no-reference] [--dry-run]   # make a draft
    scripts/gen-header.py ID --keep DRAFT                   # promote a draft to header.jpg

ID is an article id (00-06) or "favicon": a 1:1 close-up of the cleaner in its sphere, from
which --keep derives the site's icons (site/assets/img/ and site/favicon.ico).

The prompt is illustrations/style.txt + cast.txt + rules.txt + subjects/ID.txt.
For every article except 00, the hub's kept header is attached as a style reference, so
the cleaner and the sphere look the same across the series.

Drafts go to articles/ID-*/assets/drafts/ (git-ignored). --keep writes header.png (local
master, git-ignored) and header.jpg (committed, published). Every call is appended to
illustrations/log.jsonl with its cost. The script refuses to generate once image spending
reaches IMAGE_BUDGET_USD (default 4.00), so the LLM pieces 03-05 keep their share of the
OpenRouter key. The key comes from OPENROUTER_API_KEY and is never printed.
"""

from __future__ import annotations

import argparse
import base64
import datetime
import hashlib
import json
import os
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ILLUSTRATIONS = ROOT / "illustrations"
LOG = ILLUSTRATIONS / "log.jsonl"
API = "https://openrouter.ai/api/v1"

# Nano Banana 2. Nano Banana 2.1 is newer and half the price, but on 2026-10-26 its only
# provider answered HTTP 429 (quota); this one has three providers. One model for the
# whole series keeps the style consistent.
MODEL = os.environ.get("HEADER_MODEL", "google/gemini-3.1-flash-image")
# 2K (2752x1536): the author chose its look over 1K in session 03. A 2K image normally bills
# 1,680 image tokens (about $0.10); the very first one billed 8,400 ($0.51). See README.
RESOLUTION = os.environ.get("HEADER_RESOLUTION", "2K")
ASPECT_RATIO = "16:9"
# A stop line below the key's own limit, so the LLM pieces keep their share.
IMAGE_BUDGET_USD = float(os.environ.get("IMAGE_BUDGET_USD", "4.00"))
JPEG_QUALITY = 90  # the committed header.jpg: about 1.2 MB instead of a 7 MB PNG

REFERENCE_NOTE = (
    "REFERENCE IMAGE\n"
    "The attached image is an earlier header from this same series. Use it only for style: palette, "
    "grain texture, shape language, and the way the cleaner and the sphere are drawn. Do not reuse "
    "its composition or any of its elements; illustrate only the SUBJECT below."
)


FAVICON = "favicon"
SITE_IMG = ROOT / "site" / "assets" / "img"
ICON_SIZES = {"favicon-16x16.png": 16, "favicon-32x32.png": 32, "apple-touch-icon.png": 180,
              "icon-192.png": 192, "icon-512.png": 512}


def target(image_id: str) -> tuple[Path, str, str]:
    """Drafts directory, aspect ratio and resolution for an article header or the favicon."""
    if image_id == FAVICON:
        # Drafts live outside site/ so Jekyll never publishes them.
        return ILLUSTRATIONS / "drafts", "1:1", "1K"
    return article_dir(image_id) / "assets" / "drafts", ASPECT_RATIO, RESOLUTION


def article_dir(article_id: str) -> Path:
    matches = sorted((ROOT / "articles").glob(f"{article_id}-*"))
    if not matches:
        sys.exit(f"gen-header: no articles/{article_id}-* directory")
    return matches[0]


def build_prompt(article_id: str, with_reference: bool) -> str:
    subject = ILLUSTRATIONS / "subjects" / f"{article_id}.txt"
    if not subject.exists():
        sys.exit(f"gen-header: missing {subject.relative_to(ROOT)}")
    # style.txt, cast.txt and subjects/ are the author's text, verbatim; rules.txt holds our corrections.
    parts = [(ILLUSTRATIONS / name).read_text().strip() for name in ("style.txt", "cast.txt", "rules.txt")]
    if with_reference:
        parts.append(REFERENCE_NOTE)
    parts.append("SUBJECT:\n" + subject.read_text().strip())
    return "\n\n".join(parts)


def read_log() -> list[dict]:
    if not LOG.exists():
        return []
    return [json.loads(line) for line in LOG.read_text().splitlines() if line.strip()]


def append_log(entry: dict) -> None:
    with LOG.open("a") as f:
        f.write(json.dumps(entry, sort_keys=True) + "\n")


def spent() -> float:
    return sum(e.get("cost_usd") or 0 for e in read_log() if e.get("action") == "generate")


def api(path: str, body: dict | None = None) -> dict:
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        sys.exit("gen-header: OPENROUTER_API_KEY is not set (a Codespaces secret; restart the Codespace after adding it)")
    data = None if body is None else json.dumps(body).encode()
    request = urllib.request.Request(
        API + path, data=data,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=300) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        detail = error.read().decode(errors="replace")[:500]
        sys.exit(f"gen-header: OpenRouter returned HTTP {error.code}: {detail}")


def png_size(data: bytes) -> tuple[int, int] | None:
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return int.from_bytes(data[16:20], "big"), int.from_bytes(data[20:24], "big")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def now() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)


def generate(article_id: str, use_reference: bool, dry_run: bool) -> None:
    drafts, aspect_ratio, resolution = target(article_id)
    reference = None
    if use_reference and article_id != "00":
        hub = article_dir("00") / "assets"
        reference = next((p for p in (hub / "header.png", hub / "header.jpg") if p.exists()), None)
        if reference is None:
            print("gen-header: no kept hub header yet; generating without a style reference")

    prompt = build_prompt(article_id, reference is not None)
    body = {"model": MODEL, "prompt": prompt, "resolution": resolution, "aspect_ratio": aspect_ratio, "n": 1}
    if reference is not None:
        encoded = base64.b64encode(reference.read_bytes()).decode()
        media_type = "image/png" if reference.suffix == ".png" else "image/jpeg"
        body["input_references"] = [{"type": "image_url", "image_url": {"url": f"data:{media_type};base64,{encoded}"}}]

    print(f"gen-header: {article_id} | {MODEL} | {resolution} {aspect_ratio} | "
          f"reference: {reference.relative_to(ROOT) if reference else 'none'} | prompt sha256 {sha256(prompt.encode())[:12]}")
    if dry_run:
        print(prompt)
        return

    if spent() >= IMAGE_BUDGET_USD:
        sys.exit(f"gen-header: image budget reached (${spent():.4f} of ${IMAGE_BUDGET_USD:.2f}); raise IMAGE_BUDGET_USD deliberately")
    key_before = api("/key")["data"]

    started = now()
    result = api("/images", body)
    image = result["data"][0]
    data = base64.b64decode(image["b64_json"])
    usage = result.get("usage") or {}

    drafts.mkdir(parents=True, exist_ok=True)
    prefix = FAVICON if article_id == FAVICON else "header"
    draft = drafts / f"{prefix}-{started.strftime('%Y%m%dT%H%M%SZ')}.png"
    draft.write_bytes(data)
    size = png_size(data)

    append_log({
        "time": started.isoformat(),
        "action": "generate",
        "id": article_id,
        "model": MODEL,
        "resolution": resolution,
        "aspect_ratio": aspect_ratio,
        "prompt_sha256": sha256(prompt.encode()),
        "reference": None if reference is None else {"path": str(reference.relative_to(ROOT)), "sha256": sha256(reference.read_bytes())},
        "draft": str(draft.relative_to(ROOT)),
        "media_type": image.get("media_type"),
        "size": list(size) if size else None,
        "bytes": len(data),
        "sha256": sha256(data),
        "seconds": int((now() - started).total_seconds()),
        "usage": usage,
        "cost_usd": usage.get("cost"),
    })
    remaining = key_before.get("limit_remaining")
    print(f"gen-header: wrote {draft.relative_to(ROOT)} ({size[0]}x{size[1]} px)" if size else f"gen-header: wrote {draft.relative_to(ROOT)}")
    print(f"gen-header: cost ${usage.get('cost')} | images so far ${spent():.4f} of ${IMAGE_BUDGET_USD:.2f} | "
          f"key remaining before this call ${remaining}")


def keep(article_id: str, draft_arg: str) -> None:
    drafts = target(article_id)[0]
    draft = Path(draft_arg)
    if not draft.is_absolute():
        draft = (ROOT / draft) if (ROOT / draft).exists() else (drafts / draft)
    if not draft.exists():
        sys.exit(f"gen-header: no such draft: {draft_arg}")
    if not shutil.which("convert"):
        sys.exit("gen-header: ImageMagick 'convert' not found (scripts/post-create.sh installs it)")
    if article_id == FAVICON:
        keep_favicon(draft)
        return
    assets = drafts.parent
    # header.png is the local master (git-ignored, ~7 MB); header.jpg is committed and published.
    master = assets / "header.png"
    published = assets / "header.jpg"
    shutil.copyfile(draft, master)
    subprocess.run(["convert", str(master), "-strip", "-quality", str(JPEG_QUALITY), str(published)], check=True)
    append_log({
        "time": now().isoformat(),
        "action": "keep",
        "id": article_id,
        "draft": str(draft.relative_to(ROOT)),
        "kept_as": str(published.relative_to(ROOT)),
        "png_sha256": sha256(master.read_bytes()),
        "jpg_sha256": sha256(published.read_bytes()),
        "jpg_bytes": published.stat().st_size,
    })
    print(f"gen-header: kept {draft.relative_to(ROOT)} as {published.relative_to(ROOT)} "
          f"({published.stat().st_size // 1024} KB, JPEG q{JPEG_QUALITY}; PNG master stays local)")


def keep_favicon(draft: Path) -> None:
    """Derive every icon a browser asks for: PNGs at fixed sizes and a multi-size .ico."""
    SITE_IMG.mkdir(parents=True, exist_ok=True)
    made = []
    for name, px in ICON_SIZES.items():
        out = SITE_IMG / name
        subprocess.run(["convert", str(draft), "-strip", "-resize", f"{px}x{px}", str(out)], check=True)
        made.append(out)
    ico = ROOT / "site" / "favicon.ico"
    subprocess.run(["convert", str(draft), "-strip", "-define", "icon:auto-resize=48,32,16", str(ico)], check=True)
    made.append(ico)
    append_log({
        "time": now().isoformat(),
        "action": "keep",
        "id": FAVICON,
        "draft": str(draft.relative_to(ROOT)),
        "kept_as": [str(p.relative_to(ROOT)) for p in made],
        "draft_sha256": sha256(draft.read_bytes()),
    })
    print("gen-header: kept favicon as " + ", ".join(str(p.relative_to(ROOT)) for p in made))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("id", help="article id (00 to 06) or 'favicon'")
    parser.add_argument("--keep", metavar="DRAFT", help="promote a draft: header.jpg for an article, the icon set for 'favicon'")
    parser.add_argument("--no-reference", action="store_true", help="don't attach the hub header as a style reference")
    parser.add_argument("--dry-run", action="store_true", help="print the prompt and stop; costs nothing")
    args = parser.parse_args()
    if args.keep:
        keep(args.id, args.keep)
    else:
        generate(args.id, not args.no_reference, args.dry_run)


if __name__ == "__main__":
    main()
