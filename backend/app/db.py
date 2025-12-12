from datetime import datetime
from typing import List, Optional
from .models import User, GameSession

# Mock Data
_initial_users = [
    {"id": "1", "username": "ForestKing", "email": "king@forest.com", "password": "password", "createdAt": datetime(2024, 1, 15), "highScore": 2500, "totalChops": 15000, "gamesPlayed": 120},
    {"id": "2", "username": "AxeMaster", "email": "axe@master.com", "password": "password", "createdAt": datetime(2024, 2, 20), "highScore": 2200, "totalChops": 12000, "gamesPlayed": 95},
    {"id": "3", "username": "TimberWolf", "email": "timber@wolf.com", "password": "password", "createdAt": datetime(2024, 3, 10), "highScore": 1950, "totalChops": 9500, "gamesPlayed": 78},
]

class MockDB:
    def __init__(self):
        self.users = [u.copy() for u in _initial_users]
        self.sessions = []

    def get_user_by_email(self, email: str) -> Optional[dict]:
        for user in self.users:
            if user["email"].lower() == email.lower():
                return user
        return None

    def get_user_by_id(self, user_id: str) -> Optional[dict]:
        for user in self.users:
            if user["id"] == user_id:
                return user
        return None

    def create_user(self, user_data: dict) -> dict:
        new_user = user_data.copy()
        new_user["id"] = str(len(self.users) + 1)
        new_user["createdAt"] = datetime.now()
        new_user["highScore"] = 0
        new_user["totalChops"] = 0
        new_user["gamesPlayed"] = 0
        self.users.append(new_user)
        return new_user

    def update_user(self, user_id: str, updates: dict) -> Optional[dict]:
        user = self.get_user_by_id(user_id)
        if user:
            user.update(updates)
            return user
        return None

    def create_session(self, user_id: str) -> dict:
        import uuid
        session = {
            "id": str(uuid.uuid4()),
            "userId": user_id,
            "score": 0,
            "chops": 0,
            "duration": 0,
            "startedAt": datetime.now(),
            "endedAt": None
        }
        self.sessions.append(session)
        return session

    def end_session(self, session_id: str, score: int, chops: int, duration: float) -> Optional[dict]:
        for session in self.sessions:
            if session["id"] == session_id:
                session["score"] = score
                session["chops"] = chops
                session["duration"] = duration
                session["endedAt"] = datetime.now()
                return session
        return None

    def get_leaderboard(self, limit: int = 10) -> List[dict]:
        sorted_users = sorted(self.users, key=lambda u: u["highScore"], reverse=True)
        return sorted_users[:limit]

    def get_user_rank(self, user_id: str) -> int:
        sorted_users = sorted(self.users, key=lambda u: u["highScore"], reverse=True)
        for i, user in enumerate(sorted_users):
            if user["id"] == user_id:
                return i + 1
        return 0

db = MockDB()
