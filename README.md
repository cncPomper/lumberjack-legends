# Lumberjack Legends

A fast-paced lumberjack game with real-time leaderboards and user authentication.

## Project Structure

```
lumberjack-legends/
├── backend/          # FastAPI backend server
├── frontend/         # React + Vite frontend
├── docker-compose.yml # Docker setup
└── openapi.yaml      # API specification
```

## Quick Start

### Option 1: Deploy to Cloud (Render) ☁️

Deploy to Render with one-click:

```bash
./render-preflight.sh  # Check readiness
# Then go to dashboard.render.com and deploy via Blueprint
```

See [DEPLOY_RENDER.md](DEPLOY_RENDER.md) for complete cloud deployment guide.

**Cost**: Free tier available, or $14/month for production.

### Option 2: Self-Hosted Production (Docker)

Deploy both frontend and backend in a single container with PostgreSQL database:

```bash
# Quick test
./test-deployment.sh

# Or manually
cp .env.production.example .env
# Edit .env with your production values
docker-compose -f docker-compose.prod.yml up -d --build
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for complete self-hosted deployment guide.

### Option 2: Development with Docker

Run frontend and backend as separate containers (with hot-reload):

```bash
docker-compose up -d
```

Access the app at http://localhost

See [DOCKER.md](DOCKER.md) for detailed Docker development setup.

### Option 3: Local Development

### Run Both Frontend and Backend (Recommended)

```bash
npm install      # Install concurrently (first time only)
npm run dev      # Start both backend and frontend
```

This will start:
- **Backend** at http://127.0.0.1:8000 (API docs: http://127.0.0.1:8000/api/docs)
- **Frontend** at http://localhost:8080

### Or Run Separately

#### 1. Start the Backend

```bash
cd backend
make dev        # Using Makefile
# OR
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 2. Start the Frontend

```bash
cd frontend
npm install  # or bun install (first time only)
npm run dev  # or bun run dev
```

## Features

- **User Authentication**: JWT-based signup and login
- **Game Sessions**: Secure game session management to prevent cheating
- **Real-time Leaderboard**: Global rankings updated after each game
- **Responsive Design**: Works on desktop and mobile
- **Python Code Execution**: Run Python code in the browser using Pyodide (WASM)
- **25 Pre-populated Users**: Test accounts with various scores

## Test Accounts

All test accounts use the password: `password`

- paul@legends.com - Top player (5000 points)
- king@forest.com - High scorer (2500 points)
- redwood@rookie.com - New player (50 points)

See `backend/app/db.py` for the full list of test users.

## API Endpoints

All API endpoints are prefixed with `/api`:

### Authentication
- `POST /api/auth/signup` - Create new user
- `POST /api/auth/login` - Login
- `POST /api/auth/logout` - Logout
- `GET /api/auth/me` - Get current user
- `PATCH /api/auth/profile` - Update profile

### Leaderboard
- `GET /api/leaderboard` - Get top players
- `POST /api/leaderboard` - Submit score

### Game
- `POST /api/game/session` - Start game session
- `POST /api/game/session/{id}/end` - End game session
- `GET /api/game/stats` - Get user stats

## Development

### Backend
- Python 3.12+
- FastAPI framework
- uv for dependency management
- In-memory mock database (for now)

### Frontend
- React 18
- TypeScript
- Vite for build tooling
- Tailwind CSS for styling
- shadcn-ui components

## Testing

### Backend Tests
```bash
cd backend
uv run pytest
```

### Frontend Tests
```bash
cd frontend
npm test  # or bun test
```

## Architecture

The application follows a client-server architecture:

1. **Frontend** makes HTTP requests to the backend API
2. **Backend** handles authentication, game logic, and data persistence
3. **OpenAPI spec** defines the contract between frontend and backend

Authentication uses JWT tokens stored in localStorage on the frontend.

## Contributing

See `AGENTS.md` for guidelines on backend development.
