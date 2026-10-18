# TestDemo2

Small FastAPI quality pilot. The application is exported as `app` from `app.py`.

- `GET /health-quality` returns `{"status":"ok","quality_version":1}`.
- `GET /echo?text=hello` returns `{"text":"hello"}`. Text is required and
  must contain 1–40 characters; missing, empty, or longer input returns HTTP 422.
- Unknown routes return HTTP 404.

## Local run and tests

From the project directory, use the preinstalled offline environment (no package
downloads required):

```sh
/tmp/factory-tools/venv/bin/python -m pytest -q
```

Run requests locally in-process, without a network server:

```sh
/tmp/factory-tools/venv/bin/python - <<'PY'
from fastapi.testclient import TestClient
from app import app

with TestClient(app) as client:
    print(client.get("/health-quality").json())
    print(client.get("/echo", params={"text": "hello"}).json())
PY
```

`requirements.txt` pins the runtime and test packages to the versions available
in the offline toolchain. In an environment where those requirements have been
installed, run tests with `python -m pytest -q`.

To serve HTTP locally, an ASGI server is required. Uvicorn is not installed in
the supplied offline environment and is not added as a dependency. If already
available in your local environment, run `python -m uvicorn app:app --host
127.0.0.1 --port 8000` from the project directory.
