"""Integration tests for game session endpoints."""
import pytest # type: ignore
from datetime import datetime, timezone
from app import db_models


class TestGameSession:
    """Tests for game session management."""

    def test_create_game_session(self, authenticated_client, db_session):
        """Test creating a new game session."""
        client, token, test_user = authenticated_client
        
        response = client.post("/api/game/session")
        
        assert response.status_code == 201
        data = response.json()
        assert data["success"] is True
        assert data["session"]["id"] is not None
        assert data["session"]["userId"] == test_user["id"]
        assert data["session"]["score"] == 0
        assert data["session"]["chops"] == 0
        assert data["session"]["startedAt"] is not None
        assert data["session"]["endedAt"] is None
        
        # Verify session in database
        session = db_session.query(db_models.GameSession).filter(
            db_models.GameSession.id == data["session"]["id"]
        ).first()
        assert session is not None
        assert session.user_id == test_user["id"]

    def test_create_session_without_auth(self, client):
        """Test creating session fails without authentication."""
        response = client.post("/api/game/session")
        
        assert response.status_code == 401

    def test_multiple_sessions_per_user(self, authenticated_client, db_session):
        """Test user can create multiple game sessions."""
        client, token, test_user = authenticated_client
        
        # Create first session
        response1 = client.post("/api/game/session")
        session1_id = response1.json()["session"]["id"]
        
        # Create second session
        response2 = client.post("/api/game/session")
        session2_id = response2.json()["session"]["id"]
        
        assert session1_id != session2_id
        
        # Verify both exist in database
        sessions = db_session.query(db_models.GameSession).filter(
            db_models.GameSession.user_id == test_user["id"]
        ).all()
        assert len(sessions) >= 2


