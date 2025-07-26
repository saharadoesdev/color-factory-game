# blob.py - Will be for fruit objects temporarily until I replace them

import pygame

class Blob():
    def __init__(self, x, y, image, color):
        # super().__init__()
        self.x = x
        self.y = y
        self.speed = 4
        self.image = image       
        self.color = color 

    def move(self):
        """Handles left, right movement and jumping."""
        self.y += self.speed