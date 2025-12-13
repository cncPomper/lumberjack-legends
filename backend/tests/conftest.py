import pytest # type: ignore
from fastapi.testclient import TestClient # type: ignore
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.main import app
from app.database import Base, get_db
from app import db_models
from app.auth_utils import hash_password
from datetime import datetime, timezone

# Create test database engine (in-memory SQLite with special config for testing)
TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # Use static pool to keep same connection across threads
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables once at module level
Base.metadata.create_all(bind=engine)

def override_get_db():
    """Override database dependency for testing"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Override the dependency globally for all tests
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function", autouse=True)
def reset_db():
    """Reset database before each test"""
    # Clear all data
    db = TestingSessionLocal()
    try:
        db.query(db_models.GameSession).delete()
        db.query(db_models.User).delete()
        db.commit()
        
        # Seed test data
        seed_test_data(db)
    finally:
        db.close()

@pytest.fixture
def client():
    """Fixture providing TestClient with test database"""
    return TestClient(app)

def seed_test_data(db):
    """Seed database with test data"""
    hashed_pw = hash_password("password")  # Hash once for all test users
    test_users = [
        {"id": "1", "username": "ForestKing", "email": "king@forest.com", "password": hashed_pw, "created_at": datetime(2024, 1, 15, tzinfo=timezone.utc), "high_score": 2500, "total_chops": 15000, "games_played": 120},
        {"id": "2", "username": "AxeMaster", "email": "axe@master.com", "password": hashed_pw, "created_at": datetime(2024, 2, 20, tzinfo=timezone.utc), "high_score": 2200, "total_chops": 12000, "games_played": 95},
        {"id": "4", "username": "PaulBunyan", "email": "paul@legends.com", "password": hashed_pw, "created_at": datetime(2024, 1, 1, tzinfo=timezone.utc), "high_score": 5000, "total_chops": 50000, "games_played": 500},
        {"id": "24", "username": "RedwoodRookie", "email": "redwood@rookie.com", "password": hashed_pw, "created_at": datetime(2024, 8, 10, tzinfo=timezone.utc), "high_score": 50, "total_chops": 10, "games_played": 1},
    ]
    
    for user_data in test_users:
        user = db_models.User(**user_data)
        db.add(user)
    
    test_sessions = [
        {"id": "session-1", "user_id": "4", "score": 5000, "chops": 250, "duration": 180.5, "started_at": datetime(2024, 8, 1, 10, 0, tzinfo=timezone.utc), "ended_at": datetime(2024, 8, 1, 10, 3, tzinfo=timezone.utc)},
        {"id": "session-2", "user_id": "1", "score": 2500, "chops": 150, "duration": 120.0, "started_at": datetime(2024, 8, 2, 14, 0, tzinfo=timezone.utc), "ended_at": datetime(2024, 8, 2, 14, 2, tzinfo=timezone.utc)},
    ]
    
    for session_data in test_sessions:
        session = db_models.GameSession(**session_data)
        db.add(session)
    
    db.commit()

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
