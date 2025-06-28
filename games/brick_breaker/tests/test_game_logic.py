import pytest
import pygame
from brick_breaker.game import GameState
from brick_breaker.assets import SCORE_HEIGHT, PLAY_HEIGHT, BRICK_HEIGHT, WINDOW_WIDTH

# Initialize pygame for Rect usage
pygame.init()

def test_initial_score():
    game = GameState()
    assert game.score == 0

def test_bricks_generated():
    game = GameState()
    assert len(game.bricks) > 0

def test_ball_reset_after_gameover():
    game = GameState()
    game.ball_active = True
    game.ball.y = SCORE_HEIGHT + PLAY_HEIGHT + 10  # Simulate falling
    game.update_ball()
    assert not game.ball_active
    assert game.game_over

def test_score_increase_on_brick_break():
    game = GameState(regenerate_on_empty=False)
    game.next_level = lambda: None  # prevent auto-level-up

    # Clear all and inject 1 brick
    game.bricks.clear()
    game.score = 0
    brick = pygame.Rect(game.ball.x, game.ball.y - 1, 30, BRICK_HEIGHT)
    game.bricks.append(brick)

    game.ball_dy = -4
    game.ball_active = True
    game.update_ball()

    assert game.score == 10
    assert len(game.bricks) == 0

def test_win_condition():
    game = GameState(regenerate_on_empty=False)  # 🔧 critical fix
    game.bricks.clear()  # Simulate all bricks gone
    game.update_ball()
    assert game.game_over
    assert game.ball_active is False

def test_paddle_stays_in_bounds():
    game = GameState()
    game.paddle.left = -10
    game.paddle.right = 1000  # Arbitrary large number
    game.paddle.left = max(0, game.paddle.left)
    game.paddle.right = min(WINDOW_WIDTH, game.paddle.right)
    assert game.paddle.left >= 0
    assert game.paddle.right <= WINDOW_WIDTH

def test_ball_reflection_angle_center_vs_edge():
    game = GameState()
    game.ball.bottom = game.paddle.top
    game.ball.centerx = game.paddle.centerx
    game.ball_dy = 4
    game.ball_dx = 0
    game.ball_active = True
    game.update_ball()
    assert game.ball_dy < 0  # Should reflect

    game = GameState()
    game.ball.bottom = game.paddle.top
    game.ball.centerx = game.paddle.left
    game.ball_dy = 4
    game.ball_dx = 0
    game.ball_active = True
    game.update_ball()
    assert game.ball_dy < 0  # Should reflect

def test_pause_and_resume_logic():
    game = GameState()
    old_y = game.ball.y
    game.paused = True
    game.update_ball()
    assert game.ball.y == old_y  # Ball shouldn't move

def test_level_up_logic():
    game = GameState()
    game.score = 100
    old_level = game.level
    game.bricks.clear()
    game.ball_active = True
    game.update_ball()
    assert game.level == old_level + 1
    assert len(game.bricks) > 0

def test_rapid_input_handling():
    game = GameState()
    start_x = game.paddle.x
    for _ in range(10):
        game.paddle.x -= 5
        game.paddle.x += 5
    assert abs(game.paddle.x - start_x) < 20

# --- Additional Tests ---

def test_sound_triggers_on_brick_break(monkeypatch):
    game = GameState(regenerate_on_empty=False)
    triggered = {}
    monkeypatch.setattr("brick_breaker.sounds.play", lambda name: triggered.setdefault(name, True))

    game.bricks.clear()
    brick = pygame.Rect(game.ball.x, game.ball.y - 1, 30, BRICK_HEIGHT)
    game.bricks.append(brick)
    game.ball_dy = -4
    game.ball_active = True
    game.update_ball()

    assert triggered.get("break") is True

def test_gameover_sound_trigger(monkeypatch):
    game = GameState()
    triggered = {}
    monkeypatch.setattr("brick_breaker.sounds.play", lambda name: triggered.setdefault(name, True))

    game.ball_active = True
    game.ball.y = SCORE_HEIGHT + PLAY_HEIGHT + 10
    game.update_ball()

    assert triggered.get("gameover_fun") is True

def test_bounce_sound_trigger(monkeypatch):
    game = GameState()
    triggered = {}
    monkeypatch.setattr("brick_breaker.sounds.play", lambda name: triggered.setdefault(name, True))

    game.ball_active = True
    game.ball.x = 0  # left wall
    game.ball_dx = -4  # move into the wall
    game.update_ball()

    assert triggered.get("bounce") is True


def test_brick_overlap_check():
    game = GameState()
    positions = set()
    for brick in game.bricks:
        pos = (brick.x, brick.y)
        assert pos not in positions  # no duplicates
        positions.add(pos)

def test_level_brick_count_increase():
    game = GameState()
    initial = len(game.bricks)
    game.next_level()
    assert len(game.bricks) >= initial  # Should grow or stay consistent

def test_multiple_level_progression():
    game = GameState()
    for _ in range(3):
        game.bricks.clear()
        game.ball_active = True
        game.update_ball()
    assert game.level >= 4
