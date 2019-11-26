from __future__ import annotations

from typing import List, Dict
from enum import IntEnum, unique

import gefragt_gejagt.player as player
import gefragt_gejagt.question as question

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
    won: bool = False
    time: int
    players: List[Player] = []
    questions: List[Question] = []

    def __init__(self):
        super(Round, self).__init__()

    @property
    def level(self) -> int:
        levels = []
        for player in self.players:
            levels.append(player.level)
        return max(levels)

    def save(self) -> Dict:
        round_obj = {}
        round_obj['id'] = self.id
        round_obj['type'] = self.type
        round_obj['won'] = self.won
        round_obj['players'] = player.save(self.players)
        round_obj['questions'] = question.save(self.questions)
        return round_obj


def load(json_str: str) -> List[Round]:
    pass


def save(rounds: List[Round]) -> str:
    pass
