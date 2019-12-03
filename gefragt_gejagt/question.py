from __future__ import annotations

from typing import List, Dict
from enum import IntEnum, unique


@unique
class QuestionType(IntEnum):
    SIMPLE = 1
    CHASE = 2

    def __str__(self):
        return str(self.value)


class Question(object):
    """docstring for Question."""
    id: int
    type: QuestionType = QuestionType.CHASE
    level: int
    text: str
    correctAnswer: str
    wrongAnswers: List[str] = []
    category: str
    played: bool = False
    answerChaser: int = None
    answerPlayer: int = None

    def __init__(self):
        super(Question, self).__init__()

    def load(self, obj: dict):
        self.id = obj['id']
        self.type = obj['type']
        self.level = obj['level']
        self.text = obj['text']
        self.correctAnswer = obj['correctAnswer']
        self.category = obj['category']
        self.wrongAnswers = obj['wrongAnswers']
        self.played = obj.get('played', False)

    def save(self) -> Dict:
        question_obj = {}
        question_obj['id'] = self.id
        question_obj['type'] = self.type
        question_obj['level'] = self.level
        question_obj['text'] = self.text
        question_obj['correctAnswer'] = self.correctAnswer
        question_obj['wrongAnswers'] = self.wrongAnswers
        question_obj['played'] = self.played
        question_obj['answerChaser'] = self.answerChaser
        question_obj['answerPlayer'] = self.answerPlayer
        return question_obj


def load(obj: dict, question: Question = None) -> List[Question]:
    questions = []
    for question_obj in obj:
        question = Question()
        question.load(question_obj)
        questions.append(question)
    return questions


def save(questions: List[Question]) -> List:
    obj = []
    for question in questions:
        obj.append(question.save())
    return obj
