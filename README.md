# TestDemo2

The application exposes `GET /planner-health`, returning
`{"status": "ok", "planner_version": 1}` with an integer version, and
`GET /planner-echo?text=...`, returning `{"text": "..."}` unchanged. Text must contain
1–16 Python Unicode code points; missing, empty, or longer text returns HTTP
422. Whitespace is preserved. Unknown routes and `/docs`, `/redoc`, and
`/openapi.json` return HTTP 404.

Run these commands from `/workspace/project` using the supplied offline
environment. No server or dependency downloads are needed.

In-process smoke example:

```bash
/tmp/factory-tools/venv/bin/python - <<'PY'
from fastapi.testclient import TestClient
from app import app

with TestClient(app) as client:
    health = client.get("/planner-health")
    assert health.status_code == 200
    assert health.json() == {"status": "ok", "planner_version": 1}
    assert type(health.json()["planner_version"]) is int
    text = " Hello 😀 "
    echo = client.get("/planner-echo", params={"text": text})
    assert echo.status_code == 200
    assert echo.json() == {"text": text}
print("Smoke passed")
PY
```

Run the tests (`python -m pytest -q` with the supplied interpreter):

```bash
/tmp/factory-tools/venv/bin/python -m pytest -q
```
