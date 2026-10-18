# TestDemo2

Small FastAPI quality pilot. The ASGI application is exported as `app` in
`app.py`.

- `GET /health-quality` returns `{"status":"ok","quality_version":1}`.
- `GET /echo?text=hello` returns `{"text":"hello"}`. Text is required and
  must contain 1–40 characters; invalid input returns HTTP 422.
- Unknown routes return HTTP 404.

## Local setup and run

From the project directory, use the provided offline environment. No package
downloads are required. Run requests locally with FastAPI's TestClient:

```sh
/tmp/factory-tools/venv/bin/python - <<'PY'
from fastapi.testclient import TestClient
from app import app

with TestClient(app) as client:
    print(client.get("/health-quality").json())
    print(client.get("/echo", params={"text": "hello"}).json())
PY
```

This executes the application in process without opening a network port. The
offline environment does not include an ASGI server such as Uvicorn, so running
a listening HTTP server requires a separately provided server. No server or
additional service is included in this pilot.

`requirements.txt` pins the runtime and test packages to the versions available
in the offline environment. In a separately provisioned environment with these
packages available, install them with `python -m pip install -r requirements.txt`.

## Tests

Run from the project directory:

```sh
/tmp/factory-tools/venv/bin/python -m pytest -q
```

In another environment with the requirements installed, use
`python -m pytest -q`. Tests cover the exact health response, echo lengths 1 and
40, missing/empty/41-character text, input preservation, and unknown routes.
Factory owns hosted CI and publication.
