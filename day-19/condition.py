from __future__ import annotations
from abc import ABC


INVERTED_OPERATORS = {
    "<": ">=",
    "<=": ">",
    ">": "<=",
    ">=": "<",
    "&&": "||",
    "||": "&&",
}


class Condition(ABC):
    def __and__(self, other) -> Condition:
        raise NotImplementedError()

    def __or__(self, other) -> Condition:
        raise NotImplementedError()

    def inverse(self) -> Condition:
        raise NotImplementedError()

    def normalize(self) -> Condition:
        raise NotImplementedError()


class SimpleCondition(Condition):
    _property: str
    _operator: str
    _threshold: int

    def __init__(self, property: str, operator: str, threshold: int):
        self._property = property
        self._operator = operator
        self._threshold = threshold

    def __eq__(self, other) -> bool:
        if not isinstance(other, SimpleCondition):
            return False

        return (
            self._property == other._property
            and self._operator == other._operator
            and self._threshold == other._threshold
        )

    def __str__(self) -> str:
        return f"{self._property} {self._operator} {self._threshold}"

    def inverse(self) -> SimpleCondition:
        inverted_operator = INVERTED_OPERATORS[self._operator]
        return SimpleCondition(self._property, inverted_operator, self._threshold)

    def __and__(self, other) -> Condition:
        assert isinstance(other, Condition)

        if other == self:
            return self

        return ComplexCondition(self, "&&", other)

    def __or__(self, other) -> Condition:
        assert isinstance(other, Condition)

        if other == self:
            return self

        return ComplexCondition(self, "||", other)

    def normalize(self) -> Condition:
        return self


class ComplexCondition(Condition):
    _left: Condition
    _operator: str
    _right: Condition

    def __init__(self, left, operator, right):
        self._left = left
        self._operator = operator
        self._right = right

    def __str__(self) -> str:
        left_part = str(self._left)
        if isinstance(self._left, ComplexCondition):
            if self._operator == "&&" and self._left._operator == "||":
                left_part = f"({left_part})"

        right_part = str(self._right)
        if isinstance(self._right, ComplexCondition):
            if self._operator == "&&" and self._right._operator == "||":
                right_part = f"({right_part})"

        return f"{left_part} {self._operator} {right_part}"

    def inverse(self) -> ComplexCondition:
        inverted_operator = INVERTED_OPERATORS[self._operator]
        return ComplexCondition(
            self._left.inverse(), inverted_operator, self._right.inverse()
        )

    def __and__(self, other) -> Condition:
        assert isinstance(other, Condition)

        # if other == self:
        #     return self

        return ComplexCondition(self, "&&", other)

    def __or__(self, other) -> Condition:
        assert isinstance(other, Condition)

        # if other == self:
        #     return self

        return ComplexCondition(self, "||", other)

    def normalize(self) -> Condition:
        if isinstance(self._left, SimpleCondition) and isinstance(
            self._right, SimpleCondition
        ):
            return self

        if isinstance(self._left, SimpleCondition):
            return ComplexCondition(
                self._left & self._right._left,
                "||",
                self._left & self._right._right,
            )

        if isinstance(self._right, SimpleCondition):
            return ComplexCondition(
                self._left._left & self._right,
                "||",
                self._left._right & self._right,
            )

        return ComplexCondition(
            self._left._left & self._right._left,
            "||",
            self._left._left & self._right._right,
        ) | ComplexCondition(
            self._left._right & self._right._left,
            "||",
            self._left._right & self._right._right,
        )
