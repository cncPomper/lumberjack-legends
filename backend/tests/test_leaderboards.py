def test_health_endpoint(client):
    """Test the health check endpoint for monitoring"""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "lumberjack-legends"

def test_read_main(client):
    response = client.get("/api/leaderboard")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert isinstance(data["entries"], list)
    # We seeded 4 test users
    assert len(data["entries"]) == 4
    # Verify the top user is PaulBunyan (score 5000)
    assert data["entries"][0]["username"] == "PaulBunyan"
    assert data["entries"][0]["score"] == 5000

def test_game_session_flow(client, auth_token):
    # 1. Start Session
    response = client.post("/api/game/session", 
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["success"] == True
    session_id = data["session"]["id"]
    assert session_id is not None

    # 2. End Session
    response = client.post(f"/api/game/session/{session_id}/end", 
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "score": 100,
            "chops": 10,
            "duration": 60
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert data["session"]["score"] == 100
    assert data["session"]["endedAt"] is not None

def test_leaderboard_update(client, auth_token):
    # Submit a high score via the direct leaderboard endpoint
    response = client.post("/api/leaderboard", 
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "score": 9999,
            "chops": 100,
            "duration": 60,
            "golden_trees": 5,
            "trees_chopped": 100
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    
    # Check if we are in the entries returned
    entries = data["entries"]
    entry = next((item for item in entries if item["username"] == "ForestKing"), None)
    assert entry is not None
    assert entry["score"] == 9999

    # Verify with a separate GET request
    response = client.get("/api/leaderboard")
    assert response.status_code == 200
    data = response.json()
    entries = data["entries"]
    entry = next((item for item in entries if item["username"] == "ForestKing"), None)
    assert entry is not None
    assert entry["score"] == 9999
