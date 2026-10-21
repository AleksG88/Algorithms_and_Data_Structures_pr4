"""Главный модуль: запуск игры"""

import pygame

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

    x = 400.0
    y = 300.0
    speed_x = 3.0
    speed_y = 2.0
    radius = 20
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        x += speed_x
        y += speed_y
        if x - radius < 0 or x + radius > WIDTH:
            speed_x = -speed_x
        if y - radius < 0 or y + radius > HEIGHT:
            speed_y = -speed_y
        screen.fill(BACKGROUND)
        pygame.draw.circle(screen, (255, 255, 255), (x, y), radius)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
