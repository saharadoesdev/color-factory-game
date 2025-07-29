import pygame

class Bin(pygame.sprite.Sprite):
    def __init__(self, x, y, image, color):
        super().__init__()
        self.normal_image = image['normal']
        self.glow_image = image['glow']
        self.image = self.normal_image  # self.image is for current image
        self.color = color  # `color` is string in all-capital letters, ex. "RED"
        self.rect = self.image.get_rect(topleft=(x, y))   # For collision checking
        self.activation_zone = self.rect.inflate(-10,40)

    def activate(self):
        self.image = self.glow_image

    def deactivate(self):
        self.image = self.normal_image