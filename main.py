import pygame
import random
from classes.player import Player, MIX_RULES
from classes.blob import Blob
from classes.bin import Bin
from classes.hazard import Hazard

# MAX_MISSED_BLOBS = 3
# missed_blobs = 0
game_state = "start_menu"  # The initial game state

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
    pygame.mixer.init()
    window_size = (800, 600)
    window = pygame.display.set_mode(window_size)
    pygame.display.set_caption('Falling Blob Game')
    return window

def load_assets():
    background_image = pygame.image.load('assets/background.jpg')
    background_image = pygame.transform.scale(background_image, (800, 489))
    # background_image = None     # temporary

    start_menu_image = pygame.image.load('assets/start_screen.png')

    player_image = pygame.image.load('assets/robot_idle_5.png')
    player_image = pygame.transform.smoothscale(player_image, (57, 100))

    # Load blob images, which are also used for robot's color indicator, and add to dictionaries
    blob_images = {}
    indicator_images = {}
    for color in COLORS.keys():
        file_path = f"assets/blobs/{color.lower()}_blob.png"
        original_image = pygame.image.load(file_path)
        blob_images[color] = pygame.transform.smoothscale(original_image, (50, 50))
        indicator_images[color] = pygame.transform.smoothscale(original_image, (20, 20))

    # Bins will temporarily use blob images until I replace them
    # red_bin_image = pygame.image.load('assets/blobs/red_blob.png')
    # red_bin_image = pygame.transform.scale(red_bin_image, (100, 100))

    # yellow_bin_image = pygame.image.load('assets/blobs/yellow_blob.png')
    # yellow_bin_image = pygame.transform.scale(yellow_bin_image, (100, 100))

    # blue_bin_image = pygame.image.load('assets/blobs/blue_blob.png')
    # blue_bin_image = pygame.transform.scale(blue_bin_image, (100, 100))

    # orange_bin_image = pygame.image.load('assets/blobs/orange_blob.png')
    # orange_bin_image = pygame.transform.scale(orange_bin_image, (100, 100))

    # green_bin_image = pygame.image.load('assets/blobs/green_blob.png')
    # green_bin_image = pygame.transform.scale(green_bin_image, (100, 100))

    # purple_bin_image = pygame.image.load('assets/blobs/purple_blob.png')
    # purple_bin_image = pygame.transform.scale(purple_bin_image, (100, 100))

    # bin_images = {
    #     "RED": red_bin_image, "YELLOW": yellow_bin_image, "BLUE": blue_bin_image,
    #     "ORANGE": orange_bin_image, "GREEN": green_bin_image, "PURPLE": purple_bin_image
    # }

    # Load bin images and add to dictionary
    bin_images = {}
    for color in COLORS.keys():
        file_path = f"assets/bins/{color.lower()}_barrel.png"
        original_image = pygame.image.load(file_path)
        bin_images[color] = pygame.transform.smoothscale(original_image, (69, 100))

    # Hazard image (will probably add more later)
    wrench_image = pygame.image.load('assets/wrench.png')
    wrench_image = pygame.transform.smoothscale(wrench_image, (50, 50))

    # return background_image, player_image, [red_image, yellow_image, blue_image]
    return background_image, start_menu_image, player_image, blob_images, indicator_images, bin_images, wrench_image

def spawn_blob(falling_blobs, blob_images, hazard_image, screen_width):
    x_position = random.randint(0, screen_width - 50)
    y_position = 0
    if random.random() < 0.20:  # Adjust value - HAZARD_CHANCE
        falling_blobs.append(Hazard(x_position, y_position, hazard_image))
    else:   # Spawn blob
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
    # missed_blobs = 0      # Don't need this anymore, not tracking missed blobs
    for blob in falling_blobs:
        # blob[1] += blob_speed  # Move the blob down
        # if blob[1] > window_height:  # Check if the blob is off-screen
        #     missed_blobs += 1  # Increment the missed blob counter
        blob.move()
        # if blob.y > window_height:  # Check if the blob is off-screen
        #      missed_blobs += 1  # Increment the missed blob counter
    falling_blobs[:] = [blob for blob in falling_blobs if blob.y <= window_height]  # Remove off-screen blobs
    # return missed_blobs

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

