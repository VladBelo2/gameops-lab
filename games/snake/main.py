import pygame
import sys
import os
from snake.assets import *
from snake.game import SnakeGame
from snake.ui import (
    draw_grid, draw_snake, draw_food,
    draw_score, draw_footer, draw_paused,
    draw_start_screen
)
from snake.sounds import init_sounds, play

pygame.init()

# Allow clean exit in Docker build test
if os.environ.get("HEADLESS_TEST") == "1":
    print("✅ Headless test passed. Exiting cleanly.")
    sys.exit(0)

try:
    pygame.mixer.init()
except pygame.error:
    print("⚠️  Pygame mixer failed to initialize (likely headless/no sound). Skipping sound.")

win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("🐍 Snake Game")
clock = pygame.time.Clock()

# 🧠 Initialize sounds
init_sounds(SOUNDS_PATH)

game = SnakeGame()
paused = False
start_screen = True
game_over_alpha = 0

def fade_game_over():
    global game_over_alpha
    if game_over_alpha < 180:
        game_over_alpha += 10
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    overlay.set_alpha(game_over_alpha)
    overlay.fill(BLACK)
    win.blit(overlay, (0, 0))
    text = SCORE_FONT.render("Game Over - Press R to Restart", True, RED)
    win.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, WINDOW_HEIGHT // 2))

while True:
    if start_screen:
        draw_start_screen(win)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                play("click")
                start_screen = False
        continue

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and game.alive:
                paused = not paused
                play("pause")
            if event.key == pygame.K_r and not game.alive:
                game.reset()
                paused = False
                game_over_alpha = 0
                play("click")
            if event.key == pygame.K_UP:
                game.change_direction(UP)
            elif event.key == pygame.K_DOWN:
                game.change_direction(DOWN)
            elif event.key == pygame.K_LEFT:
                game.change_direction(LEFT)
            elif event.key == pygame.K_RIGHT:
                game.change_direction(RIGHT)

    if not paused and game.alive:
        game.update()
        if not game.alive:
            play("gameover")
        elif game.snake.get_head() == game.food.position:
            play("eat")

    win.fill(BLACK)
    draw_grid(win)
    draw_snake(win, game.snake)
    draw_food(win, game.food)
    draw_score(win, game.score)
    draw_footer(win)

    if not game.alive:
        fade_game_over()
    elif paused:
        draw_paused(win)

    pygame.display.flip()
    clock.tick(10)
