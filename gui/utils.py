import os
from rank import Rank
from suit import Suit
from card import Card, CardBackground
from spritesheet import SpriteSheet
from checker import HandType


GUI_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(GUI_DIR,"../assets")

def get_assets_path(asset_file_name):
    return os.path.join(ASSETS_DIR,asset_file_name)

def instantiate_card(bg_sheet, sheet,rank: str, suit: Suit, background: CardBackground, x=0, y=0):
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
    back_image = getCardBackgroundImage(bg_sheet,CardBackground.WHITE_FRONT)
    front_image = getCardImage(sheet, rank, suit)
    back_base = getCardBackgroundImage(bg_sheet, CardBackground.RED)
    new_card = Card(background, rank, suit, front_image,back_image, x, y)
    new_card.face_down_image = back_base
    return new_card
def getCardBackgroundImage(sheet: SpriteSheet, background: CardBackground):
    # Using the dimensions (69, 93) from your previous frame_0 logic
    row =0
    col = 0
    if background == CardBackground.WHITE_FRONT:
        row = 0
        col = 1
    return sheet.get_image(row, col, 70, 94, 0.7, (255, 255, 255),1,0)

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
    return sheet.get_image(row,col,70,94,0.7,(255,255,255),1,1)
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
