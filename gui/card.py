from enum import Enum
from rank import Rank
from suit import Suit
from typing import Set
import pygame


class CardBackground(Enum):
    RED = "red"
    BLUE = "blue"
    YELLOW = "yellow"
    BLACK="black"
    WHITE_FRONT="white_front"


def rank_to_score(rank: int) -> int:
    if 2 <= rank <= 10:
        return rank
    if 11 <= rank <= 13:
        return 10
    if rank == 14:
        return 11
    raise ValueError(f"Invalid card rank: {rank}")


class Card(pygame.sprite.Sprite):
    rank : int
    suits : Set[Suit]
    scored : bool = False
    num_triggers : int
    selected : bool = False
    
    def __init__(self, card_background, rank, suit, front_image, back_image, x=0, y=0):
        super().__init__()
        self.card_background = card_background
        self.rank = rank
        self.suits = {suit}
        self.scored = False
        self.num_triggers = 1
        self.selected = False
        
        # Store both versions of the "Final" image
        self.face_up_image = back_image.copy()
        front_rect = front_image.get_rect(center=self.face_up_image.get_rect().center)
        self.face_up_image.blit(front_image, front_rect)
        
        # We'll assign the actual "Back" image later via the flip setup
        self.face_down_image = None 
        
        # State tracking
        self.is_flipped = False # False = Face Up, True = Face Down
        
        self.image = self.face_up_image
        self.rect = self.image.get_rect(topleft=(x, y))
    def flip(self):
        """Toggles the card between face-up and face-down."""
        if self.face_down_image is None:
            print("Warning: Face down image not set for this card.")
            return
            
        self.is_flipped = not self.is_flipped
        
        # Update the active image based on state
        self.image = self.face_down_image if self.is_flipped else self.face_up_image
        
        # Re-center the rect in case images are slightly different sizes
        old_center = self.rect.center
        self.rect = self.image.get_rect(center=old_center)
    
    def update(self):
        pass

        
