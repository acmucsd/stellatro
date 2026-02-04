import pygame

class Joker(pygame.sprite.Sprite):
    def __init__(self, joker_image,x=0, y=0):
        super().__init__()
        self.image = joker_image
        self.rect = self.image.get_rect(topleft=(x, y))