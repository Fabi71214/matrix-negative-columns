"""Точка входа интегрированной системы MatrixNegativeColumns."""

import threading
import time
from http.server import HTTPServer
from src.calc_module import MatrixRestHandler
from src.input_module import send_matrix_rest


def run_demo(port=8089):
    """Запускает локальный REST-сервер, выполняет серию проверок и возвращает результаты."""
    api_url = f"http://127.0.0.1:{port}/api/v1/analyze"
    server = HTTPServer(("127.0.0.1", port), MatrixRestHandler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    time.sleep(0.05)

    try:
        m1 = [[-1.0, 2.0, 2.0], [-1.0, 2.0, 2.0], [-1.0, 2.0, 2.0]]
        r1 = send_matrix_rest(3, 3, m1, api_url)

        m2 = [
            [-2.5, 1.0, -0.1, 4.0],
            [-3.0, -5.0, -8.2, 0.0],
            [-0.4, 2.2, -1.9, -3.3],
        ]
        r2 = send_matrix_rest(3, 4, m2, api_url)

        m3 = [[-1.0, 2.0], [0.0, 3.0]]
        r3 = send_matrix_rest(2, 2, m3, api_url)

        return [r1, r2, r3]
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    for idx, res in enumerate(run_demo(), start=1):
        print(f"[Запрос {idx}] {res['message']}")
