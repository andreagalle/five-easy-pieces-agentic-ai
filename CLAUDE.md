# CLAUDE.md

> Project memory for Claude Code. Read this file in full at the start of every session.
> It is the single source of truth for what this repository is, how work is done here,
> and how that work is recorded for the public making-of site.

---

## 0. Prime directives (read these even if you read nothing else)

1. **English only.** Every file, commit message, code comment, journal entry, page, article and chat reply in this repository is written in English, including when the author prompts in Italian or any other language. Translate the author's intent; never paste non-English text into the repo.
2. **Keep the record.** Every working session ends with a journal entry in `site/journal/` and an update to `site/_data/series.yml`. No exceptions: the GitHub Pages site and article 06 are built from this record. If a session ended without one, the next session writes the missing entry first (reconstruct it from `git log`).
3. **Reproducibility first.** Anything that must be run to reproduce an article lives in a script or a `make` target, never only in chat or in article prose. Articles quote commands from the scripts, not the other way round.
4. **Never invent `sbx` flags.** Docker Sandboxes ships minor releases every few weeks. Verify every command against `sbx <command> --help` and the official docs before it lands in a script or article (protocol in §5.5).
5. **No secrets in the repo, ever.** Credentials go through `sbx secret` / `sbx --cloud secret` (host-side proxy injection) or GitHub Codespaces secrets. Never print a secret in output, logs, journal entries or commit messages.
6. **Identity hygiene.** Never write the author's legal name, employer, job title or affiliation anywhere in this repo (files, commits, pages, articles, metadata, screenshots). The author's handle is `andreagalle` (ADR-0006). By the author's choice, git commit metadata and the copyright line in `LICENSE` keep the configured git identity (ADR-0006); don't flag them. One more exception (ADR-0013): each article's disclosure line says the author is a Docker Captain; nowhere else. Never change git config.
7. **Cost hygiene.** Every cloud sandbox is created with an explicit `--ttl` and `--on-timeout`, and every script removes what it creates (trap on EXIT). End every session with `sbx --cloud ls` and report anything still alive.
8. **Ask, don't assume,** on anything listed in §12 (Open decisions). Record every answer as an ADR.

---

## 1. What this project is

A seven-part Medium series, the example code behind it, and a public record of how it was made.

| ID | Working title | Kind | Target length | Code |
|----|---------------|------|---------------|------|
| 00 | Five Easy Pieces on Agentic AI w/ Docker Sandboxes | Hub article | 1,500–2,000 words (~8 min) | — |
| 01 | Piece 1/5 — The simple reflex agent | Short article | 600–900 words (~4 min) | `examples/01-simple-reflex/` |
| 02 | Piece 2/5 — The model-based reflex agent | Short article | 600–900 words | `examples/02-model-based/` |
| 03 | Piece 3/5 — The goal-based agent | Short article | 600–900 words | `examples/03-goal-based/` |
| 04 | Piece 4/5 — The utility-based agent | Short article | 600–900 words | `examples/04-utility-based/` |
| 05 | Piece 5/5 — The learning agent | Short article | 600–900 words | `examples/05-learning/` |
| 06 | The making of: Claude, Docker Sandboxes and a Codespace | Meta article | 1,200–1,800 words | tells the story of `site/` |

Alongside the articles, a GitHub Pages site (`site/`) documents, session by session, how the series was produced in a GitHub Codespace with Claude Code and Docker Sandboxes. Claude writes most of the site's raw material as the work happens (journal, decisions, workflow page); the author edits and decides.

**Thesis of the series, in one line:** AIMA Chapter 2 already gave us the vocabulary for today's agentic AI; Docker Sandboxes give us a disposable, reproducible *architecture* to run each agent *program* in — on a laptop or in the cloud, with the same commands.

---

## 2. Source material and citation rules

### 2.1 Sources

