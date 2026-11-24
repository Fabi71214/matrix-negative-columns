"""Регрессионные тесты для защиты от повторного появления исправленных дефектов."""

import pytest
from src.calc_module import find_negative_columns
from src.input_module import validate_and_prepare_payload


class TestRegression:
    """Регрессионный набор по баг-репортам №1 и №2."""

    def test_regression_bug_01_matrix_shape_validation(self):
        """Регрессия Баг №1: расхождение размеров n, m с фактической матрицей."""
        with pytest.raises(ValueError):
            validate_and_prepare_payload(3, 3, [[-1.0, -2.0], [-3.0, -4.0]])
        with pytest.raises(ValueError):
            validate_and_prepare_payload(2, 3, [[-1.0, -2.0, -3.0], [-4.0]])

    def test_regression_bug_02_zero_rows_no_false_negative_columns(self):
        """Регрессия Баг №2: n <= 0 не должен возвращать ложные столбцы."""
        with pytest.raises(ValueError):
            find_negative_columns(0, 3, [])
        with pytest.raises(ValueError):
            find_negative_columns(-2, 2, [])

    def test_regression_zero_element_not_counted_as_negative(self):
        """Регрессия граничного значения 0.0: ноль не является отрицательным."""
        assert find_negative_columns(2, 2, [[-1.0, -0.001], [0.0, -0.001]]) == [1]
