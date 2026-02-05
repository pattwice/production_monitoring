from fastapi.testclient import TestClient

def test_register_user_success(client: TestClient):
    """
    Test successful user registration.
    """
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "strongpassword123",
        "full_name": "Test User"
    }

    response = client.post("/api/v1/auth/register", json=user_data)

    assert response.status_code == 201, f"Expected status code 201, but got {response.status_code}"

    response_data = response.json()
    
    assert response_data["email"] == user_data["email"]
    assert response_data["username"] == user_data["username"]
    assert response_data["full_name"] == user_data["full_name"]
    
    assert "password" not in response_data
    assert "hashed_password" not in response_data
    
    assert response_data["is_superuser"] is False
    assert response_data["is_active"] is True
    assert response_data["role"] == "User"
    assert response_data["status"] == "Enabled"
    print("\ntest_register_user_success passed!")


def test_register_user_duplicate_username(client: TestClient):
    """
    Test registration failure when username already exists.
    """
    # First, create a user
    user_data1 = {
        "email": "test1@example.com",
        "username": "duplicateuser",
        "password": "password123"
    }
    response1 = client.post("/api/v1/auth/register", json=user_data1)
    assert response1.status_code == 201, "Setup: Failed to create the initial user."

    # Now, try to create another user with the same username
    user_data2 = {
        "email": "test2@example.com",
        "username": "duplicateuser", # Same username
        "password": "password456"
    }
    response2 = client.post("/api/v1/auth/register", json=user_data2)

    # Assert that the request fails with a 400 Bad Request
    assert response2.status_code == 400
    assert "Email or username already registered" in response2.json()["detail"]
    print("\ntest_register_user_duplicate_username passed!")
