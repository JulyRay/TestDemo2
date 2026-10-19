"""Endpoint boundary and application input-retention regressions."""
import app as app_module

from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_one_and_sixty_three():
    for size in (1, 63, 64):
        text = "x" * size
        response = client.get("/bounded-echo", params={"text": text})
        assert response.status_code == 200
        assert response.json() == {"text": text}


def test_invalid_inputs():
    assert client.get("/bounded-echo").status_code == 422
    for text in ("", "x" * 65):
        assert client.get("/bounded-echo", params={"text": text}).status_code == 422
    assert client.get("/unknown").status_code == 404


def test_repeated_calls_do_not_retain_inputs_in_module_state():
    submitted = {f"retention-regression-{index:04d}" for index in range(200)}
    for text in sorted(submitted):
        response = client.get("/bounded-echo", params={"text": text})
        assert response.status_code == 200
        assert response.json() == {"text": text}

    seen = set()

    def assert_no_input(value):
        if isinstance(value, str):
            assert value not in submitted, "Request input retained in application state"
        elif isinstance(value, (dict, list, tuple, set, frozenset)):
            if id(value) in seen:
                return
            seen.add(id(value))
            if isinstance(value, dict):
                for key, item in value.items():
                    assert_no_input(key)
                    assert_no_input(item)
            else:
                for item in value:
                    assert_no_input(item)

    for name, value in vars(app_module).items():
        if not name.startswith("__"):
            assert_no_input(value)
    assert_no_input(vars(app_module.app.state))
