import random
from card import Card
from typing import List, Tuple
from checker import HandType
from checker import Checker
from card import Rank, Suit
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


class PhotoGraphMultBoost(Joker):
    name = "PhotoGraph Joker"
    description = "First played face card gives X2 Mult when scored"

    ## How to differentiate face cards?
    def apply_card_phase(
        self, chips: int, mult: int, rank: Rank, suit: Suit
    ) -> Tuple[int, int]:
        if rank == 10:
            return chips, mult * 2
        return chips, mult


class FlowerPot(Joker):
    name = "Flower Pot"
    description = "x3 Mult if played hand contains a diamond, heart, spade, and club"

    def post_card_phase(self, chips, mult, hand):
        has_diamond = False
        has_heart = False
        has_club = False
        has_spade = False
        for card in hand:
            if Suit.DIAMOND in card.suits:
                has_diamond = True
            if Suit.HEART in card.suits:
                has_heart = True
            if Suit.CLUB in card.suits:
                has_club = True
            if Suit.SPADE in card.suits:
                has_spade = True
        if has_diamond and has_heart and has_club and has_spade:
            return chips, mult * 3
        return chips, mult


class TheDuo(Joker):
    name = "The Duo"
    description = "If hand contains a pair, x2 Mult"

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
            return chips, mult * 2
        return chips, mult


class TheTrio(Joker):
    name = "The Trio"
    description = "If hand contains a Three of a Kind, x3 Mult"

    def post_card_phase(self, chips, mult, hand):
        Checker_instance = Checker(hand)
        hand_type = Checker_instance.check()

        # Includes hands that contain at least 3 of a kind
        if hand_type in {
            HandType.THREE_OF_A_KIND,
            HandType.FULL_HOUSE,
            HandType.FOUR_OF_A_KIND,
        }:
            return chips, mult * 3
        return chips, mult


class TheFamily(Joker):
    name = "The Family"
    description = "If hand contains a Four of a Kind, x4 Mult"

    def post_card_phase(self, chips, mult, hand):
        Checker_instance = Checker(hand)
        hand_type = Checker_instance.check()

        if hand_type in {
            HandType.FOUR_OF_A_KIND,
        }:
            return chips, mult * 4
        return chips, mult


class TheTribe(Joker):
    name = "The Tribe"
    description = "If hand contains a Flush, x3 Mult"

    def post_card_phase(self, chips, mult, hand):
        Checker_instance = Checker(hand)
        hand_type = Checker_instance.check()

        # Includes standard flushes and straight flushes
        if hand_type in {
            HandType.FLUSH,
            HandType.STRAIGHT_FLUSH,
            HandType.ROYAL_FLUSH,  # Include if your Enum distinguishes Royal Flushes
        }:
            return chips, mult * 3
        return chips, mult


class TheOrder(Joker):
    name = "The Order"
    description = "If hand contains a Straight, x3 Mult"

    def post_card_phase(self, chips, mult, hand):
        Checker_instance = Checker(hand)
        hand_type = Checker_instance.check()

        # Includes standard straights and straight flushes
        if hand_type in {
            HandType.STRAIGHT,
            HandType.STRAIGHT_FLUSH,
            HandType.ROYAL_FLUSH,
        }:
            return chips, mult * 3
        return chips, mult


class TheSingle(Joker):
    name = "UC Socially Dead"
    description = "If hand contains only a High Card, x5 Mult"

    def post_card_phase(self, chips, mult, hand):
        Checker_instance = Checker(hand)
        hand_type = Checker_instance.check()

        if hand_type == HandType.HIGH_CARD:
            return chips, mult * 5
        return chips, mult


class BitByte(Joker):
    name = "Bit Byte"
    description = "Face cards add 2 mult, number cards add 8 chips"

    def apply_card_phase(
        self, chips: int, mult: int, rank: Rank, suit: Suit
    ) -> Tuple[int, int]:
        if rank in {11, 12, 13}:  # Face cards
            return chips, mult + 2
        elif 2 <= rank <= 10:  # Number cards
            return chips + 8, mult
        return chips, mult


