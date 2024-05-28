import copy
import re
from typing import Any
import os

import pandas as pd
import datetime

from common import ROOT_DIR
from schedule_parser.class_num_validator import validate_class_num
from schedule_parser.execution_function import calculate_execution_time
from schedule_parser.preprocessing import preprocessing
from schedule_parser.sql import *


def shorten_address(address: str) -> str:
    """
    Функция укорачивания адресов пар.
    :param address: Изначальный адрес.
    :return: Максимально сокращенный адрес.
    """
    return address.replace(
        'Севастопольская', 'Сев-ая.').replace(
        'Вернадского', 'Верн').replace(
        'Студенческая', 'Студ-ая.').replace(
        'спорт зал', 'с.з.').replace(
        'спортзал', 'с.з.').replace(
        'читальный зал', 'чит.з.').replace(
        'Ялтинская', 'Ялт-ая.').replace(
        'ауд. Манеж', 'Манеж').replace(
        'Киевская', 'Киев.').replace(
        'Аграрное', 'Агр-е.').replace(
        'аудитория', 'а. ').replace(
        'ауд.', 'а. ').replace(
        'пр.', '').replace(
        '  ', ' ')


def normalize_name(bad_name: str) -> str:
    """
    Нормалайзер имен преподавателей. Из любого формата приводит в формат: Иванов И.И.
    :param bad_name: Ненормализованное имя.
    :return: Нормализованное имя.
    """
    normalized_name = ''
    for i in range(len(bad_name)):

        if bad_name[i].isupper() and i != 0:
            normalized_name += ' ' + bad_name[i]
        else:
            normalized_name += bad_name[i]
    return normalized_name


def _out_red(text) -> None:
    """
    :param text: Любая строка
    :return: Вывод в консоль красного жирного текста
    """
    print('\033[91m' + text + '\033[0m')


groups_list = []
teachers_schedule = {}


def get_group_list() -> list[str]:
    """
    Затычка ради удобства.
    :return: Возвращает список академических групп.
    """
    return groups_list


def is_number(s):
    try:
        # Пробуем преобразовать строку в int
        int(s)
        return True
    except ValueError:
        # Если не удалось, пробуем преобразовать в float
        try:
            float(s)
            return True
        except ValueError:
            # Если и это не удалось, значит строка не является ни int, ни float
            return False




