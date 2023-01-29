from starlette.testclient import TestClient


def test_async_sleep(client: TestClient):
    response = client.get("/async_sleep")
    assert response.status_code == 200
    assert response.json() == {"message": "async_sleep"}
