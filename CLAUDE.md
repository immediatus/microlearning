# Claude Code Project Configuration

## Project Overview
MicroLearning Platform - An AI-powered microlearning platform for STEM education targeting students aged 12-15, featuring TikTok-style educational videos with interactive quiz validation.

## Technology Stack
- **Backend**: Python + FastAPI + LangGraph
- **Frontend**: React Native + Expo (mobile), React (web)
- **Database**: PostgreSQL + Redis
- **AI Services**: OpenAI GPT-4, DALL-E 3, ElevenLabs, RunwayML
- **Infrastructure**: AWS/GCP + Docker + Kubernetes

## Development Commands

### Backend Setup
```bash
# Install Python dependencies
pip install -r requirements.txt

# Start development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run database migrations
alembic upgrade head

# Start Celery worker for AI processing
celery -A app.celery worker --loglevel=info

# Run tests
pytest tests/ -v

# Type checking
mypy app/

# Code formatting
black app/ tests/
isort app/ tests/

# Linting
ruff app/ tests/
```

### Mobile App Setup
```bash
# Install dependencies
npm install

# Start development server
npx expo start

# Run on iOS simulator
npx expo run:ios

# Run on Android emulator
npx expo run:android

# Build for production
eas build --platform all

# Run tests
npm test

# Type checking
npx tsc --noEmit

# Linting
npx eslint . --ext .ts,.tsx

# Code formatting
npx prettier --write .
```

### Creator Web App Setup
```bash
# Navigate to web app directory
cd creator-dashboard

# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Run tests
npm test

# Type checking
npm run type-check

# Linting and formatting
npm run lint
npm run format
```

### Infrastructure Commands
```bash
# Start local development environment
docker-compose up -d

# Stop local environment
docker-compose down

# Build and push Docker images
docker build -t microlearning/api:latest .
docker push microlearning/api:latest

# Deploy to Kubernetes
kubectl apply -f k8s/

# Check deployment status
kubectl get pods -n microlearning

# View logs
kubectl logs -f deployment/microlearning-api -n microlearning
```

## Project Structure
```
microlearning/
├── app/                    # FastAPI backend
│   ├── api/               # API routes
│   ├── core/              # Core configurations
│   ├── models/            # Database models
│   ├── services/          # Business logic
│   ├── ai/                # AI content generation
│   └── main.py            # Application entry point
├── mobile/                # React Native app
│   ├── src/
│   │   ├── components/    # Reusable components
│   │   ├── screens/       # App screens
│   │   ├── services/      # API services
│   │   └── utils/         # Utility functions
│   ├── app.json           # Expo configuration
│   └── package.json
├── creator-dashboard/     # React web app
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── pages/         # App pages
│   │   ├── hooks/         # Custom hooks
│   │   └── utils/         # Utility functions
│   └── package.json
├── docs/                  # Project documentation
├── k8s/                   # Kubernetes manifests
├── docker-compose.yml     # Local development
├── requirements.txt       # Python dependencies
└── README.md
```

## Environment Variables

### Backend (.env)
```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/microlearning
REDIS_URL=redis://localhost:6379

# AI Services
OPENAI_API_KEY=sk-...
ELEVENLABS_API_KEY=...
RUNWAY_API_KEY=...

# AWS/Storage
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
S3_BUCKET_NAME=microlearning-videos

# Application
SECRET_KEY=your-secret-key
DEBUG=True
ENVIRONMENT=development
```

### Mobile App (.env)
```bash
# API Configuration
API_BASE_URL=http://localhost:8000
WS_BASE_URL=ws://localhost:8000

# Analytics
AMPLITUDE_API_KEY=...

# Push Notifications
EXPO_PUSH_TOKEN=...
```

## Key Files to Monitor
- `app/ai/content_pipeline.py` - AI content generation workflow
- `mobile/src/components/VideoPlayer.tsx` - Core video player component
- `mobile/src/screens/QuizScreen.tsx` - Quiz interaction interface
- `app/api/routes/student.py` - Student API endpoints
- `app/services/content_generation.py` - Content generation service

## Common Development Tasks

### Adding New Quiz Types
1. Update `app/models/quiz.py` with new question types
2. Modify `mobile/src/components/QuizInterface.tsx` for new interactions
3. Update AI prompt in `app/ai/quiz_generator.py`
4. Add tests for new quiz functionality

### Creating New Video Templates
1. Add template configuration to `app/services/video_templates.py`
2. Update visual generation in `app/ai/visual_creator.py`
3. Test template with sample content
4. Add template preview to creator dashboard

### Optimizing Performance
1. Monitor API response times: `app/middleware/performance.py`
2. Check video load times: `mobile/src/services/video_cache.ts`
3. Optimize database queries: `app/models/` files
4. Review AI service usage and costs

## Testing Strategy
- **Unit Tests**: Individual component and service testing
- **Integration Tests**: API endpoint and workflow testing
- **E2E Tests**: Complete user journey testing
- **Performance Tests**: Load and stress testing
- **AI Content Tests**: Generated content quality validation

## Deployment Process
1. Run full test suite: `npm test && pytest`
2. Build production images: `docker build`
3. Deploy to staging: `kubectl apply -f k8s/staging/`
4. Run smoke tests and validation
5. Deploy to production: `kubectl apply -f k8s/production/`
6. Monitor deployment metrics and logs

## Troubleshooting

### Common Issues
- **Video loading slow**: Check CDN configuration and video compression
- **AI generation failures**: Verify API keys and service limits
- **Database connection issues**: Check connection string and network
- **Mobile app crashes**: Review error logs and memory usage
- **Quiz interactions not responsive**: Check touch target sizes and performance

### Debug Commands
```bash
# Check API health
curl http://localhost:8000/health

# View real-time logs
docker-compose logs -f api

# Monitor resource usage
kubectl top pods -n microlearning

# Test AI services
python -c "from app.ai.script_generator import generate_script; print(generate_script('photosynthesis', '12-15'))"
```

## Performance Targets
- API response time: <200ms for 95th percentile
- Video load time: <2 seconds on 4G
- Quiz response time: <100ms
- App launch time: <3 seconds
- Content generation: <5 minutes per video

---

*This file helps Claude Code understand the project structure and provides quick access to common development tasks.*