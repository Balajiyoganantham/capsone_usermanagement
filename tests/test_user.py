import json
from base64 import b64encode
from tests.conftest import seed_user

def get_auth_headers(username, password):
    credentials = b64encode(f"{username}:{password}".encode()).decode("utf-8")
    return {"Authorization": f"Basic {credentials}"}

def test_get_users(client, app):
    # Seed a user for authentication.
    seed_user(app, "testuser", "password", "test@example.com", "Test User")
    headers = get_auth_headers("testuser", "password")
    
    response = client.get("/users", headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data["users"], list)

def test_get_user_by_id(client, app):
    # Seed a user and get its id.
    user_id = seed_user(app, "testuser", "password", "test@example.com", "Test User")
    headers = get_auth_headers("testuser", "password")
    
    response = client.get(f"/users/{user_id}", headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    # Check that the fetched user's username is correct.
    assert data["username"] == "testuser"
