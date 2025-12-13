from datetime import datetime
from typing import List, Optional
from .models import User, GameSession

# Mock Data
_initial_users = [
    {"id": "1", "username": "ForestKing", "email": "king@forest.com", "password": "password", "createdAt": datetime(2024, 1, 15), "highScore": 2500, "totalChops": 15000, "gamesPlayed": 120},
    {"id": "2", "username": "AxeMaster", "email": "axe@master.com", "password": "password", "createdAt": datetime(2024, 2, 20), "highScore": 2200, "totalChops": 12000, "gamesPlayed": 95},
    {"id": "3", "username": "TimberWolf", "email": "timber@wolf.com", "password": "password", "createdAt": datetime(2024, 3, 10), "highScore": 1950, "totalChops": 9500, "gamesPlayed": 78},
    {"id": "4", "username": "PaulBunyan", "email": "paul@legends.com", "password": "password", "createdAt": datetime(2024, 1, 1), "highScore": 5000, "totalChops": 50000, "gamesPlayed": 500},
    {"id": "5", "username": "LumberJill", "email": "jill@forest.com", "password": "password", "createdAt": datetime(2024, 2, 1), "highScore": 2400, "totalChops": 14000, "gamesPlayed": 110},
    {"id": "6", "username": "ChopSuey", "email": "chop@suey.com", "password": "password", "createdAt": datetime(2024, 3, 15), "highScore": 1800, "totalChops": 8000, "gamesPlayed": 60},
    {"id": "7", "username": "SawDust", "email": "saw@dust.com", "password": "password", "createdAt": datetime(2024, 4, 1), "highScore": 1500, "totalChops": 5000, "gamesPlayed": 40},
    {"id": "8", "username": "Woody", "email": "woody@toy.com", "password": "password", "createdAt": datetime(2024, 4, 10), "highScore": 1200, "totalChops": 3000, "gamesPlayed": 25},
    {"id": "9", "username": "LeafErikson", "email": "leaf@viking.com", "password": "password", "createdAt": datetime(2024, 4, 20), "highScore": 800, "totalChops": 1000, "gamesPlayed": 10},
    {"id": "10", "username": "TreeHugger", "email": "peace@love.com", "password": "password", "createdAt": datetime(2024, 5, 1), "highScore": 100, "totalChops": 0, "gamesPlayed": 1},
    {"id": "11", "username": "ChopChampion", "email": "chop@champ.com", "password": "password", "createdAt": datetime(2024, 5, 5), "highScore": 4500, "totalChops": 45000, "gamesPlayed": 400},
    {"id": "12", "username": "BarkBuster", "email": "bark@buster.com", "password": "password", "createdAt": datetime(2024, 5, 10), "highScore": 3800, "totalChops": 35000, "gamesPlayed": 350},
    {"id": "13", "username": "LogLegend", "email": "log@legend.com", "password": "password", "createdAt": datetime(2024, 5, 15), "highScore": 3200, "totalChops": 28000, "gamesPlayed": 280},
    {"id": "14", "username": "WoodWarrior", "email": "wood@warrior.com", "password": "password", "createdAt": datetime(2024, 6, 1), "highScore": 2900, "totalChops": 22000, "gamesPlayed": 200},
    {"id": "15", "username": "TreeSlayer", "email": "tree@slayer.com", "password": "password", "createdAt": datetime(2024, 6, 5), "highScore": 2700, "totalChops": 20000, "gamesPlayed": 180},
    {"id": "16", "username": "ChipMonk", "email": "chip@monk.com", "password": "password", "createdAt": datetime(2024, 6, 10), "highScore": 2100, "totalChops": 11000, "gamesPlayed": 90},
    {"id": "17", "username": "SpruceBruce", "email": "spruce@bruce.com", "password": "password", "createdAt": datetime(2024, 6, 15), "highScore": 1700, "totalChops": 7500, "gamesPlayed": 55},
    {"id": "18", "username": "PineSlasher", "email": "pine@slasher.com", "password": "password", "createdAt": datetime(2024, 7, 1), "highScore": 1400, "totalChops": 4500, "gamesPlayed": 35},
    {"id": "19", "username": "MapleManiac", "email": "maple@maniac.com", "password": "password", "createdAt": datetime(2024, 7, 5), "highScore": 1100, "totalChops": 2800, "gamesPlayed": 22},
    {"id": "20", "username": "OakOracle", "email": "oak@oracle.com", "password": "password", "createdAt": datetime(2024, 7, 10), "highScore": 900, "totalChops": 1500, "gamesPlayed": 12},
    {"id": "21", "username": "BirchBrawler", "email": "birch@brawler.com", "password": "password", "createdAt": datetime(2024, 7, 15), "highScore": 600, "totalChops": 800, "gamesPlayed": 8},
    {"id": "22", "username": "WillowWhacker", "email": "willow@whacker.com", "password": "password", "createdAt": datetime(2024, 8, 1), "highScore": 400, "totalChops": 400, "gamesPlayed": 4},
    {"id": "23", "username": "CedarSeeker", "email": "cedar@seeker.com", "password": "password", "createdAt": datetime(2024, 8, 5), "highScore": 250, "totalChops": 150, "gamesPlayed": 2},
    {"id": "24", "username": "RedwoodRookie", "email": "redwood@rookie.com", "password": "password", "createdAt": datetime(2024, 8, 10), "highScore": 50, "totalChops": 10, "gamesPlayed": 1},
    {"id": "25", "username": "AspenApprentice", "email": "aspen@apprentice.com", "password": "password", "createdAt": datetime(2024, 8, 15), "highScore": 25, "totalChops": 5, "gamesPlayed": 1},
]

_initial_sessions = [
    {"id": "session-1", "userId": "4", "score": 5000, "chops": 250, "duration": 180.5, "startedAt": datetime(2024, 8, 1, 10, 0), "endedAt": datetime(2024, 8, 1, 10, 3)},
    {"id": "session-2", "userId": "1", "score": 2500, "chops": 150, "duration": 120.0, "startedAt": datetime(2024, 8, 2, 14, 0), "endedAt": datetime(2024, 8, 2, 14, 2)},
    {"id": "session-3", "userId": "5", "score": 2400, "chops": 145, "duration": 115.3, "startedAt": datetime(2024, 8, 3, 9, 0), "endedAt": datetime(2024, 8, 3, 9, 2)},
    {"id": "session-4", "userId": "2", "score": 2200, "chops": 130, "duration": 110.8, "startedAt": datetime(2024, 8, 4, 16, 0), "endedAt": datetime(2024, 8, 4, 16, 2)},
    {"id": "session-5", "userId": "11", "score": 4500, "chops": 220, "duration": 175.2, "startedAt": datetime(2024, 8, 5, 11, 0), "endedAt": datetime(2024, 8, 5, 11, 3)},
]

class MockDB:
    def __init__(self):
        self.users = [u.copy() for u in _initial_users]
        self.sessions = [s.copy() for s in _initial_sessions]

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
