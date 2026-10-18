# TestDemo2

Small FastAPI quality pilot. `app.py` exports the ASGI application `app`.

- `GET /health-quality` returns HTTP 200 and exactly
  `{"status":"ok","quality_version":1}`.
- `GET /echo?text=hello` returns HTTP 200 and exactly `{"text":"hello"}`.
  Text is required and must contain 1–40 characters. Missing, empty, or
  overlong text returns HTTP 422. Input is preserved without trimming.
- Unknown routes return HTTP 404.

## Local setup and tests

From the project directory, use the preinstalled offline environment:

```sh
/tmp/factory-tools/venv/bin/python -m pytest -q
```

`requirements.txt` pins the runtime and test packages to the versions available
in that environment. No downloads are needed for the offline workflow. In a
separately provisioned environment with package access, install those pins with
`python -m pip install -r requirements.txt`, then run `python -m pytest -q`.

## Run locally without a server

Exercise the application in process using the available HTTP test client:

```sh
/tmp/factory-tools/venv/bin/python - <<'PY'
from fastapi.testclient import TestClient
from app import app

with TestClient(app) as client:
    print(client.get("/health-quality").json())
    print(client.get("/echo", params={"text": "hello"}).json())
PY
```

The offline toolchain does not include an ASGI server such as Uvicorn, so this
project does not start a listening HTTP server or add a server dependency.
Tests cover health output, both valid length boundaries, all three invalid
query cases, exact input preservation, and an unknown route.
