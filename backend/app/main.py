from fastapi import FastAPI, Depends, HTTPException, status, Query, APIRouter # type: ignore
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
import jwt # type: ignore
import os
from datetime import datetime, timedelta, timezone
from typing import Optional
from sqlalchemy.orm import Session # type: ignore
from .models import (
    User, AuthResponse, LoginRequest, SignupRequest, ProfileUpdateRequest,
    LeaderboardResponse, LeaderboardEntry, ScoreSubmitRequest,
    GameSessionResponse, SessionEndRequest
)
from .db import database
from .database import get_db, init_db
from .auth_utils import hash_password, verify_password

app = FastAPI(
    title="Lumberjack Legends API",
    version="0.1.0",
    description="Backend for Lumberjack Legends",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
def startup_event():
    init_db()

# Security
security = HTTPBearer()
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    user = database.get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user

# API Router
router = APIRouter(prefix="/api")

# Health check endpoint (for Render and other monitoring)
@router.get("/health")
def health_check():
    return {"status": "ok", "service": "lumberjack-legends"}

# Auth Routes
@router.post("/auth/login", response_model=AuthResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = database.get_user_by_email(db, request.email)
    if not user or not verify_password(request.password, user["password"]):
        return AuthResponse(success=False, error="Invalid email or password")
    
    token = create_access_token(data={"sub": user["id"]})
    return AuthResponse(success=True, user=User(**user), token=token)

@router.post("/auth/signup", response_model=AuthResponse, status_code=201)
def signup(request: SignupRequest, db: Session = Depends(get_db)):
    if database.get_user_by_email(db, request.email):
        return AuthResponse(success=False, error="Email already registered")
    
    # Check username uniqueness
    if database.get_user_by_username(db, request.username):
        return AuthResponse(success=False, error="Username already taken")

    # Hash the password before storing
    user_data = request.model_dump()
    user_data["password"] = hash_password(user_data["password"])
    
    new_user = database.create_user(db, user_data)
    token = create_access_token(data={"sub": new_user["id"]})
    return AuthResponse(success=True, user=User(**new_user), token=token)

@router.post("/auth/logout")
def logout(current_user: dict = Depends(get_current_user)):
    return {"success": True}

@router.get("/auth/me", response_model=AuthResponse)
def get_me(current_user: dict = Depends(get_current_user)):
    return AuthResponse(success=True, user=User(**current_user))

@router.patch("/auth/profile", response_model=AuthResponse)
def update_profile(
    request: ProfileUpdateRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    updates = request.model_dump(exclude_unset=True)
    updated_user = database.update_user(db, current_user["id"], updates)
    return AuthResponse(success=True, user=User(**updated_user)) # type: ignore

# Leaderboard Routes
@router.get("/leaderboard", response_model=LeaderboardResponse)
def get_leaderboard(limit: int = Query(10, ge=1, le=100), db: Session = Depends(get_db)):
    entries_data = database.get_leaderboard(db, limit)
    entries = []
    for i, entry in enumerate(entries_data):
        entries.append(LeaderboardEntry(
            id=entry["id"],
            username=entry["username"],
            score=entry["highScore"],
            chops=entry["totalChops"],
            rank=i + 1,
            timestamp=datetime.now() # Mock timestamp
        ))
    
    # User rank (if we could get current user optionally, but here we don't have it easily without auth)
    # The spec says userRank is optional.
    return LeaderboardResponse(success=True, entries=entries)

@router.post("/leaderboard", response_model=LeaderboardResponse)
def submit_score(
    request: ScoreSubmitRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Update user stats
    updates = {
        "totalChops": current_user["totalChops"] + request.chops,
        "gamesPlayed": current_user["gamesPlayed"] + 1
    }
    if request.score > current_user["highScore"]:
        updates["highScore"] = request.score
    
    database.update_user(db, current_user["id"], updates)
    
    # Return updated leaderboard
    return get_leaderboard(limit=10, db=db)

# Game Routes
@router.post("/game/session", response_model=GameSessionResponse, status_code=201)
def start_session(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    session = database.create_session(db, current_user["id"])
    return GameSessionResponse(success=True, session=session)

@router.post("/game/session/{session_id}/end", response_model=GameSessionResponse)
def end_session(
    session_id: str,
    request: SessionEndRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    session = database.end_session(db, session_id, request.score, request.chops, request.duration)
    if not session:
        return GameSessionResponse(success=False, error="Session not found")

    return GameSessionResponse(success=True, session=session)

@router.get("/game/stats")
def get_stats(current_user: dict = Depends(get_current_user)):
    return {
        "success": True,
        "stats": {
            "totalGames": current_user["gamesPlayed"],
            "avgScore": round(current_user["totalChops"] / current_user["gamesPlayed"]) if current_user["gamesPlayed"] > 0 else 0,
            "topScore": current_user["highScore"]
        }
    }

app.include_router(router)
