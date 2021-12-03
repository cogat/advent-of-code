import typing as t

G = t.TypeVar("G")


def int_numbers(input_data: str) -> t.List[int]:
    return [int(num) for num in input_data.splitlines() if num.strip()]


def parse_lines(input_data: str, type_or_types: t.List = str, separator=" ") -> t.List:
    """
    Split each line by `separator` and put each token through the matching type_or_type function.
    """
    result = []
    for line in input_data.splitlines():
        tokens = line.split(separator)
        if len(tokens) == 1:
            result.append(type_or_types(tokens[0]))
        else:
            result.append([t(v) for t, v in zip(type_or_types, tokens)])
    return result


def first(i: t.Iterable[G]) -> G:
    """Goes boom if empty"""
    return next(iter(i))


def only(i: t.Iterable[G]) -> G:
    """Goes boom if len != 1"""
    consumed = list(i)
    if len(consumed) != 1:
        raise ValueError(f"i had {len(consumed)} values")
    return consumed[0]
