"""Модуль с классом шара-астероида."""

import math

import pygame


class Ball:
    """Шар, который летает по полю и отскакивает от стенок и других шаров."""

    def __init__(self, position: pygame.Vector2, velocity: pygame.Vector2, radius: float) -> None:
        """Создаёт шар с центром position, скоростью velocity и радиусом radius."""
        self.position = position
        self.velocity = velocity
        self.radius = radius

    @property
    def mass(self) -> float:
        """Масса шара, равная его площади."""
        return math.pi * self.radius ** 2

    def move(self) -> None:
        """Сдвигает шар на один кадр по его скорости."""
        self.position += self.velocity

    def bounce_walls(self, width: int, height: int) -> None:
        """Не даёт шару выйти за поле размером width на height и отражает его от стенок."""
        if self.position.x - self.radius < 0:
            self.position.x = self.radius
            self.velocity.x = abs(self.velocity.x)
        elif self.position.x + self.radius > width:
            self.position.x = width - self.radius
            self.velocity.x = -abs(self.velocity.x)
        if self.position.y - self.radius < 0:
            self.position.y = self.radius
            self.velocity.y = abs(self.velocity.y)
        elif self.position.y + self.radius > height:
            self.position.y = height - self.radius
            self.velocity.y = -abs(self.velocity.y)

    def collide(self, other: "Ball") -> None:
        """Обрабатывает упругое столкновение с шаром other, если шары касаются."""
        delta = other.position - self.position
        distance = delta.length()
        if distance == 0 or distance > self.radius + other.radius:
            return
        normal = delta / distance
        speed = (self.velocity - other.velocity).dot(normal)
        if speed <= 0:
            return
        total_mass = self.mass + other.mass
        impulse = 2 * speed / total_mass
        self.velocity -= impulse * other.mass * normal
        other.velocity += impulse * self.mass * normal
        overlap = self.radius + other.radius - distance
        self.position -= normal * overlap * other.mass / total_mass
        other.position += normal * overlap * self.mass / total_mass

    def draw(self, screen: pygame.Surface) -> None:
        """Рисует шар на экране screen."""
        pygame.draw.circle(screen, (255, 255, 255), self.position, self.radius)
