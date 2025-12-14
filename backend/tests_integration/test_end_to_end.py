"""End-to-end integration tests for complete user workflows."""
import pytest # type: ignore
from app import db_models


class TestCompleteUserJourney:
    """Tests simulating complete user journeys from signup to gameplay."""

    def test_new_user_complete_flow(self, client, db_session):
        """Test complete flow: signup -> login -> play game -> check stats -> view leaderboard."""
        
        # Step 1: Signup
        signup_response = client.post("/api/auth/signup", json={
            "username": "newplayer",
            "email": "newplayer@test.com",
            "password": "securepass123"
        })
        assert signup_response.status_code == 201
        signup_data = signup_response.json()
        assert signup_data["success"] is True
        token = signup_data["token"]
        user_id = signup_data["user"]["id"]
        
        # Set auth header
        client.headers = {"Authorization": f"Bearer {token}"}
        
        # Step 2: Verify profile
        me_response = client.get("/api/auth/me")
        assert me_response.status_code == 200
        assert me_response.json()["user"]["username"] == "newplayer"
        
        # Step 3: Play first game
        session1_response = client.post("/api/game/session")
        session1_id = session1_response.json()["session"]["id"]
        
        end1_response = client.post(f"/api/game/session/{session1_id}/end", json={
            "score": 2500,
            "chops": 125,
            "duration": 150.0
        })
        assert end1_response.status_code == 200
        
        # Step 4: Check stats after first game
        stats_response = client.get("/api/game/stats")
        stats = stats_response.json()["stats"]
        assert stats["totalGames"] == 1
        assert stats["topScore"] == 2500
        
        # Step 5: Play second game (higher score)
        session2_response = client.post("/api/game/session")
        session2_id = session2_response.json()["session"]["id"]
        
        end2_response = client.post(f"/api/game/session/{session2_id}/end", json={
            "score": 4000,
            "chops": 200,
            "duration": 200.0
        })
        assert end2_response.status_code == 200
        
        # Step 6: Verify stats updated
        stats_response2 = client.get("/api/game/stats")
        stats2 = stats_response2.json()["stats"]
        assert stats2["totalGames"] == 2
        assert stats2["topScore"] == 4000
        
        # Step 7: Submit score to leaderboard
        leaderboard_response = client.post("/api/leaderboard", json={
            "score": 5000,
            "chops": 250
        })
        assert leaderboard_response.status_code == 200
        
        # Step 8: View leaderboard
        view_leaderboard = client.get("/api/leaderboard")
        assert view_leaderboard.status_code == 200
        
        # Step 9: Update profile
        update_response = client.patch("/api/auth/profile", json={
            "username": "proplayer"
        })
        assert update_response.status_code == 200
        assert update_response.json()["user"]["username"] == "proplayer"
        
        # Step 10: Logout
        logout_response = client.post("/api/auth/logout")
        assert logout_response.status_code == 200
        
        # Verify final database state
        user = db_session.query(db_models.User).filter(
            db_models.User.id == user_id
        ).first()
        assert user.username == "proplayer"
        assert user.games_played == 3  # 2 game sessions + 1 leaderboard submit
        assert user.high_score == 5000
        assert user.total_chops == 125 + 200 + 250

    def test_returning_user_flow(self, client, test_user):
        """Test returning user: login -> play -> logout."""
        
        # Step 1: Login
        login_response = client.post("/api/auth/login", json={
            "email": test_user["email"],
            "password": "testpassword"
        })
        assert login_response.status_code == 200
        token = login_response.json()["token"]
        
        client.headers = {"Authorization": f"Bearer {token}"}
        
        # Step 2: Check existing stats
        stats_before = client.get("/api/game/stats").json()["stats"]
        
        # Step 3: Play a game
        session_resp = client.post("/api/game/session")
        session_id = session_resp.json()["session"]["id"]
        
        client.post(f"/api/game/session/{session_id}/end", json={
            "score": 3000,
            "chops": 150,
            "duration": 180.0
        })
        
        # Step 4: Verify stats updated
        stats_after = client.get("/api/game/stats").json()["stats"]
        assert stats_after["totalGames"] == stats_before["totalGames"] + 1
        
        # Step 5: Logout
        logout_resp = client.post("/api/auth/logout")
        assert logout_resp.status_code == 200


