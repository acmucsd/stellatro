import random
from enum import Enum
from typing import List
from collections import Counter

from src.jokers import *
from src.card import RANKS, SUITS, Card
from src.checker import Checker, HandType

class SimpleBot():
    """
    A simple bot that picks jokers based on hand type (using Checker).
    """ 
    def __init__(self):
        pass

    def pick_joker(self, game_state):
        # Placeholder for bot decision logic
        checker = Checker(game_state["hand"])
        hand_type = checker.check()
        if hand_type == HandType.PAIR:
            # If we have a pair, pick a joker that boosts pairs
            for joker in game_state["jokers"]:
                if isinstance(joker, PairMultBoost) or isinstance(joker, PairChipBoost):
                    return joker
        # Otherwise, pick a random joker
        return random.choice(game_state["jokers"])
    
    def finalize_jokers(self):
        # Placeholder for finalizing jokers
        # return the best hand and the arranged jokers
        return [], []