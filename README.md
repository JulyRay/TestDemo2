# TestDemo2

The API exposes `GET /planner-health` and `GET /planner-echo?text=...`. Echo accepts
1–16 Python Unicode code points, including whitespace, and preserves the text
unchanged. Missing, empty, or longer text returns HTTP 422. Documentation routes
(`/docs`, `/redoc`, and `/openapi.json`) are disabled.

Run this smoke example from the project directory using the preinstalled offline
environment. It imports the application and makes requests in process; no
listening server, uvicorn, or package downloads are required.

```bash
/tmp/factory-tools/venv/bin/python - <<'PY'
from fastapi.testclient import TestClient
from app import app

with TestClient(app) as client:
    health = client.get("/planner-health")
    assert health.status_code == 200
    assert health.json() == {"status": "ok", "planner_version": 1}
    assert type(health.json()["planner_version"]) is int
    text = " hello 😀 "
    echo = client.get("/planner-echo", params={"text": text})
    assert echo.status_code == 200
    assert echo.json() == {"text": text}
print("Smoke checks passed")
PY
```

Run the tests from the project directory with the same offline environment:

```bash
/tmp/factory-tools/venv/bin/python -m pytest -q
```

When that environment is already activated, the equivalent command is
`python -m pytest -q`.
