"""Заглушка и драйвер для первого этапа сэндвич-интеграции."""

from src.input_module import validate_and_prepare_payload
from src.output_module import format_report


def calc_service_stub(payload):
    """Заглушка расчётного модуля для проверки верхнего слоя."""
    return {
        "status": "stub_ok",
        "received_rows": payload["rows_count"],
        "received_cols": payload["cols_count"],
        "negative_column_indices": [0],
        "message": "[STUB] Имитация ответа расчётного модуля: столбец [0]",
    }


def run_bottom_driver():
    """Драйвер нижнего уровня для проверки модуля вывода."""
    return format_report([0, 2], rows=3, cols=3)


if __name__ == "__main__":
    sample = [[-1.0, 2.0, -3.0], [-4.0, 5.0, -6.0], [-7.0, 8.0, -9.0]]
    p = validate_and_prepare_payload(3, 3, sample)
    print("1. Тест верхнего модуля (Input -> Calc Stub):", calc_service_stub(p))
    print("2. Тест нижнего модуля (Driver -> Output):", run_bottom_driver())
