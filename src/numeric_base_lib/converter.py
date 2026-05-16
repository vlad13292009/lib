DIGITS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def _int_to_base(n: int, base: int) -> str:
    if n == 0:
        return "0"
    result = ""
    while n > 0:
        result = DIGITS[n % base] + result
        n //= base
    return result


def float_to_base(float_num: float, base: int, precision: int = 10) -> str:
    if not (2 <= base <= 36):
        raise ValueError("Base must be between 2 and 36")
    if precision < 0:
        raise ValueError("Precision must be non-negative")

    sign = "-" if float_num < 0 else ""
    float_num = abs(float_num)

    int_part = int(float_num)
    frac_part = float_num - int_part

    int_string = _int_to_base(int_part, base)

    if frac_part == 0 or precision == 0:
        return sign + int_string

    frac_string = ""
    for _ in range(precision):
        frac_part *= base
        digit = int(frac_part)
        frac_string += DIGITS[digit]
        frac_part -= digit

    return sign + int_string + "." + frac_string
