"""Unit-тесты модуля stubs_drivers (заглушка и драйвер сэндвич-интеграции)."""

from src.stubs_drivers import calc_service_stub, run_bottom_driver


class TestStubsDrivers:
    """Тесты вспомогательных компонентов интеграции."""

    def test_calc_service_stub_returns_expected_structure(self):
        """Проверка ответа заглушки верхнего уровня."""
        payload = {"rows_count": 3, "cols_count": 4, "data_grid": []}
        res = calc_service_stub(payload)
        assert res["status"] == "stub_ok"
        assert res["received_rows"] == 3
        assert res["received_cols"] == 4
        assert res["negative_column_indices"] == [0]

    def test_run_bottom_driver_calls_output_module(self):
        """Проверка драйвера нижнего уровня."""
        res = run_bottom_driver()
        assert res["status"] == "success"
        assert res["matrix_size"] == "3x3"
        assert res["negative_column_indices"] == [0, 2]
