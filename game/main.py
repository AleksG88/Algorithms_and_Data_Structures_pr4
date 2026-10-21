"""Главный модуль: запуск игры."""

import random

import pygame

from game.ball import Ball

WIDTH = 800
HEIGHT = 600
BACKGROUND = (0, 0, 0)
FPS = 60
BALL_COUNT = 20
MIN_RADIUS = 10
MAX_RADIUS = 30
MAX_SPEED = 4


def create_random_ball() -> Ball:
    """Создаёт шар со случайными размером, позицией и скоростью."""
    radius = random.uniform(MIN_RADIUS, MAX_RADIUS)
    position = pygame.Vector2(random.uniform(radius, WIDTH - radius),
                              random.uniform(radius, HEIGHT - radius))
    velocity = pygame.Vector2(random.uniform(-MAX_SPEED, MAX_SPEED),
                              random.uniform(-MAX_SPEED, MAX_SPEED))
    return Ball(position, velocity, radius)


def main() -> None:
    """Открывает окно и крутит главный цикл игры."""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Asteroids")
    clock = pygame.time.Clock()

    balls = []
    for _ in range(BALL_COUNT):
        balls.append(create_random_ball())

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        for ball in balls:
            ball.move()
            ball.bounce_walls(WIDTH, HEIGHT)
        screen.fill(BACKGROUND)
        for ball in balls:
            ball.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
