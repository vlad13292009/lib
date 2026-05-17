from itertools import product, permutations


def _solve(func_body, var_order, known_frags, find_val=0):
    local_scope = {}
    exec(func_body, local_scope)
    F = local_scope["F"]

    variables = list(var_order)
    n = len(variables)
    zero_rows = []

    for values in product([0, 1], repeat=n):
        row = dict(zip(variables, values))
        if F(*row.values()) == find_val:
            zero_rows.append(row)

    def fits(partial, full):
        for col, val in partial.items():
            if full[col] != val:
                return False
        return True

    def match(table_rows, known, idx=0, used=None):
        if used is None:
            used = set()
        if idx == len(known):
            return True
        for i, row in enumerate(table_rows):
            if i in used:
                continue
            if fits(known[idx], row):
                if match(table_rows, known, idx + 1, used | {i}):
                    return True
        return False

    for perm in permutations(variables):
        table_rows = [tuple(row[v] for v in perm) for row in zero_rows]
        if match(table_rows, known_frags):
            return "".join(perm).lower()

    return None


def solve_logic_table(func_body=None, var_order=None, known_frags=None, find_val=0):
    if func_body is not None and var_order is not None and known_frags is not None:
        return _solve(func_body, var_order, known_frags, find_val)

    header = (
        "╔══════════════════════════════════════════════════════════╗\n"
        "║        Задание 2 — логические таблицы истинности        ║\n"
        "║   Алгоритм: перебор + рекурсивное сопоставление строк   ║\n"
        "╚══════════════════════════════════════════════════════════╝"
    )
    print(header)
    print()

    print("┌─ ШАГ 1: определите функцию F ──────────────────────┐")
    print("│                                                    │")
    print("│  Логические операции:                              │")
    print("│    and — И (∧)      or — ИЛИ (∨)    not — НЕ (¬)  │")
    print("│    == — эквиваленция (≡)    != — XOR (⊕)           │")
    print("│    (not A) or B — импликация (→)                   │")
    print("│                                                    │")
    print("│  Пример:                                           │")
    print("│    def F(x, y, z, w):                              │")
    print("│        return (z == w) and (not x or y) or not w   │")
    print("│                                                    │")
    print("└────────────────────────────────────────────────────┘")
    print()

    lines = []
    for i in range(10):
        inp = input(f"  {'>' if i == 0 else '>'} ").strip()
        lines.append(inp)
        if inp.startswith("return") and (i == 0 or len(lines) >= 2):
            break
        if "return" in inp and i >= 1:
            break
        if inp == "":
            break

    func_body = "\n".join(lines)
    if not func_body.strip().startswith("def "):
        func_body = "def F(x, y, z, w):\n    " + func_body.replace("\n", "\n    ")

    local_scope = {}
    try:
        exec(func_body, local_scope)
        fn = local_scope.get("F")
        if fn is None:
            print("\n  ! Ошибка: функция F не найдена.")
            return None
    except Exception as e:
        print(f"\n  ! Ошибка в функции: {e}")
        return None

    print()

    print("┌─ ШАГ 2: переменные ───────────────────────────────┐")
    print("│                                                    │")
    print("│  Введите буквы переменных через пробел.            │")
    print("│  Enter = x y z w                                   │")
    print("│                                                    │")
    print("└────────────────────────────────────────────────────┘")
    var_input = input("  > ").strip()
    var_order = var_input.split() if var_input else ["x", "y", "z", "w"]
    print()

    print("┌─ ШАГ 3: какие строки ищем? ───────────────────────┐")
    print("│                                                    │")
    print("│  0 — строки, где F = 0 (по умолчанию)             │")
    print("│  1 — строки, где F = 1                            │")
    print("│                                                    │")
    print("└────────────────────────────────────────────────────┘")
    target = input("  > ").strip()
    find_val = int(target) if target in ("0", "1") else 0
    print()

    print("┌─ ШАГ 4: известные фрагменты таблицы ──────────────┐")
    print("│                                                    │")
    print("│  Формат: номер_столбца=значение через пробел       │")
    print("│                                                    │")
    print("│  Пример: 1=0 2=1 3=0                              │")
    print("│  Это значит: в столбце 1 стоит 0,                  │")
    print("│  в столбце 2 стоит 1, в столбце 3 стоит 0.        │")
    print("│                                                    │")
    print("│  Пустая строка = закончить ввод.                   │")
    print("│                                                    │")
    print("└────────────────────────────────────────────────────┘")
    print()

    known_frags = []
    n = 1
    while True:
        inp = input(f"  Строка {n}: ").strip()
        if not inp:
            break
        frag = {}
        for part in inp.split():
            if "=" in part:
                col, val = part.split("=", 1)
                frag[int(col.strip())] = int(val.strip())
        if frag:
            known_frags.append(frag)
            n += 1

    if not known_frags:
        print("\n  ! Нет данных для поиска.")
        return None

    print()
    print("  ┌── Поиск решения ────┐")
    result = _solve(func_body, var_order, known_frags, find_val)
    print("  └─────────────────────┘")
    print()

    if result:
        print(f"  ╔══════════════════════════════╗")
        print(f"  ║   Ответ: {result.upper():<20}║")
        print(f"  ║   {result:<28}║")
        print(f"  ╚══════════════════════════════╝")
    else:
        print("  ┌──────────────────────────────┐")
        print("  │  Решение не найдено          │")
        print("  │  Проверьте введённые данные   │")
        print("  └──────────────────────────────┘")

    return result


if __name__ == "__main__":
    solve_logic_table()
