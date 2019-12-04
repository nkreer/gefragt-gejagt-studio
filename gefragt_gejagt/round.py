from __future__ import annotations

from typing import List, Dict

import gefragt_gejagt.question
import gefragt_gejagt.offer as offer


class Round(object):
    """docstring for Round."""
    id: int
    won: bool = False
    time: int
    player: Player = None
    questions: List[Question] = []
    offers: List[Offer] = []

    def __init__(self):
        super(Round, self).__init__()

    @property
    def level(self) -> int:
        levels = []
        for player in self.players:
            levels.append(player.level)
        return max(levels)

    @property
    def acceptedOffer(self) -> Offer:
        for offer in self.offers:
            if offer.accepted:
                return offer
        return None

    @property
    def correctAnswersChaser(self) -> int:
        count = 0
        for question in self.questions:
            if question.answerChaser == 0 and question.type == gefragt_gejagt.question.QuestionType.CHASE:
                count += 1
        return count

    @property
    def correctAnswersPlayer(self) -> int:
        count = 0
        for question in self.questions:
            if question.answerPlayer == 0 and question.type == gefragt_gejagt.question.QuestionType.CHASE:
                count += 1
        return count

    @property
    def playerStartOffset(self) -> int:
        if len(self.offers) != 0:
            if self.offers[0].accepted:
                return 2
            if self.offers[2].accepted:
                return 4
        return 3

    @property
    def questionsLeftForPlayer(self) -> int:
        return 7 - self.correctAnswersPlayer - self.playerStartOffset

    def save(self) -> Dict:
        round_obj = {}
        round_obj['id'] = self.id
        round_obj['won'] = self.won
        round_obj['player'] = self.player.save
        round_obj['questions'] = gefragt_gejagt.question.save(self.questions)
        round_obj['offers'] = offer.save(self.offers)
        if self.acceptedOffer:
            round_obj['acceptedOffer'] = self.acceptedOffer.save

        round_obj['correctAnswersChaser'] = self.correctAnswersChaser
        round_obj['correctAnswersPlayer'] = self.correctAnswersPlayer
        round_obj['playerStartOffset'] = self.playerStartOffset
        round_obj['questionsLeftForPlayer'] = self.questionsLeftForPlayer
        return round_obj


def load(json_str: str) -> List[Round]:
    pass


def save(rounds: List[Round]) -> List:
    obj = []
    for round in rounds:
        obj.append(round.save())
    return obj
