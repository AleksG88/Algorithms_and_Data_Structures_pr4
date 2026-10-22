"""Главный модуль: запуск игры."""

# Часть pygame написана на C, и pylint не видит её содержимое.
# Это ложные срабатывания no-member, поэтому отключаем именно эту проверку в этом файле.
# pylint: disable=no-member

import random

import pygame

from game.ball import Ball
from game.bullet import Bullet
from game.settings import Settings, ask_settings
from game.ship import Ship
from game.tree import QuadTree, Rect

BACKGROUND = (0, 0, 0)
TREE_COLOR = (0, 110, 0)
TEXT_COLOR = (255, 255, 255)
FPS = 60
RESTART_DELAY = 5 * FPS


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


def handle_hits(bullets: list[Bullet], balls: list[Ball], tree: QuadTree, max_radius: float) -> None:
    """Ищет через квадродерево астероиды, в которые попали пули, и уничтожает их."""
    for bullet in bullets:
        area = Rect(bullet.position.x - max_radius, bullet.position.y - max_radius, 2 * max_radius, 2 * max_radius)
        for ball in tree.query(area):
            if bullet.position.distance_to(ball.position) <= ball.radius:
                tree.remove(ball)
                balls.remove(ball)
                bullet.life = 0
                break


def handle_ship_hits(ship: Ship, balls: list[Ball], tree: QuadTree, max_radius: float) -> None:
    """Ищет через квадродерево астероиды, врезавшиеся в корабль: каждый отнимает жизнь и разрушается."""
    if ship.is_invulnerable:
        return
    reach = ship.radius + max_radius
    area = Rect(ship.position.x - reach, ship.position.y - reach, 2 * reach, 2 * reach)
    for ball in tree.query(area):
        if ship.position.distance_to(ball.position) <= ball.radius + ship.radius:
            tree.remove(ball)
            balls.remove(ball)
            ship.lives -= 1


def draw_tree(screen: pygame.Surface, tree: QuadTree) -> None:
    """Рисует границы всех узлов квадродерева."""
    for rect in tree.boundaries():
        pygame.draw.rect(screen, TREE_COLOR, (rect.x, rect.y, rect.width, rect.height), 1)


def control_ship(ship: Ship, bullets: list[Bullet]) -> None:
    """Управляет кораблём по зажатым клавишам: стрелки или WASD, пробел — огонь."""
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        ship.rotate(-1)
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        ship.rotate(1)
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        ship.thrust()
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        ship.brake()
    if keys[pygame.K_SPACE]:
        bullet = ship.shoot()
        if bullet is not None:
            bullets.append(bullet)


def update_world(ship: Ship, balls: list[Ball], bullets: list[Bullet], settings: Settings) -> QuadTree:
    """Делает один шаг игры: движение, попадания, удары по кораблю, столкновения. Возвращает дерево."""
    control_ship(ship, bullets)
    ship.move(settings.width, settings.height)
    for bullet in bullets:
        bullet.move(settings.width, settings.height)
    for ball in balls:
        ball.move()
    tree = build_tree(balls, settings)
    handle_hits(bullets, balls, tree, settings.max_radius)
    handle_ship_hits(ship, balls, tree, settings.max_radius)
    bullets[:] = [bullet for bullet in bullets if bullet.alive]
    handle_collisions(balls, tree, settings.max_radius)
    for ball in balls:
        ball.bounce_walls(settings.width, settings.height)
    return tree


def draw_objects(screen: pygame.Surface, balls: list[Ball], bullets: list[Bullet], ship: Ship) -> None:
    """Рисует астероиды, пули и корабль."""
    for ball in balls:
        ball.draw(screen)
    for bullet in bullets:
        bullet.draw(screen)
    ship.draw(screen)


def new_round(settings: Settings) -> tuple[list[Ball], Ship, list[Bullet]]:
    """Начинает игру заново: новые астероиды, корабль в центре и пустой список пуль."""
    balls = []
    for _ in range(settings.ball_count):
        balls.append(create_random_ball(settings))
    ship = Ship(pygame.Vector2(settings.width / 2, settings.height / 2))
    return balls, ship, []


def draw_hud(screen: pygame.Surface, font: pygame.font.Font, lives: int) -> None:
    """Пишет число жизней в углу, а когда жизни кончились — надпись о проигрыше по центру."""
    screen.blit(font.render(f"Жизни: {max(lives, 0)}", True, TEXT_COLOR), (10, 10))
    if lives <= 0:
        text = font.render("ВЫ ПРОИГРАЛИ", True, TEXT_COLOR)
        screen.blit(text, text.get_rect(center=screen.get_rect().center))


def main() -> None:
    """Спрашивает настройки, открывает окно и крутит главный цикл игры."""
    settings = ask_settings()
    if settings is None:
        return
    pygame.init()
    screen = pygame.display.set_mode((settings.width, settings.height))
    pygame.display.set_caption("Asteroids")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 32)

    balls, ship, bullets = new_round(settings)
    tree = build_tree(balls, settings)
    game_over_frames = 0

    show_tree = True
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_t:
                show_tree = not show_tree
        if ship.lives > 0:
            tree = update_world(ship, balls, bullets, settings)
        else:
            game_over_frames += 1
            if game_over_frames >= RESTART_DELAY:
                balls, ship, bullets = new_round(settings)
                game_over_frames = 0
        screen.fill(BACKGROUND)
        if show_tree:
            draw_tree(screen, tree)
        draw_objects(screen, balls, bullets, ship)
        draw_hud(screen, font, ship.lives)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
