"""Database configuration and session management."""
import os
from sqlalchemy import create_engine # type: ignore
from sqlalchemy.ext.declarative import declarative_base # type: ignore
from sqlalchemy.orm import sessionmaker # type: ignore

# Get database URL from environment variable or default to PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://lumberjack:lumberjack_password@localhost:5432/lumberjack_legends")

# Create engine
# PostgreSQL doesn't need special connect_args like SQLite
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Enable connection health checks
    echo=False  # Set to True for SQL query logging
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()

def get_db():
    """Dependency for getting database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database tables."""
    from app.db_models import User, GameSession
    Base.metadata.create_all(bind=engine)
