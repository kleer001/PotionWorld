"""
Game constants and configuration values for PotionWorld.
"""

# Window settings
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
WINDOW_TITLE = "PotionWorld - Season 0 MVP"

# Game settings - Grid-based movement
TILE_SIZE = 40  # 40px tiles
PLAYER_MOVE_SPEED = 120.0  # 120px/s = 3 tiles/second
CAMERA_SPEED = 0.2  # Faster camera following
INPUT_BUFFER_TIME = 0.15  # 150ms input buffer
CORNER_FORGIVENESS = 6  # 6px corner snap threshold

# Stats
STAT_CAP = 100
STAT_THRESHOLDS = [25, 50, 75, 100]

# Affinity
AFFINITY_MIN = -5.0
AFFINITY_MAX = 5.0
AFFINITY_DECAY_RATE = 0.01  # Per day

# Gathering
GATHERING_INTERACTION_RANGE = 100.0
DEFAULT_RESPAWN_TIME = 300.0  # 5 minutes

# Scene paths (for organization)
SCENE_MENU = "menu"
SCENE_GAME = "game"
SCENE_INVENTORY = "inventory"
SCENE_CRAFTING = "crafting"
SCENE_DIALOGUE = "dialogue"

# Asset paths
ASSETS_DIR = "assets"
SPRITES_DIR = f"{ASSETS_DIR}/sprites"
AUDIO_DIR = f"{ASSETS_DIR}/audio"
FONTS_DIR = f"{ASSETS_DIR}/fonts"

# Resource paths
RESOURCES_DIR = "resources"
INGREDIENTS_FILE = f"{RESOURCES_DIR}/ingredients.json"
RECIPES_FILE = f"{RESOURCES_DIR}/recipes.json"
NPCS_FILE = f"{RESOURCES_DIR}/npcs.json"

# Colors
COLOR_SUCCESS = (50, 200, 50)
COLOR_WARNING = (255, 200, 50)
COLOR_ERROR = (200, 50, 50)
COLOR_INFO = (100, 150, 255)
COLOR_NEUTRAL = (200, 200, 200)

# Z-ordering (draw order)
Z_BACKGROUND = 0
Z_GROUND = 10
Z_GATHERING_SPOTS = 20
Z_PLAYER = 30
Z_NPCS = 30
Z_EFFECTS = 40
Z_UI = 100
