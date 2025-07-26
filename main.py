import pygame
import random
from classes.player import Player
from classes.blob import Blob

MAX_MISSED_BLOBS = 3
missed_blobs = 0
game_state = "playing"  # The initial game state

def initialize_game():
    pygame.init()
    window_size = (800, 600)
    window = pygame.display.set_mode(window_size)
    pygame.display.set_caption('Falling Blob Game')
    return window

def load_assets():
    # background_image = pygame.image.load('assets/background.jpg')
    # background_image = pygame.transform.scale(background_image, (800, 600))
    background_image = None     # temporary

    player_image = pygame.image.load('assets/player_basket.png')
    player_image = pygame.transform.scale(player_image, (100, 100))

    red_image = pygame.image.load('assets/apple.png')
    red_image = pygame.transform.scale(red_image, (50, 50))

    yellow_image = pygame.image.load('assets/banana.png')
    yellow_image = pygame.transform.scale(yellow_image, (50, 50))

    blue_image = pygame.image.load('assets/orange.png')
    blue_image = pygame.transform.scale(blue_image, (50, 50))

    return background_image, player_image, [red_image, yellow_image, blue_image]

def spawn_blob(falling_blobs, blob_images, screen_width):
    x_position = random.randint(0, screen_width - 50)
    y_position = 0
    blob_image = random.choice(blob_images)
    # falling_blobs.append([x_position, y_position, blob_image])
    falling_blobs.append(Blob(x_position, y_position, blob_image, "test"))

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

def render_game(window, background_image, player_image, player_position, falling_blobs, score, font):
    # window.blit(background_image, (0, 0))
     # If there's no background image, fill with a solid color (added this)
    if background_image is None:
        window.fill((135, 206, 235))  # RGB for sky blue
    else:
        window.blit(background_image, (0, 0))

    window.blit(player_image, player_position)

    for blob in falling_blobs:
        # window.blit(blob[2], (blob[0], blob[1]))
        window.blit(blob.image, (blob.x, blob.y))

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

def handle_events(game_state):
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

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False, restart, move_left, move_right

    keys = pygame.key.get_pressed()
    if game_state == "playing":
        move_left = keys[pygame.K_LEFT]
        move_right = keys[pygame.K_RIGHT]
    elif game_state == "game_over" and keys[pygame.K_r]:
        restart = True

    return True, restart, move_left, move_right

def main():
    global game_state, missed_blobs    # added these

    window = initialize_game()
    background_image, player_image, blob_images = load_assets()

    # player_position = [350, 500]
    # player_speed = 5
    player = Player(350, 500)
    screen_width = 800
    screen_height = 600
    falling_blobs = []
    # blob_speed = 5
    spawn_timer = 0
    score = 0

    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    running = True
    while running:
        running, restart, move_left, move_right = handle_events(game_state)

        if game_state == "playing":
          # Update player position
        #   player_position = update_player_position(player_position, move_left, move_right, player_speed, screen_width)

        #   player_position[0] += (move_right - move_left) * player.speed
        #   player_position[0] = max(0, min(700, player_position[0]))
            player.move(move_left, move_right)

            # Spawn blobs periodically
            spawn_timer += 1
            if spawn_timer > 30:
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
            render_game(window, background_image, player_image, [player.x,player.y], falling_blobs, score, font)

        elif game_state == "game_over":
            render_game_over(window, font)

            # Handle restart
            if restart:
                falling_blobs = []
                missed_blobs = 0
                score = 0
                game_state = "playing"

        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()