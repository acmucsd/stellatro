import os
from rank import Rank, RANKS
from suit import Suit
from card import Card, CardBackground
from spritesheet import SpriteSheet
from checker import HandType
import pygame


GUI_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(GUI_DIR,"../assets")

def get_assets_path(asset_file_name):
    return os.path.join(ASSETS_DIR,asset_file_name)

BALATRO_CARD_IMAGE_URL_TABLE = {}

def _initialize_balatro_card_image_table():
    """
    Populates the BALATRO_CARD_IMAGE_URL_TABLE with mappings from (rank, suit)
    to the corresponding image file path based on the asset naming convention.
    0-12: Hearts (2-A)
    13-25: Clubs (2-A)
    26-38: Diamonds (2-A)
    39-51: Spades (2-A)
    """
    ranks_in_order = sorted(list(RANKS.keys())) # [2, 3, ..., 14]

    suit_base_indices = {
        Suit.HEART: 0,
        Suit.CLUB: 13,
        Suit.DIAMOND: 26,
        Suit.SPADE: 39,
    }

    for suit, base_index in suit_base_indices.items():
        for i, rank in enumerate(ranks_in_order):
            image_index = base_index + i
            BALATRO_CARD_IMAGE_URL_TABLE[(rank, suit)] = f"balatro_playing_cards/balatro_playing_cards_{image_index}.png"

_initialize_balatro_card_image_table()

# Card Background Sprite Sheets
card_back_img = pygame.image.load(get_assets_path('balatro_card_backgrounds/card_background_0.png'))
white_front_img = pygame.image.load(get_assets_path('balatro_card_backgrounds/card_background_1.png'))
CARD_SCALE = 0.7
card_back_image = pygame.transform.smoothscale(card_back_img, (card_back_img.get_width() * CARD_SCALE, card_back_img.get_height() * CARD_SCALE) )
white_front_image = pygame.transform.smoothscale(white_front_img, (white_front_img.get_width() * CARD_SCALE, white_front_img.get_height() * CARD_SCALE) )
def instantiate_card(sheet,rank: str, suit: Suit, background: CardBackground, x=0, y=0):
    if rank == "J":
        rank = 11
    elif rank == "Q":
        rank = 12
    elif rank == "K":
        rank = 13
    elif rank == "A":
        rank = 14
    else:
        rank = int(rank)
    
    front_image = getCardImage(sheet, rank, suit)

    new_card = Card(background, rank, suit, front_image,white_front_image, x, y)
    new_card.face_down_image = card_back_image
    return new_card

def instantiate_joker(sheet, joker):
    pass


def getCardImage(sheet : SpriteSheet, rank : Rank , suit : Suit):
    if suit == Suit.HEART:
        row = 0
    elif suit == Suit.CLUB:
        row = 1
    elif suit == Suit.DIAMOND:
        row = 2
    elif suit == Suit.SPADE:
        row = 3
    col = rank - 2
    return sheet.get_image(row,col,70,94,CARD_SCALE,(255,255,255),1,1)
def getHandTypeStr(hand_type : HandType):
    if hand_type == HandType.HIGH_CARD:
        return "High Card"
    elif hand_type == HandType.PAIR:
        return "Pair"
    elif hand_type == HandType.TWO_PAIR:
        return "Two Pair"
    elif hand_type == HandType.THREE_OF_A_KIND:
        return "Three of a Kind"
    elif hand_type == HandType.STRAIGHT:
        return "Straight"
    elif hand_type == HandType.FLUSH:
        return "Flush"
    elif hand_type == HandType.FULL_HOUSE:
        return "Full House"
    elif hand_type == HandType.FOUR_OF_A_KIND:
        return "Four of a Kind"
    elif hand_type == HandType.STRAIGHT_FLUSH:
        return "Straight Flush"
    else:
        return "Invalid Hand Type"
