import pygame

class CardHandContainer(pygame.sprite.Group):
    def __init__(self, startPos : pygame.math.Vector2, spacing : float):
        super().__init__()
        self.spacing = spacing
        self.startPos = startPos
    #already implemented add
    
    def update(self):
        first_sprite = self.sprites()[0]
        card_w = first_sprite.rect.width
        total_width = (len(self) * card_w) + ((len(self) - 1) * self.spacing)
        start_x = self.startPos.x - (total_width / 2)
        for i, sprite in enumerate(self):
            current_x = start_x + (i * (card_w + self.spacing)) + (card_w / 2)
            target_y = self.startPos.y
            if getattr(sprite, 'selected',False):
                target_y -= 30
            sprite.rect.center = (current_x, target_y)
    def draw(self, screen):
        return super().draw(screen)
        