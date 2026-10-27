---
id: "00"
title: "Five Easy Pieces on Agentic AI w/ Docker Sandboxes"
status: draft
drafted_by: claude
edited_by: author
verified_with: "sbx v0.50.0 (2026-10-26)"
code_tag: ""
medium_url: ""
---

# Five Easy Pieces on Agentic AI w/ Docker Sandboxes

*AI agents got a parts list in 1995. Since then the parts have grown enormously. The hard problems haven't moved an inch, and they were never the easy pieces.*

![Five glass spheres stand in a row on a seabed, each holding a small fish above a grid of stones. The glass grows thicker from left to right, and the last sphere is sealed. High above, a whale glides through shafts of light.](assets/header.jpg)

*AI-generated illustration.*

Today "agent" usually means a large language model with tools. The word is older than that. Something that perceives, decides and acts, again and again, in a world it doesn't fully control, was laid out in Chapter 2 of Stuart Russell and Peter Norvig's *Artificial Intelligence: A Modern Approach*. The book was first published in 1995 and is now in its fourth edition. The chapter is short, it predates large language models by decades, and its vocabulary still fits.

This series is this hub plus five short pieces. Each piece takes one of the book's agent types, implements it as a small program, and runs it in a Docker Sandbox: a disposable microVM you create, use and throw away, on your machine or in the cloud, with the same commands. One question runs through all of them, one the textbook had no reason to ask: when does an agent actually need a fence?

The title borrows from Richard Feynman's *Six Easy Pieces*: six chapters from his 1960s physics lectures, published as a book in the mid-1990s, at about the time AIMA first appeared. Feynman's pieces were easy only in a particular sense. They were the fundamentals, stated so plainly that they looked simple, with everything hard about physics sitting right underneath.

These five are easy in the same sense. The agent programs are small. What they run into is the hard part:

- a world they can only partly see;
- a performance measure that has to say what you actually want;
- a judge the agent mustn't be able to reach.

None of that is new. It has been the hard part since the beginning.

## What AIMA calls an agent

An agent, in the book's sense, is anything that perceives its environment through sensors and acts on it through actuators (AIMA 4e, §2.1):

- **Percept:** what it senses at a given instant.
- **Percept sequence:** everything it has ever sensed.
- **Agent function:** its behaviour, described abstractly as a mapping from every possible percept sequence to an action.
- **Agent program:** the concrete thing that implements that function, running on some physical system.

Keep that distinction in mind, function versus program, because the series hangs on it. A thermostat, a chess engine and a coding assistant are all agents. What separates them is the program, and what the program is allowed to touch.

## Rational is not the same as all-knowing

The book judges an agent by consequences (§2.2). A performance measure scores the sequence of states the agent's actions produce in the environment, not what the agent meant to do. The running example is a robot vacuum cleaner that earns a point for every clean square at every time step. The series scores its vacuum agents with exactly that measure.

A rational agent, in this vocabulary, picks the action it expects to score best, given what it has perceived so far and what it knows in advance. That isn't omniscience: a rational agent can be wrong about what it couldn't see. It isn't a free pass either. A rational agent gathers information when that's worth it, learns from what happens, and becomes more autonomous the less it relies on what its designer built in.

Two ideas from this section come back later in the series:

- A performance measure should describe what you want the world to look like, not how you want the agent to behave.
- The standard an agent is judged by has to stay out of the agent's reach. Piece 5 depends on this one.

## Four letters and seven questions

Before writing an agent, the book asks you to describe its task environment as **PEAS**: Performance measure, Environment, Actuators, Sensors (§2.3). Then it asks seven questions about that environment:

- Can the agent observe all of it, or only part?
- Is it acting alone, or alongside other agents?
- Is the next state fully determined by the current one and the action?
- Is each decision separate, or does it shape the next?
- Does the world change while the agent is deliberating?
- Are states and actions discrete or continuous?
- Does the agent know how the environment works?

The hardest case is the one where every answer is the uncomfortable one: partially observable, multi-agent, nondeterministic, sequential, dynamic, continuous and unknown. Now picture a coding agent with a shell, inside a real repository, with network access. Checked against the list:

- It sees only part of a large codebase.
- It shares that codebase with people and other tools.
- The same request doesn't always give the same result.
- Every edit shapes the next one.
- The repository and its dependencies change underneath it.
- It can't know in advance what a command will do.

That's most of the hardest case, with real actuators attached. Every piece in the series opens with its own PEAS description and its answers to these questions.

## Agent = architecture + program

The book's shortest equation is the one this series is built on: an agent is an **architecture** plus a **program** (§2.4). The program implements the agent function. The architecture is what the program runs on, a computing device with sensors and actuators, which hands the program its percepts and carries out its actions.

Read that today and the mapping is direct. An LLM agent (the model, its prompt and its loop) is an agent program. What it runs on, down to which files it can write, which hosts it can reach and which credentials it can use, is its architecture. Change the architecture, and the same program can do different things to the world.

Docker Sandboxes make the architecture something you can create and destroy on demand:

- **Isolation:** each sandbox is a microVM with its own kernel, filesystem, network and Docker daemon.
- **One tool:** a single command-line program, `sbx`, drives them all.
- **Local or cloud:** the same commands work on your machine and, with `sbx --cloud`, on Docker's infrastructure.

Moving a program to a different architecture is literally a flag.

Piece 1 checks that claim before the series relies on it. Its program writes a deterministic report. That report came out byte for byte identical in my Codespace and in a cloud sandbox, under a different Python version, with the sandbox's network switched off.

