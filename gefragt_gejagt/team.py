from __future__ import annotations

from typing import List


class Team(object):
    """docstring for Team."""
    id: int
    name: str
    players: List[Player]

    def __init__(self, arg):
        super(Team, self).__init__()
        self.arg = arg


def load(json_str: str) -> List[Team]:
    pass


def save(teams: List[Team]) -> str:
    pass
