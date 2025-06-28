import os

# Window
WINDOW_WIDTH = 300
WINDOW_HEIGHT = 660
SCORE_AREA_HEIGHT = 30
FOOTER_HEIGHT = 30
PLAY_AREA_HEIGHT = 600

# Grid
GRID_WIDTH, GRID_HEIGHT = 10, 20
CELL_SIZE = WINDOW_WIDTH // GRID_WIDTH

# Colors
BLACK = (0, 0, 0)
GRAY = (40, 40, 40)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
SHADOW_COLOR = (110, 110, 110)

# Timing
FPS = 60
FALL_SPEED = 30

# Paths
BASE_PATH = getattr(__import__('sys'), '_MEIPASS', os.path.dirname(__file__))
ASSETS_PATH = os.path.join(BASE_PATH, "assets")
SOUNDS_PATH = os.path.join(ASSETS_PATH, "sounds")
FONT_PATH = os.path.join(ASSETS_PATH, "DejaVuSans.ttf")
