import itertools


INSTRUCTIONS = """
Решение задания 2 ЕГЭ по информатике (логические таблицы)

Как записывать логические операции на Python:
  ∧ (конъюнкция, И)           ->  and
  ∨ (дизъюнкция, ИЛИ)         ->  or
  ¬ (отрицание, НЕ)           ->  not
  → (импликация)              ->  (not A) or B   (или A <= B)
  ≡ (эквиваленция)            ->  ==
  ⊕ (исключающее ИЛИ, XOR)    ->  !=

Пример:
  (z == w) and (x <= y) or not z
"""


def _solve(
    expression: str,
    variables: list[str],
    table_data: list[list],
) -> str | None:
    for perm in itertools.permutations(variables):
        is_match = True

        for row in table_data:
            local_vars = {}

            for i, var_name in enumerate(perm):
                local_vars[var_name] = row[i]

            if any(v is None for v in local_vars.values()):
                continue

            try:
                res = eval(expression, {"__builtins__": None}, local_vars)
                res_int = 1 if res else 0

                table_f = row[-1]

                if table_f is not None and res_int != table_f:
                    is_match = False
                    break
            except Exception:
                is_match = False
                break

        if is_match:
            return "".join(perm).lower()

    return None


def solve_logic_table(
    expression: str | None = None,
    variables: list[str] | None = None,
    table_data: list[list] | None = None,
) -> str | None:
    if expression is not None and variables is not None and table_data is not None:
        return _solve(expression, variables, table_data)

    print(INSTRUCTIONS)
    print("-" * 60)

    expression = input("Введите логическое выражение: ").strip()

    vars_input = input("Введите переменные через пробел (например: x y z w): ").strip()
    variables = vars_input.split()

    print("Введите таблицу истинности. Формат: значения переменных и F через пробел.")
    print("Пустые ячейки обозначайте как 'None'. Пустая строка = конец ввода.")
    print("Пример строки: None None 0 0 0")
    table_data = []
    while True:
        line = input(f"Строка {len(table_data) + 1}: ").strip()
        if not line:
            break
        row = []
        for val in line.split():
            if val.lower() in ("none", "n", ""):
                row.append(None)
            else:
                row.append(int(val))
        table_data.append(row)

    result = _solve(expression, variables, table_data)

    print("-" * 60)
    if result:
        print(f"Ответ: {result}")
    else:
        print("Решение не найдено. Проверьте данные.")
    return result


if __name__ == "__main__":
    solve_logic_table()
