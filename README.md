# TestDemo2

Small FastAPI quality pilot. The ASGI application is exported as `app` from
`app.py`.

- `GET /health-quality` returns `{"status":"ok","quality_version":1}`.
- `GET /echo?text=hello` returns `{"text":"hello"}`. The required `text`
  query parameter accepts 1–40 characters, inclusive; missing, empty or longer
  values return HTTP 422. Input is preserved, including whitespace and Unicode.
- Unknown routes return HTTP 404.

## Local setup and tests

From the project directory, use the provided offline Python environment:

```sh
/tmp/factory-tools/venv/bin/python -m pytest -q
```

`requirements.txt` pins the runtime and test libraries to the available offline
toolchain. In a separately provisioned environment, install these requirements
with `python -m pip install -r requirements.txt`, then run
`python -m pytest -q`. No package download is needed in the provided environment.

## Run locally

Exercise the application offline without starting a network service:

```sh
/tmp/factory-tools/venv/bin/python - <<'PY'
from fastapi.testclient import TestClient
from app import app

with TestClient(app) as client:
    print(client.get('/health-quality').json())
    print(client.get('/echo', params={'text': 'hello'}).json())
PY
```

For HTTP serving in an environment that already supplies Uvicorn, run
`python -m uvicorn app:app --host 127.0.0.1 --port 8000`, then visit
`http://127.0.0.1:8000/health-quality` or
`http://127.0.0.1:8000/echo?text=hello`.
Uvicorn is not installed in the provided offline environment and is not added
as a dependency; the offline tests use FastAPI's in-process client.
