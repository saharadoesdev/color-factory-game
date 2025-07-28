import pygame
import random
from classes.player import Player, MIX_RULES
from classes.blob import Blob
from classes.bin import Bin

MAX_MISSED_BLOBS = 3
missed_blobs = 0
game_state = "playing"  # The initial game state

COLORS = {
    "RED": (255, 0, 0),
    "YELLOW": (255, 255, 0),
    "BLUE": (0, 0, 255),
    "ORANGE": (255, 165, 0),
    "GREEN": (0, 255, 0),
    "PURPLE": (128, 0, 128),
    # "WHITE": (255, 255, 255)
}

SPAWNABLE_COLORS = ["RED", "BLUE", "YELLOW"]

def initialize_game():
    pygame.init()
    window_size = (800, 600)
    window = pygame.display.set_mode(window_size)
    pygame.display.set_caption('Falling Blob Game')
    return window

def load_assets():
    background_image = pygame.image.load('assets/background.jpg')
    background_image = pygame.transform.scale(background_image, (800, 489))
    # background_image = None     # temporary

    player_image = pygame.image.load('assets/player_basket.png')
    player_image = pygame.transform.scale(player_image, (100, 100))

    red_image = pygame.image.load('assets/apple.png')
    red_image = pygame.transform.scale(red_image, (50, 50))

    yellow_image = pygame.image.load('assets/banana.png')
    yellow_image = pygame.transform.scale(yellow_image, (50, 50))

    blue_image = pygame.image.load('assets/orange.png')
    blue_image = pygame.transform.scale(blue_image, (50, 50))

    blob_images = {
        "RED": red_image,
        "YELLOW": yellow_image,
        "BLUE": blue_image
    }

    # Bins will temporarily use fruit images until I replace them
    red_bin_image = pygame.image.load('assets/apple.png')
    red_bin_image = pygame.transform.scale(red_bin_image, (100, 100))

    yellow_bin_image = pygame.image.load('assets/banana.png')
    yellow_bin_image = pygame.transform.scale(yellow_bin_image, (100, 100))

    blue_bin_image = pygame.image.load('assets/orange.png')
    blue_bin_image = pygame.transform.scale(blue_bin_image, (100, 100))

    bin_images = {
        "RED": red_bin_image,
        "YELLOW": yellow_bin_image,
        "BLUE": blue_bin_image
    }

    # return background_image, player_image, [red_image, yellow_image, blue_image]
    return background_image, player_image, blob_images, bin_images

def spawn_blob(falling_blobs, blob_images, screen_width):
    x_position = random.randint(0, screen_width - 50)
    y_position = 0
    color_to_spawn = random.choice(SPAWNABLE_COLORS)    # Choose blob color randomly
    # blob_image = random.choice(blob_images)
    # falling_blobs.append([x_position, y_position, blob_image])
    falling_blobs.append(Blob(x_position, y_position, blob_images[color_to_spawn], color_to_spawn)) # Create and spawn new blob

def move_blobs(falling_blobs, window_height):
    """
    Moves blobs downward and counts missed blobs.

    Parameters:
    - falling_blobs: List of blobs currently falling.
    - blob_speed: The speed of the falling blobs.
    - window_height: The height of the game window.

    Returns:
    - missed_blobs: The number of blobs that fell off the screen.
    """
    missed_blobs = 0
    for blob in falling_blobs:
        # blob[1] += blob_speed  # Move the blob down
        # if blob[1] > window_height:  # Check if the blob is off-screen
        #     missed_blobs += 1  # Increment the missed blob counter
        blob.move()
        if blob.y > window_height:  # Check if the blob is off-screen
             missed_blobs += 1  # Increment the missed blob counter
    falling_blobs[:] = [blob for blob in falling_blobs if blob.y <= window_height]  # Remove off-screen blobs
    return missed_blobs

def check_collision(player_position, blob_position):
    basket_x, basket_y = player_position
    blob_x, blob_y = blob_position

    basket_width = 100
    basket_height = 100
    blob_width = 50
    blob_height = 50

    if (blob_x < basket_x + basket_width and
        blob_x + blob_width > basket_x and
        blob_y < basket_y + basket_height and
        blob_y + blob_height > basket_y):
        return True
    return False

def render_score(window, score, font):
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    window.blit(score_text, (10, 10))

