from condition import SimpleCondition


def test_simple():
    assert str(SimpleCondition("m", "<", 1234)) == "m < 1234"
    assert str(SimpleCondition("m", "<", 1234).inverse()) == "m >= 1234"
    assert str(SimpleCondition("m", ">", 1234).inverse()) == "m <= 1234"
    assert str(SimpleCondition("m", ">=", 1234).inverse()) == "m < 1234"
    assert str(SimpleCondition("m", "<=", 1234).inverse()) == "m > 1234"

    assert str(SimpleCondition("m", "<", 1234).inverse().inverse()) == "m < 1234"


def test_combination_of_two_simple_conditions():
    c1 = SimpleCondition("x", "<", 42)
    c1_copy = SimpleCondition("x", "<", 42)
    c2 = SimpleCondition("m", ">", 55)

    assert str(c1 & c2) == "x < 42 && m > 55"
    assert str(c1 | c2) == "x < 42 || m > 55"

    assert str(c1 & c1_copy) == str(c1)
    assert str(c1 | c1_copy) == str(c1)

    assert str((c1 & c2).inverse()) == "x >= 42 || m <= 55"
    assert str((c1 | c2).inverse()) == "x >= 42 && m <= 55"


def test_combination_of_complext_conditions():
    c1 = SimpleCondition("x", "<", 42)
    c2 = SimpleCondition("m", ">", 55)
    c3 = SimpleCondition("y", "<", 100)

    assert str(c1 & c2 & c3) == "x < 42 && m > 55 && y < 100"
    assert str(c1 | c2 | c3) == "x < 42 || m > 55 || y < 100"

    assert str(c1 & c2 | c3) == "x < 42 && m > 55 || y < 100"
    assert str(c1 | c2 & c3) == "x < 42 || m > 55 && y < 100"

    assert str(c1 & (c2 | c3)) == "x < 42 && (m > 55 || y < 100)"
    assert str((c1 | c2) & c3) == "(x < 42 || m > 55) && y < 100"


def test_normalization():
    c1 = SimpleCondition("x", "<", 42)
    c2 = SimpleCondition("m", ">", 55)
    c3 = SimpleCondition("y", "<", 100)
    c4 = SimpleCondition("z", ">", 200)

    assert str(c1.normalize()) == str(c1)

    assert str((c1 & c2).normalize()) == str(c1 & c2)
    assert str((c1 | c2).normalize()) == str(c1 | c2)

    assert str((c1 & (c2 | c3)).normalize()) == str(c1 & c2 | c1 & c3)
    assert str(((c1 | c2) & c3).normalize()) == str(c1 & c3 | c2 & c3)

    assert str(((c1 | c2) & (c3 | c4)).normalize()) == str(
        c1 & c3 | c1 & c4 | c2 & c3 | c2 & c4
    )
