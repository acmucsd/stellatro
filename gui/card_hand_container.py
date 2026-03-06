
import pygame
from card import Card

class CardHandContainer(pygame.sprite.Group):
    SELECTED_OFFSET = -30
    def __init__(self, startPos : pygame.math.Vector2, spacing : float):
        # Initialize the group first
        super().__init__()
        self.spacing = spacing
        self.startPos = startPos
    
    def add(self, *sprites):
        """Adds sprites and calculates their initial position in the hand."""
        for sprite in sprites:
            super().add(sprite)
        
    
    def update(self, delta):
        sprites = self.sprites()
        if not sprites:
            return

        # Use the first sprite's original width as the standard for this container.
        # This prevents layout issues when sprites are rotated (e.g. Joker shake)
        # and their bounding box changes.
        first_sprite = sprites[0]
        if hasattr(first_sprite, 'original_image'): # Joker
            card_w = first_sprite.original_image.get_width()
        else: # Card or other sprite
            card_w = first_sprite.rect.width
        
        # Calculate the total width of the hand including spacing
        # Total width = (all cards) + (all gaps between them)
        total_width = (len(sprites) * card_w) + ((len(sprites) - 1) * self.spacing)
        
        # Calculate the starting X-coordinate so the hand is centered on startPos.x
        start_x = self.startPos.x - (total_width / 2)

        for i, sprite in enumerate(sprites):
            # Calculate the horizontal center for the i-th card
            # (Start) + (previous cards and gaps) + (half of current card width)
            current_x = start_x + (i * (card_w + self.spacing)) + (card_w / 2)
            
            target_y = self.startPos.y
            card: Card = sprite
            
            # Apply vertical offset if the card is selected
            if card.selected:
                target_y += self.SELECTED_OFFSET
            
            # Smoothly transition to the calculated position
            card.target_pos = pygame.math.Vector2(current_x, target_y)
            card.update(delta)
    
    def draw(self, screen):
        return super().draw(screen)
        