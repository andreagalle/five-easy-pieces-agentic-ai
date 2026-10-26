---
title: "ADR-0003 — Drop Tier T (Terraform-provisioned VM)"
adr: "0003"
status: accepted
date: 2026-10-26
---

**Status:** accepted, 2026-10-26. Decided by the author (open decision D1) in [session 01]({{ "/journal/2026-10-26-01-bootstrap/" | relative_url }}).

## Context

[ADR-0001]({{ "/decisions/ADR-0001-execution-tiers/" | relative_url }}) left a third execution tier open: a KVM-capable VM, provisioned with Terraform, where local sandboxes could run away from the author's laptop. It would need a cloud provider and a region, remote Terraform state, and a `make destroy` next to every `make apply`.

## Options considered

1. **Keep Tier T** and pick a provider now.
2. **Drop Tier T.** Cloud sandboxes already make the series independent of the author's laptop.
3. **Defer** until the cloud tier has been tried.

## Decision

Option 2: drop it.

## Consequences

- No `infra/terraform/`, no Terraform in the devcontainer, and no provider account to manage or pay for.
- Every run by the author happens in cloud sandboxes (Tier C). The Codespace can't run local sandboxes (`/dev/kvm` isn't accessible, and the author chose not to change group membership; see ADR-0001).
- The local tier (Tier L) stays in the scripts for readers with KVM-capable machines. An example's README says "local tier not tested: no KVM available" unless someone has actually run it locally (CLAUDE.md §11).
- To revisit only if cloud sandboxes become unavailable or unaffordable for the series.
