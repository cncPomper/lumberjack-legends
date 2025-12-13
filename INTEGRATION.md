# Frontend-Backend Integration Summary

This document summarizes the integration work completed to connect the React frontend with the FastAPI backend.

## Changes Made

### 1. Created Real API Service (`frontend/src/services/api.ts`)
- Implemented HTTP fetch calls to all backend endpoints
- JWT token management using localStorage
- Proper date parsing for API responses
- Error handling for network failures
- Follows OpenAPI specification exactly

### 2. Environment Configuration
- Created `frontend/.env` with `VITE_API_BASE_URL=http://127.0.0.1:8000/api`
- Backend serves API at `/api/*` prefix
- CORS configured in backend to allow frontend origin

### 3. Updated Context Providers

#### AuthContext (`frontend/src/contexts/AuthContext.tsx`)
- Changed import from `mockApi` to `api`
- Token persistence handled by api.ts
- Automatic session restoration on page load

#### GameContext (`frontend/src/contexts/GameContext.tsx`)
- Changed import from `mockApi` to `api`
- Added session ID tracking for backend game sessions
- Calls `api.game.startSession()` when game starts
- Calls `api.game.endSession()` when game ends with duration tracking

### 4. Updated Pages
- `frontend/src/pages/LeaderboardPage.tsx` - Uses real API
- `frontend/src/pages/Index.tsx` - Uses real API

### 5. Testing
- Kept `mockApi.ts` for unit tests
- Tests use mock API directly (no HTTP calls)
- Integration tests can be added later

### 6. Documentation
- Created `frontend/README.md` - Frontend setup guide
- Created `backend/README.md` - Backend setup guide  
- Updated root `README.md` - Complete project overview
- Created `.gitignore` files for both frontend and backend

## API Integration Details

### Authentication Flow
1. User logs in via `api.auth.login(email, password)`
2. Backend returns JWT token
3. Token stored in localStorage
4. Token automatically included in Authorization header for authenticated requests
5. Session restored on page refresh via `api.auth.getCurrentUser()`

### Game Session Flow
1. User starts game → `api.game.startSession()` creates session in backend
2. User plays game (chops trees, scores points)
3. Game ends → `api.game.endSession(sessionId, score, chops, duration)`
4. Backend updates user stats and leaderboard

### Leaderboard
- Public endpoint (no auth required): `GET /api/leaderboard`
- Submit score (requires auth): `POST /api/leaderboard`
- Returns top 10 players by default (configurable via `?limit=N`)

## Testing the Integration

### Start Backend
```bash
cd backend
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Start Frontend
```bash
cd frontend
npm run dev
```

### Test with curl
```bash
# Get leaderboard
curl http://127.0.0.1:8000/api/leaderboard?limit=3

# Login
curl -X POST http://127.0.0.1:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "king@forest.com", "password": "password"}'
```

### Test Accounts
All accounts use password: `password`
- paul@legends.com (5000 points)
- king@forest.com (2500 points)
- jill@forest.com (2400 points)

## Architecture

```
┌─────────────┐         HTTP/JSON          ┌──────────────┐
│             │  ──────────────────────►   │              │
│   React     │                            │   FastAPI    │
│   Frontend  │  ◄──────────────────────   │   Backend    │
│  (Port 8080)│     JWT Auth + Data        │  (Port 8000) │
└─────────────┘                            └──────────────┘
      │                                            │
      │                                            │
      ▼                                            ▼
 localStorage                                  Mock DB
 (JWT Token)                              (In-Memory)
```

## Next Steps

Potential improvements:
1. Add request/response interceptors for better error handling
2. Implement refresh token mechanism
3. Add loading states and retry logic
4. Replace mock database with real database (PostgreSQL/MongoDB)
5. Add WebSocket support for real-time leaderboard updates
6. Implement rate limiting and request throttling
