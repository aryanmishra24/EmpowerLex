import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.case_schema import CaseCreate, GenerateCaseRequest, FeedbackCreate
from app.models.user_schema import UserCreate
from datetime import datetime

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

def get_auth_token():
    # Sign up (ignore if already exists)
    client.post("/auth/signup", json=TEST_USER)
    # Log in
    login_data = {"username": TEST_USER["username"], "password": TEST_USER["password"]}
    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 200
    return response.json()["access_token"]

def auth_headers():
    token = get_auth_token()
    return {"Authorization": f"Bearer {token}"}

# Mock case data
mock_case = CaseCreate(
    title="Test Case",
    description="This is a test case description.",
    category="Consumer Protection",
    priority="high"
)

# Mock generate case request
mock_generate_request = GenerateCaseRequest(
    title="Test Generate Case",
    description="This is a test generate case description.",
    category="Consumer Protection",
    location="Mumbai"
)

# Mock feedback data
mock_feedback = FeedbackCreate(
    rating=5,
    comments="This is a test feedback comment."
)

@pytest.mark.asyncio
async def test_create_case():
    """Test creating a new case"""
    response = client.post("/cases/", json=mock_case.model_dump(), headers=auth_headers())
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == mock_case.title
    assert data["category"] == mock_case.category

@pytest.mark.asyncio
async def test_generate_case():
    """Test generating a case without saving"""
    response = client.post("/cases/generate", json=mock_generate_request.model_dump(), headers=auth_headers())
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == mock_generate_request.title
    assert data["category"] == mock_generate_request.category

@pytest.mark.asyncio
async def test_get_case():
    """Test getting a specific case by ID"""
    # First create a case
    create_response = client.post("/cases/", json=mock_case.model_dump(), headers=auth_headers())
    case_id = create_response.json()["id"]
    
    # Then get the case
    response = client.get(f"/cases/{case_id}", headers=auth_headers())
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == case_id
    assert data["title"] == mock_case.title

@pytest.mark.asyncio
async def test_list_cases():
    """Test listing all cases"""
    response = client.get("/cases/", headers=auth_headers())
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

@pytest.mark.asyncio
async def test_create_feedback():
    """Test creating feedback for a case"""
    # First create a case
    create_response = client.post("/cases/", json=mock_case.model_dump(), headers=auth_headers())
    case_id = create_response.json()["id"]
    
    # Then create feedback
    response = client.post(f"/cases/{case_id}/feedback", json=mock_feedback.model_dump(), headers=auth_headers())
    assert response.status_code == 200
    data = response.json()
    assert data["rating"] == mock_feedback.rating
    assert data["comments"] == mock_feedback.comments

@pytest.mark.asyncio
async def test_chat_with_agent():
    """Test chatting with the legal agent"""
    response = client.post("/cases/chat", json={"message": "What are my rights as a consumer?"}, headers=auth_headers())
    assert response.status_code == 200
    data = response.json()
    assert "response" in data 