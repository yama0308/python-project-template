import pytest

from calc import sum_numbers


class TestSumNumbers:
    def test_positive_numbers(self) -> None:
        assert sum_numbers(1, 2) == 3

    def test_negative_numbers(self) -> None:
        assert sum_numbers(-1, -2) == -3

    def test_zero(self) -> None:
        assert sum_numbers(0, 0) == 0

    def test_float_numbers(self) -> None:
        assert sum_numbers(1.5, 2.3) == pytest.approx(3.8)
