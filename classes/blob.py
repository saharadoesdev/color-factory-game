# blob.py

import pygame

class Blob(pygame.sprite.Sprite):
    def __init__(self, x, y, image, color):
        super().__init__()
        self.speed = 4
        self.image = image       
        self.color = color 
        self.rect = self.image.get_rect(topleft=(x, y))   # For collision checking

    def move(self):
        """Handles blob moving down."""
        self.rect.y += self.speed