@calculate_execution_time
def schedule_handler() -> tuple[dict[str, list[list[list[str | Any]]]], dict[str, Any]]:
    """
    Я отказываюсь комментировать что тут происходит. Просто это какой-то насраный пиздец, но оно работает.
    \nОно парсит сами расписания с файлов и выдает их уже в причесанном виде.
    \n# TODO Хорошо бы было вернуть объект вместо той жести, которая есть сейчас.
    :return: Расписание по группам, расписание по преподавателям
    """
    # Создаем словарь для расписания по группам
    schedule_by_groups = {}

    # Создаем файл для логов расписания по преподам
    log_folder = f"{ROOT_DIR}/logs"

    log_file_name = datetime.datetime.now().strftime("%Y-%m-%d_%Hh-%Mm") + ".txt"
    log_file_path = os.path.join(log_folder, log_file_name)

    # Паттерн для распознания ФИО преподавателя
    teacher_name_pattern = re.compile(r'[А-Я][а-я]+[А-Яа-я].?[А-Яа-я].?')

    with (open(log_file_path, "w") as log_file):
        # Вытаскиваем инфу о файле. (путь, имена листов в нем, группы)
        file_info = preprocessing()
        for dat in file_info:
            df = pd.read_excel(f'{ROOT_DIR}/schedule/{dat[0]}', sheet_name=dat[1][0])
            for group in dat[1][1]:
                gr = (str(group).replace(' ', '') + ' ' + str(dat[1][0])).strip().replace(
                    ' ', '_').replace(
                    'Подгруппа', '').replace(
                    'группа', '')
                groups_list.append(gr) if gr not in groups_list else 0
                try:
                    log_file.write(
                        f'рассматриваю {dat[0]} {dat[1][0]} {group}-------------------------------------------\n')
                    result = []
                    # Парсим все данные с листа с заполнением NaN соседним значением
                    df = df.ffill(axis=1, limit=1, )
                    list_cols = df.columns.tolist()

                    for column in list_cols:
                        result.append(df[column].to_string().replace('NaN', '   ').split('\n'))

                    result1 = [[cell[3:].strip() for cell in column] for column in result]

                    class_number, class_type, schedule = [], [], []
                    class_number_last, class_type_last = [], []
                    days_in_week = []
                    for res in result1:
                        if re.search(r'\bпара\b', ' '.join(res)):
                            class_number_last = res
                        if "вид занятий" in ''.join(res).lower():
                            class_type_last = res
                        if "дни недели" in ''.join(res).lower():
                            days_in_week_hat = res
                            days_in_week_hat.pop(0)
                            days_in_week_hat.pop(0)
                            days_in_week_hat.pop(0)
                            days_in_week = list(filter(bool, days_in_week_hat))

                        for cell in res:
                            if group.strip() == cell and "вид занятий" not in res:
                                schedule.append(res) if res not in schedule and len(''.join(res)) > 100 else 0
                                class_number.append(class_number_last) if class_number_last not in class_number else 0
                                class_type.append(class_type_last) if class_type_last not in class_type else 0
                    class_number = class_number[0]

                    #TODO-----------------------
                    if dat[0].startswith('06.03.01') and 'Б-б-о' in group:
                        class_number = validate_class_num(class_number)
                    #TODO-----------------------

                    for i in range(len(class_number)):
                        if str(class_number[0]) != '1':
                            class_number.pop(0)
                        else:
                            break

                    for i, row in enumerate(class_type):
                        class_type[i] = class_type[i][(-len(class_number)):]

                    for i, row in enumerate(schedule):
                        schedule[i] = schedule[i][(-len(class_number)):]

                    if len(schedule) > len(class_type):
                        while len(schedule) > len(class_type):
                            class_type = class_type * 2

                    schedule_by_days_hat = []
                    schedule_by_days = []
                    cur_day = -1
                    for i, row in enumerate(schedule):
                        for j, cell in enumerate(row):
                            # current_day = days_in_week[cur_day].replace('\\n', ' ').split(' ')[0]
                            # rest_of_current_day = ' '.join(days_in_week[cur_day].replace('/', ' ').split(' ')[1:])
                            try:
                                if class_number[j][:1] == '1':
                                    schedule_by_days.append(schedule_by_days_hat) if schedule_by_days_hat != [] else 0
                                    schedule_by_days_hat = []
                                    cur_day += 1
                                if cur_day == len(days_in_week):
                                    cur_day = -1

                                if class_number[j][:1] in ['1', '2', '3', '4', '5', '6', '7', '8']:
                                    schedule_by_days_hat.append([class_number[j][:1],
                                                                 class_type[i][j] if class_type[i][j][:1] not in ['1',
                                                                                                                  '2',
                                                                                                                  '3',
                                                                                                                  '4',
                                                                                                                  '5',
                                                                                                                  '6',
                                                                                                                  '7',
                                                                                                                  '8']
                                                                 else '',
                                                                 schedule[i][j],
                                                                 schedule[i][j + 1],
                                                                 schedule[i][j + 2],
                                                                 schedule[i][j + 3].replace(
                                                                     'даты проведения занятий', 'даты').replace(
                                                                     'дата проведения занятия', 'дата')
                                                                 ]
                                                                )
                            except:
                                pass
                    schedule_by_days.append(schedule_by_days_hat)
                    for day in schedule_by_days:
                        log_file.write(f'{day}\n')
                        schedule_by_groups[gr] = schedule_by_days

                except:
                    _out_red('FATAL ERROR in')
                    _out_red(f'{dat[0]} - {group}')
                    log_file.write(f'FATAL ERROR in {dat[0]} {dat[1][0]} {group}\n')
        for el in teachers_schedule:
            log_file.write(f'{el} {teachers_schedule[el]}\n')

        schedule_pattern = {
            'понедельник': {'1': '', '2': '', '3': '', '4': '', '5': '',
                            '6': '', '7': ''},
            'вторник': {'1': '', '2': '', '3': '', '4': '', '5': '',
                        '6': '', '7': ''},
            'среда': {'1': '', '2': '', '3': '', '4': '', '5': '', '6': '',
                      '7': ''},
            'четверг': {'1': '', '2': '', '3': '', '4': '', '5': '',
                        '6': '', '7': ''},
            'пятница': {'1': '', '2': '', '3': '', '4': '', '5': '',
                        '6': '', '7': ''},
            'суббота': {'1': '', '2': '', '3': '', '4': '', '5': '',
                        '6': '', '7': ''}
        }

        day_name = {
            0: "понедельник",
            1: "вторник",
            2: "среда",
            3: "четверг",
            4: "пятница",
            5: "суббота"
        }

        sql_teachers = get_teachers()

        for group in schedule_by_groups:

            schedule = schedule_by_groups[group]
            if len(schedule) <= 6:
                schedule = schedule * 2
            schedule = [schedule[:int(len(schedule) / 2)],
                        schedule[int(len(schedule) / 2):]]

            #  В случае, если в расписании более 2 недель, то делим еще раз каждый элемент на пополам
            if len(schedule[0]) > 6:
                schedule = [schedule[0][:int(len(schedule[0]) / 2)], schedule[0][int(len(schedule[0]) / 2):],
                            schedule[1][:int(len(schedule[1]) / 2)], schedule[1][int(len(schedule[1]) / 2):]]

            for week_num, week in enumerate(schedule):
                for day_num, day in enumerate(week):
                    for pare in day:

                        try:
                            pare_num = pare[0]
                            class_type = pare[1].upper()
                            class_name = pare[2]
                            teacher_name = normalize_name(teacher_name_pattern.findall(pare[3].replace(' ', ''))[0])
                            class_address = pare[4]
                            class_add_info = pare[5]
                            if teacher_name not in teachers_schedule and teacher_name != "":
                                teachers_schedule[teacher_name] = {'Нечетная неделя': copy.deepcopy(schedule_pattern),
                                                                   "Четная неделя": copy.deepcopy(schedule_pattern)}
                                if teacher_name not in sql_teachers:
                                    # Если препода нет в бд, то пихаем его туда
                                    insert_to_db(teacher_name, 0.0, 'NULL')

                            week_type = 'Нечетная неделя' if week_num % 2 == 0 else "Четная неделя"

                            if teacher_name != "":
                                teachers_schedule[teacher_name][week_type][day_name[day_num]][pare_num] = (
                                    f"{group.replace('_', ' ')}_"
                                    f"{class_type}_"
                                    f"{class_name}_"
                                    f"{class_address}_"
                                    f"{class_add_info}")
                        except Exception as ex:
                            # print(ex)
                            pass
        return schedule_by_groups, teachers_schedule
