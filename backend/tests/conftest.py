import pytest # type: ignore
from fastapi.testclient import TestClient # type: ignore
from app.main import app
from app.db import db, _initial_users, _initial_sessions

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture(autouse=True)
def reset_db():
    # Reset DB before each test
    db.users = [u.copy() for u in _initial_users]
    db.sessions = [s.copy() for s in _initial_sessions]

@pytest.fixture
def auth_token(client):
    # Helper to get token for existing user
    response = client.post("/api/auth/login", json={
        "email": "king@forest.com",
        "password": "password"
    })
    return response.json()["token"]

@pytest.fixture
def sample_users():
    """Fixture providing sample user data for testing"""
    return {
        "top_player": {"email": "paul@legends.com", "password": "password", "username": "PaulBunyan"},
        "mid_player": {"email": "king@forest.com", "password": "password", "username": "ForestKing"},
        "new_player": {"email": "redwood@rookie.com", "password": "password", "username": "RedwoodRookie"},
    }

@pytest.fixture
def game_session_data():
    """Fixture providing sample game session data for testing"""
    return {
        "high_score": {"score": 9999, "chops": 500, "duration": 300.0},
        "medium_score": {"score": 1500, "chops": 75, "duration": 120.0},
        "low_score": {"score": 100, "chops": 10, "duration": 60.0},
    }
