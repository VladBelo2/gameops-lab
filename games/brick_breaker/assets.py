import os
import sys
import pygame

# Paths
# BASE_PATH = sys._MEIPASS if getattr(sys, 'frozen', False) else os.path.dirname(__file__)
# BASE_PATH = getattr(sys, '_MEIPASS', os.path.dirname(__file__))
# Detect PyInstaller environment
if getattr(sys, 'frozen', False):
    BASE_PATH = os.path.join(sys._MEIPASS, "_internal")
else:
    BASE_PATH = os.path.dirname(__file__)
ASSETS_PATH = os.path.join(BASE_PATH, "assets")
# ASSETS_PATH = os.path.join(BASE_PATH, "_internal", "assets")
SOUNDS_PATH = os.path.join(ASSETS_PATH, "sounds")
FONTS_PATH = os.path.join(ASSETS_PATH, "DejaVuSans.ttf")
BACKGROUND_PATH = os.path.join(ASSETS_PATH, "background.png")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (40, 40, 40)
RED = (255, 0, 0)
BLUE = (0, 120, 255)
BRICK_COLOR = (255, 180, 0)
FOOTER_COLOR = (255, 80, 80)

# Dimensions
WINDOW_WIDTH = 600
SCORE_HEIGHT = 30
FOOTER_HEIGHT = 30
PLAY_HEIGHT = 600
WINDOW_HEIGHT = SCORE_HEIGHT + PLAY_HEIGHT + FOOTER_HEIGHT
FPS = 60

PADDLE_WIDTH = 60
PADDLE_HEIGHT = 10
BALL_RADIUS = 6
BRICK_WIDTH = 30
BRICK_HEIGHT = 20
BRICK_GAP = 1
BRICK_ROWS = 4
BRICK_COLS = WINDOW_WIDTH // (BRICK_WIDTH + BRICK_GAP)

# Fonts
pygame.font.init()
FONT = pygame.font.Font(FONTS_PATH, 24)
FOOTER_FONT = pygame.font.Font(FONTS_PATH, 10)

# Background
BACKGROUND_IMG = pygame.transform.scale(pygame.image.load(BACKGROUND_PATH), (WINDOW_WIDTH, PLAY_HEIGHT))

