import pygame
import random

MAX_MISSED_FRUITS = 3
missed_fruits = 0
game_state = "playing"  # The initial game state

def initialize_game():
    pygame.init()
    window_size = (800, 600)
    window = pygame.display.set_mode(window_size)
    pygame.display.set_caption('Falling Fruit Game')
    return window

def load_assets():
    # background_image = pygame.image.load('pygame/images/background.png')
    # background_image = pygame.transform.scale(background_image, (800, 600))
    background_image = None     # temporary

    # player_image = pygame.image.load('pygame/images/player_basket.png')
    player_image = pygame.image.load('assets/player_basket.png')
    player_image = pygame.transform.scale(player_image, (100, 100))

    # apple_image = pygame.image.load('pygame/images/apple.png')
    apple_image = pygame.image.load('assets/apple.png')
    apple_image = pygame.transform.scale(apple_image, (50, 50))

    # banana_image = pygame.image.load('pygame/images/banana.png')
    banana_image = pygame.image.load('assets/banana.png')
    banana_image = pygame.transform.scale(banana_image, (50, 50))

    # orange_image = pygame.image.load('pygame/images/orange.png')
    orange_image = pygame.image.load('assets/orange.png')
    orange_image = pygame.transform.scale(orange_image, (50, 50))

    return background_image, player_image, [apple_image, banana_image, orange_image]

def spawn_fruit(falling_fruits, fruit_images, screen_width):
    x_position = random.randint(0, screen_width - 50)
    y_position = 0
    fruit_image = random.choice(fruit_images)
    falling_fruits.append([x_position, y_position, fruit_image])

def move_fruits(falling_fruits, fruit_speed, window_height):
    """
    Moves fruits downward and counts missed fruits.

    Parameters:
    - falling_fruits: List of fruits currently falling.
    - fruit_speed: The speed of the falling fruits.
    - window_height: The height of the game window.

    Returns:
    - missed_fruits: The number of fruits that fell off the screen.
    """
    missed_fruits = 0
    for fruit in falling_fruits:
        fruit[1] += fruit_speed  # Move the fruit down
        if fruit[1] > window_height:  # Check if the fruit is off-screen
            missed_fruits += 1  # Increment the missed fruit counter
    falling_fruits[:] = [fruit for fruit in falling_fruits if fruit[1] <= window_height]  # Remove off-screen fruits
    return missed_fruits

def check_collision(player_position, fruit_position):
    basket_x, basket_y = player_position
    fruit_x, fruit_y = fruit_position

    basket_width = 100
    basket_height = 100
    fruit_width = 50
    fruit_height = 50

    if (fruit_x < basket_x + basket_width and
        fruit_x + fruit_width > basket_x and
        fruit_y < basket_y + basket_height and
        fruit_y + fruit_height > basket_y):
        return True
    return False

def render_score(window, score, font):
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    window.blit(score_text, (10, 10))

def render_game(window, background_image, player_image, player_position, falling_fruits, score, font):
    # window.blit(background_image, (0, 0))
     # If there's no background image, fill with a solid color (added this)
    if background_image is None:
        window.fill((135, 206, 235))  # RGB for sky blue
    else:
        window.blit(background_image, (0, 0))

    window.blit(player_image, player_position)

    for fruit in falling_fruits:
        window.blit(fruit[2], (fruit[0], fruit[1]))

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
    global game_state, missed_fruits    # added these

    window = initialize_game()
    background_image, player_image, fruit_images = load_assets()

    player_position = [350, 500]
    player_speed = 5
    screen_width = 800
    screen_height = 600
    falling_fruits = []
    fruit_speed = 5
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

          player_position[0] += (move_right - move_left) * player_speed
          player_position[0] = max(0, min(700, player_position[0]))

          # Spawn fruits periodically
          spawn_timer += 1
          if spawn_timer > 30:
              spawn_fruit(falling_fruits, fruit_images, screen_width)
              spawn_timer = 0

          # Move fruits and check for game-over condition
          missed_fruits += move_fruits(falling_fruits, fruit_speed, screen_height)
          if missed_fruits >= MAX_MISSED_FRUITS:
              game_state = "game_over"

          # Check for collisions
          for fruit in falling_fruits[:]:
              if check_collision(player_position, [fruit[0], fruit[1]]):
                  falling_fruits.remove(fruit)
                  score += 1

          # Render the game
          render_game(window, background_image, player_image, player_position, falling_fruits, score, font)

      elif game_state == "game_over":
          render_game_over(window, font)

          # Handle restart
          if restart:
              falling_fruits = []
              missed_fruits = 0
              score = 0
              game_state = "playing"

      clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()