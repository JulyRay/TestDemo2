# TestDemo2

Small FastAPI quality pilot. The ASGI application is exported as `app` from
`app.py` (`app:app`).

- `GET /health-quality` returns HTTP 200 and exactly
  `{"status":"ok","quality_version":1}`.
- `GET /echo?text=hello` returns HTTP 200 and exactly `{"text":"hello"}`.
  `text` is required and must contain 1–40 characters. Missing, empty, or
  longer values return HTTP 422. Input text is preserved, including whitespace.
- Unknown routes return HTTP 404.

## Local run

From the project directory, run requests in process using the preinstalled
offline environment (no network server or package downloads required):

```bash
/tmp/factory-tools/venv/bin/python - <<'PY'
from fastapi.testclient import TestClient
from app import app

with TestClient(app) as client:
    for path, params in [("/health-quality", {}), ("/echo", {"text": "hello"})]:
        response = client.get(path, params=params)
        print(response.status_code, response.json())
PY
```

This exercises the ASGI application locally without opening a listening port.
An HTTP server requires a separately provisioned ASGI server; the offline
toolchain does not include Uvicorn.

## Tests

Run from the project directory:

```bash
/tmp/factory-tools/venv/bin/python -m pytest -q
```

Tests cover the exact health response, echo lengths 1 and 40, missing/empty/
length-41 rejection, text preservation, and unknown routes.

`requirements.txt` pins the runtime and test packages to the available offline
versions. In a separately provisioned environment with these requirements
installed, the equivalent test command is `python -m pytest -q`.
Factory owns dependency installation and hosted CI validation.
