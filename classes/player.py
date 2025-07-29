import pygame

MIX_RULES = {
    "RED": {"BLUE": "PURPLE", "YELLOW": "ORANGE"},
    "BLUE": {"RED": "PURPLE", "YELLOW": "GREEN"},
    "YELLOW": {"RED": "ORANGE", "BLUE": "GREEN"}
}

class Player():
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.speed = 8
        self.image = image
        self.held_color = None
        self.is_stunned = False
        self.stun_end_time = 0

    def move(self, move_left, move_right):
        """Handles left and right movement."""

        if self.is_stunned:
            if pygame.time.get_ticks() > self.stun_end_time:    # Check if stun time is over
                self.is_stunned = False
            else:   # Stunned, so can't move
                return
            
        # Move if left or right key pressed
        self.x += (move_right - move_left) * self.speed
        self.x = max(5, min(738, self.x))   # Prevent player from moving beyond screen edges

    def update_held_color(self, new_color):
        if new_color == None:   # Clear held color
            self.held_color = None
        elif self.held_color == None:
            self.held_color = new_color
        elif self.held_color in MIX_RULES and new_color in MIX_RULES[self.held_color]:  # Mix colors based on MIX_RULES
            self.held_color = MIX_RULES[self.held_color][new_color]
        # If player catches the color they're already holding, or an impossible mix, nothing happens

    def get_stunned(self, duration=1200):   # 1.2 seconds
        self.is_stunned = True
        self.stun_end_time = pygame.time.get_ticks() + duration