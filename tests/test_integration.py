import unittest, threading, time, urllib.request, urllib.error
from http.server import HTTPServer
from src.calc_module import MatrixRestHandler, map_input_dto_to_internal
from src.input_module import send_matrix_rest
from src.stubs_drivers import calc_service_stub, run_bottom_driver

class TestSandwichIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.api_url = "http://127.0.0.1:8091/api/v1/analyze"
        cls.server = HTTPServer(("127.0.0.1", 8091), MatrixRestHandler)
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()
        time.sleep(0.1)

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def test_01_stage1_stub_and_driver(self):
        self.assertEqual(calc_service_stub({"rows_count": 2, "cols_count": 2, "data_grid": [[-1, 2], [-3, 4]]})["status"], "stub_ok")
        self.assertEqual(run_bottom_driver()["negative_column_indices"], [0, 2])

    def test_02_data_mapping(self):
        m = map_input_dto_to_internal({"rows_count": 2, "cols_count": 2, "data_grid": [[-1, 5], [-2, 6]]})
        self.assertEqual((m["n"], m["m"]), (2, 2))

    def test_03_full_rest_integration_positive(self):
        r = send_matrix_rest(2, 3, [[-1.5, 2.0, -3.1], [-0.5, 0.0, -4.2]], self.api_url)
        self.assertEqual(r["negative_column_indices"], [0, 2])

    def test_04_full_rest_integration_no_negative(self):
        r = send_matrix_rest(2, 2, [[-1.0, 2.0], [0.0, -5.0]], self.api_url)
        self.assertEqual(r["negative_column_indices"], [])

    def test_05_error_handling_bad_json(self):
        req = urllib.request.Request(self.api_url, data=b'{"bad": 1}', headers={"Content-Type": "application/json"}, method="POST")
        with self.assertRaises(urllib.error.HTTPError) as ctx:
            urllib.request.urlopen(req)
        self.assertEqual(ctx.exception.code, 400)
