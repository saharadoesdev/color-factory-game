import pygame
import random
from classes.player import Player
from classes.blob import Blob
from classes.bin import Bin
from classes.hazard import Hazard
from settings import (
    WINDOW_WIDTH, WINDOW_HEIGHT, GAME_TITLE,
    COLORS, SPAWNABLE_COLORS, SPAWN_POSITIONS,
    GAME_DURATION, HAZARD_CHANCE,
    PRIMARY_SCORE, SECONDARY_SCORE, MAX_COMBO, BONUS_MULTIPLIER
)

def initialize_game():
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.set_volume(0.7)
    window_size = (800, 600)
    window = pygame.display.set_mode(window_size)
    pygame.display.set_caption(GAME_TITLE)
    return window

def load_assets():
    background_image = pygame.image.load('assets/background.jpg')
    background_image = pygame.transform.scale(background_image, (800, 489))

    start_menu_image = pygame.image.load('assets/start_screen.png')

    # Load player animations
    player_idle_frames = []
    for i in range(6):
        frame = pygame.image.load(f'assets/player/robot_idle_{i}.png') #.convert_alpha()
        frame = pygame.transform.smoothscale(frame, (57, 100))
        player_idle_frames.append(frame)

    player_left_frames = []
    for i in range(6):
        frame = pygame.image.load(f'assets/player/robot_left_{i}.png') #.convert_alpha()
        frame = pygame.transform.smoothscale(frame, (57, 99))
        player_left_frames.append(frame)

    # Right frames are just flipped versions of left
    player_right_frames = []
    for frame in player_left_frames:
        flipped_frame = pygame.transform.flip(frame, True, False)
        player_right_frames.append(flipped_frame)

    player_images = {'idle': player_idle_frames, 'left': player_left_frames, 'right': player_right_frames}

    # Load blob images, which are also used for robot's color indicator, and add to dictionaries
    blob_images = {}
    indicator_images = {}
    for color in COLORS.keys():
        file_path = f"assets/blobs/{color.lower()}_blob.png"
        original_image = pygame.image.load(file_path)
        blob_images[color] = pygame.transform.smoothscale(original_image, (50, 50))
        indicator_images[color] = pygame.transform.smoothscale(original_image, (20, 20))

    # Load bin images and add to dictionary
    bin_images = {}
    for color in COLORS.keys():
        bin_images[color] = {}    # Each color is a dictionary, holds normal and glow images

        file_path = f"assets/bins/{color.lower()}_barrel.png"
        original_image = pygame.image.load(file_path)
        bin_images[color]['normal'] = pygame.transform.smoothscale(original_image, (69, 100))

        file_path = f"assets/bins/{color.lower()}_barrel_glow.png"
        original_image = pygame.image.load(file_path)
        bin_images[color]['glow'] = pygame.transform.smoothscale(original_image, (69, 100))

    # Hazard image
    wrench_image = pygame.image.load('assets/wrench.png')
    wrench_image = pygame.transform.smoothscale(wrench_image, (50, 50))

    # Load pipes
    pipe_images = [pygame.image.load('assets/red_pipe.png'),
                   pygame.image.load('assets/yellow_pipe.png'),
                   pygame.image.load('assets/blue_pipe.png')]
    pipe_images = [pygame.transform.rotate(image, 90) for image in pipe_images]
    pipe_images = [pygame.transform.smoothscale(image, (125, 209)) for image in pipe_images]

    # Load sound effects into a dictionary
    sounds = {
        'hazard_hit': pygame.mixer.Sound("assets/audio/hazard_hit.aif"), # metal10.aif
        'clock_tick': pygame.mixer.Sound("assets/audio/clock_tick.wav"),
        'catch_blob': pygame.mixer.Sound("assets/audio/catch_blob.ogg"),   #pop1.ogg
        'correct_deposit': pygame.mixer.Sound("assets/audio/correct_deposit.wav"),   #coin01.aif (converted to wav)
        'wrong_deposit': pygame.mixer.Sound("assets/audio/wrong_deposit.wav")   #Downer01.aif (converted to wav)
    }
    sounds['hazard_hit'].set_volume(0.4)

    return background_image, start_menu_image, player_images, blob_images, indicator_images, bin_images, wrench_image, pipe_images, sounds

