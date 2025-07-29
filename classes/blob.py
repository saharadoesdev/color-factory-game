# blob.py

import pygame
import random
from settings import BLOB_SPEED, BLOB_DRIFT

class Blob(pygame.sprite.Sprite):
    def __init__(self, x, y, image, color, speed):
        super().__init__()
        self.speed = speed + random.uniform(-0.5, 0.5)  #BLOB_SPEED
        # print(self.speed)
        self.image = image       
        self.color = color 
        self.rect = self.image.get_rect(topleft=(x, y))   # For collision checking
        self.pos_x = float(x)
        self.pos_y = float(y)
        self.speed_x = random.uniform(-BLOB_DRIFT, BLOB_DRIFT)    # Drift speed

    def move(self):
        """Handles blob moving down."""
        self.pos_y += self.speed  # rect.y can only be whole numbers, speed could be float
        self.rect.y = int(self.pos_y)
        # self.rect.y += self.speed
        self.pos_x += self.speed_x  # rect.x can only be whole numbers, speed could be float
        self.rect.x = int(self.pos_x)