import pygame

class Button(pygame.sprite.Sprite):
    def __init__(self, text, pos, color, hover_color, size=(150, 50), font_size=16):
        super().__init__()
        self.text = text
        self.pos = pos
        self.size = size
        self.color = color
        self.hover_color = hover_color
        self.border_radius = 10
        
        # Setup Font
        self.font = pygame.font.SysFont("Arial", font_size)
        self.font.set_bold(True)
        self.text_surf = self.font.render(self.text, True, (255, 255, 255)) # White text
        self.text_rect = self.text_surf.get_rect()

        # Create the initial image (Surface)
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=pos)
        
        # Initial draw
        self.create_button_surface(self.color)

    def create_button_surface(self, color):
        """Redraws the button background and re-blits the text."""
        self.image.fill((0, 0, 0, 0)) # Clear with transparency
        
        # Draw the rounded rectangle
        pygame.draw.rect(
            self.image, 
            color, 
            self.image.get_rect(),
            border_radius=self.border_radius
        )
        
        # Center and blit text
        self.text_rect.center = (self.size[0] // 2, self.size[1] // 2)
        self.image.blit(self.text_surf, self.text_rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def update(self, mouse_pos):
        """Check for hover and swap colors."""
        if self.rect.collidepoint(mouse_pos):
            self.create_button_surface(self.hover_color)
        else:
            self.create_button_surface(self.color)