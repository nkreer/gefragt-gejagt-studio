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
    def __init__(self):
        super(Question, self).__init__()

        self.id: int
        self.type: QuestionType = QuestionType.CHASE
        self.level: int
        self.text: str
        self.correctAnswer: str
        self.wrongAnswers: List[str] = []
        self.category: str
        self.played: bool = False
        self.answerChaser: int = None
        self.answerPlayer: int = None

    def load(self, obj: dict):
        self.id = obj['id']
        self.type = obj['type']
        self.level = obj['level']
        self.text = obj['text']
        self.correctAnswer = obj['correctAnswer']
        self.wrongAnswers = obj.get('wrongAnswers', [])
        self.category = obj.get('category', '')
        self.played = obj.get('played', False)
        self.answerChaser = obj.get('answerChaser', None)
        self.answerPlayer = obj.get('answerPlayer', None)

    def save(self) -> Dict:
        question_obj = {}
        question_obj['id'] = self.id
        question_obj['type'] = self.type
        question_obj['level'] = self.level
        question_obj['text'] = self.text
        question_obj['correctAnswer'] = self.correctAnswer
        question_obj['wrongAnswers'] = self.wrongAnswers
        question_obj['category'] = self.category
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
