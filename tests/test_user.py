import json
from base64 import b64encode

def get_auth_headers(username, password):
    """Helper function to create authorization headers"""
    credentials = b64encode(f"{username}:{password}".encode()).decode("utf-8")
    return {"Authorization": f"Basic {credentials}"}

def test_get_users(client):
    """Test fetching users (requires authentication)"""
    headers = get_auth_headers("testuser", "password")
    response = client.get("/users", headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data["users"], list)

def test_get_user_by_id(client):
    """Test fetching a single user by ID"""
    headers = get_auth_headers("testuser", "password")
    response = client.get("/users/1", headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data["username"] == "testuser"

def test_unauthorized_access(client):
    """Test accessing user endpoints without authentication"""
    response = client.get("/users")
    assert response.status_code == 401
