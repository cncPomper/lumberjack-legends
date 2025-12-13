# Lumberjack Legends Frontend

This is the frontend application for Lumberjack Legends, built with React, TypeScript, Vite, and Tailwind CSS.

## Features

- **Authentication**: User signup, login, and session management
- **Game Play**: Interactive lumberjack chopping game with scoring
- **Leaderboard**: Real-time leaderboard with rankings
- **Responsive Design**: Works on desktop and mobile devices

## Setup

This project uses npm or bun for dependency management.

1. **Install dependencies**:
   ```bash
   npm install
   # or
   bun install
   ```

2. **Configure backend URL** (optional):
   The `.env` file is already configured with:
   ```
   VITE_API_BASE_URL=http://127.0.0.1:8000/api
   ```

3. **Start the development server**:
   ```bash
   npm run dev
   # or
   bun run dev
   ```

The app will be available at http://localhost:8080

## Backend Integration

The frontend connects to the FastAPI backend. Make sure the backend is running before starting the frontend:

```bash
# In the backend directory
cd ../backend
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API endpoints are prefixed with `/api`:
- Authentication: `/api/auth/*`
- Leaderboard: `/api/leaderboard`
- Game Sessions: `/api/game/*`

## Testing

Run the test suite using Vitest:

```bash
npm test
# or
bun test
```

## Project Structure

- `src/components/` - React components
- `src/contexts/` - React context providers (Auth, Game)
- `src/pages/` - Page components
- `src/services/` - API service layer
  - `api.ts` - Real backend API integration
  - `mockApi.ts` - Mock API for testing
- `src/lib/` - Utility functions

## Environment Variables

- `VITE_API_BASE_URL` - Backend API base URL (default: `http://127.0.0.1:8000/api`)
