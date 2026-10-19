import pytest
from fastapi.testclient import TestClient

from app import app


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_health_exact_payload(client):
    response = client.get("/planner-health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "planner_version": 1}
    assert type(response.json()["planner_version"]) is int


@pytest.mark.parametrize("length", range(1, 17))
def test_echo_exact_valid_length_payloads(client, length):
    text = "a" * length
    response = client.get("/planner-echo", params={"text": text})

    assert response.status_code == 200
    assert response.json() == {"text": text}


@pytest.mark.parametrize("params", [{}, {"text": ""}, {"text": "a" * 17}])
def test_echo_rejects_missing_empty_and_overlong_text(client, params):
    assert client.get("/planner-echo", params=params).status_code == 422


@pytest.mark.parametrize("character", ["é", "🙂"])
@pytest.mark.parametrize("length", [16, 17])
def test_echo_unicode_limit_counts_code_points(client, character, length):
    text = character * length
    assert len(text) == length
    assert len(text.encode("utf-8")) > length

    response = client.get("/planner-echo", params={"text": text})

    if length == 16:
        assert response.status_code == 200
        assert response.json() == {"text": text}
    else:
        assert response.status_code == 422


@pytest.mark.parametrize("text", [" ", " " * 16, " \t\n", " hello ", " " + "a" * 14 + " "])
def test_echo_preserves_valid_whitespace(client, text):
    response = client.get("/planner-echo", params={"text": text})

    assert response.status_code == 200
    assert response.json() == {"text": text}


@pytest.mark.parametrize("path", ["/unknown-route", "/docs", "/redoc", "/openapi.json", "/health", "/echo"])
def test_absent_routes_return_404(client, path):
    assert client.get(path).status_code == 404
