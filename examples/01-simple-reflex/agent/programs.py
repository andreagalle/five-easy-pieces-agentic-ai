"""Simple reflex agent programs (AIMA 4e §2.4.2).

A simple reflex agent picks its action from the current percept alone, through
condition-action rules. It remembers nothing.
"""

from __future__ import annotations

import random
from typing import Sequence

from worlds import Action, Percept, pick


def reflex_vacuum_agent(percept: Percept) -> Action:
    """The two-square agent: suck if dirty, otherwise go to the other square."""
    if percept.dirty:
        return Action.SUCK
    if percept.location == (0, 0):
        return Action.RIGHT
    return Action.LEFT


def blind_reflex_agent(percept: Percept) -> Action:
    """The same rules without a location sensor: on a clean square it can only always go one way."""
    if percept.dirty:
        return Action.SUCK
    return Action.RIGHT


class RandomizedReflexAgent:
    """Blind too, but flips a coin on clean squares: the textbook escape from the loop.

    The random generator is not a model of the world; the rules still look only at
    the current percept.
    """

    def __init__(self, seed: int, moves: Sequence[Action] = (Action.LEFT, Action.RIGHT)):
        self.rng = random.Random(seed)
        self.moves = tuple(moves)

    def __call__(self, percept: Percept) -> Action:
        if percept.dirty:
            return Action.SUCK
        return pick(self.rng, self.moves)
