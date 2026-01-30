from card import Card
from typing import List, Tuple
from checker import HandType
from checker import Checker
from card import Rank, Suit


# Base class for jokers
class Joker:
    name: str
    description: str

    def pre_card_phase(self, hand: List[Card]) -> Tuple[List[Card]]:
        """Return (hand) after pre-phase application of joker."""
        return hand

    def apply_card_phase(
        self, chips: int, mult: int, rank: Rank, suit: Suit
    ) -> Tuple[int, int]:
        """Return (chips, mult) after hand evaluation application of joker."""
        return chips, mult

    def post_card_phase(
        self, chips: int, mult: int, hand: List[Card]
    ) -> Tuple[int, int]:
        """Return (chips, mult) after post-phase application of joker."""
        return chips, mult

    def __str__(self) -> str:
        return self.name


class RegularJoker(Joker):
    name = "Regular Joker"
    description = "No special abilities."


class PairMultBoost(Joker):
    name = "Jolly Joker"
    description = "Boost multiplier by 3 if the hand includes Pair."

    def post_card_phase(
        self, chips: int, mult: int, hand: List[Card]
    ) -> Tuple[int, int]:
        Checker_instance = Checker(hand)
        hand_type = Checker_instance.check()
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
    name = "Sly Joker"
    description = "Add 10 chips if the hand includes Pair."

    def post_card_phase(self, chips, mult, hand):
        Checker_instance = Checker(hand)
        hand_type = Checker_instance.check()
        if hand_type in {
            "Pair",
            "Two Pair",
            "Three of a Kind",
            "Full House",
            "Four of a Kind",
        }:
            return chips + 10, mult
        return chips, mult


class TripletMultBoost(Joker):
    name = "Zany Joker"
    description = "Boost multiplier by 5 if the hand includes Three of a Kind."

    def post_card_phase(self, chips, mult, hand):
        Checker_instance = Checker(hand)
        hand_type = Checker_instance.check()
        if hand_type in {
            "Three of a Kind",
            "Full House",
            "Four of a Kind",
        }:
            return chips, mult + 5
        return chips, mult


def TwoPairMultBoost(Joker):
    name = "Cheeky Joker"
    description = "Boost multiplier by 4 if the hand includes Two Pair."

    def post_card_phase(self, chips, mult, hand):
        Checker_instance = Checker(hand)
        hand_type = Checker_instance.check()
        if hand_type in {
            "Two Pair",
            "Full House",
            "Four of a Kind",
        }:
            return chips, mult + 4
        return chips, mult


def StraightMultBoost(Joker):
    name = "Witty Joker"
    description = "Boost multiplier by 6 if the hand includes Straight."

    def post_card_phase(self, chips, mult, hand):
        Checker_instance = Checker(hand)
        hand_type = Checker_instance.check()
        if hand_type in {
            "Straight",
            "Straight Flush",
        }:
            return chips, mult + 6
        return chips, mult


def FlushMultBoost(Joker):
    name = "Daring Joker"
    description = "Boost multiplier by 7 if the hand includes Flush."

    def post_card_phase(self, chips, mult, hand):
        Checker_instance = Checker(hand)
        hand_type = Checker_instance.check()
        if hand_type in {
            "Flush",
            "Straight Flush",
        }:
            return chips, mult + 7
        return chips, mult


def TripletChipBoost(Joker):
    name = "Merry Joker"
    description = "Add 15 chips if the hand includes Three of a Kind."

    def post_card_phase(self, chips, mult, hand):
        Checker_instance = Checker(hand)
        hand_type = Checker_instance.check()
        if hand_type in {
            "Three of a Kind",
            "Full House",
            "Four of a Kind",
        }:
            return chips + 15, mult
        return chips, mult


def TwoPairChipBoost(Joker):
    name = "Jovial Joker"
    description = "Add 12 chips if the hand includes Two Pair."

    def post_card_phase(self, chips, mult, hand):
        Checker_instance = Checker(hand)
        hand_type = Checker_instance.check()
        if hand_type in {
            "Two Pair",
            "Full House",
            "Four of a Kind",
        }:
            return chips + 12, mult
        return chips, mult


def StraightChipBoost(Joker):
    name = "Lively Joker"
    description = "Add 20 chips if the hand includes Straight."

    def post_card_phase(self, chips, mult, hand):
        Checker_instance = Checker(hand)
        hand_type = Checker_instance.check()
        if hand_type in {
            "Straight",
            "Straight Flush",
        }:
            return chips + 20, mult
        return chips, mult


def FlushChipBoost(Joker):
    name = "Vibrant Joker"
    description = "Add 25 chips if the hand includes Flush."

    def post_card_phase(self, chips, mult, hand):
        Checker_instance = Checker(hand)
        hand_type = Checker_instance.check()
        if hand_type in {
            "Flush",
            "Straight Flush",
        }:
            return chips + 25, mult
        return chips, mult


def DiamondMultBoost(Joker):
    name = "Diamond Joker"
    description = "Played cards with Diamond suit boost multiplier by 2."

    def apply_card_phase(
        self, chips: int, mult: int, rank: Rank, suit: Suit
    ) -> Tuple[int, int]:
        if suit == Suit.DIAMOND:
            return chips, mult + 2
        return chips, mult


def HeartMultBoost(Joker):
    name = "Heart Joker"
    description = "Played cards with Heart suit boost multiplier by 2."

    def apply_card_phase(
        self, chips: int, mult: int, rank: Rank, suit: Suit
    ) -> Tuple[int, int]:
        if suit == Suit.HEART:
            return chips, mult + 2
        return chips, mult


def ClubMultBoost(Joker):
    name = "Club Joker"
    description = "Played cards with Club suit boost multiplier by 2."

    def apply_card_phase(
        self, chips: int, mult: int, rank: Rank, suit: Suit
    ) -> Tuple[int, int]:
        if suit == Suit.CLUB:
            return chips, mult + 2
        return chips, mult


def SpadeMultBoost(Joker):
    name = "Spade Joker"
    description = "Played cards with Spade suit boost multiplier by 2."

    def apply_card_phase(
        self, chips: int, mult: int, rank: Rank, suit: Suit
    ) -> Tuple[int, int]:
        if suit == Suit.SPADE:
            return chips, mult + 2
        return chips, mult


def generate_jokers() -> List[Joker]:
    # For simplicity, return all jokers; in a real game, this could be randomized
    ALL_JOKERS = [
        PairMultBoost(),
        PairChipBoost(),
        FlushMultBoost(),
        TripletChipBoost(),
        TwoPairChipBoost(),
        StraightChipBoost(),
        FlushChipBoost(),
        DiamondMultBoost(),
        HeartMultBoost(),
        ClubMultBoost(),
        SpadeMultBoost(),
    ]
    return ALL_JOKERS
