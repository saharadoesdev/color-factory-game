import pygame
import math
from settings import BONUS_DURATION

class Bin(pygame.sprite.Sprite):
    def __init__(self, x, y, image, color):
        super().__init__()
        self.normal_image = image['normal']
        self.glow_image = image['glow']
        self.image = self.normal_image
        self.color = color  # `color` is string in all-capital letters, ex. "RED"
        self.rect = self.image.get_rect(topleft=(x, y))   # For collision checking
        self.activation_zone = self.rect.inflate(-10,40)
        
        self.bonus_duration = BONUS_DURATION # 10 seconds in milliseconds
        self.bonus_end_time = 0
        self.has_bonus = False
        self.is_active = False
        self.pulse_speed = 0
        self.min_alpha = 0
    
    def update(self):
        if self.has_bonus and pygame.time.get_ticks() > self.bonus_end_time:
            self.has_bonus = False

        if self.is_active and self.has_bonus:   # Fastest pulse has bonus and player nearby
            # pulse_speed = 0.015
            pulse_alpha = 128 + math.sin(pygame.time.get_ticks() * 0.015) * 127
            self.glow_image.set_alpha(pulse_alpha)        
        elif self.has_bonus:    # Slower pulse for when player far away
            # pulse_speed = 0.005
            # self.pulse(pulse_speed)
            pulse_alpha = 191 + math.sin(pygame.time.get_ticks() * 0.005) * 64
            self.glow_image.set_alpha(pulse_alpha)      
        elif self.is_active:    # Static glow (no pulse) when player nearby but no bonus
            self.glow_image.set_alpha(255)
        # Else, bin is normal

    def start_bonus(self):
        """Activates the bonus state and starts the timer."""
        self.has_bonus = True
        self.bonus_end_time = pygame.time.get_ticks() + self.bonus_duration