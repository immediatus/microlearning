# AI Agent Instructions for MicroLearning Platform

## Project Overview
You are working on an **AI-powered microlearning platform** for STEM education targeting students aged 12-15. The platform features TikTok-style educational videos (45-90 seconds) with interactive quiz validation.

## Critical Project Context

### Primary Goals
1. **Student-first experience** - Optimize everything for mobile learning
2. **AI-powered content generation** - Minimize human oversight with quality automation
3. **Cost-conscious development** - Track and optimize all AI service usage
4. **Scalable architecture** - Support 100,000+ concurrent students

### Technology Stack
- **Backend**: Python + FastAPI + LangGraph + PostgreSQL + Redis
- **Frontend**: React Native (mobile) + React (web dashboard)
- **AI Services**: OpenAI GPT-4, DALL-E 3, ElevenLabs, RunwayML, others with fallbacks
- **Infrastructure**: Docker + Kubernetes + AWS/GCP

## Development Principles (MANDATORY)

### 1. Documentation-First Development
- **EVERY change must include documentation updates**
- **EVERY technical decision requires an ADR** (Architecture Decision Record)
- **EVERY AI operation must be cost-tracked and approved**
- **NO code without comprehensive inline documentation**

### 2. Quality Standards
- **Minimum 80% test coverage** for all new code
- **All Python code must pass**: black, isort, ruff, mypy
- **All TypeScript code must pass**: prettier, eslint, type checking
- **Security scan clean** (bandit for Python)

### 3. AI Service Usage
- **Request approval for operations >$1** using cost tracker
- **Implement caching** to prevent redundant AI calls
- **Use fallback services** when primary services fail
- **Document all AI service costs** in your PRs

### 4. Mobile-First Performance
- **Video load time**: <2 seconds on 4G
- **Quiz response time**: <100ms
- **App launch time**: <3 seconds
- **Memory usage**: <150MB during active use

## Required Workflow

### Before Starting Any Task
1. **Read all documentation** in `/docs` folder
2. **Review existing code patterns** in similar modules
3. **Estimate costs** for any AI service usage
4. **Request approval** if costs >$1 using cost tracker
5. **Create feature branch** with descriptive name

### During Development
1. **Follow established patterns** - check existing code first
2. **Write tests concurrently** with implementation
3. **Update documentation** as you code
4. **Commit frequently** with descriptive messages
5. **Run quality checks** before requesting review

### Before Submitting PR
1. **Run full test suite**: `make test`
2. **Check code quality**: `make lint`
3. **Update documentation**: relevant `.md` files
4. **Estimate cost impact**: include in PR description
5. **Self-review code** using provided checklist

## Project Structure Guide

```
microlearning/
├── app/                    # FastAPI backend
│   ├── api/               # API routes (/api/v1/...)
│   ├── models/            # Database models (SQLAlchemy)
│   ├── services/          # Business logic
│   │   ├── ai_service_manager.py    # AI service integration
│   │   ├── content_cache.py         # Content caching system
│   │   └── cost_tracker.py          # AI cost tracking
│   ├── core/              # Core configurations
│   └── main.py            # Application entry point
├── mobile/                # React Native student app
├── creator-dashboard/     # React web app for creators
├── docs/                  # All documentation
│   ├── decisions/         # Architecture Decision Records
│   └── *.md              # Technical documentation
└── tests/                 # Test files
```

## Key Integration Points

### AI Service Integration
```python
from app.services.ai_service_manager import ai_service_manager, ServiceType, ServiceTier
from app.services.cost_tracker import request_ai_approval

# Always request approval first for AI operations
approval = await request_ai_approval(
    creator_id=creator_id,
    service_type=ServiceType.TEXT_GENERATION,
    model="gpt-4",
    operation_params={"prompt": prompt, "max_tokens": 500}
)

if approval["approval_status"] == "approved":
    result = await ai_service_manager.generate_content(
        ServiceType.TEXT_GENERATION,
        ServiceTier.PREMIUM,
        prompt=prompt
    )
```

### Database Models
```python
# Use existing models in app/models/
from app.models.student import Student
from app.models.content import LearningVideo, ContentProject
from app.models.quiz import QuizResponse

# Always use async database sessions
from app.core.database import get_db
async with get_db() as db:
    # Your database operations
```

### Content Caching
```python
from app.services.content_cache import content_cache, CacheType

# Always check cache first
cached_result = await content_cache.get_cached_content(
    CacheType.SCRIPT, 
    {"concept": concept, "age_group": age_group}
)

if not cached_result:
    # Generate new content
    result = await generate_content(...)
    # Cache the result
    await content_cache.cache_content(CacheType.SCRIPT, params, result)
```

## Current Development Priorities

### Phase 1: Core Backend (In Progress)
1. **Complete database models** and migrations
2. **Implement AI content generation pipeline** with LangGraph
3. **Add API endpoints** for student and creator interfaces
4. **Set up comprehensive testing** with mocking for AI services

### Phase 2: Student Mobile App
1. **Video player component** optimized for 9:16 content
2. **Quiz interface** with touch interactions
3. **Progress tracking** and achievement system
4. **Offline support** for downloaded content

### Phase 3: Creator Dashboard
1. **AI content generation interface** with approval workflow
2. **Content review and editing** tools
3. **Analytics dashboard** for content performance
4. **Budget management** for AI service usage

## Common Tasks You'll Work On

### 1. API Endpoint Development
- Student authentication and profile management
- Content delivery APIs with caching
- Quiz submission and scoring
- Progress tracking and analytics

### 2. AI Content Generation
- Script generation for educational videos
- Quiz question generation and validation
- Image generation for visual aids
- Voice synthesis for narration

### 3. Database Operations
- User progress tracking
- Content metadata management
- Cost tracking for AI operations
- Caching strategies for performance

### 4. Testing and Quality Assurance
- Unit tests for all business logic
- Integration tests for API endpoints
- Performance tests for mobile optimization
- Security tests for user data protection

## Issue Labels and Workflow

When you see GitHub issues with the `jules` label:
1. **Read the full issue description** and acceptance criteria
2. **Ask clarifying questions** in issue comments if needed
3. **Estimate cost impact** for any AI service usage
4. **Create implementation plan** with milestones
5. **Start development** following the workflow above

## Emergency Contacts and Escalation

If you encounter:
- **Budget/cost concerns**: Escalate immediately, don't proceed
- **Security vulnerabilities**: Flag in PR and notify team
- **Performance issues**: Include benchmarks in PR description
- **Integration failures**: Document error details for debugging

## Success Metrics for Your Contributions

### Code Quality
- **Test Coverage**: >80% for all new code
- **Documentation**: Complete API docs and inline comments
- **Performance**: Meet mobile-first benchmarks
- **Security**: Clean security scans

### AI Integration
- **Cost Efficiency**: Minimize AI service usage through caching
- **Quality**: >90% approval rate for generated content
- **Reliability**: Proper fallback handling for service failures
- **Transparency**: Clear cost tracking and approval workflows

## Remember
- **Students come first** - every decision should optimize their learning experience
- **Document everything** - future developers (human and AI) need context
- **Be cost-conscious** - AI services are powerful but expensive
- **Ask questions** - when in doubt, clarify requirements before implementing

---

**This project aims to revolutionize STEM education for millions of students. Your contributions directly impact young learners' educational journey. Code with care, document thoroughly, and optimize relentlessly.**