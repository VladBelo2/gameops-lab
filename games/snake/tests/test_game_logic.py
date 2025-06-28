
import pytest
from snake.game import SnakeGame
from snake.assets import GRID_WIDTH, GRID_HEIGHT

def test_game_initial_state():
    game = SnakeGame()
    assert game.snake.get_head() == (GRID_WIDTH // 2, GRID_HEIGHT // 2)
    assert game.food.position != game.snake.get_head()
    assert game.score == 0
    assert game.alive

def test_direction_change():
    game = SnakeGame()
    game.change_direction((0, -1))  # UP
    assert game.snake.direction == (0, -1)
    game.change_direction((0, 1))  # DOWN (opposite)
    assert game.snake.direction == (0, -1)  # should be ignored

def test_snake_moves():
    game = SnakeGame()
    original_head = game.snake.body[0]
    game.update()
    assert game.snake.body[0] != original_head

def test_snake_grows_on_food():
    game = SnakeGame()
    game.food.position = (game.snake.body[0][0] + 1, game.snake.body[0][1])
    game.snake.direction = (1, 0)
    game.update()
    assert len(game.snake.body) == 2
    assert game.score == 1

def test_snake_does_not_grow_without_food():
    game = SnakeGame()
    game.food.position = (0, 0)
    game.update()
    assert len(game.snake.body) == 1

def test_snake_hits_wall():
    game = SnakeGame()
    game.snake.body = [(0, 0)]
    game.snake.direction = (-1, 0)
    game.update()
    assert not game.alive

def test_snake_self_collision():
    game = SnakeGame()
    game.snake.body = [(5,5), (5,6), (6,6), (6,5), (5,5)]
    game.update()
    assert not game.alive

def test_reset_game():
    game = SnakeGame()
    game.snake.body = [(0, 0)]
    game.snake.direction = (-1, 0)
    game.update()
    game.reset()
    assert game.snake.get_head() == (GRID_WIDTH // 2, GRID_HEIGHT // 2)
    assert game.score == 0
    assert game.alive

def test_change_to_opposite_direction_ignored():
    game = SnakeGame()
    game.snake.direction = (-1, 0)
    game.change_direction((1, 0))  # Opposite
    assert game.snake.direction == (-1, 0)

def test_multiple_updates_move_snake():
    game = SnakeGame()
    initial = game.snake.body[0]
    for _ in range(5):
        game.update()
    assert game.snake.body[0] != initial

def test_snake_length_increases_properly():
    game = SnakeGame()
    game.food.position = (game.snake.body[0][0] + 1, game.snake.body[0][1])
    game.snake.direction = (1, 0)
    game.update()
    game.food.position = (game.snake.body[0][0] + 1, game.snake.body[0][1])
    game.update()
    assert len(game.snake.body) == 3

def test_food_respawn_not_on_snake():
    game = SnakeGame()
    game.snake.body = [(x, 0) for x in range(GRID_WIDTH)]
    game.food.relocate(game.snake.body)
    assert game.food.position not in game.snake.body

def test_snake_stops_when_dead():
    game = SnakeGame()
    game.alive = False
    before = list(game.snake.body)
    game.update()
    assert game.snake.body == before

def test_food_eaten_updates_score():
    game = SnakeGame()
    game.food.position = (game.snake.body[0][0] + 1, game.snake.body[0][1])
    game.snake.direction = (1, 0)
    game.update()
    assert game.score == 1

def test_snake_direction_logic():
    game = SnakeGame()
    game.change_direction((0, -1))  # UP
    assert game.snake.direction == (0, -1)
    game.change_direction((0, 1))   # DOWN
    assert game.snake.direction == (0, -1)
    game.change_direction((-1, 0))  # LEFT
    assert game.snake.direction == (-1, 0)
    game.change_direction((1, 0))   # RIGHT
    assert game.snake.direction == (-1, 0)

def test_snake_hits_top_wall():
    game = SnakeGame()
    game.snake.body = [(5, 0)]
    game.snake.direction = (0, -1)
    game.update()
    assert not game.alive

def test_snake_starts_with_one_segment():
    game = SnakeGame()
    assert len(game.snake.body) == 1
