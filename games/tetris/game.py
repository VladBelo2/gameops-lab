import random
import pygame
from tetris.assets import *

TETROMINO_SHAPES = {
    'I': [[0, 0, 0, 0], [1, 1, 1, 1]],
    'O': [[1, 1], [1, 1]],
    'T': [[0, 1, 0], [1, 1, 1]],
    'S': [[0, 1, 1], [1, 1, 0]],
    'Z': [[1, 1, 0], [0, 1, 1]],
    'L': [[0, 0, 1], [1, 1, 1]],
    'J': [[1, 0, 0], [1, 1, 1]],
}

TETROMINO_COLORS = {
    'I': (0, 255, 255),
    'O': (255, 255, 0),
    'T': (128, 0, 128),
    'S': (0, 255, 0),
    'Z': (255, 0, 0),
    'L': (255, 165, 0),
    'J': (0, 0, 255),
}

grid = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
score = 0
frame_count = 0
game_over = False

class Block:
    def __init__(self):
        self.type = random.choice(list(TETROMINO_SHAPES.keys()))
        self.shape = TETROMINO_SHAPES[self.type]
        self.color = TETROMINO_COLORS[self.type]
        self.x = 3
        self.y = 0
        self.rotation = 0

    def draw(self, screen):
        # Draw ghost/shadow
        shadow_y = self.y
        while not check_collision(self, dy=shadow_y - self.y + 1):
            shadow_y += 1

        for r, row in enumerate(self.shape):
            for c, val in enumerate(row):
                if val:
                    shadow_rect = pygame.Rect(
                        (self.x + c) * CELL_SIZE,
                        SCORE_AREA_HEIGHT + (shadow_y + r) * CELL_SIZE,
                        CELL_SIZE, CELL_SIZE
                    )
                    pygame.draw.rect(screen, SHADOW_COLOR, shadow_rect, 1)

        # Draw actual block
        for r, row in enumerate(self.shape):
            for c, val in enumerate(row):
                if val:
                    rect = pygame.Rect(
                        (self.x + c) * CELL_SIZE,
                        SCORE_AREA_HEIGHT + (self.y + r) * CELL_SIZE,
                        CELL_SIZE, CELL_SIZE
                    )
                    pygame.draw.rect(screen, self.color, rect)
                    pygame.draw.rect(screen, GRAY, rect, 1)

    def rotate(self):
        if self.type == 'O':
            return
        rotated = [list(row) for row in zip(*self.shape[::-1])]
        old = self.shape
        self.shape = rotated
        self.rotation = (self.rotation + 1) % 4
        if check_collision(self):
            self.shape = old
            self.rotation = (self.rotation - 1) % 4

    def move_left(self):
        if not check_collision(self, dx=-1): self.x -= 1

    def move_right(self):
        if not check_collision(self, dx=1): self.x += 1

    def move_down(self):
        if not check_collision(self, dy=1):
            self.y += 1
            return True
        return False

def check_collision(block, dx=0, dy=0):
    for r, row in enumerate(block.shape):
        for c, val in enumerate(row):
            if val:
                nx, ny = block.x + c + dx, block.y + r + dy
                if nx < 0 or nx >= GRID_WIDTH or ny >= GRID_HEIGHT:
                    return True
                if ny >= 0 and grid[ny][nx]:
                    return True
    return False

def freeze_block(block):
    for r, row in enumerate(block.shape):
        for c, val in enumerate(row):
            if val:
                grid[block.y + r][block.x + c] = block.color

def clear_full_rows():
    global grid, score
    cleared = 0
    new_grid = []

    for row in grid:
        if all(cell is not None for cell in row):
            cleared += 1
        else:
            new_grid.append(row)

    for _ in range(cleared):
        new_grid.insert(0, [None] * GRID_WIDTH)

    grid = new_grid
    score += cleared * 100

    return cleared

def reset_game():
    global grid, score, frame_count, game_over
    grid = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    score = 0
    frame_count = 0
    game_over = False
