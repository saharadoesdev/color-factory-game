import pygame

class Bin():
    def __init__(self, x, y, image, color):
        super().__init__()
        self.x = x
        self.y = y
        self.image = image
        self.color = color  # `color` is string in all-capital letters, ex. "RED"