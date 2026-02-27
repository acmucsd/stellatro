import pygame
from pygame.font import Font
class Text():
    def __init__(self, position, initial_text, font_size, text_color,  textFont : pygame.font.Font, antialias = True):
        self.text = initial_text
        self.font_size = font_size
        self.text_color = text_color
        self.antialias = antialias
        self.position = position
        self.font = textFont
        
        self.text_surface = Font.render(self.font, self.text, self.antialias, self.text_color)
    def updateText(self, newText):
        self.text = newText
        print(self.text)
        self.text_surface = Font.render(self.font, self.text, self.antialias, self.text_color)
    def draw(self, screen : pygame.surface.Surface):
        screen.blit(self.text_surface, self.position)
        