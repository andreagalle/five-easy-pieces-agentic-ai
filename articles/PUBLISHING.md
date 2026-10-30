# Publishing an article on Medium

Medium stopped issuing API tokens on 1 January 2025 (as documented by n8n and StackOne), so publishing means pasting into Medium's editor. This checklist makes the paste repeatable for all seven articles. Order and cadence: [ADR-0007](../site/decisions/ADR-0007-publication-order.md). Publication: Docker Captains Wisdom ([ADR-0008](../site/decisions/ADR-0008-medium-publication.md)).

## 1. Ready in the repository

1. The author has reviewed the draft, and the front matter has moved from `draft` to `review`. Step 6 moves it on to `ready`, which is the status an article has when it goes to Medium.
2. `make article-check` passes. At `review` it's strict: length and `verified_with` are errors, not warnings.
3. **Pieces 01–05 only:** the code is frozen and tagged (`git tag piece-NN-v1`, then `git push origin piece-NN-v1`), and every code link points to that tag. `make article-check` rejects links to a branch.
4. `/verify-sbx` has passed, and `verified_with` names the `sbx` version.
5. The charts are redrawn from the reference run (`make plots-NN`), and the header is kept (`assets/header.jpg`).
6. Set `status: ready`, commit, and merge to `master`.

## 2. Into Medium's editor

1. Open `article.md` in VS Code's Markdown preview (Ctrl+Shift+V). Copy from the title down, leaving out the front matter.
2. In Medium, start a new story and paste. Then check:
   - **Title and subtitle:** the first line is the title. Format the italic line under it as the subtitle.
   - **Images:** pasted images don't carry over, so insert each one with Medium's "+" → image:
     - `header.jpg` goes first, because Medium uses the first image as the story's preview. Caption it *AI-generated illustration.* (ADR-0013).
     - Charts (`fig-*.png`) go where the article places them. Use the article's image text as Medium's alt text (image menu → Alt text).
   - **Code blocks:** they're still code blocks.
   - **Links:** they're all still links.
   - **Disclosure line:** it's at the end, in italics.

## 3. Publish

1. In the story settings, add the story to **Docker Captains Wisdom**, and choose up to five tags (the author's choice).
2. **For the overture and piece 01, which go out the same day:**
   1. Publish piece 01 first.
   2. Paste its URL into the overture's series list, then publish the overture.
   3. Edit piece 01 to link back to the overture. Medium allows edits after publishing.
3. **For each weekly piece:** publish it, then edit the overture and the previous piece to replace "coming soon" with its link.

## 4. Back in the repository

1. In `site/_data/series.yml`, set `status: published`, `medium_url` and `last_session`.
2. Add or update the "Articles published N/7" badge in the README (CLAUDE.md §9.3).
3. Write a journal entry. The publication is part of the record.
