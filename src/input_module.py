import json
import urllib.request

def validate_and_prepare_payload(n, m, matrix):
    if n <= 0 or m <= 0:
        raise ValueError("Размерности n и m должны быть целыми положительными числами (> 0)")
    norm = [[float(v) for v in row] for row in matrix]
    return {"rows_count": n, "cols_count": m, "data_grid": norm}

def send_matrix_rest(n, m, matrix, api_url="http://127.0.0.1:8089/api/v1/analyze"):
    payload = validate_and_prepare_payload(n, m, matrix)
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(api_url, data=body, headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))