def spawn_object(falling_objects, blob_images, hazard_image, screen_width):
    # x_position = random.randint(0, screen_width - 50)
    # y_position = 0
    if random.random() < HAZARD_CHANCE:
        spawn_pos = random.choice(list(SPAWN_POSITIONS.values()))
        falling_objects.append(Hazard(spawn_pos[0], spawn_pos[1], hazard_image))
    else:   # Spawn blob
        color_to_spawn = random.choice(SPAWNABLE_COLORS)    # Choose blob color randomly
        spawn_pos = SPAWN_POSITIONS[color_to_spawn]
        falling_objects.append(Blob(spawn_pos[0], spawn_pos[1], blob_images[color_to_spawn], color_to_spawn)) # Create and spawn new blob

def move_blobs(falling_objects, window_height):
    """
    Moves objects (blobs, hazards) downward and removes missed objects.

    Parameters:
    - falling_objects: List of objects currently falling.
    - window_height: The height of the game window.
    """
    for object in falling_objects:
        object.move()
    falling_objects[:] = [object for object in falling_objects if object.rect.y <= window_height]  # Remove off-screen blobs

def render_ui(window, score, time_left, combo_multiplier, indicator_images, plus_sign, equals_sign, font):
    ui_bar = pygame.Surface((800, 50), pygame.SRCALPHA) 
    ui_bar.fill((0, 0, 0, 150)) # Transparent black
    window.blit(ui_bar, (0, 0))

    score_text = font.render(f"Score: {score}", True, (255,255,255))
    window.blit(score_text, (15, 15))

    combo_text = font.render(f"Combo: {combo_multiplier}x", True, (255,255,255))
    window.blit(combo_text, (540, 15))

    timer_text = font.render(f"Time: {time_left}", True, (255,255,255))
    window.blit(timer_text, (685, 15))

    # Display possible color combinations (like a recipe book):
    start_x = 175 
    start_y = 16
    # Orange
    window.blit(indicator_images["RED"], (start_x, start_y))
    window.blit(plus_sign, (start_x + 23, start_y - 4))
    window.blit(indicator_images["YELLOW"], (start_x + 41, start_y))
    window.blit(equals_sign, (start_x + 64, start_y - 4))
    window.blit(indicator_images["ORANGE"], (start_x + 84, start_y))

    start_x += 120
    # Green
    window.blit(indicator_images["YELLOW"], (start_x, start_y))
    window.blit(plus_sign, (start_x + 23, start_y - 4))
    window.blit(indicator_images["BLUE"], (start_x + 41, start_y))
    window.blit(equals_sign, (start_x + 64, start_y - 4))
    window.blit(indicator_images["GREEN"], (start_x + 84, start_y))
    
    start_x += 120
    # Purple
    window.blit(indicator_images["BLUE"], (start_x, start_y))
    window.blit(plus_sign, (start_x + 23, start_y - 3))
    window.blit(indicator_images["RED"], (start_x + 41, start_y))
    window.blit(equals_sign, (start_x + 64, start_y - 3))
    window.blit(indicator_images["PURPLE"], (start_x + 84, start_y))

