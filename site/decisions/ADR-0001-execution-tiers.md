---
title: "ADR-0001 — Execution tiers"
adr: "0001"
status: accepted
date: 2026-10-26
---

**Status:** accepted, 2026-10-26. Decided by the author in the project brief (CLAUDE.md §5.2); recorded by Claude in [session 01]({{ "/journal/2026-10-26-01-bootstrap/" | relative_url }}). Tier T is pending decision D1.

## Context

Every example in the series has to run in a Docker Sandbox, and readers have to be able to reproduce the runs. Two constraints pull in different directions:

- Local sandboxes are microVMs and need hardware virtualization: KVM on Linux (with the user in the `kvm` group), Apple silicon on macOS 14+, or Windows 11 with the Hypervisor Platform. Many readers have that; a Codespace may not.
- Cloud sandboxes (`sbx --cloud`, sbx ≥ 0.45.0) need no virtualization on the client, but they need a Docker Agentic Platform subscription and cost money per minute. They also behave differently: no host mounts, no `--clone`, separate stores for secrets, policies and templates.

## Options considered

1. **Cloud only.** Simplest story, but every reader pays, and the series depends on one experimental service.
2. **Local only.** Free for readers with KVM, but the author's own environment (a Codespace) may not support it, and the "independent of your laptop" story is lost.
3. **Cloud first, local as fallback, a self-hosted VM as an option.** Same scripts for both managed tiers, chosen with one variable.

## Decision

Option 3, with three tiers:

- **Tier C — cloud sandboxes (primary in the articles).** Run from the Codespace with `sbx --cloud`.
- **Tier L — local sandboxes (reader fallback).** The same scripts with `SBX_TARGET=local`, on any KVM-capable machine. The Codespace qualifies only if `/dev/kvm` is usable inside the devcontainer. Its absence is never worked around with privileged hacks.
- **Tier T — a KVM-capable VM provisioned with Terraform (optional).** No Terraform is written until the author picks a provider (decision D1).

All examples run through one wrapper, `scripts/sbx-run.sh`. It uses copy-in/copy-out (`sbx cp` / `sbx --cloud cp`) instead of bind mounts in *both* tiers, so a run means the same thing locally and in the cloud.

## Consequences

- Articles show cloud commands first and give the local equivalent in one line.
- The wrapper must refuse to start, with a clear message, when `sbx` is missing, not signed in, KVM is absent (local) or cloud access is not enabled.
- Every cloud sandbox gets an explicit `--ttl` and `--on-timeout`, and is removed on exit (CLAUDE.md §0.7).
- **Finding, session 01:** in the current Codespace, `/dev/kvm` exists but belongs to GID 109, a group with no name that the `codespace` user isn't in. `sbx diagnose` reports *Virtualization — not accessible*, so Tier L doesn't work in the Codespace as configured. The documented fix would add the user to the group that owns the device (`sudo usermod -aG kvm $USER`). The author chose not to force it, so Tier L isn't used in the Codespace. With Tier T dropped as well ([ADR-0003]({{ "/decisions/ADR-0003-drop-terraform-tier/" | relative_url }})), all of the author's runs happen in cloud sandboxes.
