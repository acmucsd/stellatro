from typing import List
from random import random
from dataclasses import dataclass

RANKS = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]  # 11=J,12=Q,13=K,14=A
SUITS = ["diamond", "heart", "club", "spade"]
RANK_TO_STR = {11: "J", 12: "Q", 13: "K", 14: "A"}

@dataclass(frozen=True)
class Card:
    rank: int
    suit: str

    def __str__(self) -> str:
        r = RANK_TO_STR.get(self.rank, str(self.rank))
        return f"{r}{self.suit}"
    
class Deck:
    def __init__(self):
        self.cards = [Card(r, s) for s in SUITS for r in RANKS]
        random.shuffle(self.cards)

    def draw(self, n: int) -> List[Card]:
        if len(self.cards) < n:
            # simple reshuffle behavior: rebuild new deck when low
            self.__init__()
        out = self.cards[:n]
        self.cards = self.cards[n:]
        return out