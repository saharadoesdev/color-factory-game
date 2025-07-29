import pygame

class Hazard(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.speed = 4
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))   # For collision checking     

    def move(self):
        """Hazard only moves down."""
        self.rect.y += self.speed