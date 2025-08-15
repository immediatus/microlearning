#!/bin/bash

# Post-create script for dev container setup
set -e

echo "🚀 Setting up MicroLearning Platform development environment..."

# Activate virtual environment
source /workspace/.venv/bin/activate

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Install pre-commit hooks
echo "🔧 Setting up pre-commit hooks..."
pre-commit install

# Set up environment file
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cat > .env << EOF
# Database
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/microlearning
REDIS_URL=redis://redis:6379

# Application
SECRET_KEY=your-super-secret-key-change-in-production
DEBUG=true
ENVIRONMENT=development

# AI Services (add your API keys)
OPENAI_API_KEY=your-openai-api-key-here
ELEVENLABS_API_KEY=your-elevenlabs-api-key-here

# AWS (for production)
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
S3_BUCKET_NAME=microlearning-videos

# Security
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
EOF
    echo "⚠️  Please update the .env file with your actual API keys!"
fi

# Wait for database to be ready
echo "⏳ Waiting for database to be ready..."
until pg_isready -h db -p 5432 -U postgres; do
    echo "Database is unavailable - sleeping"
    sleep 2
done
echo "✅ Database is ready!"

# Run database migrations
echo "🗄️  Setting up database..."
cd /workspace
python -c "
import asyncio
from app.core.database import create_tables
asyncio.run(create_tables())
print('Database tables created successfully!')
"

# Install Node.js dependencies for creator dashboard
if [ -d "creator-dashboard" ]; then
    echo "📦 Installing Node.js dependencies for creator dashboard..."
    cd creator-dashboard
    npm install
    cd ..
fi

# Install Node.js dependencies for mobile app
if [ -d "mobile" ]; then
    echo "📱 Installing Node.js dependencies for mobile app..."
    cd mobile
    npm install
    cd ..
fi

echo "✅ Development environment setup complete!"
echo ""
echo "🎯 Quick start commands:"
echo "  - Start backend: uvicorn app.main:app --reload --host 0.0.0.0"
echo "  - Start creator dashboard: cd creator-dashboard && npm run dev"
echo "  - Start mobile app: cd mobile && npx expo start"
echo "  - Run tests: pytest"
echo "  - Format code: black . && isort ."
echo ""
echo "🔗 Available services:"
echo "  - FastAPI docs: http://localhost:8000/docs"
echo "  - PgAdmin: http://localhost:5050 (admin@microlearning.com / admin)"
echo "  - Creator dashboard: http://localhost:3000"
echo ""