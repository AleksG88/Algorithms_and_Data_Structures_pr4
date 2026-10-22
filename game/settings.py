"""Окно настроек симуляции, которое показывается перед запуском игры."""

import tkinter as tk
from dataclasses import dataclass
from tkinter import messagebox


@dataclass
class Settings:
    """Параметры симуляции, которые выбирает пользователь."""

    ball_count: int = 20
    min_radius: int = 10
    max_radius: int = 30
    min_speed: float = 1.0
    max_speed: float = 4.0
    width: int = 800
    height: int = 600

    def validate(self) -> str:
        """Проверяет настройки. Возвращает текст ошибки или пустую строку, если всё верно."""
        checks = [
            (1 <= self.ball_count <= 500, "Количество шаров: от 1 до 500."),
            (1 <= self.min_radius <= self.max_radius, "Радиус: нужно 1 ≤ минимальный ≤ максимальный."),
            (0 <= self.min_speed <= self.max_speed <= 15, "Скорость: нужно 0 ≤ минимальная ≤ максимальная ≤ 15."),
            (200 <= self.width <= 1600, "Ширина поля: от 200 до 1600."),
            (200 <= self.height <= 1000, "Высота поля: от 200 до 1000."),
            (2 * self.max_radius < min(self.width, self.height), "Шары не помещаются в поле: уменьшите радиус."),
        ]
        for is_ok, message in checks:
            if not is_ok:
                return message
        return ""


FIELDS = [
    ("ball_count", "Количество шаров"),
    ("min_radius", "Минимальный радиус"),
    ("max_radius", "Максимальный радиус"),
    ("min_speed", "Минимальная скорость"),
    ("max_speed", "Максимальная скорость"),
    ("width", "Ширина поля"),
    ("height", "Высота поля"),
]


def ask_settings() -> Settings | None:
    """Показывает окно настроек. Возвращает выбранные настройки или None, если окно закрыли."""
    root = tk.Tk()
    root.title("Asteroids: настройки")
    defaults = Settings()
    entries: dict[str, tk.Entry] = {}
    for row, (name, label) in enumerate(FIELDS):
        tk.Label(root, text=label).grid(row=row, column=0, sticky="w", padx=10, pady=4)
        entry = tk.Entry(root, width=10)
        entry.insert(0, str(getattr(defaults, name)))
        entry.grid(row=row, column=1, padx=10, pady=4)
        entries[name] = entry
    chosen: list[Settings] = []

    def start() -> None:
        """Читает поля, проверяет их и закрывает окно, если всё верно."""
        try:
            values = {name: type(getattr(defaults, name))(entries[name].get()) for name, _ in FIELDS}
        except ValueError:
            messagebox.showerror("Ошибка", "Во всех полях должны быть числа.")
            return
        settings = Settings(**values)
        error = settings.validate()
        if error:
            messagebox.showerror("Ошибка", error)
            return
        chosen.append(settings)
        root.destroy()

    tk.Button(root, text="Старт", width=15, command=start).grid(row=len(FIELDS), column=0, columnspan=2, pady=10)
    root.mainloop()
    return chosen[0] if chosen else None
