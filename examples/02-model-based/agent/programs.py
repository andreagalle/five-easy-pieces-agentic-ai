"""Model-based reflex agent program (AIMA 4e §2.4.3).

The agent can't sense where it is, so it keeps an internal state: what it believes about
the world, updated from its last action (the transition model) and its percept (the
sensor model). Its rules look at that state, not at the percept alone.

The state is plain JSON, so it can be saved to a file, read by a person and loaded later.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional, Set

from worlds import MOVES, Action, Location, Percept

WALL_HIT = {Action.LEFT: "left", Action.RIGHT: "right", Action.UP: "top", Action.DOWN: "bottom"}


@dataclass
class State:
    """Everything the agent believes. Coordinates are relative to where it started."""

    position: Location = (0, 0)
    last_action: Optional[Action] = None
    clean: Set[Location] = field(default_factory=set)  # squares it has seen clean
    walls: Dict[str, int] = field(default_factory=dict)  # the last reachable x or y on each side

    def to_json(self) -> dict:
        return {
            "position": list(self.position),
            "last_action": self.last_action.value if self.last_action else None,
            "walls": self.walls,
            "clean": sorted(list(square) for square in self.clean),
        }

    @classmethod
    def from_json(cls, data: dict) -> "State":
        return cls(
            position=tuple(data["position"]),
            last_action=Action(data["last_action"]) if data["last_action"] else None,
            clean={tuple(square) for square in data["clean"]},
            walls=dict(data["walls"]),
        )


def update_state(state: State, percept: Percept) -> None:
    """Fold the last action and the new percept into what the agent believes."""
    action, (x, y) = state.last_action, state.position
    if percept.bumped and action in WALL_HIT:
        # Sensor model: a bump means the move failed, and this square is the last on that side.
        state.walls[WALL_HIT[action]] = x if action in (Action.LEFT, Action.RIGHT) else y
    elif action in MOVES:
        # Transition model: without a bump, a move shifts the agent by exactly one square.
        dx, dy = MOVES[action]
        state.position = (x + dx, y + dy)
    if percept.dirty:
        state.clean.discard(state.position)
    else:
        state.clean.add(state.position)


def choose_action(state: State) -> Action:
    """Condition-action rules on the internal state: find the corner, then sweep row by row."""
    x, y = state.position
    if state.position not in state.clean:
        return Action.SUCK
    if finished(state):
        return Action.NOOP
    if "left" not in state.walls:
        return Action.LEFT
    if "top" not in state.walls:
        return Action.UP
    rightward = (y - state.walls["top"]) % 2 == 0
    if x == state.walls.get("right" if rightward else "left"):
        return Action.DOWN  # a known wall ahead: turn without bumping into it again
    return Action.RIGHT if rightward else Action.LEFT


def finished(state: State) -> bool:
    """True once all four walls are known and every square between them has been seen clean."""
    if len(state.walls) < 4:
        return False
    columns = range(state.walls["left"], state.walls["right"] + 1)
    rows = range(state.walls["top"], state.walls["bottom"] + 1)
    return all((x, y) in state.clean for x in columns for y in rows)


class ModelBasedReflexAgent:
    def __init__(self, state: Optional[State] = None):
        self.state = state if state is not None else State()

    def __call__(self, percept: Percept) -> Action:
        update_state(self.state, percept)
        self.state.last_action = choose_action(self.state)
        return self.state.last_action
