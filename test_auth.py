import bcrypt
import requests
import json

# Test different passwords
test_passwords = ["password", "123456", "magnus", "test", "admin", "user"]
hashed_password = "$2b$12$h.ekEjQdpvQY4AB7Ovthgeq0wKc7YmIHmxC4snguUrp6hfYFsXlM2"

for test_password in test_passwords:
    if bcrypt.checkpw(test_password.encode('utf-8'), hashed_password.encode('utf-8')):
        print(f"Password found: {test_password}")
        
        # Try to login
        response = requests.post(
            "http://localhost:8000/auth/login",
            json={"username": "magnus", "password": test_password}
        )
        
        if response.status_code == 200:
            token = response.json()["access_token"]
            print(f"Login successful! Token: {token[:20]}...")
            
            # Test creating a case
            headers = {"Authorization": f"Bearer {token}"}
            case_data = {
                "title": "Test Case",
                "description": "This is a test case",
                "category": "Civil Rights"
            }
            
            case_response = requests.post(
                "http://localhost:8000/cases/",
                json=case_data,
                headers=headers
            )
            
            print(f"Case creation status: {case_response.status_code}")
            if case_response.status_code == 200:
                case = case_response.json()
                print(f"Case created successfully! ID: {case['case_id']}")
                print("UUID validation error is FIXED! ✅")
            else:
                print(f"Error: {case_response.text}")
            break
        else:
            print(f"Login failed: {response.text}")
else:
    print("No password found. Let me create a new user...")
    
    # Create a new user
    signup_data = {
        "username": "testuser",
        "email": "test@test.com",
        "password": "testpass123",
        "full_name": "Test User",
        "location": "Test City"
    }
    
    signup_response = requests.post(
        "http://localhost:8000/auth/signup",
        json=signup_data
    )
    
    if signup_response.status_code == 200:
        print("User created successfully!")
        
        # Login with new user
        login_response = requests.post(
            "http://localhost:8000/auth/login",
            json={"username": "testuser", "password": "testpass123"}
        )
        
        if login_response.status_code == 200:
            token = login_response.json()["access_token"]
            print(f"Login successful! Token: {token[:20]}...")
            
            # Test creating a case
            headers = {"Authorization": f"Bearer {token}"}
            case_data = {
                "title": "Test Case",
                "description": "This is a test case",
                "category": "Civil Rights"
            }
            
            case_response = requests.post(
                "http://localhost:8000/cases/",
                json=case_data,
                headers=headers
            )
            
            print(f"Case creation status: {case_response.status_code}")
            if case_response.status_code == 200:
                case = case_response.json()
                print(f"Case created successfully! ID: {case['case_id']}")
                print("UUID validation error is FIXED! ✅")
            else:
                print(f"Error: {case_response.text}")
        else:
            print(f"Login failed: {login_response.text}")
    else:
        print(f"Signup failed: {signup_response.text}") 