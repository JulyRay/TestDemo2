# TestDemo2

A small FastAPI quality pilot. `app.py` exports the ASGI application `app`.
Use Python 3.10 or newer.

- `GET /health-quality` returns HTTP 200 and exactly
  `{"status":"ok","quality_version":1}`.
- `GET /echo?text=hello` returns HTTP 200 and exactly `{"text":"hello"}`.
  The required `text` query must contain 1–40 characters; missing, empty, or
  longer values return HTTP 422.
- Unknown routes return HTTP 404.

## Local setup and tests

In an environment where package installation is available:

```sh
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pytest -q
```

For the supplied offline environment, run from `/workspace/project` without
installing or downloading packages:

```sh
/tmp/factory-tools/venv/bin/python -m pytest -q
```

## Local run without a network service

Exercise the application in process using the supplied offline environment:

```sh
/tmp/factory-tools/venv/bin/python - <<'PY'
from fastapi.testclient import TestClient
from app import app

with TestClient(app) as client:
    print(client.get('/health-quality').json())
    print(client.get('/echo', params={'text': 'hello'}).json())
PY
```

For a standard local setup, substitute `.venv/bin/python` in this command.
Serving HTTP requires an ASGI server, which is not included in the supplied
offline toolchain or these dependencies. No network service is needed for tests.
