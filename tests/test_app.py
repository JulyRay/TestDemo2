import pytest
from fastapi.testclient import TestClient

from app import app


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_health_extra_status(client):
    assert client.get("/health-extra").status_code == 200


def test_health_extra_json(client):
    response = client.get("/health-extra")
    assert response.headers["content-type"] == "application/json"
    assert response.json() == {"status": "ok"}


def test_unknown_route(client):
    assert client.get("/does-not-exist").status_code == 404
