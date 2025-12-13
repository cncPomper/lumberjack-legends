# Lumberjack Legends Backend

This is the backend API for the Lumberjack Legends game, built with FastAPI.

## Features

- **Authentication**: Signup, Login, Profile management (JWT-based).
- **Leaderboard**: Global leaderboard tracking high scores.
- **Game Session**: Secure game session management to prevent cheating.
- **Mock Database**: In-memory database for development and testing.

## Setup

This project uses `uv` for dependency management.

### Quick Start (using Makefile)

```bash
make install    # Install dependencies
make dev        # Run server with auto-reload
make test       # Run tests
```

### Manual Setup

1.  **Install dependencies**:
    ```bash
    uv sync
    ```

2.  **Run the server**:
    ```bash
    uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    ```

## API Documentation

Once the server is running, you can access the interactive API documentation at:

- **Swagger UI**: [http://127.0.0.1:8000/api/docs](http://127.0.0.1:8000/api/docs)
- **OpenAPI JSON**: [http://127.0.0.1:8000/api/openapi.json](http://127.0.0.1:8000/api/openapi.json)

## Testing

Run the test suite using `pytest`:

```bash
uv run pytest
```
