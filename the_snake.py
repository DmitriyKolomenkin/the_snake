from random import choice, randint

import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
SCREEN_CENTER = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

DIRECRIONS = (UP, DOWN, LEFT, RIGHT)

BOARD_BACKGROUND_COLOR = (0, 0, 0)

BORDER_COLOR = (93, 216, 228)

APPLE_COLOR = (0, 255, 255)

SNAKE_COLOR = (0, 255, 0)

SPEED = 5

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

pygame.display.set_caption('Змейка')

clock = pygame.time.Clock()


class GameObject:
    """
    Родительский класс,
    необходимый для объеденения обьектов.
    """

    body_color = BOARD_BACKGROUND_COLOR

    def __init__(self, body_color=BORDER_COLOR):
        """Метод, необходимый для создания отрибутов."""
        self.position = SCREEN_CENTER
        self.body_color = body_color

    def draw(self, surface):
        """Отрисовка объектов."""
        pass


class Apple(GameObject):
    """Класс игрового объекта 'Apple'."""

    def __init__(self, body_color=APPLE_COLOR):
        """Наследуем некоторые атрибуты из родительского класса."""
        super().__init__(body_color)
        self.position = self.randomize_position()

    def randomize_position(self):
        """Находим случайную точку на сетке."""
        return (randint(1, GRID_WIDTH) * GRID_SIZE - GRID_SIZE,
                randint(1, GRID_HEIGHT) * GRID_SIZE - GRID_SIZE)

    def draw(self, surface):
        """Отрисовываем яблочко."""
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Дочерний класс для создания змейки."""

    def __init__(self, body_color=SNAKE_COLOR):
        """Змеиные атрибуты: начальное положение, цвет и длинна."""
        super().__init__(self)
        self.initialize_snake()
        self.body_color = body_color
        self.next_direction = None
        self.direction = RIGHT

    def update_direction(self):
        """Обновляем направление после нажатия клавишь."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод, который заставляет змейку 'двигаться' по сетке."""
        self.update_direction()
        x = self.direction[0] * GRID_SIZE
        y = self.direction[1] * GRID_SIZE
        position_x = (self.get_head_position()[0] + x) % SCREEN_WIDTH
        position_y = (self.get_head_position()[1] + y) % SCREEN_HEIGHT
        snake_head = (position_x, position_y)
        self.positions.insert(0, snake_head)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def draw(self, surface):
        """Метод для отрисовки змейки."""
        for position in self.positions[:-1]:
            rect = (
                pygame.Rect((position[0], position[1]),
                            (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)
            self.last = None

    def get_head_position(self):
        """Метод, с помощью которого нахожу координаты головы."""
        return self.positions[0]

    def reset(self):
        """Метод, для обновления игры."""
        self.initialize_snake()
        self.next_direction = choice(DIRECRIONS)
        screen.fill(BOARD_BACKGROUND_COLOR)

    def initialize_snake(self, body_color=SNAKE_COLOR):
        """Метод, хранящий атрибуты."""
        self.length = 1
        self.positions = [SCREEN_CENTER]
        self.last = None


def handle_keys(game_object):
    """Функция, которая считывает нажатия клавишь."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основная функция игры."""
    pygame.init()
    apple = Apple()
    snake = Snake()
    while True:
        """Цикл, обновляющий положения и отрисовку."""
        handle_keys(snake)

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.position = apple.randomize_position()

        if snake.get_head_position() in snake.positions[2:]:
            snake.reset()

        while apple.position in snake.positions:
            apple.position = apple.randomize_position()

        snake.move()
        apple.draw(screen)
        snake.draw(screen)

        pygame.display.update()
        clock.tick(SPEED)


if __name__ == '__main__':
    main()
