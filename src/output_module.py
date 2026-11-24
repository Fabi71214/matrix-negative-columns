"""Модуль формирования отчёта по результатам анализа матрицы."""

from datetime import datetime


def format_report(negative_cols, rows, cols):
    """Формирует итоговый словарь ответа с индексами отрицательных столбцов."""
    if negative_cols:
        msg = f"Номера столбцов, содержащих только отрицательные элементы: {negative_cols}"
    else:
        msg = "Столбцов, содержащих только отрицательные элементы, нет."

    return {
        "status": "success",
        "matrix_size": f"{rows}x{cols}",
        "negative_column_indices": negative_cols,
        "negative_column_numbers_1based": [i + 1 for i in negative_cols],
        "message": msg,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
