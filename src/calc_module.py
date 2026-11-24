"""Расчётный модуль: поиск отрицательных столбцов и HTTP REST-обработчик."""

import json
from http.server import BaseHTTPRequestHandler
from src.output_module import format_report


def map_input_dto_to_internal(dto):
    """Сопоставляет поля входного JSON DTO внутренним переменным алгоритма."""
    n = int(dto["rows_count"])
    m = int(dto["cols_count"])
    matrix = [[float(val) for val in row] for row in dto["data_grid"]]
    return {"n": n, "m": m, "matrix": matrix}


def find_negative_columns(n, m, matrix):
    """Возвращает индексы столбцов, все элементы которых строго меньше 0."""
    if n <= 0 or m <= 0:
        raise ValueError("Размерности n и m должны быть положительными (> 0)")
    if len(matrix) != n or any(len(row) != m for row in matrix):
        raise ValueError("Фактическая размерность матрицы не соответствует n и m")
    res = []
    for j in range(m):
        prov = True
        for i in range(n):
            if matrix[i][j] >= 0:
                prov = False
                break
        if prov:
            res.append(j)
    return res


class MatrixRestHandler(BaseHTTPRequestHandler):
    """HTTP-обработчик POST-запросов для анализа матриц."""

    def log_message(self, format, *args):
        """Отключает стандартное логирование запросов в stderr."""
        pass

    def do_POST(self):
        """Принимает JSON с матрицей и возвращает отчёт анализа в формате JSON."""
        try:
            length = int(self.headers.get("Content-Length", 0))
            dto = json.loads(self.rfile.read(length).decode("utf-8"))
            internal = map_input_dto_to_internal(dto)
            neg_cols = find_negative_columns(
                internal["n"],
                internal["m"],
                internal["matrix"],
            )
            report = format_report(neg_cols, internal["n"], internal["m"])
            body = json.dumps(report, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(body)
        except Exception as exc:
            err = json.dumps(
                {"status": "error", "message": str(exc)},
                ensure_ascii=False,
            ).encode("utf-8")
            self.send_response(400)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(err)
