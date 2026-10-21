"""Модуль с классом шара-астероида."""

import pygame


class Ball:
    """Шар, который летает по полю и отскакивает от стенок."""

    def __init__(self, position: pygame.Vector2, velocity: pygame.Vector2, radius: float) -> None:
        """Создаёт шар с центром position, скоростью velocity и радиусом radius."""
        self.position = position
        self.velocity = velocity
        self.radius = radius

    def move(self) -> None:
        """Сдвигает шар на один кадр по его скорости."""
        self.position += self.velocity

    def bounce_walls(self, width: int, height: int) -> None:
        """Разворачивает скорость, если шар упёрся в край поля размером width на height."""
        if self.position.x - self.radius < 0 or self.position.x + self.radius > width:
            self.velocity.x = -self.velocity.x
        if self.position.y - self.radius < 0 or self.position.y + self.radius > height:
            self.velocity.y = -self.velocity.y

    def draw(self, screen: pygame.Surface) -> None:
        """Рисует шар на экране screen."""
        pygame.draw.circle(screen, (255, 255, 255), self.position, self.radius)
