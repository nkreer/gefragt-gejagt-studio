from __future__ import annotations

import os
import eel
import bottle
import argparse
import datetime

import gefragt_gejagt.game
import gefragt_gejagt.team
import gefragt_gejagt.question
import gefragt_gejagt.round
import gefragt_gejagt.offer
from gefragt_gejagt.game import GameState


SECONDS_PER_FASTROUND = 60
SECONDS_CHASE_TIMEOUT = 5
SECONDS_PER_FINALROUND = 120


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
        '-f',
        '--file',
        default="examples/initial.json",
        help="""The .json files for the questions, teams, players etc. The current gamestate will be saved to the parent-folder.""")
    return parser.parse_args()


if __name__ == '__main__':
    config = parse_arguments()
    game = gefragt_gejagt.game.Game(config.file)
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
        only_unplayed = game.state != GameState.FINAL_PREPARATION
        try:
            player = game.random_player(only_unplayed=only_unplayed)
        except:
            game.state = GameState.FINAL_PREPARATION
        if game.state == GameState.FINAL_PREPARATION:
            player.qualified = not player.qualified
        else:
            game.choose_player(player)
        resend_gamestate()

    @eel.expose
    def choose_player(id):
        player = game.get_player_by_id(id)
        if game.state == GameState.FINAL_PREPARATION:
            player.qualified = not player.qualified
        else:
            game.choose_player(player)
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
        game.choose_question(game.get_question_by_id(id))
        eel.all_new_question(game.current_question.save())
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
        elif game.state >= GameState.CHASE_PREPARATION and game.state <= GameState.CHASE_SOLVE:
            if player_id == 0:  # Player
                game.current_question.answerPlayer = answer_id
                already_answered = (
                    game.current_question.answerChaser is not None)
            else:  # Chaser
                game.current_question.answerChaser = answer_id
                already_answered = (
                    game.current_question.answerPlayer is not None)
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
                else:
                    eel.all_chase_both_answered()

                game.state = GameState.CHASE_SOLVE
        else:
            if game.state == GameState.FINAL_PLAYERS:
                game.current_question.answerPlayer = answer_id
                game.choose_question(game.random_question())
            elif game.state == GameState.FINAL_CHASER:
                game.current_question.answerChaser = answer_id
                if answer_id == 0:
                    game.choose_question(game.random_question())
                else:
                    game.state = GameState.FINAL_CHASER_WRONG
                    game.chaser_thread = False
            elif game.state == GameState.FINAL_CHASER_WRONG:
                game.current_question.answerPlayer = answer_id
                game.choose_question(game.random_question())
                game.state = GameState.FINAL_CHASER
                start_final_chaser()
        resend_gamestate()

    @eel.expose
    def set_offer(offer_num, offer_amount):
        game.current_round.offers[offer_num].amount = offer_amount
        resend_gamestate()

    @eel.expose
    def accept_offer(offer_num):
        game.current_round.offers[offer_num].accepted = True

        game.current_player.points = game.current_round.offers[offer_num].amount

        game.state = GameState.CHASE_QUESTIONING
        game.choose_question(game.random_question())

        resend_gamestate()

    @eel.expose
    def all_show_chaserresponse():
        game.check_round_end()
        resend_gamestate()

    @eel.expose
    def end_round():
        game.end_round()
        resend_gamestate()

    @eel.expose
    def start_final_game():
        game.setup_finalround(players=True)
        game.choose_question(game.random_question())
        resend_gamestate()

        starttime = datetime.datetime.now()
        endtime = starttime + \
            datetime.timedelta(seconds=SECONDS_PER_FINALROUND)

        while datetime.datetime.now() < endtime:
            seconds_played = (datetime.datetime.now() - starttime).seconds
            seconds_remaining = SECONDS_PER_FINALROUND - seconds_played
            eel.all_final_tick(seconds_played, seconds_remaining)
            eel.sleep(1.0)

        game.state = GameState.FINAL_BETWEEN
        resend_gamestate()

    @eel.expose
    def start_final_chaser():
        game.chaser_thread = True

        game.state = GameState.FINAL_CHASER
        game.choose_question(game.random_question())
        resend_gamestate()

        game.current_round.finalTime.append({'start': datetime.datetime.now()})

        eel.spawn(chaser_thread)

    def chaser_thread():
        timedout = False
        i = 0

        while game.state == GameState.FINAL_CHASER and not timedout and not game.current_round.chaserFinalWon and game.chaser_thread:
            if i % 10 == 0:
                seconds_played = game.current_round.timePassed.seconds
                timedout = seconds_played >= SECONDS_PER_FINALROUND
                seconds_remaining = SECONDS_PER_FINALROUND - seconds_played
                eel.all_final_tick(seconds_played, seconds_remaining)

            i += 1
            eel.sleep(0.1)

        if not game.chaser_thread:
            eel.all_final_pause(seconds_played, seconds_remaining)
            game.state = GameState.FINAL_CHASER_WRONG
        elif game.current_round.chaserFinalWon:
            game.state = GameState.FINAL_END
        elif timedout:
            eel.all_final_timeout()
            game.current_round.won = True
            game.state = GameState.FINAL_END
        game.current_round.finalTime[-1]['end'] = datetime.datetime.now()
        resend_gamestate()

    @eel.expose
    def save_game():
        timestamp = datetime.datetime.now().__format__('%Y-%m-%dT%H_%M_%S')

        print("created autosave at {}".format(timestamp))

        game.save_to_file(
            os.path.join(
                os.path.dirname(
                    config.file),
                "save-{}.json".format(timestamp)))

    @eel.expose
    def get_files():
        path = os.path.dirname(config.file)
        return [f for f in os.listdir(path) if os.path.isfile(
            os.path.join(path, f)) and f[-5:] == '.json']

    @eel.expose
    def load_game(file):
        save_game()

        global game
        del game

        game = gefragt_gejagt.game.Game(
            os.path.join(
                os.path.dirname(
                    config.file),
                file))
        game.load_json_state()

        resend_gamestate()

    @eel.expose
    def reset_game():
        save_game()

        global game
        del game

        game = gefragt_gejagt.game.Game(config.file)
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
