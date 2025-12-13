"""SQLAlchemy database models."""
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey # type: ignore
from sqlalchemy.orm import relationship # type: ignore
from .database import Base


class User(Base):
    """User model for storing user information."""
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)  # In production, this should be hashed
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    high_score = Column(Integer, default=0, nullable=False)
    total_chops = Column(Integer, default=0, nullable=False)
    games_played = Column(Integer, default=0, nullable=False)

    # Relationship to game sessions
    sessions = relationship("GameSession", back_populates="user", cascade="all, delete-orphan")

    def to_dict(self):
        """Convert model to dictionary for API responses."""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "createdAt": self.created_at,
            "highScore": self.high_score,
            "totalChops": self.total_chops,
            "gamesPlayed": self.games_played,
        }


class GameSession(Base):
    """GameSession model for storing game session information."""
    __tablename__ = "game_sessions"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    score = Column(Integer, default=0, nullable=False)
    chops = Column(Integer, default=0, nullable=False)
    duration = Column(Float, default=0.0, nullable=False)
    started_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    ended_at = Column(DateTime, nullable=True)

    # Relationship to user
    user = relationship("User", back_populates="sessions")

    def to_dict(self):
        """Convert model to dictionary for API responses."""
        return {
            "id": self.id,
            "userId": self.user_id,
            "score": self.score,
            "chops": self.chops,
            "duration": self.duration,
            "startedAt": self.started_at,
            "endedAt": self.ended_at,
        }
