# Multi-stage build for combined frontend + backend deployment

# Stage 1: Build frontend
FROM node:20-alpine AS frontend-build

WORKDIR /app/frontend

# Copy frontend package files
COPY frontend/package.json frontend/bun.lockb ./

# Install frontend dependencies
RUN npm install

# Copy frontend source code
COPY frontend/ ./

# Build the frontend application
RUN npm run build

# Stage 2: Final production image with backend + frontend
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies (nginx for serving frontend, postgresql-client for backend)
RUN apt-get update && apt-get install -y \
    nginx \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy backend files
COPY backend/pyproject.toml ./backend/
COPY backend/ ./backend/

# Install uv and Python dependencies
RUN pip install uv && \
    cd backend && \
    uv pip install --system -r pyproject.toml

# Copy built frontend from frontend-build stage
COPY --from=frontend-build /app/frontend/dist /usr/share/nginx/html

# Copy nginx configuration (use combined config for single-container deployment)
COPY nginx.combined.conf /etc/nginx/conf.d/default.conf

# Remove default nginx site
RUN rm -f /etc/nginx/sites-enabled/default

# Create a startup script
RUN echo '#!/bin/bash\n\
set -e\n\
\n\
# Start nginx in the background\n\
nginx\n\
\n\
# Start the FastAPI backend\n\
cd /app/backend\n\
exec uvicorn app.main:app --host 0.0.0.0 --port 8000\n\
' > /app/start.sh && chmod +x /app/start.sh

# Expose ports (80 for nginx/frontend, 8000 for backend)
EXPOSE 80 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:80/ || exit 1

# Start both services
CMD ["/app/start.sh"]
