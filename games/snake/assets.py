import os
import sys
import pygame

# Base path for assets (handles PyInstaller _MEIPASS)
BASE_PATH = getattr(sys, '_MEIPASS', os.path.dirname(__file__))
ASSETS_PATH = os.path.join(BASE_PATH, "assets")
SOUNDS_PATH = os.path.join(ASSETS_PATH, "sounds")
FONTS_PATH = os.path.join(ASSETS_PATH, "DejaVuSans.ttf")

# Dimensions
CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 30
GRID_PIXEL_WIDTH = GRID_WIDTH * CELL_SIZE
GRID_PIXEL_HEIGHT = GRID_HEIGHT * CELL_SIZE
TOP_UI_HEIGHT = 30
BOTTOM_UI_HEIGHT = 30
WINDOW_WIDTH = GRID_PIXEL_WIDTH
WINDOW_HEIGHT = TOP_UI_HEIGHT + GRID_PIXEL_HEIGHT + BOTTOM_UI_HEIGHT

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 200)
GRAY = (100, 100, 100)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Fonts
pygame.font.init()
SCORE_FONT = pygame.font.Font(FONTS_PATH, 24)
FOOTER_FONT = pygame.font.Font(FONTS_PATH, 16)
