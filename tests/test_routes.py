import pytest
from fastapi.testclient import TestClient

from sale_inventory.main import app
from sale_inventory.repository import ListRepository
from sale_inventory.router import set_repository


@pytest.fixture(scope="module")
def app_client():
    repo = ListRepository()
    set_repository(repo)
    client = TestClient(app=app)

    yield client


def test_get_empty_list(app_client):
    result = app_client.get("/items")
    assert result.json() == []


def test_add_item_validation_error(app_client):
    result = app_client.post("/items",
                             json={'name': "test"})
    assert result.status_code == 422


def test_add_item(app_client):
    result = app_client.post("/items",
                             json={
                                 "name": "string",
                                 "description": "string",
                                 "owner": "string",
                                 "expiration_date": "2023-11-15",
                                 "shipping": "string",
                                 "price": 0
                             })
    assert result.status_code == 201
    assert result.json()["id"] == 1

    result = app_client.post("/items",
                             json={
                                 "name": "string",
                                 "description": "string",
                                 "owner": "string",
                                 "expiration_date": "2023-11-15",
                                 "shipping": "string",
                                 "price": 0
                             })
    assert result.status_code == 201
    assert result.json()["id"] == 2


def test_get_item_not_exists(app_client):
    result = app_client.get("/items/3")
    assert result.status_code == 404


def test_get_item_ok(app_client):
    result = app_client.get("/items/1")
    assert result.json()["id"] == 1
    assert result.status_code == 200


def test_change_item_not_exists(app_client):
    result = app_client.put("/items/3",
                            json={
                                "name": "string",
                                "description": "string",
                                "owner": "string",
                                "expiration_date": "2023-11-15",
                                "shipping": "string",
                                "price": 0,
                                "id": 3
                            })
    assert result.status_code == 404


def test_change_item_wrong_id(app_client):
    result = app_client.put("/items/3",
                            json={
                                "name": "string",
                                "description": "string",
                                "owner": "string",
                                "expiration_date": "2023-11-15",
                                "shipping": "string",
                                "price": 0,
                                "id": 1
                            })
    assert result.status_code == 400


def test_change_item_ok(app_client):
    result = app_client.put("/items/1",
                            json={
                                "name": "string1",
                                "description": "string",
                                "owner": "string",
                                "expiration_date": "2023-11-15",
                                "shipping": "string",
                                "price": 0,
                                "id": 1
                            })
    assert result.status_code == 202
    assert result.json()["name"] == "string1"


def test_delete_item_ok(app_client):
    result = app_client.delete("/items/1")
    assert result.status_code == 204


def test_delete_item__not_exists_ok(app_client):
    result = app_client.delete("/items/1")
    assert result.status_code == 404


def test_get_not_empty_list(app_client):
    result = app_client.get("/items")
    item_list = result.json()
    assert len(item_list) == 1
    assert [y["id"] for y in item_list] == [2]
