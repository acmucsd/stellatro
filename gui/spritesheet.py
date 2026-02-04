import pygame

class SpriteSheet():
	def __init__(self, image):
		self.sheet = image

	def get_image(self,row,col, width, height, scale, colour, xgap=0,ygap=0):
		x_pos = (col * width) + (col * xgap)
		y_pos = (row * height) + (row * ygap)
		image = pygame.Surface((width, height)).convert_alpha()
		image.blit(self.sheet, (0, 0), (x_pos, y_pos, width, height))
		image = pygame.transform.scale(image, (width * scale, height * scale))
		image.set_colorkey(colour)

		return image