class TestMultiUserCompetition:
    """Tests simulating multiple users competing on leaderboard."""

    def test_multiple_users_competing(self, client, db_session):
        """Test multiple users signing up and competing for top rank."""
        users = []
        
        # Create 5 users
        for i in range(5):
            signup_resp = client.post("/api/auth/signup", json={
                "username": f"competitor{i}",
                "email": f"comp{i}@test.com",
                "password": "password"
            })
            token = signup_resp.json()["token"]
            user_id = signup_resp.json()["user"]["id"]
            users.append({"id": user_id, "token": token, "username": f"competitor{i}"})
        
        # Each user plays games with different scores
        scores = [5000, 3000, 8000, 6000, 4000]
        
        for user, score in zip(users, scores):
            client.headers = {"Authorization": f"Bearer {user['token']}"}
            
            # Play a game
            session_resp = client.post("/api/game/session")
            session_id = session_resp.json()["session"]["id"]
            
            client.post(f"/api/game/session/{session_id}/end", json={
                "score": score,
                "chops": score // 20,
                "duration": 120.0
            })
        
        # Check leaderboard (no auth needed)
        client.headers = {}
        leaderboard_resp = client.get("/api/leaderboard")
        entries = leaderboard_resp.json()["entries"]
        
        # Verify ordering: competitor2 (8000) should be first
        assert entries[0]["username"] == "competitor2"
        assert entries[0]["score"] == 8000
        assert entries[0]["rank"] == 1
        
        assert entries[1]["username"] == "competitor3"
        assert entries[1]["score"] == 6000


class TestEdgeCases:
    """Tests for edge cases and error scenarios."""

    def test_user_without_games_on_leaderboard(self, client, test_user):
        """Test that user appears on leaderboard even without playing games."""
        # User exists but check they appear on leaderboard
        response = client.get("/api/leaderboard?limit=100")
        entries = response.json()["entries"]
        
        user_found = any(e["id"] == test_user["id"] for e in entries)
        assert user_found

    def test_concurrent_game_sessions(self, authenticated_client):
        """Test creating multiple active sessions (edge case)."""
        client, token, test_user = authenticated_client
        
        # Create multiple sessions without ending them
        session_ids = []
        for _ in range(3):
            resp = client.post("/api/game/session")
            session_ids.append(resp.json()["session"]["id"])
        
        # All sessions should be created
        assert len(session_ids) == 3
        assert len(set(session_ids)) == 3  # All unique
        
        # End all sessions
        for session_id in session_ids:
            resp = client.post(f"/api/game/session/{session_id}/end", json={
                "score": 1000,
                "chops": 50,
                "duration": 60.0
            })
            assert resp.status_code == 200

    def test_zero_score_submission(self, authenticated_client):
        """Test submitting a game with zero score."""
        client, token, test_user = authenticated_client
        
        session_resp = client.post("/api/game/session")
        session_id = session_resp.json()["session"]["id"]
        
        response = client.post(f"/api/game/session/{session_id}/end", json={
            "score": 0,
            "chops": 0,
            "duration": 10.0
        })
        
        assert response.status_code == 200
        assert response.json()["success"] is True

    def test_very_long_game_duration(self, authenticated_client):
        """Test ending game with very long duration."""
        client, token, test_user = authenticated_client
        
        session_resp = client.post("/api/game/session")
        session_id = session_resp.json()["session"]["id"]
        
        response = client.post(f"/api/game/session/{session_id}/end", json={
            "score": 50000,
            "chops": 2500,
            "duration": 3600.0  # 1 hour
        })
        
        assert response.status_code == 200
        assert response.json()["session"]["duration"] == 3600.0


