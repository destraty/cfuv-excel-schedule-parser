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


def restore_sequences(sequences):
    # Шаг индекса
    index_step = 7

    # Восстановленные последовательности
    restored_sequences = []

    # Перебираем все последовательности
    for i, sequence in enumerate(sequences):
        # Добавляем текущую последовательность в восстановленные
        restored_sequences.extend(sequence)

        # Если это не последняя последовательность
        if i < len(sequences) - 1:
            # Получаем последний индекс текущей последовательности
            last_index = sequence[-1][1]
            # Получаем первый индекс следующей последовательности
            next_index = sequences[i + 1][0][1]

            # Вычисляем разницу между индексами
            index_diff = next_index - last_index

            # Если разница больше шага индекса, добавляем недостающие элементы
            if index_diff > index_step:
                # Вычисляем значение и индекс для недостающего элемента
                missing_value = int(sequence[-1][0]) + 1
                missing_index = last_index + 5

                # Добавляем недостающие элементы
                while missing_index < next_index:
                    restored_sequences.append((str(missing_value), missing_index))
                    missing_value += 1
                    missing_index += index_step

    return restored_sequences


def restore_array_with_indices(arr):
    # Сначала определяем начальный индекс и шаг
    start_index = arr[0][1] - (int(arr[0][0]) - 1) * 5

    # Восстанавливаем полный массив
    restored_arr = [(str(i), start_index + (i - 1) * 5) for i in range(1, int(arr[-1][0]) + 1)]

    return restored_arr


# def restore_array_with_indices(arr):
#     # Восстанавливаем полный массив
#     restored_arr = [(str(i), arr[0][1] + (i - int(arr[0][0])) * 5) for i in range(int(arr[0][0]), int(arr[-1][0]) + 1)]
#     return restored_arr

def validate_class_num(arr):
    result = arr
    if not arr:
        return []
    subsequence = []
    last = 0
    ss = []
    for ind, item in enumerate(arr):

        if is_number(item):
            cur = item[:1]
            if int(cur) > last:
                ss.append((cur, ind))
            else:
                subsequence.append(ss)
                ss = [(cur, ind)]
                last = 0
                continue
            last = int(item[:1])
    subsequence.append(ss)
    res = []
    for seq in subsequence:
        res.append(restore_array_with_indices(seq))
    rest_seq = restore_sequences(res)
    ss_val = []
    for s in subsequence:
        for item in s:
            ss_val.append(item[0])
    for cort in rest_seq:
        result[cort[1]] = cort[0]
    return result
