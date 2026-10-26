"""Run the piece 01 scenarios and write a deterministic report.

    python3 -m agent.run [--out DIR]

Prints a summary and writes DIR/results.json. Nothing in the output depends on the
machine, the time or the Python version, so the same code gives byte-identical
results on the host and in a sandbox.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Sequence

from worlds import MOVES, AgentProgram, Episode, Location, Percept, VacuumWorld, WorldConfig, run_episode

from .programs import RandomizedReflexAgent, blind_reflex_agent, reflex_vacuum_agent

TWO_SQUARES = [(0, 0), (1, 0)]
GRID = [(x, y) for y in range(4) for x in range(4)]


@dataclass(frozen=True)
class Scenario:
    name: str
    description: str
    config: WorldConfig
    start: Location
    dirty: Sequence[Location]
    make_program: Callable[[], AgentProgram]
    steps: int
    show_trace: bool = False


SCENARIOS = [
    Scenario("sighted", "location sensor on, two squares",
             WorldConfig(), (0, 0), TWO_SQUARES, lambda: reflex_vacuum_agent, 10, True),
    Scenario("blind", "location sensor off, same rules",
             WorldConfig(sense_location=False), (1, 0), TWO_SQUARES, lambda: blind_reflex_agent, 10, True),
    Scenario("blind-random", "location sensor off, coin flip on clean squares",
             WorldConfig(sense_location=False), (1, 0), TWO_SQUARES, lambda: RandomizedReflexAgent(seed=1), 10, True),
    Scenario("grid-blind", "4x4 grid, location sensor off, same rules",
             WorldConfig(width=4, height=4, sense_location=False), (0, 0), GRID, lambda: blind_reflex_agent, 200),
    Scenario("grid-random", "4x4 grid, location sensor off, random move on clean squares",
             WorldConfig(width=4, height=4, sense_location=False), (0, 0), GRID,
             lambda: RandomizedReflexAgent(seed=1, moves=tuple(MOVES)), 200),
]


def percept_label(percept: Percept) -> str:
    """AIMA-style percept, e.g. [A, Dirty]; '?' when the location sensor is off."""
    names = {(0, 0): "A", (1, 0): "B"}
    where = "?" if percept.location is None else names.get(percept.location, str(percept.location))
    parts = [where, "Dirty" if percept.dirty else "Clean"] + (["Bump"] if percept.bumped else [])
    return "[" + ", ".join(parts) + "]"


def summarize(scenario: Scenario, episode: Episode) -> dict:
    return {
        "name": scenario.name,
        "description": scenario.description,
        "world": f"{scenario.config.width}x{scenario.config.height}",
        "steps": scenario.steps,
        "score": episode.score,
        "max_score": episode.max_score,
        "all_clean_at": episode.all_clean_at,
        "final_dirty": [list(square) for square in episode.final_dirty],
        "actions": [step.action.value for step in episode.steps],
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", default="out", help="directory for results.json (default: out)")
    args = parser.parse_args(argv)

    results = []
    for scenario in SCENARIOS:
        world = VacuumWorld(scenario.config, scenario.start, scenario.dirty)
        episode = run_episode(world, scenario.make_program(), scenario.steps)
        results.append(summarize(scenario, episode))

        cleaned = f"all clean at step {episode.all_clean_at}" if episode.all_clean_at else \
            f"{len(episode.final_dirty)} square(s) still dirty"
        print(f"{scenario.name:<13} {scenario.description}")
        print(f"{'':<13} score {episode.score}/{episode.max_score}, {cleaned}")
        if scenario.show_trace:
            for step in episode.steps[:6]:
                print(f"{'':<15} {percept_label(step.percept):<20} -> {step.action.value}")
            print(f"{'':<15} ...")

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "results.json").write_text(json.dumps({"piece": "01", "scenarios": results}, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
