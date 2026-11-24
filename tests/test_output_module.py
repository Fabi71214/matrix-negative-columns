"""Unit-тесты модуля output_module (покрытие решений)."""

from src.output_module import format_report


class TestOutputModule:
    """Тесты формирования отчёта."""

    def test_format_report_with_negative_columns(self):
        """Покрытие ветви True: найдены отрицательные столбцы."""
        report = format_report([0, 2], rows=3, cols=4)
        assert report["status"] == "success"
        assert report["matrix_size"] == "3x4"
        assert report["negative_column_indices"] == [0, 2]
        assert report["negative_column_numbers_1based"] == [1, 3]
        assert "[0, 2]" in report["message"]
        assert "timestamp" in report

    def test_format_report_empty_list(self):
        """Покрытие ветви False: отрицательные столбцы отсутствуют."""
        report = format_report([], rows=2, cols=2)
        assert report["status"] == "success"
        assert report["matrix_size"] == "2x2"
        assert report["negative_column_indices"] == []
        assert report["negative_column_numbers_1based"] == []
        assert "нет" in report["message"]
