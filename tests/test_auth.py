import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Test user credentials
TEST_USER = {
    "email": "test@example.com",
    "username": "testuser",
    "full_name": "Test User",
    "password": "testpassword",
    "phone": None,
    "location": "Mumbai"
}

@pytest.mark.asyncio
async def test_signup():
    """Test user registration"""
    response = client.post("/auth/signup", json=TEST_USER)
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == TEST_USER["username"]
    assert data["email"] == TEST_USER["email"]

@pytest.mark.asyncio
async def test_login():
    """Test user login"""
    login_data = {"username": TEST_USER["username"], "password": TEST_USER["password"]}
    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data

@pytest.mark.asyncio
async def test_protected_route():
    """Test accessing a protected route"""
    login_data = {"username": TEST_USER["username"], "password": TEST_USER["password"]}
    login_response = client.post("/auth/login", json=login_data)
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/auth/protected", headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Access granted"