import json
from tests.conftest import seed_user

def test_login_success(client, app):

    seed_user(app, "balaji1", "balaji", "balaji@example.com", "Balaji")

    response = client.post("/login", json={"username": "balaji1", "password": "balaji"})

    assert response.status_code == 200, f"Expected 200 but got {response.status_code}. Response: {response.data}"
    data = response.get_json()
    assert data["message"] == "Login successful"

def test_login_fail(client):
    response = client.post("/login", json={"username": "nonexistent", "password": "wrong"})
    assert response.status_code == 401

    data = response.get_json()
    
    assert data["message"] == "Unauthorized"

