from __future__ import annotations

from typing import List


class Question(object):
    """docstring for Question."""
    id: int
    level: int
    test: str
    correctAnswer: str
    wrongAnsweres: List[str]
    category: str

    def __init__(self, arg):
        super(Question, self).__init__()
        self.arg = arg


def load(json_str: str) -> List[Question]:
    pass


def save(questions: List[Question]) -> str:
    pass
