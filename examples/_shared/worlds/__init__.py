"""Shared environments for the five pieces (CLAUDE.md §4, ADR-0002)."""

from .vacuum import (
    MOVES,
    Action,
    AgentProgram,
    Episode,
    Location,
    Percept,
    Step,
    VacuumWorld,
    WorldConfig,
    pick,
    run_episode,
)

__all__ = [
    "MOVES",
    "Action",
    "AgentProgram",
    "Episode",
    "Location",
    "Percept",
    "Step",
    "VacuumWorld",
    "WorldConfig",
    "pick",
    "run_episode",
]
