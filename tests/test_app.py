import pytest
from fastapi.testclient import TestClient

from app import app


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "planner_version": 1}
    assert type(response.json()["planner_version"]) is int


@pytest.mark.parametrize(
    "text",
    ["a", "abcdefghijklmnop", " ", "  hello  ", " " * 16, "\U0001f680" * 16],
    ids=["ascii-1", "ascii-16", "space", "surrounding-spaces", "spaces-16", "unicode-16"],
)
def test_echo_preserves_valid_text(client, text):
    response = client.get("/echo", params={"text": text})
    assert response.status_code == 200
    assert response.json() == {"text": text}


@pytest.mark.parametrize(
    "params,error_type",
    [
        ({}, "missing"),
        ({"text": ""}, "string_too_short"),
        ({"text": "abcdefghijklmnopq"}, "string_too_long"),
        ({"text": "\U0001f680" * 17}, "string_too_long"),
    ],
    ids=["missing", "empty", "ascii-17", "unicode-17"],
)
def test_echo_rejects_invalid_text(client, params, error_type):
    response = client.get("/echo", params=params)
    assert response.status_code == 422
    errors = response.json()["detail"]
    assert len(errors) == 1
    assert errors[0]["loc"] == ["query", "text"]
    assert errors[0]["type"] == error_type


@pytest.mark.parametrize("path", ["/unknown", "/docs", "/redoc", "/openapi.json"])
def test_unavailable_routes(client, path):
    response = client.get(path)
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}


def test_only_requested_routes_are_exposed():
    assert len(app.routes) == 2
    assert {(route.path, frozenset(route.methods)) for route in app.routes} == {
        ("/health", frozenset({"GET"})),
        ("/echo", frozenset({"GET"})),
    }
