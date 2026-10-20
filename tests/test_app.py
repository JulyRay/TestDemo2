import pytest
from fastapi.testclient import TestClient

from app import app


def test_only_required_routes_are_registered():
    assert {(route.path, frozenset(route.methods)) for route in app.routes} == {
        ("/planner-health", frozenset({"GET"})),
        ("/planner-echo", frozenset({"GET"})),
    }


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_health(client):
    response = client.get("/planner-health")
    assert response.status_code == 200
    payload = response.json()
    assert payload == {"status": "ok", "planner_version": 1}
    # Equality alone would also accept True (and 1.0) as 1.
    assert type(payload["planner_version"]) is int


@pytest.mark.parametrize("character", ["a", "é", "😀"], ids=["ascii", "non_ascii", "supplementary"])
@pytest.mark.parametrize("length", [1, 16, 17])
def test_echo_code_point_boundaries(client, character, length):
    text = character * length
    assert len(text) == length
    response = client.get("/planner-echo", params={"text": text})
    if length <= 16:
        assert response.status_code == 200
        assert response.json() == {"text": text}
    else:
        assert response.status_code == 422
        assert any(error["loc"] == ["query", "text"] for error in response.json()["detail"])


@pytest.mark.parametrize("params", [{}, {"text": ""}], ids=["missing", "empty"])
def test_echo_requires_nonempty_text(client, params):
    response = client.get("/planner-echo", params=params)
    assert response.status_code == 422
    assert any(error["loc"] == ["query", "text"] for error in response.json()["detail"])


@pytest.mark.parametrize("text", [" ", " " * 16, " \tHello 😀\n ", "e\u0301" * 8])
def test_echo_preserves_text_exactly(client, text):
    response = client.get("/planner-echo", params={"text": text})
    assert response.status_code == 200
    assert response.json() == {"text": text}


@pytest.mark.parametrize("path", ["/", "/unknown", "/docs", "/redoc", "/openapi.json", "/health", "/echo"])
def test_absent_routes(client, path):
    response = client.get(path)
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}