def render_timer(window, time_left, font):
    timer_text = font.render(f"Timer: {time_left}s", True, (0, 0, 0))
    window.blit(timer_text, (650, 10))

def render_combo(window, combo_multiplier, font):
    combo_text = font.render(f"Combo: {combo_multiplier}x", True, (0, 0, 0))
    window.blit(combo_text, (325, 10))

def render_game(window, background_image, indicator_images, player, falling_blobs, bins, score, time_left, combo_multiplier, font):
    # window.blit(background_image, (0, 0))
     # If there's no background image, fill with a solid color (added this)
    if background_image is None:
        window.fill((135, 206, 235))  # RGB for sky blue
    else:
        window.fill((0, 43, 34))    # Fill lower area with darkest blue-green from background
        window.blit(background_image, (0, 0))

    window.blit(player.image, (player.x, player.y))

    # # Display indicator dot for currently held color
    # if player.held_color is not None:
    #     indicator_pos = (player.x + player.image.get_width() // 2, player.y) # calculate indicator dot's position
    # # Look up the RGB tuple from the COLORS dictionary
    #     color_to_draw = COLORS[player.held_color]
    # # Use the retrieved tuple to draw the circle
    #     pygame.draw.circle(window, color_to_draw, indicator_pos, 10)

    # Display indicator above robot for currently held color
    if player.held_color is not None:
        indicator_pos = (player.x + (player.image.get_width() // 2) - 10, player.y - 10) # calculate indicator dot's position
        window.blit(indicator_images[player.held_color], indicator_pos)

    for blob in falling_blobs:
        # window.blit(blob[2], (blob[0], blob[1]))
        window.blit(blob.image, (blob.x, blob.y))

    for bin in bins:
        window.blit(bin.image, (bin.x, bin.y))
        # Render an indicator image label on top of each bin
        bin_label_pos = (bin.x + (bin.image.get_width() // 2) - 8, bin.y + (bin.image.get_height() // 2) - 10)  # Center position
        window.blit(indicator_images[bin.color], bin_label_pos)

    render_score(window, score, font)
    render_timer(window, time_left, font)
    render_combo(window, combo_multiplier, font)
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

def render_start_menu(window, start_menu_image):
    window.blit(start_menu_image, (0, 0))
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
    move_left = move_right = restart = start_game = False
    clicked_bin_color = None

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False, start_game, restart, move_left, move_right, clicked_bin_color
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Check for left mouse click
            for bin in bins:
                if bin.rect.collidepoint(event.pos):
                    clicked_bin_color = bin.color
                    break   # stop checking once clicked bin is found

    keys = pygame.key.get_pressed()
    if game_state == "start_menu" and any(keys):
        start_game = True
    if game_state == "playing":
        move_left = keys[pygame.K_LEFT]
        move_right = keys[pygame.K_RIGHT]
    elif game_state == "game_over" and keys[pygame.K_r]:
        restart = True

    return True, start_game, restart, move_left, move_right, clicked_bin_color

def main():
    global game_state, missed_blobs    # added these

    window = initialize_game()
    background_image, start_menu_image, player_image, blob_images, indicator_images, bin_images, wrench_image = load_assets()

    # player_position = [350, 500]
    # player_speed = 5
    player = Player(400 - (player_image.get_width() // 2), 388, player_image)   # NOW PLAYER is 57 x 100, but this is dynamic to center the player! // player is 100x100, position marks top left, so subtract 50 from desired center
    screen_width = 800
    screen_height = 600
    falling_blobs = []
    # blob_speed = 5
    spawn_timer = 0
    score = 0
    combo_multiplier = 1

    # Create bins - each 69 wide, so space them out accordingly
    red_bin = Bin(55, 500, bin_images["RED"], "RED")    # width is from 50 - 150
    orange_bin = Bin(179, 500, bin_images["ORANGE"], "ORANGE")
    yellow_bin = Bin(303, 500, bin_images["YELLOW"], "YELLOW")  # 350 - 450
    green_bin = Bin(427, 500, bin_images["GREEN"], "GREEN")
    blue_bin = Bin(551, 500, bin_images["BLUE"], "BLUE")   # 650 - 750
    purple_bin = Bin(675, 500, bin_images["PURPLE"], "PURPLE")   # 650 - 750
    bins = [red_bin, orange_bin,yellow_bin, green_bin, blue_bin, purple_bin]

    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    
    # Set up timer
    # start_time = pygame.time.get_ticks()
    game_duration = 30000   # 30 seconds, make longer later

    # Start music on infinite loop
    pygame.mixer.music.load("assets/audio/background_music.wav")
    pygame.mixer.music.play(loops=-1)

    running = True
    while running:
        running, start_game, restart, move_left, move_right, clicked_bin_color = handle_events(game_state, bins)

        if game_state == "start_menu":
            render_start_menu(window, start_menu_image)
            if start_game:
                start_time = pygame.time.get_ticks()
                game_state = "playing"
        elif game_state == "playing":
            # Check timer
            elapsed_time = pygame.time.get_ticks() - start_time
            time_left = (game_duration - elapsed_time) // 1000
            # print(time_left)
        
            if time_left <= 0:
                game_state = "game_over"
                time_left = 0

          # Update player position
        #   player_position = update_player_position(player_position, move_left, move_right, player_speed, screen_width)

        #   player_position[0] += (move_right - move_left) * player.speed
        #   player_position[0] = max(0, min(700, player_position[0]))
            player.move(move_left, move_right)

            if clicked_bin_color is not None:
                # if player.held_color is None:     # Nothing needs to happen (for now?)
                #     print("No color held!")
                if player.held_color == clicked_bin_color:   # or player.held_color in MIX_RULES[clicked_bin_color].values():
                    # Drop color in matching bin // OLD: or parent primary color bin (ex., purple can go in red or blue)
                    # print("Correct!")
                    score += 10 * combo_multiplier
                    combo_multiplier = 5 if combo_multiplier == 5 else combo_multiplier + 1  # Max combo multiplier is 5x
                elif player.held_color is not None:   # If color dropped in wrong bin, reset combo
                    combo_multiplier = 1
                player.update_held_color(None)


            # Spawn blobs periodically
            spawn_timer += 1
            if spawn_timer > 50:    # Originally 30
              spawn_blob(falling_blobs, blob_images, wrench_image, screen_width)
              spawn_timer = 0

            # Move blobs and check for game-over condition
            # missed_blobs += move_blobs(falling_blobs, blob_speed, screen_height)
            # missed_blobs += move_blobs(falling_blobs, screen_height)
            # if missed_blobs >= MAX_MISSED_BLOBS:
            #     game_state = "game_over"

            move_blobs(falling_blobs, screen_height)

            # Check for collisions
            for blob in falling_blobs[:]:
                if check_collision([player.x,player.y], [blob.x, blob.y]):
                    falling_blobs.remove(blob)
                    if isinstance(blob, Blob):  # This will be more refined later probably haha
                        player.update_held_color(blob.color)
                    else:   # Hazard, so stun
                        player.get_stunned()
                        combo_multiplier = 1    # Reset combo
                    # score += 1

            # Render the game
            render_game(window, background_image, indicator_images, player, falling_blobs, bins, score, time_left, combo_multiplier, font)

        elif game_state == "game_over":
            render_game_over(window, font)

            # Handle restart
            if restart:
                falling_blobs = []
                # missed_blobs = 0
                score = 0
                player.update_held_color(None)
                combo_multiplier = 1
                start_time = pygame.time.get_ticks()    # Reset timer
                game_state = "playing"

        clock.tick(60)

    pygame.mixer.music.stop()
    pygame.quit()

if __name__ == "__main__":
    main()