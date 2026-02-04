import pygame
from card import Card, CardBackground
from spritesheet import SpriteSheet
from rank import Rank
from suit import Suit


def getCardBackgroundImage(sheet: SpriteSheet, background: CardBackground):
    # Using the dimensions (69, 93) from your previous frame_0 logic
    row =0
    col = 0
    if background == CardBackground.WHITE_FRONT:
        row = 0
        col = 1
    return sheet.get_image(row, col, 70, 94, 2, (0, 0, 0),1,0)

def getCardImage(sheet : SpriteSheet, rank : Rank , suit : Suit):
    if suit == Suit.HEART:
        row = 0
    elif suit == Suit.CLUB:
        row = 1
    elif suit == Suit.DIAMOND:
        row = 2
    elif suit == Suit.SPADE:
        row = 3
    col = rank.value - 2
    return sheet.get_image(row,col,70,94,2,(0,0,0),1,1)



class Deck:
    def __init__(self,playing_cards_sheet : SpriteSheet, background_sheet : SpriteSheet):
        self.cards = pygame.sprite.Group()
        self.sheet = playing_cards_sheet
        self.bg_sheet = background_sheet

    def add_card(self, rank: Rank, suit: Suit, background: CardBackground, x=0, y=0):
        back_image = getCardBackgroundImage(self.bg_sheet,CardBackground.WHITE_FRONT)
        front_image = getCardImage(self.sheet, rank, suit)
        back_base = getCardBackgroundImage(self.bg_sheet, CardBackground.RED)
        new_card = Card(background, rank, suit, front_image,back_image, x, y)
        new_card.face_down_image = back_base
        self.cards.add(new_card)
     