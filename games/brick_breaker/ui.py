import pygame
from brick_breaker.assets import *

def draw_footer(screen):
    footer = FOOTER_FONT.render("Developed by - Vlad Belo", True, FOOTER_COLOR)
    screen.blit(footer, (10, WINDOW_HEIGHT - 22))

def draw_score(screen, score):
    score_label = FONT.render(f"Score: {score}", True, WHITE)
    screen.blit(score_label, (10, (SCORE_HEIGHT - score_label.get_height()) // 2))

def draw_pause(screen):
    pause_label = FONT.render("Paused", True, RED)
    screen.blit(pause_label, ((WINDOW_WIDTH - pause_label.get_width()) // 2, 300))

def draw_gameover(screen, fade_alpha):
    overlay = pygame.Surface((300, 120), pygame.SRCALPHA)
    pygame.draw.rect(overlay, (200, 200, 200, fade_alpha), overlay.get_rect(), border_radius=20)
    pygame.draw.rect(overlay, RED, overlay.get_rect(), width=2, border_radius=20)
    screen.blit(overlay, ((WINDOW_WIDTH - 300) // 2, 250))
    over1 = FONT.render("Game Over!", True, RED)
    over2 = FONT.render("Press SPACE to Retry", True, RED)
    screen.blit(over1, ((WINDOW_WIDTH - over1.get_width()) // 2, 260))
    screen.blit(over2, ((WINDOW_WIDTH - over2.get_width()) // 2, 300))

def draw_start_menu(screen):
    screen.blit(BACKGROUND_IMG, (0, 0))
    label = FONT.render("Press SPACE to Start", True, WHITE)
    screen.blit(label, ((WINDOW_WIDTH - label.get_width()) // 2, 300))
    draw_footer(screen)
