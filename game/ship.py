"""Модуль с классом космического корабля игрока."""

import pygame

SHIP_SIZE = 15
TURN_SPEED = 4
THRUST_POWER = 0.15
FRICTION = 0.99
SHIP_COLOR = (80, 200, 255)


class Ship:
    """Корабль-треугольник, которым управляет игрок."""

    def __init__(self, position: pygame.Vector2) -> None:
        """Создаёт неподвижный корабль в точке position, нос смотрит вверх."""
        self.position = position
        self.velocity = pygame.Vector2(0, 0)
        self.angle = -90.0

    @property
    def direction(self) -> pygame.Vector2:
        """Стрелка длиной 1, показывающая, куда смотрит нос."""
        return pygame.Vector2(1, 0).rotate(self.angle)

    def rotate(self, side: int) -> None:
        """Поворачивает корабль: side = -1 влево, 1 вправо."""
        self.angle += TURN_SPEED * side

    def thrust(self) -> None:
        """Разгоняет корабль в сторону носа."""
        self.velocity += self.direction * THRUST_POWER

    def move(self, width: int, height: int) -> None:
        """Сдвигает корабль, гасит скорость трением и переносит через края поля."""
        self.position += self.velocity
        self.velocity *= FRICTION
        self.position.x %= width
        self.position.y %= height

    def points(self) -> list[pygame.Vector2]:
        """Три вершины треугольника: нос и два задних угла."""
        nose = self.position + self.direction * SHIP_SIZE
        left = self.position + self.direction.rotate(140) * SHIP_SIZE
        right = self.position + self.direction.rotate(-140) * SHIP_SIZE
        return [nose, left, right]

    def draw(self, screen: pygame.Surface) -> None:
        """Рисует корабль на экране screen."""
        pygame.draw.polygon(screen, SHIP_COLOR, self.points(), 2)
