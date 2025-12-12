from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
import jwt
from datetime import datetime, timedelta, timezone
from typing import Optional
from .models import (
    User, AuthResponse, LoginRequest, SignupRequest, ProfileUpdateRequest,
    LeaderboardResponse, LeaderboardEntry, ScoreSubmitRequest,
    GameSessionResponse, SessionEndRequest
)
from .db import db

app = FastAPI(
    title="Lumberjack Legends API",
    version="0.1.0",
    description="Backend for Lumberjack Legends"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()
SECRET_KEY = "supersecretkey"
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

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    user = db.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user

# Auth Routes
@app.post("/auth/login", response_model=AuthResponse)
def login(request: LoginRequest):
    user = db.get_user_by_email(request.email)
    if not user or user["password"] != request.password:
        return AuthResponse(success=False, error="Invalid email or password")
    
    token = create_access_token(data={"sub": user["id"]})
    return AuthResponse(success=True, user=User(**user), token=token)

@app.post("/auth/signup", response_model=AuthResponse, status_code=201)
def signup(request: SignupRequest):
    if db.get_user_by_email(request.email):
        return AuthResponse(success=False, error="Email already registered")
    
    # Check username uniqueness (simple check)
    for u in db.users:
        if u["username"].lower() == request.username.lower():
             return AuthResponse(success=False, error="Username already taken")

    new_user = db.create_user(request.model_dump())
    token = create_access_token(data={"sub": new_user["id"]})
    return AuthResponse(success=True, user=User(**new_user), token=token)

@app.post("/auth/logout")
def logout(current_user: dict = Depends(get_current_user)):
    return {"success": True}

@app.get("/auth/me", response_model=AuthResponse)
def get_me(current_user: dict = Depends(get_current_user)):
    return AuthResponse(success=True, user=User(**current_user))

@app.patch("/auth/profile", response_model=AuthResponse)
def update_profile(request: ProfileUpdateRequest, current_user: dict = Depends(get_current_user)):
    updates = request.model_dump(exclude_unset=True)
    updated_user = db.update_user(current_user["id"], updates)
    return AuthResponse(success=True, user=User(**updated_user))

# Leaderboard Routes
@app.get("/leaderboard", response_model=LeaderboardResponse)
def get_leaderboard(limit: int = Query(10, ge=1, le=100)):
    entries_data = db.get_leaderboard(limit)
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

@app.post("/leaderboard", response_model=LeaderboardResponse)
def submit_score(request: ScoreSubmitRequest, current_user: dict = Depends(get_current_user)):
    # Update user stats
    updates = {
        "totalChops": current_user["totalChops"] + request.chops,
        "gamesPlayed": current_user["gamesPlayed"] + 1
    }
    if request.score > current_user["highScore"]:
        updates["highScore"] = request.score
    
    db.update_user(current_user["id"], updates)
    
    # Return updated leaderboard
    return get_leaderboard(limit=10)

# Game Routes
@app.post("/game/session", response_model=GameSessionResponse, status_code=201)
def start_session(current_user: dict = Depends(get_current_user)):
    session = db.create_session(current_user["id"])
    return GameSessionResponse(success=True, session=session)

@app.post("/game/session/{session_id}/end", response_model=GameSessionResponse)
def end_session(session_id: str, request: SessionEndRequest, current_user: dict = Depends(get_current_user)):
    session = db.end_session(session_id, request.score, request.chops, request.duration)
    if not session:
        return GameSessionResponse(success=False, error="Session not found")
    
    # Also update leaderboard/stats
    # Re-using logic from submit_score or calling it?
    # The spec says "End a game session and optionally update leaderboard"
    # Let's update it here too.
    updates = {
        "totalChops": current_user["totalChops"] + request.chops,
        "gamesPlayed": current_user["gamesPlayed"] + 1
    }
    if request.score > current_user["highScore"]:
        updates["highScore"] = request.score
    db.update_user(current_user["id"], updates)

    return GameSessionResponse(success=True, session=session)

@app.get("/game/stats")
def get_stats(current_user: dict = Depends(get_current_user)):
    return {
        "success": True,
        "stats": {
            "totalGames": current_user["gamesPlayed"],
            "avgScore": round(current_user["totalChops"] / current_user["gamesPlayed"]) if current_user["gamesPlayed"] > 0 else 0,
            "topScore": current_user["highScore"]
        }
    }
