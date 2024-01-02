from decimal import Decimal


def solve_2x2(m: list[list[Decimal]], b: list[Decimal]) -> list[Decimal]:
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
