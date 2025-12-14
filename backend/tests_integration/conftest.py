"""Configuration for integration tests using SQLite database."""
import pytest # type: ignore
from fastapi.testclient import TestClient # type: ignore
from sqlalchemy import create_engine # type: ignore
from sqlalchemy.orm import sessionmaker # type: ignore
from sqlalchemy.pool import StaticPool # type: ignore
from app.main import app
from app.database import Base, get_db
from app import db_models
from app.auth_utils import hash_password
from datetime import datetime, timezone


# Create test database engine (file-based SQLite for integration tests)
TEST_DATABASE_URL = "sqlite:///./test_integration.db"
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# Override the dependency globally for all tests
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """Create tables once for the entire test session"""
    Base.metadata.create_all(bind=engine)
    yield
    # Cleanup after all tests
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function", autouse=True)
def reset_db():
    """Reset database before each test"""
    db = TestingSessionLocal()
    try:
        # Clear all data
        db.query(db_models.GameSession).delete()
        db.query(db_models.User).delete()
        db.commit()
    finally:
        db.close()


@pytest.fixture
def client():
    """Fixture providing TestClient with test database"""
    return TestClient(app)


@pytest.fixture
def db_session():
    """Provide a database session for direct database manipulation"""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def test_user(db_session):
    """Create a test user in the database"""
    user = db_models.User(
        id="test-user-123",
        username="testuser",
        email="test@example.com",
        password=hash_password("testpassword"),
        created_at=datetime.now(timezone.utc),
        high_score=100,
        total_chops=500,
        games_played=5
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user.to_dict()


@pytest.fixture
def multiple_users(db_session):
    """Create multiple users for leaderboard testing"""
    users = [
        db_models.User(
            id=f"user-{i}",
            username=f"player{i}",
            email=f"player{i}@example.com",
            password=hash_password("password"),
            created_at=datetime.now(timezone.utc),
            high_score=1000 * (10 - i),  # Descending scores
            total_chops=5000 * (10 - i),
            games_played=i * 10
        )
        for i in range(1, 11)
    ]
    for user in users:
        db_session.add(user)
    db_session.commit()
    return [user.to_dict() for user in users]


@pytest.fixture
def authenticated_client(client, test_user):
    """Provide a client with authentication token"""
    response = client.post("/api/auth/login", json={
        "email": test_user["email"],
        "password": "testpassword"
    })
    token = response.json()["token"]
    
    # Create a new client with auth header
    client.headers = {"Authorization": f"Bearer {token}"}
    return client, token, test_user
