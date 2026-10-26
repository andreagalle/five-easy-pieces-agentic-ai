---
title: "ADR-0010 — Cloud only until the local tier is tested"
adr: "0010"
status: accepted
date: 2026-10-26
---

**Status:** accepted, 2026-10-26. Decided by the author in session 02. Amends [ADR-0001]({{ "/decisions/ADR-0001-execution-tiers/" | relative_url }}).

## Context

ADR-0001 made local sandboxes (Tier L, `SBX_TARGET=local`) the reader's fallback: the same scripts, run on any KVM-capable machine. The author can't test that tier yet:

- The Codespace has `/dev/kvm`, but it isn't accessible, and the author chose not to force it (ADR-0001).
- The Terraform-provisioned VM was dropped (ADR-0003).
- The author's current laptop isn't capable enough to run local sandboxes. A new one is coming soon.

The brief's rule is that articles describe runs that actually happened (CLAUDE.md §10.3). Publishing local commands nobody has run would break it.

## Options considered

1. **Publish the local commands untested**, with a warning.
2. **Leave the local tier out entirely** until it's tested.
3. **Cloud only for now, with an honest mention.** Show only the cloud tier, and say in one line that a locally tested version will follow.

## Decision

Option 3.

- Articles and example READMEs show cloud commands only. Each mentions in one line that the local version will be published once the author has tested it on a capable machine, which is expected soon.
- `scripts/sbx-run.sh` refuses `SBX_TARGET=local` with a clear message until the local tier has been tested.
- Piece 01 originally planned to show identical output locally and in the cloud. It shows identical output on the host and in a cloud sandbox instead; the local comparison is added when the tier is tested.

## Consequences

- CLAUDE.md §3.4 step 5 ("then one line for the local equivalent") and the local half of the §11 definition of done are on hold until this ADR is superseded.
- When the author's machine arrives: test every example with `SBX_TARGET=local`, record the runs in `RUNINFO.json`, update READMEs and articles, and write an ADR that lifts this one. Published articles get a short update rather than a rewrite.
- One less variable for now: every number in the articles comes from cloud runs.
