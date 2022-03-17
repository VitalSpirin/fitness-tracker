# Проект: Спринт 1. Программный модуль для фитнес-трекера.
import datetime as dt
from typing import Dict, Tuple, Union

WEIGHT: int = 75
HEIGHT: int = 175
FORMAT: str = "%H:%M:%S"
STEP_M: float = 0.65  # Длина шага в метрах.
K_1: float = 0.035  # Коэффициент для подсчета калорий.
K_2: float = 0.029  # Коэффициент для подсчета калорий.

Storage = Dict[str, int]
Package = Tuple[str, int]

storage_data: Storage = {}


def check_correct_data(data: Package) -> bool:
    """Проверить корректность полученного пакета."""
    return False if len(data) != 2 or None in data else True


def check_correct_time(time: dt.time) -> bool:
    """Проверить корректность параметра времени."""
    if storage_data is not None:
        for time_check in storage_data.keys():
            if dt.datetime.strptime(time_check, FORMAT).time() >= time:
                return False

    return True


def get_step_day(steps: int) -> int:
    """Получить количество пройденных шагов за этот день."""
    return sum(storage_data.values()) + steps


def get_distance(steps: int) -> float:
    """Получить дистанцию пройденного пути в км."""
    return steps * STEP_M / 1000


def get_spent_calories(dist: float, current_time: dt.time) -> float:
    """Получить значения потраченных калорий."""
    hour: float = current_time.hour + current_time.minute / 60
    minutes: int = current_time.hour * 60 + current_time.minute
    mean_speed: float = dist / hour

    spent_calories: float = (
        0.035 * WEIGHT + (mean_speed**2 / HEIGHT) * 0.029 * WEIGHT
    ) * minutes

    return spent_calories


def get_achievement(dist: float) -> str:
    """Получить поздравления за пройденную дистанцию."""
    if dist >= 6.5:
        return "Отличный результат! Цель достигнута."
    elif dist >= 3.9:
        return "Неплохо! День был продуктивным."
    elif dist >= 2:
        return "Маловато, но завтра наверстаем!"
    else:
        return "Лежать тоже полезно. Главное — участие, а не победа!"


def get_message(
    time: dt.time, steps: int, dist: float, calories: float, achievement: str
) -> str:
    """Получить сообщение с основными данными."""
    return (
        f"Время: {time}.\n"
        f"Количество шагов за сегодня: {steps}.\n"
        f"Дистанция составила {dist:.2f} км.\n"
        f"Вы сожгли {calories:.2f} ккал.\n"
        f"{achievement}\n"
    )


def accept_package(data: Package) -> Union[Storage, str]:
    """Обработать пакет данных."""
    if check_correct_data(data) is False:
        return "Некорректный пакет"

    time: str
    steps: int
    time, steps = data
    pack_time: dt.time = dt.datetime.strptime(time, FORMAT).time()

    if check_correct_time(pack_time) is False:
        return "Некорректное значение времени"

    day_steps: int = get_step_day(steps)

    dist: float = get_distance(steps) + get_distance(
        sum(storage_data.values())
    )

    spent_calories: float = get_spent_calories(dist, pack_time)
    achievement: str = get_achievement(dist)
    print(get_message(pack_time, day_steps, dist, spent_calories, achievement))
    storage_data.update({data})
    return storage_data


def main() -> None:
    package_0: Package = ("7:30:00", 3000)
    package_1: Package = ("12:00:00", 2500)
    package_2: Package = ("16:00:00", 2500)
    package_3: Package = ("18:00:00", 2000)

    accept_package(package_0)
    accept_package(package_1)
    accept_package(package_2)
    accept_package(package_3)


if __name__ == "__main__":
    main()
