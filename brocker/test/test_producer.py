from fastapi.testclient import TestClient
from src.main import app


def test_producer():
    client = TestClient(app)
    response_post = client.post(
        "/meme/push/",
        json={"text": "Надел мужик шляпу, а она ему как раз"}
    )
    assert response_post.status_code == 200
    response_get = client.get("/meme/rating/1")
    assert response_get.status_code == 200
    assert response_get.json() == '0'