def render_game(window, background_image, pipe_images, indicator_images, player, falling_objects, bins, score, time_left, combo_multiplier, plus_sign, equals_sign, font):
    window.fill((0, 43, 34))    # Fill lower area with darkest blue-green from background
    window.blit(background_image, (0, 0))

    window.blit(player.image, player.rect)

    # Display indicator above robot for currently held color
    if player.held_color is not None:
        indicator_pos = (player.rect.x + (player.image.get_width() // 2) - 10, player.rect.y - 10) # Calculate indicator image's position
        window.blit(indicator_images[player.held_color], indicator_pos)

    for object in falling_objects:
        window.blit(object.image, object.rect)

    # Render pipes at top (over blobs, under UI)
    window.blit(pipe_images[0], (76,-125))  # Red
    window.blit(pipe_images[1], (336,-125)) # Yellow
    window.blit(pipe_images[2], (587,-125)) # Blue

    for bin in bins:
        if bin.has_bonus:   # Pulsing effect, render both normal and glow
            window.blit(bin.normal_image, bin.rect)
            window.blit(bin.glow_image, bin.rect)
        elif bin.is_active: # Bin doesn't have bonus but could be glowing for active
            window.blit(bin.glow_image, bin.rect)
        else:
            window.blit(bin.normal_image, bin.rect)
        # Render an indicator image label on top of each bin
        bin_label_pos = (bin.rect.x + (bin.image.get_width() // 2) - 8, bin.rect.y + (bin.image.get_height() // 2) - 10)  # Center position
        window.blit(indicator_images[bin.color], bin_label_pos)

    render_ui(window, score, time_left, combo_multiplier, indicator_images, plus_sign, equals_sign, font)
    pygame.display.flip()

def render_game_over(window, font, new_high_score):
    """
    Displays the game-over screen.

    Parameters:
    - window: The game window.
    - font: The font object for rendering text.
    """
    game_over_text = font.render("Game Over", True, (255, 0, 0))  # Red text
    restart_text = font.render("Press R to Restart", True, (255, 255, 255))  # White text

    # Center the text on the screen
    if new_high_score:
        high_score_text = font.render("New High Score!", True, (255, 255, 0))  # Yellow text
        window.blit(high_score_text, (WINDOW_WIDTH // 2 - high_score_text.get_width() // 2, WINDOW_HEIGHT // 2 - 110))
    window.blit(game_over_text, (WINDOW_WIDTH // 2 - game_over_text.get_width() // 2, WINDOW_HEIGHT // 2 - 50))
    window.blit(restart_text, (WINDOW_WIDTH // 2 - restart_text.get_width() // 2, WINDOW_HEIGHT // 2 + 10))
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
    move_left = move_right = restart = start_game = down_key_pressed = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False, start_game, restart, move_left, move_right, down_key_pressed
        
        # if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Check for left mouse click
        #     for bin in bins:
        #         if bin.rect.collidepoint(event.pos):
        #             clicked_bin_color = bin.color
        #             break   # stop checking once clicked bin is found

    keys = pygame.key.get_pressed()
    if game_state == "start_menu" and any(keys):
        start_game = True
    if game_state == "playing":
        move_left = keys[pygame.K_LEFT] or keys[pygame.K_a]
        move_right = keys[pygame.K_RIGHT] or keys[pygame.K_d]
        down_key_pressed = keys[pygame.K_DOWN] or keys[pygame.K_s]
    elif game_state == "game_over" and keys[pygame.K_r]:
        restart = True

    return True, start_game, restart, move_left, move_right, down_key_pressed

def main():
    global game_state

    window = initialize_game()
    background_image, start_menu_image, player_images, blob_images, indicator_images, bin_images, wrench_image, pipe_images, sounds = load_assets()

    player = Player(400 - (player_images['idle'][0].get_width() // 2), 388, player_images)   # Center the player
    screen_width = 800
    screen_height = 600
    falling_objects = []
    spawn_timer = 0
    spawn_delay = 0
    bin_bonus_timer = 0    
    score = 0
    high_score = 0
    combo_multiplier = 1

    # Create bins - each 69 wide, so space them out accordingly
    red_bin = Bin(55, 500, bin_images["RED"], "RED")
    orange_bin = Bin(179, 500, bin_images["ORANGE"], "ORANGE")
    yellow_bin = Bin(303, 500, bin_images["YELLOW"], "YELLOW")
    green_bin = Bin(427, 500, bin_images["GREEN"], "GREEN")
    blue_bin = Bin(551, 500, bin_images["BLUE"], "BLUE")
    purple_bin = Bin(675, 500, bin_images["PURPLE"], "PURPLE")
    bins = [red_bin, orange_bin,yellow_bin, green_bin, blue_bin, purple_bin]

    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    # Setup for the "recipe book" UI display (displayed by render_ui function later)
    plus_sign = font.render("+", True, (255,255,255))
    equals_sign = font.render("=", True, (255,255,255))
    
    # Set up for clock ticks
    last_tick_second = -1

    # Start music on infinite loop
    pygame.mixer.music.load("assets/audio/menu_music.mp3")
    pygame.mixer.music.play(loops=-1)

    game_state = "start_menu"  # The initial game state

    running = True
    while running:
        running, start_game, restart, move_left, move_right, down_key_pressed = handle_events(game_state, bins)

        if game_state == "start_menu":
            render_start_menu(window, start_menu_image)
            if start_game:
                pygame.mixer.music.load("assets/audio/background_music.wav")
                pygame.mixer.music.play(loops=-1)  
                start_time = pygame.time.get_ticks()
                bin_bonus_timer = start_time + 4000    # First bonus will appear 4 seconds in
                game_state = "playing"
        elif game_state == "playing":
            # Check timer
            elapsed_time = pygame.time.get_ticks() - start_time
            time_left = (GAME_DURATION - elapsed_time) // 1000

            # Check if last 10 seconds and play sound (if one hasn't already played for this second)
            if time_left <= 10 and time_left != last_tick_second:
                sounds['clock_tick'].play()
                last_tick_second = time_left
        
            if time_left <= 0:
                game_state = "game_over"
                time_left = 0

            # Update player position
            player.move(move_left, move_right)

            # Determine which bin should be active based on proximity, also update bins
            active_bin = None
            for bin in bins:
                bin.update()
                if player.rect.colliderect(bin.activation_zone):
                    active_bin = bin
                    bin.is_active = True
                else:
                    bin.is_active = False

            if down_key_pressed and active_bin is not None and not player.is_stunned:
                if player.held_color is not None:
                    if player.held_color == active_bin.color:
                        # Drop color in correct (matching) bin
                        sounds['correct_deposit'].play()

                        # Calculate score for drop
                        bonus_multiplier = BONUS_MULTIPLIER if active_bin.has_bonus else 1  # Check if bonus is active on that bin
                        if active_bin.color in SPAWNABLE_COLORS:   # Primary colors aren't worth as many points
                            score += PRIMARY_SCORE * combo_multiplier * bonus_multiplier
                        else:       # Secondary (mixed) colors are worth more points
                            score += SECONDARY_SCORE * combo_multiplier * bonus_multiplier

                        combo_multiplier = min(combo_multiplier + 1, MAX_COMBO)  # Max combo multiplier is 5x
                    elif player.held_color is not None:   # If color dropped in wrong bin, reset combo
                        sounds['wrong_deposit'].play()
                        combo_multiplier = 1
                    player.update_held_color(None)

            # Spawn blobs periodically
            if pygame.time.get_ticks() - spawn_timer > spawn_delay:
              spawn_object(falling_objects, blob_images, wrench_image, screen_width)
              spawn_timer = pygame.time.get_ticks()
              spawn_delay = random.randint(800, 1500)
            
            # Activate bins periodically with bonuses
            if pygame.time.get_ticks() > bin_bonus_timer:
              random.choice(bins).start_bonus()
              bin_bonus_timer = pygame.time.get_ticks() + random.randint(13000,15000)    # Next bonus in 13-15 seconds (10 second long bonuses)

            move_blobs(falling_objects, screen_height)

            # Check for collisions
            for object in falling_objects[:]:
                if player.rect.colliderect(object.rect):
                    if isinstance(object, Blob):  # If touching blob, try to catch it
                        if player.update_held_color(object.color):    # If color successfully changes (blob is caught)
                            sounds['catch_blob'].play()
                            falling_objects.remove(object)
                        # Else, not catchable, so nothing happens - blobs falls down screen
                    else:   # Hazard
                        sounds['hazard_hit'].play()
                        player.get_stunned()
                        combo_multiplier = 1    # Reset combo
                        player.update_held_color(None)
                        falling_objects.remove(object)   

            # Render the game
            render_game(window, background_image, pipe_images, indicator_images, player, falling_objects, bins, score, time_left, combo_multiplier, plus_sign, equals_sign, font)

        elif game_state == "game_over":
            new_high_score = False
            if score > high_score:
                new_high_score = True
                high_score = score
            render_game_over(window, font, new_high_score)

            # Handle restart
            if restart:
                falling_objects = []
                score = 0
                player.update_held_color(None)
                combo_multiplier = 1
                start_time = pygame.time.get_ticks()    # Reset timer
                bin_bonus_timer = start_time + 4000
                game_state = "playing"

        clock.tick(60)

    pygame.mixer.music.stop()
    pygame.quit()

if __name__ == "__main__":
    main()