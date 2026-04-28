import pytest
from app.main import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health_returns_200(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "healthy"}


def test_get_items_returns_list(client):
    response = client.get("/api/items")
    assert response.status_code == 200
    data = response.get_json()
    assert "items" in data
    assert isinstance(data["items"], list)
    assert len(data["items"]) == 2


def test_create_item_success(client):
    response = client.post(
        "/api/items",
        json={"name": "Widget C"},
        content_type="application/json",
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["item"]["name"] == "Widget C"


def test_create_item_missing_name(client):
    response = client.post(
        "/api/items",
        json={"description": "no name here"},
        content_type="application/json",
    )
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_create_item_empty_body(client):
    response = client.post("/api/items", data="", content_type="application/json")
    assert response.status_code == 400


def test_create_item_empty_name(client):
    response = client.post(
        "/api/items",
        json={"name": "   "},
        content_type="application/json",
    )
    assert response.status_code == 400
