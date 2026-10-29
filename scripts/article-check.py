#!/usr/bin/env python3
"""Check every article past 'idea' against the rules it must follow before Medium.

    scripts/article-check.py [articles/NN-*/article.md ...]

Errors (exit 1):
  - headings deeper than ## , tables, footnotes          (CLAUDE.md §3.3: Medium has none)
  - code blocks longer than 40 lines                     (CLAUDE.md §3.2)
  - links to the repository on a branch, not a tag       (CLAUDE.md §3.3: published links must not rot)
  - missing disclosure line, or missing parts of it      (ADR-0013)
  - header image without the "AI-generated" caption      (ADR-0013)
  - missing front matter keys                            (CLAUDE.md §7)
Warnings, which become errors from status 'review' on (a draft may still be too long):
  - length outside the target for its kind               (CLAUDE.md §1)
  - empty verified_with in an article that runs sbx      (CLAUDE.md §5.5)
Always a warning, for a human to check:
  - text in quotation marks right before "(AIMA"         (ADR-0012: quote only what was checked in English)

Length counts prose only: no front matter, code blocks, images, series navigation or disclosure.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPO_URL = "github.com/andreagalle/five-easy-pieces-agentic-ai"
STATUSES = ["idea", "outline", "draft", "review", "ready", "published"]
REQUIRED_KEYS = ["id", "title", "status", "drafted_by", "edited_by", "verified_with", "code_tag", "medium_url"]
TARGET_WORDS = {"00": (1500, 2000), "06": (1200, 1800)}  # pieces 01-05: (600, 1200), ADR-0017
MAX_CODE_LINES = 40


def front_matter(text: str) -> tuple[dict, str]:
    match = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not match:
        return {}, text
    meta = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            meta[key.strip()] = value.strip().strip('"')
    return meta, text[match.end():]


def prose_words(body: str) -> int:
    words = 0
    in_code = False
    for line in body.splitlines():
        if line.startswith("```"):
            in_code = not in_code
            continue
        if line.startswith("## The series"):
            break  # series navigation is boilerplate, and the disclosure line follows it
        if in_code or line.startswith("![") or line.startswith("*Disclosure"):
            continue
        words += len(line.split())
    return words


def check(path: Path) -> tuple[list[str], list[str]]:
    errors, warnings = [], []
    text = path.read_text()
    meta, body = front_matter(text)
    status = meta.get("status", "")
    strict = status in STATUSES and STATUSES.index(status) >= STATUSES.index("review")

    missing = [k for k in REQUIRED_KEYS if k not in meta]
    if missing:
        errors.append(f"front matter: missing {', '.join(missing)}")

    lines = body.splitlines()
    in_code, code_start = False, 0
    for n, line in enumerate(lines, 1):
        if line.startswith("```"):
            if in_code and n - code_start - 1 > MAX_CODE_LINES:
                errors.append(f"line {code_start}: code block of {n - code_start - 1} lines (max {MAX_CODE_LINES})")
            in_code, code_start = not in_code, n
            continue
        if in_code:
            continue
        if re.match(r"#{3,}\s", line):
            errors.append(f"line {n}: heading deeper than ## (Medium has two levels)")
        if line.lstrip().startswith("|"):
            errors.append(f"line {n}: table row (Medium has no tables)")
        if "[^" in line:
            errors.append(f"line {n}: footnote (Medium has none; use an inline link)")
        for ref in re.findall(re.escape(REPO_URL) + r"/(?:tree|blob)/([^/\s)]+)", line):
            if not re.fullmatch(r"piece-\d\d-v\d+", ref):
                errors.append(f"line {n}: link to '{ref}'; code links must point to a piece-NN-vN tag")
        if re.search(r"[\"“][^\"”]{10,}[\"”]\s*\(AIMA", line):
            warnings.append(f"line {n}: looks like a direct AIMA quote; verify it against an English copy (ADR-0012)")

    disclosure = next((l for l in lines if l.startswith("*Disclosure:")), None)
    if disclosure is None:
        errors.append("no disclosure line (ADR-0013)")
    else:
        for part in ("Docker Captain", "Claude (Anthropic)", "AI-generated"):
            if part not in disclosure:
                errors.append(f"disclosure line lacks '{part}' (ADR-0013)")

    if (path.parent / "assets" / "header.jpg").exists():
        image = next((i for i, l in enumerate(lines) if "](assets/header.jpg)" in l), None)
        if image is None:
            errors.append("assets/header.jpg exists but the article doesn't show it")
        elif not any("*AI-generated illustration.*" in l for l in lines[image + 1:image + 4]):
            errors.append("header image without the '*AI-generated illustration.*' caption (ADR-0013)")

    low, high = TARGET_WORDS.get(meta.get("id", ""), (600, 1200))
    words = prose_words(body)
    if not low <= words <= high:
        (errors if strict else warnings).append(f"{words} words of prose; target {low}-{high}")

    if not meta.get("verified_with") and re.search(r"\bsbx\b|make run-", body):
        (errors if strict else warnings).append("verified_with is empty but the article uses sbx (CLAUDE.md §5.5)")

    return errors, warnings


def main() -> int:
    paths = [Path(p) for p in sys.argv[1:]] or sorted((ROOT / "articles").glob("*/article.md"))
    failed = 0
    for path in paths:
        meta, _ = front_matter(path.read_text())
        name = path.resolve().relative_to(ROOT) if path.resolve().is_relative_to(ROOT) else path
        if meta.get("status", "idea") == "idea":
            continue  # placeholders: nothing to check yet
        errors, warnings = check(path)
        print(f"{name} [{meta.get('status')}]: " + ("ok" if not errors else f"{len(errors)} error(s)"))
        for e in errors:
            print(f"  ERROR   {e}")
        for w in warnings:
            print(f"  warning {w}")
        failed += bool(errors)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
