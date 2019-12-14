from __future__ import annotations

from typing import List, Dict

import gefragt_gejagt.player as player


class Team(object):
    def __init__(self):
        super(Team, self).__init__()

        self.id: int = None
        self.name: str = None
        self.players: List[Player] = []

    @property
    def level(self) -> int:
        levels = []
        for player in self.players:
            levels.append(player.level)
        return max(levels)

    @property
    def played(self) -> bool:
        for player in self.players:
            if player.played:
                return True
        return False

    @property
    def qualified(self) -> bool:
        for player in self.players:
            if player.qualified:
                return True
        return False

    def load(self, obj: Dict):
        self.id = obj['id']
        self.name = obj['name']
        if obj['players']:
            self.players = player.load(obj['players'], self)

    def save(self, include_players=False) -> Dict:
        team_obj = {}
        team_obj['id'] = self.id
        team_obj['name'] = self.name
        team_obj['played'] = self.played
        if include_players:
            team_obj['players'] = player.save(self.players)
        return team_obj


def load(obj: Dict) -> List[Team]:
    teams = []
    for team_obj in obj:
        team = Team()
        team.load(team_obj)
        teams.append(team)
    return teams


def save(teams: List[Team], include_players=True) -> List:
    obj = []
    for team in teams:
        obj.append(team.save(include_players=include_players))
    return obj
