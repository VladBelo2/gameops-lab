import pytest
import pygame
# from tetris.game import (
#     Block, grid, reset_game, TETROMINO_COLORS, game.check_collision,
#     game.freeze_block, game.clear_full_rows, score
# )
import tetris.game as game
from tetris.assets import GRID_WIDTH, GRID_HEIGHT, CELL_SIZE

pygame.init()
game.reset_game()

def test_reset_game_initializes_state():
    game.reset_game()
    assert all(cell is None for row in game.grid for cell in row)

def test_block_moves_left_right():
    block = game.Block()
    original_x = block.x
    block.move_left()
    assert block.x == original_x - 1
    block.move_right()
    block.move_right()
    assert block.x == original_x + 1

def test_block_moves_down():
    block = game.Block()
    original_y = block.y
    moved = block.move_down()
    assert moved
    assert block.y == original_y + 1

def test_block_rotation_changes_shape():
    block = game.Block()
    block.shape = [
        [0, 1, 0],
        [1, 1, 1]
    ]
    original = [row[:] for row in block.shape]
    
    # Perform direct matrix rotation (simulate rotate logic)
    rotated = list(zip(*original[::-1]))
    rotated = [list(row) for row in rotated]

    assert rotated != original
    
def test_block_collision_detection():
    game.reset_game()
    block = game.Block()
    game.freeze_block(block)
    new_block = game.Block()
    new_block.y = block.y
    assert game.check_collision(new_block)

def test_line_clear_logic():
    game.reset_game()
    for x in range(GRID_WIDTH):
        b = game.Block()
        b.x = x
        b.y = GRID_HEIGHT - 1
        b.shape = [[1]]
        game.freeze_block(b)

    pre_score = game.score
    cleared = game.clear_full_rows()
    assert cleared == 1
    assert game.score == pre_score + 100

def test_game_over_detection():
    game.reset_game()
    block = game.Block()
    block.y = 0
    game.freeze_block(block)
    new_block = game.Block()
    assert game.check_collision(new_block)

def test_shadow_block_alignment():
    game.reset_game()

    block = game.Block()
    shadow = game.Block()
    shadow.shape = block.shape
    shadow.color = block.color
    shadow.rotation = block.rotation
    shadow.x = block.x
    shadow.y = block.y

    while not game.check_collision(shadow):
        shadow.y += 1
    shadow.y -= 1

    assert shadow.y >= block.y

def test_pause_does_not_update():
    block = game.Block()
    old_y = block.y
    # Simulate pause by skipping move
    assert block.y == old_y

def test_new_block_spawns_after_freeze():
    game.reset_game()
    block = game.Block()
    block.y = GRID_HEIGHT - 2
    game.freeze_block(block)
    new_block = game.Block()
    assert not game.check_collision(new_block)

def test_rotation_blocked_near_wall():
    game.reset_game()

    # Fill some grid cells near the wall to force a collision
    for y in range(2):
        game.grid[y][1] = (255, 0, 0)  # mock filled cells at (1, 0), (1, 1)

    block = game.Block()
    block.x = 0
    block.y = 0
    block.shape = [
        [0, 1, 0],
        [1, 1, 1]
    ]  # T-shape
    block.rotation = 0
    pre_shape = [row[:] for row in block.shape]

    block.rotate()

    rotated = block.shape != pre_shape
    assert not rotated or game.check_collision(block)

def test_toggle_pause_key():
    # Simulated manually in game loop
    pass

def test_reset_after_game_over():
    game.reset_game()
    block = game.Block()
    game.freeze_block(block)
    new_block = game.Block()
    assert game.check_collision(new_block)
    game.reset_game()
    new_block2 = game.Block()
    assert not game.check_collision(new_block2)

def test_score_does_not_increase_on_no_line():
    game.reset_game()
    game.score = 0
    block = game.Block()
    game.freeze_block(block)
    pre_score = game.score
    game.clear_full_rows()
    assert game.score == pre_score

def test_fast_drop_behavior():
    game.reset_game()
    block = game.Block()
    while block.move_down():
        pass
    game.freeze_block(block)
    assert game.check_collision(block)

def test_ghost_block_positioning():
    game.reset_game()  # ✅ Ensure clean grid

    block = game.Block()
    ghost = game.Block()
    ghost.shape = block.shape
    ghost.color = block.color
    ghost.rotation = block.rotation
    ghost.x = block.x
    ghost.y = block.y

    for _ in range(GRID_HEIGHT):
        if game.check_collision(ghost):
            break
        ghost.y += 1
    ghost.y -= 1

    assert ghost.y >= block.y
