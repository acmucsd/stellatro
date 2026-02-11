import os
from rank import Rank
from suit import Suit
from card import Card, CardBackground
from spritesheet import SpriteSheet


GUI_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(GUI_DIR,"../assets")

def get_assets_path(asset_file_name):
    return os.path.join(ASSETS_DIR,asset_file_name)

def instantiate_card(bg_sheet, sheet,rank: Rank, suit: Suit, background: CardBackground, x=0, y=0):
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
    return sheet.get_image(row, col, 70, 94, 1, (0, 0, 0),1,0)

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
    return sheet.get_image(row,col,70,94,1,(0,0,0),1,1)