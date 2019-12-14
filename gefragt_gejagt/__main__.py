from __future__ import annotations

import os
import eel
import json
import bottle
import random
import argparse
import datetime
from typing import List, Dict
from enum import IntEnum, unique

import gefragt_gejagt.game
import gefragt_gejagt.team
import gefragt_gejagt.question
import gefragt_gejagt.round
import gefragt_gejagt.offer
from  gefragt_gejagt.game import GameState


SECONDS_PER_FASTROUND = 6
SECONDS_CHASE_TIMEOUT = 5


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
    game = gefragt_gejagt.game.Game(config.storage)
    game.load_json_state()

    app = bottle.Bottle()
    eel.init('gefragt_gejagt/web', allowed_extensions=['.js', '.html'])

    # Exposed Functions
    @eel.expose
    def list_teams():
        return gefragt_gejagt.team.save(game.teams)

    @eel.expose
    def game_state():
        return game.state

    @eel.expose
    def get_game():
        return game.save()

    @eel.expose
    def random_team():
        game.choose_team(game.random_team())
        resend_gamestate()

    @eel.expose
    def choose_team(id):
        game.choose_team(game.get_team_by_id(id))
        resend_gamestate()

    @eel.expose
    def start_game():
        game.start()
        resend_gamestate()

    @eel.expose
    def random_player():
        game.choose_player(game.random_player())
        resend_gamestate()

    @eel.expose
    def choose_player(id):
        game.choose_player(game.get_player_by_id(id))
        resend_gamestate()

    @eel.expose
    def reset_player():
        game.reset_player()
        resend_gamestate()

    @eel.expose
    def start_round():
        game.new_round()

        game.choose_question(game.random_question())

        eel.spawn(fastround_timer)
        resend_gamestate()

    def fastround_timer():
        starttime = datetime.datetime.now()
        endtime = starttime + datetime.timedelta(seconds=SECONDS_PER_FASTROUND)

        while datetime.datetime.now() < endtime:
            seconds_played = (datetime.datetime.now() - starttime).seconds
            seconds_remaining = SECONDS_PER_FASTROUND - seconds_played
            eel.all_fast_tick(seconds_played, seconds_remaining)
            eel.sleep(1.0)

        eel.all_fast_timeout()
        game.end_fastround()
        game.current_round.setup_offers(game.current_player.points)
        resend_gamestate()

    @eel.expose
    def random_question():
        game.choose_question(game.random_question())
        resend_gamestate()

    @eel.expose
    def choose_question(id):
        game.choose_question(game.get_question_by_id())
        resend_gamestate()

    @eel.expose
    def stop_question():
        game.stop_question()
        game.random_question()
        resend_gamestate()

    @eel.expose
    def question_answered(answer_id, player_id=0):
        if game.state == GameState.FAST_GUESS:
            game.answer_fast_question(answer_id)
            game.choose_question(game.random_question())
        else:
            if player_id == 0:  # Player
                game.current_question.answerPlayer = answer_id
                already_answered = (not game.current_question.answerChaser is None)
            else:  # Chaser
                game.current_question.answerChaser = answer_id
                already_answered = (not game.current_question.answerPlayer is None)
            if not already_answered:
                starttime = datetime.datetime.now()
                endtime = starttime + \
                    datetime.timedelta(seconds=SECONDS_CHASE_TIMEOUT)

                timedout = False

                while (
                        game.current_question.answerChaser is None or game.current_question.answerPlayer is None) and not timedout:
                    timedout = datetime.datetime.now() > endtime
                    seconds_played = (
                        datetime.datetime.now() - starttime
                    ).seconds
                    seconds_remaining = SECONDS_CHASE_TIMEOUT - seconds_played
                    eel.all_chase_tick(seconds_played, seconds_remaining)
                    eel.sleep(1.0)
                if timedout:
                    eel.all_chase_timeout()

                game.state = GameState.CHASE_SOLVE
        resend_gamestate()

    @eel.expose
    def set_offer(offer_num, offer_amount):
        game.current_round.offers[offer_num].amount = offer_amount
        resend_gamestate()

    @eel.expose
    def accept_offer(offer_num):
        game.current_round.offers[offer_num].accepted = True

        game.state = GameState.CHASE_QUESTIONING
        game.random_question()

        resend_gamestate()

    @eel.expose
    def all_show_solution():
        game.check_round_end()
        resend_gamestate()

    @eel.expose
    def end_round():
        game.end_round()
        resend_gamestate()

    @eel.expose
    def reset_game():
        global game
        del game

        game = gefragt_gejagt.game.Game(config.storage)
        game.load_json_state()

        resend_gamestate()

    def resend_gamestate():
        eel.all_change_gamestate(game.state)

    # Page-Close Handler
    def onclose(page, sockets):
        # This does nothing for the reason, that the eel-server keeps running
        pass

    # Auxillary bottle routes
    @app.route(r'/<path><:re:((\/\w+)+|\/?)$>')
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
