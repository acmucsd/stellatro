import random
import pygame
from card import Card
from typing import List, Tuple
from checker import Checker, HandType
from rank import Rank
from suit import Suit
from itertools import product
from random import randint

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
        return self.name + ": " + self.description


class JokerSprite(pygame.sprite.Sprite):
    def __init__(self, joker : Joker, image, x=0, y=0):
        super().__init__()
        self.joker = joker
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))


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
            HandType.PAIR,
            HandType.TWO_PAIR,
            HandType.THREE_OF_A_KIND,
            HandType.FULL_HOUSE,
            HandType.FOUR_OF_A_KIND,
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
            HandType.PAIR,
            HandType.TWO_PAIR,
            HandType.THREE_OF_A_KIND,
            HandType.FULL_HOUSE,
            HandType.FOUR_OF_A_KIND,
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
            HandType.THREE_OF_A_KIND,
            HandType.FULL_HOUSE,
            HandType.FOUR_OF_A_KIND,
        }:
            return chips, mult + 5
        return chips, mult


class TwoPairMultBoost(Joker):
    name = "Cheeky Joker"
    description = "Boost multiplier by 4 if the hand includes Two Pair."

    def post_card_phase(self, chips, mult, hand):
        Checker_instance = Checker(hand)
        hand_type = Checker_instance.check()
        if hand_type in {
            HandType.TWO_PAIR,
            HandType.FULL_HOUSE,
            HandType.FOUR_OF_A_KIND,
        }:
            return chips, mult + 4
        return chips, mult


class StraightMultBoost(Joker):
    name = "Witty Joker"
    description = "Boost multiplier by 6 if the hand includes Straight."

    def post_card_phase(self, chips, mult, hand):
        Checker_instance = Checker(hand)
        hand_type = Checker_instance.check()
        if hand_type in {
            HandType.STRAIGHT,
            HandType.STRAIGHT_FLUSH,
        }:
            return chips, mult + 6
        return chips, mult


class FlushMultBoost(Joker):
    name = "Daring Joker"
    description = "Boost multiplier by 7 if the hand includes Flush."

    def post_card_phase(self, chips, mult, hand):
        Checker_instance = Checker(hand)
        hand_type = Checker_instance.check()
        if hand_type in {
            HandType.FLUSH,
            HandType.STRAIGHT_FLUSH,
        }:
            return chips, mult + 7
        return chips, mult


class TripletChipBoost(Joker):
    name = "Merry Joker"
    description = "Add 15 chips if the hand includes Three of a Kind."

    def post_card_phase(self, chips, mult, hand):
        Checker_instance = Checker(hand)
        hand_type = Checker_instance.check()
        if hand_type in {
            HandType.THREE_OF_A_KIND,
            HandType.FULL_HOUSE,
            HandType.FOUR_OF_A_KIND,
        }:
            return chips + 15, mult
        return chips, mult


class TwoPairChipBoost(Joker):
    name = "Jovial Joker"
    description = "Add 12 chips if the hand includes Two Pair."

    def post_card_phase(self, chips, mult, hand):
        Checker_instance = Checker(hand)
        hand_type = Checker_instance.check()
        if hand_type in {
            HandType.TWO_PAIR,
            HandType.FULL_HOUSE,
            HandType.FOUR_OF_A_KIND,
        }:
            return chips + 12, mult
        return chips, mult


class StraightChipBoost(Joker):
    name = "Lively Joker"
    description = "Add 20 chips if the hand includes Straight."

    def post_card_phase(self, chips, mult, hand):
        Checker_instance = Checker(hand)
        hand_type = Checker_instance.check()
        if hand_type in {
            HandType.STRAIGHT,
            HandType.STRAIGHT_FLUSH,
        }:
            return chips + 20, mult
        return chips, mult


class FlushChipBoost(Joker):
    name = "Vibrant Joker"
    description = "Add 25 chips if the hand includes Flush."

    def post_card_phase(self, chips, mult, hand):
        Checker_instance = Checker(hand)
        hand_type = Checker_instance.check()
        if hand_type in {
            HandType.FLUSH,
            HandType.STRAIGHT_FLUSH,
        }:
            return chips + 25, mult
        return chips, mult


