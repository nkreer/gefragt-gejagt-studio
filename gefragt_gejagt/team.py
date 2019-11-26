from __future__ import annotations

from typing import List, Dict

import gefragt_gejagt.player as player


class Team(object):
    """docstring for Team."""
    id: int = None
    name: str = None
    players: List[Player] = []

    def __init__(self):
        super(Team, self).__init__()

    def load(self, obj: Dict):
        self.id = obj['id']
        self.name = obj['name']
        if obj['players']:
            self.players = player.load(obj['players'], self)

    def save(self, include_players=False) -> Dict:
        team_obj = {}
        team_obj['id'] = self.id
        team_obj['name'] = self.name
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
