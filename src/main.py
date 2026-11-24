import threading, time
from http.server import HTTPServer
from src.calc_module import MatrixRestHandler
from src.input_module import send_matrix_rest

API_URL = "http://127.0.0.1:8089/api/v1/analyze"

server = HTTPServer(("127.0.0.1", 8089), MatrixRestHandler)
threading.Thread(target=server.serve_forever, daemon=True).start()
time.sleep(0.1)

m1 = [[-1.0, 2.0, 2.0], [-1.0, 2.0, 2.0], [-1.0, 2.0, 2.0]]
r1 = send_matrix_rest(3, 3, m1, API_URL)
print("Итог:", r1["message"])
server.shutdown()
