# TestDemo2

## Local in-process smoke check

Once the application node supplies `app.py`, run this from the project directory
using the preinstalled offline Python environment. `TestClient` exercises the
application in process; no uvicorn process or listening server is required.

```sh
/tmp/factory-tools/venv/bin/python - <<'PY'
from fastapi.testclient import TestClient
from app import app

with TestClient(app) as client:
    response = client.get("/__smoke_unknown__")
    assert response.status_code == 404, response.text
print("In-process smoke check passed")
PY
```

## Tests

Run the endpoint contract tests from the project directory:

```sh
/tmp/factory-tools/venv/bin/python -m pytest -q
```

With that environment activated, the equivalent command is `python -m pytest -q`.
The environment already includes the dependencies in `requirements.txt`; no
package downloads are needed.