- **Primary:** Russell, S. & Norvig, P., *Artificial Intelligence: A Modern Approach*, 4th ed., Pearson — Chapter 2, "Intelligent Agents". Confirm edition and year against the author's copy before the first citation is written. **Confirmed (ADR-0012):** cite the 4th edition (Pearson, 2020); the author reads the Italian translation (Pearson Italia), so section numbers are checked there and direct quotes are used only if verified against an English copy — otherwise paraphrase.
- **No secondary summaries (ADR-0015).** Third-party study notes on the book are not cited or linked anywhere; the hub opens with the full reference to the US 4th edition (Russell & Norvig, Pearson, 2020, ISBN 978-0-13-461099-3).
- **Optional code reference:** the official AIMA code repositories on GitHub (`aimacode/*`). Check each repository's license before reusing anything; prefer writing our own code.
- Keep `references/bibliography.md` (full references) and `references/aima-ch2-map.md` (concept → AIMA section → article) up to date.

### 2.2 Quoting rules (the author quotes AIMA extensively — do it safely)

- Prefer paraphrase. Direct quotes are short (one sentence, ideally under ~25 words), in quotation marks, with the section number, e.g. *(AIMA 4e, §2.4.2)*.
- Budget: at most one or two direct quotes per short article, a handful in the hub. Definitions make the best quotes (agent, rational agent, *agent = architecture + program*).
- **Never reproduce the book's figures or pseudocode.** Redraw diagrams from scratch (Mermaid sources → rendered images in `articles/<id>/assets/`) and implement algorithms in our own code and words.
- When unsure whether a passage is too long to quote, paraphrase it.

### 2.3 Chapter 2 concept map (seed for `references/aima-ch2-map.md`)

| AIMA § | Concept | Used in |
|--------|---------|---------|
| 2.1 | agent, environment, sensors/actuators, percept, percept sequence, agent function vs agent program | 00 |
| 2.2 | performance measure (consequentialism), rationality (four factors), omniscience vs rationality, information gathering, learning, autonomy | 00, 04, 05 |
| 2.3.1 | PEAS task-environment description | every piece (PEAS box) |
| 2.3.2 | environment properties: observable, single/multi-agent, deterministic, episodic/sequential, static/dynamic, discrete/continuous, known/unknown | 00, every piece |
| 2.4 | agent = architecture + program | 00 (the sandbox *is* the architecture) |
| 2.4.1 | table-driven agent and why it cannot scale | 00 |
| 2.4.2 | simple reflex agent; condition–action rules; loops under partial observability; randomization as escape | 01 |
| 2.4.3 | model-based reflex agent; internal state; transition model; sensor model | 02 |
| 2.4.4 | goal-based agent; search and planning | 03 |
| 2.4.5 | utility-based agent; expected utility; model-free agents | 04 |
| 2.4.6 | learning agent: performance element, learning element, critic, problem generator; fixed performance standard | 05 |
| 2.4.7 | atomic / factored / structured representations; localist vs distributed | 00 (brief) |

---

## 3. Editorial line

### 3.1 Candidate theses for the hub (the author picks; do not use all of them)

- **Agent = architecture + program, updated.** An LLM-powered agent is an agent *program*; the harness plus the sandbox is the *architecture*. Changing the architecture (laptop → cloud) without touching the program is exactly what `sbx` / `sbx --cloud` allows.
- **Real agentic work is the "hardest case".** AIMA names partially observable, multi-agent, nondeterministic, sequential, dynamic, continuous and unknown as the hardest combination. A coding agent loose in a real repository with network access ticks most of those boxes — that is the argument for isolation.
- **Actuators need a fence.** Tools are actuators. A sandbox constrains actuators (filesystem, network egress, credentials) without rewriting the agent program.
- **The critic must sit outside.** AIMA insists the performance standard be fixed and outside the agent's control. With sandboxes this can be enforced physically: critic on the host, agent in the sandbox. Today's reward-hacking problem, in textbook vocabulary that predates LLMs by decades.
- **A sandbox's network policy is itself a simple reflex agent** (condition–action rules applied to each outbound request). Good one-liner; use it once.

### 3.2 Style

