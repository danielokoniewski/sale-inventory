import pytest
from fastapi import Cookie
from fastapi.testclient import TestClient

from sale_inventory.main import app
from sale_inventory.repository import ListRepository
from sale_inventory.router import set_repository


@pytest.fixture(scope="module")
def app_client():
    client = TestClient(app=app)

    yield client


def test_user_no_auth(app_client):
    result = app_client.get("/user")
    assert result.status_code == 401


def test_logout_no_auth(app_client):
    result = app_client.post("/logout")
    assert result.status_code == 401


def test_token_failed(app_client):
    result = app_client.post(
        "/token",
        data={"username": "johndoe", "password": "secret"},
        headers={"content-type": "application/x-www-form-urlencoded"})

    assert result.status_code == 401


def test_token_ok(app_client):
    result = app_client.post(
        "/token",
        data={"username": "testuser", "password": "fakepassword"},
        headers={"content-type": "application/x-www-form-urlencoded"})

    assert result.status_code == 200
    assert "Set-Cookie" in result.headers
    assert "token=" in result.headers["Set-Cookie"]


@pytest.fixture(scope="module")
def app_client_with_token():
    client = TestClient(app=app)
    result = client.post(
        "/token",
        data={"username": "testuser", "password": "fakepassword"},
        headers={"content-type": "application/x-www-form-urlencoded"})
    cookies = result.cookies
    client = TestClient(app=app, cookies=cookies)
    yield client


def test_user_ok(app_client_with_token):
    result = app_client_with_token.get("/user")

    assert result.status_code == 200
    assert result.json()["username"] == "testuser"


def test_logout_ok(app_client_with_token):
    result = app_client_with_token.post("/logout")

    assert result.status_code == 200
