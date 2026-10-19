"""Endpoint contracts, including Unicode code-point boundaries."""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app import app


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_application_has_only_requested_get_routes():
    assert isinstance(app, FastAPI)
    assert len(app.routes) == 2
    assert {(route.path, frozenset(route.methods)) for route in app.routes} == {
        ("/planner-health", frozenset({"GET"})),
        ("/planner-echo", frozenset({"GET"})),
    }


def test_health(client):
    response = client.get("/planner-health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "planner_version": 1}
    assert type(response.json()["planner_version"]) is int


@pytest.mark.parametrize("text", [
    "a", "a" * 16, " ", " " * 16, "  hello \t\n",
    "é" * 16, "😀" * 16, "e\u0301" * 8,
])
def test_echo_preserves_valid_text(client, text):
    response = client.get("/planner-echo", params={"text": text})
    assert response.status_code == 200
    assert response.json() == {"text": text}


@pytest.mark.parametrize("params", [
    {}, {"text": ""}, {"text": "a" * 17}, {"text": " " * 17},
    {"text": "é" * 17}, {"text": "😀" * 17},
    {"text": "e\u0301" * 8 + "e"},
])
def test_echo_rejects_missing_or_invalid_length(client, params):
    assert client.get("/planner-echo", params=params).status_code == 422


@pytest.mark.parametrize("path", ["/unknown", "/docs", "/redoc", "/openapi.json"])
def test_unknown_and_disabled_documentation_routes(client, path):
    assert client.get(path).status_code == 404
