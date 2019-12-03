from __future__ import annotations

from typing import List, Dict
from enum import IntEnum, unique


@unique
class OfferType(IntEnum):
    HIGH = 0
    NORMAL = 1
    LOW = 2

    def __str__(self):
        return str(self.value)


class Offer(object):
    """docstring for Round."""
    type: OfferType = OfferType.NORMAL
    accepted: bool = False
    amount: int = 0

    def __init__(self):
        super(Offer, self).__init__()

    def save(self) -> Dict:
        offer_obj = {}
        offer_obj['type'] = self.type
        offer_obj['accepted'] = self.accepted
        offer_obj['amount'] = self.amount

        return offer_obj


def load(json_str: str) -> List[Offer]:
    pass


def save(offers: List[Offer]) -> List:
    obj = []
    for offer in offers:
        obj.append(offer.save())
    return obj