class DiamondMultBoost(Joker):
    name = "Diamond Joker"
    description = "Played cards with Diamond suit boost multiplier by 2."

    def apply_card_phase(
        self, chips: int, mult: int, rank: Rank, suit: Suit
    ) -> Tuple[int, int]:
        if suit == Suit.DIAMOND:
            return chips, mult + 2
        return chips, mult


class HeartMultBoost(Joker):
    name = "Heart Joker"
    description = "Played cards with Heart suit boost multiplier by 2."

    def apply_card_phase(
        self, chips: int, mult: int, rank: Rank, suit: Suit
    ) -> Tuple[int, int]:
        if suit == Suit.HEART:
            return chips, mult + 2
        return chips, mult


class ClubMultBoost(Joker):
    name = "Club Joker"
    description = "Played cards with Club suit boost multiplier by 2."

    def apply_card_phase(
        self, chips: int, mult: int, rank: Rank, suit: Suit
    ) -> Tuple[int, int]:
        if suit == Suit.CLUB:
            return chips, mult + 2
        return chips, mult


class SpadeMultBoost(Joker):
    name = "Spade Joker"
    description = "Played cards with Spade suit boost multiplier by 2."

    def apply_card_phase(
        self, chips: int, mult: int, rank: Rank, suit: Suit
    ) -> Tuple[int, int]:
        if suit == Suit.SPADE:
            return chips, mult + 2
        return chips, mult


# class Superposition(Joker):
#     name = "Superposition"
#     description = "(The Ace can represent any rank to form a Straight)"

#     def post_card_phase(self, chips, mult, hand):
#         has_ace = False
#         has_straight = self.can_form_straight(hand)
#         for card in hand:
#             if 14 in card.ranks:
#                 has_ace = True
#         return chips, mult + 20 if has_ace and has_straight else chips, mult

#     def can_form_straight(self, hand: List[Card]) -> bool:
#         rank_choices = [list(card.ranks) for card in hand]
#         for combination in product(*rank_choices):
#             checker = Checker(list(combination))
#             if checker.is_straight():
#                 return True
#         return False


# class Cavendish(Joker):
#     name = "Cavendish"
#     description = "(1 in 1000 chance for x3 Mult)"

#     def post_card_phase(self, chips, mult, hand):
#         rand_int = randint(1, 1000)
#         return chips, mult * 3 if rand_int == 1 else chips, mult


# class SquareJoker(Joker):
#     name = "Square Joker"
#     description = "(This joker gains +5 chips for each hand played)"
#     chips = 0

#     def post_card_phase(self, chips, mult, hand):
#         self.chips += 5
#         return chips + self.chips, mult


# class Obelisk(Joker):
#     name = "Obelisk"
#     description = "(This joker gains x0.2 Mult per consecutive hand played without playing your most played poker hand)"
#     poker_hands = {}
#     current_mult = 0

#     def post_card_phase(self, chips, mult, hand):
#         highestCount = 0
#         highestHand = None
#         for handType, count in self.poker_hands.items():
#             if count > highestCount:
#                 highestCount = count
#                 highestHand = handType

#         checker = Checker(hand)
#         hand_type = checker.check()
#         if hand_type not in self.poker_hands:
#             self.poker_hands[hand_type] = 1
#         else:
#             self.poker_hands[hand_type] += 1
#         if highestHand != hand_type or highestCount == 0:
#             self.current_mult += 0.2
#         return chips, mult * (1 + self.current_mult)


# class Hiker(Joker):
#     name = "Hiker"
#     description = "(Every played card is granted +5 chips when scored)"

#     card_table = {}

#     def apply_card_phase(self, chips, mult, rank, suit):
#         if (rank, suit) in self.card_table:
#             self.card_table[(rank, suit)] += 5
#         else:
#             self.card_table[(rank, suit)] = 5
#         return chips + self.card_table[(rank, suit)], mult


def generate_jokers(num_jokers: int) -> List[Joker]:
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
        # Superposition(),
        # Cavendish(),
        # SquareJoker(),
        # Obelisk(),
        # Hiker(),
    ]

    toReturn = []
    # shuffle
    random.shuffle(ALL_JOKERS)
    for i in range(num_jokers):
        toReturn.append(ALL_JOKERS[i % len(ALL_JOKERS)])
    return toReturn
