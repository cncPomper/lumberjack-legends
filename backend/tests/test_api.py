from fastapi.testclient import TestClient
from app.main import app
from app.db import db, _initial_users

client = TestClient(app)

def setup_module(module):
    # Reset DB before tests
    db.users = [u.copy() for u in _initial_users]
    db.sessions = []

def test_read_main():
    response = client.get("/leaderboard")
    assert response.status_code == 200
    assert response.json()["success"] == True

def test_signup():
    response = client.post("/auth/signup", json={
        "username": "NewUser",
        "email": "new@user.com",
        "password": "password123"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["success"] == True
    assert data["user"]["username"] == "NewUser"
    assert "token" in data

def get_auth_token():
    # First signup or use existing
    response = client.post("/auth/login", json={
        "email": "king@forest.com",
        "password": "password"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert "token" in data
    return data["token"]

def test_login():
    token = get_auth_token()
    assert token is not None

def test_get_me():
    token = get_auth_token()
    response = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert data["user"]["email"] == "king@forest.com"

def test_game_session():
    token = get_auth_token()
    # Start session
    response = client.post("/game/session", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    data = response.json()
    assert data["success"] == True
    session_id = data["session"]["id"]

    # End session
    response = client.post(f"/game/session/{session_id}/end", json={
        "score": 100,
        "chops": 50,
        "duration": 60.0
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert data["session"]["score"] == 100

def test_leaderboard_update():
    token = get_auth_token()
    # Submit score
    response = client.post("/leaderboard", json={
        "score": 3000,
        "chops": 100
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    
    # Check if ForestKing is #1 (he had 2500, now 3000)
    entries = data["entries"]
    assert entries[0]["username"] == "ForestKing"
    assert entries[0]["score"] == 3000
