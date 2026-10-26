"""AIMA's vacuum world, generalized to an N x M grid.

The two-square world of AIMA 4e, Chapter 2, is the 2 x 1 case: squares A = (0, 0)
and B = (1, 0). Three switches turn it into the harder environments later pieces need:

- ``sense_location=False``: the agent no longer perceives where it is (partially observable)
- ``slip=p``: a move fails with probability p and the agent stays put (stochastic)
- ``dirt_rate=q``: after every step, each clean square gets dirty with probability q (dynamic)

All randomness comes from one ``random.Random(seed)`` and only through ``random()``,
which returns the same sequence on every platform and Python 3 version. A run is
therefore reproducible on the host and in any sandbox.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from enum import Enum
from typing import Callable, Iterable, Optional, Tuple

Location = Tuple[int, int]  # (x, y); (0, 0) is the top-left square


class Action(str, Enum):
    SUCK = "Suck"
    LEFT = "Left"
    RIGHT = "Right"
    UP = "Up"
    DOWN = "Down"
    NOOP = "NoOp"


MOVES = {
    Action.LEFT: (-1, 0),
    Action.RIGHT: (1, 0),
    Action.UP: (0, -1),
    Action.DOWN: (0, 1),
}


@dataclass(frozen=True)
class Percept:
    """What the agent senses before choosing each action."""

    location: Optional[Location]  # None when the location sensor is switched off
    dirty: bool
    bumped: bool  # the previous move hit a wall


@dataclass(frozen=True)
class WorldConfig:
    width: int = 2
    height: int = 1
    sense_location: bool = True
    slip: float = 0.0
    dirt_rate: float = 0.0
    seed: int = 0


AgentProgram = Callable[[Percept], Action]


class VacuumWorld:
    def __init__(self, config: WorldConfig, start: Location = (0, 0), dirty: Iterable[Location] = ()):
        self.config = config
        self.squares = [(x, y) for y in range(config.height) for x in range(config.width)]
        self.location = start
        self.dirty = set(dirty)
        self.bumped = False
        self.rng = random.Random(config.seed)
        unknown = ({start} | self.dirty) - set(self.squares)
        if unknown:
            raise ValueError(f"squares outside a {config.width}x{config.height} world: {sorted(unknown)}")

    def percept(self) -> Percept:
        location = self.location if self.config.sense_location else None
        return Percept(location, self.location in self.dirty, self.bumped)

    def execute(self, action: Action) -> None:
        self.bumped = False
        if action is Action.SUCK:
            self.dirty.discard(self.location)
        elif action in MOVES and not self._slips():
            dx, dy = MOVES[action]
            x, y = self.location[0] + dx, self.location[1] + dy
            if 0 <= x < self.config.width and 0 <= y < self.config.height:
                self.location = (x, y)
            else:
                self.bumped = True
        if self.config.dirt_rate:
            for square in self.squares:
                if square not in self.dirty and self.rng.random() < self.config.dirt_rate:
                    self.dirty.add(square)

    def clean_count(self) -> int:
        return len(self.squares) - len(self.dirty)

    def _slips(self) -> bool:
        return self.config.slip > 0 and self.rng.random() < self.config.slip


@dataclass(frozen=True)
class Step:
    t: int
    percept: Percept
    action: Action


@dataclass(frozen=True)
class Episode:
    steps: Tuple[Step, ...]
    score: int  # performance measure: one point per clean square per time step
    max_score: int
    all_clean_at: Optional[int]  # first step after which no square was dirty
    final_dirty: Tuple[Location, ...]


def run_episode(world: VacuumWorld, program: AgentProgram, steps: int) -> Episode:
    """Run the percept -> action loop for a fixed number of steps and score it."""
    trace = []
    score = 0
    all_clean_at = None
    for t in range(1, steps + 1):
        percept = world.percept()
        action = program(percept)
        world.execute(action)
        trace.append(Step(t, percept, action))
        score += world.clean_count()
        if all_clean_at is None and not world.dirty:
            all_clean_at = t
    return Episode(
        steps=tuple(trace),
        score=score,
        max_score=steps * len(world.squares),
        all_clean_at=all_clean_at,
        final_dirty=tuple(sorted(world.dirty)),
    )


def pick(rng: random.Random, options):
    """Choose uniformly with ``random()`` only, so choices match across Python versions."""
    return options[int(rng.random() * len(options))]
