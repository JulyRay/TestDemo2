# TestDemo2

V2.0 minimal FastAPI application baseline. Login and CRUD are outside this baseline.

## Local setup

Use Python 3.10 or newer (validated with Python 3.13). From the repository root:

```sh
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows, activate with `.venv\Scripts\activate` instead.

## Run

```sh
python -m uvicorn app:app --reload
```

The server runs at `http://127.0.0.1:8000`. `GET /health-extra` returns HTTP 200
and exactly `{"status":"ok"}` JSON. Unknown routes return HTTP 404.

## Test

```sh
python -m pytest
```

Tests use FastAPI's TestClient to check the health status, exact JSON response,
and an unknown route. No running server is required.
