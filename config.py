# Screen settings
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60

# Colors
OCEAN_BLUE = (0, 127, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Environmental factors
TEMP_MIN = 20.0
TEMP_MAX = 32.0
TEMP_OPTIMAL = 26.0

PH_MIN = 7.5
PH_MAX = 8.5
PH_OPTIMAL = 8.2

SALINITY_MIN = 30.0
SALINITY_MAX = 36.0
SALINITY_OPTIMAL = 33.0

# Game settings
INITIAL_HEALTH = 100
HEALTH_DECREASE_RATE = 0.1
DIFFICULTY_LEVELS = {
    "easy": 0.5,
    "medium": 1.0,
    "hard": 2.0
}

DIFFICULTY_SETTINGS = {
    "easy": {
        "health_decrease_rate": 0.05,
        "event_frequency": 0.5,
        "damage_multiplier": 0.75,
        "starting_health": 100
    },
    "normal": {
        "health_decrease_rate": 0.1,
        "event_frequency": 1.0,
        "damage_multiplier": 1.0,
        "starting_health": 100
    },
    "hard": {
        "health_decrease_rate": 0.15,
        "event_frequency": 1.5,
        "damage_multiplier": 1.25,
        "starting_health": 80
    }
} 