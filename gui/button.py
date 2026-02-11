import pygame

class Button(pygame.sprite.Sprite):
    def __init__(self, text, color, pos, size=(150, 50), font_size=16):
        super().__init__()
        self.text = text
        self.color = color
        
        # 1. Create the button surface and rect
        self.image = pygame.Surface(size)
        self.image.fill(self.color)
        self.rect = self.image.get_rect(center=pos)
        
        # 2. Render the text
        self.font = pygame.font.SysFont("Arial", font_size)
        self.text_surf = self.font.render(self.text, True, (255, 255, 255)) # White text
        self.text_rect = self.text_surf.get_rect(center=(size[0]/2, size[1]/2))
        
        # 3. Blit text onto button background
        self.image.blit(self.text_surf, self.text_rect)

    def is_clicked(self, mouse_pos):
        """Check if the button was clicked."""
        return self.rect.collidepoint(mouse_pos)

    def draw(self, screen):
        """Standard draw method."""
        screen.blit(self.image, self.rect)