class TestEndSession:
    """Tests for ending game sessions."""

    def test_end_game_session_successfully(self, authenticated_client, db_session):
        """Test ending a game session updates database correctly."""
        client, token, test_user = authenticated_client
        
        # Create session
        create_response = client.post("/api/game/session")
        session_id = create_response.json()["session"]["id"]
        
        # Get initial user stats
        initial_games_played = test_user["gamesPlayed"]
        initial_total_chops = test_user["totalChops"]
        initial_high_score = test_user["highScore"]
        
        # End session
        response = client.post(f"/api/game/session/{session_id}/end", json={
            "score": 1500,
            "chops": 75,
            "duration": 120.5
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["session"]["score"] == 1500
        assert data["session"]["chops"] == 75
        assert data["session"]["duration"] == 120.5
        assert data["session"]["endedAt"] is not None
        
        # Verify session in database
        session = db_session.query(db_models.GameSession).filter(
            db_models.GameSession.id == session_id
        ).first()
        assert session.score == 1500
        assert session.chops == 75
        assert session.ended_at is not None
        
        # Verify user stats updated
        user = db_session.query(db_models.User).filter(
            db_models.User.id == test_user["id"]
        ).first()
        assert user.games_played == initial_games_played + 1
        assert user.total_chops == initial_total_chops + 75
        if 1500 > initial_high_score:
            assert user.high_score == 1500

    def test_end_session_updates_high_score(self, authenticated_client, db_session):
        """Test ending session with new high score updates user record."""
        client, token, test_user = authenticated_client
        
        # Create and end session with high score
        create_response = client.post("/api/game/session")
        session_id = create_response.json()["session"]["id"]
        
        new_high_score = test_user["highScore"] + 1000
        response = client.post(f"/api/game/session/{session_id}/end", json={
            "score": new_high_score,
            "chops": 100,
            "duration": 150.0
        })
        
        assert response.status_code == 200
        
        # Verify high score updated
        user = db_session.query(db_models.User).filter(
            db_models.User.id == test_user["id"]
        ).first()
        assert user.high_score == new_high_score

    def test_end_session_doesnt_update_high_score(self, authenticated_client, db_session):
        """Test ending session with low score doesn't change high score."""
        client, token, test_user = authenticated_client
        
        # Create and end session with low score
        create_response = client.post("/api/game/session")
        session_id = create_response.json()["session"]["id"]
        
        initial_high_score = test_user["highScore"]
        low_score = 50  # Lower than initial high score
        
        response = client.post(f"/api/game/session/{session_id}/end", json={
            "score": low_score,
            "chops": 5,
            "duration": 30.0
        })
        
        assert response.status_code == 200
        
        # Verify high score unchanged
        user = db_session.query(db_models.User).filter(
            db_models.User.id == test_user["id"]
        ).first()
        assert user.high_score == initial_high_score

    def test_end_nonexistent_session(self, authenticated_client):
        """Test ending non-existent session returns error."""
        client, token, test_user = authenticated_client
        
        response = client.post("/api/game/session/nonexistent-id/end", json={
            "score": 100,
            "chops": 10,
            "duration": 60.0
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is False
        assert "not found" in data["error"].lower()

    def test_end_session_without_auth(self, client, test_user, db_session):
        """Test ending session fails without authentication."""
        # Create a session directly in database
        session = db_models.GameSession(
            id="test-session",
            user_id=test_user["id"],
            started_at=datetime.now(timezone.utc)
        )
        db_session.add(session)
        db_session.commit()
        
        response = client.post("/api/game/session/test-session/end", json={
            "score": 100,
            "chops": 10,
            "duration": 60.0
        })
        
        assert response.status_code == 401


class TestGameStats:
    """Tests for game statistics endpoint."""

    def test_get_stats(self, authenticated_client):
        """Test getting game statistics for current user."""
        client, token, test_user = authenticated_client
        
        response = client.get("/api/game/stats")
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "stats" in data
        assert "totalGames" in data["stats"]
        assert "avgScore" in data["stats"]
        assert "topScore" in data["stats"]
        assert data["stats"]["totalGames"] == test_user["gamesPlayed"]
        assert data["stats"]["topScore"] == test_user["highScore"]

    def test_get_stats_without_auth(self, client):
        """Test getting stats fails without authentication."""
        response = client.get("/api/game/stats")
        
        assert response.status_code == 401

    def test_stats_update_after_game(self, authenticated_client, db_session):
        """Test that stats endpoint reflects changes after playing a game."""
        client, token, test_user = authenticated_client
        
        # Get initial stats
        response1 = client.get("/api/game/stats")
        initial_stats = response1.json()["stats"]
        
        # Play a game
        create_response = client.post("/api/game/session")
        session_id = create_response.json()["session"]["id"]
        
        client.post(f"/api/game/session/{session_id}/end", json={
            "score": 2000,
            "chops": 100,
            "duration": 180.0
        })
        
        # Get updated stats
        response2 = client.get("/api/game/stats")
        updated_stats = response2.json()["stats"]
        
        assert updated_stats["totalGames"] == initial_stats["totalGames"] + 1
        if 2000 > initial_stats["topScore"]:
            assert updated_stats["topScore"] == 2000

    def test_stats_avg_score_calculation(self, authenticated_client, db_session):
        """Test that average score is calculated correctly."""
        client, token, test_user = authenticated_client
        
        # Get user's total chops and games played
        user = db_session.query(db_models.User).filter(
            db_models.User.id == test_user["id"]
        ).first()
        
        expected_avg = round(user.total_chops / user.games_played) if user.games_played > 0 else 0
        
        response = client.get("/api/game/stats")
        stats = response.json()["stats"]
        
        assert stats["avgScore"] == expected_avg


class TestGameSessionLifecycle:
    """Tests for complete game session lifecycle."""

    def test_complete_game_flow(self, authenticated_client, db_session):
        """Test complete flow: create session, play, end session."""
        client, token, test_user = authenticated_client
        
        # Step 1: Create session
        create_response = client.post("/api/game/session")
        assert create_response.status_code == 201
        session_data = create_response.json()["session"]
        session_id = session_data["id"]
        
        # Verify session is active (not ended)
        assert session_data["endedAt"] is None
        
        # Step 2: End session with game results
        end_response = client.post(f"/api/game/session/{session_id}/end", json={
            "score": 3500,
            "chops": 200,
            "duration": 240.0
        })
        assert end_response.status_code == 200
        ended_session = end_response.json()["session"]
        
        # Verify session is ended
        assert ended_session["endedAt"] is not None
        assert ended_session["score"] == 3500
        
        # Step 3: Verify stats updated
        stats_response = client.get("/api/game/stats")
        stats = stats_response.json()["stats"]
        
        # Total games should have increased
        user = db_session.query(db_models.User).filter(
            db_models.User.id == test_user["id"]
        ).first()
        assert user.games_played > test_user["gamesPlayed"]
        assert user.total_chops >= test_user["totalChops"] + 200

    def test_multiple_game_sessions_sequence(self, authenticated_client, db_session):
        """Test playing multiple games in sequence."""
        client, token, test_user = authenticated_client
        
        initial_games = test_user["gamesPlayed"]
        
        # Play 3 games
        for i in range(3):
            # Create session
            create_resp = client.post("/api/game/session")
            session_id = create_resp.json()["session"]["id"]
            
            # End session
            end_resp = client.post(f"/api/game/session/{session_id}/end", json={
                "score": 1000 + (i * 100),
                "chops": 50 + (i * 10),
                "duration": 120.0
            })
            assert end_resp.status_code == 200
        
        # Verify all games recorded
        user = db_session.query(db_models.User).filter(
            db_models.User.id == test_user["id"]
        ).first()
        assert user.games_played == initial_games + 3
