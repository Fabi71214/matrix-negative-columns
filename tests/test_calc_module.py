"""Unit-тесты модуля calc_module (анализ граничных значений и покрытие решений)."""

import pytest
from src.calc_module import find_negative_columns, map_input_dto_to_internal


class TestCalcModule:
    """Тесты алгоритма поиска отрицательных столбцов и маппинга DTO."""

    def test_boundary_around_zero(self):
        """Анализ граничных значений вокруг нуля: -0.0001 (<0), 0.0 (>=0), 0.0001 (>0)."""
        matrix = [
            [-0.0001, 0.0, 0.0001],
            [-1.5, -2.5, -3.5],
        ]
        assert find_negative_columns(2, 3, matrix) == [0]

    def test_all_columns_negative(self):
        """Все столбцы строго отрицательные (покрытие ветви prov=True)."""
        matrix = [[-1.0, -2.5], [-0.1, -99.9]]
        assert find_negative_columns(2, 2, matrix) == [0, 1]

    def test_no_negative_columns(self):
        """Ни один столбец не подходит (покрытие ветви prov=False и break)."""
        matrix = [[0.0, 1.0], [-1.0, -2.0]]
        assert find_negative_columns(2, 2, matrix) == []

    def test_single_element_negative_and_zero(self):
        """Граничный размер матрицы 1x1."""
        assert find_negative_columns(1, 1, [[-0.01]]) == [0]
        assert find_negative_columns(1, 1, [[0.0]]) == []

    def test_zero_or_negative_dimensions_raise_error(self):
        """Дефект №2: нулевые или отрицательные n, m не должны давать ложные столбцы."""
        with pytest.raises(ValueError):
            find_negative_columns(0, 2, [])
        with pytest.raises(ValueError):
            find_negative_columns(-1, 2, [])

    def test_mismatched_matrix_shape_raises_error(self):
        """Проверка несоответствия фактической формы матрицы в calc_module."""
        with pytest.raises(ValueError):
            find_negative_columns(2, 2, [[-1.0, -2.0]])

    def test_map_input_dto_to_internal_valid(self):
        """Корректный маппинг DTO -> внутренние переменные."""
        dto = {"rows_count": 2, "cols_count": 2, "data_grid": [[-1, 2], [-3, 4]]}
        result = map_input_dto_to_internal(dto)
        assert result == {"n": 2, "m": 2, "matrix": [[-1.0, 2.0], [-3.0, 4.0]]}

    def test_map_input_dto_missing_key(self):
        """Отсутствие обязательных полей в DTO вызывает KeyError."""
        with pytest.raises(KeyError):
            map_input_dto_to_internal({"rows_count": 2})
