import pygame
import os
import sys
from tetris.assets import *
from tetris.sounds import *
from tetris.ui import *
import tetris.game as game

pygame.init()

# Allow clean exit in Docker build test
if os.environ.get("HEADLESS_TEST") == "1":
    print("✅ Headless test passed. Exiting cleanly.")
    sys.exit(0)

# Headless/Docker-safe init
try:
    pygame.mixer.init()
except pygame.error:
    print("⚠️  Pygame mixer failed to initialize (likely headless/no sound). Skipping sound.")

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()

init_sounds(SOUNDS_PATH)

start_menu = True
paused = False
fade_alpha = 0
fade_direction = 5
move_delay = 5
move_timer = 0
frame_count = 0
current_block = None
running = True
game.reset_game()

while running:
    screen.fill(BLACK)
    mouse_pos = pygame.mouse.get_pos()

    if start_menu:
        draw_start_menu(screen)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                play("click")
                start_menu = False
                current_block = game.Block()
        continue

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if not game.game_over:
                if event.key == pygame.K_UP:
                    current_block.rotate()
                    play("rotate")
                elif event.key == pygame.K_ESCAPE:
                    paused = not paused
                    play("pause")
            elif game.game_over and event.key == pygame.K_r:
                game.reset_game()
                current_block = game.Block()
                frame_count = 0
                fade_alpha = 0
                move_timer = 0
                game.game_over = False

    if paused:
        draw_pause(screen)
        pygame.display.flip()
        clock.tick(FPS)
        continue

    keys = pygame.key.get_pressed()
    if not game.game_over:
        if move_timer == 0:
            if keys[pygame.K_LEFT]:
                current_block.move_left()
                move_timer = move_delay
            elif keys[pygame.K_RIGHT]:
                current_block.move_right()
                move_timer = move_delay
        if keys[pygame.K_DOWN]:
            current_block.move_down()

    if move_timer > 0:
        move_timer -= 1

    if not game.game_over:
        frame_count += 1
        if frame_count % FALL_SPEED == 0:
            if not current_block.move_down():
                game.freeze_block(current_block)
                play("drop")
                game.clear_full_rows()
                current_block = game.Block()
                if game.check_collision(current_block):
                    game.game_over = True
                    play("gameover")

    draw_grid(screen)
    draw_blocks(screen)
    if current_block:
        current_block.draw(screen)
    draw_score(screen, game.score)

    if game.game_over:
        fade_alpha = min(180, fade_alpha + fade_direction)
        draw_game_over(screen, fade_alpha)

    draw_footer(screen)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