class StudentID(Joker):
    name = "Student ID"
    description = "If hand contains a single ace and no face cards, +10 mult"

    def post_card_phase(self, chips, mult, hand):
        Checker_instance = Checker(hand)
        hand_type = Checker_instance.check()

        has_single_ace = False
        has_face_card = False
        for card in hand:
            if card.rank == 14:  # Ace
                if has_single_ace:  # More than one ace
                    return chips, mult
                has_single_ace = True
            elif card.rank in {11, 12, 13}:  # Face cards
                has_face_card = True

        if has_single_ace and not has_face_card:
            return chips, mult + 10
        return chips, mult


class WebReg(Joker):
    name = "WebReg"
    description = "Retrigger each card that has rank <= 8"

    def pre_card_phase(self, hand):
        for card in hand:
            if card.rank <= 8:
                card.add_trigger()
        return hand


class LastLecture(Joker):
    name = "Last Lecture"
    description = "Final card gets retriggered 2 extra times"

    def pre_card_phase(self, hand):
        if hand:
            hand[-1].add_trigger()
            hand[-1].add_trigger()
        return hand


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

class HalfJoker(Joker):
    name = "Half Joker"
    description = "Add 20 to multiplier if played hand contains 3 or fewer cards."

    def post_card_phase(
        self, chips: int, mult: int, hand: List[Card]
    ) -> Tuple[int, int]:
        Checker_instance = Checker(hand)
        hand_type = Checker_instance.check()
        if hand_type in {
            HandType.PAIR,
            HandType.THREE_OF_A_KIND,
            HandType.HIGH_CARD
        }:
            return chips, mult + 20
        return chips, mult
    
# class FourFingers(Joker):
#     name = "Four Fingers Joker"
#     description = "All Flushes and Straights can be made with 4 cards."

#     def pre_card_phase(self, hand: List[Card]) -> Tuple[List[Card]]:
#         """Return (hand) after pre-phase application of joker."""
#         return hand

#     def post_card_phase(
#         self, chips: int, mult: int, hand: List[Card]
#     ) -> Tuple[int, int]:
#         Checker_instance = Checker(hand)
#         hand_type = Checker_instance.check()
#         if hand_type in {
#             HandType.PAIR,
#             HandType.THREE_OF_A_KIND,
#             HandType.HIGH_CARD
#         }:
#             return chips, mult + 20
#         return chips, mult

# class RaisedFist(Joker):
#     name = "Raised Fist Joker"
#     description = "Adds double the rank of lowest ranked card held in hand to mult."

#     lowest_rank = 1000000

#     def post_card_phase(
#         self, chips: int, mult: int, hand: List[Card]
#     ) -> Tuple[int, int]:
#         Checker_instance = Checker(hand)
#         hand_type = Checker_instance.check()
#         if hand_type in {
#             HandType.PAIR,
#             HandType.THREE_OF_A_KIND,
#             HandType.HIGH_CARD
#         }:
#             return chips, mult + 20
#         return chips, mult

class Fibonacci(Joker):
    name = "Fibonacci Joker"
    description = "Each played Ace, 2, 3, 5, or 8 gives +8 Mult when scored."

    def apply_card_phase(
        self, chips: int, mult: int, rank: Rank, suit: Suit
    ) -> Tuple[int, int]:
        mult_add = 0
        if rank == 14 or rank == 2 or rank == 3 or rank == 5 or rank == 8:
            return chips, mult + 8
        return chips, mult
    
class ScaryFace(Joker):
    name = "Scary Face Joker"
    description = "Each face card gives +10 mult."

    def apply_card_phase(
        self, chips: int, mult: int, rank: Rank, suit: Suit
    ) -> Tuple[int, int]:
        mult_add = 0
        if rank == 11 or rank == 12 or rank == 13:
            return chips, mult + 10
        return chips, mult


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
        HalfJoker(),
        Fibonacci(),
        ScaryFace(),
    ]

    toReturn = []
    # shuffle
    random.shuffle(ALL_JOKERS)
    for i in range(num_jokers):
        toReturn.append(ALL_JOKERS[i % len(ALL_JOKERS)])
    return toReturn
