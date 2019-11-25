from __future__ import annotations

import os
import eel
import json
import bottle
import random
import argparse
from typing import List, Dict
from enum import IntEnum, unique

import gefragt_gejagt.team
import gefragt_gejagt.question


@unique
class GameState(IntEnum):
    PREPARATION = 0
    WAITING = 1   # Waiting for Team
    NEXT_STATE = 2

    def __str__(self):
        return str(self.value)


class GefragtGejagt(object):
    """docstring for GefragtGejagt."""
    teams: List[Team] = []
    questions: List[Question] = []
    current_team: Team = None
    state: GameState = GameState.PREPARATION

    def __init__(self, storage):
        super(GefragtGejagt, self).__init__()
        self.storage = storage

    def load_json_state(self, filename='initial.json'):
        with open(os.path.join(self.storage, filename), 'r') as fp:
            obj = json.load(fp)
        self.teams = gefragt_gejagt.team.load(obj['teams'])
        self.questions = gefragt_gejagt.question.load(obj['questions'])

    def get_team_by_id(self, id) -> Team:
        for team in self.teams:
            if team.id == id:
                return team
        raise IndexError

    def save(self, include_team=False) -> Dict:
        game_obj = {}
        game_obj['state'] = self.state
        game_obj['teams'] = gefragt_gejagt.team.save(self.teams)
        game_obj['questions'] = gefragt_gejagt.question.save(self.questions)
        if self.current_team:
            game_obj['current_team'] = self.current_team.save()
        else:
            game_obj['current_team'] = None
        return game_obj


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Run the GefragtGejagt-Server',
        prog='python -m gefragt-gejagt')
    parser.add_argument(
        '-c', '--continue',
        action='store_true',
        help="Continue the last-saved Game")
    parser.add_argument(
        '-a', '--address',
        default="127.0.0.1",
        help="The address to listen to")
    parser.add_argument(
        '-p', '--port',
        default="8000",
        help="The port to listen to")
    parser.add_argument(
        '-s',
        '--storage',
        default="examples",
        help="""The folder in which the .json files for the questions, teams,
        players etc. are stored and the current gamestate will be saved to.""")
    return parser.parse_args()


if __name__ == '__main__':
    config = parse_arguments()
    game = GefragtGejagt(config.storage)
    game.load_json_state()

    app = bottle.Bottle()
    eel.init('gefragt_gejagt/web', allowed_extensions=['.js', '.html'])

    # Exposed Functions
    @eel.expose
    def list_teams():
        # eel.js_set_url('https://nwng.eu/36c3-gg/')
        return gefragt_gejagt.team.save(game.teams)

    @eel.expose
    def game_state():
        return game.state

    @eel.expose
    def get_game():
        return game.save()

    @eel.expose
    def random_team():
        team = random.choice(game.teams)
        choose_team(team.id)

    @eel.expose
    def choose_team(id):
        game.state = GameState.WAITING
        team = game.get_team_by_id(id)
        game.current_team = team

        eel.all_change_gamestate(game.state)
        eel.beamer_set_subheading(
            'Team {} bitte auf die Bühne!'.format(team.name))

    @eel.expose
    def start_game():
        game.state = GameState.NEXT_STATE
        eel.all_change_gamestate(game.state)

    @eel.expose
    def reset_game():
        game.state = GameState.PREPARATION
        game.current_team = None
        eel.all_change_gamestate(game.state)

    # Page-Close Handler
    def onclose(page, sockets):
        # This does nothing for the reason, that the eel-server keeps running
        pass

    # Auxillary bottle routes
    @app.route('/<path><:re:((\/\w+)+|\/?)$>')
    def redirect_to_index(path):
        bottle.redirect('/{}/index.html'.format(path))

    @app.route('/')
    def redirect_to_dashboard():
        bottle.redirect('/dashboard/index.html')

    print('Listening on {}:{}'.format(config.address, config.port))
    eel.start(
        host=config.address,
        port=config.port,
        close_callback=onclose,
        app=app,
        reloader=True)
