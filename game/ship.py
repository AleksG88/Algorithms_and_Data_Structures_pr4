"""Модуль с классом космического корабля игрока."""

import pygame

from game.bullet import Bullet

SHIP_SIZE = 30
TURN_SPEED = 2
THRUST_POWER = 0.15
FRICTION = 0.99
BRAKE = 0.9
FIRE_DELAY = 20
SHIP_COLOR = (255, 0, 0)


class Ship:
    """Корабль-треугольник, которым управляет игрок."""

    def __init__(self, position: pygame.Vector2) -> None:
        """Создаёт неподвижный корабль в точке position, нос смотрит вверх."""
        self.position = position
        self.velocity = pygame.Vector2(0, 0)
        self.angle = -90.0
        self.cooldown = 0

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

    def brake(self) -> None:
        """Быстро гасит скорость корабля."""
        self.velocity *= BRAKE

    def shoot(self) -> Bullet | None:
        """Стреляет из носа корабля. Возвращает новую пулю или None, если идёт перезарядка."""
        if self.cooldown > 0:
            return None
        self.cooldown = FIRE_DELAY
        return Bullet(self.points()[0], self.direction)

    def move(self, width: int, height: int) -> None:
        """Сдвигает корабль, гасит скорость трением и переносит через края поля."""
        self.position += self.velocity
        self.velocity *= FRICTION
        self.position.x %= width
        self.position.y %= height
        if self.cooldown > 0:
            self.cooldown -= 1

    def points(self) -> list[pygame.Vector2]:
        """Три вершины треугольника: нос и два задних угла."""
        nose = self.position + self.direction * SHIP_SIZE
        left = self.position + self.direction.rotate(140) * SHIP_SIZE
        right = self.position + self.direction.rotate(-140) * SHIP_SIZE
        return [nose, left, right]

    def draw(self, screen: pygame.Surface) -> None:
        """Рисует корабль на экране screen."""
        pygame.draw.polygon(screen, SHIP_COLOR, self.points())
