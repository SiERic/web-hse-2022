from time import sleep
import pexpect

from fastapi.testclient import TestClient
from src.main import app


def test_producer():
    client = TestClient(app)
    response_post = client.post(
        "/meme/push/",
        json={"text": "Надел мужик шляпу, а она ему как раз"}
    )
    assert response_post.status_code == 200
    assert response_post.json() == 1
    response_get = client.get("/meme/rating/1")
    assert response_get.status_code == 200
    assert response_get.json() == 0


def test_integration():
    child = pexpect.spawn("python3 ../src/consumer.py")
    child.expect_exact("CONGRATULATIONS !!! YOU ARE A MEME RATER !!!")

    client = TestClient(app)

    sleep(2)

    text = "I failed math so many times at school, I can't even count"
    response_post = client.post(
        "/meme/push/",
        json={"text": text}
    )
    assert response_post.status_code == 200
    assert response_post.json() == 1

    sleep(3)

    child.expect_exact("Rate this meme (0/1, 1 = like)")
    child.expect_exact(f"(id: 1): {text}")
    child.sendline("1")

    response_get = client.get("/meme/rating/1")
    assert response_get.status_code == 200
    print(response_get.json())
    assert response_get.json() == 1
