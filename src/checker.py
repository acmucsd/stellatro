from typing import List
from card import RANKS, SUITS, Card
from collections import Counter

class Checker:
    def __init__(self, hand: List[Card]):
        self.hand = hand

    def is_straight(self, ranks: List[int]) -> bool:
        """Return True if ranks form a straight (supports A-2-3-4-5)."""
        uniq = sorted(set(ranks))
        if len(uniq) != 5:
            return False
        # normal straight
        if uniq[-1] - uniq[0] == 4:
            return True
        # wheel: A,2,3,4,5
        return uniq == [2, 3, 4, 5, 14]

    def check(self) -> str:
        """
        Given 5 cards, return hand name.
        """
        if len(self.hand) != 5:
            raise ValueError("Hand must contain exactly 5 cards to classify.")

        ranks = [c.rank for c in self.hand]
        suits = [c.suit for c in self.hand]
        rank_counts = Counter(ranks)
        counts = sorted(rank_counts.values(), reverse=True)

        flush = len(set(suits)) == 1
        straight = self.is_straight(ranks)

        if straight and flush:
            return "Straight Flush"
        if counts == [4, 1]:
            return "Four of a Kind"
        if counts == [3, 2]:
            return "Full House"
        if flush:
            return "Flush"
        if straight:
            return "Straight"
        if counts == [3, 1, 1]:
            return "Three of a Kind"
        if counts == [2, 2, 1]:
            return "Two Pair"
        if counts == [2, 1, 1, 1]:
            return "Pair"
        return "High Card"
