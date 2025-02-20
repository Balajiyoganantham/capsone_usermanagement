import json

def test_login_success(client):
    """Test successful login"""
    response = client.post("/login", json={"username": "balaji1", "password": "balaji"})
    assert response.status_code == 200
    data = response.get_json()
    assert "Login successful" in data["message"]

def test_login_fail(client):
    """Test login failure with wrong credentials"""
    response = client.post("/login", json={"username": "testuser", "password": "wrongpassword"})
    assert response.status_code == 401
    data = response.get_json()
    assert "Unauthorized" in data["message"]
