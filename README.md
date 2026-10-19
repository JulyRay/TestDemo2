# TestDemo2

This FastAPI app provides `GET /health` and `GET /echo?text=...`.
Echo accepts 1–16 Unicode code points and preserves whitespace. Missing,
empty, or longer text returns HTTP 422. Interactive documentation and the
OpenAPI route are disabled.

Run an in-process smoke request from `/workspace/project` with the available
offline Python environment; no server installation or running server is needed:

```sh
/tmp/factory-tools/venv/bin/python - <<'PY'
from fastapi.testclient import TestClient
from app import app

with TestClient(app) as client:
    response = client.get("/echo", params={"text": "hello"})
    assert response.status_code == 200
    assert response.json() == {"text": "hello"}
    print(response.json())
PY
```

Run the tests from the same project directory using the preinstalled environment:

```sh
/tmp/factory-tools/venv/bin/python -m pytest -q
```

With that environment activated, the equivalent command is `python -m pytest -q`.
No package downloads are required.
