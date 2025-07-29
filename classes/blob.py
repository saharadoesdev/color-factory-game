# blob.py

import pygame

class Blob():
    def __init__(self, x, y, image, color):
        self.x = x
        self.y = y
        self.speed = 4
        self.image = image       
        self.color = color 

    def move(self):
        """Handles left, right movement and jumping."""
        self.y += self.speed