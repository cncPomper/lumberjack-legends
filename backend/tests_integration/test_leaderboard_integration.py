"""Integration tests for leaderboard endpoints."""
import pytest # type: ignore
from app import db_models


class TestLeaderboardRetrieval:
    """Tests for retrieving leaderboard data."""

    def test_get_leaderboard_default(self, client, multiple_users):
        """Test getting leaderboard with default limit."""
        response = client.get("/api/leaderboard")
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "entries" in data
        assert len(data["entries"]) == 10  # Default limit
        
        # Verify entries are sorted by score (descending)
        scores = [entry["score"] for entry in data["entries"]]
        assert scores == sorted(scores, reverse=True)
        
        # Verify rank assignment
        for i, entry in enumerate(data["entries"]):
            assert entry["rank"] == i + 1

    def test_get_leaderboard_custom_limit(self, client, multiple_users):
        """Test getting leaderboard with custom limit."""
        response = client.get("/api/leaderboard?limit=5")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["entries"]) == 5

    def test_get_leaderboard_max_limit(self, client, multiple_users):
        """Test leaderboard respects maximum limit."""
        response = client.get("/api/leaderboard?limit=100")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["entries"]) <= 100

    def test_get_leaderboard_min_limit(self, client, multiple_users):
        """Test leaderboard respects minimum limit."""
        response = client.get("/api/leaderboard?limit=1")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["entries"]) == 1
        
        # Should be the top player
        assert data["entries"][0]["rank"] == 1

    def test_leaderboard_entry_structure(self, client, multiple_users):
        """Test that leaderboard entries have correct structure."""
        response = client.get("/api/leaderboard")
        
        data = response.json()
        entry = data["entries"][0]
        
        # Verify all required fields present
        assert "id" in entry
        assert "username" in entry
        assert "score" in entry
        assert "chops" in entry
        assert "rank" in entry
        assert "timestamp" in entry
        
        # Verify types
        assert isinstance(entry["score"], int)
        assert isinstance(entry["chops"], int)
        assert isinstance(entry["rank"], int)

    def test_leaderboard_empty_database(self, client):
        """Test leaderboard with no users."""
        response = client.get("/api/leaderboard")
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["entries"] == []

    def test_leaderboard_no_auth_required(self, client, multiple_users):
        """Test that leaderboard can be accessed without authentication."""
        response = client.get("/api/leaderboard")
        
        assert response.status_code == 200
        assert response.json()["success"] is True