class TestDataPersistence:
    """Tests for data persistence across requests."""

    def test_user_data_persists_across_sessions(self, client, db_session):
        """Test that user data persists after logout and login."""
        
        # Signup and play game
        signup_resp = client.post("/api/auth/signup", json={
            "username": "persistent",
            "email": "persist@test.com",
            "password": "password"
        })
        token1 = signup_resp.json()["token"]
        
        client.headers = {"Authorization": f"Bearer {token1}"}
        
        # Play a game
        session_resp = client.post("/api/game/session")
        session_id = session_resp.json()["session"]["id"]
        
        client.post(f"/api/game/session/{session_id}/end", json={
            "score": 7777,
            "chops": 388,
            "duration": 200.0
        })
        
        # Get stats
        stats1 = client.get("/api/game/stats").json()["stats"]
        
        # Logout (simulated by removing auth)
        client.headers = {}
        
        # Login again
        login_resp = client.post("/api/auth/login", json={
            "email": "persist@test.com",
            "password": "password"
        })
        token2 = login_resp.json()["token"]
        
        client.headers = {"Authorization": f"Bearer {token2}"}
        
        # Check stats again - should be the same
        stats2 = client.get("/api/game/stats").json()["stats"]
        
        assert stats2["totalGames"] == stats1["totalGames"]
        assert stats2["topScore"] == stats1["topScore"]
        assert stats2["topScore"] == 7777

    def test_leaderboard_reflects_latest_scores(self, client, db_session):
        """Test that leaderboard always shows latest high scores."""
        
        # Create user and play multiple games
        signup_resp = client.post("/api/auth/signup", json={
            "username": "climber",
            "email": "climber@test.com",
            "password": "password"
        })
        token = signup_resp.json()["token"]
        user_id = signup_resp.json()["user"]["id"]
        
        client.headers = {"Authorization": f"Bearer {token}"}
        
        # Play games with increasing scores
        scores = [1000, 2000, 3000, 2500, 4000]
        
        for score in scores:
            session_resp = client.post("/api/game/session")
            session_id = session_resp.json()["session"]["id"]
            
            client.post(f"/api/game/session/{session_id}/end", json={
                "score": score,
                "chops": 50,
                "duration": 60.0
            })
        
        # Check leaderboard
        client.headers = {}
        leaderboard_resp = client.get("/api/leaderboard")
        entries = leaderboard_resp.json()["entries"]
        
        user_entry = next((e for e in entries if e["id"] == user_id), None)
        assert user_entry is not None
        assert user_entry["score"] == 4000  # Highest score


class TestAuthenticationFlow:
    """Tests for authentication token flow."""

    def test_token_reuse_multiple_endpoints(self, client, test_user):
        """Test using same token across multiple endpoints."""
        
        # Login once
        login_resp = client.post("/api/auth/login", json={
            "email": test_user["email"],
            "password": "testpassword"
        })
        token = login_resp.json()["token"]
        
        client.headers = {"Authorization": f"Bearer {token}"}
        
        # Use token for multiple endpoints
        endpoints = [
            ("/api/auth/me", "get"),
            ("/api/game/stats", "get"),
            ("/api/game/session", "post"),
        ]
        
        for endpoint, method in endpoints:
            if method == "get":
                resp = client.get(endpoint)
            else:
                resp = client.post(endpoint)
            
            assert resp.status_code in [200, 201]

    def test_invalid_token_rejected(self, client):
        """Test that invalid tokens are properly rejected."""
        
        client.headers = {"Authorization": "Bearer invalidtoken"}
        
        # Test GET endpoints
        get_endpoints = [
            "/api/auth/me",
            "/api/game/stats",
        ]
        
        for endpoint in get_endpoints:
            resp = client.get(endpoint)
            assert resp.status_code == 401
        
        # Test POST endpoints
        post_endpoints = [
            "/api/game/session",
        ]
        
        for endpoint in post_endpoints:
            resp = client.post(endpoint)
            assert resp.status_code == 401
