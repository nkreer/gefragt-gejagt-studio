from __future__ import annotations

from typing import List, Dict

import gefragt_gejagt.team as team


class Player:
    """docstring for Player."""
    id: int = None
    level: int = None
    name: str = None
    points: int = 0
    played: bool = False
    team: Team = None
    qualified: bool = False
    round: Round = None

    def __init__(self):
        super(Player, self).__init__

    @property
    def won(self) -> bool:
        if self.round:
            return self.round.won
        return False

    def load(self, obj: dict, set_team: Team = None):
        self.id = obj['id']
        self.name = obj['name']
        self.level = obj['level']
        self.points = obj.get('points', 0)
        self.played = obj['played']
        if obj.get('team'):
            self.team = team.Team()
            self.team.load(obj['team'])
        else:
            self.team = set_team

    def save(self, include_team=False) -> Dict:
        player_obj = {}
        player_obj['id'] = self.id
        player_obj['name'] = self.name
        player_obj['level'] = self.level
        player_obj['points'] = self.points
        player_obj['played'] = self.played
        player_obj['won'] = self.won
        player_obj['qualified'] = self.qualified
        if include_team:
            player_obj['players'] = self.team.save()
        return player_obj


def load(obj: dict, team: Team = None) -> List[Player]:
    players = []
    for player_obj in obj:
        player = Player()
        player.load(player_obj)
        players.append(player)
    return players


def save(players: List[Player]) -> List:
    obj = []
    for player in players:
        obj.append(player.save())
    return obj
