# settings.py

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

GAME_TITLE = "Color Factory Frenzy!"

COLORS = {
    "RED": (255, 0, 0),
    "YELLOW": (255, 255, 0),
    "BLUE": (0, 0, 255),
    "ORANGE": (255, 165, 0),
    "GREEN": (0, 255, 0),
    "PURPLE": (128, 0, 128),
}

SPAWNABLE_COLORS = ["RED", "BLUE", "YELLOW"]

SPAWN_POSITIONS = {"RED": (115, 0), "YELLOW": (375, 0), "BLUE": (627, 0)}   # approx: x of pipe + pipe width // 2 - blob width // 2

MIX_RULES = {
    "RED": {"BLUE": "PURPLE", "YELLOW": "ORANGE"},
    "BLUE": {"RED": "PURPLE", "YELLOW": "GREEN"},
    "YELLOW": {"RED": "ORANGE", "BLUE": "GREEN"}
}

GAME_DURATION = 60000
HAZARD_CHANCE = 0.20

PLAYER_SPEED = 8
PLAYER_ANIMATION_SPEED = 50 # ms
PLAYER_STUN_DURATION = 1200 # ms

BLOB_SPEED = 4
BLOB_DRIFT = 0.4

HAZARD_SPEED = 4
HAZARD_DRIFT = 0.4

BONUS_DURATION = 10000  # ms

PRIMARY_SCORE = 100
SECONDARY_SCORE = 500
MAX_COMBO = 5
BONUS_MULTIPLIER = 2

PHASES = [
    {
        "time_left": (GAME_DURATION // 1000) // 3 * 2,  # phase starts when time_left > 60
        "min_spawn_delay": 800,
        "max_spawn_delay": 1500,
        "hazard_chance": 0.15,
        "base_fall_speed": 3.5,
        "malfunction_chance": 0.15
    },
    {
        "time_left": (GAME_DURATION // 1000) // 3,  # phase starts when 30 < time_left <= 60
        "min_spawn_delay": 500,
        "max_spawn_delay": 1000,
        "hazard_chance": 0.20,
        "base_fall_speed": 4,
        "malfunction_chance": 0.25
    },
    {
        "time_left": 0,  # phase starts when 30 < time_left <= 60
        "min_spawn_delay": 300,
        "max_spawn_delay": 700,
        "hazard_chance": 0.25,
        "base_fall_speed": 4.5,
        "malfunction_chance": 0.35
    }
]