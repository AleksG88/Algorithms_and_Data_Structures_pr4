"""Модуль с классом пули, которой стреляет корабль."""

import pygame

BULLET_SPEED = 8
BULLET_LIFETIME = 60
BULLET_RADIUS = 2
BULLET_COLOR = (255, 220, 80)


class Bullet:
    """Пуля: летит прямо и исчезает через BULLET_LIFETIME кадров."""

    def __init__(self, position: pygame.Vector2, direction: pygame.Vector2) -> None:
        """Создаёт пулю в точке position, летящую в сторону direction."""
        self.position = pygame.Vector2(position)
        self.velocity = direction * BULLET_SPEED
        self.life = BULLET_LIFETIME

    @property
    def alive(self) -> bool:
        """True, пока пуля ещё летит."""
        return self.life > 0

    def move(self, width: int, height: int) -> None:
        """Сдвигает пулю и уменьшает оставшуюся жизнь. За краем поля width на height пуля погибает."""
        self.position += self.velocity
        self.life -= 1
        if not (0 <= self.position.x < width and 0 <= self.position.y < height):
            self.life = 0

    def draw(self, screen: pygame.Surface) -> None:
        """Рисует пулю на экране screen."""
        pygame.draw.circle(screen, BULLET_COLOR, self.position, BULLET_RADIUS)
