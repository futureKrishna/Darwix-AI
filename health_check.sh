#!/bin/bash
# Health check script for Docker container

set -e

# Check if the application is responding
echo "Checking application health..."

# Wait for the application to start
sleep 2

# Check health endpoint
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health || echo "000")

if [ "$response" = "200" ]; then
    echo "✅ Health check passed - Application is healthy"
    exit 0
else
    echo "❌ Health check failed - HTTP status: $response"
    exit 1
fi
