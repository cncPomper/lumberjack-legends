#!/bin/bash
# Quick test script for the combined container

set -e

echo "🧪 Testing combined container..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  Creating .env file from template..."
    cp .env.production.example .env
    echo "✏️  Please edit .env with proper values before production deployment"
fi

echo ""
echo "🏗️  Building production containers..."
docker-compose -f docker-compose.prod.yml build

echo ""
echo "🚀 Starting services..."
docker-compose -f docker-compose.prod.yml up -d

echo ""
echo "⏳ Waiting for services to be ready..."
sleep 10

echo ""
echo "🔍 Checking service health..."

# Check if containers are running
if docker ps | grep -q lumberjack-app-prod; then
    echo "✅ App container is running"
else
    echo "❌ App container is not running"
    docker-compose -f docker-compose.prod.yml logs app
    exit 1
fi

if docker ps | grep -q lumberjack-db-prod; then
    echo "✅ Database container is running"
else
    echo "❌ Database container is not running"
    docker-compose -f docker-compose.prod.yml logs postgres
    exit 1
fi

echo ""
echo "🌐 Testing HTTP endpoints..."

# Test frontend
if curl -f -s http://localhost/ > /dev/null; then
    echo "✅ Frontend is accessible"
else
    echo "❌ Frontend is not accessible"
    exit 1
fi

# Test backend API
if curl -f -s http://localhost/api/docs > /dev/null; then
    echo "✅ Backend API is accessible"
else
    echo "❌ Backend API is not accessible"
    exit 1
fi

echo ""
echo "📊 Container status:"
docker-compose -f docker-compose.prod.yml ps

echo ""
echo "✅ All tests passed!"
echo ""
echo "📝 Next steps:"
echo "  - Access the app: http://localhost"
echo "  - View logs: docker-compose -f docker-compose.prod.yml logs -f"
echo "  - Stop services: docker-compose -f docker-compose.prod.yml down"
