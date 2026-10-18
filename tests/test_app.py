"""Initial CI fixture intentionally omits the required length64 boundary."""
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_one_and_sixty_three():
    for size in (1, 63):
        text = "x" * size
        response = client.get("/bounded-echo", params={"text": text})
        assert response.status_code == 200
        assert response.json() == {"text": text}


def test_invalid_inputs():
    assert client.get("/bounded-echo").status_code == 422
    for text in ("", "x" * 65):
        assert client.get("/bounded-echo", params={"text": text}).status_code == 422
    assert client.get("/unknown").status_code == 404