class TestScoreSubmission:
    """Tests for submitting scores to leaderboard."""

    def test_submit_score_successfully(self, authenticated_client, db_session):
        """Test submitting a score updates user stats and returns leaderboard."""
        client, token, test_user = authenticated_client
        
        initial_total_chops = test_user["totalChops"]
        initial_games_played = test_user["gamesPlayed"]
        
        response = client.post("/api/leaderboard", json={
            "score": 2500,
            "chops": 125
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "entries" in data
        
        # Verify user stats updated in database
        user = db_session.query(db_models.User).filter(
            db_models.User.id == test_user["id"]
        ).first()
        assert user.total_chops == initial_total_chops + 125
        assert user.games_played == initial_games_played + 1

    def test_submit_new_high_score(self, authenticated_client, db_session):
        """Test submitting a new high score updates user record."""
        client, token, test_user = authenticated_client
        
        initial_high_score = test_user["highScore"]
        new_high_score = initial_high_score + 1000
        
        response = client.post("/api/leaderboard", json={
            "score": new_high_score,
            "chops": 200
        })
        
        assert response.status_code == 200
        
        # Verify high score updated
        user = db_session.query(db_models.User).filter(
            db_models.User.id == test_user["id"]
        ).first()
        assert user.high_score == new_high_score

    def test_submit_lower_score_no_high_score_update(self, authenticated_client, db_session):
        """Test submitting lower score doesn't update high score."""
        client, token, test_user = authenticated_client
        
        initial_high_score = test_user["highScore"]
        lower_score = 50
        
        response = client.post("/api/leaderboard", json={
            "score": lower_score,
            "chops": 25
        })
        
        assert response.status_code == 200
        
        # Verify high score unchanged
        user = db_session.query(db_models.User).filter(
            db_models.User.id == test_user["id"]
        ).first()
        assert user.high_score == initial_high_score

    def test_submit_score_increments_games_played(self, authenticated_client, db_session):
        """Test that submitting score increments games played counter."""
        client, token, test_user = authenticated_client
        
        initial_games = test_user["gamesPlayed"]
        
        # Submit multiple scores
        for _ in range(3):
            client.post("/api/leaderboard", json={
                "score": 1000,
                "chops": 50
            })
        
        # Verify games played increased
        user = db_session.query(db_models.User).filter(
            db_models.User.id == test_user["id"]
        ).first()
        assert user.games_played == initial_games + 3

    def test_submit_score_accumulates_chops(self, authenticated_client, db_session):
        """Test that submitting scores accumulates total chops."""
        client, token, test_user = authenticated_client
        
        initial_chops = test_user["totalChops"]
        
        # Submit multiple scores
        chop_amounts = [100, 150, 200]
        for chops in chop_amounts:
            client.post("/api/leaderboard", json={
                "score": 1000,
                "chops": chops
            })
        
        # Verify total chops accumulated
        user = db_session.query(db_models.User).filter(
            db_models.User.id == test_user["id"]
        ).first()
        assert user.total_chops == initial_chops + sum(chop_amounts)

    def test_submit_score_without_auth(self, client):
        """Test submitting score fails without authentication."""
        response = client.post("/api/leaderboard", json={
            "score": 1000,
            "chops": 50
        })
        
        assert response.status_code == 401

    def test_submit_score_returns_updated_leaderboard(self, authenticated_client, multiple_users):
        """Test that submitting score returns current leaderboard."""
        client, token, test_user = authenticated_client
        
        response = client.post("/api/leaderboard", json={
            "score": 10000,  # Very high score
            "chops": 500
        })
        
        assert response.status_code == 200
        data = response.json()
        
        # Should return leaderboard
        assert "entries" in data
        assert len(data["entries"]) > 0


class TestLeaderboardRankings:
    """Tests for leaderboard ranking logic."""

    def test_leaderboard_sorted_by_high_score(self, client, db_session):
        """Test that leaderboard is sorted by high score descending."""
        from app.auth_utils import hash_password
        
        # Create users with specific scores
        users_data = [
            ("user1", "user1@test.com", 5000),
            ("user2", "user2@test.com", 3000),
            ("user3", "user3@test.com", 8000),
            ("user4", "user4@test.com", 1000),
        ]
        
        for username, email, score in users_data:
            user = db_models.User(
                id=f"id-{username}",
                username=username,
                email=email,
                password=hash_password("password"),
                high_score=score,
                total_chops=score * 10,
                games_played=10
            )
            db_session.add(user)
        db_session.commit()
        
        response = client.get("/api/leaderboard")
        entries = response.json()["entries"]
        
        # Verify order
        assert entries[0]["username"] == "user3"  # 8000
        assert entries[1]["username"] == "user1"  # 5000
        assert entries[2]["username"] == "user2"  # 3000
        assert entries[3]["username"] == "user4"  # 1000

    def test_leaderboard_rank_assignment(self, client, multiple_users):
        """Test that ranks are assigned correctly (1, 2, 3, ...)."""
        response = client.get("/api/leaderboard")
        entries = response.json()["entries"]
        
        for i, entry in enumerate(entries):
            assert entry["rank"] == i + 1

    def test_user_moves_up_leaderboard(self, authenticated_client, db_session, multiple_users):
        """Test that user's position improves after achieving high score."""
        client, token, test_user = authenticated_client
        
        # Get initial leaderboard position
        response1 = client.get("/api/leaderboard?limit=100")
        entries1 = response1.json()["entries"]
        
        initial_rank = None
        for entry in entries1:
            if entry["id"] == test_user["id"]:
                initial_rank = entry["rank"]
                break
        
        # Submit extremely high score
        client.post("/api/leaderboard", json={
            "score": 99999,
            "chops": 1000
        })
        
        # Get updated leaderboard
        response2 = client.get("/api/leaderboard?limit=100")
        entries2 = response2.json()["entries"]
        
        new_rank = None
        for entry in entries2:
            if entry["id"] == test_user["id"]:
                new_rank = entry["rank"]
                break
        
        # User should have moved up (lower rank number)
        if initial_rank:
            assert new_rank < initial_rank or new_rank == 1


class TestLeaderboardWithGameSession:
    """Tests for leaderboard integration with game sessions."""

    def test_game_session_affects_leaderboard(self, authenticated_client, db_session):
        """Test that ending a game session updates leaderboard."""
        client, token, test_user = authenticated_client
        
        # Create and end game session
        create_resp = client.post("/api/game/session")
        session_id = create_resp.json()["session"]["id"]
        
        high_score = 15000
        client.post(f"/api/game/session/{session_id}/end", json={
            "score": high_score,
            "chops": 750,
            "duration": 300.0
        })
        
        # Check leaderboard
        leaderboard_resp = client.get("/api/leaderboard")
        entries = leaderboard_resp.json()["entries"]
        
        # Find user in leaderboard
        user_entry = None
        for entry in entries:
            if entry["id"] == test_user["id"]:
                user_entry = entry
                break
        
        assert user_entry is not None
        assert user_entry["score"] == high_score

    def test_multiple_games_update_leaderboard_correctly(self, authenticated_client, db_session):
        """Test that playing multiple games keeps highest score on leaderboard."""
        client, token, test_user = authenticated_client
        
        scores = [5000, 3000, 8000, 6000]  # 8000 should be the high score
        
        for score in scores:
            create_resp = client.post("/api/game/session")
            session_id = create_resp.json()["session"]["id"]
            
            client.post(f"/api/game/session/{session_id}/end", json={
                "score": score,
                "chops": 100,
                "duration": 120.0
            })
        
        # Check leaderboard shows highest score
        leaderboard_resp = client.get("/api/leaderboard")
        entries = leaderboard_resp.json()["entries"]
        
        user_entry = next((e for e in entries if e["id"] == test_user["id"]), None)
        assert user_entry is not None
        assert user_entry["score"] == 8000  # Highest score
