"""Интеграционные тесты системы MatrixNegativeColumns (сэндвич-интеграция + REST API)."""

import threading
import time
import unittest
import urllib.error
import urllib.request
from http.server import HTTPServer
from src.calc_module import MatrixRestHandler, map_input_dto_to_internal
from src.input_module import send_matrix_rest
from src.main import run_demo
from src.stubs_drivers import calc_service_stub, run_bottom_driver


class TestSandwichIntegration(unittest.TestCase):
    """Сквозная проверка взаимодействия всех модулей системы."""

    @classmethod
    def setUpClass(cls):
        cls.api_url = "http://127.0.0.1:8091/api/v1/analyze"
        cls.server = HTTPServer(("127.0.0.1", 8091), MatrixRestHandler)
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()
        time.sleep(0.05)

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def test_01_stage1_stub_and_driver(self):
        payload = {"rows_count": 2, "cols_count": 2, "data_grid": [[-1, 2], [-3, 4]]}
        self.assertEqual(calc_service_stub(payload)["status"], "stub_ok")
        self.assertEqual(run_bottom_driver()["negative_column_indices"], [0, 2])

    def test_02_data_mapping(self):
        dto = {"rows_count": 2, "cols_count": 2, "data_grid": [[-1, 5], [-2, 6]]}
        mapped = map_input_dto_to_internal(dto)
        self.assertEqual((mapped["n"], mapped["m"]), (2, 2))

    def test_03_full_rest_integration_positive(self):
        matrix = [[-1.5, 2.0, -3.1], [-0.5, 0.0, -4.2]]
        resp = send_matrix_rest(2, 3, matrix, self.api_url)
        self.assertEqual(resp["negative_column_indices"], [0, 2])

    def test_04_full_rest_integration_no_negative(self):
        matrix = [[-1.0, 2.0], [0.0, -5.0]]
        resp = send_matrix_rest(2, 2, matrix, self.api_url)
        self.assertEqual(resp["negative_column_indices"], [])

    def test_05_error_handling_bad_json(self):
        req = urllib.request.Request(
            self.api_url,
            data=b'{"bad": 1}',
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with self.assertRaises(urllib.error.HTTPError) as ctx:
            urllib.request.urlopen(req)
        self.assertEqual(ctx.exception.code, 400)

    def test_06_main_demo_end_to_end(self):
        results = run_demo(port=8092)
        self.assertEqual(results[0]["negative_column_indices"], [0])
        self.assertEqual(results[1]["negative_column_indices"], [0, 2])
        self.assertEqual(results[2]["negative_column_indices"], [])
