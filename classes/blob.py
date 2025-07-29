# blob.py

import pygame
import random

class Blob(pygame.sprite.Sprite):
    def __init__(self, x, y, image, color):
        super().__init__()
        self.speed = 4
        self.image = image       
        self.color = color 
        self.rect = self.image.get_rect(topleft=(x, y))   # For collision checking
        self.pos_x = float(x)
        self.speed_x = random.uniform(-0.5, 0.5)

    def move(self):
        """Handles blob moving down."""
        self.rect.y += self.speed
        self.pos_x += self.speed_x
        self.rect.x = int(self.pos_x)