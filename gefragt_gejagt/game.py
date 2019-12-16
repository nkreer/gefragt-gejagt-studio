from __future__ import annotations

import os
import json
import random
from typing import List, Dict
from enum import IntEnum, unique

import gefragt_gejagt.team
import gefragt_gejagt.question
import gefragt_gejagt.round
import gefragt_gejagt.offer


POINTS_PER_QUESTION = 1


@unique
class GameState(IntEnum):
    PREPARATION = 0
    TEAM_CHOSEN = 1
    GAME_STARTED = 2
    PLAYER_CHOSEN = 3
    FAST_GUESS = 4
    CHASE_PREPARATION = 5
    CHASE_QUESTIONING = 6
    CHASE_SOLVE = 7
    ROUND_ENDED = 8
    FINAL_PREPARATION = 9
    FINAL_PLAYERS = 10
    FINAL_BETWEEN = 11
    FINAL_CHASER = 12
    FINAL_CHASER_WRONG = 13
    FINAL_END = 14
    EVALUATION = 15

    def __str__(self):
        return str(self.value)


class Game(object):
    """docstring for GefragtGejagt."""

    def __init__(self, file):
        super(Game, self).__init__()
        self.file = file

        self.teams: List[Team] = []
        self.questions: List[Question] = []
        self.rounds: List[Round] = []
        self.current_team: Team = None
        self.current_round: Round = None
        self.current_player: Player = None
        self.current_question: Question = None
        self.state: GameState = GameState.PREPARATION

    def load_json_state(self, filename=None):
        if filename is None:
            filename = self.file
        with open(filename, 'r') as fp:
            obj = json.load(fp)

        self.state = obj.get('state', GameState.PREPARATION)
        self.teams = gefragt_gejagt.team.load(obj['teams'])
        self.questions = gefragt_gejagt.question.load(obj['questions'])

        if obj.get('current_team'):
            self.current_team = self.get_team_by_id(obj['current_team']['id'])
        if obj.get('current_player'):
            self.current_player = self.get_player_by_id(
                obj['current_player']['id'])
        if obj.get('current_question'):
            self.current_question = self.get_question_by_id(
                obj['current_question']['id'])

        if obj.get('rounds'):
            self.rounds = gefragt_gejagt.round.load(obj['rounds'], self)
            if obj.get('current_round'):
                self.current_round = self.get_round_by_id(
                    obj['current_round']['id'])

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

    def get_round_by_id(self, id) -> Round:
        for round in self.rounds:
            if round.id == id:
                return round
        raise IndexError

    def get_question_by_id(self, id) -> Question:
        for question in self.questions:
            if question.id == id:
                return question
        raise IndexError

    def choose_team(self, team: Team):
        self.state = GameState.TEAM_CHOSEN
        self.current_team = team

    def random_team(self) -> Team:
        teams = []
        for team in self.teams:
            if not team.played:
                teams.append(team)
        team = random.choice(teams)
        return team

    def start(self):
        self.state = GameState.GAME_STARTED

    def choose_player(self, player: Player):
        self.state = GameState.PLAYER_CHOSEN
        self.current_player = player

    def random_player(self, only_unplayed=True) -> Player:
        if not only_unplayed:
            players = self.current_team.players
        else:
            players = []
            for player in self.current_team.players:
                if not player.played:
                    players.append(player)
        return random.choice(players)

    def reset_player():
        self.state = GameState.GAME_STARTED
        self.current_player = None

    def new_round(self):
        self.state = GameState.FAST_GUESS
        round = gefragt_gejagt.round.Round()
        round.id = len(self.rounds)
        round.player = self.current_player
        self.current_player.played = True

        self.current_round = round
        self.rounds.append(round)

    def end_fastround(self):
        self.state = GameState.CHASE_PREPARATION
        self.current_question = None

    def random_question(self) -> Question:
        # TODO: Fallback if no questions left
        if self.state >= GameState.CHASE_PREPARATION and self.state <= GameState.CHASE_SOLVE:
            round_questiontype = gefragt_gejagt.question.QuestionType.CHASE
        else:
            round_questiontype = gefragt_gejagt.question.QuestionType.SIMPLE

        questions = []
        for question in self.questions:
            if not question.played and question.type == round_questiontype:
                questions.append(question)
        question = random.choice(questions)
        return question

    def choose_question(self, question: Question):
        if self.state >= GameState.CHASE_PREPARATION and self.state <= GameState.CHASE_SOLVE:
            self.state = GameState.CHASE_QUESTIONING
        question.played = True
        self.current_question = question
        self.current_round.questions.append(question)

    def stop_question(self):
        if self.state == GameState.FAST_GUESS:
            self.current_question.played = True
            self.current_round.questions.pop()

    def answer_fast_question(self, answer_id: int):
        if answer_id == 0:
            self.current_player.points += POINTS_PER_QUESTION
        self.current_question.played = True

    def check_round_end(self):
        round = self.current_round
        if round.questionsLeftForPlayer <= 0:
            round.won = True
            self.current_player.qualified = True
            self.state = GameState.ROUND_ENDED
        elif (round.correctAnswersPlayer + round.playerStartOffset) <= round.correctAnswersChaser:
            self.state = GameState.ROUND_ENDED

    def setup_finalround(self, players=False):
        round = gefragt_gejagt.round.Round()
        round.id = len(self.rounds)
        round.type = gefragt_gejagt.round.RoundType.FINAL
        round.team = self.current_team

        self.current_round = round

        if players:
            self.state = GameState.FINAL_PLAYERS
        else:
            self.state = GameState.FINAL_CHASER

    def end_round(self):
        self.current_round = None
        self.current_player = None
        self.current_question = None
        not_all_played = False

        for player in self.current_team.players:
            if not player.played:
                not_all_played = True
                break

        if not_all_played:
            self.state = GameState.GAME_STARTED
        else:
            self.state = GameState.FINAL_PREPARATION

    def save_to_file(self, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(
                self.save(),
                f,
                ensure_ascii=False,
                indent=4,
                default=lambda o: None)

    def save(self, include_team=False) -> Dict:
        game_obj = {}
        game_obj['state'] = self.state
        game_obj['teams'] = gefragt_gejagt.team.save(
            self.teams, include_players=True)
        game_obj['rounds'] = gefragt_gejagt.round.save(self.rounds)
        game_obj['questions'] = gefragt_gejagt.question.save(self.questions)
        if self.current_team:
            game_obj['current_team'] = self.current_team.save(
                include_players=True)
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
