import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app import app


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_exports_fastapi_app():
    assert isinstance(app, FastAPI)


def test_health_quality(client):
    response = client.get("/health-quality")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "quality_version": 1}
    assert type(response.json()["quality_version"]) is int


@pytest.mark.parametrize("text", ["a", "x" * 40, " ", " café & + ? ", "é" * 40])
def test_echo_preserves_valid_text(client, text):
    response = client.get("/echo", params={"text": text})
    assert response.status_code == 200
    assert response.json() == {"text": text}


@pytest.mark.parametrize("params", [{}, {"text": ""}, {"text": "x" * 41}])
def test_echo_rejects_invalid_text(client, params):
    response = client.get("/echo", params=params)
    assert response.status_code == 422


def test_unknown_route(client):
    assert client.get("/unknown-route").status_code == 404
