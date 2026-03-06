import random
import pygame
import math
from card import Card
from typing import List, Tuple
from checker import Checker, HandType
from rank import Rank
from suit import Suit
from itertools import product
from random import randint
from utils import get_assets_path

#key : imageUrl, value: pygame.Surface
JOKER_IMAGE_TABLE = {}

# Base class for jokers
class Joker(pygame.sprite.Sprite):
    name: str
    description: str
    imageUrl : str
    
    def __init__(self):
        super().__init__()
        if self.imageUrl not in JOKER_IMAGE_TABLE:
            img_path = get_assets_path(self.imageUrl)
            # Using .convert_alpha() is good practice for performance with transparent images
            JOKER_IMAGE_TABLE[self.imageUrl] = pygame.image.load(img_path).convert_alpha()
        
        self.original_image = JOKER_IMAGE_TABLE[self.imageUrl]
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(topleft=(0, 0))
        self.target_pos = pygame.math.Vector2(self.rect.center)
        self.lerp_speed= 20
        self.selected = False

        # Shake animation attributes
        self.is_shaking = False
        self.shake_timer = 0.0
        self.shake_duration = 0.3  # seconds
        self.shake_angle = 15      # degrees
    
    def update(self, dt):
        # Position interpolation
        curr_pos = pygame.math.Vector2(self.rect.center)
        if curr_pos.distance_to(self.target_pos) > 1:
            lerp = min(max(self.lerp_speed * dt,0),1)
            new_pos = curr_pos.lerp(self.target_pos, lerp)
            self.rect.center = (new_pos.x, new_pos.y)

        # Shake animation
        if self.is_shaking:
            center = self.rect.center # Save center before rotation changes rect size
            self.shake_timer += dt
            if self.shake_timer >= self.shake_duration:
                self.is_shaking = False
                self.shake_timer = 0.0
                # Restore original image and position
                self.image = self.original_image.copy()
                self.rect = self.image.get_rect(center=center)
            else:
                progress = self.shake_timer / self.shake_duration
                # A sine wave for rotation angle. pi*4 gives two full shakes.
                angle = self.shake_angle * math.sin(progress * math.pi * 4)
                
                # Rotate from original image to avoid quality degradation
                self.image = pygame.transform.rotate(self.original_image, angle)
                self.rect = self.image.get_rect(center=center)

    def shake(self):
        if not self.is_shaking:
            self.is_shaking = True
            self.shake_timer = 0.0
        else:
            self.shake_timer = 0.0


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
    imageUrl = "balatro_jokers/balatro_jokers_0.png"
    
class PairMultBoost(Joker):
    name = "Jolly Joker"
    description = "Boost multiplier by 3 if the hand includes Pair."
    imageUrl = "balatro_jokers/balatro_jokers_1.png"

    def post_card_phase(self, chips: int, mult: int, hand: List[Card]) -> Tuple[int, int]:
        Checker_instance = Checker(hand)
        hand_type = Checker_instance.check()
        if hand_type in {HandType.PAIR,HandType.TWO_PAIR,HandType.THREE_OF_A_KIND,HandType.FULL_HOUSE,HandType.FOUR_OF_A_KIND,}:
            return chips, mult + 3
        return chips, mult




class PairChipBoost(Joker):
    name = "Sly Joker"
    description = "Add 10 chips if the hand includes Pair."
    imageUrl = "balatro_jokers/balatro_jokers_2.png" # Added

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
    imageUrl = "balatro_jokers/balatro_jokers_3.png" # Added

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
    imageUrl = "balatro_jokers/balatro_jokers_4.png" # Added

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
    imageUrl = "balatro_jokers/balatro_jokers_5.png" # Added

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
    imageUrl = "balatro_jokers/balatro_jokers_6.png" # Added

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
    imageUrl = "balatro_jokers/balatro_jokers_7.png" # Added

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
    imageUrl = "balatro_jokers/balatro_jokers_8.png" # Added

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
    imageUrl = "balatro_jokers/balatro_jokers_9.png" # Added

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
    imageUrl = "balatro_jokers/balatro_jokers_10.png" # Added

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
    imageUrl = "balatro_jokers/balatro_jokers_11.png" # Added

    def apply_card_phase(
        self, chips: int, mult: int, rank: Rank, suit: Suit
    ) -> Tuple[int, int]:
        if suit == Suit.DIAMOND:
            return chips, mult + 2
        return chips, mult


class HeartMultBoost(Joker):
    name = "Heart Joker"
    description = "Played cards with Heart suit boost multiplier by 2."
    imageUrl = "balatro_jokers/balatro_jokers_12.png" # Added

    def apply_card_phase(
        self, chips: int, mult: int, rank: Rank, suit: Suit
    ) -> Tuple[int, int]:
        if suit == Suit.HEART:
            return chips, mult + 2
        return chips, mult


class ClubMultBoost(Joker):
    name = "Club Joker"
    description = "Played cards with Club suit boost multiplier by 2."
    imageUrl = "balatro_jokers/balatro_jokers_13.png" # Added

    def apply_card_phase(
        self, chips: int, mult: int, rank: Rank, suit: Suit
    ) -> Tuple[int, int]:
        if suit == Suit.CLUB:
            return chips, mult + 2
        return chips, mult


class SpadeMultBoost(Joker):
    name = "Spade Joker"
    description = "Played cards with Spade suit boost multiplier by 2."
    imageUrl = "balatro_jokers/balatro_jokers_14.png" # Added

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