Why not skip the program altogether and use a lookup table from percept sequences to actions? The book's answer (§2.4.1) is that the table would need an entry for every possible history, and the number of histories explodes long before the world gets interesting. Programs exist because tables can't scale.

## Five easy pieces

The book describes four basic kinds of agent program, each able to do something the previous one can't, and then shows how any of them can become an agent that learns. That makes five pieces.

All five live in the same small world, the book's vacuum cleaner generalized to a grid, so you can compare them. Each one swaps in a new program and shows one thing a sandbox can do:

- **Piece 1, the simple reflex agent (§2.4.2).**
  - *What it does:* acts on the current percept alone, through condition–action rules. Take away its location sensor and it loops forever; a coin flip breaks the loop.
  - *What the sandbox shows:* disposability. Create, copy in, run, copy out, delete.
  - *Does it need a fence?* No.
- **Piece 2, the model-based reflex agent (§2.4.3).**
  - *What it does:* keeps internal state about what it can't currently see, so it sweeps the grid instead of wandering.
  - *What the sandbox shows:* persistence. The state survives stopping and restarting the sandbox.
  - *Does it need a fence?* Still no.
- **Piece 3, the goal-based agent (§2.4.4).**
  - *What it does:* searches for actions that reach a goal. Here it will be an LLM agent writing code until a test suite passes.
  - *What the sandbox shows:* network policy. Deny everything, then allow one host.
  - *Does it need a fence?* Yes, for the first time.
- **Piece 4, the utility-based agent (§2.4.5).**
  - *What it does:* weighs the outcomes it prefers against what they cost. Here several LLM-written candidates will run, each in its own sandbox, scored on quality, model cost and sandbox minutes.
  - *Does it need a fence?* Yes, once per candidate.
- **Piece 5, the learning agent (§2.4.6).**
  - *What it does:* a critic, held to a fixed standard, tells the agent how it's doing, and the agent rewrites its own instructions.
  - *What the sandbox shows:* the critic stays outside and the agent stays inside.
  - *Does it need a fence?* That's the whole point.

One more idea from the end of the chapter (§2.4.7) changes along the way: how the agent represents its world. The first two pieces use a factored state, a position plus a few clean-or-dirty flags. The last three hand an LLM a structured world of files, functions and tests.

## Why the first two pieces have no LLM

Pieces 1 and 2 are deterministic Python programs, standard library only, with no model inside. That's deliberate, for two reasons:

- **An LLM isn't needed there.** The simple reflex agent's lesson is one rule and the loop it causes. The model-based agent's lesson is a few lines of explicit state. In both cases you can point at the line responsible, and a model would hide exactly what the pieces are about.
- **It keeps the complexity down.** With nothing unpredictable running, those pieces can concentrate on containment itself: how a sandbox is created, fed, run, emptied and destroyed, and how state survives in it.

We sandbox those two programs even though they don't need it, and the pieces say so. Learning the mechanics where nothing can go wrong is what makes it obvious, from piece 3 on, when they become indispensable. That's when the program starts running code nobody has read, needs the network to reach its model, and will optimize whatever it can reach.

## Run it yourself

Everything in the series is in [one repository](https://github.com/andreagalle/five-easy-pieces-agentic-ai). Open it in a GitHub Codespace and run:

```bash
make check-env   # what this machine can run
make run-01      # piece 1 in a cloud sandbox
```

Cloud sandboxes need a Docker account with cloud sandboxes enabled. At the time of writing that's part of Docker's Agentic Platform, which Docker labels experimental. Every run leaves a `RUNINFO.json` behind: what ran, where, on which versions, and how it ended. The numbers in these articles come from those files.

Local sandboxes use exactly the same scripts on a machine with hardware virtualization. I haven't tested that path yet, so I'm not publishing it yet. A locally tested version will follow.

The series also has a [making-of site](https://andreagalle.github.io/five-easy-pieces-agentic-ai/). It has a journal entry for every working session, every decision with its reasons, and the dead ends, including the ones that were Claude's.

## A note on sources

The series follows the fourth edition of the book (Pearson, 2020) and cites it by section number. I read it in the Italian translation (Pearson Italia), and the sources I checked don't say whether that translation was made from the US or the Global Edition. Section numbers were checked against it.

Because I can't check the English wording against my copy, I paraphrase rather than quote. The ideas are the authors'; the sentences here are paraphrases. For a free summary of the chapter, Z. Yu's [study notes](https://artificialintelligence.readthedocs.io/en/latest/part1/chap2.html) are a good companion. They skip a heading for §2.4.4, but the text is there.

## The series

- **Five Easy Pieces on Agentic AI w/ Docker Sandboxes** (you are here)
- Piece 1/5 — The simple reflex agent (link added at publication)
- Piece 2/5 — The model-based reflex agent (coming soon)
- Piece 3/5 — The goal-based agent (coming soon)
- Piece 4/5 — The utility-based agent (coming soon)
- Piece 5/5 — The learning agent (coming soon)
- The making of: Claude, Docker Sandboxes and a Codespace (coming soon)

*Disclosure: I'm a Docker Captain, and I'm enthusiastic about this technology. This article was written with the assistance of Claude (Anthropic), and the header image is AI-generated (Google's Nano Banana 2, via OpenRouter). The code and the full making-of live in [five-easy-pieces-agentic-ai](https://github.com/andreagalle/five-easy-pieces-agentic-ai).*
