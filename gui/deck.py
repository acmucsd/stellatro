import pygame
from card import Card, CardBackground
from spritesheet import SpriteSheet
from rank import Rank, RANKS
from suit import Suit, SUITS
from typing import List
import random
from utils import instantiate_card




class Deck:
    def __init__(self, bg_sheet, sheet, cardBackground : CardBackground):
        self.bg_sheet = bg_sheet
        self.sheet = sheet
        self.cardBackground = cardBackground
        self.build_and_shuffle()
    def build_and_shuffle(self):
        """Standardizes deck creation and shuffling."""
        self.cards = [
            instantiate_card(self.bg_sheet, self.sheet, r, s, self.cardBackground) 
            for s in SUITS for r in RANKS
        ]
        random.shuffle(self.cards)
    def add_card(self, card):
        self.cards.append(card)
    def draw(self, n: int) -> List[Card]:
        if len(self.cards) < n:
            self.build_and_shuffle()
        drawn_cards = []
        for _ in range(min(n, len(self.cards))):
            drawn_cards.append(self.cards.pop())
        return drawn_cards