from itertools import product, permutations


# Логическая функция F = (x ∨ y ∨ w) ∧ ((¬y) ∨ z)
def F(x, y, z, w):
    # (z ≡ w) ∧ (x → y) ∨ ¬w
    # Эквивалентность (z ≡ w) заменяется на (z == w)
    # Импликация (x → y) заменяется на (not x or y)
    # ¬w заменяется на (not w)
    return int(x or (z and ((not y) or (w and (not z)))))


variables = 'xyzw'  # Переменные в исходном порядке
zero_rows = []  # Список для хранения всех наборов, где F=0

# Генерируем все возможные комбинации значений переменных (16 штук)
for values in product([0, 1], repeat=4):
    row = dict(zip(variables, values))  # Создаем словарь {x: val, y: val, z: val, w: val}
    # Если функция F равна 0 для этого набора, сохраняем его
    if F(row['x'], row['y'], row['z'], row['w']) == 0:
        zero_rows.append(row)

# Известные фрагменты строк из таблицы истинности
# Формат: {номер_столбца: значение, ...}
known = [
    {1:0, 2:1, 3:0},
    {3:1},
    {2:1},
    {2:1},
    {1:1, 2:1, 3:1},
]


def fits(partial_row, full_row):
    """
    Проверяет, согласуется ли частичная строка (из known) с полной строкой.
    partial_row: известные значения из таблицы {номер_столбца: значение}
    full_row: полный набор значений переменных
    """
    for column, value in partial_row.items():
        if full_row[column] != value:  # Если значение в столбце не совпадает
            return False
    return True


def can_match_all_rows(table_rows, known_rows, index=0, used=None):
    """
    Рекурсивная функция для проверки, можно ли сопоставить все известные строки
    со строками таблицы, где F=0.

    table_rows: список всех строк, где F=0 (для текущей перестановки переменных)
    known_rows: известные фрагменты из условия
    index: индекс текущей обрабатываемой строки из known_rows
    used: множество уже использованных строк из table_rows
    """
    if used is None:
        used = set()

    # Если все известные строки обработаны, нашли подходящую перестановку
    if index == len(known_rows):
        return True

    # Перебираем все строки таблицы, где F=0
    for i, row in enumerate(table_rows):
        if i in used:  # Пропускаем уже использованные строки
            continue

        # Проверяем, согласуется ли текущая строка с известным фрагментом
        if fits(known_rows[index], row):
            # Рекурсивно проверяем остальные строки
            if can_match_all_rows(table_rows, known_rows, index + 1, used | {i}):
                return True

    return False


# Перебираем все возможные перестановки переменных (24 варианта)
for order in permutations(variables):
    table_rows = []

    # Для каждой перестановки формируем таблицу строк, где F=0
    for row in zero_rows:
        # Создаем кортеж значений в порядке текущей перестановки
        table_rows.append(tuple(row[var] for var in order))

    # Проверяем, подходит ли эта перестановка под известные фрагменты
    if can_match_all_rows(table_rows, known):
        print(''.join(order))  # Выводим подходящую перестановку