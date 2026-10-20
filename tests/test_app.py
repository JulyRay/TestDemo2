import pytest
from fastapi.testclient import TestClient

from app import app


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


def test_health_exact_response(client):
    response = client.get("/planner-health")
    assert response.status_code == 200
    body = response.json()
    assert body == {"status": "ok", "planner_version": 1}
    assert type(body["planner_version"]) is int


@pytest.mark.parametrize("character", ["a", "é", "界", "😀"])
@pytest.mark.parametrize("length", [1, 16, 17])
def test_echo_code_point_boundaries(client, character, length):
    text = character * length
    assert len(text) == length
    response = client.get("/planner-echo", params={"text": text})
    if length == 17:
        assert response.status_code == 422
    else:
        assert response.status_code == 200
        assert response.json() == {"text": text}
        assert type(response.json()["text"]) is str


@pytest.mark.parametrize("params", [{}, {"text": ""}])
def test_echo_requires_nonempty_text(client, params):
    assert client.get("/planner-echo", params=params).status_code == 422


@pytest.mark.parametrize(
    "text",
    [" ", " " * 16, "\t hello\n", "\u2003", "e\u0301" * 8, "😀" * 14 + " \n"],
)
def test_echo_preserves_strings_and_whitespace(client, text):
    response = client.get("/planner-echo", params={"text": text})
    assert response.status_code == 200
    assert response.json() == {"text": text}
    assert type(response.json()["text"]) is str


@pytest.mark.parametrize("text", [" " * 17, "a" * 16 + " ", "e\u0301" * 8 + "\n"])
def test_echo_counts_whitespace_toward_limit(client, text):
    assert len(text) == 17
    assert client.get("/planner-echo", params={"text": text}).status_code == 422


@pytest.mark.parametrize(
    "path", ["/", "/unknown", "/health", "/echo", "/docs", "/redoc", "/openapi.json"]
)
def test_absent_routes(client, path):
    response = client.get(path)
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}
