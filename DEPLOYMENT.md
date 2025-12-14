# Deployment Guide

This guide covers deploying Lumberjack Legends using the combined frontend + backend container.

## Architecture

The production deployment uses a single container that runs:
- **Nginx** on port 80 (serves frontend and proxies API requests)
- **FastAPI backend** on port 8000 (internal)
- **PostgreSQL** in a separate container

## Quick Start

### 1. Set Up Environment Variables

```bash
# Copy the example environment file
cp .env.production.example .env

# Edit .env with your production values
nano .env
```

**Important:** Change these values in production:
- `POSTGRES_PASSWORD`: Strong database password
- `SECRET_KEY`: Long random string for JWT signing (generate with: `openssl rand -hex 32`)

### 2. Build and Deploy

```bash
# Build and start all services
docker-compose -f docker-compose.prod.yml up -d --build

# Check logs
docker-compose -f docker-compose.prod.yml logs -f

# Check status
docker-compose -f docker-compose.prod.yml ps
```

### 3. Initialize Database

The database will be automatically initialized on first startup. To manually run migrations or seed data:

```bash
# Access the app container
docker exec -it lumberjack-app-prod bash

# Run database initialization
cd /app/backend
uv run python -m app.seed
```

### 4. Access the Application

Open your browser to: `http://localhost` (or your server's IP/domain)

## Container Structure

The combined container includes:
```
/app/backend/              # FastAPI application
/usr/share/nginx/html/     # Built frontend static files
/etc/nginx/conf.d/         # Nginx configuration
```

## Monitoring

### View Logs

```bash
# All services
docker-compose -f docker-compose.prod.yml logs -f

# Specific service
docker-compose -f docker-compose.prod.yml logs -f app
docker-compose -f docker-compose.prod.yml logs -f postgres
```

### Check Health

```bash
# App health check
curl http://localhost/api/health

# Container health
docker ps
```

## Scaling

To increase backend workers for better performance:

Edit `Dockerfile` and change the uvicorn command:
```bash
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Backup Database

```bash
# Backup
docker exec lumberjack-db-prod pg_dump -U lumberjack lumberjack_legends > backup.sql

# Restore
cat backup.sql | docker exec -i lumberjack-db-prod psql -U lumberjack lumberjack_legends
```

## SSL/HTTPS Setup

For production with SSL, use a reverse proxy like:
- **Caddy** (automatic HTTPS)
- **Traefik** (automatic HTTPS)
- **Nginx** with Let's Encrypt

Example with Caddy:
```
your-domain.com {
    reverse_proxy localhost:80
}
```

## Updating

```bash
# Pull latest code
git pull

# Rebuild and restart
docker-compose -f docker-compose.prod.yml up -d --build

# Remove old images
docker image prune -f
```

## Troubleshooting

### Backend not responding
```bash
# Check if backend process is running in container
docker exec lumberjack-app-prod ps aux | grep uvicorn

# Check backend logs
docker exec lumberjack-app-prod tail -f /var/log/nginx/error.log
```

### Database connection issues
```bash
# Check database is ready
docker exec lumberjack-db-prod pg_isready -U lumberjack

# Verify connection from app container
docker exec lumberjack-app-prod nc -zv postgres 5432
```

### Port conflicts
If port 80 is already in use, modify `docker-compose.prod.yml`:
```yaml
ports:
  - "8080:80"  # Change external port
```

## Stopping Services

```bash
# Stop all services
docker-compose -f docker-compose.prod.yml down

# Stop and remove volumes (WARNING: deletes database)
docker-compose -f docker-compose.prod.yml down -v
```

## Production Checklist

- [ ] Changed `POSTGRES_PASSWORD` to a strong password
- [ ] Generated and set a secure `SECRET_KEY`
- [ ] Configured firewall to allow only port 80/443
- [ ] Set up SSL/HTTPS with reverse proxy
- [ ] Configured database backups
- [ ] Set up log rotation
- [ ] Configured monitoring/alerting
- [ ] Tested backup restoration procedure
- [ ] Documented server access credentials securely
