"""Database operations using SQLAlchemy."""
from datetime import datetime, timezone
from typing import List, Optional
import uuid
from sqlalchemy.orm import Session
from . import db_models


class Database:
    """Database operations wrapper for SQLAlchemy."""

    def get_user_by_email(self, db: Session, email: str) -> Optional[dict]:
        """Get user by email address."""
        user = db.query(db_models.User).filter(
            db_models.User.email == email.lower()
        ).first()
        return user.to_dict() if user else None

    def get_user_by_id(self, db: Session, user_id: str) -> Optional[dict]:
        """Get user by ID."""
        user = db.query(db_models.User).filter(
            db_models.User.id == user_id
        ).first()
        return user.to_dict() if user else None

    def get_user_by_username(self, db: Session, username: str) -> Optional[dict]:
        """Get user by username."""
        user = db.query(db_models.User).filter(
            db_models.User.username == username
        ).first()
        return user.to_dict() if user else None

    def create_user(self, db: Session, user_data: dict) -> dict:
        """Create a new user."""
        new_user = db_models.User(
            id=str(uuid.uuid4()),
            username=user_data["username"],
            email=user_data["email"].lower(),
            password=user_data["password"],
            created_at=datetime.now(timezone.utc),
            high_score=0,
            total_chops=0,
            games_played=0
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user.to_dict()

    def update_user(self, db: Session, user_id: str, updates: dict) -> Optional[dict]:
        """Update user information."""
        user = db.query(db_models.User).filter(
            db_models.User.id == user_id
        ).first()
        
        if not user:
            return None
        
        # Map camelCase to snake_case for database fields
        field_mapping = {
            "username": "username",
            "email": "email",
            "highScore": "high_score",
            "totalChops": "total_chops",
            "gamesPlayed": "games_played",
        }
        
        for key, value in updates.items():
            db_field = field_mapping.get(key)
            if db_field and hasattr(user, db_field):
                setattr(user, db_field, value)
        
        db.commit()
        db.refresh(user)
        return user.to_dict()

    def create_session(self, db: Session, user_id: str) -> dict:
        """Create a new game session."""
        session = db_models.GameSession(
            id=str(uuid.uuid4()),
            user_id=user_id,
            score=0,
            chops=0,
            duration=0.0,
            started_at=datetime.now(timezone.utc),
            ended_at=None
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        return session.to_dict()

    def end_session(
        self, db: Session, session_id: str, score: int, chops: int, duration: float
    ) -> Optional[dict]:
        """End a game session and update user statistics."""
        session = db.query(db_models.GameSession).filter(
            db_models.GameSession.id == session_id
        ).first()
        
        if not session:
            return None
        
        session.score = score
        session.chops = chops
        session.duration = duration
        session.ended_at = datetime.now(timezone.utc)
        
        # Update user statistics
        user = db.query(db_models.User).filter(
            db_models.User.id == session.user_id
        ).first()
        
        if user:
            user.games_played += 1
            user.total_chops += chops
            if score > user.high_score:
                user.high_score = score
        
        db.commit()
        db.refresh(session)
        return session.to_dict()

    def get_leaderboard(self, db: Session, limit: int = 10) -> List[dict]:
        """Get top users by high score."""
        users = db.query(db_models.User).order_by(
            db_models.User.high_score.desc()
        ).limit(limit).all()
        
        return [user.to_dict() for user in users]

    def get_user_rank(self, db: Session, user_id: str) -> int:
        """Get user's rank based on high score."""
        users = db.query(db_models.User).order_by(
            db_models.User.high_score.desc()
        ).all()
        
        for i, user in enumerate(users):
            if user.id == user_id:
                return i + 1
        return 0


# Create database instance
database = Database()
