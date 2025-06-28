import pygame
from snake.assets import (
    GRID_WIDTH, GRID_HEIGHT, CELL_SIZE,
    GRID_PIXEL_HEIGHT, TOP_UI_HEIGHT, BOTTOM_UI_HEIGHT,
    WINDOW_WIDTH, WINDOW_HEIGHT,
    BLACK, WHITE, GREEN, RED, GRAY,
    SCORE_FONT, FOOTER_FONT
)

def draw_grid(win):
    for x in range(0, WINDOW_WIDTH, CELL_SIZE):
        pygame.draw.line(win, GRAY, (x, TOP_UI_HEIGHT), (x, TOP_UI_HEIGHT + GRID_PIXEL_HEIGHT))
    for y in range(0, GRID_PIXEL_HEIGHT + CELL_SIZE, CELL_SIZE):
        pygame.draw.line(win, GRAY, (0, TOP_UI_HEIGHT + y), (WINDOW_WIDTH, TOP_UI_HEIGHT + y))

def draw_snake(win, snake):
    for segment in snake.body:
        rect = pygame.Rect(
            segment[0] * CELL_SIZE,
            TOP_UI_HEIGHT + segment[1] * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE
        )
        pygame.draw.rect(win, GREEN, rect)

def draw_food(win, food):
    rect = pygame.Rect(
        food.position[0] * CELL_SIZE,
        TOP_UI_HEIGHT + food.position[1] * CELL_SIZE,
        CELL_SIZE,
        CELL_SIZE
    )
    pygame.draw.rect(win, RED, rect)


def draw_score(win, score):
    text = SCORE_FONT.render(f"Score: {score}", True, WHITE)
    win.blit(text, (10, 5))


def draw_footer(win):
    footer = FOOTER_FONT.render("Developed by Vlad Belo", True, GRAY)
    win.blit(footer, (WINDOW_WIDTH - 190, WINDOW_HEIGHT - BOTTOM_UI_HEIGHT + 8))


def draw_game_over(win):
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    overlay.set_alpha(180)
    overlay.fill(BLACK)
    win.blit(overlay, (0, 0))
    text = SCORE_FONT.render("Game Over. Press R to Restart", True, RED)
    win.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, WINDOW_HEIGHT // 2))


def draw_paused(win):
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    overlay.set_alpha(120)
    overlay.fill(BLACK)
    win.blit(overlay, (0, 0))
    text = SCORE_FONT.render("⏸️ Paused - Press ESC to Resume", True, WHITE)
    win.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, WINDOW_HEIGHT // 2))


def draw_start_screen(win):
    win.fill(BLACK)
    title = SCORE_FONT.render("🐍 Snake Game", True, GREEN)
    prompt = FOOTER_FONT.render("Press any key to start", True, WHITE)
    win.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, WINDOW_HEIGHT // 2 - 40))
    win.blit(prompt, (WINDOW_WIDTH // 2 - prompt.get_width() // 2, WINDOW_HEIGHT // 2 + 10))
    pygame.display.flip()
