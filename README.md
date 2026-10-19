# TestDemo2

The application provides `GET /health` and `GET /echo?text=...`.
Echo accepts 1–16 Unicode code points and preserves whitespace. Missing,
empty, or longer text returns HTTP 422. Other paths, including `/docs`,
`/redoc`, and `/openapi.json`, return HTTP 404.

With the dependencies in `requirements.txt` available, run this in-process
smoke check from the project directory (no server is required):

```sh
python - <<'PY'
from fastapi.testclient import TestClient
from app import app

with TestClient(app) as client:
    health = client.get("/health")
    assert health.status_code == 200
    assert health.json() == {"status": "ok", "planner_version": 1}
    assert type(health.json()["planner_version"]) is int
    echo = client.get("/echo", params={"text": " hello "})
    assert echo.status_code == 200
    assert echo.json() == {"text": " hello "}
print("Smoke check passed")
PY
```

Run the contract and boundary tests from the project directory:

```sh
python -m pytest -q
```

In the preinstalled Factory offline environment, use:

```sh
/tmp/factory-tools/venv/bin/python -m pytest -q
```
