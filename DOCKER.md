# Docker Setup Guide

This guide explains how to run Lumberjack Legends using Docker Compose.

## Architecture

The application consists of three services:

1. **PostgreSQL Database** - Stores user data, game sessions, and leaderboards
2. **FastAPI Backend** - REST API server
3. **Nginx + React Frontend** - Static frontend served by Nginx with API proxy

## Prerequisites

- Docker (version 20.10 or higher)
- Docker Compose (version 2.0 or higher)

## Quick Start

1. **Clone the repository** (if not already done)

2. **Start all services**:
   ```bash
   docker-compose up -d
   ```

   This will:
   - Pull the PostgreSQL image
   - Build the backend and frontend images
   - Start all services in detached mode

3. **Access the application**:
   - Frontend: http://localhost
   - Backend API: http://localhost/api
   - API Docs: http://localhost/api/docs
   - Direct Backend (dev): http://localhost:8000

## Environment Variables

You can customize the setup using a `.env` file in the root directory:

```env
# Database
POSTGRES_USER=lumberjack
POSTGRES_PASSWORD=lumberjack_password
POSTGRES_DB=lumberjack_legends

# Backend
SECRET_KEY=your_super_secret_key_here
```

## Development Mode

The docker-compose.yml is configured for development with:
- Hot reload enabled for backend (volume mount)
- PostgreSQL exposed on port 5432 for direct access
- Backend exposed on port 8000 for direct API access

## Useful Commands

### View logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres
```

### Stop services
```bash
docker-compose down
```

### Stop and remove volumes (⚠️ deletes database data)
```bash
docker-compose down -v
```

### Rebuild after code changes
```bash
# Rebuild all services
docker-compose up -d --build

# Rebuild specific service
docker-compose up -d --build backend
```

### Access database
```bash
docker-compose exec postgres psql -U lumberjack -d lumberjack_legends
```

### Access backend shell
```bash
docker-compose exec backend bash
```

## Database Migrations

The backend automatically creates tables on startup. For production, you should use proper migrations:

```bash
# Run migrations (when implemented)
docker-compose exec backend alembic upgrade head
```

## Production Deployment

For production, you should:

1. **Update environment variables**:
   - Use strong passwords
   - Generate a secure SECRET_KEY
   - Set proper CORS origins

2. **Remove development features**:
   - Disable backend hot reload
   - Remove volume mounts
   - Use production build for frontend

3. **Add SSL/TLS**:
   - Configure nginx with SSL certificates
   - Use a reverse proxy like Traefik or Caddy

4. **Scale services** (if needed):
   ```bash
   docker-compose up -d --scale backend=3
   ```

## Troubleshooting

### Backend fails to start
- Check if PostgreSQL is healthy: `docker-compose ps`
- Wait for database initialization to complete
- Check logs: `docker-compose logs postgres`

### Frontend shows connection errors
- Ensure backend is running: `docker-compose ps backend`
- Check backend logs: `docker-compose logs backend`
- Verify API proxy in nginx.conf

### Database connection issues
- Verify DATABASE_URL in backend service
- Check PostgreSQL health: `docker-compose exec postgres pg_isready`

## Network Architecture

All services communicate through a bridge network `lumberjack-network`:
- Frontend → Backend: via nginx proxy at `/api`
- Backend → PostgreSQL: via hostname `postgres` on port 5432

## Ports

- `80` - Frontend (Nginx)
- `8000` - Backend API (development)
- `5432` - PostgreSQL (development)
