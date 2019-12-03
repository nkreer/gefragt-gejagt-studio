from __future__ import annotations

from typing import List, Dict
from enum import IntEnum, unique

import gefragt_gejagt.player as player
import gefragt_gejagt.question as question

class Round(object):
    """docstring for Round."""
    id: int
    won: bool = False
    time: int
    player: Player = None
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
        round_obj['won'] = self.won
        round_obj['players'] = self.player.save
        round_obj['questions'] = question.save(self.questions)
        return round_obj


def load(json_str: str) -> List[Round]:
    pass


def save(rounds: List[Round]) -> str:
    pass
