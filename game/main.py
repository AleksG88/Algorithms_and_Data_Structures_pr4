"""Главный модуль: запуск игры"""

import pygame

WIDTH = 800
HEIGHT = 600
BACKGROUND = (0, 0, 0)


def main() -> None:
    """Откывает окно и крутит главный цикл игры."""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Asteroids")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill(BACKGROUND)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
