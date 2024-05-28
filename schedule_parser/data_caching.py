import json
import os
from datetime import datetime, timedelta


def save_data_to_file(data: dict[str: dict] | list, filename: str) -> None:
    """
    Кеширование данных(расписание по преподавателям, расписание по группам, список групп).
    :param data: Любые данные для кэширования.
    :param filename: Имя файла для сохранения в формате пути.
    :return: NoReturn.
    """
    with open(filename, 'w') as file:
        json.dump(data, file)


def load_data_from_file(filename: str) -> dict[str: dict] | list:
    """
    Загрузка данных из файла с кэшем.
    :param filename: Путь к файлу.
    :return: Кэшированные данные.
    """
    with open(filename, 'r') as file:
        data = json.load(file)
    return data


def check_file_age(filename: str,
                   delay: int = 0) -> bool:
    """
    Проверяет, прошло ли н-ное количество часов с момента создания файла.
    :param delay: Кол-во часов, после которых файл считается устаревшим
    :param filename: Путь к файлу.
    :return: True | False.
    """
    if os.path.exists(filename):
        file_time = datetime.fromtimestamp(os.path.getmtime(filename))
        current_time = datetime.now()
        if current_time - file_time < timedelta(hours=delay):
            return True
        else:
            os.remove(filename)
            return False
    return False
