"""Главный модуль: запуск игры."""

# Часть pygame написана на C, и pylint не видит её содержимое.
# Это ложные срабатывания no-member, поэтому отключаем именно эту проверку в этом файле.
# pylint: disable=no-member

import random

import pygame

from game.ball import Ball
from game.settings import Settings, ask_settings
from game.ship import Ship
from game.tree import QuadTree, Rect

BACKGROUND = (0, 0, 0)
TREE_COLOR = (0, 110, 0)
FPS = 60


def create_random_ball(settings: Settings) -> Ball:
    """Создаёт шар со случайными размером, позицией, направлением и скоростью в пределах настроек."""
    radius = random.uniform(settings.min_radius, settings.max_radius)
    position = pygame.Vector2(random.uniform(radius, settings.width - radius),
                              random.uniform(radius, settings.height - radius))
    speed = random.uniform(settings.min_speed, settings.max_speed)
    velocity = pygame.Vector2(speed, 0).rotate(random.uniform(0, 360))
    return Ball(position, velocity, radius)


def build_tree(balls: list[Ball], settings: Settings) -> QuadTree:
    """Строит квадродерево по текущим позициям шаров."""
    tree = QuadTree(Rect(0, 0, settings.width, settings.height))
    for ball in balls:
        tree.insert(ball)
    return tree


def handle_collisions(balls: list[Ball], tree: QuadTree, max_radius: float) -> None:
    """Сталкивает каждый шар с соседями, найденными через квадродерево."""
    for ball in balls:
        reach = ball.radius + max_radius
        area = Rect(ball.position.x - reach, ball.position.y - reach, 2 * reach, 2 * reach)
        for other in tree.query(area):
            if other is not ball:
                ball.collide(other)


def draw_tree(screen: pygame.Surface, tree: QuadTree) -> None:
    """Рисует границы всех узлов квадродерева."""
    for rect in tree.boundaries():
        pygame.draw.rect(screen, TREE_COLOR, (rect.x, rect.y, rect.width, rect.height), 1)


def control_ship(ship: Ship) -> None:
    """Поворачивает и разгоняет корабль по зажатым стрелкам."""
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        ship.rotate(-1)
    if keys[pygame.K_RIGHT]:
        ship.rotate(1)
    if keys[pygame.K_UP]:
        ship.thrust()


def main() -> None:
    """Спрашивает настройки, открывает окно и крутит главный цикл игры."""
    settings = ask_settings()
    if settings is None:
        return
    pygame.init()
    screen = pygame.display.set_mode((settings.width, settings.height))
    pygame.display.set_caption("Asteroids")
    clock = pygame.time.Clock()

    balls = []
    for _ in range(settings.ball_count):
        balls.append(create_random_ball(settings))
    ship = Ship(pygame.Vector2(settings.width / 2, settings.height / 2))

    show_tree = True
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_t:
                show_tree = not show_tree
        control_ship(ship)
        ship.move(settings.width, settings.height)
        for ball in balls:
            ball.move()
        tree = build_tree(balls, settings)
        handle_collisions(balls, tree, settings.max_radius)
        for ball in balls:
            ball.bounce_walls(settings.width, settings.height)
        screen.fill(BACKGROUND)
        if show_tree:
            draw_tree(screen, tree)
        for ball in balls:
            ball.draw(screen)
        ship.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
