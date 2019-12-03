from __future__ import annotations

from typing import List, Dict

import gefragt_gejagt.question as question
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
            if question.answerChaser == 0:
                count += 1
        return count

    @property
    def correctAnswersPlayer(self) -> int:
        count = 0
        for question in self.questions:
            if question.answerPlayer == 0:
                count += 1
        return count

    def save(self) -> Dict:
        round_obj = {}
        round_obj['id'] = self.id
        round_obj['won'] = self.won
        round_obj['player'] = self.player.save
        round_obj['questions'] = question.save(self.questions)
        round_obj['offers'] = offer.save(self.offers)
        if self.acceptedOffer:
            round_obj['acceptedOffer'] = self.acceptedOffer.save

        round_obj['correctAnswersChaser'] = self.correctAnswersChaser
        round_obj['correctAnswersPlayer'] = self.correctAnswersPlayer
        return round_obj


def load(json_str: str) -> List[Round]:
    pass


def save(rounds: List[Round]) -> List:
    obj = []
    for round in rounds:
        obj.append(round.save())
    return obj
