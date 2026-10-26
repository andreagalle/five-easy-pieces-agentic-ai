# Network policy — piece 01

**Policy: no egress at all.** The sandbox is created with `--deny-network '**'` (`SBX_NETWORK=deny-all`, the default in `scripts/sbx-run.sh`).

**Why no network:** the agent is a deterministic, standard-library Python program. It downloads nothing, calls no API and holds no secrets, so it has no legitimate reason to reach anything outside the sandbox.

**Is the fence needed here? No.** The program is 40 trusted lines that we wrote and read. We apply the policy anyway, for two reasons:

- It costs nothing, and it turns a claim into a fact: the output depends on nothing outside the sandbox.
- It's the simplest possible policy, deny everything. Piece 03 starts from it and opens exactly one host, so the difference between the two is easy to see.

**Verified (2026-10-26, sbx v0.50.0):** inside a cloud sandbox created this way, an HTTPS request to `example.com` fails at DNS resolution (`Temporary failure in name resolution`).
