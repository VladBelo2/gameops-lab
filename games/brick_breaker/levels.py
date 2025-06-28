from brick_breaker.assets import BRICK_COLS, BRICK_WIDTH, BRICK_HEIGHT, BRICK_GAP, SCORE_HEIGHT
import pygame

def generate_bricks(level: int):
    bricks = []
    rows = min(4 + level, 10)
    x_offset = (600 - (BRICK_COLS * (BRICK_WIDTH + BRICK_GAP) - BRICK_GAP)) // 2
    for row in range(rows):
        for col in range(BRICK_COLS):
            x = x_offset + col * (BRICK_WIDTH + BRICK_GAP)
            y = SCORE_HEIGHT + row * (BRICK_HEIGHT + BRICK_GAP)
            bricks.append(pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT))
    return bricks

