import random
from snake.assets import GRID_WIDTH, GRID_HEIGHT, UP, DOWN, LEFT, RIGHT

class Snake:
    def __init__(self):
        self.body = [(5, 5)]
        self.direction = RIGHT

    def move(self):
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)
        self.body.insert(0, new_head)
        self.body.pop()

    def grow(self):
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)
        self.body.insert(0, new_head)

    def change_direction(self, new_dir):
        if (self.direction[0] * -1, self.direction[1] * -1) != new_dir:
            self.direction = new_dir

    def get_head(self):
        return self.body[0]

    def collides_with_self(self):
        return self.body[0] in self.body[1:]

    def collides_with_wall(self):
        x, y = self.body[0]
        return not (0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT)


class Food:
    def __init__(self):
        self.position = self._random_position([])

    def relocate(self, snake_body):
        self.position = self._random_position(snake_body)

    def _random_position(self, snake_body):
        while True:
            pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if pos not in snake_body:
                return pos


class SnakeGame:
    def __init__(self):
        self.reset()

    def reset(self):
        self.snake = Snake()
        self.snake.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.snake.direction = (1, 0)
        self.food = Food()
        self.score = 0
        self.alive = True

    def update(self):
        if not self.alive:
            return
        self.snake.move()
        if self.snake.get_head() == self.food.position:
            self.snake.grow()
            self.food.relocate(self.snake.body)
            self.score += 10
        if self.snake.collides_with_self() or self.snake.collides_with_wall():
            self.alive = False

    def change_direction(self, new_dir):  # ← Add this
        self.snake.change_direction(new_dir)
