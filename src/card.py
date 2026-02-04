from typing import List
import random
from dataclasses import dataclass
from enum import Enum


class Suit(Enum):
    DIAMOND = "diamond"
    HEART = "heart"
    CLUB = "club"
    SPADE = "spade"


class Rank(Enum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14


RANKS = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]  # 11=J,12=Q,13=K,14=A
SUITS = [Suit.DIAMOND, Suit.HEART, Suit.CLUB, Suit.SPADE]
RANK_TO_STR = {11: "J", 12: "Q", 13: "K", 14: "A"}


class Card:
    rank: int
    suits: set[Suit]
    scored: bool = True
    num_triggers = 1

    def __init__(self, rank: int, suit: Suit):
        # Initialize as sets using curly braces
        self.rank = rank
        self.suits = {suit}

    def add_suit(self, suit: Suit):
        # Use .add() for sets
        self.suits.add(suit)

    def add_trigger(self):
        self.num_triggers += 1

    def __str__(self):
        rank_str = RANK_TO_STR.get(self.rank, str(self.rank))
        suits_list = sorted([s.value for s in self.suits])
        suits_str = ", ".join(suits_list)
        return f"{rank_str} of {suits_str}"


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
