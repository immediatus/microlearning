#!/bin/bash

# Post-start script for dev container
set -e

echo "🔄 Starting development services..."

# Activate virtual environment
source /workspace/.venv/bin/activate

# Check database connection
echo "🔍 Checking database connection..."
python -c "
import asyncio
from app.core.database import check_database_connection
result = asyncio.run(check_database_connection())
print('✅ Database connection OK!' if result else '❌ Database connection failed!')
"

# Check Redis connection
echo "🔍 Checking Redis connection..."
redis-cli -h redis ping && echo "✅ Redis connection OK!" || echo "❌ Redis connection failed!"

echo "🎉 Development environment is ready!"