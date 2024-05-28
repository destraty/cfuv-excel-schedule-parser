import sqlite3

from common import SQL_PATH

def get_teachers() -> list[str]:
    """Делает запрос к бд и возвращает list из строк с ФИО преподавателей"""
    conn = sqlite3.connect(SQL_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM t_rating")
    names = cursor.fetchall()
    conn.close()
    return [n[0] for n in names]


def insert_to_db(teacher: str, rating: float = 0.0, voters: str = "NULL") -> None:
    """
    Добавляет преподавателя в базу данных. Никаких проверок на отсутствие в базе данных не предусмотрено.
    :param teacher: ФИО преподавателя.
    :param rating: Начальный рейтинг. По умолчанию равен 0.0.
    :param voters: Список голосовавших. По умолчанию NULL.
    :return: None
    """
    conn = sqlite3.connect(SQL_PATH)
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO t_rating (name, rating, voters) VALUES (?, ?, ?)", (teacher, rating, voters))
    print(f'Добавлен новый препод {teacher}')
    conn.commit()
    conn.close()
