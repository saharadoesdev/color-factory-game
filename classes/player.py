import pygame

class Player():
    def __init__(self, x, y, image):
        # super().__init__()
        self.x = x
        self.y = y
        self.speed = 8
        # player_image = pygame.image.load('assets/player_basket.png')    # Load original image
        # self.image = pygame.transform.scale(player_image, (100, 100))   # Scale image
        self.image = image
        self.held_color = None
        # self.rect = self.image.get_rect(topleft=(x, y))   # I think i can use this?? is it just when it's a sprite?
        # self.vel_y = 0  # Vertical velocity for jumping
        # self.on_ground = False  # Track if player is on a surface

    def move(self, move_left, move_right):  # or just keys
        """Handles left, right movement and jumping."""
        # if keys[pygame.K_LEFT]:
        #     # self.rect.x -= PLAYER_SETTINGS["speed"]
        #     self.rect.x -= self.speed
        # if keys[pygame.K_RIGHT]:
        #     # self.rect.x += PLAYER_SETTINGS["speed"]
        #     self.rect.x += self.speed

        # if move_left:
        #     self.rect.x -= self.speed
        # if move_right:
        #     self.rect.x += self.speed

        self.x += (move_right - move_left) * self.speed
        self.x = max(0, min(700, self.x))

        # Prevent player from moving beyond the left boundary - i think i can use this??
        # if self.rect.left < 0:
        #     self.rect.left = 0

        # Righthand boundary value - i think i can use this?? (bottom one)
        # # if self.rect.right > SETTINGS["WIDTH"] + 400:  
        # #     self.rect.right = SETTINGS["WIDTH"] + 400
        # if self.rect.right > 800 + 400:  
        #     self.rect.right = 800 + 400

    def update_held_color(self, color):
        # if held_color == "red" and color == "blue":   # For later use when mixing colors
        #     self.held_color = "purple"    # Actually I'll use a dictionary instead !!
        # else: # held_color == None
        #     self.held_color = color

        self.held_color = color
        # print(self.held_color)    # for testing