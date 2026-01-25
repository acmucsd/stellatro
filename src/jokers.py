from card import Card
from typing import List, Tuple


# Base class for jokers
class Joker:
    name: str

    def pre_card(self, chips: int, mult: int, hand: List[Card]) -> Tuple[int, int]:
        """Return (chips, mult) after pre-phase application of joker."""
        return chips, mult

    def apply_card(self, chips: int, mult: int, hand: List[Card]) -> Tuple[int, int]:
        """Return (chips, mult) after hand evaluation application of joker."""
        return chips, mult

    def post_card(self, chips: int, mult: int, hand: List[Card]) -> Tuple[int, int]:
        """Return (chips, mult) after post-phase application of joker."""
        return chips, mult

    def __str__(self) -> str:
        return self.name


class PairMultBoost(Joker):
    name = "Pair Boost (+3 mult if the hand includes Pair)"  # Value TBD

    def apply(self, chips: int, mult: int, hand_type: str) -> Tuple[int, int]:
        if hand_type in {
            "Pair",
            "Two Pair",
            "Three of a Kind",
            "Full House",
            "Four of a Kind",
        }:
            return chips, mult + 3
        return chips, mult


class PairChipBoost(Joker):
    name = "Pair Boost (+10 chips if the hand includes Pair)"  # Value TBD

    def apply(self, chips: int, mult: int, hand_type: str) -> Tuple[int, int]:
        if hand_type in {
            "Pair",
            "Two Pair",
            "Three of a Kind",
            "Full House",
            "Four of a Kind",
        }:
            return chips + 10, mult
        return chips, mult


def generate_jokers() -> List[Joker]:
    # For simplicity, return all jokers; in a real game, this could be randomized
    ALL_JOKERS = [PairMultBoost(), PairChipBoost()]
    return ALL_JOKERS
