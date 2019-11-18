from __future__ import annotations

import os
import eel
import json
import bottle
import argparse
from typing import List

import gefragt_gejagt.team as team


class GefragtGejagt(object):
    """docstring for GefragtGejagt."""
    teams: List[Team]

    def __init__(self, storage):
        super(GefragtGejagt, self).__init__()
        self.storage = storage

    def load_json_state(self):
        with open(os.path.join(self.storage, 'initial.json'), 'r') as fp:
            obj = json.load(fp)
        self.teams = team.load(obj['teams'])


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
        return team.save(game.teams)

    # Page-Close Handler
    def onclose(page, sockets):
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
        app=app)
