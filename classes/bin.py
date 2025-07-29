import pygame

class Bin(pygame.sprite.Sprite):
    def __init__(self, x, y, image, color):
        super().__init__()
        self.image = image
        self.color = color  # `color` is string in all-capital letters, ex. "RED"
        self.rect = self.image.get_rect(topleft=(x, y))   # For collision checking