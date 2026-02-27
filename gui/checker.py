from typing import List
from card import Card
from collections import Counter
from enum import Enum


class HandType(Enum):
    HIGH_CARD = 1
    PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    STRAIGHT = 5
    FLUSH = 6
    FULL_HOUSE = 7
    FOUR_OF_A_KIND = 8
    STRAIGHT_FLUSH = 9


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
    def checkGUI(self) -> HandType:
        """
        Given at most 5 cards, return hand name.
        """
        # for now, each card should only have one rank and one suit
        ranks = [c.rank for c in self.hand]
        suits = [c.suits for c in self.hand]
        
        unique_suits = set()
        for s_set in [c.suits for c in self.hand]:
            unique_suits.update(s_set)

        # rank scoring
        rank_counts = Counter(ranks)
        counts = sorted(rank_counts.values(), reverse=True)

        flush = len(unique_suits) == 1 and len(ranks) == 5
        straight = self.is_straight(ranks)

        hand_type = HandType.HIGH_CARD

        if straight and flush:
            hand_type = HandType.STRAIGHT_FLUSH
        elif counts.count(4) == 1:
            hand_type = HandType.FOUR_OF_A_KIND
        elif counts == [3, 2]:
            hand_type = HandType.FULL_HOUSE
        elif flush:
            hand_type = HandType.FLUSH
        elif straight:
            hand_type = HandType.STRAIGHT
        elif counts.count(3) == 1:
            hand_type = HandType.THREE_OF_A_KIND
        elif counts.count(2) == 2:
            hand_type = HandType.TWO_PAIR
        elif counts.count(2) == 1:
            hand_type = HandType.PAIR
        return hand_type

    def check(self) -> HandType:
        """
        Given 5 cards, return hand name.
        """
        if len(self.hand) != 5:
            raise ValueError("Hand must contain exactly 5 cards to classify.")
        for c in self.hand:
            c.scored = False
        # for now, each card should only have one rank and one suit
        ranks = [c.rank for c in self.hand]
        suits = [c.suits for c in self.hand]

        # rank scoring
        rank_counts = Counter(ranks)
        counts = sorted(rank_counts.values(), reverse=True)

        flush = len(suits) == 1
        straight = self.is_straight(ranks)

        hand_type = HandType.HIGH_CARD

        if straight and flush:
            hand_type = HandType.STRAIGHT_FLUSH
            # score all cards
            for c in self.hand:
                c.scored = True
        elif counts == [4, 1]:
            hand_type = HandType.FOUR_OF_A_KIND
            # score four cards
            most_common_rank = rank_counts.most_common(1)[0][0]
            for c in self.hand:
                if c.rank == most_common_rank:
                    c.scored = True
        elif counts == [3, 2]:
            hand_type = HandType.FULL_HOUSE
            # score all cards
            for c in self.hand:
                c.scored = True
        elif flush:
            hand_type = HandType.FLUSH
            # score all cards
            for c in self.hand:
                c.scored = True
        elif straight:
            hand_type = HandType.STRAIGHT
            # score all cards
            for c in self.hand:
                c.scored = True
        elif counts == [3, 1, 1]:
            hand_type = HandType.THREE_OF_A_KIND
            # score three cards
            most_common_rank = rank_counts.most_common(1)[0][0]
            for c in self.hand:
                if c.rank == most_common_rank:
                    c.scored = True
        elif counts == [2, 2, 1]:
            hand_type = HandType.TWO_PAIR
            # score four cards
            pairs = [rank for rank, count in rank_counts.items() if count == 2]
            for c in self.hand:
                if c.rank in pairs:
                    c.scored = True
        elif counts == [2, 1, 1, 1]:
            hand_type = HandType.PAIR
            # score two cards
            pair_rank = rank_counts.most_common(1)[0][0]
            for c in self.hand:
                if c.rank == pair_rank:
                    c.scored = True
        else:
            hand_type = HandType.HIGH_CARD
            highest_card = self.hand[0]
            for c in self.hand:
                if c.rank > highest_card.rank:
                    highest_card = c
            highest_card.scored = True
        return hand_type
