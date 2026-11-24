"""Unit-тесты модуля input_module (граничные значения и комбинаторное покрытие условий)."""

import pytest
from src.input_module import validate_and_prepare_payload


class TestInputModule:
    """Тесты валидации и подготовки JSON-полезной нагрузки."""

    def test_valid_min_boundary_1x1(self):
        """Граничный тест: минимальная допустимая матрица 1x1."""
        payload = validate_and_prepare_payload(1, 1, [[-0.0001]])
        assert payload == {"rows_count": 1, "cols_count": 1, "data_grid": [[-0.0001]]}

    def test_valid_converts_ints_to_float(self):
        """Проверка преобразования целочисленных элементов в float."""
        payload = validate_and_prepare_payload(2, 2, [[-1, 0], [-2, 3]])
        assert payload["data_grid"] == [[-1.0, 0.0], [-2.0, 3.0]]

    @pytest.mark.parametrize(
        "n, m",
        [
            (0, 2),    # n <= 0 (True),  m <= 0 (False)
            (2, 0),    # n <= 0 (False), m <= 0 (True)
            (-1, -1),  # n <= 0 (True),  m <= 0 (True)
            (-5, 3),   # отрицательное n
            (3, -5),   # отрицательное m
        ],
    )
    def test_dimensions_combinatorial_and_boundaries(self, n, m):
        """Комбинаторное покрытие условий (n <= 0 or m <= 0) и граничные значения."""
        with pytest.raises(ValueError):
            validate_and_prepare_payload(n, m, [[-1.0]])

    def test_non_integer_dimensions_rejected(self):
        """Проверка некорректного типа размерностей (bool, float, str)."""
        with pytest.raises(TypeError):
            validate_and_prepare_payload(True, 2, [[-1.0, -2.0]])
        with pytest.raises(TypeError):
            validate_and_prepare_payload("2", 2, [[-1.0, -2.0]])

    def test_matrix_dimension_mismatch_rows(self):
        """Дефект №1: несоответствие числа строк матрицы значению n."""
        with pytest.raises(ValueError):
            validate_and_prepare_payload(3, 2, [[-1.0, -2.0], [-3.0, -4.0]])

    def test_matrix_dimension_mismatch_cols(self):
        """Дефект №1: несоответствие числа столбцов строки значению m."""
        with pytest.raises(ValueError):
            validate_and_prepare_payload(2, 3, [[-1.0, -2.0], [-3.0, -4.0]])
