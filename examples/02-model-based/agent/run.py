"""Run the piece 02 scenarios and write a deterministic report.

    python3 -m agent.run [--out DIR]              everything in one go
    python3 -m agent.run --stop-at T [--out DIR]  sweep up to step T, save to DIR/state, exit
    python3 -m agent.run --resume [--out DIR]     load DIR/state, finish, write the report

The two routes write the same DIR/results.json, byte for byte, because everything the
second half needs is in the saved files. Nothing depends on the machine, the time or the
Python version, so results also match between the host and a sandbox.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence, Tuple

from worlds import Episode, VacuumWorld, WorldConfig, run_episode

from .programs import ModelBasedReflexAgent, State

TWO_SQUARES = [(0, 0), (1, 0)]
GRID = [(x, y) for y in range(4) for x in range(4)]
BLIND_TWO_SQUARES = WorldConfig(sense_location=False)
BLIND_GRID = WorldConfig(width=4, height=4, sense_location=False)
STEPS = 200
FORGET_AT = 18  # halfway through the sweep: two rows done, two to go


def summarize(name: str, description: str, config: WorldConfig, episode: Episode) -> dict:
    return {
        "name": name,
        "description": description,
        "world": f"{config.width}x{config.height}",
        "steps": len(episode.steps),
        "score": episode.score,
        "max_score": episode.max_score,
        "all_clean_at": episode.all_clean_at,
        "final_dirty": [list(square) for square in episode.final_dirty],
        "start": list(episode.start),
        "dirty_start": [list(square) for square in episode.dirty_start],
        "actions": [step.action.value for step in episode.steps],
        "path": [list(step.location) for step in episode.steps],  # location after each step
        "clean": [step.clean for step in episode.steps],  # clean squares after each step
        "bumps": sum(step.percept.bumped for step in episode.steps),
    }


def join(first: dict, second: dict) -> dict:
    """One summary from two stretches of the same run."""
    late = second["all_clean_at"] and second["all_clean_at"] + first["steps"]
    return {
        **first,
        "steps": first["steps"] + second["steps"],
        "score": first["score"] + second["score"],
        "max_score": first["max_score"] + second["max_score"],
        "all_clean_at": first["all_clean_at"] or late,
        "final_dirty": second["final_dirty"],
        "actions": first["actions"] + second["actions"],
        "path": first["path"] + second["path"],
        "clean": first["clean"] + second["clean"],
        "bumps": first["bumps"] + second["bumps"],
    }


def sweep(world: VacuumWorld, agent: ModelBasedReflexAgent, steps: int) -> dict:
    return summarize("grid-model", "4x4 grid, location sensor off, internal state", world.config,
                     run_episode(world, agent, steps))


def save_state(directory: Path, agent: ModelBasedReflexAgent, world: VacuumWorld, so_far: dict) -> None:
    """Two files: what the agent believes, and the simulated world with the run so far."""
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "agent-state.json").write_text(json.dumps(agent.state.to_json(), indent=2) + "\n")
    world_state = {
        "location": list(world.location),
        "dirty": sorted(list(square) for square in world.dirty),
        "bumped": world.bumped,
        "so_far": so_far,
    }
    (directory / "world.json").write_text(json.dumps(world_state, indent=2) + "\n")


def load_state(directory: Path) -> Tuple[ModelBasedReflexAgent, VacuumWorld, dict]:
    agent = ModelBasedReflexAgent(State.from_json(json.loads((directory / "agent-state.json").read_text())))
    saved = json.loads((directory / "world.json").read_text())
    world = VacuumWorld(BLIND_GRID, tuple(saved["location"]), [tuple(square) for square in saved["dirty"]])
    world.bumped = saved["bumped"]
    return agent, world, saved["so_far"]


def forgetful_sweep() -> dict:
    """The same sweep, but the agent loses its state halfway, as if its sandbox had been deleted."""
    world = VacuumWorld(BLIND_GRID, (0, 0), GRID)
    first = summarize("grid-amnesia", f"4x4 grid, internal state lost at step {FORGET_AT}", BLIND_GRID,
                      run_episode(world, ModelBasedReflexAgent(), FORGET_AT))
    second = summarize("grid-amnesia", "", BLIND_GRID, run_episode(world, ModelBasedReflexAgent(), STEPS - FORGET_AT))
    return join(first, second)


def report(scenario: dict) -> None:
    cleaned = f"all clean at step {scenario['all_clean_at']}" if scenario["all_clean_at"] else \
        f"{len(scenario['final_dirty'])} square(s) still dirty"
    print(f"{scenario['name']:<13} {scenario['description']}")
    print(f"{'':<13} score {scenario['score']}/{scenario['max_score']}, {cleaned}, {scenario['bumps']} bumps")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", default="out", help="directory for results.json (default: out)")
    route = parser.add_mutually_exclusive_group()
    route.add_argument("--stop-at", type=int, metavar="T", help="save the sweep after step T and exit")
    route.add_argument("--resume", action="store_true", help="finish a sweep saved with --stop-at")
    args = parser.parse_args(argv)
    out = Path(args.out)

    if args.stop_at is not None:
        if not 0 < args.stop_at < STEPS:
            parser.error(f"--stop-at must be between 1 and {STEPS - 1}")
        agent, world = ModelBasedReflexAgent(), VacuumWorld(BLIND_GRID, (0, 0), GRID)
        save_state(out / "state", agent, world, sweep(world, agent, args.stop_at))
        print(f"grid-model    stopped after step {args.stop_at}, with {world.clean_count()}/16 squares clean")
        print(f"{'':<13} the agent believes: {json.dumps(agent.state.to_json())}")
        return 0

    if args.resume:
        if not (out / "state" / "agent-state.json").exists():
            parser.error(f"nothing to resume: no {out / 'state' / 'agent-state.json'}")
        agent, world, so_far = load_state(out / "state")
        print(f"grid-model    resuming after step {so_far['steps']}, in the state it was saved")
        grid = join(so_far, sweep(world, agent, STEPS - so_far["steps"]))
    else:
        grid = sweep(VacuumWorld(BLIND_GRID, (0, 0), GRID), ModelBasedReflexAgent(), STEPS)

    two_squares = summarize("two-squares", "location sensor off, starting on B as in piece 1", BLIND_TWO_SQUARES,
                            run_episode(VacuumWorld(BLIND_TWO_SQUARES, (1, 0), TWO_SQUARES), ModelBasedReflexAgent(), 10))
    results = [two_squares, grid, forgetful_sweep()]
    for scenario in results:
        report(scenario)

    out.mkdir(parents=True, exist_ok=True)
    (out / "results.json").write_text(json.dumps({"piece": "02", "scenarios": results}, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
