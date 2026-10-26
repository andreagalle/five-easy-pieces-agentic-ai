---
title: "ADR-0005 — Site generator: Jekyll built in GitHub Actions"
adr: "0005"
status: accepted
date: 2026-10-26
---

**Status:** accepted, 2026-10-26. Decided by the author (open decision D3) in [session 01]({{ "/journal/2026-10-26-01-bootstrap/" | relative_url }}).

## Context

The making-of record lives in `site/` and is published with GitHub Pages. It has to stay easy to write (Markdown with front matter, written by Claude during each session) and must need no tooling beyond what the repository already has.

## Options considered

1. **Jekyll, built by GitHub's own `jekyll-build-pages` action** and deployed with `deploy-pages`: no Gemfile, no extra tooling.
2. **Classic "deploy from a branch" Pages build.** Same Jekyll, but `site/` isn't a source folder GitHub Pages can serve directly (only `/` or `/docs`).
3. **Another generator** (MkDocs, Hugo, Astro): more control, more tooling to install and keep current.

## Decision

Option 1. `.github/workflows/pages.yml` builds `site/` with `actions/jekyll-build-pages@v1` (the `minima` theme, permalinks set to `pretty`) and deploys from `master`.

## Consequences

- The repository needs Settings → Pages → Source set to "GitHub Actions" (one-time, by the author).
- Only plugins bundled with the `github-pages` gem are available.
- `make site-build` reproduces the build locally with the same builder image (`ghcr.io/actions/jekyll-build-pages:v1.0.13`). It calls `github-pages build` directly, because the image's entrypoint always exports an empty GitHub token when none is given, and that fails GitHub API authentication.
- `baseurl` is the repository name (`/five-easy-pieces-agentic-ai`). Renaming the repository means changing `site/_config.yml`.
