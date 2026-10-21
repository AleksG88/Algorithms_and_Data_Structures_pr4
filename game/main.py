"""Главный модуль: запуск игры"""

import pygame
from game.ball import Ball

WIDTH = 800
HEIGHT = 600
BACKGROUND = (0, 0, 0)
FPS = 60


def main() -> None:
    """Открывает окно и крутит главный цикл игры."""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Asteroids")
    clock = pygame.time.Clock()

    ball = Ball(pygame.Vector2(400, 300), pygame.Vector2(3, 2), 20)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        ball.move()
        ball.bounce_walls(WIDTH, HEIGHT)
        screen.fill(BACKGROUND)
        ball.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
