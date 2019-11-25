from __future__ import annotations

from typing import List, Dict


class Question(object):
    """docstring for Question."""
    id: int
    level: int
    text: str
    correctAnswer: str
    wrongAnswers: List[str] = []
    category: str

    def __init__(self):
        super(Question, self).__init__()

    def load(self, obj: dict, set_team: Team = None):
        self.id = obj['id']
        self.level = obj['level']
        self.text = obj['text']
        self.correctAnswer = obj['correctAnswer']
        self.category = obj['category']
        self.wrongAnswers = obj['wrongAnswers']

    def save(self, include_team=False) -> Dict:
        question_obj = {}
        question_obj['id'] = self.id
        question_obj['level'] = self.level
        question_obj['text'] = self.text
        question_obj['correctAnswer'] = self.correctAnswer
        question_obj['wrongAnswers'] = self.wrongAnswers
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
