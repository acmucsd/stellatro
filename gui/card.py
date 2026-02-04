from enum import Enum
from rank import Rank
from suit import Suit
import pygame


class CardBackground(Enum):
    RED = "red"
    BLUE = "blue"
    YELLOW = "yellow"
    BLACK="black"
    WHITE_FRONT="white_front"


class Card(pygame.sprite.Sprite):
    def __init__(self, card_background, card_rank, card_suit, front_image, back_image, x=0, y=0):
        super().__init__()
        self.card_background = card_background
        self.card_rank = card_rank
        self.card_suit = card_suit
        
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
    
    def update():
        pass

        