import pygame
from brick_breaker.assets import *
import brick_breaker.sounds
from brick_breaker.levels import generate_bricks

class GameState:
    def __init__(self, regenerate_on_empty=True):
        self.regenerate_on_empty = regenerate_on_empty

        self.score = 0
        self.level = 1
        self.bricks = generate_bricks(self.level)
        self.paddle = pygame.Rect(WINDOW_WIDTH // 2 - PADDLE_WIDTH // 2, SCORE_HEIGHT + PLAY_HEIGHT - 30, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.ball = pygame.Rect(WINDOW_WIDTH // 2 - BALL_RADIUS, self.paddle.y - BALL_RADIUS * 2, BALL_RADIUS * 2, BALL_RADIUS * 2)
        self.ball_dx, self.ball_dy = 4, -4
        self.ball_active = False
        self.paused = False
        self.start_menu = True
        self.game_over = False
        self.fade_alpha = 0

    def reset_level(self):
        self.bricks = generate_bricks(self.level)
        self.ball_active = False
        self.ball.centerx = self.paddle.centerx
        self.ball.bottom = self.paddle.top

    def next_level(self):
        self.level += 1
        brick_breaker.sounds.play("level_up_fun")
        self.reset_level()

    def reset_game(self):
        self.level = 1
        self.score = 0
        self.game_over = False
        self.fade_alpha = 0
        self.bricks = generate_bricks(self.level)
        self.ball_active = False
        self.ball.centerx = self.paddle.centerx
        self.ball.bottom = self.paddle.top

    def update_ball(self):
        if self.paused:
            return

        # Always check win condition, regardless of ball_active
        if not self.bricks:
            self.game_over = True
            self.ball_active = False
            if self.regenerate_on_empty:
                self.next_level()
            return

        if not self.ball_active:
            return

        self.ball.x += self.ball_dx
        self.ball.y += self.ball_dy

        if self.ball.left <= 0 or self.ball.right >= WINDOW_WIDTH:
            self.ball_dx *= -1
            brick_breaker.sounds.play("bounce")
        if self.ball.top <= SCORE_HEIGHT:
            self.ball_dy *= -1
        if self.ball.colliderect(self.paddle):
            self.ball_dy *= -1
            brick_breaker.sounds.play("bounce")

        for brick in self.bricks[:]:
            if self.ball.colliderect(brick):
                self.bricks.remove(brick)
                self.ball_dy *= -1
                self.score += 10
                brick_breaker.sounds.play("break")
                if not self.bricks:
                    self.next_level()
                break

        if self.ball.bottom >= SCORE_HEIGHT + PLAY_HEIGHT:
            self.ball_active = False
            self.game_over = True
            brick_breaker.sounds.play("gameover_fun")
            self.fade_alpha = 0
        
        if not self.bricks:
            if self.regenerate_on_empty:
                self.next_level()
            else:
                self.game_over = True
                self.ball_active = False


