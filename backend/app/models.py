from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field # type: ignore

class User(BaseModel):
    id: str
    username: str
    email: EmailStr
    createdAt: datetime
    highScore: int
    totalChops: int
    gamesPlayed: int

class AuthResponse(BaseModel):
    success: bool
    user: Optional[User] = None
    token: Optional[str] = None
    error: Optional[str] = None

class LeaderboardEntry(BaseModel):
    id: str
    username: str
    score: int
    chops: int
    rank: int
    timestamp: datetime

class LeaderboardResponse(BaseModel):
    success: bool
    entries: List[LeaderboardEntry]
    userRank: Optional[int] = None
    error: Optional[str] = None

class GameSession(BaseModel):
    id: str
    userId: str
    score: int
    chops: int
    duration: float
    startedAt: datetime
    endedAt: Optional[datetime] = None

class GameSessionResponse(BaseModel):
    success: bool
    session: Optional[GameSession] = None
    error: Optional[str] = None

# Request Models
class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=4)

class SignupRequest(BaseModel):
    username: str = Field(..., min_length=3)
    email: EmailStr
    password: str = Field(..., min_length=6)

class ProfileUpdateRequest(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    highScore: Optional[int] = None
    totalChops: Optional[int] = None
    gamesPlayed: Optional[int] = None

class ScoreSubmitRequest(BaseModel):
    score: int
    chops: int

class SessionEndRequest(BaseModel):
    score: int
    chops: int
    duration: float
