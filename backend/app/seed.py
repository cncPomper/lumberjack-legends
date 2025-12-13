"""Seed database with initial data."""
from datetime import datetime, timezone, timedelta
from .database import SessionLocal, init_db
from .db_models import User, GameSession
from .auth_utils import hash_password


def seed_database():
    """Populate database with initial seed data."""
    print("Initializing database schema...")
    init_db()
    
    db = SessionLocal()
    
    try:
        # Check if data already exists
        existing_users = db.query(User).count()
        if existing_users > 0:
            print(f"Database already has {existing_users} users. Skipping seed.")
            return
        
        print("Seeding database with initial data...")
        
        # Create initial users with hashed passwords
        hashed_pw = hash_password("password")  # Pre-hash once for all users
        users_data = [
            {"id": "1", "username": "ForestKing", "email": "king@forest.com", "password": hashed_pw, "created_at": datetime(2024, 1, 15, tzinfo=timezone.utc), "high_score": 2500, "total_chops": 15000, "games_played": 120},
            {"id": "2", "username": "AxeMaster", "email": "axe@master.com", "password": hashed_pw, "created_at": datetime(2024, 2, 20, tzinfo=timezone.utc), "high_score": 2200, "total_chops": 12000, "games_played": 95},
            {"id": "3", "username": "TimberWolf", "email": "timber@wolf.com", "password": hashed_pw, "created_at": datetime(2024, 3, 10, tzinfo=timezone.utc), "high_score": 1950, "total_chops": 9500, "games_played": 78},
            {"id": "4", "username": "PaulBunyan", "email": "paul@legends.com", "password": hashed_pw, "created_at": datetime(2024, 1, 1, tzinfo=timezone.utc), "high_score": 5000, "total_chops": 50000, "games_played": 500},
            {"id": "5", "username": "LumberJill", "email": "jill@forest.com", "password": hashed_pw, "created_at": datetime(2024, 2, 1, tzinfo=timezone.utc), "high_score": 2400, "total_chops": 14000, "games_played": 110},
            {"id": "6", "username": "ChopSuey", "email": "chop@suey.com", "password": hashed_pw, "created_at": datetime(2024, 3, 15, tzinfo=timezone.utc), "high_score": 1800, "total_chops": 8000, "games_played": 60},
            {"id": "7", "username": "SawDust", "email": "saw@dust.com", "password": hashed_pw, "created_at": datetime(2024, 4, 1, tzinfo=timezone.utc), "high_score": 1500, "total_chops": 5000, "games_played": 40},
            {"id": "8", "username": "Woody", "email": "woody@toy.com", "password": hashed_pw, "created_at": datetime(2024, 4, 10, tzinfo=timezone.utc), "high_score": 1200, "total_chops": 3000, "games_played": 25},
            {"id": "9", "username": "LeafErikson", "email": "leaf@viking.com", "password": hashed_pw, "created_at": datetime(2024, 4, 20, tzinfo=timezone.utc), "high_score": 800, "total_chops": 1000, "games_played": 10},
            {"id": "10", "username": "TreeHugger", "email": "peace@love.com", "password": hashed_pw, "created_at": datetime(2024, 5, 1, tzinfo=timezone.utc), "high_score": 100, "total_chops": 0, "games_played": 1},
            {"id": "11", "username": "ChopChampion", "email": "chop@champ.com", "password": hashed_pw, "created_at": datetime(2024, 5, 5, tzinfo=timezone.utc), "high_score": 4500, "total_chops": 45000, "games_played": 400},
            {"id": "12", "username": "BarkBuster", "email": "bark@buster.com", "password": hashed_pw, "created_at": datetime(2024, 5, 10, tzinfo=timezone.utc), "high_score": 3800, "total_chops": 35000, "games_played": 350},
            {"id": "13", "username": "LogLegend", "email": "log@legend.com", "password": hashed_pw, "created_at": datetime(2024, 5, 15, tzinfo=timezone.utc), "high_score": 3200, "total_chops": 28000, "games_played": 280},
            {"id": "14", "username": "WoodWarrior", "email": "wood@warrior.com", "password": hashed_pw, "created_at": datetime(2024, 6, 1, tzinfo=timezone.utc), "high_score": 2900, "total_chops": 22000, "games_played": 200},
            {"id": "15", "username": "TreeSlayer", "email": "tree@slayer.com", "password": hashed_pw, "created_at": datetime(2024, 6, 5, tzinfo=timezone.utc), "high_score": 2700, "total_chops": 20000, "games_played": 180},
            {"id": "16", "username": "ChipMonk", "email": "chip@monk.com", "password": hashed_pw, "created_at": datetime(2024, 6, 10, tzinfo=timezone.utc), "high_score": 2100, "total_chops": 11000, "games_played": 90},
            {"id": "17", "username": "SpruceBruce", "email": "spruce@bruce.com", "password": hashed_pw, "created_at": datetime(2024, 6, 15, tzinfo=timezone.utc), "high_score": 1700, "total_chops": 7500, "games_played": 55},
            {"id": "18", "username": "PineSlasher", "email": "pine@slasher.com", "password": hashed_pw, "created_at": datetime(2024, 7, 1, tzinfo=timezone.utc), "high_score": 1400, "total_chops": 4500, "games_played": 35},
            {"id": "19", "username": "MapleManiac", "email": "maple@maniac.com", "password": hashed_pw, "created_at": datetime(2024, 7, 5, tzinfo=timezone.utc), "high_score": 1100, "total_chops": 2800, "games_played": 22},
            {"id": "20", "username": "OakOracle", "email": "oak@oracle.com", "password": hashed_pw, "created_at": datetime(2024, 7, 10, tzinfo=timezone.utc), "high_score": 900, "total_chops": 1500, "games_played": 12},
            {"id": "21", "username": "BirchBrawler", "email": "birch@brawler.com", "password": hashed_pw, "created_at": datetime(2024, 7, 15, tzinfo=timezone.utc), "high_score": 600, "total_chops": 800, "games_played": 8},
            {"id": "22", "username": "WillowWhacker", "email": "willow@whacker.com", "password": hashed_pw, "created_at": datetime(2024, 8, 1, tzinfo=timezone.utc), "high_score": 400, "total_chops": 400, "games_played": 4},
            {"id": "23", "username": "CedarSeeker", "email": "cedar@seeker.com", "password": hashed_pw, "created_at": datetime(2024, 8, 5, tzinfo=timezone.utc), "high_score": 250, "total_chops": 150, "games_played": 2},
            {"id": "24", "username": "RedwoodRookie", "email": "redwood@rookie.com", "password": hashed_pw, "created_at": datetime(2024, 8, 10, tzinfo=timezone.utc), "high_score": 50, "total_chops": 10, "games_played": 1},
            {"id": "25", "username": "AspenApprentice", "email": "aspen@apprentice.com", "password": hashed_pw, "created_at": datetime(2024, 8, 15, tzinfo=timezone.utc), "high_score": 25, "total_chops": 5, "games_played": 1},
        ]
        
        for user_data in users_data:
            user = User(**user_data)
            db.add(user)
        
        # Create initial game sessions
        sessions_data = [
            {"id": "session-1", "user_id": "4", "score": 5000, "chops": 250, "duration": 180.5, "started_at": datetime(2024, 8, 1, 10, 0, tzinfo=timezone.utc), "ended_at": datetime(2024, 8, 1, 10, 3, tzinfo=timezone.utc)},
            {"id": "session-2", "user_id": "1", "score": 2500, "chops": 150, "duration": 120.0, "started_at": datetime(2024, 8, 2, 14, 0, tzinfo=timezone.utc), "ended_at": datetime(2024, 8, 2, 14, 2, tzinfo=timezone.utc)},
            {"id": "session-3", "user_id": "5", "score": 2400, "chops": 145, "duration": 115.3, "started_at": datetime(2024, 8, 3, 9, 0, tzinfo=timezone.utc), "ended_at": datetime(2024, 8, 3, 9, 2, tzinfo=timezone.utc)},
            {"id": "session-4", "user_id": "2", "score": 2200, "chops": 130, "duration": 110.8, "started_at": datetime(2024, 8, 4, 16, 0, tzinfo=timezone.utc), "ended_at": datetime(2024, 8, 4, 16, 2, tzinfo=timezone.utc)},
            {"id": "session-5", "user_id": "11", "score": 4500, "chops": 220, "duration": 175.2, "started_at": datetime(2024, 8, 5, 11, 0, tzinfo=timezone.utc), "ended_at": datetime(2024, 8, 5, 11, 3, tzinfo=timezone.utc)},
        ]
        
        for session_data in sessions_data:
            session = GameSession(**session_data)
            db.add(session)
        
        db.commit()
        print(f"Successfully seeded database with {len(users_data)} users and {len(sessions_data)} sessions!")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
