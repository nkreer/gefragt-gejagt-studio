from __future__ import annotations

from typing import List
from enum import IntEnum, unique


@unique
class RoundType(IntEnum):
    FAST = 1
    CHASE = 2
    FINAL = 3

    def __str__(self):
        return str(self.value)


class Round(object):
    """docstring for Round."""
    id: int
    type: RoundType
    won: bool
    time: int
    players: List[Player]
    questions: List[Question]

    def __init__(self):
        super(Round, self).__init__()

    def __serialize__(self):
        return self.__dict__.update({
            'type': int(self.type)
        })

    @property
    def level(self) -> int:
        levels = []
        for player in self.players:
            levels.append(player.level)
        return max(levels)


def load(json_str: str) -> List[Round]:
    pass


def save(rounds: List[Round]) -> str:
    pass
