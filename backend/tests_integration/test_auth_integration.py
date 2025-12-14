"""Integration tests for authentication endpoints."""
import pytest # type: ignore
from app import db_models


class TestSignup:
    """Tests for user registration."""

    def test_successful_signup(self, client, db_session):
        """Test successful user registration creates user in database."""
        response = client.post("/api/auth/signup", json={
            "username": "newuser",
            "email": "new@example.com",
            "password": "securepass123"
        })
        
        assert response.status_code == 201
        data = response.json()
        assert data["success"] is True
        assert data["token"] is not None
        assert data["user"]["username"] == "newuser"
        assert data["user"]["email"] == "new@example.com"
        assert "password" not in data["user"] or data["user"]["password"] == ""
        
        # Verify user exists in database
        user = db_session.query(db_models.User).filter(
            db_models.User.email == "new@example.com"
        ).first()
        assert user is not None
        assert user.username == "newuser"
        assert user.high_score == 0
        assert user.total_chops == 0
        assert user.games_played == 0

    def test_signup_duplicate_email(self, client, test_user):
        """Test signup fails with duplicate email."""
        response = client.post("/api/auth/signup", json={
            "username": "different",
            "email": test_user["email"],
            "password": "password123"
        })
        
        assert response.status_code == 201  # Endpoint returns 201 even on error
        data = response.json()
        assert data["success"] is False
        assert "email" in data["error"].lower()

    def test_signup_duplicate_username(self, client, test_user):
        """Test signup fails with duplicate username."""
        response = client.post("/api/auth/signup", json={
            "username": test_user["username"],
            "email": "different@example.com",
            "password": "password123"
        })
        
        assert response.status_code == 201
        data = response.json()
        assert data["success"] is False
        assert "username" in data["error"].lower()

    def test_signup_password_hashed(self, client, db_session):
        """Test that password is properly hashed in database."""
        password = "myplainpassword"
        response = client.post("/api/auth/signup", json={
            "username": "secureuser",
            "email": "secure@example.com",
            "password": password
        })
        
        assert response.status_code == 201
        
        # Check database directly
        user = db_session.query(db_models.User).filter(
            db_models.User.email == "secure@example.com"
        ).first()
        assert user.password != password
        assert len(user.password) > 50  # Hashed password should be longer


class TestLogin:
    """Tests for user login."""

    def test_successful_login(self, client, test_user):
        """Test successful login returns token and user data."""
        response = client.post("/api/auth/login", json={
            "email": test_user["email"],
            "password": "testpassword"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["token"] is not None
        assert data["user"]["id"] == test_user["id"]
        assert data["user"]["username"] == test_user["username"]

    def test_login_wrong_password(self, client, test_user):
        """Test login fails with incorrect password."""
        response = client.post("/api/auth/login", json={
            "email": test_user["email"],
            "password": "wrongpassword"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is False
        assert "invalid" in data["error"].lower()

    def test_login_nonexistent_user(self, client):
        """Test login fails for non-existent user."""
        response = client.post("/api/auth/login", json={
            "email": "nonexistent@example.com",
            "password": "password"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is False

    def test_login_case_insensitive_email(self, client, test_user):
        """Test login works with different email case."""
        response = client.post("/api/auth/login", json={
            "email": test_user["email"].upper(),
            "password": "testpassword"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True


class TestAuthenticatedEndpoints:
    """Tests for endpoints requiring authentication."""

    def test_get_current_user(self, authenticated_client):
        """Test getting current user profile."""
        client, token, test_user = authenticated_client
        
        response = client.get("/api/auth/me")
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["user"]["id"] == test_user["id"]
        assert data["user"]["username"] == test_user["username"]

    def test_get_current_user_without_auth(self, client):
        """Test me endpoint fails without authentication."""
        response = client.get("/api/auth/me")
        
        assert response.status_code == 401

    def test_get_current_user_invalid_token(self, client):
        """Test me endpoint fails with invalid token."""
        client.headers = {"Authorization": "Bearer invalidtoken123"}
        response = client.get("/api/auth/me")
        
        assert response.status_code == 401

    def test_logout(self, authenticated_client):
        """Test logout endpoint."""
        client, token, test_user = authenticated_client
        
        response = client.post("/api/auth/logout")
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    def test_update_profile(self, authenticated_client, db_session):
        """Test updating user profile."""
        client, token, test_user = authenticated_client
        
        response = client.patch("/api/auth/profile", json={
            "username": "updatedname"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["user"]["username"] == "updatedname"
        
        # Verify in database
        user = db_session.query(db_models.User).filter(
            db_models.User.id == test_user["id"]
        ).first()
        assert user.username == "updatedname"


class TestTokenValidation:
    """Tests for JWT token validation and expiration."""

    def test_token_contains_user_id(self, client, test_user):
        """Test that token can be decoded to get user ID."""
        import jwt # type: ignore
        
        response = client.post("/api/auth/login", json={
            "email": test_user["email"],
            "password": "testpassword"
        })
        
        token = response.json()["token"]
        
        # Decode without verification to check payload
        decoded = jwt.decode(token, options={"verify_signature": False})
        assert "sub" in decoded
        assert decoded["sub"] == test_user["id"]
        assert "exp" in decoded

    def test_token_works_across_requests(self, authenticated_client):
        """Test that token can be reused for multiple requests."""
        client, token, test_user = authenticated_client
        
        # Make multiple requests with same token
        response1 = client.get("/api/auth/me")
        response2 = client.get("/api/game/stats")
        
        assert response1.status_code == 200
        assert response2.status_code == 200
