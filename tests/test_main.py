import pytest
from app.main import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.get_json()["message"] == "Secure App API running"

def test_echo_valid(client):
    response = client.post("/echo", json={"text": "hello"})
    assert response.status_code == 200
    assert response.get_json()["echo"] == "hello"

def test_echo_invalid(client):
    response = client.post("/echo", json={"message": "no text"})
    assert response.status_code == 400
    assert "error" in response.get_json()

