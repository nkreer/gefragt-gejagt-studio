from __future__ import annotations

import os
import eel
import json
import time
import bottle
import random
import argparse
import datetime
from typing import List, Dict
from enum import IntEnum, unique

import gefragt_gejagt.team
import gefragt_gejagt.question
import gefragt_gejagt.round

@unique
class GameState(IntEnum):
    PREPARATION         = 0
    TEAM_CHOSEN         = 1
    GAME_STARTED        = 2
    PLAYER_CHOSEN       = 3
    FAST_GUESS          = 4
    CHASE_PREPARATION   = 5
    CHASE_QUESTIONING   = 6
    CHASE_SOLVE         = 7

    def __str__(self):
        return str(self.value)


class GefragtGejagt(object):
    """docstring for GefragtGejagt."""
    teams: List[Team] = []
    questions: List[Question] = []
    rounds: List[Round] = []
    current_team: Team = None
    current_round: Round = None
    current_player: Player = None
    current_question: Question = None
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

    def get_player_by_id(self, id) -> Player:
        for player in self.current_team.players:
            if player.id == id:
                return player
        raise IndexError

    def get_question_by_id(self, id) -> Question:
        for question in self.questions:
            if question.id == id:
                return question
        raise IndexError

    def save(self, include_team=False) -> Dict:
        game_obj = {}
        game_obj['state'] = self.state
        game_obj['teams'] = gefragt_gejagt.team.save(self.teams, include_players=True)
        game_obj['rounds'] = gefragt_gejagt.round.save(self.rounds)
        game_obj['questions'] = gefragt_gejagt.question.save(self.questions)
        if self.current_team:
            game_obj['current_team'] = self.current_team.save(include_players=True)
        else:
            game_obj['current_team'] = None
        if self.current_round:
            game_obj['current_round'] = self.current_round.save()
        else:
            game_obj['current_round'] = None
        if self.current_player:
            game_obj['current_player'] = self.current_player.save()
        else:
            game_obj['current_player'] = None
        if self.current_question:
            game_obj['current_question'] = self.current_question.save()
        else:
            game_obj['current_question'] = None
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
        game.state = GameState.TEAM_CHOSEN
        team = game.get_team_by_id(id)
        game.current_team = team

        eel.all_change_gamestate(game.state)
        eel.beamer_set_subheading(
            'Team {} bitte auf die Bühne!'.format(team.name))

    @eel.expose
    def start_game():
        game.state = GameState.GAME_STARTED
        eel.all_change_gamestate(game.state)

    @eel.expose
    def random_player():
        player = random.choice(game.current_team.players)
        choose_player(player.id)

    @eel.expose
    def choose_player(id):
        game.state = GameState.PLAYER_CHOSEN
        player = game.get_player_by_id(id)
        game.current_player = player

        eel.all_change_gamestate(game.state)

    @eel.expose
    def reset_player():
        game.state = GameState.GAME_STARTED
        game.current_player = None

        eel.all_change_gamestate(game.state)

    @eel.expose
    def start_round():
        game.state = GameState.FAST_GUESS
        game.current_round = gefragt_gejagt.round.Round()
        game.current_round.id = 1
        game.current_round.player = game.current_player

        random_question()

        eel.spawn(fastround_timer)
        eel.all_change_gamestate(game.state)

    def fastround_timer():
        starttime = datetime.datetime.now()
        endtime = starttime + datetime.timedelta(minutes=1)

        while datetime.datetime.now() < endtime:
            eel.sleep(1.0)
            seconds_played = (datetime.datetime.now() - starttime).seconds
            eel.all_fast_tick(seconds_played)

        eel.all_fast_timeout()

        game.state = GameState.CHASE_PREPARATION
        game.current_question = None

        eel.all_change_gamestate(game.state)

    @eel.expose
    def random_question():
        if game.state >= GameState.CHASE_PREPARATION and game.state <= GameState.CHASE_SOLVE:
            round_questiontype = gefragt_gejagt.question.QuestionType.CHASE
        else:
            round_questiontype = gefragt_gejagt.question.QuestionType.SIMPLE


        questions = []
        for question in game.questions:
            if not question.played and question.type == round_questiontype:
                questions.append(question)
        question = random.choice(questions)

        choose_question(question.id)

    @eel.expose
    def choose_question(id):
        if game.state >= GameState.CHASE_PREPARATION and game.state <= GameState.CHASE_SOLVE:
            game.state = GameState.CHASE_QUESTIONING
        question = game.get_question_by_id(id)
        game.current_question = question
        game.current_round.questions.append(question)

        eel.all_change_gamestate(game.state)

    @eel.expose
    def stop_question():
        if game.state == GameState.FAST_GUESS:
            game.current_round.questions.pop()
            random_question()

        eel.all_change_gamestate(game.state)

    @eel.expose
    def question_answered(answer_id):
        if answer_id == 0:
            game.current_player.points += 1
            print(game.current_player.points)
        else:
            pass
        game.current_question.played = True
        if game.state == GameState.FAST_GUESS:
            random_question()

        eel.all_change_gamestate(game.state)

    # TODO: eel.set_offer
    # TODO: eel.accept_offer

    @eel.expose
    def reset_game():
        game = GefragtGejagt(config.storage)
        game.load_json_state()
        
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
