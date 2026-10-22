"""Главный модуль: запуск игры."""

import random

import pygame

from game.ball import Ball
from game.tree import QuadTree, Rect

WIDTH = 800
HEIGHT = 600
BACKGROUND = (0, 0, 0)
TREE_COLOR = (0, 110, 0)
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


def build_tree(balls: list[Ball]) -> QuadTree:
    """Строит квадродерево по текущим позициям шаров."""
    tree = QuadTree(Rect(0, 0, WIDTH, HEIGHT))
    for ball in balls:
        tree.insert(ball)
    return tree


def handle_collisions(balls: list[Ball], tree: QuadTree) -> None:
    """Сталкивает каждый шар с соседями, найденными через квадродерево."""
    for ball in balls:
        reach = ball.radius + MAX_RADIUS
        area = Rect(ball.position.x - reach, ball.position.y - reach, 2 * reach, 2 * reach)
        for other in tree.query(area):
            if other is not ball:
                ball.collide(other)


def draw_tree(screen: pygame.Surface, tree: QuadTree) -> None:
    """Рисует границы всех узлов квадродерева."""
    for rect in tree.boundaries():
        pygame.draw.rect(screen, TREE_COLOR, (rect.x, rect.y, rect.width, rect.height), 1)


def main() -> None:
    """Открывает окно и крутит главный цикл игры."""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Asteroids")
    clock = pygame.time.Clock()

    balls = []
    for _ in range(BALL_COUNT):
        balls.append(create_random_ball())

    show_tree = True
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_t:
                show_tree = not show_tree
        for ball in balls:
            ball.move()
        tree = build_tree(balls)
        handle_collisions(balls, tree)
        for ball in balls:
            ball.bounce_walls(WIDTH, HEIGHT)
        screen.fill(BACKGROUND)
        if show_tree:
            draw_tree(screen, tree)
        for ball in balls:
            ball.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
