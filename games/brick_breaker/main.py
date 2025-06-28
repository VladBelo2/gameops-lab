import pygame
from brick_breaker.assets import *
from brick_breaker.game import GameState
from brick_breaker.ui import *
import brick_breaker.sounds
import os

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

brick_breaker.sounds.init_sounds(os.path.join(ASSETS_PATH, "sounds"))
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Brick Breaker")
clock = pygame.time.Clock()
game = GameState()

running = True
while running:
    screen.fill(BLACK)

    if game.start_menu:
        draw_start_menu(screen)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                brick_breaker.sounds.play("click_fun")
                game.start_menu = False
        continue

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if not game.game_over and event.key == pygame.K_ESCAPE:
                game.paused = not game.paused
                brick_breaker.sounds.play("pause_fun")
            elif event.key == pygame.K_m:
                muted = brick_breaker.sounds.toggle_mute()
                print("🔇 Muted" if muted else "🔊 Unmuted")
                
    keys = pygame.key.get_pressed()
    if not game.paused and not game.game_over:
        if keys[pygame.K_LEFT]:
            game.paddle.x -= 6
        if keys[pygame.K_RIGHT]:
            game.paddle.x += 6
        game.paddle.x = max(0, min(WINDOW_WIDTH - PADDLE_WIDTH, game.paddle.x))

        if not game.ball_active:
            game.ball.centerx = game.paddle.centerx
            game.ball.bottom = game.paddle.top
        else:
            game.update_ball()

    if keys[pygame.K_SPACE] and not game.ball_active and not game.game_over:
        game.ball_active = True

    for brick in game.bricks:
        pygame.draw.rect(screen, BRICK_COLOR, brick)
        pygame.draw.rect(screen, BLACK, brick, 1)

    pygame.draw.rect(screen, BLUE, game.paddle)
    pygame.draw.ellipse(screen, RED, game.ball)

    draw_score(screen, game.score)
    draw_footer(screen)

    if game.game_over:
        game.fade_alpha = min(180, game.fade_alpha + 5)
        draw_gameover(screen, game.fade_alpha)
        if keys[pygame.K_SPACE]:
            brick_breaker.sounds.play("win_fun")
            game.reset_game()

    if game.paused and not game.game_over:
        draw_pause(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
