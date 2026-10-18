# TestDemo2

A small FastAPI quality pilot. The ASGI application is exported as `app` from
`app.py`.

- `GET /health-quality` returns `200` and exactly
  `{"status":"ok","quality_version":1}`.
- `GET /echo?text=hello` returns `200` and exactly `{"text":"hello"}`.
  Text is required and must contain 1–40 characters. Missing, empty, or longer
  text returns `422`.
- Unknown routes return `404`.

## Local setup and tests

With dependency installation available, create an environment and install the
pinned runtime and test dependencies:

```sh
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pytest -q
```

In the provided offline environment, use the preinstalled toolchain without
installing packages. Run from `/workspace/project`:

```sh
/tmp/factory-tools/venv/bin/python -m pytest -q
```

## Run locally without a network server

The offline toolchain has no ASGI server such as Uvicorn. Exercise the app
in-process using the included httpx-based FastAPI client:

```sh
/tmp/factory-tools/venv/bin/python - <<'PY'
from fastapi.testclient import TestClient
from app import app

with TestClient(app) as client:
    print(client.get("/health-quality").json())
    print(client.get("/echo", params={"text": "hello"}).json())
PY
```

For a locally created environment, substitute `.venv/bin/python` for the offline
Python path. This runs the application without opening a port; network serving
would require a separately supplied ASGI server. No server dependency is added.