- Precise, plain, lightly wry. The title nods to Richard Feynman's *Six Easy Pieces*: the fundamentals look easy, the problems underneath never were, and since AIMA's first edition (1995) the hard problems of agents have barely moved. Use that irony, sparingly (author's note, session 04). No hype words ("revolutionary", "game-changer", "unleash", "supercharge").
- **Always state the why.** Every decision, sandbox feature and step comes with its reason, in articles, ADRs, journal entries and chat (author's standing request, session 02). In particular, say for each piece whether containment is actually needed, and why.
- No invented numbers. Every figure comes from a run we did (and is recorded in a `RUNINFO.json`) or from a cited source.
- Short paragraphs, one idea per section. Code excerpts in articles ≤ ~40 lines; full code lives in the repo.
- Every article ends with series navigation (hub · previous · next) and a "Reproduce it" box.
- Every article carries a disclosure line: written with assistance from Claude (Anthropic); code and runs reproducible from the linked repository at a given tag. Final wording is an author decision (record it as an ADR). **Decided: ADR-0013** (exact wording there).

### 3.3 Medium constraints (drafts must paste cleanly)

- Medium has no tables, no footnotes and only two heading levels. In `articles/*/article.md` use only `#` and `##`, no tables (use bullet lists or an image), no footnotes (inline links instead), short fenced code blocks.
- Diagrams: Mermaid sources in `articles/<id>/assets/*.mmd`, rendered to PNG (≥ 1400 px wide) with mermaid-cli. Commit both source and render.
- Charts: `scripts/plots.py` (`make plots-NN`, matplotlib in a git-ignored `.venv`), drawn only from a recorded run's `results.json` + `RUNINFO.json`, 1500 px wide, with a footer naming the run and an `assets/plots.json` provenance file. Colours from the illustration palette, validated with the dataviz checks: cerulean `#2F80C0` and coral `#E8574A` for series (coral is the agent that loops), a teal ramp `#84BFB8`→`#1F5C6B` for magnitude, plum-navy text. Comparisons across pieces use emphasis (the piece's own agent in colour, earlier agents in grey) rather than more hues.
- Links to code always point to a **tag**, never to `main` (e.g. `…/tree/piece-01-v1/examples/01-simple-reflex`), so published articles don't rot.

### 3.4 Skeleton of a short piece (01–05)

1. Hook — 2–3 sentences with a present-day example of this agent type.
2. What AIMA says — section reference, at most one short quote, explanation in our own words.
3. PEAS and environment properties — as a bullet list.
4. The agent program — ≤ 40-line excerpt, link to the full code at the tag.
5. Run it in a sandbox — cloud commands first, then one line for the local equivalent ("same script, `SBX_TARGET=local`"). Until ADR-0010 is lifted: cloud commands only, plus one line saying a locally tested version will follow.
6. What the sandbox adds here — exactly one Docker Sandboxes feature (see §4).
7. Why it still matters — 2–3 sentences: today's twin of this agent type.
8. Reproduce it — repo tag, `sbx` version, template or kit reference, the one command.
9. Series navigation.

---

## 4. The five pieces — implementation plan

**Design principle: same world, five agent programs, one architecture.** All pieces share a small environment package (`examples/_shared/worlds/`) based on AIMA's vacuum world, generalized to an N×M grid with switches for partial observability, stochastic actions and dynamic dirt. Each piece adds one agent program and showcases one sandbox feature.

**Language and dependencies:** Python 3.12, **standard library only** for environments and agent cores, tests with `unittest`. Nothing needs installing inside a sandbox for the deterministic path. Optional LLM variants (decision D2) live in a separate `agent_llm/` subfolder with their own pinned dependencies.

**Decided in ADR-0011 (overrides the twin columns below):** one mode per piece, no dual versions. 01 and 02 are deterministic, with no LLM. 03, 04 and 05 are LLM agents via OpenRouter and have no deterministic core; their code lives in `agent/`, with no `agent_llm/`. One-page summary: `site/pieces.md`.

| Piece | AIMA | Deterministic core (no LLM) | Optional today's twin (LLM, D2) | Sandbox feature showcased |
|-------|------|-----------------------------|---------------------------------|---------------------------|
| 01 Simple reflex | §2.4.2 | Condition–action rules on the current percept; demonstrate the infinite loop under partial observability and the randomized escape | Rule-based guardrail or hook — or simply observe that the sandbox's network policy *is* a reflex agent | Disposability: create, run, remove; identical output local vs cloud |
| 02 Model-based reflex | §2.4.3 | Internal state + transition model + sensor model; state persisted to a file | Agent with a persistent memory file | Persistence: stop/resume keeps state (`sbx stop` locally; `sbx --cloud stop` preserves memory and filesystem); `template save` as a snapshot |
| 03 Goal-based | §2.4.4 | BFS / A* planner reaching a goal state on the grid | A coding agent inside a sandbox whose goal is a test predicate ("all tests pass") | Network policy: deny by default, explicit allowlist; repository cloned inside the sandbox |
| 04 Utility-based | §2.4.5 | Expected-utility action selection on the stochastic grid (one-step lookahead or small value iteration) | Best-of-N candidates scored by a utility function (quality, diff size, runtime, **cloud cost**) | Parallel sandboxes + resource sizes (`--cpus`/`--memory`) + `--ttl`/`--on-timeout delete` as a cost term in the utility |
| 05 Learning | §2.4.6 | Tabular Q-learning (model-free); separate critic with a fixed performance standard; problem generator = ε-exploration | Agent that rewrites its own instruction file from critic feedback — bridge to article 06 and to this very CLAUDE.md | Critic isolation: critic outside, agent inside; artifacts exchanged via `sbx cp` / `sbx --cloud cp`; locally the critic can also be mounted read-only (`:ro`) |

Each example directory:

```
examples/0N-<name>/
├── README.md     # what it shows, how to run (mirrors the article's Reproduce box)
├── agent/        # the agent program (stdlib only)
├── agent_llm/    # optional LLM variant (only if D2 = yes)
├── tests/        # unittest; must pass on the host AND inside a sandbox
├── run.sh        # thin wrapper around scripts/sbx-run.sh with this example's settings
├── policy.md     # network policy for this example and why (usually: no egress at all)
└── out/          # git-ignored: run outputs + RUNINFO.json
```

---

## 5. Execution environment: Docker Sandboxes

### 5.1 Facts (checked on 2026-10-21 — re-verify before publishing, see §5.5)

- **Docker Sandboxes** runs AI agents in isolated **microVMs**. The CLI is the standalone **`sbx`** (a single binary that also runs the `sandboxd` daemon). Each sandbox has its own kernel, filesystem, network and private Docker daemon. Docker Desktop is not required; Docker Desktop's older `docker sandbox` plugin is deprecated in favour of `sbx`.
- Built-in agents include `claude`, `codex`, `copilot`, `cursor`, `gemini`, `kiro`, `opencode`, `docker-agent` and **`shell`** (a Bash login shell with no agent pre-installed — what the deterministic examples use locally).
- **Local sandboxes** need hardware virtualization: x86_64 Linux (Ubuntu 24.04+) with KVM (`/dev/kvm`, user in the `kvm` group), macOS 14+ on Apple silicon, or Windows 11.
- **Cloud sandboxes** (`sbx --cloud …`, requires `sbx` ≥ 0.45.0) run on Docker-managed infrastructure and need an active **Docker Agentic Platform** subscription (labelled experimental in the docs at the time of writing); compute is pay-as-you-go. Differences from local that matter here:
  - No host workspace mounts, no `--clone`, no `--branch` worktrees, no host port bindings. Move files with `sbx --cloud cp` (absolute sandbox paths) or `git clone` inside the sandbox.
  - Separate stores for secrets, network policy, templates and volumes (`sbx --cloud secret …`, `sbx --cloud policy …`). Nothing configured locally carries over.
  - Default size 2 CPU / 4 GiB; fixed sizes from 1 CPU / 2 GiB up to 16 CPU / 32 GiB via `--cpus` / `--memory`.
  - Default TTL 1 h. Set `--ttl` and `--on-timeout stop|restart|delete` at creation; extend with `sbx --cloud ttl +30m <name>` (never beyond 24 h from creation).
  - Cloud sandbox names: letters, digits and hyphens only (no periods); `default` is reserved.
  - Published ports become public HTTPS URLs — treat them as public.
  - Known limitation: inside a cloud sandbox, `docker exec`, `docker compose exec` and Docker healthchecks may hit the VM filesystem instead of the container's. Keep examples off those paths.
  - `sbx move <name> --to cloud|local` copies a sandbox filesystem between backends.
- Headless sign-in: `echo "$DOCKER_PAT" | sbx login --username "$DOCKER_ID" --password-stdin`. On Linux without a desktop keyring, `sbx` stores credentials under `~/.config/com.docker.sandboxes` — outside the repo; keep it that way.
- **Terminology in articles:** "Docker Sandboxes", "`sbx`", "cloud sandboxes (`sbx --cloud`)". Do **not** call them "Docker Cloud", and do not confuse them with **Docker Offload** (Docker Desktop's cloud container engine) or **Docker Build Cloud** — different products.

### 5.2 Execution tiers

- **Tier C — cloud sandboxes (primary in the articles).** Run from the Codespace with `sbx --cloud`. This is the "independent of your laptop" story.
- **Tier L — local sandboxes (reader fallback).** Same scripts, `SBX_TARGET=local`, on any KVM-capable machine. The Codespace qualifies only if `/dev/kvm` is present and usable inside the devcontainer: test once, record the result in the journal, and never work around its absence with privileged hacks.
- **Tier T — self-hosted cloud VM via Terraform (optional, decision D1).** A KVM-capable VM (nested virtualization or bare metal) provisioned with Terraform; cloud-init installs `docker-sbx`; then Tier L runs there. **Write no Terraform until the author has chosen a provider.** If it happens: `infra/terraform/<provider>/`, remote state not in git, `*.tfvars` git-ignored, and a documented `make destroy` next to every `make apply`.
- **CI:** host-side checks only (`.github/workflows/test.yml`: unit tests on Python 3.12 and 3.14, `make lint`, `make article-check`, `make site-check`, and a site build on every pull request; no sandboxes, no secrets). **Sandboxes in CI: ADR-0014.** `.github/workflows/sandbox.yml` runs the deterministic pieces in a real cloud sandbox after each merge to `master` and on demand, never on pull requests. Docker credentials sit in the `cloud-sandboxes` environment, limited to `master`. LLM pieces run there against a fake model, and CI holds no OpenRouter key.

### 5.3 One wrapper for all examples: `scripts/sbx-run.sh`

All examples run through one script so cloud and local behave the same:

- Inputs: `SBX_TARGET=cloud|local` (default `cloud`), example directory, entry command, optional size and TTL.
- Sandbox name: `fep-<piece>-<shortsha>`.
- **Copy-in / copy-out in both tiers** (mountless sandbox + `sbx cp` / `sbx --cloud cp`) instead of bind mounts, so semantics are identical locally and in the cloud. Sandbox paths must be absolute; Docker-provided templates use `/home/agent/workspace`.
- Candidate sequences (verify each with `--help` before relying on it):
  - local: `sbx create --name <n> shell` (mountless) → `sbx run -d --name <n>` (keep it running) → `sbx cp` in → `sbx exec <n> …` → `sbx cp` out → `sbx rm --force <n>`.
  - cloud: `sbx --cloud create --name <n> --ttl <t> --on-timeout delete <agent>` → `sbx --cloud cp` in → `sbx --cloud exec --workdir … <n> …` → `sbx --cloud cp` out → `sbx --cloud rm --force <n>`. Check whether `shell` is accepted with `--cloud`; if not, use a built-in agent template and only `exec` into it, or a kit.
- Check that `python3` exists in the chosen template before relying on it. If it doesn't, build a kit or template — never `pip install` at run time.
- `trap` on EXIT removes the sandbox.
- Writes `out/RUNINFO.json`: UTC timestamp, tier, `sbx version`, template/kit reference, size, git commit, exit code, wall-clock duration.
- Fails loudly with a clear message if `sbx` is missing, not signed in, KVM is absent (local) or cloud access isn't enabled (`sbx --cloud diagnose`).

### 5.4 Credentials and network

- Deterministic cores need **no network**. Run them with egress blocked and say so in `policy.md`.
- LLM variants: store keys with `sbx secret set …` / `sbx --cloud secret set …` so the host-side proxy injects them and the agent never sees the raw value. For OpenRouter in the cloud, the docs require a custom secret (`sbx --cloud secret set-custom --host openrouter.ai --env OPENROUTER_API_KEY`); verify on first use (ADR-0011). Allow only the provider host(s) needed. Never pass keys via `-e`, env files or files inside the sandbox — they would end up in saved templates.
- Before any `template save`, confirm the sandbox filesystem holds no credentials.

### 5.5 Verification protocol for anything `sbx`

1. Run `sbx version` in the Codespace and record it.
2. Run `sbx <command> --help` for every subcommand and flag used.
3. Cross-check the official docs at https://docs.docker.com/ai/sandboxes/ (appending `.md` to a docs URL returns raw Markdown) and the release notes at https://github.com/docker/sbx-releases/releases.
4. Put `verified_with: "sbx vX.Y.Z (YYYY-MM-DD)"` in the article front matter and in the example README.
5. If docs and `--help` disagree, trust `--help` and note the discrepancy in the journal.

---

## 6. Development environment (Codespace / devcontainer)

- Base image: Ubuntu 24.04 (required by the `docker-sbx` apt package). Features: Python 3.12, Node LTS (for mermaid-cli and Claude Code), GitHub CLI. Terraform only if D1 = yes.
- `postCreateCommand` → `scripts/post-create.sh`: install `docker-sbx` from Docker's apt repository (`curl -fsSL https://get.docker.com | sudo REPO_ONLY=1 sh` then `sudo apt-get install -y docker-sbx`), install mermaid-cli, then run `scripts/check-env.sh`. Check the current Claude Code install method in Anthropic's docs rather than hard-coding one from memory.
- `scripts/check-env.sh` is read-only and reports: `sbx version`; whether `/dev/kvm` exists and is accessible; whether `sbx` is signed in; the result of `sbx --cloud diagnose`; the Python version.
- Codespaces secrets the author may define (never committed): `DOCKER_ID`, `DOCKER_PAT`, and `OPENROUTER_API_KEY` (for pieces 03–05, ADR-0011). Scripts read them from the environment and hand them straight to `sbx login` / `sbx secret`.
- Claude Code runs in the Codespace, not inside a sandbox, unless decision D5 says otherwise.

---

## 7. Repository layout

```
.
├── CLAUDE.md                 # this file
├── README.md                 # public entry point: series, examples, how to reproduce
├── LICENSE                   # code license (D4); article text license stated separately
├── Makefile                  # check-env, test, run-0N, diagrams, site-check
├── .gitignore
├── .devcontainer/            # devcontainer.json + references to scripts/post-create.sh
├── .claude/commands/         # project slash commands (§9.4)
├── .github/workflows/
│   ├── pages.yml             # build site/ with Jekyll, deploy to GitHub Pages
│   └── test.yml              # host-side unit tests (no sandboxes, no secrets)
├── articles/
│   ├── 00-hub/               # article.md + assets/
│   ├── 01-simple-reflex/
│   ├── 02-model-based/
│   ├── 03-goal-based/
│   ├── 04-utility-based/
│   ├── 05-learning/
│   └── 06-making-of/
├── examples/
│   ├── _shared/worlds/       # vacuum / grid world, stdlib only
│   └── 01-simple-reflex/ … 05-learning/
├── scripts/                  # sbx-run.sh, check-env.sh, post-create.sh, new-journal.sh
├── references/               # bibliography.md, aima-ch2-map.md, sbx-notes.md
├── infra/terraform/          # only if D1 = yes
└── site/                     # GitHub Pages source: the making-of
    ├── _config.yml
    ├── index.md              # what this is, series status, latest journal entries
    ├── workflow.md           # living description of the workflow
    ├── journal/              # one entry per session (Claude writes)
    ├── decisions/            # ADRs
    ├── prompts/              # notable prompts, in English, with context
    ├── assets/img/           # screenshots, rendered diagrams
    └── _data/
        ├── series.yml        # status of every article and example (single source of truth)
        └── metrics.yml       # running counters for article 06
```

Article front matter (kept in the repo; strip it before pasting into Medium):

```yaml
---
id: "01"
title: "…"
status: idea | outline | draft | review | ready | published
drafted_by: claude | author | both
edited_by: author
verified_with: "sbx vX.Y.Z (YYYY-MM-DD)"
code_tag: piece-01-v1
medium_url: ""
---
```

---

## 8. Git conventions

- Conventional commits scoped by area: `docs(00): …`, `feat(ex-03): …`, `test(ex-05): …`, `chore(site): …`, `journal: …`, `adr: …`, `infra: …`.
- Small commits. Journal entries are committed on their own (`journal: session 01`).
- Before the project's first commit, show the author the configured identity (`git config user.name`, `git config user.email`) and wait for confirmation. Never modify it.
- Tag `piece-0N-v1` when a piece's code is frozen for publication; the article links to that tag.
- `.gitignore` must cover at least: `.env*`, `out/`, `.sbx/`, `*.tfstate*`, `*.tfvars`, `.terraform/`, `node_modules/`, `__pycache__/`, `_site/`.

---

## 9. Keeping the record (the making-of)

Not busywork: article 06 and the GitHub Page are *made of* this record. Write it as you go, factually, including what went wrong.

### 9.1 Journal entries — `site/journal/YYYY-MM-DD-NN-<slug>.md`

One per session, written at the end (or on `/wrap`):

```markdown
---
layout: post
title: "Session NN — <what happened, in a few words>"
date: YYYY-MM-DD
session: NN
pieces: ["01", "03"]              # articles/examples touched
sbx_version: "vX.Y.Z"
model: "<model reported by Claude Code>"
sandbox_runs: { cloud: N, local: N }
---

## Goal
The author's request, paraphrased in English. If the prompt was in another
language, add "(translated from Italian)".

## What we did
Concrete outcomes, with links to commits and files.

## Commands that mattered
Copied from scripts / Makefile, never retyped from memory.

## Decisions
Links to ADRs created or changed.

## Dead ends and surprises
What did not work and why. Keep these: they are the best material for article 06.

## Who did what
Claude drafted … / the author rewrote … / the author decided …

## Next
One to three next steps.
```

### 9.2 Other records

- **ADRs** — `site/decisions/ADR-NNNN-<slug>.md`: context, options considered, decision, consequences. Every answer to an open decision in §12 becomes an ADR.
- **Prompts** — `site/prompts/`: only prompts that changed the direction of the work, rendered in English, with one line of context and a link to the journal entry. No secrets, no personal data.
- **`site/workflow.md`** — the current workflow in prose plus one Mermaid diagram (Codespace → Claude Code → `sbx` → cloud sandbox → results back → article). Update it whenever the workflow changes and note the change in the journal.
- **`site/_data/series.yml`** — per article and per example: `status`, `code_tag`, `medium_url`, `last_session`. Updated at the end of every session.
- **`site/_data/metrics.yml`** — running counters for article 06: sessions, commits, journal entries, sandbox runs per tier, approximate cloud sandbox minutes, notable failures. Real numbers only.
- **Screenshots** (e.g. the `sbx` TUI) — `site/assets/img/`, with alt text. Check them for secrets, account IDs and personal information before committing.

### 9.3 README badges: add each one when it becomes true

Badges in `README.md` must say something checkable. The backlog below was agreed with the author in session 04; add each badge on your own as soon as its trigger has happened, and note it in the journal. Use the illustration palette for colours. No vanity badges (stars, downloads): they say nothing about reproducibility.

- [ ] **Open in GitHub Codespaces** (`https://github.com/codespaces/badge.svg`) — when a fresh Codespace has been built from `.devcontainer/` and `make check-env` passes in it.
- [ ] **Latest tag** (shields.io `github/v/tag`) — when `piece-01-v1` exists.
- [ ] **Articles published N/7** (shields.io dynamic YAML badge reading `site/_data/series.yml`) — after the first article is published.
- [ ] **Local sandboxes tested** — when ADR-0010 is lifted.
- [x] **Cloud sandbox run** (GitHub's badge for `sandbox.yml`) — after its first successful run on `master` (ADR-0014). Added in session 06, after run 40570668299 passed.
- [ ] **OpenRouter spend** (shields.io dynamic YAML badge reading `site/_data/metrics.yml`) — optional, once pieces 03–05 start spending.

### 9.4 Project slash commands (create during bootstrap; keep in sync with this file)

- `/status` — read `series.yml` and the latest journal entry; summarize where things stand; propose the next step.
- `/wrap` — write the journal entry, update `series.yml` and `metrics.yml`, list live cloud sandboxes, commit with `journal:`.
- `/verify-sbx <article-or-example>` — run the §5.5 protocol on every `sbx` command it uses.
- `/new-piece <NN>` — scaffold `articles/<NN>-…` and `examples/<NN>-…` from the skeletons in §3.4 and §4.

---

## 10. Session protocol

1. **Start:** read this file, `site/_data/series.yml` and the latest journal entry. If the previous session has no journal entry, write it first. State in three bullets what this session will do.
2. **Work:** small steps; run `make test` after touching examples; run sandboxes only through `scripts/sbx-run.sh`.
3. **Before writing article prose about an example:** the code exists, its tests pass on the host and in at least one sandbox tier, and `RUNINFO.json` exists. Articles describe runs that actually happened.
4. **End:** `/wrap`.

---

## 11. Definition of done

**Example 0N:** stdlib-only core; `unittest` passes on the host and inside a sandbox; runs with `SBX_TARGET=cloud` and `SBX_TARGET=local` (or the README honestly says "local tier not tested: no KVM available"; until ADR-0010 is lifted, cloud only and the README says the local version will follow once tested); `policy.md` written; README contains the Reproduce box; tag created.

**Article 0N:** `make article-check` passes at status `review` (it enforces the mechanical rules below); within target length; Medium-safe formatting (§3.3); within the quote budget (§2.2); every `sbx` command verified (§5.5) and copied from the scripts; code links point to the tag; diagrams original; disclosure line present; reviewed by the author; `series.yml` updated.

**Site:** builds via `pages.yml`; the index shows series status; every session has a journal entry; `workflow.md` is current.

---

## 12. Open decisions (ask the author; record each answer as an ADR)

- **D1** Tier T (Terraform-provisioned VM): keep or drop? If kept, which provider and region? → **dropped** (ADR-0003)
- **D2** LLM today's-twin variants for pieces 03–05 (and 01–02?): yes or no; provider and model; budget cap. → **one mode per piece: 01–02 without LLM, 03–05 LLM via OpenRouter** (ADR-0011, supersedes ADR-0004)
- **D3** Site generator: plain GitHub Pages with Jekyll built in Actions (proposed — zero extra tooling) or something else. → **Jekyll in Actions** (ADR-0005)
- **D4** Repository name, `<AUTHOR_HANDLE>`, code license (proposed: MIT) and article-text license (proposed: CC BY 4.0, excluding quoted AIMA material). → **as proposed; handle `andreagalle`** (ADR-0006)
- **D5** Dogfooding: should Claude Code itself run inside a sandbox (`sbx run claude` / `sbx --cloud run claude`) for some sessions? Strong material for article 06, but it changes the workflow. → **absolutely not** (though the correct answer would have been yes; ADR-0009)
- **D6** Publication order and cadence on Medium (hub first with "coming soon" links, or pieces first). → **hub + 01 together, then weekly, 06 last** (ADR-0007)
- **D7** Publish on the author's own Medium profile or in a Medium publication. → **Docker Captains Wisdom publication** (ADR-0008)

---

## 13. Bootstrap (first session only — tick items here as they are done)

- [x] Create and run `scripts/check-env.sh`; keep the output for journal session 01.
- [x] Create the §7 layout with placeholder READMEs, `.gitignore`, `Makefile`, `.devcontainer/`, `.claude/commands/`, `pages.yml`, `test.yml`.
- [x] Seed `references/aima-ch2-map.md` from §2.3 and `references/bibliography.md` from §2.1; start `references/sbx-notes.md` from §5.1.
- [x] Create `site/` with `_config.yml`, `index.md`, a first `workflow.md`, `_data/series.yml` (every item `idea`) and `_data/metrics.yml`.
- [x] Write ADR-0001 "Execution tiers" (§5.2) and ADR-0002 "Same world, five programs" (§4).
- [x] Ask the author D1–D7 in a single message; record the answers as ADRs. (D5 still open after session 01.)
- [x] Show the git identity, wait for confirmation, then make the first commit.
- [x] Write journal session 01 and commit it.
