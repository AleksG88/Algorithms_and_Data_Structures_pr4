"""Модуль с квадродеревом для быстрого поиска соседних объектов."""

from game.ball import Ball

MIN_NODE_SIZE = 4


class Rect:
    """Прямоугольник с левым верхним углом (x, y), шириной width и высотой height."""

    def __init__(self, x: float, y: float, width: float, height: float) -> None:
        """Запоминает положение и размеры прямоугольника."""
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def contains(self, x: float, y: float) -> bool:
        """Проверяет, лежит ли точка (x, y) внутри прямоугольника."""
        return (self.x <= x < self.x + self.width
                and self.y <= y < self.y + self.height)

    def intersects(self, other: "Rect") -> bool:
        """Проверяет, пересекается ли прямоугольник с другим прямоугольником other."""
        return not (other.x > self.x + self.width
                    or other.x + other.width < self.x
                    or other.y > self.y + self.height
                    or other.y + other.height < self.y)


class QuadTree:
    """Узел квадродерева: хранит шары своей области или делится на 4 дочерних узла."""

    def __init__(self, boundary: Rect, capacity: int = 4) -> None:
        """Создаёт пустой узел с областью boundary и вместимостью capacity."""
        self._boundary = boundary
        self._capacity = capacity
        self._balls: list[Ball] = []
        self._children: list["QuadTree"] = []

    @property
    def boundary(self) -> Rect:
        """Область поля, за которую отвечает узел."""
        return self._boundary

    @property
    def capacity(self) -> int:
        """Сколько шаров узел хранит, прежде чем разделиться."""
        return self._capacity

    @property
    def balls(self) -> list[Ball]:
        """Шары, которые лежат прямо в этом узле."""
        return self._balls

    @property
    def children(self) -> list["QuadTree"]:
        """Дочерние узлы; пустой список, если узел не делился."""
        return self._children

    @property
    def is_leaf(self) -> bool:
        """True, если узел — лист, то есть не делился на части."""
        return not self._children

    def subdivide(self) -> None:
        """Делит узел на четыре равные части."""
        x = self._boundary.x
        y = self._boundary.y
        half_w = self._boundary.width / 2
        half_h = self._boundary.height / 2
        self._children = [
            QuadTree(Rect(x, y, half_w, half_h), self._capacity),
            QuadTree(Rect(x + half_w, y, half_w, half_h), self._capacity),
            QuadTree(Rect(x, y + half_h, half_w, half_h), self._capacity),
            QuadTree(Rect(x + half_w, y + half_h, half_w, half_h), self._capacity),
        ]

    def insert(self, ball: Ball) -> bool:
        """Вставляет шар в дерево. Возвращает True, если центр шара попал в область узла."""
        if not self._boundary.contains(ball.position.x, ball.position.y):
            return False
        if self.is_leaf:
            if len(self._balls) < self._capacity or self._boundary.width < MIN_NODE_SIZE:
                self._balls.append(ball)
                return True
            self.subdivide()
            old_balls = self._balls
            self._balls = []
            for old_ball in old_balls:
                self._insert_into_children(old_ball)
        return self._insert_into_children(ball)

    def _insert_into_children(self, ball: Ball) -> bool:
        """Отдаёт шар тому дочернему узлу, в чью область он попадает."""
        for child in self._children:
            if child.insert(ball):
                return True
        return False

    def query(self, area: Rect) -> list[Ball]:
        """Возвращает все шары, центры которых лежат в прямоугольнике area."""
        found: list[Ball] = []
        if not self._boundary.intersects(area):
            return found
        for ball in self._balls:
            if area.contains(ball.position.x, ball.position.y):
                found.append(ball)
        for child in self._children:
            found.extend(child.query(area))
        return found

    def remove(self, ball: Ball) -> bool:
        """Удаляет шар из дерева. Возвращает True, если шар был найден и удалён."""
        if not self._boundary.contains(ball.position.x, ball.position.y):
            return False
        if ball in self._balls:
            self._balls.remove(ball)
            return True
        for child in self._children:
            if child.remove(ball):
                return True
        return False

    def boundaries(self) -> list[Rect]:
        """Возвращает границы этого узла и всех его потомков."""
        result = [self._boundary]
        for child in self._children:
            result.extend(child.boundaries())
        return result