def render_game(window, background_image, player, falling_blobs, bins, score, font):
    # window.blit(background_image, (0, 0))
     # If there's no background image, fill with a solid color (added this)
    if background_image is None:
        window.fill((135, 206, 235))  # RGB for sky blue
    else:
        window.fill((0, 43, 34))    # Fill lower area with darkest blue-green from background
        window.blit(background_image, (0, 0))

    window.blit(player.image, (player.x, player.y))

    # Display indicator dot for currently held color
    if player.held_color is not None:
        indicator_pos = (player.x, player.y) # calculate indicator dot's position
    # Look up the RGB tuple from the COLORS dictionary
        color_to_draw = COLORS[player.held_color]
    
    # Use the retrieved tuple to draw the circle
        pygame.draw.circle(window, color_to_draw, indicator_pos, 15)

    for blob in falling_blobs:
        # window.blit(blob[2], (blob[0], blob[1]))
        window.blit(blob.image, (blob.x, blob.y))

    for bin in bins:
        window.blit(bin.image, (bin.x, bin.y))

    render_score(window, score, font)
    pygame.display.flip()

def render_game_over(window, font):
    """
    Displays the game-over screen.

    Parameters:
    - window: The game window.
    - font: The font object for rendering text.
    """
    game_over_text = font.render("Game Over", True, (255, 0, 0))  # Red text
    restart_text = font.render("Press R to Restart", True, (255, 255, 255))  # White text

    # Center the text on the screen
    window_width, window_height = window.get_size()
    window.blit(game_over_text, (window_width // 2 - game_over_text.get_width() // 2, window_height // 2 - 50))
    window.blit(restart_text, (window_width // 2 - restart_text.get_width() // 2, window_height // 2 + 10))
    pygame.display.flip()

def handle_events(game_state, bins):
    """
    Handles game events, including quitting and restarting.

    Parameters:
    - game_state: The current state of the game.

    Returns:
    - running: Whether the game should continue running.
    - restart: Whether the game should restart.
    - move_left: Whether the player is moving left.
    - move_right: Whether the player is moving right.
    """
    move_left = move_right = restart = False
    clicked_bin_color = None

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False, restart, move_left, move_right, clicked_bin_color
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Check for left mouse click
            for bin in bins:
                if bin.rect.collidepoint(event.pos):
                    clicked_bin_color = bin.color
                    break   # stop checking once clicked bin is found

    keys = pygame.key.get_pressed()
    if game_state == "playing":
        move_left = keys[pygame.K_LEFT]
        move_right = keys[pygame.K_RIGHT]
    elif game_state == "game_over" and keys[pygame.K_r]:
        restart = True

    return True, restart, move_left, move_right, clicked_bin_color

def main():
    global game_state, missed_blobs    # added these

    window = initialize_game()
    background_image, player_image, blob_images, bin_images = load_assets()

    # player_position = [350, 500]
    # player_speed = 5
    player = Player(350, 388, player_image)   # player is 100x100, position marks top left, so subtract 50 from desired center
    screen_width = 800
    screen_height = 600
    falling_blobs = []
    # blob_speed = 5
    spawn_timer = 0
    score = 0

    # Create bins
    red_bin = Bin(50, 500, bin_images["RED"], "RED")    # width is from 50 - 150
    yellow_bin = Bin(350, 500, bin_images["YELLOW"], "YELLOW")  # 350 - 450
    blue_bin = Bin(650, 500, bin_images["BLUE"], "BLUE")   # 650 - 750
    bins = [red_bin, yellow_bin, blue_bin]

    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    running = True
    while running:
        running, restart, move_left, move_right, clicked_bin_color = handle_events(game_state, bins)

        if game_state == "playing":
          # Update player position
        #   player_position = update_player_position(player_position, move_left, move_right, player_speed, screen_width)

        #   player_position[0] += (move_right - move_left) * player.speed
        #   player_position[0] = max(0, min(700, player_position[0]))
            player.move(move_left, move_right)

            if clicked_bin_color is not None:
                if player.held_color is None:
                    print("No color held!")
                elif player.held_color == clicked_bin_color or player.held_color in MIX_RULES[clicked_bin_color].values():
                    # Drop color in matching bin or parent primary color bin (ex., purple can go in red or blue)
                    print("Correct!")
                else:
                    print("Incorrect!")
                player.update_held_color(None)


            # Spawn blobs periodically
            spawn_timer += 1
            if spawn_timer > 50:    # Originally 30
              spawn_blob(falling_blobs, blob_images, screen_width)
              spawn_timer = 0

            # Move blobs and check for game-over condition
            # missed_blobs += move_blobs(falling_blobs, blob_speed, screen_height)
            missed_blobs += move_blobs(falling_blobs, screen_height)
            if missed_blobs >= MAX_MISSED_BLOBS:
                game_state = "game_over"

            # Check for collisions
            for blob in falling_blobs[:]:
                if check_collision([player.x,player.y], [blob.x, blob.y]):
                    falling_blobs.remove(blob)
                    player.update_held_color(blob.color)
                    score += 1

            # Render the game
            render_game(window, background_image, player, falling_blobs, bins, score, font)

        elif game_state == "game_over":
            render_game_over(window, font)

            # Handle restart
            if restart:
                falling_blobs = []
                missed_blobs = 0
                score = 0
                player.update_held_color(None)
                game_state = "playing"

        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()