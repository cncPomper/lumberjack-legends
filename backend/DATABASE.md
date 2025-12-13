# Database Configuration

This backend supports both PostgreSQL and SQLite databases via SQLAlchemy.

## Environment Variables

### `DATABASE_URL`
Specifies the database connection string.

**Default:** `sqlite:///./lumberjack.db` (SQLite database in the backend directory)

**Examples:**

```bash
# SQLite (default)
DATABASE_URL=sqlite:///./lumberjack.db

# PostgreSQL
DATABASE_URL=postgresql://username:password@localhost:5432/lumberjack_legends

# PostgreSQL with psycopg2
DATABASE_URL=postgresql+psycopg2://username:password@localhost:5432/lumberjack_legends
```

## Setup Instructions

### Using SQLite (Default)

No additional setup required. The database file will be created automatically when you first run the application.

```bash
# Sync dependencies
uv sync

# Seed the database with initial data
uv run python -m app.seed

# Run the server
uv run uvicorn app.main:app --reload
```

### Using PostgreSQL

1. **Install PostgreSQL** (if not already installed)

2. **Create a database:**
   ```bash
   psql -U postgres
   CREATE DATABASE lumberjack_legends;
   \q
   ```

3. **Set the DATABASE_URL environment variable:**
   ```bash
   export DATABASE_URL=postgresql://username:password@localhost:5432/lumberjack_legends
   ```

4. **Sync dependencies and run:**
   ```bash
   # Sync dependencies
   uv sync

   # Seed the database with initial data
   uv run python -m app.seed

   # Run the server
   uv run uvicorn app.main:app --reload
   ```

## Database Commands

### Seed Database
```bash
uv run python -m app.seed
```

### Reset Database
To reset the database, simply delete the database file (for SQLite) or drop and recreate the database (for PostgreSQL), then run the seed command again.

**SQLite:**
```bash
rm lumberjack.db
uv run python -m app.seed
```

**PostgreSQL:**
```bash
psql -U postgres
DROP DATABASE lumberjack_legends;
CREATE DATABASE lumberjack_legends;
\q
uv run python -m app.seed
```

## Database Schema

### Users Table
- `id` (String, Primary Key)
- `username` (String, Unique)
- `email` (String, Unique)
- `password` (String)
- `created_at` (DateTime)
- `high_score` (Integer)
- `total_chops` (Integer)
- `games_played` (Integer)

### Game Sessions Table
- `id` (String, Primary Key)
- `user_id` (String, Foreign Key to Users)
- `score` (Integer)
- `chops` (Integer)
- `duration` (Float)
- `started_at` (DateTime)
- `ended_at` (DateTime, Nullable)

## Development Tips

- The database schema is automatically created on application startup
- Use the seed script to populate with test data
- For production, consider using migrations with Alembic
- Password storage is currently plain text - implement hashing for production use

## Production Considerations

For production deployments:

1. **Use PostgreSQL** for better performance and scalability
2. **Enable SSL** in the DATABASE_URL if required
3. **Implement password hashing** (e.g., using bcrypt or passlib)
4. **Set up database migrations** using Alembic
5. **Configure connection pooling** appropriately
6. **Use environment-specific configuration**
