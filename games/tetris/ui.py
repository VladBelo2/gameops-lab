import pygame
from tetris.assets import *

_font = None
_footer_font = None

def init_fonts():
    global _font, _footer_font
    if _font is None:
        pygame.font.init()
        _font = pygame.font.Font(FONT_PATH, 20)
        _footer_font = pygame.font.Font(FONT_PATH, 10)

def draw_score(screen, score):
    init_fonts()
    label = _font.render(f"Score: {score}", True, WHITE)
    screen.blit(label, (10, (SCORE_AREA_HEIGHT - label.get_height()) // 2))

def draw_footer(screen):
    init_fonts()
    label = _footer_font.render("Developed by - Vlad Belo", True, (255, 80, 80))
    screen.blit(label, (10, WINDOW_HEIGHT - 22))

def draw_pause(screen):
    init_fonts()
    label = _font.render("Paused", True, RED)
    screen.blit(label, ((WINDOW_WIDTH - label.get_width()) // 2, 300))

def draw_game_over(screen, alpha):
    init_fonts()
    overlay = pygame.Surface((260, 100), pygame.SRCALPHA)
    pygame.draw.rect(overlay, (255, 255, 255, 240), overlay.get_rect(), border_radius=12)
    pygame.draw.rect(overlay, (200, 0, 0), overlay.get_rect(), width=2, border_radius=12)
    overlay.set_alpha(alpha)
    screen.blit(overlay, ((WINDOW_WIDTH - 260) // 2, 250))
    label1 = _font.render("-- GAME OVER --", True, RED)
    label2 = _font.render("Press R to Restart", True, RED)
    screen.blit(label1, ((WINDOW_WIDTH - label1.get_width()) // 2, 260))
    screen.blit(label2, ((WINDOW_WIDTH - label2.get_width()) // 2, 300))

def draw_start_menu(screen):
    init_fonts()
    screen.fill(BLACK)
    label = _font.render("Click to Start", True, WHITE)
    screen.blit(label, ((WINDOW_WIDTH - label.get_width()) // 2, 300))
    draw_footer(screen)

def draw_grid(screen):
    for y in range(PLAY_AREA_HEIGHT // CELL_SIZE):
        for x in range(GRID_WIDTH):
            pygame.draw.rect(
                screen,
                GRAY,
                pygame.Rect(
                    x * CELL_SIZE,
                    SCORE_AREA_HEIGHT + y * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE
                ),
                1
            )

def draw_blocks(screen):
    from tetris.game import grid
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x]:
                rect = pygame.Rect(
                    x * CELL_SIZE,
                    SCORE_AREA_HEIGHT + y * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE
                )
                pygame.draw.rect(screen, grid[y][x], rect)
                pygame.draw.rect(screen, GRAY, rect, 1)