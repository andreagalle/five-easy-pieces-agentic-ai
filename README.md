# five-easy-pieces-agentic-ai

AIMA's five agent types (simple reflex → learning), running in Docker Sandboxes, locally or in the cloud. Code, Medium drafts, and a making-of site built with Claude Code.

**Status:** bootstrapping. No article is published and no example runs yet. Current status: [`site/_data/series.yml`](site/_data/series.yml).

## The series

- **00** — Five Easy Pieces on Agentic AI w/ Docker Sandboxes (hub)
- **01** — The simple reflex agent → [`examples/01-simple-reflex/`](examples/01-simple-reflex/)
- **02** — The model-based reflex agent → [`examples/02-model-based/`](examples/02-model-based/)
- **03** — The goal-based agent → [`examples/03-goal-based/`](examples/03-goal-based/)
- **04** — The utility-based agent → [`examples/04-utility-based/`](examples/04-utility-based/)
- **05** — The learning agent → [`examples/05-learning/`](examples/05-learning/)
- **06** — The making of: Claude, Docker Sandboxes and a Codespace

The argument in one line: Chapter 2 of Russell & Norvig's *Artificial Intelligence: A Modern Approach* already gave us the vocabulary for today's agentic AI. Docker Sandboxes give each agent *program* a disposable, reproducible *architecture* to run in, on a laptop or in the cloud, with the same commands.

## Repository

- `examples/` — one stdlib-only Python program per agent type, sharing one grid world (`examples/_shared/worlds/`)
- `articles/` — Medium drafts with their diagram sources
- `scripts/` — environment checks and the sandbox wrapper
- `references/` — bibliography, AIMA Chapter 2 concept map, `sbx` notes
- `site/` — the making-of: journal, decisions, workflow (GitHub Pages)

## Reproduce

Open the repository in a GitHub Codespace (or any Ubuntu 24.04 devcontainer), then:

```bash
make check-env   # what this machine can run: cloud sandboxes, local sandboxes, neither
make test        # host-side unit tests
```

Running examples in sandboxes (`make run-NN`) arrives with the first example.

## Licence

- Code: MIT, see [`LICENSE`](LICENSE).
- Article text and site prose: CC BY 4.0, see [`LICENSE-text.md`](LICENSE-text.md). Quoted material from *AIMA* and other cited works is excluded and stays under its owners' copyright.

The articles will appear in the Medium publication [Docker Captains Wisdom](https://medium.com/docker-captains-wisdom), by andreagalle.
