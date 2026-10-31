# Network policy — piece 02

**Policy: no egress at all.** The sandbox is created with `--deny-network '**'` (`SBX_NETWORK=deny-all`, the default in `scripts/sbx-run.sh`).

**Why no network:** like piece 01, the agent is a deterministic, standard-library Python program. It downloads nothing, calls no API and holds no secrets. Its state file stays inside the sandbox, so nothing needs to leave.

**Is the fence needed here? Still no.** It's a small program that we wrote and read. What changes from piece 01 is what's at stake inside the sandbox: the agent's memory now lives there, so deleting the sandbox costs something. From piece 03 on, LLM agents keep their memory in files inside the sandbox too.

**One thing to watch:** a stopped cloud sandbox has no running TTL, so `--on-timeout delete` can't clean it up. Compute isn't billed while it's stopped, and the wrapper's EXIT trap removes it, but a run killed outright could leave it behind. `sbx --cloud ls` shows it.
