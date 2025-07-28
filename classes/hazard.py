import pygame

class Hazard():
    def __init__(self, x, y, image):
        # super().__init__()
        self.x = x
        self.y = y
        self.speed = 4
        self.image = image       

    def move(self):
        """Hazard only moves down."""
        self.y += self.speed