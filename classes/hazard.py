import pygame
import random
from settings import HAZARD_SPEED, HAZARD_DRIFT

class Hazard(pygame.sprite.Sprite):
    def __init__(self, x, y, image, speed):
        super().__init__()
        self.speed = speed   # HAZARD_SPEED
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))   # For collision checking  
        self.pos_x = float(x)
        self.speed_x = random.uniform(-HAZARD_DRIFT, HAZARD_DRIFT)    # Drift speed   

    def move(self):
        """Hazard only moves down."""
        self.rect.y += self.speed
        self.pos_x += self.speed_x  # rect.x can only be whole numbers, speed could be float
        self.rect.x = int(self.pos_x)