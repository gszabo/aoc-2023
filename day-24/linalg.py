from copy import deepcopy
from decimal import Decimal
from fractions import Fraction
from typing import TypeVar

T = TypeVar("T", Fraction, Decimal)


def solve_2x2(m: list[list[T]], b: list[T]) -> list[T]:
    assert len(m) == 2
    assert len(m[0]) == 2
    assert len(m[1]) == 2
    assert len(b) == 2

    det = m[0][0] * m[1][1] - m[0][1] * m[1][0]
    if det == 0:
        raise ValueError("Matrix is singular")

    x = (m[1][1] * b[0] - m[0][1] * b[1]) / det
    y = (m[0][0] * b[1] - m[1][0] * b[0]) / det

    return [x, y]


def solve_4x4(m: list[list[T]], b: list[T]) -> list[T]:
    m = deepcopy(m)
    b = deepcopy(b)

    assert len(m) == 4
    assert len(m[0]) == 4
    assert len(m[1]) == 4
    assert len(m[2]) == 4
    assert len(m[3]) == 4
    assert len(b) == 4

    def debug_print():
        for i in range(4):
            print(m[i][0], m[i][1], m[i][2], m[i][3], sep=" ", end=" | ")
            print(b[i])
        print()

    # Gaussian elimination
    # https://en.wikipedia.org/wiki/Gaussian_elimination

    # Generated by Github Copilot
    # TODO: Understand how and why this works

    # Forward elimination
    # debug_print()
    for i in range(3):
        for j in range(i + 1, 4):
            m[j][i] = m[j][i] / m[i][i]
            # debug_print()
            for k in range(i + 1, 4):
                m[j][k] = m[j][k] - m[j][i] * m[i][k]
                # debug_print()
            b[j] = b[j] - m[j][i] * b[i]
            # debug_print()

    # Back substitution
    x = [0, 0, 0, 0]
    x[3] = b[3] / m[3][3]
    for i in range(2, -1, -1):
        x[i] = b[i]
        for j in range(i + 1, 4):
            x[i] = x[i] - m[i][j] * x[j]
        x[i] = x[i] / m[i][i]

    return x