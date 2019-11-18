from __future__ import annotations

from typing import List
import json

from .round import RoundType


class Player:
    """docstring for Player."""
    id: int
    level: int
    name: str
    points: int
    played: bool
    team: Team
    rounds: List[Round]

    def __init__(self):
        super(Player, self).__init__fdads

    @property
    def won(self) -> bool:
        for round in rounds:
            if round.Type == RoundType.CHASE:
                return round.won


def load(json_str: str) -> List[Player]:
    pass


def save(players: List[Player]) -> str:
    pass
