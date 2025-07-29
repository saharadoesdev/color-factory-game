import pygame
from settings import MIX_RULES, PLAYER_SPEED, PLAYER_ANIMATION_SPEED, PLAYER_STUN_DURATION

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, images):
        super().__init__()
        self.speed = PLAYER_SPEED
        self.images = images
        self.held_color = None
        self.is_stunned = False
        self.stun_end_time = 0

        # Setup for animations
        self.action = 'idle'
        self.current_frame = 0
        self.image = images[self.action][self.current_frame]
        self.last_update_time = pygame.time.get_ticks()
        self.animation_speed = PLAYER_ANIMATION_SPEED   # ms per frame

        self.rect = self.image.get_rect(topleft=(x, y))   # For collision checking

    def move(self, move_left, move_right):
        """Handles left and right movement."""
        if self.is_stunned:
            if pygame.time.get_ticks() > self.stun_end_time:    # Check if stun time is over
                self.is_stunned = False
            else:   # Stunned, so can't move
                return
        
        new_action = 'idle'
        if move_left and not move_right:    # If both left and right pressed together, stay idle
            self.rect.x -= self.speed
            new_action = 'left'
        elif not move_left and move_right:
            self.rect.x += self.speed
            new_action = 'right'

        self.rect.x = max(5, min(738, self.rect.x))   # Prevent player from moving beyond screen edges

        if self.action != new_action:
            self.action = new_action

        self.animate()

    def animate(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update_time > self.animation_speed:
            self.last_update_time = current_time
            self.current_frame = (self.current_frame + 1) % 6   # Each animation is 6 frames
            self.image = self.images[self.action][self.current_frame]

    def update_held_color(self, new_color):
        """Returns True if color changes updates to a non-None value, False otherwise."""
        if new_color == None:   # Clear held color
            self.held_color = None
        elif self.held_color == None:
            self.held_color = new_color
            return True
        elif self.held_color in MIX_RULES and new_color in MIX_RULES[self.held_color]:  # Mix colors based on MIX_RULES
            self.held_color = MIX_RULES[self.held_color][new_color]
            return True
        # If player catches the color they're already holding, or an impossible mix, nothing happens
        return False

    def get_stunned(self):   # 1.2 seconds
        self.is_stunned = True
        self.stun_end_time = pygame.time.get_ticks() + PLAYER_STUN_DURATION